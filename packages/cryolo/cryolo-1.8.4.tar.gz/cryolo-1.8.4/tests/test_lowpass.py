import unittest
from cryolo.lowpass import zero_pad, next_power_of2
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_zeropad_correct_size(self):

        img = np.zeros((5, 5)) + 1
        new_size = (10, 10)
        padded, _ = zero_pad(img, new_size)
        self.assertTupleEqual(padded.shape, new_size)

    def test_next_power_of2(self):

        num = next_power_of2(2 ** 2 + 1)
        self.assertEqual(num, 2 ** 3)


if __name__ == "__main__":
    unittest.main()
