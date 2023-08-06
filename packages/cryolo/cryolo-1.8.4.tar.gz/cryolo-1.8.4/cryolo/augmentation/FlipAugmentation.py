import copy

import numpy as np

from cryolo.augmentation.AugmentationMethod import AugmentationMethod


class FlipAugmentation(AugmentationMethod):

    FLIP_BOTH = 1
    FLIP_HORIZONTAL = 2
    FLIP_VERTICAL = 3

    def __init__(self, flipping_mode):
        if flipping_mode not in [0,1,2,3]:
            raise ValueError("Flipping mode is not supported")
        self.flipping_mode = flipping_mode


    def transform_image(self, image: np.array) -> np.array:

        if self.flipping_mode == self.FLIP_VERTICAL:
            image = np.flip(image, 1)
        if self.flipping_mode == self.FLIP_HORIZONTAL:
            image = np.flip(image, 0)
        if self.flipping_mode == self.FLIP_BOTH:
            image = np.flip(np.flip(image, 0), 1)

        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        '''

        :param object_coords:
        :param image_dims: list of image width and image height
        :return:
        '''

        object_coords_cpy = copy.deepcopy(object_coords)
        for obj in object_coords_cpy:
            if self.flipping_mode == self.FLIP_VERTICAL or self.flipping_mode == self.FLIP_BOTH:
                xmin = obj["xmin"]
                obj["xmin"] = image_dims[0] - obj["xmax"]
                obj["xmax"] = image_dims[0] - xmin

            if self.flipping_mode == self.FLIP_HORIZONTAL or self.flipping_mode == self.FLIP_BOTH:
                ymin = obj["ymin"]
                obj["ymin"] = image_dims[1] - obj["ymax"]
                obj["ymax"] = image_dims[1] - ymin

            if "angle" in obj and (self.flipping_mode in [self.FLIP_HORIZONTAL, self.FLIP_VERTICAL]):
                # in case of flip_both the direction doesnt change...
                obj["angle"] = np.pi - obj["angle"]

        return object_coords_cpy