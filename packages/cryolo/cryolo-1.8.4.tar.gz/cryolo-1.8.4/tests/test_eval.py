import unittest
from cryolo import eval
import os


class MyTestCase(unittest.TestCase):
    def test_readbox(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/2018_08_14_BBSXL_AuXPos1_02791.box"
        )
        boxes = eval.read_box(path, 0)

        self.assertEqual(len(boxes), 1)


if __name__ == "__main__":
    unittest.main()
