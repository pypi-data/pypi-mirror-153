import unittest
import cryolo.CoordsIO
import os
from cryolo.utils import Filament, BoundBox


class CoordsIOTest(unittest.TestCase):
    def test_read_eman1_boxfile_lencorrect(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/gammaADP-3200.box")
        boxes = cryolo.CoordsIO.read_eman1_boxfile(path)
        self.assertEqual(len(boxes), 21)

    def test_read_eman1_boxfile_last_box_correct(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/gammaADP-3200.box")
        boxes = cryolo.CoordsIO.read_eman1_boxfile(path)

        self.assertEqual(boxes[len(boxes) - 1].x, 2177)
        self.assertEqual(boxes[len(boxes) - 1].y, 300)
        self.assertEqual(boxes[len(boxes) - 1].w, 256)
        self.assertEqual(boxes[len(boxes) - 1].h, 256)

    def test_write_eman1_boxfile(self):
        box_written = []
        for i in range(250, 750, 8):
            box_written.append(BoundBox(x=512, y=i, w=30, h=30))

        path = os.path.join(
            os.path.dirname(__file__), "../resources/test_write_eman1_boxfile.box"
        )

        cryolo.CoordsIO.write_eman1_boxfile(boxes=box_written, path=path)

        box_read = cryolo.CoordsIO.read_eman1_boxfile(path)

        for i, box in enumerate(box_written):
            self.assertEqual(box.x, box_read[i].x)
            self.assertEqual(box.y, box_read[i].y)
            self.assertEqual(box.w, box_read[i].w)
            self.assertEqual(box.h, box_read[i].h)

    def test_read_eman1_helicon_file3_onlyonefilament(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/actin_cAla_1_corrfull_ptcl_coord_onlyone.txt",
        )
        filaments = cryolo.CoordsIO.read_eman1_helicon(path)
        print("NUM", len(filaments[0].boxes))
        self.assertEqual(1, len(filaments))

    def test_read_eman1_helicon_file3_onlyonefilament_numboxes(self):
        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/actin_cAla_1_corrfull_ptcl_coord_onlyone.txt",
        )
        filaments = cryolo.CoordsIO.read_eman1_helicon(path)
        self.assertEqual(14, len(filaments[0].boxes))

    def test_read_eman1_helicon_file1(self):

        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/actin_cAla_1_corrfull_ptcl_coord.txt",
        )
        filaments = cryolo.CoordsIO.read_eman1_helicon(path)
        self.assertEqual(4, len(filaments))

    def test_read_eman1_helicon_file2(self):

        path = os.path.join(
            os.path.dirname(__file__), "../resources/Actin-ADP-BeFx_0001.box"
        )
        filaments = cryolo.CoordsIO.read_eman1_helicon(path)
        self.assertEqual(23, len(filaments))

    def test_write_eman1_helicon_file1(self):
        boxes = []
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512, y=i, w=30, h=30))

        filaments = [Filament(boxes)]

        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/test_write_eman1_heliction_file1.box",
        )
        cryolo.CoordsIO.write_eman1_helicon(filaments, path, image_filename="test.mrc")

        filaments_read = cryolo.CoordsIO.read_eman1_helicon(path)

        box_written = filaments[0].boxes
        box_read = filaments_read[0].boxes
        self.assertEqual(len(box_written), len(box_read))
        for i, box in enumerate(box_written):
            print(box.x, box_read[i].x, box.y, box_read[i].y)

        for i, box in enumerate(box_written):
            print(box.x, box_read[i].x)
            self.assertEqual(box.x, box_read[i].x)
            self.assertEqual(box.y, box_read[i].y)
            self.assertEqual(box.w, box_read[i].w)
            self.assertEqual(box.h, box_read[i].h)

    def test_read_eman1_filament_start_end_len_file1(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/Myo5ADP_0682.txt")
        filaments = cryolo.CoordsIO.read_eman1_filament_start_end(path)
        self.assertEqual(6, len(filaments))

    def test_write_eman1_filament_start_end_len_correct(self):
        boxes = []
        for i in range(250, 750, 8):
            boxes.append(BoundBox(x=512, y=i, w=30, h=30))

        filaments_written = [Filament(boxes)]

        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/test_write_eman1_filament_start_end.box",
        )
        cryolo.CoordsIO.write_eman1_filament_start_end(
            filaments=filaments_written, path=path
        )

        filaments_read = cryolo.CoordsIO.read_eman1_filament_start_end(path)
        self.assertEqual(len(filaments_written), len(filaments_read))

    def test_write_eman1_filament_start_end_box_correct(self):
        box_written = []
        for i in range(250, 750, 8):
            box_written.append(BoundBox(x=512, y=i, w=30, h=30))

        filaments_written = [Filament(box_written)]

        path = os.path.join(
            os.path.dirname(__file__),
            "../resources/test_write_eman1_filament_start_end.box",
        )
        cryolo.CoordsIO.write_eman1_filament_start_end(
            filaments=filaments_written, path=path
        )

        filaments_read = cryolo.CoordsIO.read_eman1_filament_start_end(path)

        box_read = filaments_read[0].boxes

        self.assertEqual(box_read[0].x, box_written[0].x)
        self.assertEqual(box_read[0].y, box_written[0].y)
        self.assertEqual(box_read[0].w, box_written[0].w)
        self.assertEqual(box_read[0].h, box_written[0].h)

        self.assertEqual(
            box_read[len(box_read) - 1].x, box_written[len(box_written) - 1].x
        )
        self.assertEqual(
            box_read[len(box_read) - 1].y, box_written[len(box_written) - 1].y
        )
        self.assertEqual(
            box_read[len(box_read) - 1].w, box_written[len(box_written) - 1].w
        )
        self.assertEqual(
            box_read[len(box_read) - 1].h, box_written[len(box_written) - 1].h
        )

    def test_read_star_file_num_boxes(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/TcdA1-0001_frames_sum.star"
        )
        boxes = cryolo.CoordsIO.read_star_file(path, 220)
        self.assertEqual(len(boxes), 128)

    def test_read_star_file_num_boxes_file2(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/nompc.star")
        boxes = cryolo.CoordsIO.read_star_file(path, 220)
        self.assertEqual(len(boxes), 120)

    def test_read_star_file_first_box_correct(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/TcdA1-0001_frames_sum.star"
        )
        boxes = cryolo.CoordsIO.read_star_file(path, 220)
        self.assertEqual(boxes[0].x + boxes[0].w / 2, 2302.0)
        self.assertEqual(boxes[0].y + boxes[0].h / 2, 4028.0)
        self.assertEqual(boxes[0].w, 220)
        self.assertEqual(boxes[0].h, 220)

    def test_read_star_file_last_box_correct(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/TcdA1-0001_frames_sum.star"
        )
        boxes = cryolo.CoordsIO.read_star_file(path, 220)
        self.assertEqual(boxes[len(boxes) - 1].x + boxes[len(boxes) - 1].w / 2, 2602.5)
        self.assertEqual(boxes[len(boxes) - 1].y + boxes[len(boxes) - 1].w / 2, 90.5)
        self.assertEqual(boxes[len(boxes) - 1].w, 220)
        self.assertEqual(boxes[len(boxes) - 1].h, 220)

    def test_write_star_file(self):
        box_written = []
        for i in range(250, 750, 8):
            box_written.append(BoundBox(x=512, y=i, w=30, h=30))
        path = os.path.join(
            os.path.dirname(__file__), "../resources/test_write_star_file.star"
        )
        cryolo.CoordsIO.write_star_file(path, box_written)
        box_read = cryolo.CoordsIO.read_star_file(path, 30)

        for i, box in enumerate(box_written):
            self.assertEqual(box.x, box_read[i].x)
            self.assertEqual(box.y, box_read[i].y)
            self.assertEqual(box.w, box_read[i].w)
            self.assertEqual(box.h, box_read[i].h)

    def test_read_star_filament_file_checklen(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/actin_cAla_1.star")
        boxwidth = 100
        filaments = cryolo.CoordsIO.read_star_filament_file(
            path=path, box_width=boxwidth
        )

        self.assertEqual(len(filaments), 4)

    def test_read_star_filament_file_checkfirst(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/actin_cAla_1.star")
        boxwidth = 100
        filaments = cryolo.CoordsIO.read_star_filament_file(
            path=path, box_width=boxwidth
        )
        boxes = filaments[0].boxes
        self.assertEqual(boxes[0].x + boxes[0].w / 2, 3597.0)
        self.assertEqual(boxes[0].y + boxes[0].h / 2, 2470.0)
        self.assertEqual(boxes[0].w, boxwidth)
        self.assertEqual(boxes[0].h, boxwidth)

        self.assertEqual(boxes[len(boxes) - 1].x + boxes[len(boxes) - 1].w / 2, 3110.0)
        self.assertEqual(boxes[len(boxes) - 1].y + boxes[len(boxes) - 1].h / 2, 3091.0)
        self.assertEqual(boxes[len(boxes) - 1].w, boxwidth)
        self.assertEqual(boxes[len(boxes) - 1].h, boxwidth)

    def test_is_star_filament_file_singleparticle(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/nompc.star")
        is_star_filament = cryolo.CoordsIO.is_star_filament_file(path)
        self.assertTrue(is_star_filament)

    def test_is_star_filament_file_singleparticle_file2(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/normal_boxfile.box"
        )
        is_star_filament = cryolo.CoordsIO.is_star_filament_file(path)
        self.assertFalse(is_star_filament)

    def test_is_star_filament_file_filament(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/actin_cAla_1.star")
        is_star_filament = cryolo.CoordsIO.is_star_filament_file(path)
        self.assertTrue(is_star_filament)

    def test_write_coords(self):
        path = os.path.join(os.path.dirname(__file__), "../resources/test.coords")
        a = cryolo.utils.BoundBox(x=0, y=0, z=0, w=5, h=5, depth=5)
        b = cryolo.utils.BoundBox(x=0, y=0, z=0, w=5, h=5, depth=5)
        boxes = [a, b]
        cryolo.CoordsIO.write_coords_file(path, boxes)
        # os.remove()
