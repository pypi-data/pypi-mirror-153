import unittest
import numpy as np
import random
import time
from cryolo.augmentation.augmentation import Augmentation
from cryolo.augmentation.FlipAugmentation import FlipAugmentation
from cryolo.augmentation.CustomRotationAugmentation import CustomRotationAugmentation
from cryolo.augmentation.Rot90Augmentation import Rot90Augmentation
from cryolo.augmentation.AddConstantAugmentation import AddConstantAugmentation
from cryolo.augmentation.AdditiveGaussianNoiseAugmentation import (
    AdditiveGaussianNoiseAugmentation,
)
from cryolo.augmentation.AverageBlurAugmentation import AverageBlurAugmentation
from cryolo.augmentation.ContrastNormalizationAugmentation import (
    ContrastNormalizationAugmentation,
)
from cryolo.augmentation.DropoutAugmentation import DropoutAugmentation
from cryolo.augmentation.GaussBlurAugmentation import GaussBlurAugmentation


class AugTest(unittest.TestCase):
    def test_custom_rotation_augmentation_rot90_1x(self):
        img_width = 1024
        img_height = 1024
        boxwh = 100
        obj = {}
        box_center_x = 50
        box_center_y = 50

        obj["xmax"] = box_center_x + boxwh / 2
        obj["xmin"] = 0
        obj["ymax"] = box_center_y + boxwh / 2
        obj["ymin"] = 0
        obj["angle"] = np.pi / 2

        exp_obj = {}
        exp_obj["xmax"] = img_width - obj["ymin"]
        exp_obj["xmin"] = img_width - obj["ymax"]
        exp_obj["ymax"] = obj["xmax"]
        exp_obj["ymin"] = obj["xmin"]
        exp_obj["angle"] = obj["angle"] + np.pi / 2

        aug = Rot90Augmentation(1)

        aug_obj = aug.transform_coords([obj], image_dims=[img_width, img_height])[0]
        print(aug_obj)
        self.assertEqual(aug_obj["xmax"], exp_obj["xmax"], "Xmax is not the same")
        self.assertEqual(aug_obj["xmin"], exp_obj["xmin"], "Xmin is not the same")
        self.assertEqual(aug_obj["ymax"], exp_obj["ymax"], "ymax is not the same")
        self.assertEqual(aug_obj["ymin"], exp_obj["ymin"], "ymin is not the same")
        self.assertEqual(aug_obj["angle"], exp_obj["angle"], "angle is not the same")

    def test_custom_rotation_augmentation_rot90_4x(self):

        img_width = 1024
        img_height = 512
        boxwh = 100
        obj = {}
        box_center_x = 50
        box_center_y = 50

        obj["xmax"] = box_center_x + boxwh / 2
        obj["xmin"] = 0
        obj["ymax"] = box_center_y + boxwh / 2
        obj["ymin"] = 0
        obj["angle"] = np.pi / 2

        aug = Rot90Augmentation(4)

        aug_obj = aug.transform_coords([obj], image_dims=[img_width, img_height])[0]

        self.assertEqual(aug_obj["xmax"], obj["xmax"], "Xmax is not the same")
        self.assertEqual(aug_obj["xmin"], obj["xmin"], "Xmin is not the same")
        self.assertEqual(aug_obj["ymax"], obj["ymax"], "ymax is not the same")
        self.assertEqual(aug_obj["ymin"], obj["ymin"], "ymin is not the same")
        self.assertEqual(aug_obj["angle"], obj["angle"], "angle is not the same")

    def test_custom_rotation_augmentation_flip_vertical(self):

        img_width = 512
        img_height = 512
        boxwh = 100
        obj = {}
        obj["xmax"] = boxwh
        obj["xmin"] = 0
        obj["ymax"] = boxwh
        obj["ymin"] = 0
        obj["angle"] = np.pi / 2

        exp_obj = {}
        exp_obj["xmax"] = img_width - obj["xmin"]
        exp_obj["xmin"] = img_width - obj["xmax"]
        exp_obj["ymax"] = obj["ymax"]
        exp_obj["ymin"] = obj["ymin"]
        exp_obj["angle"] = np.pi - obj["angle"]
        aug = FlipAugmentation(FlipAugmentation.FLIP_VERTICAL)

        aug_obj = aug.transform_coords([obj], image_dims=[512, 512])[0]

        self.assertEqual(aug_obj["xmax"], exp_obj["xmax"], "Xmax is not the same")
        self.assertEqual(aug_obj["xmin"], exp_obj["xmin"], "Xmin is not the same")
        self.assertEqual(aug_obj["ymax"], exp_obj["ymax"], "ymax is not the same")
        self.assertEqual(aug_obj["ymin"], exp_obj["ymin"], "ymin is not the same")
        self.assertEqual(aug_obj["angle"], exp_obj["angle"], "angle is not the same")

    def test_custom_rotation_augmentation_rot90(self):

        rotation_center_x = 128
        rotation_center_y = 128
        boxwh = 10
        center_x = rotation_center_x + 10
        center_y = rotation_center_y + 0

        center_after_rot_x = rotation_center_x + 0
        center_after_rot_y = rotation_center_y - 10

        obj = {}
        obj["xmax"] = center_x + boxwh
        obj["xmin"] = center_x - boxwh
        obj["ymax"] = center_y + boxwh
        obj["ymin"] = center_y - boxwh
        obj["angle"] = np.pi / 2

        exp_obj = {}
        exp_obj["xmax"] = center_after_rot_x + boxwh
        exp_obj["xmin"] = center_after_rot_x - boxwh
        exp_obj["ymax"] = center_after_rot_y + boxwh
        exp_obj["ymin"] = center_after_rot_y - boxwh
        exp_obj["angle"] = np.pi / 2 - np.pi / 2
        cust_rot = CustomRotationAugmentation(np.deg2rad(90))
        rot_obj = cust_rot.transform_coords([obj], image_dims=[256, 256])[0]

        self.assertEqual(rot_obj["xmax"], exp_obj["xmax"], "Xmax is not the same")
        self.assertEqual(rot_obj["xmin"], exp_obj["xmin"], "Xmin is not the same")
        self.assertEqual(rot_obj["ymax"], exp_obj["ymax"], "ymax is not the same")
        self.assertEqual(rot_obj["ymin"], exp_obj["ymin"], "ymin is not the same")
        self.assertEqual(rot_obj["angle"], exp_obj["angle"], "angle is not the same")

    def test_custom_rotation_augmentation_rot360(self):
        rotation_center_x = 128
        rotation_center_y = 128
        boxwh = 10
        center_x = rotation_center_x + 10
        center_y = rotation_center_y + 0

        center_after_rot_x = rotation_center_x + 10
        center_after_rot_y = rotation_center_y + 0

        obj = {}
        obj["xmax"] = center_x + boxwh
        obj["xmin"] = center_x - boxwh
        obj["ymax"] = center_y + boxwh
        obj["ymin"] = center_y - boxwh
        obj["angle"] = np.pi / 4

        exp_obj = {}
        exp_obj["xmax"] = center_after_rot_x + boxwh
        exp_obj["xmin"] = center_after_rot_x - boxwh
        exp_obj["ymax"] = center_after_rot_y + boxwh
        exp_obj["ymin"] = center_after_rot_y - boxwh
        exp_obj["angle"] = np.pi / 4

        cust_rot = CustomRotationAugmentation(np.deg2rad(360))
        rot_obj = cust_rot.transform_coords([obj], image_dims=[256, 256])[0]

        self.assertEqual(rot_obj["xmax"], exp_obj["xmax"], "Xmax is not the same")
        self.assertEqual(rot_obj["xmin"], exp_obj["xmin"], "Xmin is not the same")
        self.assertEqual(rot_obj["ymax"], exp_obj["ymax"], "ymax is not the same")
        self.assertEqual(rot_obj["ymin"], exp_obj["ymin"], "ymin is not the same")
        self.assertEqual(rot_obj["angle"], exp_obj["angle"], "angle is not the same")

    def test_custom_rotation_augmentation_rot720(self):
        rotation_center_x = 128
        rotation_center_y = 128
        boxwh = 10
        center_x = rotation_center_x + 10
        center_y = rotation_center_y + 0

        center_after_rot_x = rotation_center_x + 10
        center_after_rot_y = rotation_center_y + 0

        obj = {}
        obj["xmax"] = center_x + boxwh
        obj["xmin"] = center_x - boxwh
        obj["ymax"] = center_y + boxwh
        obj["ymin"] = center_y - boxwh
        obj["angle"] = np.pi / 4

        exp_obj = {}
        exp_obj["xmax"] = center_after_rot_x + boxwh
        exp_obj["xmin"] = center_after_rot_x - boxwh
        exp_obj["ymax"] = center_after_rot_y + boxwh
        exp_obj["ymin"] = center_after_rot_y - boxwh
        exp_obj["angle"] = np.pi / 4
        cust_rot = CustomRotationAugmentation(np.deg2rad(720))
        rot_obj = cust_rot.transform_coords([obj], image_dims=[256, 256])[0]

        self.assertEqual(rot_obj["xmax"], exp_obj["xmax"], "Xmax is not the same")
        self.assertEqual(rot_obj["xmin"], exp_obj["xmin"], "Xmin is not the same")
        self.assertEqual(rot_obj["ymax"], exp_obj["ymax"], "ymax is not the same")
        self.assertEqual(rot_obj["ymin"], exp_obj["ymin"], "ymin is not the same")
        self.assertAlmostEqual(
            rot_obj["angle"], exp_obj["angle"], places=5, msg="angle is not the same"
        )

    def test_image_augmentation_time(self):
        np.random.seed(6)
        random.seed(10)
        img = np.random.random_sample(size=(4096, 4096)) * 255
        img = img.astype(np.uint8)
        img = img.astype(np.float32)
        start = time.time()
        aug = Augmentation(True)
        for i in range(10):
            aug.image_augmentation(img.copy())
            # aug.gauss_blur(img.copy())
            # print img.dtype
        end = time.time()

    def test_image_augmentation_float32(self):
        np.random.seed(6)
        random.seed(10)
        img = np.random.random_sample(size=(10, 10))
        img = img.astype(np.float32)
        aug = Augmentation()
        result = aug.image_augmentation(img.copy())
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "Image augmentation failed. Type is not correct")

    def test_image_augmentation_uint8(self):
        np.random.seed(7)
        random.seed(10)
        img = np.random.randint(0, 255, size=(10, 10))
        img = img.astype(np.float32)
        aug = Augmentation(True)
        result = aug.image_augmentation(img.copy())
        is_int = np.issubdtype(result.dtype, np.uint8)
        self.assertTrue(is_int, "Image augmentation failed. Type is not correct")

    def test_additive_gauss_noise_typecheck_float32(self):
        img = np.random.random_sample(size=(3, 3))
        img = img.astype(np.float32)
        aug = AdditiveGaussianNoiseAugmentation(0.05)
        result = aug.transform_image(img.copy())
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "ADD GAUSS NOISE FLOAT32 failed. Type is not correct")

    def test_avg_blur_float32(self):
        np.random.seed(7)
        img = np.random.random_sample(size=(3, 3))
        img = img.astype(np.float32)
        aug = AverageBlurAugmentation([3, 4])
        result = aug.transform_image(img.copy())
        t = np.allclose(np.mean(img), result[1, 1], atol=0.0001)
        self.assertTrue(t, "AVG BLUR FLOAT32 failed.")
        is_float = np.issubdtype(result.dtype, np.float32)
        self.assertTrue(is_float, "AVG BLUR FLOAT32 failed. Type is not correct")

    def test_avg_blur_uint8(self):
        np.random.seed(7)
        img = np.random.randint(0, 255, size=(3, 3))
        print(img)
        img = img.astype(np.uint8)
        aug = AverageBlurAugmentation([3, 4])
        result = aug.transform_image(img.copy())
        self.assertEqual(140, result[1, 1])
        is_int = np.issubdtype(result.dtype, np.uint8)
        self.assertTrue(is_int, "Avg blurring failed. Type is not correct")

    def test_gaussian_blur_float32(self):
        np.random.seed(7)
        img = np.random.random_sample(size=(3, 3))
        aug = GaussBlurAugmentation(sigma_range=[0, 3])
        result = aug.transform_image(img.copy())
        print(result)
        img_exp = [
            [0.3956204, 0.45140969, 0.4693832],
            [0.43998803, 0.44855732, 0.43916815],
            [0.43967383, 0.40600407, 0.37695657],
        ]
        t = np.allclose(img_exp, result, atol=0.00001)
        self.assertTrue(t, "Gaussian blurring failed")
        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Gaussian blurring failed. Type is not correct")

    def test_gaussian_blur_uint8(self):
        np.random.seed(7)
        img = np.random.randint(0, 255, size=(3, 3))
        img = img.astype(np.float32)
        aug = GaussBlurAugmentation(sigma_range=[0, 3])
        result = aug.transform_image(img.copy())
        result = result.astype(np.uint8)
        print(result)
        img_exp = [[178, 144, 99], [175, 140, 125], [154, 125, 115]]
        t = np.array_equal(img_exp, result)
        self.assertTrue(t, "Gaussian blurring failed")

        is_int = np.issubdtype(result.dtype, np.integer)

        self.assertTrue(is_int, "Gaussian blurring failed. Type is not correct")

    def test_contrast_normalization_float32(self):
        np.random.seed(9)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255
        aug = ContrastNormalizationAugmentation([0.5, 2.0])
        print(img)
        result = aug.transform_image(img.copy())
        print(result)

        img_exp = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 131.46811]])

        t = np.allclose(img_exp, result, atol=0.0001)
        self.assertTrue(
            t, msg="Contrast normalization failed. Result is not as expected"
        )

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Contrast normalization failed. Type is not correct")

    def test_contrast_normalization_uint8(self):
        np.random.seed(9)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255
        aug = ContrastNormalizationAugmentation([0.5, 2.0])
        result = aug.transform_image(img.copy())
        print(result)
        result = result.astype(np.uint8)
        img_exp = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 131]])

        t = np.allclose(img_exp, result, atol=0.0001)

        self.assertTrue(
            t, msg="Contrast normalization failed. Result is not as expected"
        )

    def test_add_float32(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        img[0, 0] = 0
        img[2, 2] = 10
        aug = AddConstantAugmentation(0.1)
        result = aug.transform_image(img.copy())
        t = np.array_equal(img + 0.46959287, result)
        self.assertTrue(t, msg="Add failed. Result is not as expected")

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Add failed. Type is not correct")

    def test_add_uint8(self):
        np.random.seed(10)
        img = np.zeros((3, 3), dtype="float32")
        img[2, 2] = 255

        aug = AddConstantAugmentation(0.1)
        result = aug.transform_image(img.copy())
        result = np.clip(result, 0, 255)
        print(result)
        img_exp = img + 13.045981748296022
        img_exp[2, 2] = 255.0
        t = np.array_equal(img_exp, result)

        self.assertTrue(t, msg="Add failed. Result is not as expected")

    def test_multiply_float32(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        aug = Augmentation()
        result = aug.multiply(img.copy())
        img_exp = img * 1.27132064327
        t = np.array_equal(img_exp, result)
        self.assertTrue(
            t, msg="Float 32 multiplication failed. Result is not as expected"
        )

        is_float = np.issubdtype(result.dtype, np.float32)

        self.assertTrue(is_float, "Multiplication failed. Type is not correct")

    def test_multiply_uint8(self):
        np.random.seed(10)
        img = np.ones((3, 3), dtype="float32")
        img = img * 100
        img[2, 2] = 250
        aug = Augmentation(True)
        result = aug.multiply(img.copy())
        np.clip(result, 0, 255, out=result)
        result = result.astype(np.uint8, copy=False)

        img_exp = [[127, 127, 127], [127, 127, 127], [127, 127, 255]]

        t = np.array_equal(img_exp, result)
        self.assertTrue(t, msg="unit8 multiplication failed. Result is not as expected")

        is_int = np.issubdtype(result.dtype, np.uint8)

        self.assertTrue(is_int, "Multiplication failed. Type is not correct")

    def test_dropout_5x5_float32(self):
        np.random.seed(10)
        img = np.ones((6, 6), dtype="float32")
        img[:3, :] = 3
        aug = DropoutAugmentation(0.1)
        res = aug.transform_image(img.copy())
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(3, num_zero_elements, "Dropout test failed.")

        is_float = np.issubdtype(res.dtype, np.float32)

        self.assertTrue(is_float, "Dropout failed. Type is not correct")

    def test_dropout_5x5_uint8(self):
        np.random.seed(10)
        img = np.ones((6, 6), dtype="float32")
        img[:3, :] = 3
        aug = DropoutAugmentation(0.1)
        res = aug.transform_image(img.copy())
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(3, num_zero_elements, "Dropout test failed.")

    def test_dropout_10x10_uint8(self):
        np.random.seed(10)
        img = np.ones((10, 10), dtype="float32")
        img[:5, :] = 3
        aug = DropoutAugmentation(0.1)
        res = aug.transform_image(img.copy())
        num_zero_elements = np.sum(res == 2)
        self.assertEqual(8, num_zero_elements, "Dropout test failed.")
