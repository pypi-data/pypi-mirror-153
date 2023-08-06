from cryolo.augmentation.AugmentationMethod import AugmentationMethod
from scipy import ndimage

import numpy as np

class AverageBlurAugmentation(AugmentationMethod):

    def __init__(self, kernel_size : list):
        """
        :param kernel_size: Range for random kernel size
        """

        self.kernel_size = kernel_size

    def transform_image(self, image : np.array) -> np.array:
        """
        Applys average blurring with random kernel size
        :param image: Input image (numpy array)
        :return: Blurred image
        """
        rang_kernel_size = np.random.randint(self.kernel_size[0], self.kernel_size[1])
        image = ndimage.uniform_filter(
            image, size=rang_kernel_size, mode="nearest", output=image
        )
        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords
