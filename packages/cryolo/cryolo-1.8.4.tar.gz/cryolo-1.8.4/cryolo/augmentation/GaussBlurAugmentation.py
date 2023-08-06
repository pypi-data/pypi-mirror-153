import numpy as np
from cryolo.augmentation.AugmentationMethod import AugmentationMethod
from scipy import ndimage

class GaussBlurAugmentation(AugmentationMethod):

    def __init__(self, sigma_range : list):
        self.sigma_range = sigma_range

    def transform_image(self, image: np.array) -> np.array:
        """
        Applys gaussian blurring with random sigma
        :param image: Input image
        :return: Blurred image
        """
        
        rand_sigma = self.sigma_range[0] + np.random.rand() * (
                self.sigma_range[1] - self.sigma_range[0]
        )
        result = ndimage.gaussian_filter(
            image, sigma=rand_sigma, mode="nearest", output=image
        )

        if not np.issubdtype(image.dtype, np.float32):
            result = result.astype(np.float32, copy=False)
        return result


    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        return object_coords