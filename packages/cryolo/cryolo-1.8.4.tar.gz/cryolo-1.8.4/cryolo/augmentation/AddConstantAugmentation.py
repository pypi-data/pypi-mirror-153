from cryolo.augmentation.AugmentationMethod import AugmentationMethod

import numpy as np

class AddConstantAugmentation(AugmentationMethod):

    def __init__(self, scale : float):
        """
        :param scale: Scale for random constant. The random constant
        will be between 0 and scale*6*std(image)
        """
        self.scale = scale

    def transform_image(self, image : np.array) -> np.array:
        """
        Adds a random constant to the image
        :param image: Input image
        :return: Modified image
        """
        width = 2 * 3 * np.std(image)
        width_rand = self.scale * width
        rand_constant = (np.random.rand() * width_rand) - width_rand / 2
        np.add(image, rand_constant, out=image)
        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords