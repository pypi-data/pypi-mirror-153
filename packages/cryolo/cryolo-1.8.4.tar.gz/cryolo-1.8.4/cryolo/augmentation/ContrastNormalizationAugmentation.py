from cryolo.augmentation.AugmentationMethod import AugmentationMethod

import numpy as np

class ContrastNormalizationAugmentation(AugmentationMethod):

    def __init__(self, alpha_range : list):
        """
        :param alpha_range: Range for alpha. Alpha controls the normalization.
        """
        self.alpha_range = alpha_range

    def transform_image(self, image : np.array) -> np.array:
        """
        Spread or squeeze the pixel values.
        :param image: Input image
        :return: Modified image
        """
        rand_multiplyer = self.alpha_range[0] + np.random.rand() * (
                self.alpha_range[1] - self.alpha_range[0]
        )
        middle = np.median(image)
        np.subtract(image, middle, out=image)
        np.multiply(rand_multiplyer, image, out=image)
        np.add(middle, image, out=image)

        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords