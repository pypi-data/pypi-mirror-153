import unittest
import os
import pickle
from cryolo.frontend import YOLO
import cryolo.utils as utils


class FrontendTest(unittest.TestCase):
    def test_nms_no_overlapping_boxes(self):
        from cryolo.utils import non_maxima_suppress_fast

        box = utils.BoundBox(x=10, y=10, w=10, h=10, c=0, classes=[1])
        box2 = utils.BoundBox(x=20, y=20, w=10, h=10, c=0, classes=[1])

        boxes = [box, box2]
        # front = YOLO("YOLO", [768, 768], 3, ["p"], 700, [200, 200], backend_weights=None, uniitest=True)
        nms_threshold = 0.3
        obj_threshold = 0.3
        res = non_maxima_suppress_fast(boxes, 1, nms_threshold, obj_threshold)

        self.assertEqual(len(res), 2)

    def test_nms_two_overlapping(self):
        from cryolo.utils import non_maxima_suppress_fast

        box = utils.BoundBox(x=10, y=10, w=10, h=10, c=0, classes=[1])
        box2 = utils.BoundBox(x=12, y=12, w=10, h=10, c=0, classes=[1])
        box3 = utils.BoundBox(x=20, y=20, w=10, h=10, c=0, classes=[1])
        box4 = utils.BoundBox(x=22, y=22, w=10, h=10, c=0, classes=[1])

        boxes = [box, box2, box3, box4]
        nms_threshold = 0.3
        obj_threshold = 0.3
        res = non_maxima_suppress_fast(boxes, 1, nms_threshold, obj_threshold)

        self.assertEqual(len(res), 2)

    def test_nms_two_overlapping_3d(self):
        from cryolo.utils import non_maxima_suppress_fast_3d

        boxsize = 40
        box = utils.BoundBox(
            x=100, y=100, z=100, depth=boxsize, w=boxsize, h=boxsize, c=0, classes=[1]
        )
        box2 = utils.BoundBox(
            x=109, y=109, z=109, depth=boxsize, w=boxsize, h=boxsize, c=0, classes=[1]
        )
        box3 = utils.BoundBox(
            x=200, y=200, z=200, depth=boxsize, w=boxsize, h=boxsize, c=0, classes=[1]
        )
        box4 = utils.BoundBox(
            x=201, y=201, z=201, depth=boxsize, w=boxsize, h=boxsize, c=0, classes=[1]
        )
        box.meta["num_boxes"] = 1
        box2.meta["num_boxes"] = 1
        box3.meta["num_boxes"] = 1
        box4.meta["num_boxes"] = 1
        boxes = [box, box2, box3, box4]
        nms_threshold = 0.3
        obj_threshold = 0.3
        res = non_maxima_suppress_fast_3d(boxes, nms_threshold, obj_threshold)

        self.assertEqual(len(res), 2)

    def test_nms_no_overlapping_boxes_3d(self):
        from cryolo.utils import non_maxima_suppress_fast_3d

        box = utils.BoundBox(x=10, y=10, z=10, depth=10, w=10, h=10, c=0, classes=[1])
        box2 = utils.BoundBox(x=20, y=20, z=20, depth=10, w=10, h=10, c=0, classes=[1])
        box.meta["num_boxes"] = 1
        box2.meta["num_boxes"] = 1
        boxes = [box, box2]
        # front = YOLO("YOLO", [768, 768], 3, ["p"], 700, [200, 200], backend_weights=None, uniitest=True)
        nms_threshold = 0.3
        obj_threshold = 0.3
        res = non_maxima_suppress_fast_3d(boxes, nms_threshold, obj_threshold)

        self.assertEqual(len(res), 2)


if __name__ == "__main__":
    unittest.main()
