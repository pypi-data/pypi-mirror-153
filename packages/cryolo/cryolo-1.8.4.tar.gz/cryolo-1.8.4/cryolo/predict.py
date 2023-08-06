"""
Prediction script crYOLO
"""

# ! /usr/bin/env python
#
# COPYRIGHT
#
# All contributions by Ngoc Anh Huyn:
# Copyright (c) 2017, Ngoc Anh Huyn.
# All rights reserved.
#
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#
from __future__ import print_function
import multiprocessing
import time
import argparse
import os
import sys
import json
import numpy as np
from cryolo.utils import BoundBox
from lineenhancer import line_enhancer, maskstackcreator
from . import CoordsIO
from . import imagereader
from . import utils
from . import filament_tracer
from . import config_tools
from gooey import Gooey, GooeyParser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
try:
    os.environ["CUDA_VISIBLE_DEVICES"]
except KeyError:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"


ARGPARSER = None
MONITOR=False
filament_tracers = []


def create_parser(parser, use_gooey=True):
    """

    :param parser: Parser where the subgroups are added
    :param use_gooey: ture if gooey is used
    :return:
    """

    required_group = parser.add_argument_group(
        "Required arguments", "These options are mandatory to run crYOLO prediction"
    )
    args = ["-c", "--conf"]
    kwargs = {
        "help": "Path to the crYOLO configuration file.",
        "required": True,
        "gooey_options": {
            "validator": {
                "test": 'user_input.endswith("json")',
                "message": "File has to end with .json!",
            },
            "wildcard": "*.json",
        },
    }

    if use_gooey:
        kwargs["widget"] = "FileChooser"
    required_group.add_argument(*args, **kwargs)

    args = ["-w", "--weights"]
    kwargs = {
        "help": "Path to the trained model. It can either be a model that you trained from scratch, a refined model or a general model.",
        "required": True,
        "gooey_options": {
            "validator": {
                "test": 'user_input.endswith("h5")',
                "message": "File has to end with .h5!",
            },
            "wildcard": "*.h5",
        },
    }

    if use_gooey:
        kwargs["widget"] = "FileChooser"
    required_group.add_argument(*args, **kwargs)

    args = ["-i", "--input"]
    kwargs = {
        "nargs": "+",
        "help": "Path to one or multiple image folders / images (only directories in GUI).",
        "required": True,
    }
    if use_gooey:
        kwargs["widget"] = "DirChooser"
    required_group.add_argument(*args, **kwargs)

    args = ["-o", "--output"]
    kwargs = {
        "help": "Path to the output folder. All particle coordinates will be written there.",
        "required": True,
    }
    if use_gooey:
        kwargs["widget"] = "DirChooser"

    required_group.add_argument(*args, **kwargs)

    optional_group = parser.add_argument_group(
        "Optional arguments", "Optional arguments for crYOLO"
    )

    optional_group.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.3,
        help="Confidence threshold. Have to be between 0 and 1. The higher, the more conservative.",
        gooey_options={
            "validator": {
                "test": "0.0 <= float(user_input) <= 1.0",
                "message": "Must be between 0.0 and 1.0",
            }
        },
    )

    optional_group.add_argument(
        "-g",
        "--gpu",
        default="",
        # type=int,
        nargs="+",
        help="Specify which gpu(s) should be used. Multiple GPUs are separated by a whitespace. If not defined otherwise by your system, it will use GPU 0 by default.",
    )

    optional_group.add_argument(
        "-d",
        "--distance",
        default=0,
        type=int,
        help="Particles with a distance less than this value (in pixel) will be removed. This option should not be used in filament mode.",
    )

    optional_group.add_argument(
        "--minsize",
        type=int,
        help="Particles with a estimated diameter less than this value (in pixel) will be removed. This option typically is only useful for the general model.",
    )

    optional_group.add_argument(
        "--maxsize",
        type=int,
        help="Particles with a estimated diameter greather than this value (in pixel) will be removed.  This option typically is only useful for the general model.",
    )

    optional_group.add_argument(
        "-pbs",
        "--prediction_batch_size",
        default=3,
        type=int,
        help="How many images should be predicted in one batch. Smaller values might resolve memory issues.",
    )

    optional_group.add_argument(
        "--gpu_fraction",
        type=float,
        default=1.0,
        help="Specify the fraction of memory per GPU used by crYOLO during prediction. Only values between 0.0 and 1.0 are allowed.",
        gooey_options={
            "validator": {
                "test": "0.0 <= float(user_input) <= 1.0",
                "message": "Must be between 0.0 and 1.0",
            }
        },
    )

    optional_group.add_argument(
        "-nc",
        "--num_cpu",
        type=int,
        default=-1,
        help="Number of CPUs used during filtering / filament tracing. By default it will use all of the available CPUs.",
    )

    optional_group.add_argument(
        "--norm_margin",
        type=float,
        default=0.0,
        help="Relative margin size for normalization.",
        gooey_options={
            "validator": {
                "test": "0.0 <= float(user_input) <= 1.0",
                "message": "Must be between 0.0 and 1.0",
            }
        },
    )

    optional_group.add_argument(
        "--monitor",
        action="store_true",
        help='When this option is activated, crYOLO will monitor your input folder. This especially useful for automation purposes. You can stop the monitor mode by writing an empty file with the name "stop.cryolo" in the input directory.',
    )

    optional_group.add_argument(
        "--otf",
        action="store_true",
        default=False,
        help="On the fly filtering. Filtered micrographs will not be written to disk. Might be slower",
    )

    optional_group.add_argument(
        "--cleanup",
        action="store_true",
        default=False,
        help="If true, it will delete the filtered images after training is done."
    )

    optional_group.add_argument(
        "--skip",
        action="store_true",
        default=False,
        help="If true, it will skip images that were already picked."
    )

    filament_group = parser.add_argument_group(
        "Filament options",
        "These options are only relevant if you want to use the filament mode.",
    )

    filament_group.add_argument(
        "--filament", action="store_true", help="Activate filament mode"
    )

    filament_group.add_argument(
        "-bd",
        "--box_distance",
        default=None,
        type=int,
        help="Distance in pixel between two boxes.",
    )

    filament_group.add_argument(
        "-mn",
        "--minimum_number_boxes",
        default=None,
        type=int,
        help="Minimum number of boxes per filament.",
    )

    filament_group.add_argument(
        "-sm",
        "--straightness_method",
        default="LINE_STRAIGHTNESS",
        help="Method to measure the straightness of a line. LINE_STRAIGHTNESS divides the length "
             "from start to end by the accumulated length between adjacent boxes. RMS calculates the "
             "root mean squared deviation of the line points to line given by start and the endpoint "
             "of the filament. Adjust the straightness_threshold accordingly!",
        choices=["NONE", "LINE_STRAIGHTNESS", "RMSD"],
    )

    filament_group.add_argument(
        "-st",
        "--straightness_threshold",
        default=0.95,
        type=float,
        help="Threshold value for the straightness method. The default value works good for LINE_STRAIGHTNESS. Lines with a LINE_STRAIGHTNESS lower than this threshold get splitted. For RMSD, lines with a RMSD higher than this threshold will be splitted. A good value for RMSD is 20 percent of your filament width.",
    )

    filament_group.add_argument(
        "-sr",
        "--search_range_factor",
        type=float,
        default=1.41,
        help="The search range for connecting boxes is the box size times this factor.",
    )

    filament_group.add_argument(
        "-ad",
        "--angle_delta",
        type=float,
        default=10,
        help="Angle delta in degree. This value is good more or less straight filaments. More curvy filaments might require values around 20.",
    )

    filament_group.add_argument(
        "--directional_method",
        default="PREDICTED",
        help="",
        choices=["PREDICTED", "CONVOLUTION"],
    )

    filament_group.add_argument(
        "-fw",
        "--filament_width",
        default=None,
        type=int,
        help="(OPTIONAL) Filament width (in pixel). You only need to provide this information when you use the"
             "directional_method \"CONVOLUTION\".",
    )

    filament_group.add_argument(
        "-mw",
        "--mask_width",
        default=100,
        type=int,
        help="(OPTIONAL) Mask width (in pixel). A Gaussian filter mask is used to estimate the direction of the filaments. This parameter defines how elongated the mask is. The default value typically don't has to be changed. It is only used when you use the directional_method \"CONVOLUTION\".",
    )

    filament_group.add_argument(
        "--nosplit",
        action="store_true",
        help="(DEPRECATED) The filament mode does not split to curved filaments. It is deprecated, you can set straightness_method to None instead.",
    )

    filament_group.add_argument(
        "--nomerging",
        action="store_true",
        help="The filament mode does not merge filaments",
    )

    tomo_group = parser.add_argument_group(
        "Tomography options",
        "These options are only relevant if you want to pick tomograms",
    )

    tomo_group.add_argument(
        "--tomogram", action="store_true", help="Activate tomography picking mode."
    )

    tomo_group.add_argument(
        "-tsr",
        "--tracing_search_range",
        type=int,
        default=-1,
        help="Search range in pixel. On default it will choose 25 percent of the box size.",
    )

    tomo_group.add_argument(
        "-tmem",
        "--tracing_memory",
        type=int,
        default=0,
        help="The maximum number of frames during which a particle can vanish, "
                               "then reappear nearby, and be considered the same particle",
    )

    tomo_group.add_argument(
        "-mn3d",
        "--minimum_number_boxes_3d",
        type=int,
        default=2,
        help=" (filaments only) Minimum number of boxes per filament.",
    )

    tomo_group.add_argument(
        "-tmin",
        "--tracing_min_length",
        type=int,
        default=5,
        help=" (particles only) The minimum number of boxes in one trace to be considered as valid particle."
    )
    tomo_group.add_argument(
        "-twin",
        "--tracing_window_size",
        type=int,
        default=-1,
        help="(filaments only) Window width when averaging filament positions. Default (-1) will use the box size as window width."
    )

    tomo_group.add_argument(
        "-tedge",
        "--tracing_min_edge_weight",
        type=float,
        default=0.4,
        help="(filaments only) Number between 0 and 1. The edge weight describes the amount of overlapping between two filaments from different slices that belong to the same filament."
    )

    tomo_group.add_argument(
        "-tmerge",
        "--tracing_merge_thresh",
        type = float,
        default = 0.8,
        help = "(filaments only) Number between 0 and 1. Filaments that are overlaping more than this threshold are merged completely."
    )


    depexp_group = parser.add_argument_group(
        "Deprecated/Experimental/Special ",
        "Contains either deprecated / experimental or very special options.",
    )
    depexp_group.add_argument(
        "-p",
        "--patch",
        type=int,
        help="(DEPRECATED) Number of patches. Use the config file in case you want to use patches.",
    )

    depexp_group.add_argument(
        "--write_empty",
        action="store_true",
        help="Write empty box files when not particle could be found.",
    )


def get_parser():
    parser = GooeyParser(
        description="Pick particles with crYOLO on any dataset",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_parser(parser)
    return parser


def _main_():

    # if sys.argv[1] == "gui":

    if len(sys.argv) >= 2:
        if not "--ignore-gooey" in sys.argv:
            sys.argv.append("--ignore-gooey")

    # r'^\d+ particles are found in .* \( (\d+) % \)$'
    kwargs = {"terminal_font_family": "monospace", "richtext_controls": True}
    Gooey(
        main,
        program_name="crYOLO Predict",
        image_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../icons"),
        progress_regex=r"^.* \( Progress:\s+(-?\d+) % \)$",
        disable_progress_bar_animation=True,
        tabbed_groups=True,
        **kwargs
    )()


def main(args=None):
    import logging
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    start_method = "fork"
    try:
        os_start_method = os.environ["CRYOLO_MP_START"]

        if os_start_method in ["spawn", "fork"]:
            start_method = os_start_method
    except:
        pass
    try:
        multiprocessing.set_start_method(start_method)
    except RuntimeError:
        pass
    import cryolo.utils as util

    util.check_for_updates()

    if args is None:
        parser = get_parser()
        args = parser.parse_args()

    if isinstance(args.gpu, list):
        if len(args.gpu) == 1:
            num_gpus = 1
            if args.gpu[0] != "-1":
                str_gpus = args.gpu[0].strip().split(" ")
                num_gpus = len(str_gpus)
                os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)
        else:
            str_gpus = [str(entry) for entry in args.gpu]
            num_gpus = len(str_gpus)
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)
    else:
        num_gpus = 1
        if args.gpu != -1 and len(args.gpu) > 0:
            str_gpus = str(args.gpu)
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)

    config_proto_args = {}
    if args.num_cpu != -1:
        config_proto_args["intra_op_parallelism_threads"] =args.num_cpu
        config_proto_args["inter_op_parallelism_threads"] = args.num_cpu
    if args.gpu_fraction < 1.0 and args.gpu_fraction > 0.0:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session

        config = tf.ConfigProto(**config_proto_args)
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = args.gpu_fraction
        set_session(tf.Session(config=config))
    else:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session

        config = tf.ConfigProto(
            **config_proto_args)
        config.gpu_options.allow_growth = True


        set_session(tf.Session(config=config))

    config_path = args.conf
    weights_path = args.weights
    input_path = args.input
    for path_index, path in enumerate(input_path):
        input_path[path_index] = os.path.realpath(path)
    obj_threshold = args.threshold
    min_distance = args.distance
    mask_width = args.mask_width
    prediction_batch_size = args.prediction_batch_size
    no_merging = args.nomerging
    otf = args.otf
    do_merging = True
    global MONITOR
    MONITOR = args.monitor
    norm_margin = args.norm_margin
    search_range_factor = args.search_range_factor
    angle_delta = args.angle_delta
    straightness_method_str = args.straightness_method
    if straightness_method_str == "RMSD":
        straightness_method = filament_tracer._get_rms
    elif straightness_method_str == "LINE_STRAIGHTNESS":
        straightness_method = filament_tracer._get_straightness
    else:
        straightness_method = None

    straightness_threshold = args.straightness_threshold

    directional_method = args.directional_method

    predict_3D = args.tomogram
    tomo_search_range = args.tracing_search_range
    tomo_memory = args.tracing_memory
    tomo_min_length = args.tracing_min_length
    tomo_filament_window_size = args.tracing_window_size
    tomo_min_edge_weight = args.tracing_min_edge_weight
    tomo_merge_thresh = args.tracing_merge_thresh
    filament_mode = args.filament

    #if filament_mode and predict_3D:
    #    print("Filament mode and tomogram prediction are not compatible. Exit.")
    #    sys.exit()

    if no_merging:
        do_merging = False

    nosplit = False
    if args.nosplit is not None:
        nosplit = args.nosplit

    if straightness_method is None:
        nosplit = True

    outdir = None
    if args.output is not None:
        outdir = str(args.output)
    write_empty = args.write_empty
    min_size = args.minsize
    max_size = args.maxsize
    num_cpus = int(multiprocessing.cpu_count() / 2)
    if args.num_cpu != -1:
        num_cpus = args.num_cpu

    with open(config_path) as config_buffer:
        try:
            config = json.load(config_buffer)
        except json.JSONDecodeError:
            print(
                "Your configuration file seems to be corrupted. Please check if it is valid."
            )
        config["model"]["input_size"] = config_tools.get_adjusted_input_size(config)

    # Setup log dir
    if "other" in config and "log_path" in config["other"]:
        log_path = config["other"]["log_path"]
    else:
        log_path = "logs/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Setup logging
    import sys
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # Write command to disk

    utils.write_command(
        os.path.join(log_path, "cmdlogs/", "command_predict_" + timestr + ".txt"),
        "cryolo_predict.py " + " ".join(sys.argv[1:]),
    )


    if filament_mode:
        if args.directional_method == "CONVOLUTION" and args.filament_width is None:
            sys.exit("Please specify your filament width ( -fw / --filament_width)")
        else:
            filament_width = args.filament_width
        if args.box_distance is None:
            sys.exit("Please specify your box distance ( -bd / --box_distance)")
        else:
            box_distance = args.box_distance
        minimum_number_boxes = 1
        if args.minimum_number_boxes is not None:
            minimum_number_boxes = args.minimum_number_boxes
        minimum_number_boxes_3d = args.minimum_number_boxes_3d

    if args.patch is not None and args.patch > 0:
        num_patches = int(args.patch)
    else:
        num_patches = config_tools.get_number_patches(config)

    # Get overlap patches
    overlap_patches = 0
    if "overlap_patches" in config["model"]:
        overlap_patches = int(config["model"]["overlap_patches"])
    elif "anchors" in config["model"]:
        if not len(config["model"]["anchors"]) > 2:
            overlap_patches = config["model"]["anchors"][0]

    #  Get normalization option
    normalization_string = "STANDARD"
    if "norm" in config["model"]:
        normalization_string = config["model"]["norm"]

    write_direct = True
    if predict_3D or filament_mode:
        write_direct = False
    try:
        picking_results, about = do_prediction(
            config_path=config_path,
            config_pre=config,
            weights_path=weights_path,
            input_path=input_path,
            obj_threshold=obj_threshold,
            num_patches=num_patches,
            filament_mode=filament_mode,
            write_empty=write_empty,
            overlap=overlap_patches,
            num_images_batch_prediction=prediction_batch_size,
            num_gpus=num_gpus,
            num_cpus=num_cpus,
            otf=otf,
            normalization=normalization_string,
            normalization_margin=norm_margin,
            write_direct=write_direct,
            min_distance=min_distance,
            outdir=outdir,
            min_size=min_size,
            max_size=max_size,
            skip_picked=args.skip,
        )
    except tf.errors.ResourceExhaustedError:
        print("############################")
        print("Not enough GPU memory. Try to reduce prediction batch size (-pbs). ")
        print("############################")
        sys.exit(0)

    export_box_size = config_tools.get_box_size(config)[0]
    if write_direct == False:
        del_not_fully_immersed, del_min_distance, del_min_size = picking_postprocessing(
            picking_results,
            export_box_size,
            min_distance,
            min_size=min_size,
            max_size=max_size,
        )

        if min_distance > 0:
            print(
                del_min_distance,
                "particles were filtered because of the distance threshold",
                min_distance,
            )

        print(
            "Deleted",
            del_not_fully_immersed,
            "particles as they were not fully immersed in the micrograph",
        )

        print(
            "Deleted",
            del_min_size,
            "particles as they were out of specified size range",
        )

    ###############################
    #   Filament Post Processing
    ###############################

    # 1. Build sets of images (size = number of processors)
    # 2. Enhance
    # 3. Filamental post processing
    use_est_angles = False
    if about["filament_model"] and directional_method=="PREDICTED":
        use_est_angles = True
    elif about["filament_model"] and directional_method=="CONVOLUTION":
        use_est_angles = False
        print("Use the old convolutional method to estimate the local filament direction. ")
    elif filament_mode and about["filament_model"]==False and directional_method=="PREDICTED":
        use_est_angles = False
        print("##########")
        print("The directional method \"" + directional_method + "\" can't be used as your model is not a filament model."
                                                               "You need to retrain your picking model. Fall back to"
                                                               " old directional method \"CONVOLUTION\".")
        print("##########")

        if args.filament_width is None:
            sys.exit("Please specify your filament width ( -fw / --filament_width)")

    if filament_mode:
        picking_result_with_boxes = []
        picking_result_no_boxes = []
        picking_result_with_boxes_subsets = []
        picked_filaments = 0

        for picking_result_micrograph in picking_results:
            if picking_result_micrograph["boxes"]:

                picking_result_with_boxes.append(picking_result_micrograph)
            else:
                picking_result_micrograph["filaments"] = []
                picking_result_no_boxes.append(picking_result_micrograph)

        if picking_result_with_boxes:
            image_width, image_height = imagereader.read_width_height(
                picking_result_with_boxes[0]["img_path"]
            )
            rescale_factor = 1024.0 / max(image_width, image_height)
            rescale_factor_x = 1024.0 / image_width
            rescale_factor_y = 1024.0 / image_height
            print("Start filament tracing")
            if use_est_angles == False:
                mask_creator = maskstackcreator.MaskStackCreator(
                    filament_width=filament_width * rescale_factor,
                    mask_size=1024,
                    mask_width=mask_width,
                    angle_step=2,
                    bright_background=True,
                )

                print("Initialisation mask stack")
                mask_creator.init()
                # Devide picking result into chunks

            number_processors = num_cpus


            # Make subsets per tomogram/micrograph
            picking_result_with_boxes_subsets = [
                picking_result_with_boxes[i : i + number_processors]
                for i in range(0, len(picking_result_with_boxes), number_processors)
            ]
            process_counter = 1

            # Parallel tracing

            search_radius_scaled = export_box_size * rescale_factor * search_range_factor
            from tqdm import tqdm
            print("Trace filaments in batches")
            for picking_result_subset in tqdm(picking_result_with_boxes_subsets):
                image_subset = [
                    picking_result_subset[i]["img_path"]
                    for i in range(0, len(picking_result_subset))
                ]

                boxes_subset = [
                    picking_result_subset[i]["boxes"]
                    for i in range(0, len(picking_result_subset))
                ]

                if use_est_angles == False:
                    print("Enhance!!")
                    enhanced_images_list = line_enhancer.enhance_images(
                        image_subset, mask_creator, num_cpus
                    )

                # global filament_tracers
                global filament_tracers
                filament_tracers = []
                for image_index, boxset in enumerate(boxes_subset):
                    if use_est_angles == False:
                        enhanced_images = enhanced_images_list[image_index]
                        angle_images = [
                            enhanced_images[i]["max_angle"] for i in range(len(enhanced_images))
                        ]
                    # if it is tomogram boxset will be a list of list. one for each frame.
                    # in case of micrograph, it will just be a list of bounding boxes
                    is_micrograph = isinstance(boxset[0],BoundBox)
                    if is_micrograph:
                        # Micrograph
                        angle_image_flipped = None
                        if use_est_angles == False:
                            angle_image_flipped = np.flipud(angle_images[image_index])

                        tracer = filament_tracer.FilamentTracer(
                                boxes=boxset,
                                orientation_image=angle_image_flipped,
                                search_radius=search_radius_scaled,
                                angle_delta=angle_delta,
                                rescale_factor=rescale_factor,
                                rescale_factor_x=rescale_factor_x,
                                rescale_factor_y=rescale_factor_y,
                                do_merging=do_merging,
                                box_distance=box_distance,
                                nosplit=nosplit,
                                straightness_method=straightness_method,
                                straightness_threshold=straightness_threshold
                            )
                        filament_tracers.append((image_index,0,tracer))
                    else:
                        # Tomogram
                        for frame_index, boxes in enumerate(boxset):
                            angle_image_flipped = None
                            if use_est_angles == False:
                                angle_image_flipped = np.flipud(angle_images[frame_index])

                            tracer = filament_tracer.FilamentTracer(
                                    boxes=boxes,
                                    orientation_image=angle_image_flipped,
                                    search_radius=search_radius_scaled,
                                    angle_delta=angle_delta,
                                    rescale_factor=rescale_factor,
                                    rescale_factor_x=rescale_factor_x,
                                    rescale_factor_y=rescale_factor_y,
                                    do_merging=do_merging,
                                    box_distance=box_distance,
                                    nosplit=nosplit,
                                    straightness_method=straightness_method,
                                    straightness_threshold=straightness_threshold
                                )

                            filament_tracers.append(
                                (image_index,frame_index,tracer)
                            )
                #pool = multiprocessing.Pool(processes=num_cpus)
                #print("NUM TRACERS:", len(filament_tracers), "CPUS", num_cpus)
                with multiprocessing.Pool(processes=num_cpus) as pool:
                    subset_new_filaments = pool.map(
                                trace_subset_filements,
                                range(len(filament_tracers)),
                                chunksize=1,
                            )


                print("Tracing done")
                for image_index, frame_index, filaments in subset_new_filaments:

                    if "filaments" not in picking_result_subset[image_index]:
                        picking_result_subset[image_index]["filaments"] = {}

                    # Min number of boxes filter:
                    filaments = filament_tracer.filter_filaments_by_num_boxes(
                        filaments, minimum_number_boxes
                    )
                    picked_filaments += len(filaments)

                    if len(filaments) >= 1:
                        if int(frame_index) in picking_result_subset[image_index]["filaments"]:
                            print("Strange. There are multiple picks per frame. Stop")
                            import sys
                            sys.exit(0)
                        picking_result_subset[image_index]["filaments"][int(frame_index)] = filaments




                print("Total number of filaments picked so far: ", picked_filaments)
                process_counter += 1

        if write_empty:
            picking_result_with_boxes_subsets.append(picking_result_no_boxes)

        print("Total number of filaments picked: ", picked_filaments)


    ###############################
    #   Write bounding boxes
    ###############################
    if len(picking_results) > 0:
        write_size_distribution_to_disk(picking_results, os.path.join(outdir, "DISTR"))

    if predict_3D and filament_mode == False:
        picking_results = predict_3D_boxes_from_2D_boxes(picking_results=picking_results,
                                                         obj_threshold=obj_threshold,
                                                         tomo_min_length=tomo_min_length,
                                                         tomo_search_range=tomo_search_range,
                                                         tomo_memory=tomo_memory)

    if filament_mode:
        if predict_3D:
            print("Do 3D filament tracing")
            '''
            boxsize = utils.anchor_to_boxsize(
                anchor_dim=about["used_anchors"],
                grid_dim=config_tools.get_gridcell_dimensions(config),
                input_image_dim=about["adjusted_input_size"]
            )
            '''

            used_boxsize = export_box_size
            if  tomo_search_range == -1:
                tomo_search_range = used_boxsize/2

            if tomo_memory == -1:
                tomo_memory = 0 #max(1, used_boxsize // 10)

            if tomo_filament_window_size == -1:
                tomo_filament_window_size = int(used_boxsize)*3

            picking_result_with_boxes_subsets = predict_3D_filaments_from_2d_filaments(
                picking_results=picking_result_with_boxes_subsets,
                tomo_search_range=tomo_search_range,
                tomo_memory=tomo_memory,
                window_size=tomo_filament_window_size,
                min_edge_weight=tomo_min_edge_weight,
                box_distance=box_distance,
                minimum_number_boxes=minimum_number_boxes_3d,
                tomo_merge_threshold=tomo_merge_thresh
            )
            num_traced = 0
            for r in picking_result_with_boxes_subsets:
                for r2 in r:
                    if "filaments_traced" not in r2:
                        num_traced = -1
                        break
                    num_traced = num_traced + len(r2["filaments_traced"])
                if num_traced == -1:
                    break
            if num_traced > -1:
                print("Volume tracing found ", num_traced, " Filaments")
        write_filaments_to_disk(outdir, picking_result_with_boxes_subsets, write_empty, is_3d=predict_3D)
    elif write_direct == False:
        prediction_result_to_disk(outdir, picking_results, write_empty=write_empty)




    if args.cleanup:
        print("#####################################")
        print("Delete filtered images...")
        if os.path.exists(config["model"]["filter"][-1]):
            import shutil
            shutil.rmtree(config["model"]["filter"][-1])
        print("Done")
        print("#####################################")


def write_size_distribution_to_disk(picking_results, output_folder=""):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    estimated_size = []
    confidence = []

    for box_to_write in picking_results:
        boxes_set = box_to_write["boxes_unfiltered"]
        for boxes in boxes_set:
            for box in boxes:
                est_width = box.meta["boxsize_estimated"][0]
                est_height = box.meta["boxsize_estimated"][1]
                avg_size = (est_height + est_width) // 2
                estimated_size.append(avg_size)
                confidence.append(box.c)

    #################################
    # Size distribution histogram
    #################################
    if len(estimated_size)>0:
        est_size_mean = int(np.mean(estimated_size))
        est_size_sd = int(np.std(estimated_size))
        est_size_25q = int(np.percentile(estimated_size, 25))
        est_size_50q = int(np.percentile(estimated_size, 50))
        est_size_75q = int(np.percentile(estimated_size, 75))
        print("#####################################")
        print("")
        print("## Particle diameter distribution ##")
        print("MEAN:", est_size_mean, "px")
        print("SD:", est_size_sd, "px")
        print("25%-Quantile:", est_size_25q, "px")
        print("50%-Quantile:", est_size_50q, "px")
        print("75%-Quantile:", est_size_75q, "px")

        import matplotlib as mpl

        mpl.use("Agg")
        import matplotlib.pyplot as pl

        mpl.rcParams["figure.dpi"] = 200
        mpl.rcParams.update({"font.size": 7})
        width = max(10, int((np.max(estimated_size) - np.min(estimated_size)) / 10))
        pl.hist(estimated_size, bins=width)
        pl.title("Particle diameter distribution")
        pl.xlabel("Partilce diameter [px] (Bin size: " + str(width) + "px )")
        pl.ylabel("Count")

        timestr = time.strftime("%Y%m%d-%H%M%S")
        import csv

        output_path_distr_raw_txt = os.path.join(
            output_folder, "size_distribution_raw_" + timestr + ".txt"
        )
        np.savetxt(output_path_distr_raw_txt, estimated_size, fmt="%d")
        output_path_distr_txt = os.path.join(
            output_folder, "size_distribution_summary_" + timestr + ".txt"
        )
        with open(output_path_distr_txt, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["MEAN", est_size_mean])
            writer.writerow(["SD", est_size_sd])
            writer.writerow(["Q25", est_size_25q])
            writer.writerow(["Q50", est_size_50q])
            writer.writerow(["Q75", est_size_75q])
        print("Wrote particle size distribution summary to", output_path_distr_txt)
        output_path_distr_img = os.path.join(
            output_folder, "size_distribution_" + timestr + ".png"
        )
        print("Wrote plot of particle size distribution to", output_path_distr_img)
        pl.savefig(output_path_distr_img)
        pl.close()

        #################################
        # Confidence distribution histogram
        #################################
        output_path_conf_img = os.path.join(
            output_folder, "confidence_distribution_" + timestr + ".png"
        )
        output_path_conf_raw = os.path.join(
            output_folder, "confidence_distribution_raw_" + timestr + ".txt"
        )
        output_path_conf_sum = os.path.join(
            output_folder, "confidence_distribution_summary_" + timestr + ".txt"
        )

        # RAW DATA
        np.savetxt(output_path_conf_raw, confidence, fmt="%1.2f")

        # SUMMARY
        conf_mean = np.mean(confidence)
        conf_sd = np.std(confidence)
        conf_25q = np.percentile(confidence, 25)
        conf_50q = np.percentile(confidence, 50)
        conf_75q = np.percentile(confidence, 75)

        with open(output_path_conf_sum, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["MEAN", conf_mean])
            writer.writerow(["SD", conf_sd])
            writer.writerow(["Q25", conf_25q])
            writer.writerow(["Q50", conf_50q])
            writer.writerow(["Q75", conf_75q])

        # PLOT
        width = max(10, int((np.max(confidence) - np.min(confidence)) / 0.05))
        pl.hist(confidence, bins=width)
        pl.title("Confidence distribution")
        bin_size_str = "{0:.2f}".format(((np.max(confidence) - np.min(confidence)) / width))
        pl.xlabel("Confidence (Bin size: " + bin_size_str + ")")
        pl.ylabel("Count")
        pl.savefig(output_path_conf_img)
        print("")
        print("## Particle confidence distribution ##")
        print("Wrote confidence distribution summary", output_path_conf_sum)
        print("Wrote confidence distribution to", output_path_conf_img)
        print("")
        print("#####################################")
        pl.close()

def write_filaments_to_disk(outdir, picking_results, write_empty=False, is_3d = False):

    for picking_result_subset in picking_results:

        for result in picking_result_subset:
            if result["filaments"] or write_empty:

                if is_3d == False:
                    for frame in result["filaments"]:
                        pth = result["pth"]
                        eman_helix_segmented_path = pth
                        eman_start_end = pth
                        star_start_end = pth[:-3] + "star"
                        cbox_segmented = pth[:-3] + "cbox"
                        if outdir is not None:
                            filename = os.path.basename(pth)
                            eman_helix_segmented_path = os.path.join(
                                outdir, "EMAN_HELIX_SEGMENTED", filename
                            )
                            eman_start_end = os.path.join(
                                outdir, "EMAN_START_END", filename
                            )
                            filename = os.path.splitext(filename)[0] + ".star"
                            star_start_end = os.path.join(
                                outdir, "STAR_START_END", filename
                            )

                            filename = os.path.splitext(filename)[0] + ".cbox"
                            cbox_segmented = os.path.join(
                                outdir, "CBOX_FILAMENT_SEGMENTED", filename
                            )

                            cbox_unfitlered = os.path.join(
                                outdir, "CBOX", filename
                            )


                        if len(result["filaments"]) > 1:
                            root_ext = os.path.splitext(eman_helix_segmented_path)
                            eman_helix_segmented_path = root_ext[0] + "_slice" + str(frame).zfill(4) + \
                                                        root_ext[1]

                            root_ext = os.path.splitext(eman_start_end)
                            eman_start_end = root_ext[0] + "_slice" + str(frame).zfill(4) + \
                                             root_ext[1]

                            root_ext = os.path.splitext(star_start_end)
                            star_start_end = root_ext[0] + "_slice" + str(frame).zfill(4) + \
                                             root_ext[1]

                        if not os.path.exists(os.path.dirname(eman_helix_segmented_path)):
                            os.makedirs(os.path.dirname(eman_helix_segmented_path))

                        if not os.path.exists(os.path.dirname(eman_start_end)):
                            os.makedirs(os.path.dirname(eman_start_end))

                        if not os.path.exists(os.path.dirname(star_start_end)):
                            os.makedirs(os.path.dirname(star_start_end))

                        if not os.path.exists(os.path.dirname(cbox_segmented)):
                            os.makedirs(os.path.dirname(cbox_segmented))

                        if not os.path.exists(os.path.dirname(cbox_unfitlered)):
                            os.makedirs(os.path.dirname(cbox_unfitlered))

                        CoordsIO.write_eman1_helicon(
                            filaments=result["filaments"][frame],
                            path=eman_helix_segmented_path,
                            image_filename=os.path.basename(result["img_path"]),
                        )

                        CoordsIO.write_eman1_filament_start_end(
                            filaments=result["filaments"][frame], path=eman_start_end
                        )

                        CoordsIO.write_star_filemant_file(
                            filaments=result["filaments"][frame], path=star_start_end
                        )

                        CoordsIO.write_cbox_file(
                            coordinates=result["filaments"][frame],
                            path=cbox_segmented
                        )

                        CoordsIO.write_cbox_file(
                            coordinates=result["boxes_unfiltered"][frame],
                            path=cbox_unfitlered
                        )
                else:

                    root_ext = os.path.splitext(result["pth"])
                    cbox_segmented_path = root_ext[0] + ".cbox"

                    if outdir is not None:
                        filename = os.path.basename(cbox_segmented_path)
                        cbox_segmented_path_untraced = os.path.join(
                            outdir, "CBOX_FILAMENTS_UNTRACED", filename
                        )

                        cbox_unfitlered = os.path.join(
                            outdir, "CBOX", filename
                        )

                        cbox_segmented_path_traced = os.path.join(
                            outdir, "CBOX_FILAMENTS_TRACED", filename
                        )

                        coords_path_traced = os.path.join(
                            outdir, "COORDS_TRACED", os.path.basename(root_ext[0])+".coords"
                        )

                        coords_fid_traced = os.path.join(
                            outdir, "COORDS_TRACED_FID", os.path.basename(root_ext[0])+"_fid.coords"
                        )

                    if not os.path.exists(os.path.dirname(cbox_segmented_path_untraced)):
                        os.makedirs(os.path.dirname(cbox_segmented_path_untraced))

                    if not os.path.exists(os.path.dirname(cbox_unfitlered)):
                        os.makedirs(os.path.dirname(cbox_unfitlered))

                    # Set z for coordinates
                    all_untraced_filaments = []
                    all_untraced_boxes = []
                    for frame in result["filaments"]:
                        for filament in result["filaments"][frame]:
                            for box in filament.boxes:
                                box.depth = 1
                                box.z = frame
                            all_untraced_filaments.append(filament)

                    for frame,boxset in enumerate(result["boxes"]):
                        for box in boxset:
                            box.depth = 1
                            box.z = frame
                            all_untraced_boxes.append(box)

                    CoordsIO.write_cbox_file(cbox_segmented_path_untraced, all_untraced_filaments)
                    CoordsIO.write_cbox_file(cbox_unfitlered, all_untraced_boxes)
                    if "filaments_traced" in result:

                        if not os.path.exists(os.path.dirname(cbox_segmented_path_traced)):
                            os.makedirs(os.path.dirname(cbox_segmented_path_traced))
                        CoordsIO.write_cbox_file(cbox_segmented_path_traced, result["filaments_traced"])
                        fil_boxes = []
                        fil_ids_array = [[],[],[],[]]

                        for fil_id, fil in enumerate(result["filaments_traced"]):
                            xs = [box.x + box.w/2 for box in fil.boxes]
                            ys = [box.y + box.h/2 for box in fil.boxes]
                            zs = [box.z for box in fil.boxes]
                            fil_boxes.extend(fil.boxes)

                            fil_ids_array[0].extend(xs)
                            fil_ids_array[1].extend(ys)
                            fil_ids_array[2].extend(zs)
                            fil_ids_array[3].extend([fil_id+1] * len(fil.boxes)) # FID needs be >1, otherweise relion will not recognize it.


                        if not os.path.exists(os.path.dirname(coords_path_traced)):
                            os.makedirs(os.path.dirname(coords_path_traced))
                        CoordsIO.write_coords_file(coords_path_traced, fil_boxes)

                        if not os.path.exists(os.path.dirname(coords_fid_traced)):
                            os.makedirs(os.path.dirname(coords_fid_traced))

                        np.savetxt(coords_fid_traced, np.array(fil_ids_array).T, fmt='%f')



def prediction_result_to_disk(outdir, picking_results, write_empty=False):
    for box_to_write in picking_results:

        original_path = box_to_write["pth"]
        eman_path = original_path
        box_set = box_to_write["boxes"]
        box_set_unfiltered = box_to_write["boxes_unfiltered"]

        if not write_empty:
            box_set = [boxes for boxes in box_set if len(boxes)>0]
            box_set_unfiltered = [boxes for boxes in box_set_unfiltered if len(boxes) > 0]

        if "is_3d" in box_to_write and box_to_write["is_3d"] == True:

            #Write eman 3d boxes
            for boxes_index, boxes in enumerate(box_set):

                if outdir is not None:
                    filename = os.path.basename(eman_path)
                    eman_path = os.path.join(outdir, "EMAN_3D", filename)

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(eman_path)):
                    os.makedirs(os.path.dirname(eman_path))

                CoordsIO.write_eman_boxfile3d(path=eman_path,boxes=boxes)

            # Write CBOX / coords 3D coordinates
            for boxes_index, boxes in enumerate(box_set):

                cbox_path = os.path.splitext(original_path)[0] + ".cbox"
                coords_path = os.path.splitext(original_path)[0] + ".coords"

                if outdir is not None:
                    cbox_path = os.path.join(outdir, "CBOX_3D", os.path.basename(cbox_path))
                    coords_path = os.path.join(outdir, "COORDS", os.path.basename(coords_path))

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(cbox_path)):
                    os.makedirs(os.path.dirname(cbox_path))
                if not os.path.exists(os.path.dirname(coords_path)):
                    os.makedirs(os.path.dirname(coords_path))
                CoordsIO.write_cbox_file(path=cbox_path,
                                         coordinates=boxes)
                CoordsIO.write_coords_file(path=coords_path,
                                         boxes=boxes)


            #Write CBOX slices coordinates
            for boxes_index, boxes in enumerate(box_set_unfiltered):

                cbox_path = os.path.splitext(original_path)[0] + ".cbox"

                if outdir is not None:
                    filename = os.path.basename(cbox_path)
                    cbox_path = os.path.join(outdir, "CBOX_UNTRACED", filename)

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(cbox_path)):
                    os.makedirs(os.path.dirname(cbox_path))
                CoordsIO.write_cbox_file(path=cbox_path, coordinates=boxes)



        else:
            for boxes_index, boxes in enumerate(box_set):

                slices_index = ""
                if len(box_set)>1:
                    slices_index = "_slice"+str(boxes_index).zfill(4)

                star_path = os.path.splitext(original_path)[0] + slices_index + ".star"
                cbox_path = os.path.splitext(original_path)[0] + slices_index + ".cbox"

                if outdir is not None:
                    filename = os.path.basename(eman_path)
                    eman_path = os.path.join(outdir, "EMAN", filename)

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(eman_path)):
                    os.makedirs(os.path.dirname(eman_path))

                CoordsIO.write_eman1_boxfile(path=eman_path, boxes=boxes)

                if outdir is not None:
                    filename = os.path.basename(star_path)
                    star_path = os.path.join(outdir, "STAR", filename)

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(star_path)):
                    os.makedirs(os.path.dirname(star_path))
                CoordsIO.write_star_file(path=star_path, boxes=boxes)

                if outdir is not None:
                    filename = os.path.basename(cbox_path)
                    star_path = os.path.join(outdir, "CBOX", filename)

                # Create directory if it does not existes
                if not os.path.exists(os.path.dirname(star_path)):
                    os.makedirs(os.path.dirname(star_path))
                CoordsIO.write_cbox_file(path=star_path, coordinates=box_to_write["boxes_unfiltered"][boxes_index])


def min_distance_filter(boxes, min_distance):
    min_distance_sq = min_distance * min_distance

    import itertools

    all_comb = list(itertools.combinations(boxes, 2))

    distsqs = list(itertools.starmap(utils.box_squared_distance, all_comb))
    low_distance_pairs = list(
        itertools.compress(all_comb, [distsq < min_distance_sq for distsq in distsqs])
    )
    for box_a, box_b in low_distance_pairs:
        box_to_delte = box_a
        if box_a.c > box_b.c:
            box_to_delte = box_b
        if box_to_delte in boxes:
            boxes.remove(box_to_delte)

    return boxes


def rescale(box, image_height, image_width, export_size=None):
    x_ll = box.x * image_width - box.w / 2.0 * image_height  # lower left
    y_ll = image_height - box.y * image_height - box.h / 2.0 * image_width # lower right

    if "angle" in box.meta:
        box.meta["angle"] = np.pi - box.meta["angle"]

    boxheight_in_pxl = box.h * image_width
    boxwidth_in_pxl = box.w * image_height
    if export_size is not None:
        delta_boxheight = export_size - boxheight_in_pxl
        delta_boxwidth = export_size - boxwidth_in_pxl
        x_ll = x_ll - delta_boxwidth / 2
        y_ll = y_ll - delta_boxheight / 2
        boxheight_in_pxl = export_size
        boxwidth_in_pxl = export_size
    box.x = x_ll
    box.y = y_ll

    box.w = boxwidth_in_pxl
    box.h = boxheight_in_pxl


    return box


def picking_postprocessing_single_res(
    boxes, img_path, export_size, min_distance, min_size=None, max_size=None
):
    # Rescaling
    image_width, image_height = imagereader.read_width_height(
        img_path
    )

    # Save estimated box size in meta data
    for box in boxes:
        box.meta["boxsize_estimated"] = (
            int(box.w * image_width),
            int(box.h * image_height),
        )
        #print(box.meta["boxsize_estimated"])

    # Resize box
    boxes = [
        rescale(box, image_height, image_width, export_size)
        for box in boxes]

    # Min distance filter
    del_min_distance = 0
    if min_distance > 0:
        del_min_distance = len(boxes)
        boxes = min_distance_filter(
            boxes, min_distance
        )
        del_min_distance = del_min_distance - len(boxes)

    # Filtering of particles which are not fully immersed in the micrograph
    del_not_fully_immersed = 0
    boxes_to_delete = get_not_fully_immersed_box_indices(
        boxes, image_height, image_width
    )
    for index in sorted(boxes_to_delete, reverse=True):
        del boxes[index]
    del_not_fully_immersed += len(boxes_to_delete)

    # Filtering according size
    out_of_size = 0

    out_of_size_box_indices = get_out_of_sizes_boxes(
        boxes, min_size=min_size, max_size=max_size
    )
    for index in sorted(out_of_size_box_indices, reverse=True):
        del boxes[index]
    out_of_size += len(out_of_size_box_indices)

    return boxes, del_not_fully_immersed, del_min_distance, out_of_size


def predict_3D_filaments_from_2d_filaments(
        picking_results,
        tomo_search_range,
        tomo_memory,
        window_size,
        min_edge_weight,
        box_distance,
        minimum_number_boxes=1,
        tomo_merge_threshold=0.8
):

    from cryolo import grouping3d
    for picking_result_subset in picking_results: # One for each image

        for result in picking_result_subset:
            filaments_traced_3d = grouping3d.do_tracing_filaments(
                filaments_dict=result["filaments"],
                search_range=tomo_search_range,
                memory=tomo_memory,
                window_size=window_size,
                min_edge_weight=min_edge_weight,
                box_distance=box_distance,
                resample_dist=box_distance,
                min_length_filament=minimum_number_boxes,
                merge_threshold=tomo_merge_threshold,
            )

            result["filaments_traced"] = filaments_traced_3d
    return picking_results


def predict_3D_boxes_from_2D_boxes(
        picking_results, obj_threshold, tomo_min_length, tomo_search_range=-1, tomo_memory=-1
):
    """
    :param picking_results:
    :param obj_threshold:
    :param tomo_min_length:
    :param tomo_search_range:
    :param tomo_memory:
    :return:
    """
    # create copy
    picking_results_copy = []
    from cryolo import grouping3d
    num_tomo_particles = 0
    num_particles = 0
    for result_ in picking_results:
        result = dict(result_)
        picking_results_copy.append(result)
        mean_box_size = np.mean(
            [np.mean([(box.w + box.h) / 2 for box in slice_boxes]) for slice_boxes in
             result["boxes"] if len(slice_boxes) > 0])
        if tomo_search_range == -1:
            tomo_search_range = max(1, mean_box_size // 4.0)
        if tomo_memory == -1:
            tomo_memory = max(1, mean_box_size // 10)
        num_particles += np.sum([len(slice_boxes) for slice_boxes in result["boxes"]])
        tracing_dict = {}
        assert len(result["boxes"]) == len(result[
                                               "slices_indices"]), "Slices indicies and number of box lists are not equal. stop."

        for k in range(len(result["boxes"])):
            tracing_dict[int(result["slices_indices"][k])] = result["boxes"][k]

        bounding_boxes_3d = grouping3d.do_tracing(
            boxes_dict=tracing_dict,
            search_range=tomo_search_range,
            memory=tomo_memory,
            min_length=tomo_min_length
        )

        bounding_boxes_3d = utils.non_maxima_suppress_fast_3d(bounding_boxes_3d,
                                                        nms_threshold=0.3,
                                                        obj_threshold=obj_threshold)

        for box in bounding_boxes_3d:
            box.depth = box.w  # its always a square box

        result["boxes"] = [bounding_boxes_3d]

        result["is_3d"] = True
        num_tomo_particles += len(bounding_boxes_3d)
        # Set the depth
        boxes_3D_per_slice = []
        for frame_index, boxes in enumerate(result["boxes_unfiltered"]):
            for box in boxes:
                box.z = frame_index
                box.depth = 1
                boxes_3D_per_slice.append(box)

        result["boxes_unfiltered"] = [boxes_3D_per_slice]
    print(num_tomo_particles, "Particles were found by tracing", num_particles,
          "through the volumes.")
    return picking_results_copy

def picking_postprocessing(
    picking_results, export_size, min_distance, min_size=None, max_size=None
):
    # Rescaling
    del_not_fully_immersed = 0
    del_min_distance = 0
    out_of_size = 0
    for picking_result_micrograph in picking_results:
        for boxes_index, boxes in enumerate(picking_result_micrograph["boxes"]):
            post_res = picking_postprocessing_single_res(
                boxes=boxes,
                img_path=picking_result_micrograph["img_path"],
                export_size=export_size,
                min_distance=min_distance,
                min_size=min_size,
                max_size=max_size
            )
            picking_result_micrograph["boxes"][boxes_index] = post_res[0]
            del_not_fully_immersed += post_res[1]
            del_min_distance += post_res[2]
            out_of_size += post_res[3]

            post_res2 = picking_postprocessing_single_res(
                boxes=picking_result_micrograph["boxes_unfiltered"][boxes_index],
                img_path=picking_result_micrograph["img_path"],
                export_size=export_size,
                min_distance=min_distance,
                min_size=None,
                max_size=None
            )
            picking_result_micrograph["boxes_unfiltered"][boxes_index] = post_res2[0]

    return del_not_fully_immersed, del_min_distance, out_of_size


def setup_prediction_monitor(input_path, img_paths):
    """
    Setups the monitor mode
    :param input_path: Folder to monitor
    :param img_paths: List that should be updated when a new file is popping up
    :return: None
    """

    # Setup the monitor mode
    def add_to_list(event):
        if os.path.basename(event.src_path).lower().startswith("stop.cryolo"):

            global MONITOR
            MONITOR = False
            os.remove(event.src_path)
        else:
            img_paths.append(event.src_path)

    patterns = [
        "*.tiff",
        "*.mrc",
        "*.tif",
        "*.mrcs",
        "*.png",
        "*.png",
        "*.jpeg",
        "*.cryolo",
    ]
    ignore_patterns = None  # ".*" #ignore invisible files
    ignore_directories = True
    case_sensitive = False
    image_dir_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive
    )

    image_dir_handler.on_created = add_to_list

    go_recursively = False
    my_observer = Observer()
    print("Monitoring:", input_path[0])
    my_observer.schedule(
        image_dir_handler, os.path.realpath(input_path[0]), recursive=go_recursively
    )
    my_observer.start()
    return my_observer

def get_total_number_of_batches(img_pths, batchsize):
    num_frms = 0
    for pth in img_pths:
        num_frms += imagereader.get_num_frames(pth)
    return np.ceil(num_frms/batchsize)


def generate_batches(img_pths,
                     batchsize,
                     num_patches,
                     overlap,
                     otf = False,
                     config = None,
                     filter_options=None,
                     resize_to=None,
                     num_cpus=None,
                     ):
    """

    :param img_pths: Input image paths
    :param batchsize: Batch size
    :param num_patches: Number of patches
    :param overlap: Overlap of pathces
    :param otf: Indiciator (True/False) if on-the-fly processing is used
    :param config: Only needed in case if filtering (OTF or Monitor): crYOLO configuration dictory
    :param filter_options: Filtering options
    :param resize_to: In case of filtering, additional parameter for resizing
    :param num_cpus: Number of threads used for filtering
    :return:
        - batch_np - 3D numpy array with batch image data
        - tiles_coords - tile coordiantes incase of patching is used
        - slice_indicis - Tuple (a,b), where a is current slice indict and b is the total number of slices
        - img_size - Image size before patching
        - batch_img_paths - The paths of the images used in this batch.
    """
    skipped_images = []
    image_indices = []
    tiles_coords = []
    batch = []
    img_tiles = None
    slice_indices = []
    img_size = None
    batch_img_paths = []
    for current_index_image, img_pth in enumerate(img_pths):
        if os.path.basename(img_pth)[0] == ".":
            continue
        # Read image file!
        try:
            if (otf or MONITOR) and "filter" in config["model"]:
                image = do_filtering(
                    img_paths=[img_pth],
                    filter_options=filter_options,
                    resize_to=resize_to,
                    num_cpus=num_cpus,
                    return_np=True
                )[0]
            else:
                image = imagereader.image_read(img_pth)
        except ValueError:
            print("Image not valid: ", img_pth, "SKIPPED")
            skipped_images.append(img_pth)
            continue

        if len(image.shape) == 2:
            image = image[np.newaxis,...]

        if image is not None or image.shape[0] == 0 or image.shape[1] == 0:
            image_indices.append(current_index_image)

            for slice_index in range(image.shape[0]):
                slice = image[slice_index]
                if img_size == None:
                    img_size = slice.shape
                else:
                    if img_size != slice.shape:
                        print("It seems that crYOLO is picking images with different shape. That"
                              "should not happen. Image:", img_pth, slice_index)
                for patch_x in np.arange(0, num_patches):
                    for patch_y in np.arange(0, num_patches):
                        tile_coordinates = imagereader.get_tile_coordinates(
                            slice.shape[1],
                            slice.shape[0],
                            num_patches,
                            (patch_x, patch_y),
                            overlap=overlap,
                        )
                        tiles_coords.append(tile_coordinates)
                        img_tmp = slice[tile_coordinates[1], tile_coordinates[0]]

                        batch.append(img_tmp[np.newaxis,...])
                        slice_indices.append((slice_index+1,image.shape[0]))
                        batch_img_paths.append(img_pth)

                last_slice_on_last_image = slice_index==(image.shape[0]-1) and (len(img_pths)-1)==current_index_image
                if len(batch) == batchsize or last_slice_on_last_image:
                    batch_np = np.concatenate(batch)
                    yield batch_np, tiles_coords, slice_indices, img_size, batch_img_paths
                    batch = []
                    tiles_coords = []
                    slice_indices = []
                    batch_img_paths = []
        if MONITOR:
            while current_index_image == (len(img_pths)-1):
                import time
                time.sleep(1)
                if MONITOR == False:
                    break






def do_filtering(img_paths, filter_options, resize_to, num_cpus, return_np=False):
    if len(filter_options) > 2:
        if not return_np:
            print("Filter data using noise2noise model: ", filter_options[0])
            img_paths_filtered = utils.filter_images_noise2noise_dir(
                img_paths=img_paths,
                output_dir_filtered_imgs=filter_options[3],
                model_path=filter_options[0],
                padding=filter_options[1],
                batch_size=filter_options[2],
                resize_to=resize_to,
            )
            return img_paths_filtered
        else:
            filtered_images = []
            for img_pth in img_paths:
                image = utils.filter_image_noise2noise(
                    img_path=img_pth,
                    model_path=filter_options[0],
                    padding=filter_options[1],
                    batch_size=filter_options[2],
                )

                if resize_to is not None:
                    from PIL import Image

                    image = np.array(
                        Image.fromarray(image).resize(
                            resize_to, resample=Image.BILINEAR
                        )
                    )
                filtered_images.append(image)
            return filtered_images
    else:
        # Normal lowpass filter
        if not return_np:
            start_f = time.time()
            img_paths_filtered = utils.filter_images_lowpass(
                img_paths=img_paths,
                output_dir_filtered_imgs=filter_options[1],
                cutoff=filter_options[0],
                num_cpus=num_cpus,
                resize_to=resize_to,
            )
            end_f = time.time()
            print("Time needed for filtering:", end_f - start_f)
            return img_paths_filtered
        else:
            images = utils.filter_images_lowpass(
                img_paths=img_paths,
                output_dir_filtered_imgs=None,
                cutoff=filter_options[0],
                num_cpus=num_cpus,
                otf=True,
                resize_to=resize_to,
            )
            return images
    return img_paths_filtered


def get_prediction_image_list(input_path, ignore_pth=None):
    """
    Will find all images to pick in input_path. Will ignore those images for which already a
    boxfile exist in ignore_pth

    :param input_path: Path with images to predict
    :param ignore_pth:
    :return:
    """
    img_paths = []
    if isinstance(input_path, list):

        for path in input_path:
            isdir = os.path.isdir(path)
            if isdir:
                dir_files = os.listdir(path)

                dir_files = [
                    i
                    for i in dir_files
                    if not i.startswith(".")
                       and os.path.isfile(os.path.join(path, i))
                       and i.endswith(("tiff", "tif", "mrc", "mrcs", "png", "jpg", "jpeg", "rec"))
                ]

                img_paths.extend(
                    [os.path.join(path, image_file) for image_file in dir_files]
                )
            elif os.path.isfile(path):

                if path.endswith(".star"):
                    from pyStarDB import sp_pystardb as star
                    sfile = star.StarFile(path)
                    if 'micrographs' in sfile:
                        panda_dataframe = sfile['micrographs'] # With relion 3.1
                    else:
                        panda_dataframe = sfile[''] # the panda dataframe has noname (i.e.:data_)
                    if '_rlnMicrographName' in panda_dataframe.columns:
                        for pth in panda_dataframe._rlnMicrographName.unique():
                            if pth.endswith(
                                    ("tiff", "tif", "mrc", "png", "mrcs", "jpg", "jpeg", "rec")):
                                img_paths.append(pth)

                if not path.startswith(".") and path.endswith(
                        ("tiff", "tif", "mrc", "png", "mrcs", "jpg", "jpeg", "rec")
                ):
                    img_paths.append(path)
    else:
        isdir = os.path.isdir(input_path)
        if isdir:
            img_paths = os.listdir(input_path)

            img_paths = [
                i
                for i in img_paths
                if not i.startswith(".")
                   and os.path.isfile(os.path.join(input_path, i))
                   and i.endswith(("tiff", "tif", "mrc", "mrcs", "png", "jpg", "jpeg"))
            ]

    if ignore_pth is not None:
        import glob
        already_picked = glob.glob(os.path.join(ignore_pth, "*/*.box"))
        already_picked = [os.path.splitext(os.path.basename(box_path))[0] for box_path in
                          already_picked]
        img_paths = [img_path for img_path in img_paths if
                     os.path.splitext(os.path.basename(img_path))[0] not in already_picked]

    return img_paths

def do_prediction(
    config_path,
    weights_path,
    input_path,
    num_patches,
    obj_threshold=0.3,
    write_empty=False,
    config_pre=None,
    overlap=0,
    filament_mode=False,
    num_images_batch_prediction=3,
    num_gpus=1,
    num_cpus=-1,
    yolo=None,
    otf=False,
    normalization="STANDARD",
    normalization_margin=0,
    skip_picked=False,
    **kwargs
):
    """
    :param config_path: Path to the config file
    :param weights_path: Path do weights file (h5)
    :param input_path: Path to the folder containing the input images
    :param num_patches: Number of patches to use
    :param obj_threshold: Threshold for objects
    :param write_empty:
    :param config_pre:
    :param overlap: Overlap if patches are used
    :param filament_mode: If true, higher nms threshold is used to allow more overlapping.
    :param num_images_batch_prediction:
    :param num_gpus:
    :param yolo:
    :param otf: on the fly picking
    :param write_direct: on the fly writing of box files
    :return:
    1. List of dictionaris (on for each image) with the following keys:
        - pth - Potential path to the box file box_pth,
        - img_width - Original image width
        - img_height - Original image height
        - img_path - Oriignal image path
        - boxes - List of lists (one for each micrograph/slice) of Boxes filtered according confidence threshold
        - boxes_unfiltered - List of lists (one for each micrograph/slice) Boxes without applied confidence filtering
        - slices_indices - Slice indices for tomograms
    2. dictonary with information about training
    """
    for path in input_path:
        path_exists = os.path.exists(path)
        if not path_exists:
            sys.exit("Input path does not exist: " + path)

    if skip_picked:
        img_paths = get_prediction_image_list(input_path, kwargs["outdir"])
    else:
        img_paths = get_prediction_image_list(input_path)

    import time

    my_observer = None
    if MONITOR:
        my_observer = setup_prediction_monitor(input_path, img_paths)

    if not img_paths and MONITOR == False:
        sys.exit("No valid image in your specified input")

    if len(img_paths) == 0 and MONITOR == True:
        while len(img_paths) == 0:
            time.sleep(1)
        # When monitoring a directory, wait for the first valid image

    img_paths.sort()
    about = {}
    from cryolo.preprocessing import get_image_size_distr

    size_distr = get_image_size_distr(img_paths)
    if len(size_distr)>1:
        print("Prediction on mixed-size images is not supported in single prediction run.")
        print("The following input image sizes were detected:")
        for size in size_distr:
            print(size[0], "x", size[1], "( N:", size[2], ")")
        print("Stop crYOLO.")
        sys.exit(1)


    if config_pre is not None:
        config = config_pre.copy()
    else:
        with open(config_path) as config_buffer:
            config = json.load(config_buffer)
    cryolo_mode = utils.get_cryolo_mode(size_distr=size_distr, config_input_size=config["model"]["input_size"])
    if cryolo_mode == cryolo_mode.NON_SQUARE:
        ar = size_distr[0][0]/size_distr[0][1]
        if ar < 1:
            input_size = [int(config["model"]["input_size"] / ar), config["model"]["input_size"]]
        else:
            input_size = [config["model"]["input_size"], int(config["model"]["input_size"] * ar)]
        adjusted_size = config_tools.adjust_size(input_size)
        print("Your training input size",config["model"]["input_size"],"was adjusted to",adjusted_size)
        config["model"]["input_size"] = adjusted_size
        about["adjusted_input_size"] = adjusted_size

    # Read (first) image and check the image depth.
    first_image_path = img_paths[0]
    try:
        img_first = imagereader.image_read(first_image_path)
    except ValueError:
        sys.exit("Image " + first_image_path + " is not valid")
    if img_first is None:
        sys.exit("No valid image: " + first_image_path)

    if len(img_first.shape) == 2:
        depth = 1
    elif img_first.shape[2] == 1:
        depth = 1
    elif img_first.shape[2] > 3:
        depth = 1
    elif img_first.shape[2] == 3 and \
            np.all(img_first[:, :, 0] == img_first[:, :, 1]) and \
            np.all(
        img_first[:, :, 0] == img_first[:, :, 2]
    ):
        depth = 1
    else:
        depth = 3
    about["depth"] = depth
    #grid_w, grid_h = config_tools.get_gridcell_dimensions(config)

    #############################################
    # Read meta data about the model
    #############################################
    anchors = None
    yolo_kwargs = {}
    cryolo_version = None

    custom_params = utils.get_custom_paramters_from_model(weights_path)

    if "anchors" in custom_params:
        anchors = custom_params["anchors"]
    if "num_free_layers" in custom_params:
        yolo_kwargs["num_fine_tune_layers"] = custom_params["num_free_layers"]
    if "cryolo_version" in custom_params:
        cryolo_version = custom_params["cryolo_version"]
        about["model_cryolo_version"] = cryolo_version
    if "filament_model" in custom_params:
        filament_model = custom_params["filament_model"]
        about["filament_model"] = filament_model
    else:
        filament_model = False
        about["filament_model"] = False

    if cryolo_version is not None:
        print("Load crYOLO model which was trained with", cryolo_version)

    if anchors is None:
        #
        # TODO: Deprecated, anchors are now saved in the model and always defined.
        #
        anchors = utils.get_anchors(config, image_size=img_first.shape)
        print("Calculated Anchors using first image", anchors)
    else:
        print("Read Anchor from model", anchors)

    about["used_anchors"] = anchors

    if yolo is None:
        ###############################
        #   Make the model
        ###############################
        backend_weights = None
        if "backend_weights" in config["model"]:
            backend_weights = config["model"]["backend_weights"]
        from .frontend import YOLO

        yolo = YOLO(
            architecture=config["model"]["architecture"],
            input_size=config["model"]["input_size"],
            input_depth=depth,
            labels=["particle"],
            max_box_per_image=config["model"]["max_box_per_image"],
            anchors=anchors,
            backend_weights=backend_weights,
            pretrained_weights=weights_path,
            filament_model=filament_model,
            **yolo_kwargs
        )

        ###############################
        #   Load trained weights
        ###############################

        # USE MULTIGPU
        if num_gpus > 1:
            from keras.utils import multi_gpu_model

            parallel_model = multi_gpu_model(yolo.model, gpus=num_gpus)
            yolo.model = parallel_model
    else:
        yolo.anchors = anchors

    ##############################
    # Filter the data
    ##############################

    resize_to = None
    if num_patches == 1:
        # In case only one patch is used (should be default), the resizing can already
        # be done at the filtering step
        resize_to = config["model"]["input_size"]

    if MONITOR:
        # Monitor mode only works OTF
        otf = True

    if otf and not "filter" in config["model"]:
        print(
            "You specified the --otf option. However, filtering is not configured in your"
            "config line, therefore crYOLO will ignore --otf."
        )

    do_nn_filter = False
    filter_options = None
    if "filter" in config["model"]:
        filter_options = config["model"]["filter"]
        if otf == False:
            img_paths_filtered = do_filtering(
                img_paths=img_paths,
                filter_options=filter_options,
                resize_to=resize_to,
                num_cpus=num_cpus,
                         )
        else:
            img_paths_filtered = img_paths
    else:
        img_paths_filtered = img_paths
    ###############################
    #   Predict bounding boxes
    ###############################
    print("Reset progress bar: ( Progress: -1 % )")
    total_picked = 0
    boxes_to_write = []
    measured_times = []
    batchsize = num_patches * num_patches * num_images_batch_prediction
    skipped_images = []
    sum_del_not_fully_immersed = 0
    sum_del_min_distance = 0
    sum_del_out_of_size = 0
    boxes_per_image_dict = {}
    boxes_per_image_unfiltered_dict = {}

    total_num_batches = get_total_number_of_batches(img_paths_filtered,batchsize)

    batch_generator = generate_batches(img_paths_filtered, #pass a copy...
                         batchsize,
                         num_patches,
                         overlap,
                         otf,
                         config,
                         filter_options,
                         resize_to,
                         num_cpus,
                         )
    batch_num = 1
    if filament_mode:
        nms_thresh = 0.5
    else:
        nms_thresh = 0.3 # change back to 0.3 after testing!!!
    about["nms_thresh"] = nms_thresh

    for batch, tile_coord, slices_indicies, img_size, batch_img_paths in batch_generator:
        start = time.time()
        # Prediction

        boxes_per_image_nms_batch, boxes_per_image_unfiltered_batch = yolo.predict(
            batch,
            tile_coord,
            img_size,
            obj_threshold=obj_threshold,
            nms_threshold=nms_thresh,
            num_patches=num_patches,
            normalize_margin=normalization_margin,
            normalization=normalization,
        )

        # Now organize all boxes per image
        # In case of tomograms, there will be multiple box sets per image (on for each slice)
        particles_per_batch = 0

        images_completely_picked = []

        for batch_index, boxes in enumerate(boxes_per_image_nms_batch):
            particles_per_batch += len(boxes)
            key = os.path.basename(batch_img_paths[batch_index])
            if key in boxes_per_image_dict:
                boxes_per_image_dict[key]["boxes"].append(boxes)
                boxes_per_image_dict[key]["slice_indices"].append(slices_indicies[batch_index][0])
                boxes_per_image_unfiltered_dict[key]["boxes"].append(boxes_per_image_unfiltered_batch[batch_index])
            else:
                boxes_per_image_dict[key] = {
                    "boxes": [boxes],
                    "slice_indices": [slices_indicies[batch_index][0]]
                }
                boxes_per_image_unfiltered_dict[key] = {"boxes": [boxes_per_image_unfiltered_batch[batch_index]]}


            if slices_indicies[batch_index][0] == slices_indicies[batch_index][1]:
                images_completely_picked.append(key)


        # Generate datasets of boxes that contain all necessary meta data
        new_boxes_to_write = []
        if len(images_completely_picked) > 0:

            for preprocessed_img_pth in images_completely_picked:

                # Use original image data instead of filtered
                orig_img_path = utils.find_corresponding_path(img_paths,preprocessed_img_pth)

                # Use original image size instead of filtered image

                imgw, imgh = imagereader.read_width_height(
                    orig_img_path
                )

                box_pth = os.path.join(
                    os.path.dirname(orig_img_path),
                    "boxes",
                    os.path.splitext(os.path.basename(orig_img_path))[0]
                    + ".box",
                )

                boxes_filtered = boxes_per_image_dict[preprocessed_img_pth]["boxes"]
                boxes_unfiltered = boxes_per_image_unfiltered_dict[preprocessed_img_pth]["boxes"]

                boxes_on_one_image_to_write = {
                    "pth": box_pth,
                    "img_width": imgw,
                    "img_height": imgh,
                    "img_path": orig_img_path,
                    "boxes": boxes_filtered,
                    "boxes_unfiltered": boxes_unfiltered,
                    "slices_indices": boxes_per_image_dict[preprocessed_img_pth]["slice_indices"],
                }
                for boxes in boxes_filtered:
                    total_picked = total_picked + len(boxes)
                new_boxes_to_write.append(boxes_on_one_image_to_write)


        # Write to disk
        if "write_direct" in kwargs and len(images_completely_picked) > 0:
            if kwargs["write_direct"] == True:
                export_size = config_tools.get_box_size(config)[0]
                (
                    del_not_fully_immersed,
                    del_min_distance,
                    del_min_size,
                ) = picking_postprocessing(
                    picking_results=new_boxes_to_write,
                    export_size=export_size,
                    min_distance=kwargs["min_distance"],
                    min_size=kwargs["min_size"],
                    max_size=kwargs["max_size"],
                )

                sum_del_min_distance += del_min_distance
                sum_del_not_fully_immersed += del_not_fully_immersed

                sum_del_out_of_size += del_min_size

                prediction_result_to_disk(
                    kwargs["outdir"], new_boxes_to_write, write_empty=write_empty
                )

        boxes_to_write.extend(new_boxes_to_write)


        # Print progress
        prnt_progress = [
            particles_per_batch,
            "particles are found in image batch",
            batch_num,
            " / ",
            int(total_num_batches)
        ]

        if MONITOR == False:
            prnt_progress.append(" ( Progress: ")
            prnt_progress.append(
                int(float(batch_num) * 100 / total_num_batches)
            )

            prnt_progress.append("% )")
        print(*prnt_progress)
        batch_num += 1
        end = time.time()
        measured_times.append(end - start)

    # Run post-processing
    if len(skipped_images) > 0:
        print(
            "The following images were skipped because of errors during reading them:"
        )
        for img in skipped_images:
            print(img)

    print("#####################################")
    print(
        total_picked,
        "particles in total has been found",
        "(",
        int(np.sum(measured_times)),
        "seconds)",
    )

    if "write_direct" in kwargs and kwargs["write_direct"] == True:
        if sum_del_min_distance > 0:
            print(
                sum_del_min_distance,
                "particles were filtered because of the distance threshold",
                kwargs["min_distance"],
            )

        print(
            "Deleted",
            sum_del_not_fully_immersed,
            "particles as they were not fully immersed in the micrograph",
        )
        print(
            "Deleted",
            sum_del_out_of_size,
            "particles as they were out of specified size range",
        )
    print("#####################################")
    return boxes_to_write, about


def get_out_of_sizes_boxes(boxes, min_size=None, max_size=None):
    if min_size is None and max_size is None:
        return []

    out_of_size_boxes = []
    for box_index, box in enumerate(boxes):
        box_width = box.meta["boxsize_estimated"][0]
        box_height = box.meta["boxsize_estimated"][1]
        size = (box_width + box_height) / 2
        out_of_size = False

        if min_size:
            if size <= min_size:
                out_of_size = True

        if max_size:
            if size >= max_size:
                out_of_size = True

        if out_of_size:
            out_of_size_boxes.append(box_index)

    return out_of_size_boxes


def get_not_fully_immersed_box_indices(boxes, image_height, image_width):
    boxes_to_delete = []
    for box_index, box in enumerate(boxes):
        box_width = box.w
        box_height = box.h
        if box_width == 0 and box_height == 0:
            box_width = box.meta["boxsize_estimated"][0]
            box_height = box.meta["boxsize_estimated"][1]
        if (
            (box.x + box_width) >= image_width
            or box.x < 0
            or box.y < 0
            or (box.y + box_height) >= image_height
        ):
            boxes_to_delete.append(box_index)


    return boxes_to_delete



def trace_subset_filements(i):
    image_index = filament_tracers[i][0]
    frame_index = filament_tracers[i][1]
    traceing_results =filament_tracers[i][2].trace_filaments()
    return (image_index,frame_index,traceing_results)


if __name__ == "__main__":
    _main_()
