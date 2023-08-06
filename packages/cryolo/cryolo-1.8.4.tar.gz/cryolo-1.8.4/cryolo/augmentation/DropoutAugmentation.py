from cryolo.augmentation.AugmentationMethod import AugmentationMethod

import numpy as np

class DropoutAugmentation(AugmentationMethod):

    def __init__(self, ratio : list):
        """
        :param ratio: Range for random ratio
        """
        self.ratio = ratio

    def transform_image(self, image : np.array) -> np.array:
        """
        Set a random selection of pixels to the mean of the image
        :param image: Input image
        :return: Modified image
        """
        if isinstance(self.ratio, float):
            rand_ratio = self.ratio
        else:
            rand_ratio = self.ratio[0] + np.random.rand() * (self.ratio[1] - self.ratio[0])
        mean_val = np.mean(image)
        drop = np.random.binomial(
            n=1, p=1 - rand_ratio, size=(image.shape[0], image.shape[1])
        )
        image[drop == 0] = mean_val

        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords