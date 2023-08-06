import unittest
import cryolo.filament_tracer
from cryolo.utils import BoundBox
import numpy as np
import random
from cryolo.utils import Filament
import matplotlib.pyplot as plt
import os


class FilamentReplacerTest(unittest.TestCase):
    def test_is_valid(self):

        ref_angle = 0
        delta_angle = 10
        test_angle = 180

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertTrue(valid)

    def test_is_valid_2(self):
        ref_angle = 0
        delta_angle = 10
        test_angle = 0

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertTrue(valid)

    def test_is_valid_3(self):
        ref_angle = 0
        delta_angle = 10
        test_angle = 11

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertFalse(valid)

    def test_is_valid_4(self):
        ref_angle = 0
        delta_angle = 10
        test_angle = 169

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertFalse(valid)

    def test_is_valid_5(self):
        ref_angle = 70
        delta_angle = 10
        test_angle = 81

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertFalse(valid)

    def test_is_valid_6(self):
        ref_angle = 180
        delta_angle = 10
        test_angle = 5

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertTrue(valid)

    def test_is_valid_7(self):

        ref_angle = 178
        delta_angle = 10
        test_angle = 2

        valid = cryolo.filament_tracer.is_valid(ref_angle, delta_angle, test_angle)

        self.assertTrue(valid)

    def test_angle_between_two_boxes_90degree(self):
        boxa = BoundBox(x=0, y=1, w=10, h=10)
        boxb = BoundBox(x=1, y=0, w=10, h=10)

        angle = cryolo.filament_tracer.angle_between_two_boxes(boxa, boxb)

        self.assertAlmostEqual(first=90, second=angle, places=1)

    def test_angle_between_two_boxes_0degree(self):
        boxa = BoundBox(x=3, y=3, w=10, h=10)
        boxb = BoundBox(x=3, y=3, w=10, h=10)

        angle = cryolo.filament_tracer.angle_between_two_boxes(boxa, boxb)

        self.assertAlmostEqual(first=0, second=angle, places=1)

    def test_angle_between_two_boxes_45degree(self):
        boxa = BoundBox(x=3, y=3, w=10, h=10)
        boxb = BoundBox(x=0, y=3, w=10, h=10)

        angle = cryolo.filament_tracer.angle_between_two_boxes(boxa, boxb)

        self.assertAlmostEqual(first=45, second=angle, places=1)

    def test_angle_between_two_boxes_180degree(self):
        boxa = BoundBox(x=1, y=1, w=10, h=10)
        boxb = BoundBox(x=-1, y=-1, w=10, h=10)

        angle = cryolo.filament_tracer.angle_between_two_boxes(boxa, boxb)

        self.assertAlmostEqual(first=180, second=angle, places=1)

    def test_next_valid_box(self):

        angle_image = np.zeros(shape=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))
        for i in range(250, 750, 5):
            boxes.append(BoundBox(x=512 - 10 - width / 2, y=i, w=width / 2, h=width))

        assigned = []
        assigned.append(boxes[0])

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, search_radius=60, angle_delta=10
        )
        candidate_boxes = [box for box in boxes if box not in assigned]
        next_box_index = tracer.next_valid_box(
            filament=None, candidate_boxes=candidate_boxes, ref_box=boxes[0]
        )

        self.assertEqual(boxes[1], candidate_boxes[0])

    def test_correct_merging(self):

        angle_image = np.zeros(shape=(1024, 1024))
        angle_image[250:750, 512 - 40 : 512 + 40] = 90

        angle_image[750:1000, 512 - 40 : 512 + 40] = 90

        boxes = []
        width = 30
        for i in range(250, 300, 10):
            box = BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width)
            boxes.append(box)
            print(box.x, box.y)
        print("First part:", len(boxes))
        len1 = len(boxes)
        for i in range(300, 350, 10):
            box = BoundBox(
                x=512 - 15 - width / 2, y=i - width / 2, w=width / 2, h=width
            )
            boxes.append(box)
            print(box.x, box.y)
        print("Secondpart part:", len(boxes) - len1)
        len1 = len(boxes)
        assigned = []
        assigned.append(boxes[0])

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, search_radius=30, angle_delta=10
        )
        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments))

    def test_correct_merging_numboxes(self):

        angle_image = np.zeros(shape=(1024, 1024))
        angle_image[250:750, 512 - 40 : 512 + 40] = 90

        angle_image[750:1000, 512 - 40 : 512 + 40] = 90

        boxes = []
        width = 30
        for i in range(250, 300, 10):
            box = BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width)
            boxes.append(box)
            print(box.x, box.y)
        print("First part:", len(boxes))
        len1 = len(boxes)
        for i in range(290, 340, 10):
            box = BoundBox(
                x=512 - 16 - width / 2, y=i - width / 2, w=width / 2, h=width
            )
            boxes.append(box)
            print(box.x, box.y)
        print("Secondpart part:", len(boxes) - len1)
        len1 = len(boxes)
        assigned = []
        assigned.append(boxes[0])

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, search_radius=60, angle_delta=10
        )
        filaments = tracer.trace_filaments()

        self.assertEqual(5, len(filaments[0].boxes))
        self.assertEqual(5, len(filaments[1].boxes))

    def test_split_filament(self):

        boxes = []
        width = 30
        boxes.append(BoundBox(x=100 - width / 2, y=100 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=101 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=102 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=103 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=104 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=105 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=106 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=107 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=108 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=100 - width / 2, y=109 - width / 2, w=width, h=width))

        boxes.append(BoundBox(x=101 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=102 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=103 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=104 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=105 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=106 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=107 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=108 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=109 - width / 2, y=109 - width / 2, w=width, h=width))
        boxes.append(BoundBox(x=110 - width / 2, y=109 - width / 2, w=width, h=width))

        fil = Filament(boxes)
        splitted_filaments = cryolo.filament_tracer.split_filament_by_straightness_rec(
            [fil],
            straightness_method=cryolo.filament_tracer._get_straightness,
            straightness_threshold=0.9,
        )

        self.assertEqual(len(splitted_filaments), 2)

    def test_split_filaments_2(self):
        import cryolo.CoordsIO

        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/Myo5a_ELC_Rigor_00105_wrong_splitting.box",
        )
        boxes = cryolo.CoordsIO.read_eman1_boxfile(path)
        filament = Filament()
        filament.boxes = boxes
        segments = cryolo.filament_tracer.split_filament_by_straightness(filament)

        num_boxes = 0
        for seg in segments:
            num_boxes += len(seg.boxes)
        self.assertEqual(75, num_boxes)

    def test_filament_direction(self):
        boxes = []
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512, y=i, w=30, h=30))

        filament = Filament()
        filament.boxes = boxes

        fil_dir = cryolo.filament_tracer.filament_direction(filament)

    def test_replace_boxes_single_line(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(1, len(filaments))
        self.assertTrue(
            is_ordered(y_to_list(filaments[0])), "Filament 0 is not ordered"
        )

    def test_replace_boxes_single_line_shuffeld_length_test(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:750, (512 - 8) : (512 + 8)] = 90

        boxes = []
        width = 30
        for i in range(300, 500, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))
        random.Random(5).shuffle(boxes)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(1, len(filaments), "Only one filament should be detected.")
        self.assertEqual(
            len(filaments[0].boxes),
            len(boxes),
            "Input and out have not the same length.",
        )

    def test_replace_boxes_single_line_shuffeld_num_boxes(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 450, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))
        random.Random(5).shuffle(boxes)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(
            len(filaments[0].boxes),
            len(boxes),
            "Input and out have not the same length.",
        )

    def test_replace_boxes_single_line_shuffeld_ordered(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 450, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))
        random.Random(5).shuffle(boxes)
        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image
        )

        filaments = tracer.trace_filaments()

        for i in range(len(filaments)):
            self.assertTrue(
                is_ordered(y_to_list(filaments[i])),
                "Filament " + str(i) + " is not ordered",
            )

    def test_replace_boxes_two_lines(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:400, 512 - 8 : 512 + 8] = 90
        angle_image[500:750, 512 - 8 : 512 + 8] = 90
        boxes = []
        width = 30
        for index, i in enumerate(range(250, 750, 8)):
            box = BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width)
            print(
                index,
                int(box.x),
                int(box.y),
                angle_image[int(box.y + box.h / 2), int(box.x + box.w / 2)],
            )
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, angle_delta=10
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments))
        self.assertTrue(
            is_ordered(y_to_list(filaments[0])), "Filament 0 is not ordered"
        )
        self.assertTrue(
            is_ordered(y_to_list(filaments[1])), "Filament 1 is not ordered"
        )

    def test_replace_boxes_real_example(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/Actin-ADP-BeFx_0250_60e_DW_downscaled_enhanced.txt",
        )
        angle_image = np.loadtxt(path)
        angle_image = np.flipud(angle_image)

        path = os.path.join(
            os.path.dirname(__file__), "../resources/Actin-ADP-BeFx_0250_60e_DW.box"
        )
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])  # 4096-int(row[1])-box_height
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)
        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=60,
            angle_delta=10,
            rescale_factor=0.25,
            box_distance=5,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments))

    def test_replace_boxes_real_example_2(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/enhanced.txt")
        angle_image = np.loadtxt(path)
        # plt.imshow(angle_image)
        angle_image = np.flipud(angle_image)

        # plt.show()
        path = os.path.join(
            os.path.dirname(__file__), "../resources/Actin-ADP-BeFx_0254_60e_DW.box"
        )
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])  # 4096-int(row[1])-box_height
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=60,
            angle_delta=10,
            rescale_factor=0.25,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments))

    def test_replace_boxes_real_example_3(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/enhanced_3251.txt")
        angle_image = np.loadtxt(path)
        # plt.imshow(angle_image)
        angle_image = np.flipud(angle_image)

        # plt.show()
        path = os.path.join(os.path.dirname(__file__), "../resources/gammaADP-3251.box")
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])  # 4096-int(row[1])-box_height
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=96,
            angle_delta=10,
            rescale_factor=0.25,
        )

        filaments = tracer.trace_filaments()

        print(len(filaments[0].boxes))

        self.assertEqual(1, len(filaments))

    def test_replace_boxes_real_example_6(self):
        # Example contains only one filament. Merging should do the job.
        # However, it failed in the past
        path = os.path.join(os.path.dirname(__file__), "../resources/01.txt")
        angle_image = np.loadtxt(path)
        angle_image = np.flipud(angle_image)
        print("Shape:", angle_image.shape)
        # plt.imshow(angle_image)

        path = os.path.join(os.path.dirname(__file__), "../resources/01.box")
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        xs = []
        ys = []
        rescale_factor = 0.2668
        for row in box_lines:
            xs.append(int((row[0] + row[2] / 2) * rescale_factor))
            ys.append(int((row[1] + row[3] / 2) * rescale_factor))
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        # plt.scatter(xs, ys, s=100, edgecolors="r", facecolors='none')
        # plt.show()
        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=53.361,
            angle_delta=10,
            rescale_factor=rescale_factor,
            box_distance=5,
            rescale_factor_x=0.2760,
            rescale_factor_y=0.2668,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(1, len(filaments))

    def test_distance_perpendicluar_to_box_direction(self):
        box1 = BoundBox(x=5, y=0, w=30, h=30)
        box2 = BoundBox(x=10, y=1, w=30, h=30)

        dist = cryolo.filament_tracer.distance_perpendicluar_to_box_direction(
            ref_box=box1, candiate_box=box2, ref_angle=0
        )

        self.assertAlmostEqual(first=1, second=dist, places=4)

    def test_trace_filaments_real_example_4(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/3200_enhanced.txt")
        angle_image = np.loadtxt(path)
        angle_image = np.flipud(angle_image)
        path = os.path.join(os.path.dirname(__file__), "../resources/gammaADP-3200.box")
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])  # 4096-int(row[1])-box_height
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=256 * 1.5 * 0.25,
            angle_delta=10,
            box_distance=10,
            rescale_factor=0.25,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(1, len(filaments))

    def test_trace_filaments_real_example_5(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/greg_angle_image.txt"
        )
        angle_image = np.loadtxt(path)
        # plt.imshow(angle_image)
        angle_image = np.flipud(angle_image)

        # plt.show()
        path = os.path.join(os.path.dirname(__file__), "../resources/greg_mrc_01.box")
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])  # 4096-int(row[1])-box_height
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=55,
            angle_delta=10,
            rescale_factor=0.2668,
            min_number_boxes=6,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments))

    def test_trace_filaments_real_example_7_pickonefilament(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/Myo5a_ELC_ADP03334_enhanced.txt"
        )
        angle_image = np.loadtxt(path)
        # plt.imshow(angle_image)
        angle_image = np.flipud(angle_image)

        # plt.show()
        path = os.path.join(
            os.path.dirname(__file__), "../resources/Myo5a_ELC_ADP03334.box"
        )
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=68.30,
            angle_delta=10,
            rescale_factor=0.2668,
            rescale_factor_x=0.2760,
            rescale_factor_y=0.2668,
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(1, len(filaments))

    @unittest.skip("Need to rewrite this this")
    def test_trace_filaments_real_example_8_pickonefilament(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/Myo5a_ELC_ADP03719.txt"
        )
        angle_image = np.loadtxt(path)
        # plt.imshow(angle_image)
        angle_image = np.flipud(angle_image)

        # plt.show()
        path = os.path.join(
            os.path.dirname(__file__), "../resources/Myo5a_ELC_ADP03719.box"
        )
        box_lines = np.atleast_2d(np.genfromtxt(path))
        boxes = []
        for row in box_lines:
            box_xmin = int(row[0])
            box_width = int(row[2])
            box_height = int(row[3])
            box_ymin = int(row[1])
            box = BoundBox(x=box_xmin, y=box_ymin, w=box_width, h=box_height)
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes,
            orientation_image=angle_image,
            search_radius=68.30,
            angle_delta=10,
            rescale_factor=0.2668,
            rescale_factor_x=0.2760,
            rescale_factor_y=0.2668,
        )

        filaments = tracer.trace_filaments()
        for f_i, f in enumerate(filaments):
            print("FI:", f_i)
            for b in f.boxes:
                print("x", b.x, "y", b.y)

        import cryolo.utils as utils

        minimum_number_boxes = 6
        box_distance = 26
        resamples_filaments = utils.resample_filaments(filaments, box_distance)

        # Make straight filaments

        resamples_filaments = cryolo.filament_tracer.split_filaments_by_straightness(
            resamples_filaments,
            straightness_method=cryolo.filament_tracer._get_straightness,
            straightness_threshold=0.95,
        )

        # Min number of boxes filter:
        resamples_filaments = cryolo.filament_tracer.filter_filaments_by_num_boxes(
            resamples_filaments, minimum_number_boxes
        )

        for f_i, f in enumerate(resamples_filaments):
            print("F:", f_i)
            for b in f.boxes:
                print("x", b.x, "y", b.y)

        self.assertEqual(1, len(resamples_filaments))

    def test_replace_boxes_two_lines_shuffeld(self):

        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:400, 512 - 8 : 512 + 8] = 90
        angle_image[500:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width))
        random.Random(5).shuffle(boxes)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, angle_delta=10, search_radius=30
        )

        filaments = tracer.trace_filaments()

        self.assertEqual(2, len(filaments), "Containes more elemetns as expected")
        self.assertTrue(
            is_ordered(y_to_list(filaments[0])), "Filament 0 is not ordered"
        )
        self.assertTrue(
            is_ordered(y_to_list(filaments[1])), "Filament 1 is not ordered"
        )

    def test_merge_filaments(self):
        angle_image = np.zeros(shape=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        for i in range(250, 750, 8):
            box = BoundBox(x=512 - width / 2, y=i - width / 2, w=width, h=width)
            # box.info = i
            boxes.append(box)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, search_radius=20, angle_delta=10
        )
        filaments = tracer.trace_filaments()
        print("Fil length:", len(filaments[0].boxes))
        fil_a = Filament()
        fil_a.boxes = filaments[0].boxes[: len(filaments[0].boxes) // 2]
        fil_b = Filament()
        fil_b.boxes = filaments[0].boxes[len(filaments[0].boxes) // 2 :]

        new_filament = tracer.merge_filament(filament_a=fil_a, filament_b=fil_b)

        self.assertIsNotNone(new_filament)

    def test_in_search_region_expected_true(self):

        ref_box = BoundBox(x=1, y=1, w=30, h=30)
        candidate_box = BoundBox(x=2, y=2, w=30, h=30)
        ref_angle = 45
        angle_delta = 10

        result = cryolo.filament_tracer.in_angular_search_region(
            ref_box, candidate_box, ref_angle, angle_delta
        )

        self.assertTrue(result)

    def test_in_search_region_mirrored_expected_true(self):

        ref_box = BoundBox(x=1, y=1, w=30, h=30)
        candidate_box = BoundBox(x=-2, y=-2, w=30, h=30)
        ref_angle = 45
        angle_delta = 10

        result = cryolo.filament_tracer.in_angular_search_region(
            ref_box, candidate_box, ref_angle, angle_delta
        )

        self.assertTrue(result)

    def test_in_search_region_expected_false(self):

        ref_box = BoundBox(x=0, y=1, w=30, h=30)
        candidate_box = BoundBox(x=1, y=0, w=30, h=30)
        ref_angle = 0
        angle_delta = 10

        result = cryolo.filament_tracer.in_angular_search_region(
            ref_box, candidate_box, ref_angle, angle_delta
        )

        self.assertFalse(result)

    def test_merge_filement_manyboxes_to_one(self):
        angle_image = np.random.randint(low=0, high=60 + 1, size=(1024, 1024))
        angle_image[250:750, 512 - 8 : 512 + 8] = 90

        boxes = []
        width = 30
        """
        Generates the coordinates:
        497 339
        497 347
        497 355
        497 363
        497 371
        497 379
        497 387
        497 395
        497 403
        497 411
        497 419
        """
        for i in range(354, 435, 8):
            x = 512 - width / 2
            boxes.append(BoundBox(x=x, y=i - width / 2, w=width, h=width))
        fila = Filament(boxes)

        boxes = []
        boxes.append(BoundBox(x=497, y=427, w=width, h=width))
        filb = Filament(boxes)

        tracer = cryolo.filament_tracer.FilamentTracer(
            boxes, orientation_image=angle_image, search_radius=20, angle_delta=10
        )
        new_filament = tracer.merge_filament(filament_a=fila, filament_b=filb)
        self.assertIsNotNone(new_filament)

    def test_nms_imag72_twofilaments(self):
        import cryolo.CoordsIO as coords

        path = os.path.join(
            os.path.dirname(__file__), "../resources/ActinLifeAct_00072_nms_bug.box"
        )
        filaments = coords.read_eman1_helicon(path)
        filaments_nms = cryolo.filament_tracer.nms_for_filaments(
            filaments, iou_thresh=0.5
        )

        self.assertEqual(len(filaments_nms), 1)

    def test_nms_for_filaments_three_overlapping_2(self):
        width = 10
        boxes = []
        boxes2 = []
        boxes3 = []

        # Generating this:
        #          ----------------------
        # ---------
        #       -------
        # Extepecting:
        #          ----------------------
        # ---------
        for i in range(100, 300, 10):
            boxes.append(BoundBox(x=i, y=50, w=width, h=width))
        for i in range(0, 100, 10):
            boxes2.append(BoundBox(x=i, y=50, w=width, h=width))
        for i in range(70, 150, 10):
            boxes3.append(BoundBox(x=i, y=50, w=width, h=width))

        fila = Filament(boxes)
        filb = Filament(boxes2)
        filc = Filament(boxes3)

        filaments = cryolo.filament_tracer.nms_for_filaments([filc, filb, fila])
        filaments_nms = cryolo.filament_tracer.nms_for_filaments(
            filaments, iou_thresh=0.5
        )

        self.assertEqual(2, len(filaments_nms))

    def test_nms_for_filaments_two_in_three(self):
        """
        Generating two filaments that cross at one box. They should be splitted into 3 filaments
        """
        # nms_for_filaments
        width = 10
        boxes = []
        boxes2 = []
        for i in range(0, 200, 10):
            boxes.append(BoundBox(x=i, y=50, w=width, h=width))
            boxes2.append(BoundBox(x=100, y=i, w=width, h=width))
        fila = Filament(boxes)
        filb = Filament(boxes2)

        filaments = cryolo.filament_tracer.nms_for_filaments([fila, filb])
        len_total = 0
        for fil in filaments:
            len_total += len(fil.boxes)
        """
        Expected result: The two filaments are splitted in into three filaments
        One hsould have length 20, on should have length 5 and one length 14. One overlapping
        box of on filaments (the shorter in general) is deleted.
        """
        self.assertEqual(
            len(filaments),
            3,
            "The number of splitted filaments should be 3 but is "
            + str(len(filaments)),
        )
        self.assertEqual(
            len_total,
            20 + 14 + 5,
            "The total lenght should be 39 but is " + str(len_total),
        )

    def test_nms_for_filaments_complete_overlap(self):
        """
        Generating two filaments that cross at one box. They should be splitted into 3 filaments
        """
        # nms_for_filaments
        width = 10
        boxes = []
        boxes2 = []
        for i in range(0, 200, 10):
            boxes.append(BoundBox(x=i, y=50, w=width, h=width))
        for i in range(0, 100, 10):
            boxes2.append(BoundBox(x=i, y=50, w=width, h=width))
        fila = Filament(boxes)
        filb = Filament(boxes2)

        filaments = cryolo.filament_tracer.nms_for_filaments([fila, filb])

        """
        Expected result: Only one filament with length 20
        """
        self.assertEqual(
            len(filaments),
            1,
            "The number of splitted filaments should be 1 but is "
            + str(len(filaments)),
        )
        self.assertEqual(
            len(filaments[0].boxes),
            20,
            "The total lenght should be 20 but is " + str(len(filaments[0].boxes)),
        )


def x_to_list(filament):
    xlist = []
    for box in filament.boxes:
        xlist.append(box.x)
    return xlist


def y_to_list(filament):
    ylist = []
    for box in filament.boxes:
        ylist.append(box.y)
    return ylist


def is_ordered(alist):
    descending = True
    for i in range(1, len(alist)):
        if alist[i] > alist[i - 1]:
            descending = False
            break
    ascending = True
    for i in range(len(alist) - 1):
        if alist[i] > alist[i + 1]:
            ascending = False
            break
    return descending or ascending


if __name__ == "__main__":
    unittest.main()
