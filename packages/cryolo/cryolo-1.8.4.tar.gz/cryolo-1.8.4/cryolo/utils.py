"""
Abitary Utils for crYOLO
"""
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
import numpy as np
import sys
import copy

from . import imagereader
import urllib.request, json
from sklearn import mixture
from typing import List, Dict, Tuple

class BoundBox:
    """
    A bounding box of a particle
    """

    def __init__(self, x, y, w, h, c=None, classes=None, z=None, depth=None):
        """
        Creates a BoundBox
        :param x: x coordinate of the center
        :param y: y coordinate of the center
        :param w: width of box
        :param h: height of the box
        :param c: confidence of the box
        :param classes: Class of the BoundBox object
        """

        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.depth = depth
        self.meta = {}

        self.c = c
        self.classes = classes

        self.label = -1
        self.score = -1
        self.info = None  # helping data during processing

    def get_label(self):
        """

        :return: Class with highest probability
        """
        if self.label == -1:
            self.label = np.argmax(self.classes)

        return self.label

    def get_score(self):
        """
        :return: Probability of the class
        """
        # if self.score == -1:
        self.score = self.classes[self.get_label()]

        return self.score

class Filament:
    """
    Filament object
    """

    def __init__(self, boxes: List[BoundBox]=None):
        """
        Constructor
        :param boxes: Boxes of the filament
        """
        self.meta = {}

        if boxes is None:
            self.boxes: List[BoundBox] = []
        else:
            self.boxes = boxes

    def add_box(self, box: BoundBox):
        """
        Appends a box to the filament box list.
        :param box: box to append
        :return: filament object
        """
        self.boxes.append(box)
        return self

    def get_num_boxes(self):
        """
        :return: Number of boxes that belong the filament

        """
        return len(self.boxes)

    def does_overlap(self, box: BoundBox, threshold: float):
        """
        Compares a box with all other boxes in the filament box list and calculates the IOU overlap.
        This overlap if compared to a threshold.
        :param box: Box to compare
        :param threshold: IOU Threshold
        :return: True if IOU >= threshold
        """

        for filbox in self.boxes:
            if bbox_iou(filbox, box) >= threshold:
                return True
        return False


from enum import Enum
class CryoloMode(Enum):

    FIXED_SIZE=1
    MIXED_ASPECT_RATIO=2
    SQUARE=3
    NON_SQUARE=4


def getEquidistantBoxes(box1, box2, num_boxes):
    """
    Create multiple boxes between box1 and box2 with equidistant boxes
    :param box1: First box
    :param box2: Second box
    :param num_boxes: number of boxes
    :return: List of N=num_boxes equidistant boxes between box1 and box2
    """
    dat = [np.linspace(box1.x, box2.x, num_boxes + 1, endpoint=True), np.linspace(box1.y, box2.y, num_boxes + 1, endpoint=True)]
    if box1.z is not None and box2.z is not None:
        dat.append(np.linspace(box1.z, box2.z, num_boxes + 1, endpoint=True))

    points = zip(*dat)
    new_boxes = []
    if box1.c is None or box2.c is None:
        c = 1
    else:
        c = (box1.c + box2.c) / 2

    num_boxes = None
    if "num_boxes" in box1.meta and "num_boxes" in box2.meta:
        num_boxes = (box1.meta["num_boxes"]+box2.meta["num_boxes"])//2

    angle = None
    if "angle" in box1.meta and "angle" in box2.meta:
        # replace this with proper angle average
        angle = box1.meta["angle"]

    classes = ""
    if box1.classes:
        classes = box1.classes
    w = box1.w
    h = box1.w
    depth = box1.depth
    for point in points:
        b = BoundBox(x=point[0], y=point[1], w=w, h=h, c=c, depth=depth, classes=classes)
        if len(point) == 3:
            b.z = point[2]
        if num_boxes is not None:
            b.meta["num_boxes"] = num_boxes
        if angle is not None:
            b.meta["angle"] = angle
        new_boxes.append(b)
    return new_boxes


def resample_filaments(new_filaments, box_distance):
    """
    Resample a list of filaments
    :param new_filaments: List of filament
    :param box_distance: Target distance between two boxes
    :return: List of resampled filaments
    """
    res_fils = [
        resample_filament(fil, box_distance) for fil in new_filaments
    ]

    res_fils = [fil for fil in res_fils if fil is not None and fil.boxes]
    return res_fils


def resample_filament_(filament, dist):

    dim = 2
    if filament.boxes[0].z is not None:
        dim = 3
    fil = np.zeros((len(filament.boxes),dim))
    filwidth = filament.boxes[0].w
    filheight = filament.boxes[0].h
    fildepth = filament.boxes[0].depth
    filclass = filament.boxes[0].classes

    for boxi, box in enumerate(filament.boxes):
        fil[boxi, 0] = box.x
        fil[boxi, 1] = box.y
        if dim == 3:
            fil[boxi, 2] = box.z

    def interpolate(points, new_dist):
        new_points = []

        new_points.append(np.atleast_2d(points[0, :3]))

        for u in range(1, points.shape[0]):
            dist = np.linalg.norm(new_points[-1] - points[u, :])
            if dist > new_dist:
                while dist > new_dist:
                    dist = np.linalg.norm(points[u] - new_points[-1])
                    normvec = (points[u] - new_points[-1]) / dist
                    next_point = new_points[-1] + new_dist * normvec
                    new_points.append(np.atleast_2d(next_point))
            elif dist == new_dist:
                new_points.append(np.atleast_2d(points[u, :]))

        result = np.concatenate(new_points)
        return result


    interpolated_fil = interpolate(
        fil[:, :3],
        new_dist=dist
    )

    boxes = []
    for row in interpolated_fil:
        z=None
        if dim == 3:
            z = row[2]

        boxes.append(BoundBox(x=row[0],y=row[1],z=z,w=filwidth,h=filheight,depth=fildepth,classes=filclass))
    inter_filament = Filament(boxes)
    inter_filament.meta = filament.meta
    return inter_filament


def resample_filament(filament : Filament, new_distance : float):
    if len(filament.boxes)<=1:
        return filament
    from scipy.interpolate import interp1d
    import numpy as np


    x = [box.x for box in filament.boxes]
    y = [box.y for box in filament.boxes]
    z = None
    if filament.boxes[0].z is not None and np.isnan(filament.boxes[0].z) == False:
        z = [box.z for box in filament.boxes]

    # Linear length on the line
    sqsum = np.ediff1d(x, to_begin=0) ** 2 + np.ediff1d(y, to_begin=0) ** 2
    if z is not None:
        sqsum += np.ediff1d(z, to_begin=0) ** 2

    distance_elem = np.cumsum(np.sqrt(sqsum))
    total_elength = distance_elem[-1]


    distance = distance_elem / distance_elem[-1]  # normalized
    fx, fy = interp1d(distance, x), interp1d(distance, y)
    if z is not None:
        fz = interp1d(distance, z)

    num = int(total_elength / new_distance) +1

    alpha = np.linspace(0, 1, num)

    x_regular, y_regular = fx(alpha), fy(alpha)
    if z is not None:
        z_regular = fz(alpha)
    new_boxes = []

    for i in range(len(x_regular)):

        second_box_index = np.argmax(distance >= alpha[i])
        first_box_index = second_box_index - 1

        if first_box_index < 0:
            first_box_index = 0
            second_box_index = 1
        box1 = filament.boxes[first_box_index]
        box2 = filament.boxes[second_box_index]
        c = None
        if box1.c is not None and box2.c is not None:
            c = (box1.c + box2.c)/2

        num_boxes = None
        if "num_boxes" in box1.meta and "num_boxes" in box2.meta:
            num_boxes = (box1.meta["num_boxes"] + box2.meta["num_boxes"]) // 2

        angle = None
        if "angle" in box1.meta and "angle" in box2.meta:
            # replace this with proper angle average
            angle = box1.meta["angle"]

        classes = ""
        if box1.classes:
            classes = box1.classes

        w = (box1.w+box2.w)/2
        h = (box1.h+box2.h)/2
        depth = None
        if box1.depth is not None and box2.depth is not None:
            depth = (box1.depth+box2.depth)/2

        b = BoundBox(x=x_regular[i], y=y_regular[i], w=w, h=h, c=c, depth=depth, classes=classes)
        if z is not None:
            b.z = z_regular[i]
        if num_boxes is not None:
            b.meta["num_boxes"] = num_boxes
        if angle is not None:
            b.meta["angle"] = angle
        new_boxes.append(b)

    return Filament(new_boxes)

def resample_filament_old(filament, distance):
    """
    Resamples a filament. The new filament will have a specified distance between the boxes.
    :param filament: Target filament
    :param distance: Distance between two adjacent boxes.
    :return: Resampeld filament
    """
    if len(filament.boxes)==1:
        return filament
    # Find two boxes with maximum distance
    boxes = filament.boxes
    max_distance = -1
    max_boxa = None
    for i in range(len(boxes)):
        for j in range(len(boxes)):
            if i == j:
                continue
            dist = box_squared_distance(boxes[i], boxes[j])
            if dist > max_distance:
                max_boxa = i
                max_distance = dist
    if max_boxa is not None:
        # Construct a polyline, start from max_boxa
        polyline = []
        polyline.append(boxes[max_boxa])
        assigned_boxes = []
        assigned_boxes.append(max_boxa)
        last_appended_box = boxes[max_boxa]
        last_appended_index = max_boxa
        added_new = True

        while added_new:
            min_distance = 99999999
            nearest_box_index = None
            added_new = False
            for i in range(len(boxes)):
                if i == last_appended_index:
                    continue
                if i in assigned_boxes:
                    continue

                measured_distance = box_squared_distance(last_appended_box, boxes[i])

                if measured_distance < min_distance:
                    nearest_box_index = i
                    min_distance = measured_distance

            if nearest_box_index is not None:
                polyline.append(boxes[nearest_box_index])
                assigned_boxes.append(nearest_box_index)
                last_appended_box = boxes[nearest_box_index]
                last_appended_index = nearest_box_index
                added_new = True

        # Create new boxes based on the polyline
        new_boxes_candidates = []
        sqdistance = distance * distance

        for i in range(len(polyline) - 1):
            eq_boxes = getEquidistantBoxes(polyline[i], polyline[i + 1], num_boxes=100)
            new_boxes_candidates.extend(eq_boxes)
        new_boxes = []
        dist = -1
        for box in new_boxes_candidates:
            if dist == -1:
                new_boxes.append(box)
                dist = 0
            else:
                dist = box_squared_distance(new_boxes[len(new_boxes) - 1], box)
                if dist >= sqdistance:
                    new_boxes.append(box)

        new_filament = Filament()
        for box in new_boxes:
            new_filament.add_box(box)

        return new_filament
    return None

def get_cryolo_mode(size_distr, config_input_size):
    square_data_available = any([size[0] == size[1] for size in size_distr])
    non_square_data_available = any([size[0] != size[1] for size in size_distr])

    if type(config_input_size) == list:
        return CryoloMode.FIXED_SIZE

    if (square_data_available and non_square_data_available) or \
            (non_square_data_available and len(size_distr)>1):
        return CryoloMode.MIXED_ASPECT_RATIO

    if square_data_available and not non_square_data_available:
        return CryoloMode.SQUARE

    if not square_data_available and non_square_data_available and len(size_distr)==1:
        return CryoloMode.NON_SQUARE

def get_custom_paramters_from_model(model_path):
    import h5py
    params_dict = {}
    with h5py.File(model_path, mode="r") as f:
        if "anchors" in f:
            params_dict["anchors"] = list(f["anchors"])
        if "num_free_layers" in f:
            params_dict["num_free_layers"] = int(list(f["num_free_layers"])[0])
        if "cryolo_version" in f:
            params_dict["cryolo_version"] = list(f["cryolo_version"])[0].decode("utf-8")
        if "filament_model" in f:
            params_dict["filament_model"] = bool(list(f["filament_model"])[0])

    return params_dict
def anchor_to_boxsize(anchor_dim,grid_dim, input_image_dim):
    """
    COnverts network anchors back to box size
    :param anchor_dim
    :param grid_dim: Grid dimension
    :param input_image_dim: Input image dimension
    :return: box width box height
    """
    import cryolo.config_tools as config_tools
    grid_w, grid_h = grid_dim #config_tools.get_gridcell_dimensions(config)
    img_width,img_height = input_image_dim
    anchor_width, anchor_height = anchor_dim
    cell_w = img_width / grid_w
    cell_h = img_height / grid_h
    box_width = anchor_width*cell_w
    box_height = anchor_height*cell_h
    return box_width,box_height

def get_anchors(config, path_weights=None, image_sizes=None):
    '''
    Calculates the anchors.
    When fixed size mode ...
    When non-square mode...
    When square-mode ...
    When mixed-size mode

    :param config:
    :param path_weights:
    :param image_size:
    :return:
    '''
    import cryolo.config_tools as config_tools

    is_single_anchor = len(config["model"]["anchors"]) == 2
    num_patches = 1
    if "num_patches" in config["model"]:
        num_patches = config["model"]["num_patches"]

    grid_w, grid_h = config_tools.get_gridcell_dimensions(config)
    anchors = None

    if path_weights:
        import h5py

        with h5py.File(path_weights, mode="r") as f:
            try:
                anchors = list(f["anchors"])
            except KeyError:
                anchors = None

    if is_single_anchor and anchors is None:

        # if single size, use the it as given
        # if multi-size, use the average length of the short side
        #
        if len(image_sizes) == 1:
            img_width = float(image_sizes[0][1]) / num_patches
            img_height = float(image_sizes[0][0]) / num_patches
        else:
            sum_size = 0
            sum_num_images = 0
            for img_info in image_sizes:
                if img_info[0]>img_info[1]:
                    sum_size += img_info[1] * img_info[2]
                else:
                    sum_size += img_info[0] * img_info[2]
                sum_num_images += img_info[2]
            mean_size = int(sum_size/sum_num_images)
            img_width = mean_size
            img_height = mean_size


        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        box_width, box_height = config_tools.get_box_size(config)

        anchor_width = 1.0 * box_width / cell_w
        anchor_height = 1.0 * box_height / cell_h
        anchors = [anchor_width, anchor_height]
    elif anchors is None:
        img_width = 4096.0 / num_patches
        img_height = 4096.0 / num_patches
        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        anchors = np.array(config["model"]["anchors"], dtype=float)
        anchors[::2] = anchors[::2] / cell_w
        anchors[1::2] = anchors[1::2] / cell_h

    return anchors


def box_squared_distance(boxa, boxb):
    """
    calculates the squared distance between the center of two boxes.
    :param boxa: First box
    :param boxb: Second box
    :return: Squared distance between boxa and boxb
    """
    sqd = np.square(boxa.x - boxb.x) + np.square(boxa.y - boxb.y)

    if boxa.z is not None and boxb.z is not None and np.isnan(boxa.z)==False and np.isnan(boxb.z)==False:
        sqd = sqd + np.square(boxa.z - boxb.z)
    return sqd

def get_normalization_func(normalization):
    if normalization == "STANDARD":
        norm_func = normalize
    elif normalization == "GMM":
        norm_func = normalize_gmm
    else:
        print("Normalization option ", normalization, "unknown. Check your config file.")
        import sys
        sys.exit(1)
    return norm_func

def normalize_gmm(image, margin_size=0):


    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]

    clf = mixture.GaussianMixture(n_components=2, covariance_type='diag')
    clf.fit(np.expand_dims(image[mask].ravel()[::15], axis=1))
    mean = None
    var = None
    if (clf.means_[1, 0]>clf.means_[0, 0]):
        mean = clf.means_[1, 0]
        var = clf.covariances_[1, 0]
    else:
        mean = clf.means_[0, 0]
        var = clf.covariances_[0, 0]
    #print(mean,var,np.sqrt(var))
    image = (image - mean) / (2*3*np.sqrt(var))

    return image

def normalize(image, margin_size=0):
    """
    Normalize an image. If wanted, a specified relative margin can be ignored.
    :param image: Image to normalize
    :param margin_size: Relative size of the margin to be ignored during normalization. Number between 0 - 1.
    :return: Normalized image
    """
    if margin_size < 0 or margin_size > 1:
        print("Normalization has to be between 0 and 1.")
        if margin_size < 0:
            margin_size = 0
        else:
            margin_size = 1
        print("Set it to", margin_size)

    if not np.issubdtype(image.dtype, np.float32):
        image = image.astype(np.float32)
    mask = np.s_[
        int(image.shape[0] * (margin_size)) : int(image.shape[0] * (1 - margin_size)),
        int(image.shape[1] * margin_size) : int(image.shape[1] * (1 - margin_size)),
    ]
    img_mean = np.mean(image[mask])
    img_std = np.std(image[mask])

    image = (image - img_mean) / (3 * 2 * img_std+0.000001)

    return image


def bbox_iou(box1: BoundBox, box2: BoundBox):
    """
    Calculates the intersection of union for two boxes.
    :param box1: First box
    :param box2: Second box
    :return: Intersection of union
    """
    x1_min = box1.x - box1.w / 2
    x1_max = box1.x + box1.w / 2
    y1_min = box1.y - box1.h / 2
    y1_max = box1.y + box1.h / 2

    x2_min = box2.x - box2.w / 2
    x2_max = box2.x + box2.w / 2
    y2_min = box2.y - box2.h / 2
    y2_max = box2.y + box2.h / 2

    intersect_w = interval_overlap([x1_min, x1_max], [x2_min, x2_max])
    intersect_h = interval_overlap([y1_min, y1_max], [y2_min, y2_max])

    intersect = intersect_w * intersect_h

    union = box1.w * box1.h + box2.w * box2.h - intersect

    return float(intersect) / union


def interval_overlap(interval_a, interval_b):
    """
    Calculates the overlap between two intervals
    :param interval_a: Tuple with two elements (lower and upper bound)
    :param interval_b: Tuple with two elements (lower and upper bound)
    :return: Overlap between two intervals
    """
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2, x4) - x1
    else:
        if x2 < x3:
            return 0
        else:
            return min(x2, x4) - x3


def sigmoid(x):
    """
    Sigmoid function
    :param x: argument
    :return: sigmoid of x
    """
    return 1.0 / (1.0 + np.exp(-x))


def get_num_fine_tune_layers(path_weights):
    import h5py

    with h5py.File(path_weights, mode="r") as f:
        try:
            num_free_layers = int(list(f["num_free_layers"])[0])
        except KeyError:
            num_free_layers = None
    return num_free_layers


def filter_image_noise2noise(img_path, model_path, padding=15, batch_size=4, resize_to=None):
    """
    Filters an images using JANNI (noise2noise implementation)
    :param img_path: Input image
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :return: Denoised image
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    image = imagereader.image_read(img_path)
    fitlered_img = janni_predict.predict_np(
        model, image, patch_size=(1024, 1024), padding=padding, batch_size=batch_size
    )



    return fitlered_img

def filter_images_lowpass(
    img_paths, output_dir_filtered_imgs, cutoff, num_cpus=-1, otf=False, resize_to=None
):
    import os
    import multiprocessing
    from . import lowpass

    """
    Filteres a list of images and return a new list with the paths to the filtered images.

    :param img_paths: Path to images to filter
    :param output_dir_filtered_imgs: Output directory to save the filtered images
    :param cutoff: Absolute cutoff frequency (0-0.5)
    :return: List of paths to the filtered images
    """
    if not otf and not os.path.isdir(output_dir_filtered_imgs):
        os.makedirs(output_dir_filtered_imgs)

    arg_tubles = []
    for img_id, img_pth in enumerate(img_paths):
        if os.path.basename(img_pth)[0] != ".":
            if otf:
                arg_tubles.append((img_pth, cutoff, resize_to))
            else:
                arg_tubles.append(
                    (
                        img_pth,
                        cutoff,
                        output_dir_filtered_imgs,
                        img_id + 1,
                        len(img_paths),
                        resize_to,
                    )
                )

    num_processes = int(multiprocessing.cpu_count() / 2)
    if num_cpus != -1:
        num_processes = num_cpus

    #num_processes = 1
    #maxtaskperchild = max(1,int(np.ceil(len(arg_tubles)/num_processes)))

    pool = multiprocessing.Pool(
        maxtasksperchild=None,
        processes=num_processes,
    )

    if otf:
        filtered_images = pool.starmap(
            lowpass.filter_single_image, arg_tubles, chunksize=1
        )

    else:
        filtered_images = pool.starmap(
            lowpass.filter_single_image_and_write_to_disk, arg_tubles, chunksize=1
        )
    pool.close()
    pool.join()

    filtered_images = [img for img in filtered_images if img is not None]
    return filtered_images


def filter_images_noise2noise_dir(
    img_paths,
    output_dir_filtered_imgs,
    model_path,
    padding=15,
    batch_size=4,
    resize_to=None,
):
    """
    Filters multiple images using JANNI (noise2noise implementation) and save it to disk
    :param img_paths: List of images paths
    :param output_dir_filtered_imgs: Path to write denoised images
    :param model_path: Path to JANNI model
    :param padding: Padding to reduce edge effects
    :param batch_size: How many batches used in denoising
    :param resize_to: Size to which to output is resized
    :return:
    """
    import h5py
    from janni import predict as janni_predict
    from janni import models as janni_models

    with h5py.File(model_path, mode="r") as f:
        try:
            import numpy as np

            model = str(np.array((f["model_name"])))
            patch_size = tuple(f["patch_size"])
        except KeyError:
            print("Not supported filtering model. Stop.")
            sys.exit(0)

    if model == "unet":
        model = janni_models.get_model_unet(input_size=patch_size)
        model.load_weights(model_path)
    else:
        print("Not supported model", model, "Stop")
        sys.exit(0)

    filtered_paths = janni_predict.predict_list(
        image_paths=img_paths,
        output_path=output_dir_filtered_imgs,
        model=model,
        patch_size=patch_size,
        padding=padding,
        batch_size=batch_size,
        output_resize_to=resize_to,
        sliceswise=True
    )

    return filtered_paths


def non_maxima_suppress_fast(boxes, number_classes, nms_threshold, obj_threshold):
    for c in range(number_classes):
        sorted_indices = list(reversed(np.argsort([box.classes[c] for box in boxes])))
        boxes_data = np.empty(shape=(len(boxes), 7))
        for i, sorted_index in enumerate(sorted_indices):
            boxes_data[i, 0] = boxes[sorted_index].x
            boxes_data[i, 1] = boxes[sorted_index].y
            boxes_data[i, 2] = boxes[sorted_index].w
            boxes_data[i, 3] = boxes[sorted_index].h
            boxes_data[i, 4] = boxes[sorted_index].classes[c]
            boxes_data[i, 5] = sorted_index
            boxes_data[i, 6] = i

        for i in range(len(boxes_data)):
            box_i = boxes_data[i, :]
            if box_i[4] == 0:
                continue
            else:
                other_box = boxes_data[(i + 1):]
                if other_box.shape[0] > 0:
                    boxes_i_rep = np.array([box_i] * len(other_box))
                    ious = bbox_iou_vec(boxes_i_rep, other_box)
                    boxes_data[other_box[ious >= nms_threshold, 6].astype(int), 4] = 0

        for row in boxes_data[boxes_data[:, 4] == 0]:
            boxes[row[5].astype(int)].classes[c] = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [copy.copy(box) for box in boxes if box.get_score() > obj_threshold]

    return boxes

def overlapping_boxes_indicis(fildata_a: np.array, fildata_b: np.array, nms_thresh: float) -> List[Tuple[int, int, float]]:
    # Returns the number of boxes for which can be found pair

    longfil = fildata_a
    shortfil = fildata_b
    swapped=False
    if len(fildata_b)>len(fildata_a):
        longfil = fildata_b
        shortfil = fildata_a
        swapped=True

    num_overlapping = 0
    overlapping_indices = []
    for rowindex, row in enumerate(shortfil):
        boxes_i_rep = np.array([row] * len(longfil))
        ious = bbox_iou_vec_3d(boxes_i_rep, longfil)

        if swapped:
            aindex = rowindex
            bindex = np.argmax(ious)
            maxiou = ious[bindex]
        else:
            aindex = np.argmax(ious)
            bindex = rowindex
            maxiou = ious[aindex]

        if maxiou>nms_thresh:
            overlapping_indices.append((aindex,bindex,maxiou))

        if np.sum(ious>nms_thresh) > 0:
            num_overlapping = num_overlapping +1
    return overlapping_indices

def filament_to_array(fil):
    boxes_data = np.empty(shape=(len(fil.boxes), 6))
    for i, box in enumerate(fil.boxes):
        boxes_data[i, 0] = box.x
        boxes_data[i, 1] = box.y
        boxes_data[i, 2] = box.z
        boxes_data[i, 3] = box.w
        boxes_data[i, 4] = box.h
        boxes_data[i, 5] = box.depth
    return boxes_data

def get_consecutive_subarrays(number_array_1d: np.array) -> np.array:
    '''
    Get list of sub-arrays with consecutive numbers e.g
    [0,1,2,5,6,7] -> [[0,1,2], [5,6,7]]
    :param number_array_1d: List of numbers
    :return: List of sub-arrays that have consecutive numbering
    '''

    split_indices = np.where((number_array_1d[1:] - number_array_1d[:-1]) > 1)[0]

    #split_indices = np.append(split_indices, len(overlapping_indicis) - 1)
    return np.split(number_array_1d, split_indices + 1)


def get_closest_point_distance(pointsetA : np.array, pointsetB : np.array) -> float:

    from scipy.spatial import distance

    mdist = distance.cdist(pointsetA, pointsetB)

    return min(mdist.min(axis=1))

def add_metainfo_for_merging(filament, id, parent_filament):
    filament.meta["merge_fid"] = id[0]
    id[0] = id[0] + 1
    filament.meta["merge_parent_ids"] = []
    filament.meta["merge_does_not_overlap_ids"] = set()
    if parent_filament is not None:
        filament.meta["merge_parent_ids"].append(parent_filament.meta["merge_fid"])
    return filament

def create_filament_for_merging(boxes, id, parent_filament):
    f = Filament(boxes)
    f = add_metainfo_for_merging(f, id, parent_filament)
    return f

def set_not_overlapping_pair(filament_a: Filament, filament_b: Filament):

    filament_a.meta["merge_does_not_overlap_ids"].add(filament_b.meta['merge_fid'])
    filament_a.meta["merge_does_not_overlap_ids"].update(filament_b.meta['merge_parent_ids'])

    filament_b.meta["merge_does_not_overlap_ids"].add(filament_a.meta['merge_fid'])
    filament_b.meta["merge_does_not_overlap_ids"].update(filament_a.meta['merge_parent_ids'])

def could_overlap_by_meta(filament_a: Filament, filament_b: Filament):

    if filament_a.meta["merge_fid"] in filament_b.meta["merge_does_not_overlap_ids"]:
        return False

    if filament_b.meta["merge_fid"] in filament_a.meta["merge_does_not_overlap_ids"]:
        return False

    for pid in filament_a.meta["merge_parent_ids"]:
        if pid in filament_b.meta["merge_does_not_overlap_ids"]:
            return False

    for pid in filament_b.meta["merge_parent_ids"]:
        if pid in filament_a.meta["merge_does_not_overlap_ids"]:
            return False

    return True



def merge_filaments_3d(filaments, iou_threshold, merge_threshold, window_radius, box_distance, partial = False):
    """

    :param filaments: List of filaments
    :param iou_threshold: IOU treshold. Boxes with a IOU higher than this value are condsidered as the same boxes
    :param merge_threshold: Filaments with a overlapping score hight than this value get merged
    :param window_radius: Window radius for averaging
    :param box_distance: Resampling distance after merging.
    :return:
    """

    # For each filament pair:
    #   Calculate the number of boxes that have pairs in the other filament
    #   Add to overlapping matrix
    # Start with the longest filament and merge all with overlapping > T
    # Repeat procedure with not yet merged filements

    def merge_filaments(filaments, window_size, box_distance):
        """
        Merge a set of filaments by averaging along
        the major direction

        :param filaments: List of filaments
        :param window_size: Window radius for average
        :param box_distance: box distance between two adjacent boxes after merging.
        :return:
        """
        # sort major eigenvector
        # run moving average
        if len(filaments) == 1:
            return filaments

        allboxes = []
        weights = []
        subs = []
        for fil in filaments:
            allboxes.extend(fil.boxes)
            weights.extend([box.meta['num_boxes'] for box in fil.boxes])
            if "group3d_fids" in fil.meta:
                subs.extend(fil.meta["group3d_fids"])
        boxsize = allboxes[0].w #its square...


        A = np.zeros((len(allboxes),4))
        weights = np.array(weights)
        for i,box in enumerate(allboxes):
            A[i, 0] = box.x
            A[i, 1] = box.y
            A[i, 2] = box.z
            A[i, 3] = box.c

        Acentered = A[:,:3] - A[:,:3].mean(axis=0)
        Acov = np.matmul(Acentered.T, Acentered)
        evals, evecs = np.linalg.eigh(Acov)
        eigvect = evecs[:, np.argmax(evals)]

        dotproducts = np.matmul(Acentered, eigvect)
        boxes3d = []
        N= max(1,int((max(dotproducts)-min(dotproducts))/(0.5*box_distance)))
        sample_points = np.linspace(min(dotproducts),max(dotproducts),N)
        for i in sample_points:#range(int(min(dotproducts)), int(max(dotproducts))+1):

            lower = i - window_size / 2
            upper = i + window_size / 2
            window_elements = np.logical_and(dotproducts > lower, dotproducts < upper)
            if np.sum(window_elements) > 0:

                x3d = np.average(A[window_elements][:,0], weights=weights[window_elements]) # np.mean(A[window_elements][:,0])
                y3d = np.average(A[window_elements][:,1], weights=weights[window_elements])
                z3d = np.average(A[window_elements][:,2], weights=weights[window_elements])
                conf3d = np.average(A[window_elements][:,3], weights=weights[window_elements])
                box3d = BoundBox(x=x3d, y=y3d, z=z3d, w=boxsize, h=boxsize, depth=boxsize, c=conf3d)
                box3d.meta["num_boxes"] = np.sum(np.unique(weights[window_elements]))

                if len(boxes3d) == 0:
                    boxes3d.append(box3d)
                elif not np.allclose(
                        [boxes3d[-1].x, boxes3d[-1].y, boxes3d[-1].z],
                        [x3d, y3d, z3d]
                ):
                    boxes3d.append(box3d)
                else:
                    pass

        new_fil = Filament(boxes=boxes3d)
        new_fil = resample_filaments([new_fil], box_distance)
        new_fil[0].meta["group3d_fids"] = subs
        return new_fil



    def get_overlapping_matrix_and_tubles(filaments: List[Filament]) -> Tuple[np.array, Dict]:
        #############################
        #  Build up overlapping matrix
        #############################
        overlapping_factor_matrix = np.eye(len(filaments))
        overlapping_tubles = {}


        for i in tqdm.tqdm(list(range(len(filaments) - 1)), desc="Updating overlapping factor matrix"):


            fildat_a = filament_to_array(filaments[i])
            boxsizea = filaments[i].boxes[0].w

            overlapping_tubles[i] = {}




            for j in range(i + 1, len(filaments)):
                # Check if
                #   filaments[j].meta["merge_fil_id"] is not in filaments[i].meta["merge_no_overlap_ids"]
                #
                fildat_b = filament_to_array(filaments[j])
                boxsizeb = filaments[j].boxes[0].w

                if could_overlap_by_meta(filaments[i],filaments[j]):
                    minimum_distance = get_closest_point_distance(fildat_a[:,:3], fildat_b[:,:3]) #used to speed up the calculation
                    if minimum_distance > (boxsizea/2 + boxsizeb/2):
                        overlapping_indicies_tubles = {}
                        set_not_overlapping_pair(filaments[i], filaments[j])
                    else:
                        overlapping_indicies_tubles = overlapping_boxes_indicis(fildat_a, fildat_b,
                                                                                iou_threshold)
                        if len(overlapping_indicies_tubles) == 0:
                            set_not_overlapping_pair(filaments[i], filaments[j])
                else:
                    overlapping_indicies_tubles = {}

                if j not in overlapping_tubles:
                    overlapping_tubles[j] = {}
                overlapping_tubles[i][j] = overlapping_indicies_tubles
                overlapping_tubles[j][i] = overlapping_indicies_tubles
                num_overlapping = len(overlapping_indicies_tubles)

                # overlapping factor:
                overlapping_factor = num_overlapping / min(len(fildat_a), len(fildat_b))
                overlapping_factor_matrix[i, j] = overlapping_factor
                overlapping_factor_matrix[j, i] = overlapping_factor
        return overlapping_factor_matrix, overlapping_tubles

    running_merging_id = [0] #I'm using a list so that add_metainfo can modify it.

    # Prepare for merging procedure
    filaments = sorted(filaments, key=lambda k: len(k.boxes), reverse=True)

    for f in filaments:
        add_metainfo_for_merging(f,running_merging_id, None)
    #############################
    #  Build up overlapping matrix
    #############################

    import tqdm
    continue_merging = True
    iteration = 0
    while continue_merging:
        iteration = iteration +1
        print("Merging Iteration", iteration, "Num Filaments", len(filaments))
        continue_merging = False
        overlapping_factor_matrix, overlapping_tubles = get_overlapping_matrix_and_tubles(filaments)
        filaments_to_add = []

        for filament_index, fil in tqdm.tqdm(enumerate(filaments), desc="Merge Filaments"):

            if fil is None:
                continue

            filament_indices_for_merging =  np.where(overlapping_factor_matrix[filament_index] > merge_threshold)[0].tolist()
            if len(filament_indices_for_merging) <= 1:
                continue


            if partial:
                filamentsForMerge = [filaments[filament_index]]

                for fil_index_to_merge in filament_indices_for_merging:
                    if fil_index_to_merge != filament_index:
                        # split filament at position i into overlapping parts (used for merging) and
                        # create new filaments for the non overlapping parts
                        shorter_filament = filaments[fil_index_to_merge]
                        overlap_shorter_index = np.array(
                            [box_index_on_shorter for box_index_on_longer, box_index_on_shorter, _
                             in
                             overlapping_tubles[filament_index][fil_index_to_merge]])

                        # Add all overlapping parts to filaments for merge
                        sub_fil_indicis = get_consecutive_subarrays(overlap_shorter_index)
                        for sub_fil_ind in sub_fil_indicis:
                            shorter_fil_boxes = np.copy(
                                [shorter_filament.boxes[i] for i in sub_fil_ind.tolist()])
                            if len(shorter_fil_boxes) > 0:
                                continue_merging = True
                                filamentsForMerge.append(Filament(shorter_fil_boxes))

                        # Create new filaments for all non overlapping parts
                        non_overlap_shorter_index = np.array([k for k in range(len(shorter_filament.boxes)) if k not in overlap_shorter_index])
                        sub_fil_indicis = get_consecutive_subarrays(non_overlap_shorter_index)
                        for sub_fil_ind in sub_fil_indicis:
                            shorter_fil_boxes = np.copy(
                                [shorter_filament.boxes[i] for i in sub_fil_ind.tolist()])
                            if len(shorter_fil_boxes) > 0:
                                continue_merging = True
                                f = create_filament_for_merging(shorter_fil_boxes,running_merging_id,shorter_filament)
                                filaments_to_add.append(f)
                                #filaments.append(f)

                        # Delete the old one
                        filaments[fil_index_to_merge] = None
                        overlapping_factor_matrix[fil_index_to_merge, :] = 0
                        overlapping_factor_matrix[:, fil_index_to_merge] = 0

                #filaments = [f for f in filaments if f is not None] # Remove deleted filaments

            else:
                filamentsForMerge = [filaments[k] for k in filament_indices_for_merging]
                mergedFila = merge_filaments(filamentsForMerge, window_radius, box_distance)

                assert len(mergedFila)==1, "More than one filament when merging completely should not happen"

                for k in filament_indices_for_merging:
                    filaments[k] = None
                    overlapping_factor_matrix[k, :] = 0
                    overlapping_factor_matrix[:, k] = 0

                #not_merged_filaments = [f for fi, f in enumerate(filaments) if fi not in filament_indices_for_merging]
                #filaments = []
                #filaments.extend(not_merged_filaments)

                mergedFila = add_metainfo_for_merging(mergedFila[0], running_merging_id, None)
                filaments_to_add.append(mergedFila)



                continue_merging = True

            #if continue_merging:
                #New filaments were added, some were deleted. New run with updated overlapping matrix is necessary
            #    break
        filaments = [f for f in filaments if f is not None]
        filaments.extend(filaments_to_add)
    filaments = [f for f in filaments if f is not None]  # Remove deleted filaments
    return filaments


def merge_filaments_3d_(filaments, iou_threshold, merge_threshold, window_radius, box_distance, partial = False):
    """

    :param filaments: List of filaments
    :param iou_threshold: IOU treshold. Boxes with a IOU higher than this value are condsidered as the same boxes
    :param merge_threshold: Filaments with a overlapping score hight than this value get merged
    :param window_radius: Window radius for averaging
    :param box_distance: Resampling distance after merging.
    :return:
    """

    # For each filament pair:
    #   Calculate the number of boxes that have pairs in the other filament
    #   Add to overlapping matrix
    # Start with the longest filament and merge all with overlapping > T
    # Repeat procedure with not yet merged filements

    def merge_filaments(filaments, window_size, box_distance):
        """
        Merge a set of filaments by averaging along
        the major direction

        :param filaments: List of filaments
        :param window_size: Window radius for average
        :param box_distance: box distance between two adjacent boxes after merging.
        :return:
        """
        # sort major eigenvector
        # run moving average
        if len(filaments) == 1:
            return filaments

        allboxes = []
        weights = []
        subs = []
        for fil in filaments:
            allboxes.extend(fil.boxes)
            weights.extend([box.meta['num_boxes'] for box in fil.boxes])
            if "group3d_fids" in fil.meta:
                subs.extend(fil.meta["group3d_fids"])
        boxsize = allboxes[0].w #its square...


        A = np.zeros((len(allboxes),4))
        weights = np.array(weights)
        for i,box in enumerate(allboxes):
            A[i, 0] = box.x
            A[i, 1] = box.y
            A[i, 2] = box.z
            A[i, 3] = box.c

        Acentered = A[:,:3] - A[:,:3].mean(axis=0)
        Acov = np.matmul(Acentered.T, Acentered)
        evals, evecs = np.linalg.eigh(Acov)
        eigvect = evecs[:, np.argmax(evals)]

        dotproducts = np.matmul(Acentered, eigvect)
        boxes3d = []
        N= max(1,int((max(dotproducts)-min(dotproducts))/(0.5*box_distance)))
        sample_points = np.linspace(min(dotproducts),max(dotproducts),N)
        for i in sample_points:#range(int(min(dotproducts)), int(max(dotproducts))+1):

            lower = i - window_size / 2
            upper = i + window_size / 2
            window_elements = np.logical_and(dotproducts > lower, dotproducts < upper)
            if np.sum(window_elements) > 0:

                x3d = np.average(A[window_elements][:,0], weights=weights[window_elements]) # np.mean(A[window_elements][:,0])
                y3d = np.average(A[window_elements][:,1], weights=weights[window_elements])
                z3d = np.average(A[window_elements][:,2], weights=weights[window_elements])
                conf3d = np.average(A[window_elements][:,3], weights=weights[window_elements])
                box3d = BoundBox(x=x3d, y=y3d, z=z3d, w=boxsize, h=boxsize, depth=boxsize, c=conf3d)
                box3d.meta["num_boxes"] = np.sum(np.unique(weights[window_elements]))

                if len(boxes3d) == 0:
                    boxes3d.append(box3d)
                elif not np.allclose(
                        [boxes3d[-1].x, boxes3d[-1].y, boxes3d[-1].z],
                        [x3d, y3d, z3d]
                ):
                    boxes3d.append(box3d)
                else:
                    pass

        new_fil = Filament(boxes=boxes3d)
        new_fil = resample_filaments([new_fil], box_distance)
        new_fil[0].meta["group3d_fids"] = subs
        return new_fil

    def is_completly_merged(merged_indices, filament):

        for i, _ in enumerate(filament.boxes):
            if i not in merged_indices:
                return False
        return True
    # sort filaments according length
    #filament_indicies_sorted_length = list(
    #    reversed(np.argsort([len(fil.boxes) for fil in filaments])))

    def get_overlapping_matrix_and_tubles(filaments: List[Filament]) -> Tuple[np.array, Dict]:
        #############################
        #  Build up overlapping matrix
        #############################
        overlapping_factor_matrix = np.eye(len(filaments))
        overlapping_tubles = {}

        for i in range(len(filaments) - 1):

            fildat_a = filament_to_array(filaments[i])
            overlapping_tubles[i] = {}
            for j in range(i + 1, len(filaments)):
                fildat_b = filament_to_array(filaments[j])

                overlapping_indicies_tubles = overlapping_boxes_indicis(fildat_a, fildat_b,
                                                                        iou_threshold)

                if j not in overlapping_tubles:
                    overlapping_tubles[j] = {}
                overlapping_tubles[i][j] = overlapping_indicies_tubles
                overlapping_tubles[j][i] = overlapping_indicies_tubles
                num_overlapping = len(overlapping_indicies_tubles)

                # overlapping factor:
                overlapping_factor = num_overlapping / min(len(fildat_a), len(fildat_b))
                overlapping_factor_matrix[i, j] = overlapping_factor
                overlapping_factor_matrix[j, i] = overlapping_factor
        return overlapping_factor_matrix, overlapping_tubles

    filaments = sorted(filaments, key=lambda k: len(k.boxes), reverse=True)#filaments[filament_indicies_sorted_length]

    for fil in filaments:
        print(fil.boxes[0].y)
    #############################
    #  Build up overlapping matrix
    #############################
    overlapping_factor_matrix,  overlapping_tubles = get_overlapping_matrix_and_tubles(filaments)


    #############################
    #  Start merging
    #############################
    # Start with the longest filament and merge all with overlapping > T
    # Repeat procedure with not yet merged filements

    filaments_to_return = []
    merged_indicies_per_filament = {}
    for filament_index in range(len(filaments)):
        merged_indicies_per_filament[filament_index] = [] #Init dict

    for filament_index in range(len(filaments)):#filament_indicies_sorted_length:
        print(f"Process {filament_index}")
        # Merge filaments completely for highly overlapping

        # Get indicis that of filament that exceed the overlapping threshold
        filament_indices_for_merging = np.where(overlapping_factor_matrix[filament_index] > merge_threshold)[0].tolist()
        filament_indices_for_merging = [i for i in filament_indices_for_merging if i != filament_index]

        if len(filament_indices_for_merging) == 0:
            continue



        overlapping_factor_matrix[filament_index, filament_index] = 0
        overlapping_factor_matrix[filament_index, :] = 0
        overlapping_factor_matrix[:, filament_index] = 0

        if is_completly_merged(merged_indicies_per_filament[filament_index], filaments[filament_index]):
            print("continue")
            continue

        if not partial:
            filamentsForMerge = [filaments[k] for k in filament_indices_for_merging]
            filamentsForMerge.append(filaments[filament_index])
            merged_indicies_per_filament[filament_index].extend(list(range(len(filaments[filament_index].boxes))))
            for fil_index, fil in enumerate(filaments):
                if fil_index in filament_indices_for_merging:
                    merged_indicies_per_filament[fil_index].extend(list(range(len(fil.boxes))))

        else:
            filamentsForMerge = [filaments[filament_index]]

            #Probably only extend by those indicis that where not yet merged.
            merged_indicies_per_filament[filament_index].extend(list(range(len(filaments[filament_index].boxes))))

            for fil_index_to_merge in filament_indices_for_merging:

                if fil_index_to_merge != filament_index:
                    # split filament at position i into overlapping parts (used for merging) and
                    # non overlapping parts (return them unchanged

                    shorter_filament = filaments[fil_index_to_merge]
                    overlap_shorter_index = np.array(
                        [box_index_on_shorter for box_index_on_longer, box_index_on_shorter, _
                         in
                         overlapping_tubles[filament_index][fil_index_to_merge]])

                    #overlapping part
                    sub_fil_indicis = get_consecutive_subarrays(overlap_shorter_index)
                    for sub_fil_ind in sub_fil_indicis:
                        shorter_fil_boxes = np.copy([shorter_filament.boxes[i] for i in sub_fil_ind.tolist()])
                        if len(shorter_fil_boxes) > 0:
                            filamentsForMerge.append(Filament(shorter_fil_boxes))
                            print(f"Merge {filament_index} with {fil_index_to_merge}. Indicies: {sub_fil_ind}")
                            if fil_index_to_merge in merged_indicies_per_filament:
                                merged_indicies_per_filament[fil_index_to_merge].extend(sub_fil_ind.tolist())
                            else:
                                merged_indicies_per_filament[fil_index_to_merge] = sub_fil_ind.tolist()
        print(merged_indicies_per_filament)
        mergedFila = merge_filaments(filamentsForMerge, window_radius, box_distance)

        for fil in mergedFila:
            print("Add filament:")
            for b in fil.boxes:
                print(b.y)

        filaments_to_return.extend(mergedFila)

    # Add those filaments which where not merged should be also returned..
    for index_fil, fil in enumerate(filaments):
        non_overlap_shorter_index = np.array(
            [k for k in range(len(fil.boxes)) if k not in merged_indicies_per_filament[index_fil]])
        if len(non_overlap_shorter_index) > 0:
            sub_fil_indicis = get_consecutive_subarrays(non_overlap_shorter_index)
            for sub_fil_ind in sub_fil_indicis:
                shorter_fil_boxes = np.copy(
                    [fil.boxes[i] for i in sub_fil_ind.tolist()])
                if len(shorter_fil_boxes) > 0:
                    filaments_to_return.append(Filament(shorter_fil_boxes))


    return filaments_to_return


def non_maxima_suppress_fast_3d(boxes, nms_threshold: float, obj_threshold: float, average: bool=True):
    '''

    :param boxes: List of boxes
    :param nms_threshold: Non-maximum-suppression threshold.
    :param obj_threshold: Boxes with a confidence lower that threshold are removed.
    :return: Filtered boxes
    '''

    if not boxes:
        return []
    number_classes = len(boxes[0].classes)
    for c in range(number_classes):
        sorted_indices = list(reversed(np.argsort([box.meta["num_boxes"] for box in boxes])))
        boxes_data_size = 10
        boxes_data = np.empty(shape=(len(boxes), boxes_data_size))
        for i, sorted_index in enumerate(sorted_indices):
            boxes_data[i, 0] = boxes[sorted_index].x
            boxes_data[i, 1] = boxes[sorted_index].y
            boxes_data[i, 2] = boxes[sorted_index].z
            boxes_data[i, 3] = boxes[sorted_index].w
            boxes_data[i, 4] = boxes[sorted_index].h
            boxes_data[i, 5] = boxes[sorted_index].depth
            boxes_data[i, 6] = boxes[sorted_index].classes[c]
            boxes_data[i, 7] = sorted_index
            boxes_data[i, 8] = i
            boxes_data[i, 9] = boxes[sorted_index].meta["num_boxes"]

        for i in range(len(boxes_data)):
            box_i = boxes_data[i, :]
            if box_i[6] == 0:
                continue
            else:
                other_box = boxes_data[(i + 1):]
                if other_box.shape[0] > 0:
                    boxes_i_rep = np.array([box_i] * len(other_box))
                    ious = bbox_iou_vec_3d(boxes_i_rep, other_box)

                    if average:
                        weightsum = boxes_data[i, 9]

                        sumx = boxes_data[i, 0] * boxes_data[i, 9]
                        sumy = boxes_data[i, 1] * boxes_data[i, 9]
                        sumz = boxes_data[i, 2] * boxes_data[i, 9]
                        sumconf = boxes_data[i, 6] * boxes_data[i, 9]
                        weights = [boxes_data[i, 9]]
                        confs = [boxes_data[i, 6]]

                        for box in boxes_data[other_box[ious >= nms_threshold, 8].astype(int)]:
                            weights.append(box[9])
                            weightsum = weightsum + box[9]
                            sumx = sumx + box[0] * box[9]
                            sumy = sumy + box[1] * box[9]
                            sumz = sumz + box[2] * box[9]
                            confs.append(box[6])
                            sumconf = sumconf + box[9] * box[6]

                        boxes_data[i, 0] = sumx / weightsum
                        boxes_data[i, 1] = sumy / weightsum
                        boxes_data[i, 2] = sumz / weightsum
                        boxes_data[i, 6] = sumconf / weightsum


                        boxes[boxes_data[i, 7].astype(int)].x = boxes_data[i, 0]
                        boxes[boxes_data[i, 7].astype(int)].y = boxes_data[i, 1]
                        boxes[boxes_data[i, 7].astype(int)].z = boxes_data[i, 2]



                    boxes_data[other_box[ious >= nms_threshold, 8].astype(int), 6] = 0

        for row in boxes_data[boxes_data[:, 6] == 0]:
            boxes[row[7].astype(int)].classes[c] = 0

    # remove the boxes which are less likely than a obj_threshold
    boxes = [copy.copy(box) for box in boxes if box.get_score() > obj_threshold]

    return boxes


def bbox_iou_vec_3d(boxesA, boxesB):
    # 0 x
    # 1 y
    # 2 z
    # 3 w
    # 4 h
    # 5 depth
    # 6 confidence
    # 7 sorted index
    # 8 i

    x1_min = boxesA[:, 0] - boxesA[:, 3] / 2
    x1_max = boxesA[:, 0] + boxesA[:, 3] / 2
    y1_min = boxesA[:, 1] - boxesA[:, 4] / 2
    y1_max = boxesA[:, 1] + boxesA[:, 4] / 2
    z1_min = boxesA[:, 2] - boxesA[:, 5] / 2
    z1_max = boxesA[:, 2] + boxesA[:, 5] / 2

    x2_min = boxesB[:, 0] - boxesB[:, 3] / 2
    x2_max = boxesB[:, 0] + boxesB[:, 3] / 2
    y2_min = boxesB[:, 1] - boxesB[:, 4] / 2
    y2_max = boxesB[:, 1] + boxesB[:, 4] / 2
    z2_min = boxesB[:, 2] - boxesB[:, 5] / 2
    z2_max = boxesB[:, 2] + boxesB[:, 5] / 2

    intersect_w = interval_overlap_vec(x1_min, x1_max, x2_min, x2_max)
    intersect_h = interval_overlap_vec(y1_min, y1_max, y2_min, y2_max)
    intersect_depth = interval_overlap_vec(z1_min, z1_max, z2_min, z2_max)
    intersect = intersect_w * intersect_h * intersect_depth
    union = boxesA[:, 3] * boxesA[:, 4] * boxesA[:, 5] + boxesB[:, 3] * boxesB[:, 4] * boxesB[:,
                                                                                       5] - intersect
    return intersect / union

def bbox_iou_one_with_many(box,boxes):

    box_rep_arr = np.array([box.x, box.y, box.w, box.h] * len(boxes)).reshape((len(boxes),4))
    boxes_arr = np.zeros(shape=(len(boxes), 4))

    for i, box in enumerate(boxes):
        boxes_arr[i, 0] = box.x
        boxes_arr[i, 1] = box.y
        boxes_arr[i, 2] = box.w
        boxes_arr[i, 3] = box.h
    return bbox_iou_vec(box_rep_arr, boxes_arr)

def bbox_iou(boxa,boxb):
    boxa_arr = np.zeros(shape=(1,4))
    boxb_arr = np.zeros(shape=(1, 4))
    def fill(arr, box):
        arr[0, 0] = box.x
        arr[0, 1] = box.y
        arr[0, 2] = box.w
        arr[0, 3] = box.h
        return arr
    boxa_arr = fill(boxa_arr, boxa)
    boxb_arr = fill(boxb_arr, boxb)
    return bbox_iou_vec(boxa_arr,boxb_arr)[0]

def bbox_iou_vec(boxesA, boxesB):
    x1_min = boxesA[:, 0] - boxesA[:, 2] / 2
    x1_max = boxesA[:, 0] + boxesA[:, 2] / 2
    y1_min = boxesA[:, 1] - boxesA[:, 3] / 2
    y1_max = boxesA[:, 1] + boxesA[:, 3] / 2

    x2_min = boxesB[:, 0] - boxesB[:, 2] / 2
    x2_max = boxesB[:, 0] + boxesB[:, 2] / 2
    y2_min = boxesB[:, 1] - boxesB[:, 3] / 2
    y2_max = boxesB[:, 1] + boxesB[:, 3] / 2
    intersect_w = interval_overlap_vec(x1_min, x1_max, x2_min, x2_max)
    intersect_h = interval_overlap_vec(y1_min, y1_max, y2_min, y2_max)
    intersect = intersect_w * intersect_h
    union = boxesA[:, 2] * boxesA[:, 3] + boxesB[:, 2] * boxesB[:, 3] - intersect
    return intersect / union


def interval_overlap_vec(x1_min, x1_max, x2_min, x2_max):
    intersect = np.zeros(shape=(len(x1_min)))
    cond_a = x2_min < x1_min
    cond_b = cond_a & (x2_max >= x1_min)
    intersect[cond_b] = np.minimum(x1_max[cond_b], x2_max[cond_b]) - x1_min[cond_b]
    cond_c = ~cond_a & (x1_max >= x2_min)
    intersect[cond_c] = np.minimum(x1_max[cond_c], x2_max[cond_c]) - x2_min[cond_c]

    return intersect

def find_corresponding_path(list_of_paths,path):
    import pathlib
    import os
    pth = pathlib.PurePath(path)
    current_lookup_var = pth.name
    paths = [path for path in list_of_paths if current_lookup_var in path]
    while len(paths) > 1:
        current_lookup_var = os.path.join(pth.parent.name,current_lookup_var)
        pth = pth.parent
        paths = [path for path in list_of_paths if current_lookup_var in path]
    return paths[0]

def vector_to_direction(x,y):
    '''
    Converts vector (x,y) into direction (rad) 0 - PI
    :param x: x component
    :param y: y component
    :return: Direction as radiant (0 - PI)
    '''
    angle = np.arctan2(x, y)
    if angle < 0:
        angle = np.arctan2(-1 * x, -1 * y)
    return angle

def write_command(filename, txt):
    try:
        import os

        os.makedirs(os.path.dirname(filename))
    except Exception:
        pass

    text_file = open(filename, "w")
    text_file.write(txt)
    text_file.close()


def check_for_updates():
    """
    Checks if cryolo updates are available
    :return: None
    """
    try:
        import cryolo

        with urllib.request.urlopen(
            url="https://pypi.org/pypi/cryolo/json", timeout=5
        ) as url:
            data = json.loads(url.read().decode())
            from distutils.version import LooseVersion as V

            current_version = cryolo.__version__
            latest_version = current_version
            for ver in data["releases"].keys():
                vers = V(ver)
                if vers > V(latest_version) and len(vers.version) == 3:
                    latest_version = ver
            if V(latest_version) > V(current_version):
                print("###############################################")
                print("New version of crYOLO available")
                print("Local version:\t\t", current_version)
                print("Latest version:\t\t", latest_version)
                print(
                    "More information here:\n",
                    "https://cryolo.readthedocs.io/en/latest/changes.html",
                )
                print("###############################################")
    except Exception as e:
        print("###############################################")
        print("Skip version check, as it failed with the following error:")
        print(e)
        print("###############################################")
        pass
