import unittest
import cryolo
import cryolo.CoordsIO
import cryolo.grouping3d
import os
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_tracing_filament_3(self):

        from cryolo import utils
        from cryolo import grouping3d

        def generate_fil(length, offset=0):
            boxes = []

            for x in np.arange(offset, offset + length):
                box = utils.BoundBox(x=x, y=x, w=5, h=5, c=1)
                boxes.append(box)

            return utils.Filament(boxes)

        input_dict = {}
        input_dict[1] = [generate_fil(10, 0.5)]
        input_dict[2] = [generate_fil(10, 0.5)]

        filaments = grouping3d.do_tracing_filaments(
            input_dict,
            search_range=1,
            memory=2,
            min_edge_weight=0.3,
            window_size=2,
            resample_dist=1,
            merge_threshold=0.8,
        )

        self.assertEqual(1, len(filaments))

    def test_tracing_filament(self):
        """
        In this unit test I will generate the following filament pattern. Each row is a slice.
        - means filament position, x means no filament positions, - divided by x are seperate filaments.
        The result of the tracing should be 2 filaments.

        0123456789
        ----xx----
        ----------
        ----xx----
        xxxxxxxxx----xx----
        xxxxxxxxx----------
        xxxxxxxxx----xx----
        """
        from cryolo import utils
        from cryolo import grouping3d

        def generate_fil(length, offset=0):
            boxes = []
            for x in range(offset, offset + length):

                box = utils.BoundBox(x=x, y=0, w=5, h=5, c=1)
                boxes.append(box)

            return utils.Filament(boxes)

        input_dict = {}
        input_dict[1] = [generate_fil(4, 0), generate_fil(4, 6)]  # - - - - x x - - - -
        input_dict[2] = [generate_fil(10, 0)]
        input_dict[3] = [generate_fil(4, 0), generate_fil(4, 6)]
        input_dict[4] = [generate_fil(4, 9), generate_fil(4, 9 + 6)]
        input_dict[5] = [generate_fil(10, 9)]
        input_dict[6] = [generate_fil(4, 9), generate_fil(4, 9 + 6)]

        filaments = grouping3d.do_tracing_filaments(
            input_dict,
            search_range=1,
            memory=2,
            min_edge_weight=0.3,
            window_size=2,
            resample_dist=1,
            merge_threshold=0.8,
        )
        self.assertEqual(2, len(filaments))

    def test_tracing_filament_single_2(self):
        from cryolo import utils
        from cryolo import grouping3d

        def generate_fil(length, offset=0, c=1):
            boxes = []
            for x in range(offset, offset + length):
                box = utils.BoundBox(x=1.5, y=x, w=5, h=5, c=c)
                boxes.append(box)

            return utils.Filament(boxes)

        input_dict = {}
        input_dict[0] = [generate_fil(30, 5, 0.5)]
        input_dict[2] = [generate_fil(30, 0, 1)]

        filaments = grouping3d.do_tracing_filaments(
            input_dict,
            search_range=1,
            memory=0,
            min_edge_weight=0.3,
            window_size=1,
            resample_dist=1,
            merge_threshold=0.8,
        )
        print("Len:", len(filaments[0].boxes))
        for box in filaments[0].boxes:
            print(box.x, box.y, box.z)

        self.assertEqual(1, len(filaments))

    def test_tracing_filament_single(self):

        from cryolo import utils
        from cryolo import grouping3d

        def generate_fil(length, offset=0):
            boxes = []
            for x in range(offset, offset + length):
                box = utils.BoundBox(x=x, y=0, w=5, h=5, c=1)
                boxes.append(box)

            return utils.Filament(boxes)

        input_dict = {}
        input_dict[0] = [generate_fil(10, 0)]
        input_dict[2] = [generate_fil(5, 0)]

        filaments = grouping3d.do_tracing_filaments(
            input_dict,
            search_range=1,
            memory=0,
            min_edge_weight=0.3,
            window_size=2,
            resample_dist=1,
            merge_threshold=0.8,
        )
        for box in filaments[0].boxes:
            print(box.x, box.y, box.z)

        self.assertEqual(1, len(filaments))

    def test_filament_to_group3D_diag_1fil(self):
        import pandas as pd
        from cryolo import grouping3d

        path = os.path.join(
            os.path.dirname(__file__), "../resources/dataframe_diagonal_filament.csv"
        )
        df = pd.read_csv(path)
        fil3d = grouping3d.filaments_group_to_3D(df, window_size=90, box_distance=13)

        self.assertTrue(fil3d is not None, "Filament is none...")

    def test_tracing_filament_2(self):
        path = os.path.join(
            os.path.dirname(__file__), "../resources/filaments_untraced.cbox"
        )
        filaments = cryolo.CoordsIO.read_cbox_boxfile(path)

        input_dict = {}

        for fil in filaments:
            if int(fil.boxes[0].z) not in input_dict:
                input_dict[int(fil.boxes[0].z)] = [fil]
            else:
                input_dict[int(fil.boxes[0].z)].append(fil)
        from cryolo import grouping3d

        filaments_traced = grouping3d.do_tracing_filaments(
            input_dict,
            search_range=33.086 / 2,
            memory=2,
            min_edge_weight=0.0,
            window_size=33,
            min_length_filament=1,
            resample_dist=10,
        )

        self.assertEqual(3, len(filaments_traced))


if __name__ == "__main__":
    unittest.main()
