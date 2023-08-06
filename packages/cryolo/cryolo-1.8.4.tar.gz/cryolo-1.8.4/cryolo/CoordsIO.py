"""
Boxfile writing methods
Author: Thorsten Wagner (thorsten.wagner@mpi-dortmund.mpg.de)
"""
#! /usr/bin/env python
#
# COPYRIGHT
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
import csv
import os
import numpy as np
from typing import List, Union
import cryolo.utils as utils
from cryolo.utils import Filament, BoundBox
from pyStarDB import sp_pystardb as star
import pandas as pd
from abc import ABC, abstractmethod

class BoxPosition(ABC):
    @abstractmethod
    def get_center_coords(self):
        pass

    @abstractmethod
    def get_extent(self):
        pass

def write_box_yolo(path, boxes, write_star=False):
    """
    Write box/star files.
    :param path: Filepath or filename of the box file to write
    :param boxes: Boxes to write
    :param outpath: When path is a filename, it one can specifiy the output path with outpath.
    :param write_star: If true, a star file is written.
    :return: None
    """
    if write_star:
        path = path[:-3] + "star"
        write_star_file(path, boxes)

    else:
        write_eman1_boxfile(path, boxes)


def get_star_file_header(file_name):
    """
        Load the header information.
        Arguments:
        file_name - Path to the file that contains the header.
        Returns:
        List of header names, rows that are occupied by the header.
    """
    start_header = False
    header_names = []
    idx = None

    with open(file_name, "r") as read:
        for idx, line in enumerate(read.readlines()):
            if line.startswith("_"):
                if start_header:
                    header_names.append(line.strip().split()[0])
                else:
                    start_header = True
                    header_names.append(line.strip().split()[0])
            elif start_header:
                break

    if not start_header:
        raise IOError(f"No header information found in {file_name}")

    return header_names, idx

def write_star_file(path, boxes):
    is_3d =  boxes and boxes[0].z is not None
    columns=['_rlnCoordinateX', '_rlnCoordinateY']
    if is_3d is True:
        columns = ['_rlnCoordinateX', '_rlnCoordinateY','_rlnCoordinateZ']

    coords = np.zeros(shape=(len(boxes),len(columns)))
    for box_index, box in enumerate(boxes):
        coords[box_index, 0] = box.x + box.w / 2
        coords[box_index, 1] = box.y + box.h / 2

    if is_3d:
        for box_index, box in enumerate(boxes):
            coords[box_index, 2] = box.z

    df = pd.DataFrame(coords, columns=columns)
    sfile = star.StarFile(path)
    sfile.update('', df, True)
    sfile.write_star_file(overwrite=True)

def read_star_file(path, box_size=200):
    """
    Read a box file from STAR file
    :param path: Path to star file
    :param box_size
    """
    sfile = star.StarFile(path)
    panda_dataframe=sfile['']                   # the panda dataframe has noname (i.e.:data_)
    if len(panda_dataframe.iloc[:]) == 0:
        return []

    boxes=[]

    # 200 is the default value of the box size
    box_width = box_size
    box_height = box_size
    is_3d = '_rlnCoordinateZ' in panda_dataframe.columns
    for i in range(len(panda_dataframe.iloc[:])):
        b=BoundBox(x=panda_dataframe.iloc[i]['_rlnCoordinateX'] - box_width / 2, y=panda_dataframe.iloc[i]['_rlnCoordinateY']  - box_height / 2, w=box_width, h=box_height)
        if is_3d:
            b.z = panda_dataframe.iloc[i]['_rlnCoordinateZ'] # the constructor of BoundBox has not 'z' parameter
        boxes.append(b)

    return boxes

def is_star_filament_file(path):
    try:
        star.StarFile(path)
    except:
        return False

    if path.endswith(".star") == False:
        return False
    return True

def read_star_filament_file(path, box_width, min_distance=0):
    sfile = star.StarFile(path)

    xcoords = sfile['']["_rlnCoordinateX"]
    ycoords = sfile['']["_rlnCoordinateY"]
    filaments = []
    for i in range(len(xcoords)):
        if i % 2 == 0:
            x_start = int(xcoords[i] - box_width / 2)
            y_start = int(ycoords[i] - box_width / 2)
            box_start = BoundBox(x=x_start, y=y_start, w=box_width, h=box_width)
        else:
            x_end = int(xcoords[i] - box_width / 2)
            y_end = int(ycoords[i] - box_width / 2)
            box_end = BoundBox(x=x_end, y=y_end, w=box_width, h=box_width)
            length = np.sqrt((x_start - x_end) ** 2 + (y_start - y_end) ** 2)
            if min_distance == 0:
                parts = int((length / (0.1 * box_width)))
            else:
                parts = length / min_distance
            boxes = utils.getEquidistantBoxes(
                box1=box_start, box2=box_end, num_boxes=parts
            )
            f = Filament(boxes)
            filaments.append(f)
    return filaments

def write_star_filemant_file(path, filaments):
    num_boxes = 2*len(filaments)

    coords = np.zeros(shape=(num_boxes,2))
    i = 0
    for fil in filaments:
        bstart = fil.boxes[0]
        bend = fil.boxes[-1]
        coords[i, 0] = bstart.x + bstart.w / 2
        coords[i, 1] = bstart.y + bstart.h / 2
        coords[i+1, 0] = bend.x + bend.w / 2
        coords[i+1, 1] = bend.y + bend.h / 2
        i = i + 2

    df = pd.DataFrame(coords, columns=['_rlnCoordinateX', '_rlnCoordinateY'])
    sfile = star.StarFile(path)
    sfile.update('', df, True)
    sfile.write_star_file(overwrite=True)


def read_eman1_boxfile(path, is_SPA=True, box_size_default=200) -> List[BoundBox]:
    """
    Read a box file in EMAN1 box format.
    :param path: Path to box file
    :param is_SPA: False if the file is referred to a tomo
    :param box_size_default: boxsize for tomo box files
    :return: List of bounding boxes
    """
    boxreader = np.atleast_2d(np.genfromtxt(path))
    boxes =[]
    len_row = len(boxreader[0])
    if is_SPA: #2D case is always with width and height values
        boxes = [BoundBox(x=box[0], y=box[1], w=box[2], h=box[3]) for box in boxreader]
    elif len_row in [3,5]: #3D case without width and height values
        w= box_size_default if len_row == 3 else boxreader[0][3]
        h = box_size_default if len_row == 3 else boxreader[0][4]
        boxes = [BoundBox(x=box[0]-w/2, y=box[1]-h/2, z=box[2], w=w, h=h) for box in boxreader]
    return boxes

def _create_cbox_boundbox(box):
    bound_box = BoundBox(x=box[0], y=box[1], w=box[2], h=box[3], c=box[4])
    if len(box) > 5:
        bound_box.meta["est_box_size"] = (box[5], box[6])
    return bound_box

def read_cbox_include_list(path):
    starfile = star.StarFile(path)
    return starfile['cryolo_include']["_slice_index"].tolist()



def read_cbox_boxfile(path, min_dist_boxes_filament=0) -> Union[List[BoundBox], List[Filament]]:
    """

    :param path: Path to read
    :param min_dist_boxes_filament: Minimum distance between filament boxes (in case it is filament)
    :return: Either a list of bounding boxes or a list of filaments.
    """
    try:
        starfile = star.StarFile(path)
        boxes = []
        filaments = {}
        if 'cryolo' in starfile:
            is_filament = '_filamentid' in starfile['cryolo']
            for i in range(len(starfile['cryolo']['_CoordinateX'])):
                box = BoundBox(x=starfile['cryolo']['_CoordinateX'][i],
                               y=starfile['cryolo']['_CoordinateY'][i],
                               z=starfile['cryolo']['_CoordinateZ'][i],
                               w=starfile['cryolo']['_Width'][i],
                               h=starfile['cryolo']['_Height'][i],
                               c=starfile['cryolo']['_Confidence'][i],
                               depth=starfile['cryolo']['_Depth'][i]
                               )
                if starfile['cryolo']["_EstWidth"][i] is not None and \
                        starfile['cryolo']["_EstHeight"][i] is not None:
                    box.meta["est_box_size"] = (starfile['cryolo']["_EstWidth"][i],
                                                      starfile['cryolo']["_EstHeight"][i])
                if starfile['cryolo']["_NumBoxes"][i] is not None:
                    box.meta["num_boxes"] = starfile['cryolo']["_NumBoxes"][i]
                if "_Angle" in starfile['cryolo'] and starfile['cryolo']["_Angle"][i] is not None:
                    box.meta["angle"] = starfile['cryolo']["_Angle"][i]
                if is_filament:
                    fid = int(starfile['cryolo']['_filamentid'][i])
                    if fid in filaments:
                        filaments[fid].append(box)
                    else:
                        filaments[fid] = [box]
                else:
                    boxes.append(box)

            if is_filament:
                filaments_list = [Filament(filaments[key]) for key in filaments]
                if min_dist_boxes_filament > 0:
                    filaments_list = utils.resample_filaments(filaments_list, min_dist_boxes_filament)

                return filaments_list
            else:
                return boxes
    except Exception :

        print("Reading old CBOX format file")

        return read_cbox_boxfile_old(path)

def read_cbox_boxfile_old(path):
    """
    Read a box file in EMAN1 box format.
    :param path: Path to box file
    :return: List of bounding boxes
    """
    boxreader = np.atleast_2d(np.genfromtxt(path))

    boxes = [_create_cbox_boundbox(box) for box in boxreader]
    return boxes


def write_eman1_boxfile(path, boxes):
    with open(path, "w") as boxfile:
        boxwriter = csv.writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_NONE
        )

        for box in boxes:
            # box.x / box.y = Lower left corner
            boxwriter.writerow([box.x, box.y, box.w, box.h])

def write_eman_boxfile3d(path,boxes):

    with open(path, "w") as boxfile:

        boxwriter = csv.writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_NONE
        )

        for box in boxes:
            # box.x / box.y / box.z need to be center coordinates. z is already centered after tracing
            boxwriter.writerow([box.x+box.w/2, box.y+box.h/2, box.z])

def write_coords_file(path ,boxes):
    with open(path, "w") as boxfile:

        boxwriter = csv.writer(
            boxfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_NONE, dialect=csv.unix_dialect,
        )

        for box in boxes:
            # box.x / box.y / box.z need to be center coordinates. z is already centered after tracing
            boxwriter.writerow([box.x+box.w/2, box.y+box.h/2, box.z])


def box_to_np_array(boxes, filament_id=None):
    num_boxes = len(boxes)
    num_fields = 11
    if filament_id is not None:
        num_fields = num_fields + 1
    coords = np.zeros(shape=(num_boxes, num_fields))

    for i, box in enumerate(boxes):
        coords[i, 0] = box.x
        coords[i, 1] = box.y
        coords[i, 2] = box.z
        coords[i, 3] = box.w
        coords[i, 4] = box.h
        coords[i, 5] = box.depth
        if "boxsize_estimated" in box.meta:
            coords[i, 6] = box.meta["boxsize_estimated"][0]
            coords[i, 7] = box.meta["boxsize_estimated"][1]
        else:
            coords[i, 6] = None
            coords[i, 7] = None
        coords[i, 8] = box.c
        if "num_boxes" in box.meta:
            coords[i, 9] = box.meta["num_boxes"]
        else:
            coords[i, 9] = None
        if "angle" in box.meta:
            coords[i, 10] = box.meta["angle"]
        else:
            coords[i, 10] = None
        if filament_id is not None:
            coords[i, 11] = filament_id

    return coords



def write_cbox_file(path, coordinates, additional_slice_include=None, additional_slice_exclude=None):
    """
    Write a CBOX file in STAR format.
    :param path: File path
    :param coordinates: List of BoundingBoxes / Filaments
    :param additional_slice_include: Only needed for tomograms. List of indicies that should be added\
    to the cryolo_include_list.
    :param additional_slice_exclude: Only needed for tomograms. A list of slices that should be ignored.
    :param filament_id if boxes
    """
    if len(coordinates)==0:
        open(path, 'a').close()
        return
    columns = []
    columns.append('_CoordinateX')
    columns.append('_CoordinateY')
    columns.append('_CoordinateZ')
    columns.append('_Width')
    columns.append('_Height')
    columns.append('_Depth')
    columns.append('_EstWidth')
    columns.append('_EstHeight')
    columns.append('_Confidence')
    columns.append('_NumBoxes')
    columns.append('_Angle')

    if len(coordinates)>0 and isinstance(coordinates[0], Filament):
        coords = []
        for filament_id, filament in enumerate(coordinates):
            fil_box_coords = box_to_np_array(filament.boxes,filament_id=filament_id)
            coords.append(fil_box_coords)

        coords = np.concatenate(coords)
        columns.append('_filamentid')

    else:
        coords = box_to_np_array(coordinates)

    include_slices = [a for a in np.unique(coords[:,2]).tolist() if not np.isnan(a)]

    if additional_slice_include is not None:
        include_slices.extend(additional_slice_include)
        include_slices = list(set(include_slices))

    if additional_slice_exclude is not None:
        include_slices = [i for i in include_slices if i not in additional_slice_exclude]



    sfile = star.StarFile(path)




    version_df = pd.DataFrame([["1.0"]], columns=['_cbox_format_version'])
    sfile.update('global', version_df, False)

    df = pd.DataFrame(coords, columns=columns)
    sfile.update('cryolo', df, True)


    include_df = pd.DataFrame(include_slices, columns=['_slice_index'])
    sfile.update('cryolo_include', include_df, True)

    sfile.write_star_file(overwrite=True, tags=['global','cryolo','cryolo_include'])


def write_cbox_file_(path, boxes):
    with open(path, "w") as boxfile:
        boxwriter = csv.writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_NONE
        )

        for box in boxes:
            est_width = box.meta["boxsize_estimated"][0]
            est_height = box.meta["boxsize_estimated"][1]
            # box.x / box.y = Lower left corner
            boxwriter.writerow(
                [box.x, box.y, box.w, box.h, box.c, est_width, est_height]
            )


def write_boxfile_manager(path, rectangles):
    """

    :param path: Filepath
    :param rectangles: Rectangles to write
    :return: None
    """
    boxes = []
    for rect in rectangles:
        x_lowerleft = int(rect.get_x())
        y_lowerleft = int(rect.get_y())
        boxize = int(rect.get_width())
        box = BoundBox(x=x_lowerleft, y=y_lowerleft, w=boxize, h=boxize)
        boxes.append(box)
    write_eman1_boxfile(path, boxes)


def write_eman1_filament_start_end(filaments, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, "w", newline='', encoding='utf-8') as boxfile:
        boxwriter = csv.writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_NONE, lineterminator="\n",
        )
        for fil in filaments:
            fil_boxes = fil.boxes

            boxwriter.writerow(
                [
                    ""
                    + str(fil_boxes[0].x)
                    + " "
                    + str(fil_boxes[0].y)
                    + " "
                    + str(fil_boxes[0].w)
                    + " "
                    + str(fil_boxes[0].h)
                    + " "
                    + str(-1)
                ]
            )

            boxwriter.writerow(
                [
                    ""
                    + str(fil_boxes[len(fil_boxes) - 1].x)
                    + " "
                    + str(fil_boxes[len(fil_boxes) - 1].y)
                    + " "
                    + str(fil_boxes[len(fil_boxes) - 1].w)
                    + " "
                    + str(fil_boxes[len(fil_boxes) - 1].h)
                    + " "
                    + str(-2)
                ]
            )


def is_eman1_filament_start_end(path):
    if not path.endswith(".box"):
        return False
    try:
        box_lines = np.atleast_2d(np.genfromtxt(path))
        if len(box_lines) < 2:
            return False
        return (
            len(box_lines[0]) == 5 and box_lines[0][4] == -1 and box_lines[1][4] == -2
        )
    except ValueError:
        return False


def read_eman1_filament_start_end(path, min_distance=0):
    boxreader = np.atleast_2d(np.genfromtxt(path))
    filaments = []
    for box in boxreader:
        if int(box[4]) == -1:
            x_start = int(box[0])
            y_start = int(box[1])
            box_width = int(box[2])
            box_start = BoundBox(x=x_start, y=y_start, w=box_width, h=box_width)
        if int(box[4]) == -2:
            x_end = int(box[0])
            y_end = int(box[1])
            box_width = int(box[2])
            box_end = BoundBox(x=x_end, y=y_end, w=box_width, h=box_width)
            length = np.sqrt((x_start - x_end) ** 2 + (y_start - y_end) ** 2)
            if min_distance == 0:
                parts = int((length / (0.1 * box_width)))
            else:
                parts = length / min_distance
            boxes = utils.getEquidistantBoxes(
                box1=box_start, box2=box_end, num_boxes=parts
            )
            f = Filament(boxes)
            filaments.append(f)

    return filaments

def is_eman1_helicon(path):
    if not (path.endswith(".box") or path.endswith(".txt")):
        return False
    with open(path) as f:
        first_line = f.readline()
        f.close()
    return "#micrograph" in first_line


def read_eman1_helicon(path, min_distance=0):
    """

    :param path: Path to boxfiel in helicon formats
    :param min_distance: Two boxes in the filament will have at least this distance
    :return:
    """

    def get_first_and_last_coord(helix_line):
        if not helix_line.startswith("#helix"):
            raise ValueError("Line does not start with '#helix'")
        import re
        result = re.findall('\d+.\d*',helix_line)
        allnumbers = [float(r) for r in result]
        return allnumbers[:4]

    if os.stat(path).st_size != 0:
        split_indicis = []
        boxsize = 0
        index_first_helix = -1
        csvlines = None
        with open(path, "r") as csvfile:
            csvlines = csvfile.readlines()
            helixlines_indicies = []
            for index, row in enumerate(csvlines):
                if row.startswith("#segment"):
                    boxsize = int(float(row.split()[2]))
                elif row.startswith("#helix"):
                    boxsize = int(float(row[(row.rfind(",") + 1) :]))
                    if index_first_helix == -1:
                        index_first_helix = index
                    else:

                        split_indicis.append(
                            index - index_first_helix - (len(split_indicis) + 1)
                        )
                    helixlines_indicies.append(index)

        filaments = []
        coordinates = np.atleast_2d(np.genfromtxt(path))
        coordinates_lowleftcorner = coordinates - boxsize / 2
        coord_filaments = np.split(coordinates_lowleftcorner, split_indicis)
        #sqdistance = min_distance * min_distance

        for filament_index, filament in enumerate(coord_filaments):
            #print("FIL-----------START")
            f = Filament()
            first_and_last_coord = get_first_and_last_coord(csvlines[helixlines_indicies[filament_index]])

            bb = BoundBox(first_and_last_coord[0]-boxsize/2, first_and_last_coord[1]-boxsize/2, boxsize, boxsize)
            f.add_box(bb)

            for coords in filament:
                if len(coords)>0:
                    bb = BoundBox(coords[0], coords[1], boxsize, boxsize)
                    f.add_box(bb)

            bb = BoundBox(first_and_last_coord[2]-boxsize/2, first_and_last_coord[3]-boxsize/2, boxsize,
                               boxsize)
            f.add_box(bb)
            if min_distance>0:
                fr = utils.resample_filament(f,min_distance)
                f = fr
            
            filaments.append(f)

        return filaments
    return None


def write_eman1_helicon(filaments, path, image_filename):


    with open(path, "w", newline='', encoding='utf-8') as boxfile:
        boxwriter = csv.writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_NONE, lineterminator="\n",
        )
        # micrograph: actin_cAla_1_corrfull.mrc
        # segment length: 384
        # segment width: 384

        if filaments is not None and len(filaments) > 0:

            boxsize = filaments[0].boxes[0].w

            boxwriter.writerow(["#micrograph: " + image_filename])
            boxwriter.writerow(["#segment length: " + str(int(boxsize))])
            boxwriter.writerow(["#segment width: " + str(int(boxsize))])

            for fil in filaments:
                if len(fil.boxes) > 0:
                    boxwriter.writerow(
                        [
                            "#helix: ("
                            + str(fil.boxes[0].x + boxsize / 2)
                            + ", "
                            + str(fil.boxes[0].y + boxsize / 2)
                            + "),"
                            + "("
                            + str(fil.boxes[len(fil.boxes) - 1].x + boxsize / 2)
                            + ", "
                            + str(fil.boxes[len(fil.boxes) - 1].y + boxsize / 2)
                            + "),"
                            + str(int(boxsize))
                        ]
                    )

                    # helix: (3597.3, 2470.9),(3110.9, 3091.7000000000003),38
                    for box in fil.boxes[1:-1]:
                        boxwriter.writerow(
                            [
                                ""
                                + str(box.x + boxsize / 2)
                                + " "
                                + str(box.y + boxsize / 2)
                            ]
                        )
