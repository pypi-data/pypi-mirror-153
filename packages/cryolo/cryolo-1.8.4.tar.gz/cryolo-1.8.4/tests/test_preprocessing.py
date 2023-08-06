import unittest
import os
import cryolo.preprocessing


class MyTestCase(unittest.TestCase):
    def test_is_helicon_with_particle_coords_should_be_false(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/Myo5ADP_0682.txt")
        is_helicon = cryolo.preprocessing.is_helicon_with_particle_coords(path)
        self.assertFalse(is_helicon)

    def test_is_eman1_helicion_should_be_true(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/Myo5ADP_0682.txt")
        is_eman1 = cryolo.preprocessing.is_eman1_helicion(path)
        self.assertTrue(is_eman1)
