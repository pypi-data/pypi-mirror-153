import copy

import numpy as np

from cryolo.augmentation.AugmentationMethod import AugmentationMethod


class Rot90Augmentation(AugmentationMethod):

    def __init__(self, num_rotations : float):
        self.num_rotations = num_rotations

    def transform_image(self, image : np.array) -> np.array:

        if np.squeeze(image).shape[0] != np.squeeze(image).shape[1] and self.num_rotations % 2 != 0:
            raise ValueError("Rotational data augmentations failed. For non-square images the number of rotations needs even.")

        image = np.rot90(image, k=self.num_rotations, axes=(1, 0))
        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        object_coords_cpy = copy.deepcopy(object_coords)
        for obj in object_coords_cpy:
            hcenter = float(image_dims[1]) / 2
            wcenter = float(image_dims[0]) / 2

            for i in range(self.num_rotations):
                obj["xmin"] = obj["xmin"] - wcenter
                obj["xmax"] = obj["xmax"] - wcenter
                obj["ymin"] = obj["ymin"] - hcenter
                obj["ymax"] = obj["ymax"] - hcenter

                help = obj["xmin"]
                obj["xmin"] = -1 * obj["ymin"]
                obj["ymin"] = help

                help = obj["xmax"]
                obj["xmax"] = -1 * obj["ymax"]
                obj["ymax"] = help

                obj["xmin"] = obj["xmin"] + wcenter
                obj["xmax"] = obj["xmax"] + wcenter
                obj["ymin"] = obj["ymin"] + hcenter
                obj["ymax"] = obj["ymax"] + hcenter

                # Swap xmin and xmax
                help = obj["xmax"]
                obj["xmax"] = obj["xmin"]
                obj["xmin"] = help

                if "angle" in obj:
                    obj["angle"] = obj["angle"] + np.pi / 2
                    if obj["angle"] > np.pi:
                        obj["angle"] = obj["angle"] - np.pi

        return object_coords_cpy