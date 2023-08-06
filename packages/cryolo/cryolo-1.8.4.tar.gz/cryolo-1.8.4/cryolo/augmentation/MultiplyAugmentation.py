from cryolo.augmentation.AugmentationMethod import AugmentationMethod
from typing import List
import numpy as np

class MultiplyAugmentation(AugmentationMethod):

    def __init__(self, mult_range : List[float]):
        """
        :param mult_range: Range for random multiplier
        """
        self.mult_range = mult_range

    def transform_image(self, image : np.array) -> np.array:
        """
        Multipy the input image by a random float.
        :param image: Input image
        :return: multiplied image
        """

        rand_multiplyer = self.mult_range[0] + np.random.rand() * (
            self.mult_range[1] - self.mult_range[0]
        )
        np.multiply(image, rand_multiplyer, out=image)
        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords