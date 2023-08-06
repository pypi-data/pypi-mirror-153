#
# COPYRIGHT
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
# pylint: disable=C0330
import itertools
import numpy as np
from scipy.spatial import cKDTree
from .utils import Filament
from . import utils
import copy

class FilamentTracer:
    def __init__(
        self,
        boxes,
        orientation_image,
        search_radius=60,
        angle_delta=10,
        min_number_boxes=2,
        rescale_factor=1,
        rescale_factor_x=1,
        rescale_factor_y=1,
        do_merging=True,
        box_distance=None,
        nosplit=False,
        straightness_method=-1,
        straightness_threshold=0.95,
        iou_thresh = 0.5
    ):
        """
        Traces filaments in the image using picked boxes as support points.

        :param orientation_image: Estimated orientation at each position in the image, when none
        then the estimated angles of box files are used
        :param boxes: Picked boxes
        :param search_radius: Search radius to search for the next valid box.
        :param angle_delta: Allowed delta in orientation
        :param min_number_boxes: Minimum number of boxes a filament should contain
        :param rescale_factor: Resacle factor for box coordinates
        :param iou_tresh: Parameter used in suppression/splitting of overlapping filaments
        """
        self.iou_thresh = iou_thresh
        self.search_radius = search_radius
        self.angle_delta = angle_delta
        self.min_number_boxes = min_number_boxes
        self.rescale_factor = rescale_factor
        self.rescale_factor_x = rescale_factor_x
        self.rescale_factor_y = rescale_factor_y
        self.dir_delta = self.angle_delta * 1.75
        self.box_coords_data = None  # Init in update_box_coords_data
        self.box_coord_kdtree = None  # Init in update_box_coords_data
        self.boxes_distance_matrix = None  # Init in update_box_coords_data
        self.boxes = copy.deepcopy(boxes)
        self.orientation_image = orientation_image
        self.do_merging = do_merging
        self.box_distance = box_distance
        self.nosplit = nosplit
        if straightness_method == -1:
            self.straightness_method = _get_straightness
        else:
            self.straightness_method = straightness_method
        self.straightness_threshold = straightness_threshold

    @property
    def boxes(self):
        return self.__boxes

    @boxes.setter
    def boxes(self, boxes):

        self.__boxes = boxes
        self.update_box_coords_data()

    def update_box_coords_data(self):
        self.box_coords_data = np.empty(shape=(len(self.boxes), 2),dtype=np.float32)
        for i, box in enumerate(self.boxes):
            box.x = box.x * self.rescale_factor
            box.y = box.y * self.rescale_factor
            box.w = box.w * self.rescale_factor
            box.h = box.h * self.rescale_factor
            box.info = i
            self.box_coords_data[i, 0] = box.x
            self.box_coords_data[i, 1] = box.y

        self.box_coord_kdtree = cKDTree(self.box_coords_data)
        '''
        self.boxes_distance_matrix = self.box_coord_kdtree.sparse_distance_matrix(
            self.box_coord_kdtree, 999999
        ).astype(np.float32,copy=False)
        print("type:", self.boxes_distance_matrix.dtype)
        '''
    def merge_filaments(self, filaments):
        search_radius_sq = self.search_radius * self.search_radius
        merged = True
        while merged:
            min_dist_filament = None
            min_dist_fil_a_index = None
            min_dist_fil_b_index = None
            merged = False
            for i in range(len(filaments)):
                for j in range((i + 1), len(filaments)):
                    if i != j:

                        if (
                            distancesq_filament(filaments[i], filaments[j])
                            > search_radius_sq
                        ):
                            # Skip if filaments are to far away
                            continue

                        merge_candidate = self.merge_filament(
                            filaments[i], filaments[j]
                        )
                        # print("Try to merge", i, j, merge_candidate is None)
                        if merge_candidate is not None:
                            if min_dist_filament is None:
                                min_dist_filament = merge_candidate
                                min_dist_fil_a_index = i
                                min_dist_fil_b_index = j
                            elif merge_candidate[1] < min_dist_filament[1]:
                                min_dist_filament = merge_candidate
                                min_dist_fil_a_index = i
                                min_dist_fil_b_index = j

            if min_dist_filament is not None:
                if min_dist_fil_a_index > min_dist_fil_b_index:
                    del filaments[min_dist_fil_a_index]
                    del filaments[min_dist_fil_b_index]
                else:
                    del filaments[min_dist_fil_b_index]
                    del filaments[min_dist_fil_a_index]
                filaments.append(min_dist_filament[0])
                merged = True

        return filaments

    def trace_filaments(self):
        """
        Traces filaments based on boxes provided by crYOLO + orientation image
        :return: List of traced filements
        """
        assigned_boxes = []
        filaments = []
        # while len(assigned_boxes) < len(self.boxes):
        for box in self.boxes:
            if not contains_box(box, assigned_boxes):  # box not in assigned_boxes:
                fil = Filament()

                fil.add_box(box)

                assigned_boxes.append(box)

                new_box_found = True
                while new_box_found:
                    new_box_found = False
                    candidate_boxes = self.get_box_neightborhood(
                        fil.boxes[-1], self.search_radius
                    )
                    candidate_boxes = [
                        box
                        for box in candidate_boxes
                        if not contains_box(box, assigned_boxes)
                    ]
                    next_box_indices, ignore = self.next_valid_box(
                        filament=fil,
                        ref_box=fil.boxes[-1],
                        candidate_boxes=candidate_boxes,
                    )

                    for i in next_box_indices:
                        new_box_found = True

                        fil.add_box(candidate_boxes[i])
                        assigned_boxes.append(candidate_boxes[i])
                    for i in ignore:
                        assigned_boxes.append(candidate_boxes[i])
                filaments.append(fil)
        #
        # Merge filaments
        #
        if self.do_merging:
            filaments = self.merge_filaments(filaments)

        filaments = [f for f in filaments if f.get_num_boxes() >= self.min_number_boxes]
        # Smooth
        for fil in filaments:
            fil.boxes = moving_window(boxes=fil.boxes, window_width=3)
        # Rescale
        for fil in filaments:
            for box in fil.boxes:
                box.x = box.x / self.rescale_factor
                box.y = box.y / self.rescale_factor
                box.w = box.w / self.rescale_factor
                box.h = box.h / self.rescale_factor

        # Resample
        if self.box_distance is not None:
            filaments = utils.resample_filaments(filaments, self.box_distance)

        # NMS for filaments:
        filaments = nms_for_filaments(filaments, self.iou_thresh)

        # Make straight filaments
        if not self.nosplit:
            filaments = split_filaments_by_straightness(filaments, self.straightness_method, self.straightness_threshold)

        # Add direction information
        for fil in filaments:
            for box in fil.boxes:
                orientation = get_orientation_for_box(box, self.orientation_image)
                box.meta["orientation"] = orientation
        return filaments

    def merge_filament(self, filament_a, filament_b):
        filament_a = Filament(filament_a.boxes.copy())
        filament_b = Filament(filament_b.boxes.copy())
        a_start = filament_a.boxes[0]
        a_end = filament_a.boxes[-1]
        b_start = filament_b.boxes[0]
        b_end = filament_b.boxes[-1]

        boxes = [b_start, b_end]

        candidate_box_1_index, _ = self.next_valid_box(
            filament=None, ref_box=a_start, candidate_boxes=boxes, debug=False
        )

        candidate_box_1 = None
        if len(candidate_box_1_index) > 0:
            candidate_box_1 = boxes[candidate_box_1_index[0]]
        boxes = [b_start, b_end]
        candidate_box_2_index, _ = self.next_valid_box(
            filament=None, ref_box=a_end, candidate_boxes=boxes, debug=True
        )
        candidate_box_2 = None
        if len(candidate_box_2_index) > 0:
            candidate_box_2 = boxes[candidate_box_2_index[0]]

        result_tuble = None
        if candidate_box_1 is not None:
            if box_are_equal(candidate_box_1, b_start):
                # Connects a_start with b_start
                reversed_b = list(reversed(filament_b.boxes))
                is_compatible_dir = merge_is_compatible_direction(
                    basis_filament=filament_a,
                    to_add_filament=Filament(reversed_b),
                    from_head_a=True,
                )
                if is_compatible_dir:
                    reversed_b.extend(filament_a.boxes)
                    new_filament_boxes = reversed_b
                    new_filament = Filament()
                    new_filament.boxes = new_filament_boxes
                    sq_dist = self.get_distance(a_start, b_start)
                    result_tuble = (new_filament, sq_dist)

            elif box_are_equal(candidate_box_1, b_end):
                # TODO: Do the same for the otehr cases...
                filament_b_for_dir_est = filament_b
                if len(filament_b.boxes) < 3:
                    filament_b_for_dir_est = Filament(filament_b.boxes)
                    for b in filament_a.boxes[:-2]:
                        filament_b_for_dir_est.boxes.append(b)

                is_compatible_dir = merge_is_compatible_direction(
                    basis_filament=filament_a,
                    to_add_filament=filament_b_for_dir_est,
                    from_head_a=True,
                )
                if is_compatible_dir:
                    new_filament_boxes = list(filament_b.boxes)
                    new_filament_boxes.extend(filament_a.boxes)
                    new_filament = Filament()
                    new_filament.boxes = new_filament_boxes
                    sq_dist = self.get_distance(a_start, b_end)
                    result_tuble = (new_filament, sq_dist)

        elif candidate_box_2 is not None:
            if box_are_equal(candidate_box_2, b_start):
                is_compatible_dir = merge_is_compatible_direction(
                    basis_filament=filament_a,
                    to_add_filament=filament_b,
                    from_head_b=True,
                )
                if is_compatible_dir:
                    new_filament_boxes = list(filament_a.boxes)
                    new_filament_boxes.extend(filament_b.boxes)

                    new_filament = Filament()
                    new_filament.boxes = new_filament_boxes
                    sq_dist = self.get_distance(a_end, b_start)
                    result_tuble = (new_filament, sq_dist)

            elif box_are_equal(candidate_box_2, b_end):
                reversed_b = list(reversed(filament_b.boxes))

                is_compatible_dir = merge_is_compatible_direction(
                    basis_filament=filament_a,
                    to_add_filament=Filament(reversed_b),
                    from_head_b=True,
                )
                if is_compatible_dir:

                    new_filament_boxes = list(filament_a.boxes)
                    new_filament_boxes.extend(reversed_b)

                    new_filament = Filament()
                    new_filament.boxes = new_filament_boxes
                    sq_dist = self.get_distance(a_end, b_end)

                    result_tuble = (new_filament, sq_dist)
        return result_tuble

    def get_box_neightborhood(self, ref_box, search_radius):
        """
        Finds neighboring boxes in a specific radius
        :param ref_box:
        :param search_radius:
        :return: List of box neighbors
        """
        box_indicies_in_search_radius = self.box_coord_kdtree.query_ball_point(
            [ref_box.x, ref_box.y], search_radius
        )
        boxes_in_search_radius = [
            self.boxes[index] for index in box_indicies_in_search_radius
        ]
        return boxes_in_search_radius

    def next_valid_box(self, filament, candidate_boxes, ref_box, debug=False):
        """
        Find the next valid box for a given filament
        :param filament: All boxes taht belong to the filament.
        Mainly used for orientation estimation
        :param ref_box: Refrence box. Outgoing from this the next valid box is searched.
        :param assigned_boxes: Boxes that are already assigned
        :param candidate_boxes: Candidate boxes

        :return: Next valid box
        """
        if filament is None:
            ref_orientation = get_orientation_for_box(ref_box, self.orientation_image)
        else:
            ref_orientation = filament_orientation(filament, self.orientation_image)

        ref_tracing_direction = filament_direction(filament)

        # Get boxes inside angular search region
        # ref_box_ = ref_box
        # if filament is not None:
        #    xavg = np.average([b.x for b in filament.boxes[-5:]])
        #    yavg = np.average([b.y for b in filament.boxes[-5:]])
        #    ref_box_ = utils.BoundBox(xavg,yavg,0,0)
        selected_candidate_boxes = [
            box
            for box in candidate_boxes
            if in_angular_search_region(
                ref_box=ref_box,
                candidate_box=box,
                angle_delta=self.dir_delta,
                ref_angle=ref_orientation,
            )
        ]

        to_ignore = [
            box
            for box in candidate_boxes
            if not in_angular_search_region(
                ref_box=ref_box,
                candidate_box=box,
                angle_delta=self.dir_delta,
                ref_angle=ref_orientation,
            )
        ]
        ious = utils.bbox_iou_one_with_many(ref_box, to_ignore)>self.iou_thresh
        to_ignore = [
            box
            for box_i, box in enumerate(to_ignore)
            if ious[box_i]
        ]
        '''
        print("new",)
        to_ignore_index = [
            box_i
            for box_i,box in enumerate(to_ignore)
            if utils.bbox_iou(ref_box, box) > self.iou_thresh
        ]
        print("old", to_ignore_index)
        to_ignore = [
            box
            for box in to_ignore
            if utils.bbox_iou(ref_box,box) > self.iou_thresh
        ]
        '''


        # Check if in search radius
        selected_candidate_boxes = [
            box
            for box in selected_candidate_boxes
            if self.get_distance(ref_box, box) < self.search_radius
        ]

        # Check if in search range
        selected_candidate_boxes = [
            box
            for box in selected_candidate_boxes
            if angle_between_two_boxes(ref_box, box) < self.angle_delta
        ]

        # Check if same orientation

        selected_candidate_boxes = [
            box
            for box in selected_candidate_boxes
            if is_valid(
                ref_orientation,
                self.angle_delta,
                get_orientation_for_box(box, self.orientation_image),
            )
        ]

        if ref_tracing_direction is None and filament is not None:
            max_coh = 0
            max_coh_dir = None
            for bo_i, bo in enumerate(selected_candidate_boxes):
                help_dir = box_diff_direction_vector(bo, filament.boxes[-1])
                coherrence = 0
                for bo_j, bo2 in enumerate(selected_candidate_boxes):
                    if bo_i != bo_j:
                        help2_dir = box_diff_direction_vector(bo2, filament.boxes[-1])
                        if angle_between_two_vec(help_dir, help2_dir) < self.dir_delta:
                            coherrence = coherrence + 1
                if coherrence > max_coh:
                    max_coh_dir = help_dir
                    max_coh = max_coh
            ref_tracing_direction = max_coh_dir

        # If ref_tracing_direction, check same direction
        # Select candidates according direction ref_tracing_direction
        if ref_tracing_direction is not None and filament is not None:

            selected_candidate_boxes = [
                box
                for box_i, box in enumerate(selected_candidate_boxes)
                if angle_between_two_vec(
                    ref_tracing_direction,
                    # filament_direction(Filament(filament.boxes[-4:]).add_box(box)),
                    box_diff_direction_vector(box, filament.boxes[-1]),
                )
                < self.dir_delta
            ]

        nearest_valid_boxes_indices = [
            candidate_boxes.index(box) for box in selected_candidate_boxes
        ]

        to_delete_indices = [candidate_boxes.index(box) for box in to_ignore]

        nearest_valid_box_distancesq = [
            self.get_distance(ref_box, box) for box in selected_candidate_boxes
        ]

        # Sort according distances
        sorted_indeces = np.argsort(nearest_valid_box_distancesq)
        nearest_valid_boxes_indices = [
            nearest_valid_boxes_indices[i] for i in sorted_indeces
        ]

        return nearest_valid_boxes_indices, to_delete_indices

    def get_distance(self, boxa, boxb):
        """
        Calculates the euclidian distance between two boxes
        :param boxa: First box
        :param boxb: Second box
        :return: Euclidian distance between boxa and boxb
        """
        if (
            self.boxes_distance_matrix is not None
            and boxa.info is not None
            and boxb.info is not None
        ):
            return self.boxes_distance_matrix[boxa.info, boxb.info]
        return np.sqrt(sq_distance_between_two_boxes(boxa, boxb))


def merge_is_compatible_direction(
    basis_filament,
    to_add_filament,
    filament_direction_delta=50,
    from_head_a=False,
    from_head_b=False,
):
    if len(basis_filament.boxes) < 2:
        boxes = [basis_filament.boxes[0], to_add_filament.boxes[0]]
        a_filament = Filament(boxes)
    else:
        a_filament = basis_filament

    if len(to_add_filament.boxes) < 2:
        boxes = [
            basis_filament.boxes[len(basis_filament.boxes) - 1],
            to_add_filament.boxes[0],
        ]
        b_filament = Filament(boxes)
    else:
        b_filament = to_add_filament

    dira = filament_direction(a_filament, from_head=from_head_a)

    dirb = filament_direction(b_filament, from_head=from_head_b)

    angle_box_dir = angle_between_two_vec(dira, dirb)
    return angle_box_dir < filament_direction_delta


def nms_for_filaments(filaments, iou_thresh=0.3):
    # NMS for filaments
    repeat = True

    while repeat:
        filaments_nms_remove_indices = []
        new_filaments = []
        repeat = False
        for i in range(len(filaments)):
            for j in range((i + 1), len(filaments)):
                if i != j:
                    if not is_in_search_radius(filaments[i], filaments[j], iou_thresh):

                        continue
                    long = i
                    short = j
                    if len(filaments[i].boxes) < len(filaments[j].boxes):
                        long = j
                        short = i

                    split_indices = []

                    for box_i, box in enumerate(filaments[short].boxes):
                        ious = utils.bbox_iou_one_with_many(box, filaments[long].boxes)> iou_thresh
                        if np.any(ious):
                            split_indices.append(box_i)

                    '''
                    for box_combination_indices in itertools.product(
                        range(len(filaments[short].boxes)),
                        range(len(filaments[long].boxes)),
                    ):
    
                        iou = utils.bbox_iou(filaments[short].boxes[box_combination_indices[0]], filaments[long].boxes[box_combination_indices[1]])
                        if iou > iou_thresh:
                            if box_combination_indices[0] not in split_indices:
                                split_indices.append(box_combination_indices[0])
                    '''
                    if split_indices:
                        if short not in filaments_nms_remove_indices:
                            filaments_nms_remove_indices.append(short)
                        if len(filaments[short].boxes) > 1:
                            splitted_filament = split_filamant(
                                filaments[short], split_indices
                            )

                            new_filaments.extend(splitted_filament)

        filaments_nms_remove = [
            filaments[fil_index] for fil_index in filaments_nms_remove_indices
        ]
        #filaments = [fil for i, fil in enumerate(filaments) if i not in filaments_nms_remove_indices]
        for fil in filaments_nms_remove:
            filaments.remove(fil)
        for fil in new_filaments:
            repeat=True
            filaments.append(fil)

    return filaments

def is_in_search_radius(filament_a, filament_b, iou_thresh):
    """
    If some boxes of two filaments have a  IOU larger then specif threshold, return t
    :param filament_a: First filament
    :param filament_b: Second filament
    :param iou_thresh: IOU Threshold
    :return: True if at least one box pair of the two filaments have a IOU larger then the given IOU thresh
    """

    for box_a in filament_a.boxes:
         ious = utils.bbox_iou_one_with_many(box_a,filament_b.boxes)> iou_thresh
         if np.any(ious):
             return True
    '''
    for box_combination in itertools.product(filament_a.boxes, filament_b.boxes):

        iou = utils.bbox_iou(box_combination[0], box_combination[1])
        if iou > iou_thresh:
            return True
    '''

    return False

def is_in_search_radius_(filament_a, filament_b, search_radius):
    """
    If some boxes of two filaments have a distance smaller then the given radius
    :param filament_a: First filament
    :param filament_b: Second filament
    :param search_radius: Search radius
    :return: True if at least one box pair of the two filaments have a distance smaller then the given radius
    """
    search_radius_sq = search_radius * search_radius
    for box_combination in itertools.product(filament_a.boxes, filament_b.boxes):
        dist = sq_distance_between_two_boxes(box_combination[0], box_combination[1])
        if dist < search_radius_sq:
            return True
    return False


def split_filamant(filament, split_indices):
    """
    Splits a filament at specified inidices
    :param filament: Filament to be splitted
    :param split_indices: list of indicies where the filament is splitted
    :return: List of filament segments
    """
    segments = []
    split_indices.sort()

    boxes_new_a = filament.boxes[(split_indices[-1] + 1) :]
    if boxes_new_a:
        new_fil_a = Filament(boxes_new_a)
        segments.append(new_fil_a)

    if split_indices[0] > 0:
        boxes_new_b = filament.boxes[: split_indices[0]]
        new_fil_b = Filament(boxes_new_b)
        segments.append(new_fil_b)

    if len(split_indices) > 1:
        for i in range(len(split_indices) - 1):
            boxes_new = filament.boxes[(split_indices[i] + 1) : split_indices[i + 1]]
            if boxes_new:
                new_fil = Filament(boxes_new)
                segments.append(new_fil)
    return segments


def moving_window(boxes, window_width=3):
    """
    Applied a moving average filter on a set of boxes
    :param boxes: The boxes
    :param window_width: Width width for filtering
    :return: Smoothed set of boxes
    """
    if len(boxes) < (window_width + 1):
        return boxes

    new_boxes = []
    offset = int((window_width - 1) / 2)
    for i in range(offset):
        new_boxes.append(boxes[i])
    for i in range(offset, len(boxes) - offset):
        mean_x = 0
        mean_y = 0
        mean_w = 0
        mean_h = 0
        mean_c = 0
        angles = []
        window_range = range(i - offset, i + offset + 1)
        for j in window_range:
            mean_x += boxes[j].x
            mean_y += boxes[j].y
            mean_w += boxes[j].w
            mean_h += boxes[j].h
            if "angle" in boxes[j].meta:
                angles.append(boxes[j].meta["angle"])

            if boxes[j].c is None:
                mean_c += 1
            else:
                mean_c += boxes[j].c
        mean_x = int(mean_x / len(window_range))
        mean_y = int(mean_y / len(window_range))
        mean_w = mean_w / len(window_range)
        mean_h = mean_h / len(window_range)
        mean_c = mean_c / len(window_range)

        new_box = utils.BoundBox(x=mean_x, y=mean_y, w=mean_w, h=mean_h, c=mean_c)
        new_box.info = i
        if len(angles) > 0:
            median_angle = np.median(angles)
            new_box.meta["angle"] = median_angle
        new_boxes.append(new_box)
    for i in range(len(boxes) - offset, len(boxes)):
        new_boxes.append(boxes[i])
    return new_boxes


def box_are_equal(box1, box2):
    """
    :param box1: First box
    :param box2: Second box
    :return: True, if x,y, width and height are equal
    """
    if (
        int(box1.x) == int(box2.x)
        and int(box1.y) == int(box2.y)
        and int(box1.w) == int(box2.w)
        and int(box1.h) == int(box2.h)
    ):
        return True
    return False


def filter_filaments_by_num_boxes(filaments, minimum_number_boxes):
    """
    Removes filaments that are shorter than a minimum number of boxes.
    :param filaments: List of filaments
    :param minimum_number_boxes: Minimum number of boxes per filament
    :return: All filaments that have more boxes than minimum_number_boxes
    """
    filtered_filaments = [f for f in filaments if len(f.boxes) > minimum_number_boxes]
    return filtered_filaments


def split_filaments_by_straightness(resamples_filaments, straightness_method, straightness_threshold):
    """
    Splits multiple filaments by using a straightness method.
    :param resamples_filaments: List of filaments
    :param straightness_threshold: straightness threshold.
    :return: List of splitted filaments
    """

    new_fiament_segments = []
    for fil in resamples_filaments:
        segments = split_filament_by_straightness_rec([fil], straightness_method, straightness_threshold)
        new_fiament_segments.extend(segments)

    return new_fiament_segments

def split_filament_by_straightness_rec(filaments, straightness_method, straightness_threshold):

    straight_line = [utils.BoundBox(x=0,y=0, w=0,h=0),
                     utils.BoundBox(x=1,y=0, w=0,h=0),
                     utils.BoundBox(x=2,y=0, w=0,h=0)]
    non_straight_line = [utils.BoundBox(x=0,y=0, w=0,h=0),
                         utils.BoundBox(x=1,y=1, w=0,h=0),
                         utils.BoundBox(x=2,y=0, w=0,h=0)]

    if straightness_method(straight_line) < straightness_method(non_straight_line):
        a_is_more_straight = lambda a, b: a <= b
    else:
        a_is_more_straight = lambda a, b: a >= b

    splitted_fils = []

    for filament in filaments:
        s = straightness_method(filament.boxes)
        if not a_is_more_straight(s, straightness_threshold):
            split_point = len(filament.boxes)//2
            split = [Filament(filament.boxes[split_point:]), Filament(filament.boxes[:split_point])]
            splitted_fils.extend(
                split_filament_by_straightness_rec(
                    split,
                    straightness_method=straightness_method,
                    straightness_threshold=straightness_threshold
                )
            )
        else:
            splitted_fils.append(filament)

    return splitted_fils




def split_filament_by_straightness(filament, straightness_threshold=0.95):
    """
    Splits a filament into multiple subfilaments based on its straightness
    :param filament:
    :param straightness_threshold:
    :return: List of splitted sub-filaments
    """
    overall_staightness = _get_straightness(filament.boxes)
    overall_rms = _get_rms(filament.boxes)
    straightness_method = _get_rms
    straightness_threshold = 20
    a_is_more_straight = lambda a,b  : a<=b
    print("overall:", overall_staightness, overall_rms)
    if a_is_more_straight(straightness_method(filament.boxes), straightness_threshold):
        return [filament]



    list_splitted_filaments = [filament]
    last_list_size = 0
    print("Do split")
    while len(list_splitted_filaments) > last_list_size:

        last_list_size = len(list_splitted_filaments)
        for fil in list_splitted_filaments:

            if a_is_more_straight(straightness_method(fil.boxes),straightness_threshold):
                continue


            max_straightness = -1
            max_straightness_index = -1
            for i in range(2, len(fil.boxes) - 2):
                straightness_to_i = straightness_method(fil.boxes[:i])
                straightness_from_i = straightness_method(fil.boxes[i:])
                mean_straightness = (straightness_to_i + straightness_from_i) / 2
                print("Mean:", mean_straightness)
                if max_straightness == -1:
                    max_straightness = mean_straightness
                    max_straightness_index = i
                elif a_is_more_straight(mean_straightness,max_straightness):
                    max_straightness = mean_straightness
                    max_straightness_index = i

            if max_straightness_index > -1:
                boxes_new_a = fil.boxes[max_straightness_index:]
                boxes_new_b = fil.boxes[:max_straightness_index]
                new_fil_a = Filament(boxes_new_a)
                new_fil_b = Filament(boxes_new_b)
                list_splitted_filaments.remove(fil)
                list_splitted_filaments.append(new_fil_a)
                list_splitted_filaments.append(new_fil_b)
    print("Splitted into", len(list_splitted_filaments))
    return list_splitted_filaments

def _get_rms(boxes):
    def point_distance(lp_x1,lp_y1, lp_x2,lp_y2,p_x,p_y):
        """
        Measures distance point to line
        """
        dist = np.abs((lp_y2-lp_y1)*p_x - (lp_x2-lp_x1)*p_y + lp_x2*lp_y1 - lp_y2*lp_x1)/np.sqrt(np.power(lp_y2-lp_y1,2)+np.power(lp_x2-lp_x1,2))
        return dist

    if len(boxes) < 3:
        return 0

    sum_dist = 0
    sumi = 0
    for i in range(1, len(boxes)-1):
        sumi = sumi + 1
        sum_dist = sum_dist + np.power(
            point_distance(boxes[0].x,
                       boxes[0].y,
                       boxes[-1].x,
                       boxes[-1].y,
                       boxes[i].x,
                       boxes[i].y)
            ,2)
    rms = np.sqrt(sum_dist/(len(boxes)-2))
    return rms

def _get_straightness(boxes):
    """
    Calculates the straightness for a set of boxes
    :param boxes: The boxes
    :return: Straightness value
    """
    len_sum = 0
    if len(boxes)<3:
        return 1
    for i in range(1, len(boxes)):
        len_sum += np.sqrt(
            (boxes[i].x - boxes[i - 1].x) ** 2 + (boxes[i].y - boxes[i - 1].y) ** 2
        )
    len_start_end = np.sqrt(
        (boxes[0].x - boxes[len(boxes) - 1].x) ** 2
        + (boxes[0].y - boxes[len(boxes) - 1].y) ** 2
    )

    return len_start_end / len_sum


def distance_perpendicluar_to_box_direction(ref_box, candiate_box, ref_angle):

    ref_angle_rad = ref_angle / 180.0 * np.pi
    p1x = ref_box.x
    p1y = ref_box.y
    p2x = ref_box.x + np.cos(ref_angle_rad)
    p2y = ref_box.y + np.sin(ref_angle_rad)
    dist = np.abs(
        (p2y - p1y) * candiate_box.x
        - (p2x - p1x) * candiate_box.y
        + p2x * p1y
        - p2y * p1x
    ) / np.sqrt((p2y - p1y) ** 2 + (p2x - p1x) ** 2)
    return dist


def in_angular_search_region(ref_box, candidate_box, ref_angle, angle_delta):
    """

    :param ref_box:
    :param candidate_box:
    :param ref_angle: orientation in degree
    :param angle_delta: max angle delta in degree
    :return:
    """

    ref_angle_rad = ref_angle / 180.0 * np.pi
    ref_angle_vector = np.asarray([np.cos(ref_angle_rad), np.sin(ref_angle_rad)])
    ref_angle_vector_180 = -1 * ref_angle_vector

    cand_angle_vector = (candidate_box.x - ref_box.x, candidate_box.y - ref_box.y)
    norm = np.linalg.norm(cand_angle_vector)
    cand_angle_vector = cand_angle_vector / norm

    delta = angle_between_two_vec(ref_angle_vector, cand_angle_vector)
    delta_180 = angle_between_two_vec(ref_angle_vector_180, cand_angle_vector)
    in_search_region = delta < angle_delta or delta_180 < angle_delta
    return in_search_region


def get_orientation_for_box(box, orientation_image):

    if orientation_image is not None:
        index_y = int(box.y + box.h / 2)
        index_x = int(box.x + box.w / 2)
        index_y = (
            index_y
            if index_y < orientation_image.shape[0]
            else orientation_image.shape[0] - 1
        )
        index_x = (
            index_x
            if index_x < orientation_image.shape[1]
            else orientation_image.shape[1] - 1
        )
        return orientation_image[index_y, index_x]
    elif "angle" in box.meta:
        ang_ret = np.rad2deg(box.meta["angle"])
        return ang_ret
    else:
        raise ValueError("No orientation could be estimated. Stop")


def filament_orientation(filament, orientation_image, len_window=5):
    if filament is None:
        return None
    if len(filament.boxes) < 2:
        return get_orientation_for_box(filament.boxes[0], orientation_image)
    mean_orientation = 0
    last5_boxes = filament.boxes[-len_window:]
    for i in range(1, len(last5_boxes)):
        mean_orientation += get_orientation_for_box(last5_boxes[i], orientation_image)
    ref_orientation = mean_orientation / (len(last5_boxes) - 1)

    return ref_orientation


def filament_direction(filament, num_last_boxes=5, from_head=False):
    """
    Estimates the current filament direction (vector) based on the last num_last_positions boxes.
    :param filament: Filament
    :param num_last_boxes: Number of boxes to estimates the current directions
    :param from_head: Direction of estimation
    :return: Current direction as a vector
    """
    if filament is None:
        return None
    if len(filament.boxes) < 2:
        return None
    mean_y = 0
    mean_x = 0
    if from_head:
        last5_boxes = filament.boxes[:num_last_boxes]
    else:
        last5_boxes = filament.boxes[-num_last_boxes:]

    for i in range(1, len(last5_boxes)):
        vec_box_normed = box_diff_direction_vector(last5_boxes[i], last5_boxes[i - 1])
        mean_x += vec_box_normed[0]
        mean_y += vec_box_normed[1]
    ref_vec = (mean_x / (len(last5_boxes) - 1), mean_y / (len(last5_boxes) - 1))

    return ref_vec


def box_diff_direction_vector(box_a, box_b):
    norm_vec = (box_a.x - box_b.x, box_a.y - box_b.y)
    norm_vec = norm_vec / (np.linalg.norm(norm_vec)+0.0001)
    return norm_vec


def sq_distance_between_two_boxes(box_a, box_b):
    """
    Calculates the squared euclidian distance between two boxes
    :param box_a: First box
    :param box_b: Second box
    :return: Squared distance between two boxes
    """
    return (box_a.x - box_b.x) ** 2 + (box_a.y - box_b.y) ** 2


def angle_between_two_boxes(box_a, box_b):
    """
    Calculates the angle (degree) between the centers of two boxes
    :param box_a: First box
    :param box_b: Second box
    :return: Angle between the centers of two boxes (degree)
    """
    vec_box_a = (box_a.x, box_a.y)
    vec_box_a = vec_box_a / np.linalg.norm(vec_box_a)
    vec_box_b = (box_b.x, box_b.y)
    vec_box_b = vec_box_b / np.linalg.norm(vec_box_b)

    return angle_between_two_vec(vec_box_a, vec_box_b)


def angle_between_two_vec(vec_a, vec_b):
    """
    Calculates the angle (degree) between the centers of two vectors

    :param vec_a: First vector
    :param vec_b: Second vector
    :return: Angle between the centers of two boxes (degree)
    """
    angle_rad = np.arccos(np.clip(np.dot(vec_a, vec_b), -1.0, 1.0))
    angle = angle_rad / (2 * np.pi) * 360
    return angle


def is_valid(ref_angle, delta_angle, test_angle, debug=False):
    """
    Checks if the differencen between two angles (in degree) is less then a give delta_angle
    :param ref_angle: Reference angleis_valid
    :param delta_angle: Allowed delta
    :param test_angle: Test angle
    :return: True if the difference is lower than the allowed delta
    """

    delta_1 = np.abs(ref_angle - test_angle)
    ref_2 = np.abs(ref_angle - 180)
    delta_2 = np.abs(ref_2 - test_angle)

    is_angle_valid = delta_1 < delta_angle or delta_2 < delta_angle
    if debug:
        print("V", delta_1, delta_2)
    return is_angle_valid


def contains_box(box, list_box):
    contains = False
    for b in list_box:
        if int(box.x) == int(b.x) and int(box.y) == int(b.y):
            return True

    return contains


def distancesq_filament(filament_a, filament_b):
    """

    :param filament_a: First filament
    :param filament_b: Second filament
    :return: Minimum distance between start and end points of the two filaments
    """
    start_end_boxes_a = [filament_a.boxes[0], filament_a.boxes[-1]]
    start_end_boxes_b = [filament_b.boxes[0], filament_b.boxes[-1]]
    min_dist = 999999999
    for start_end_combination in itertools.product(
        start_end_boxes_a, start_end_boxes_b
    ):
        dist = sq_distance_between_two_boxes(
            start_end_combination[0], start_end_combination[1]
        )
        if dist < min_dist:
            min_dist = dist
    return min_dist
