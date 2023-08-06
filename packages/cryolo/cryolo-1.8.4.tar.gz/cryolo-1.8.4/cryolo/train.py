"""
Skript to train crYOLO

Author: Thorsten Wagner
"""
#! /usr/bin/env python

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

from __future__ import print_function

import argparse
import json
import multiprocessing
import os

import numpy as np

import cryolo.config_tools as config_tools
import cryolo.imagereader as imagereader
import cryolo.lowpass as lowpass
import cryolo.preprocessing as preprocess
from . import utils
from gooey import Gooey, GooeyParser

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
try:
    os.environ["CUDA_VISIBLE_DEVICES"]
except KeyError:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

try:
    os.environ["CUDA_VISIBLE_DEVICES"]
except KeyError:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

try:
    os.environ["CRYOLO_USE_MULTITHREADING"]
except KeyError:
    os.environ["CRYOLO_USE_MULTITHREADING"] = "FALSE"

def create_parser(parser):
    """
    Adds argument groups to parser
    :param parser: The parser that is used to add argument groups
    :return: An updated parser
    """
    required_group = parser.add_argument_group(
        "Required arguments", "These options are mandatory to run crYOLO train"
    )

    required_group.add_argument(
        "-c",
        "--conf",
        required=True,
        help="Path to configuration file",
        widget="FileChooser",
        gooey_options={
            "validator": {
                "test": 'user_input.endswith("json")',
                "message": "File has to end with .json!",
            },
            "wildcard": "*.json",
        },
    )

    required_group.add_argument(
        "-w",
        "--warmup",
        type=int,
        required=True,
        default=5,
        help="Number of warmup epochs. Set it to zero if you fine tune a model.",
    )

    optional_group = parser.add_argument_group(
        "Optional arguments", "These options are optional to run crYOLO train"
    )

    optional_group.add_argument(
        "-g",
        "--gpu",
        default="",
        nargs="+",
        help="Specifiy which gpu(s) should be used. Multiple GPUs are separated by a whitespace. If not defined otherwise by your system, it will use GPU 0 by default.",
    )

    optional_group.add_argument(
        "-nc",
        "--num_cpu",
        type=int,
        default=-1,
        help="Number of CPUs used during training. By default it will use half of the available CPUs.",
    )

    optional_group.add_argument(
        "--gpu_fraction",
        type=float,
        default=1.0,
        help="Specify the fraction of memory per GPU used by crYOLO during training. Only values between 0.0 and 1.0 are allowed.",
        gooey_options={
            "validator": {
                "test": "0.0 <= float(user_input) <= 1.0",
                "message": "Must be between 0 and 1.0",
            }
        },
    )

    optional_group.add_argument(
        "-e",
        "--early",
        default=10,
        type=int,
        help="Early stop patience. If the validation loss did not improve longer than the early stop patience, "
        "the training is stopped.",
    )

    optional_group.add_argument(
        "--fine_tune",
        action="store_true",
        default=False,
        help="Set it to true if you only want to use the fine tune mode. "
        "When using the fine tune mode, only the last layers of your network are trained and you"
        'have to specify pretrained_weights (see action "config"->"Training options") '
        "You typically use a general model as pretrained weights.",
    )

    optional_group.add_argument(
        "-lft",
        "--layers_fine_tune",
        default=2,
        type=int,
        help="Layers to be trained when using fine tuning.",
    )

    optional_group.add_argument(
        "--cleanup",
        action="store_true",
        default=False,
        help="If true, it will delete the filtered images after training is done."
    )

    optional_group.add_argument(
        "--ignore_directions",
        action="store_true",
        default=False,
        help="When using filament training data, crYOLO will automatically detect that and train the"
             "model in wtih directional estimation included. If you use this option, this directional"
             "learning is skipped.",
    )

    deexsp_group = parser.add_argument_group(
        "Deprecated/Experimental/Special ",
        "Contains either deprecated / experimental or very special options.",
    )

    deexsp_group.add_argument(
        "--seed",
        type=int,
        default=10,
        help="Seed for random number generator. Mainly influences selection of validation images. Should be the same during different training runs!",
    )

    deexsp_group.add_argument(
        "--warm_restarts",
        action="store_true",
        help="Use warm restarts and cosine annealing during training",
    )

    deexsp_group.add_argument(
        "--skip_augmentation",
        action="store_true",
        default=False,
        help="Use it if you want to deactivate data augmentation during training.",
    )

def get_parser():
    """
    Creates parser
    :return: New parser
    """
    parser = GooeyParser(
        description="Train crYOLO model on any datasett",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    create_parser(parser)
    return parser

def get_model(
    config,
    depth,
    anchors,
    experimental_loss,
    do_fine_tune,
    num_fine_tune_layers,
    num_gpus,
    pretrained_weights,
    is_filament_training
):
    """
    Create the model for training/prediction

    :param config: Configuration dictonary
    :param depth: Image depth
    :param anchors: Anchors
    :param experimental_loss: True if the experimental loss should be used
    :param do_fine_tune: True if fine tuning should be done
    :param num_fine_tune_layers: Number of layers to fine tune
    :param num_gpus: List of GPU IDs to use
    :param pretrained_weights: Pretrained weights for initialization
    :return: Configuriered model
    """
    ###############################
    #   Construct the model
    ###############################
    backend_weights = None
    if "backend_weights" in config["model"]:
        backend_weights = config["model"]["backend_weights"]
    from cryolo.frontend import YOLO

    # import tensorflow as tf
    # graph = tf.Graph()
    # with graph.as_default():

    if num_gpus > 1:
        import tensorflow as tf

        with tf.device("/cpu:0"):
            yolo = YOLO(
                architecture=config["model"]["architecture"],
                input_size=config["model"]["input_size"],
                input_depth=depth,
                labels=config["model"]["labels"],
                max_box_per_image=config["model"]["max_box_per_image"],
                anchors=anchors,
                backend_weights=backend_weights,
                experimental_loss=experimental_loss,
                pretrained_weights=pretrained_weights,
                pretrained_weights_init=True,
                fine_tune=do_fine_tune,
                num_fine_tune_layers=num_fine_tune_layers,
                filament_model=is_filament_training
            )
    else:
        yolo = YOLO(
            architecture=config["model"]["architecture"],
            input_size=config["model"]["input_size"],
            input_depth=depth,
            labels=config["model"]["labels"],
            max_box_per_image=config["model"]["max_box_per_image"],
            anchors=anchors,
            backend_weights=backend_weights,
            experimental_loss=experimental_loss,
            pretrained_weights=pretrained_weights,
            pretrained_weights_init=True,
            fine_tune=do_fine_tune,
            num_fine_tune_layers=num_fine_tune_layers,
            filament_model=is_filament_training
        )

    # print a summary of the whole model
    yolo.model.summary()

    return yolo


def _main_():
    """
    Fake main function, initilazies gooey
    :return: None
    """
    start_method="spawn"
    try:
        os_start_method = os.environ["CRYOLO_MP_START"]
        if os_start_method in ["spawn","fork"]:
            start_method = os_start_method
    except:
        pass

    try:

        multiprocessing.set_start_method(start_method)
    except RuntimeError:
        print("Ignore set start method")

    import sys

    # if sys.argv[1] == "gui":
    if len(sys.argv) >= 2:
        if not "--ignore-gooey" in sys.argv:
            sys.argv.append("--ignore-gooey")

    # r'^\d+ particles are found in .* \( (\d+) % \)$'
    kwargs = {"terminal_font_family": "monospace", "richtext_controls": True}

    Gooey(
        main,
        program_name="crYOLO train",
        image_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), "../icons"),
        progress_regex=r"^.* \( Progress:\s+(-?\d+) % \)$",
        disable_progress_bar_animation=True,
        tabbed_groups=True,
        **kwargs
    )()




def main(args=None):
    """
    Main function. Read the arguments, start the program :-)
    :return: None
    """
    #import os
    import logging
    #logging.getLogger('tensorflow').disabled = True
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        pass
    import cryolo.utils as util

    util.check_for_updates()

    if args is None:
        parser = get_parser()
        args = parser.parse_args()

    ###############################
    #   Setup which GPU is used
    ###############################
    if isinstance(args.gpu, list):
        if len(args.gpu) == 1:
            str_gpus = args.gpu[0].strip().split(" ")
        else:
            str_gpus = [str(entry) for entry in args.gpu]
        num_gpus = len(str_gpus)
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)
    else:
        num_gpus = 1
        if args.gpu != -1 and len(args.gpu) > 0:
            str_gpus = str(args.gpu)
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)

    ###############################
    #   Setup amount of GPU memory used
    ###############################
    config_proto_args = {}
    if args.num_cpu != -1:
        config_proto_args["intra_op_parallelism_threads"] = args.num_cpu
        config_proto_args["inter_op_parallelism_threads"] = args.num_cpu
    if args.gpu_fraction < 1.0 and args.gpu_fraction > 0.0:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session

        config = tf.compat.v1.ConfigProto(**config_proto_args)

        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = args.gpu_fraction

        set_session(tf.compat.v1.Session(config=config))
    else:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session

        config = tf.compat.v1.ConfigProto(**config_proto_args)
        config.gpu_options.allow_growth = True

        set_session(tf.compat.v1.Session(config=config))

    early_stop = int(args.early)
    do_multiprocessing = False
    warm_restarts = args.warm_restarts

    do_augmentation = not args.skip_augmentation

    do_fine_tune = args.fine_tune
    num_fine_tune_layers = args.layers_fine_tune

    num_cpus = int(multiprocessing.cpu_count() / 2)
    if args.num_cpu != -1:
        num_cpus = args.num_cpu
    seed = args.seed

    experimental_loss = False



    ###############################
    #   Read configuration
    ###############################
    config_path = args.conf
    with open(config_path) as config_buffer:
        try:
            config = json.loads(config_buffer.read())
        except json.JSONDecodeError:
            print(
                "Your configuration file seems to be corruped. Please check if it is valid."
            )

    # Setup log dir
    if "other" in config and "log_path" in config["other"]:
        log_path = config["other"]["log_path"]
    else:
        log_path = "logs_cryolo/"

    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            import sys

            print(
                "Log path can't be created. Check your configuration ("
                + config_path
                + ")."
            )
            sys.exit(1)

    ###############################
    #   Write crYOLO command to disk
    ###############################
    import time
    import sys

    timestr = time.strftime("%Y%m%d-%H%M%S")
    utils.write_command(
        os.path.join(log_path, "cmdlogs/", "command_train_" + timestr + ".txt"),
        "cryolo_train.py " + " ".join(sys.argv[1:]),
    )

    ###############################
    #   Read number of warmup epochs
    ###############################
    if args.warmup is not None:
        warmup_epochs = int(args.warmup)
    else:
        if config["train"]["warmup_epochs"] is not None:
            warmup_epochs = config["train"]["warmup_epochs"]
            print("Read warmup by config")
        else:
            warmup_epochs = 0
            print("Set warmup to zero")

    if args.warmup is not None and do_fine_tune:
        warmup_epochs = 0
        print("Ignore warmup, as fine tuning is activated.")

    # Early stop should be at least the number of warmup epochs
    if early_stop < warmup_epochs:
        early_stop = warmup_epochs

    num_patches = config_tools.get_number_patches(config)
    experimental_loss = False

    if early_stop < warmup_epochs:
        early_stop = warmup_epochs

    # Check if directional estimation should ignore
    ignore_directions = args.ignore_directions
    ###############################
    #   Parse the annotations
    ###############################

    # Identify all image - annotation pair
    train_annot_pairs = preprocess.find_image_annotation_pairs_by_dir(os.path.realpath(config["train"]["train_annot_folder"]),
                                                                      os.path.realpath(config["train"]["train_image_folder"]))


    # Identifiy all image sizes:
    sizes = preprocess.get_image_size_distr([pair[0] for pair in train_annot_pairs])
    cryolo_mode = utils.get_cryolo_mode(size_distr=sizes, config_input_size=config["model"]["input_size"])

    print("###############################################")
    print("The following training image sizes were detected:")
    for size in sizes:
        print(size[0], "x", size[1], "( N:",size[2],")")
    print("")
    print("crYOLO will train in mode:", cryolo_mode.name)

    config["model"]["input_size"] = config_tools.get_adjusted_input_size(config)
    if cryolo_mode == utils.CryoloMode.NON_SQUARE:
        width = sizes[0][0]
        height = sizes[0][1]
        ar = height/width
        if ar < 1:
            input_size = [config["model"]["input_size"],config["model"]["input_size"] / ar]
        else:
            input_size = [config["model"]["input_size"] * ar,config["model"]["input_size"]]
        adjusted_size = config_tools.adjust_size(input_size)
        print("Your training input size",config["model"]["input_size"],"was adjusted to",adjusted_size,"(height, width)")
        config["model"]["input_size"]= adjusted_size

    print("###############################################")

    grid_w, grid_h = config_tools.get_gridcell_dimensions(config)

    # parse annotations of the training set
    parse_dict = preprocess.parse_annotation(
        train_annot_pairs,
        grid_dims=(grid_w, grid_h, num_patches),
        anchor_size=int(config["model"]["anchors"][0]),
    )
    train_imgs = parse_dict["images"]

    max_part = np.max([len(img["object"]) for img in train_imgs])
    is_filament_data = parse_dict["is_filament_data"]

    if max_part > config["model"]["max_box_per_image"]:
        print("The value for max_box_per_image", config["model"]["max_box_per_image"], "is to small for the given training data.")
        config["model"]["max_box_per_image"] = int(max_part*1.1)
        print("Set max_box_per_image to", config["model"]["max_box_per_image"])

    config["model"]["labels"] = ["particle"]

    if len(train_imgs) == 0:
        print("No image files were found.")
        import sys

        sys.exit(0)
    # parse annotations of the validation set, if any, otherwise split the training set
    if os.path.exists(config["valid"]["valid_annot_folder"]):

        valid_annot_pairs = preprocess.find_image_annotation_pairs_by_dir(
            os.path.realpath(config["valid"]["valid_annot_folder"]),
            os.path.realpath(config["valid"]["valid_image_folder"]))

        parse_dict = preprocess.parse_annotation(
            valid_annot_pairs,
            grid_dims=(grid_w, grid_h, num_patches),
            anchor_size=int(config["model"]["anchors"][0]),
        )
        valid_imgs = parse_dict["images"]
        valid_labels = parse_dict["labels"]
        if (
            len(valid_imgs) == 0
            or len(valid_labels) == 0
            or len(valid_labels) != len(valid_imgs)
        ):
            if len(valid_imgs) == 0:
                print(
                    "No validation images were found. Invalid validation configuration. Check your config file."
                )
            if len(valid_labels) == 0:
                print(
                    "No validation labels were found. Invalid validation configuration. Check your config file."
                )
    else:

        np.random.seed(seed)
        images_picked = [img for img in train_imgs if len(img["object"])>0]
        images_empty = [img for img in train_imgs if len(img["object"]) == 0]

        train_valid_split_picked = int(0.8 * len(images_picked))
        np.random.shuffle(images_picked)
        valid_imgs = images_picked[train_valid_split_picked:]
        train_imgs = images_picked[:train_valid_split_picked]


        if len(images_empty)>0:
            train_valid_split_empty = int(0.8 * len(images_empty))
            np.random.shuffle(images_empty)
            valid_imgs.extend(images_empty[train_valid_split_empty:])
            train_imgs.extend(images_empty[:train_valid_split_empty])

    if len(train_imgs) == 0:
        import sys
        print("Training data size is too small. Please pick at least two images / slices.")
        sys.exit(0)
    print("Validation set:", len(valid_imgs), "images")
    #####################################
    # Write runfile
    #####################################

    valid_imgs_paths = [item["filename"] for item in valid_imgs]
    valid_annot_paths = [{"path":item["boxpath"]} if "z" not in item else {"path:":item["boxpath"], "slice":item["z"]} for item in valid_imgs]
    train_imgs_paths = [item["filename"] for item in train_imgs]
    train_annot_paths = [{"path":item["boxpath"]} if "z" not in item else {"path": item["boxpath"], "slice": item["z"]} for item in train_imgs]

    runjson = {}
    runjson["run"] = {}
    runjson["run"]["valid_images"] = valid_imgs_paths
    runjson["run"]["valid_annot"] = valid_annot_paths
    runjson["run"]["train_images"] = train_imgs_paths
    runjson["run"]["train_annot"] = train_annot_paths

    runfiles_path = os.path.join(log_path, "runfiles/")
    if not os.path.exists(runfiles_path):
        os.mkdir(runfiles_path)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    runfile_path = os.path.join(runfiles_path, timestr + ".json")
    with open(runfile_path, "w") as outfile:
        json.dump(runjson, outfile, ensure_ascii=False, indent=4)
    print("Wrote runfile to: " + runfile_path)

    ##############################
    # Filter the data
    ##############################

    resize_to = None
    if num_patches == 1:
        # In case only one patch is used (should be default), the resizing can already
        # be done at the filtering step
        resize_to = config["model"]["input_size"]

    if "filter" in config["model"]:
        filter_options = config["model"]["filter"]
        if len(filter_options) > 2:
            model_path, overlap, nn_batch_size, filter_img_path = filter_options
            print("Filter data using noise2noise model: ", model_path)

            # Get set of unique filenames
            train_imgs_paths = list(set([img["filename"] for img in train_imgs]))

            filtered_paths = utils.filter_images_noise2noise_dir(
                img_paths=train_imgs_paths,
                output_dir_filtered_imgs=filter_img_path,
                model_path=model_path,
                padding=overlap,
                batch_size=nn_batch_size,
                resize_to=resize_to,
            )

            # Update paths of newly filtered images
            for img in train_imgs:
                img["filename"] = filtered_paths[train_imgs_paths.index(img["filename"])]

            valid_imgs_paths = list(set([img["filename"] for img in valid_imgs]))
            filtered_paths = utils.filter_images_noise2noise_dir(
                img_paths=valid_imgs_paths,
                output_dir_filtered_imgs=filter_img_path,
                model_path=model_path,
                padding=overlap,
                batch_size=nn_batch_size,
                resize_to=resize_to,
            )

            # Update paths of newly filtered images
            for img in valid_imgs:
                img["filename"] = filtered_paths[valid_imgs_paths.index(img["filename"])]


        else:
            cutoff, filter_img_path = filter_options
            start = time.time()
            lowpass.filter_images(
                images=train_imgs,
                filter_cutoff=cutoff,
                filter_tmp_path=filter_img_path,
                num_cpu=num_cpus,
                resize_to_shape=resize_to,
            )
            lowpass.filter_images(
                images=valid_imgs,
                filter_cutoff=cutoff,
                filter_tmp_path=filter_img_path,
                num_cpu=num_cpus,
                resize_to_shape=resize_to,
            )

            end = time.time()
            print("Time needed for filtering:", end - start)

    # Read first image and check the image depth.
    img_first = imagereader.image_read(train_imgs[0]["filename"], use_mmap=True)

    isgrey = False
    if len(img_first.shape) == 2:
        isgrey = True
    elif img_first.shape[0]==3 and np.all(img_first[:, :, 0] == img_first[:, :, 1]) and np.all(img_first[:, :, 0] == img_first[:, :, 2]
    ):
        isgrey = True
    elif len(img_first.shape)==3 and img_first.shape[0]>3:
        # Tomo data
        img_first = img_first[0,:,:]
        isgrey = True

    if isgrey:
        depth = 1
    else:
        depth = 3
    # As only on box size is expected, the anchor box size automatically
    anchors = utils.get_anchors(config, image_sizes=sizes)#

    # Get overlap patches
    overlap_patches = 0
    if "overlap_patches" in config["model"]:
        overlap_patches = int(config["model"]["overlap_patches"])
    elif not len(config["model"]["anchors"]) > 2:
        overlap_patches = config["model"]["anchors"][0]


    #  Get normalization option
    normalization_string = "STANDARD"
    if "norm" in config["model"]:
        normalization_string = config["model"]["norm"]

    ###############################
    # Start the training processn setup.
    ###############################
    pretrained_weights = None
    if os.path.exists(config["train"]["pretrained_weights"]):
        pretrained_weights = config["train"]["pretrained_weights"]

    if ignore_directions and is_filament_data:
        print("Ignoring directional filament information.")
    is_filament_model = is_filament_data and ignore_directions==False

    if is_filament_model:
        print("#############################")
        print("Filaments are used fore training. crYOLO will learn to estimate their directions "
              "directly. If you don't want this, use the --ignore_directions option.")
        print("#############################")
    import tensorflow as tf

    start = time.time()
    # graph = tf.Graph()
    yolo = get_model(
        config,
        depth,
        anchors,
        experimental_loss,
        do_fine_tune,
        num_fine_tune_layers,
        num_gpus,
        pretrained_weights,
        is_filament_model
    )

    # USE MULTIGPU
    parallel_model = None
    if num_gpus > 1:
        from keras.utils import multi_gpu_model

        parallel_model = multi_gpu_model(yolo.model, gpus=num_gpus, cpu_merge=False)
        config["train"]["batch_size"] = config["train"]["batch_size"]*num_gpus
    try:
        tf_log_path = os.path.join(log_path, "tensorflow/")
        if not os.path.exists(tf_log_path):
            os.mkdir(tf_log_path)
        yolo.train(
            train_imgs=train_imgs,
            valid_imgs=valid_imgs,
            train_times=config["train"]["train_times"],
            valid_times=config["valid"]["valid_times"],
            nb_epoch=config["train"]["nb_epoch"],
            learning_rate=config["train"]["learning_rate"],
            batch_size=config["train"]["batch_size"],
            warmup_epochs=warmup_epochs,
            object_scale=config["train"]["object_scale"],
            no_object_scale=config["train"]["no_object_scale"],
            coord_scale=config["train"]["coord_scale"],
            class_scale=config["train"]["class_scale"],
            saved_weights_name=config["train"]["saved_weights_name"],
            debug=config["train"]["debug"],
            log_path=tf_log_path,
            early_stop_thresh=early_stop,
            num_patches=num_patches,
            warm_restarts=warm_restarts,
            overlap_patches=overlap_patches,
            parallel_model=parallel_model,
            num_cpus=num_cpus,
            do_augmentation=do_augmentation,
            do_multiprocessing=do_multiprocessing,
            normalization=normalization_string,
            cryolo_mode=cryolo_mode,
            filament_model=is_filament_model,
        )
    except tf.errors.ResourceExhaustedError:
        print("############################")
        print("Not enough GPU memory. Try to reduce training batch size. ")
        print("############################")
        import sys

        sys.exit(0)

    end = time.time()

    # We need to do this, otherwise we get an exception at the end of the training...
    for p in multiprocessing.active_children():
        p.terminate()

    print("Time elapsed for training:", (end - start))
    if args.cleanup:
        print("#########################")
        print("Delete filtered images...")
        if os.path.exists(config["model"]["filter"][-1]):
            import shutil
            shutil.rmtree(config["model"]["filter"][-1])
        print("Done")
        print("#########################")



if __name__ == "__main__":
    start_method = "fork"
    try:
        os_start_method = os.environ["CRYOLO_MP_START"]

        if os_start_method in ["spawn","fork"]:
            start_method = os_start_method
    except:
        pass

    multiprocessing.set_start_method(start_method)

    _main_()


