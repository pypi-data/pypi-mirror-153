from cryolo.augmentation.AugmentationMethod import AugmentationMethod

import numpy as np

class AdditiveGaussianNoiseAugmentation(AugmentationMethod):

    def __init__(self, max_sigma_range_factor : float):
        """
        :param max_sigma_range_factor: Range for max_sigma_range. The standard deviation of the noise
        is choosen randomly depending on the standard deviation of the image.
        """
        self.max_sigma_range_factor = max_sigma_range_factor

    def transform_image(self, image : np.array) -> np.array:
        """
        Add random gaussian noise to image
        :param image: Input image
        choosen randomly depending on the standard deviation of the image.
        The choosen standard deviation for noise is between: 0 and  max_sigma_factor*6*np.std(image)
        :return: noise added image
        """
        width = 2 * 3 * np.std(image)
        max_sigma = width * self.max_sigma_range_factor
        rand_sigma = np.random.rand() * max_sigma
        noise = np.random.randn(image.shape[0], image.shape[1])

        # image = noise*rand_sigma + image

        np.multiply(noise, rand_sigma, out=noise)
        np.add(image, noise, out=image)

        if not np.issubdtype(image.dtype, np.float32):
            image = image.astype(np.float32, copy=False)

        return image

    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords