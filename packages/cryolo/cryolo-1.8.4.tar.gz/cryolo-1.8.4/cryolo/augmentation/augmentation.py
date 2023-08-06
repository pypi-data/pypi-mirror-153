"""
Author: Thorsten Wagner (thorsten.wagner@mpi-dortmund.mpg.de)
"""
#
# COPYRIGHT
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#

import random
import numpy as np
from cryolo.augmentation.GaussBlurAugmentation import GaussBlurAugmentation
from cryolo.augmentation.AverageBlurAugmentation import AverageBlurAugmentation
from cryolo.augmentation.AdditiveGaussianNoiseAugmentation import AdditiveGaussianNoiseAugmentation
from cryolo.augmentation.AddConstantAugmentation import AddConstantAugmentation
from cryolo.augmentation.ContrastNormalizationAugmentation import ContrastNormalizationAugmentation
from cryolo.augmentation.DropoutAugmentation import DropoutAugmentation
from cryolo.augmentation.MultiplyAugmentation import MultiplyAugmentation

class Augmentation:
    """
    Class for doing data augmentation
    """

    def __init__(self, is_grey=False):
        self.is_grey = is_grey

    def image_augmentation(self, image):
        """
        Applies random selection of data augmentations
        :param image:  Input image
        :return: Augmented image
        """

        gauss_blur = GaussBlurAugmentation(sigma_range=[0, 3])
        avg_blur = AverageBlurAugmentation(kernel_size=[2, 7])
        gauss_noise = AdditiveGaussianNoiseAugmentation(max_sigma_range_factor=0.05)
        add_constant = AddConstantAugmentation(scale=0.05)
        constrast_normalization = ContrastNormalizationAugmentation(alpha_range=[0.5, 2.0])
        dropout = DropoutAugmentation(ratio=[0.01, 0.1])
        multiply = MultiplyAugmentation(mult_range=[0.5, 1.5])
        augmentations = [
            gauss_noise.transform_image,
            add_constant.transform_image,
            constrast_normalization.transform_image,
            multiply.transform_image,
            dropout.transform_image,
        ]

        num_augs = np.random.randint(0, np.minimum(6, len(augmentations)))
        if num_augs > 0:

            if np.random.rand() > 0.5:
                augmentations.append(gauss_blur.transform_image)
            else:
                augmentations.append(avg_blur.transform_image)

            selected_augs = random.sample(augmentations, num_augs)
            image = image.astype(np.float32, copy=False)
            for sel_aug in selected_augs:
                image = sel_aug(image)
            #   print "Mean after", sel_aug, " sum: ", np.mean(image)
            if self.is_grey:
                min_img = np.min(image)
                max_img = np.max(image)
                image = ((image - min_img) / (max_img - min_img)) * 255
                #    image = np.clip(image, 0, 255)
                image = image.astype(np.uint8, copy=False)

        return image



    def multiply(self, image, mult_range=(0.5, 1.5)):
        """
        Multipy the input image by a random float.
        :param image: Input image
        :param mult_range: Range for random multiplier
        :return: multiplied image
        """

        rand_multiplyer = mult_range[0] + np.random.rand() * (
            mult_range[1] - mult_range[0]
        )
        np.multiply(image, rand_multiplyer, out=image)
        return image
