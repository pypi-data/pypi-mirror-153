import copy

import numpy as np
from scipy import ndimage

from cryolo.augmentation.AugmentationMethod import AugmentationMethod


class CustomRotationAugmentation(AugmentationMethod):

    def __init__(self, rotation_angle_rad : float):
        self.rotation_in_rad = rotation_angle_rad

    def transform_image(self, image : np.array) -> np.array:
        return ndimage.rotate(image, np.rad2deg(self.rotation_in_rad), reshape=False, mode='reflect', order=1)

    def transform_coords(self, object_coords : list, image_dims: list) -> list:
        hcenter = float(image_dims[1]) / 2
        wcenter = float(image_dims[0]) / 2

        object_coords_cpy = copy.deepcopy(object_coords)

        for obj in object_coords_cpy:
            # 1. calculate center coordinate of object
            rotational_center_x = wcenter
            rotational_center_y = hcenter
            center_x = obj["xmin"] + (obj["xmax"] - obj["xmin"]) / 2 - rotational_center_x
            center_y = obj["ymin"] + (obj["ymax"] - obj["ymin"]) / 2 - rotational_center_y

            # 2. rotate center point
            c, s = np.cos(-1*self.rotation_in_rad), np.sin(-1*self.rotation_in_rad)
            R = np.array(((c, -s), (s, c)))

            #rot_point = R @ np.array([center_x, center_y])
            rot_point =  np.dot(R, np.array([center_x, center_y])) #matmul leads to errors in docker ci unittesting
            rot_point[0] = rot_point[0] + rotational_center_x
            rot_point[1] = rot_point[1] + rotational_center_y

            # 4. calculate new xmin/max
            boxw = obj["xmax"] - obj["xmin"]
            boxh = obj["ymax"] - obj["ymin"]
            obj["xmin"] = rot_point[0] - boxw / 2
            obj["xmax"] = rot_point[0] + boxw / 2
            obj["ymin"] = rot_point[1] - boxh / 2
            obj["ymax"] = rot_point[1] + boxh / 2

            # 3. update angle by adding rotation range c
            if "angle" in obj:
                obj["angle"] = obj["angle"] - self.rotation_in_rad
                while obj["angle"] < 0:
                    obj["angle"] = obj["angle"] + np.pi
        return object_coords_cpy