import unittest

import cryolo.utils


class MyTestCase(unittest.TestCase):
    def test_resample_filament_returns_fila(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=1182, y=2116, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=1248, y=1926, w=30, h=30, c=1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 10)
        self.assertTrue(res_fil.boxes is not None, "No boxes")

    def test_resample_filament_correct_length(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=0, y=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=100, y=0, w=30, h=30, c=1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 10)
        self.assertEqual(11, len(res_fil.boxes))

    def test_resample_filament_correct_length_1(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=0, y=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=10, y=0, w=30, h=30, c=1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 20)
        self.assertEqual(1, len(res_fil.boxes))

    def test_resample_filament_correct_length_2(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=0, y=0, z=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=1, y=0, z=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=2, y=0, z=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=3, y=0, z=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=4, y=0, z=0, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=5, y=0, z=1, w=30, h=30, c=1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 1)
        self.assertEqual(6, len(res_fil.boxes))

    def test_resample_filament_correct_maxx(self):

        boxes = []
        boxes.append(cryolo.utils.BoundBox(x=20, y=5, w=30, h=30, c=1, classes=""))
        boxes.append(cryolo.utils.BoundBox(x=85, y=35, w=30, h=30, c=1, classes=""))
        fil = cryolo.utils.Filament(boxes)
        res_fil = cryolo.utils.resample_filament(fil, 6)
        for b in res_fil.boxes:
            print(b.x, b.y)
        self.assertTrue(res_fil.boxes[-1].x <= 85)
        self.assertTrue(res_fil.boxes[0].x >= 20)
        self.assertTrue(res_fil.boxes[-1].y <= 35)
        self.assertTrue(res_fil.boxes[0].y >= 5)

    def test_find_corresponding_paths(self):
        path = "/u/v/w/a/b/c/d/file.mrc"
        list_of_paths = [
            "/u/v/w/a/b/c/e/file.mrc",
            "/u/v/w/a/b/c/d/file.mrc",
            "/u/v/w/a/f/c/d/file.mrc",
        ]
        pth = cryolo.utils.find_corresponding_path(list_of_paths, path)
        self.assertEqual(pth, path)

    def test_overlapping_boxes(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=10, ystart=50, z=3, numbox=10, dy=10)

        fila = cryolo.utils.filament_to_array(fila)
        filb = cryolo.utils.filament_to_array(filb)
        r = cryolo.utils.overlapping_boxes_indicis(fila, filb, 0.3)

        self.assertEquals(len(r), 5)

    def test_non_maxima_suppression3D_average(self):
        # Test to try if averaging is working

        boxa = cryolo.utils.BoundBox(
            x=0, y=0, z=0, w=10, h=10, depth=10, c=1, classes=[1]
        )
        boxa.meta["num_boxes"] = 10
        boxb = cryolo.utils.BoundBox(
            x=1, y=1, z=1, w=10, h=10, depth=10, c=0.9, classes=[1]
        )
        boxb.meta["num_boxes"] = 10
        nms_thresh = 0.3
        obj_thresh = 0.3

        newboxes = cryolo.utils.non_maxima_suppress_fast_3d(
            [boxa, boxb], nms_thresh, obj_thresh
        )

        self.assertTrue(len(newboxes) == 1)
        self.assertTrue(newboxes[0].x == 0.5)
        self.assertTrue(newboxes[0].y == 0.5)
        self.assertTrue(newboxes[0].z == 0.5)

    def test_non_maxima_suppression3D_twoboxes(self):
        # Test to try if averaging is working

        boxa = cryolo.utils.BoundBox(
            x=0, y=0, z=0, w=10, h=10, depth=10, c=1, classes=[1]
        )
        boxa.meta["num_boxes"] = 10
        boxb = cryolo.utils.BoundBox(
            x=0, y=0, z=10, w=10, h=10, depth=10, c=0.9, classes=[1]
        )
        boxb.meta["num_boxes"] = 10
        nms_thresh = 0.3
        obj_thresh = 0.3

        newboxes = cryolo.utils.non_maxima_suppress_fast_3d(
            [boxa, boxb], nms_thresh, obj_thresh
        )

        self.assertTrue(len(newboxes) == 2)

    def test_merging_3D_filaments_1(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=5, ystart=0, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0.3

        newfils = cryolo.utils.merge_filaments_3d(
            [filb, fila], nms_thresh, obj_thresh, window_radius=1, box_distance=5
        )

        self.assertTrue(len(newfils) == 1, "Number of fils should be 1 but is" + str(len(newfils)))

    def test_get_closest_point(self):
        def create_filament(flength, ystart, z, numbox, dy=1, x=0, dz=0):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=x, y=ystart + i * dy, z=z +i*dz, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=10, ystart=0, z=5, numbox=10, dy=10, dz=0.5)

        fildat_a = cryolo.utils.filament_to_array(fila)
        fildat_b = cryolo.utils.filament_to_array(filb)
        distance = cryolo.utils.get_closest_point_distance(fildat_a[:,:3],fildat_b[:,:3])
        print(distance)
        self.assertEqual(5,distance)



    def test_merging_3D_filaments_only_one(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0.3

        newfils = cryolo.utils.merge_filaments_3d(
            [fila], nms_thresh, obj_thresh, window_radius=1, box_distance=5
        )

        self.assertTrue(len(newfils) == 1, "Number of fils should be 1 but is" + str(len(newfils)))

    def test_merging_3D_filaments_many_for_timing(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)
        fils = []
        import numpy as np
        np.random.seed(100)
        nfilas = 500
        for i in range(nfilas):
            z = np.random.randint(0,300)
            fils.append(create_filament(flength=10, ystart=0, z=z, numbox=10, dy=10))

        nms_thresh = 0.3
        obj_thresh = 0.3

        newfils = cryolo.utils.merge_filaments_3d(
            fils, nms_thresh, obj_thresh, window_radius=1, box_distance=5
        )

        self.assertTrue(True)


    def test_merging_3D_filaments_partial(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 2 filaments with partial merging.
        # * * * * * * * * * *
        #           * * * * *
        #           * * * * * * * * * *
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=5, ystart=0, z=0, numbox=10, dy=10)
        filc = create_filament(flength=10, ystart=50, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filb, fila, filc], nms_thresh, obj_thresh, window_radius=1, box_distance=10, partial=True
        )
        for f in newfils:
            print("Filament")
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 2, "Laenge " + str(len(newfils)))

    def test_merging_3D_filaments_partial2(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 2 filaments of length 10
        # * * * * * * * * * * L10
        #           * * * * * * * * * L9
        #                     * * * * * * * * * * L10
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=9, ystart=50, z=2, numbox=10, dy=10)
        filc = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)

        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filb, fila, filc], nms_thresh, obj_thresh, window_radius=1, box_distance=10,
            partial=True
        )

        self.assertTrue(len(newfils) == 2, "Laenge " + str(len(newfils)))

    def test_merging_3D_filaments_partial3(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 2 filaments of length 10
        # * * * * * * * * * * L10
        #           * * * * * * * * * L9
        #                     * * * * * * * * * * L10
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=10)
        filb = create_filament(flength=9, ystart=50, z=2, numbox=10, dy=10)
        filc = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        fild = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        file = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filb, fila, filc, fild, file], nms_thresh, obj_thresh, window_radius=1, box_distance=10,
            partial=True
        )
        for f in newfils:
            print("Fialment")
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 2, "Laenge " + str(len(newfils)))

    def test_merging_3D_filaments_partial4(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 1 filament if m
        # * * * * * * * * * *           L10
        # * * * * * * * * * *           L10
        #         * * * * * * * * * *   L10
        filc = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        fild = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        file = create_filament(flength=10, ystart=140, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filc, fild, file], nms_thresh, obj_thresh, window_radius=1, box_distance=10,
            partial=True
        )
        sum_length = 0 # should be 10 + 4
        for f in newfils:
            print("Fialment")
            sum_length += len(f.boxes)
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 2, f"Number of filament should be 2 but is {len(newfils)} ")
        self.assertTrue(sum_length == 14, f"Sum should be 12 but is {sum_length}")

    def test_merging_3D_filaments_partial5(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 1 filament if m
        # * * * * * * * * *           L9
        #         * * * * * * * * * *           L10
        #                 * * * * * * * * *    L9
        filc = create_filament(flength=9, ystart=100, z=2, numbox=10, dy=10)
        fild = create_filament(flength=10, ystart=140, z=2, numbox=10, dy=10)
        file = create_filament(flength=9, ystart=180, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filc, fild, file], nms_thresh, obj_thresh, window_radius=1, box_distance=10,
            partial=True
        )
        sum_length = 0 # should be 10 + 4
        print("Test result:")
        for f in newfils:
            print(f"Fialment {len(f.boxes)}" )
            sum_length += len(f.boxes)
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 3, f"Number of filament should be 2 but is {len(newfils)} ")
        self.assertTrue(sum_length == (4+10+3), f"Sum should be {4+10+3} but is {sum_length}")

    def test_merging_3D_filaments_nonpartial5(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        # Filaments are generated in that way. I expect 1 filament if m
        # * * * * * * * * *           L9
        #         * * * * * * * * * *           L10
        #                 * * * * * * * * *    L9
        filc = create_filament(flength=9, ystart=100, z=2, numbox=10, dy=10)
        fild = create_filament(flength=10, ystart=140, z=2, numbox=10, dy=10)
        file = create_filament(flength=9, ystart=180, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [filc, fild, file], nms_thresh, obj_thresh, window_radius=1, box_distance=10,
            partial=False
        )
        sum_length = 0  # should be 10 + 4
        print("Test result:")
        for f in newfils:
            print(f"Fialment {len(f.boxes)}")
            sum_length += len(f.boxes)
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 1, f"Number of filament should be 1 but is {len(newfils)} ")
        self.assertTrue(sum_length == 17,
                        f"Sum should be {17} but is {sum_length}")

    def test_merging_3D_filaments_nonpartial4(self):
        def create_filament(flength, ystart, z, numbox, dy=1):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0, y=ystart + i * dy, z=z, w=10, h=10, depth=10, c=1, classes=[1]
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        fila = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        filc = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        fild = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        file = create_filament(flength=10, ystart=100, z=2, numbox=10, dy=10)
        nms_thresh = 0.3
        obj_thresh = 0

        newfils = cryolo.utils.merge_filaments_3d(
            [fila, filc, fild, file], nms_thresh, obj_thresh, window_radius=1,
            box_distance=10,
            partial=False
        )
        for f in newfils:
            print("Fialment")
            for b in f.boxes:
                print(b.y)
        self.assertTrue(len(newfils) == 1, "Laenge " + str(len(newfils)))

    def test_get_consecutive_subarrays(self):
        # 0 1 2 3 4 5 6 7 8 9 10 11
        # * * o o o * * o o o * *
        import numpy as np
        overlap = np.array([2,3,4,7,8,9])
        splt = cryolo.utils.get_consecutive_subarrays(overlap)
        np.testing.assert_array_equal(splt[0], np.array([2, 3, 4]))
        np.testing.assert_array_equal(splt[1], np.array([7, 8, 9]))

    def test_merging_3D_filaments_length_Correct(self):
        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                print(i, box.x, box.y)
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 2
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=dy, bsize=3)
        filb = create_filament(
            flength=10, ystart=5 * dy, z=1, numbox=10, dy=dy, bsize=3
        )

        merged = cryolo.utils.merge_filaments_3d(
            [fila, filb],
            iou_threshold=0.3,
            merge_threshold=0.4,
            window_radius=dy,
            box_distance=dy,
        )

        self.assertEqual(1, len(merged))
        self.assertEqual(15, len(merged[0].boxes))

    def test_resampling_filament_noeffect(self):
        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                print(i, box.x, box.y)
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 2
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=dy, bsize=3)
        rfila = cryolo.utils.resample_filament(fila, dy)
        self.assertEqual(len(fila.boxes), len(rfila.boxes))

    def test_merging_3D_filaments_2(self):
        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 2
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=dy, bsize=3)
        filb = create_filament(
            flength=10, ystart=5 * dy, z=1, numbox=10, dy=dy, bsize=3
        )

        merged = cryolo.utils.merge_filaments_3d(
            [fila, filb],
            iou_threshold=0.3,
            merge_threshold=0.4,
            window_radius=3 * dy,
            box_distance=dy,
        )

        self.assertEqual(1, len(merged))

    def test_iou_boxes_shifted(self):
        import numpy as np

        box1 = cryolo.utils.BoundBox(x=100, y=100, w=50, h=50, c=1, classes=[1])
        box2 = cryolo.utils.BoundBox(x=100 + 25, y=100, w=50, h=50, c=1, classes=[1])
        iou = cryolo.utils.bbox_iou(box1, box2)
        self.assertEqual(iou, 1.0 / 3.0)

    def test_iou_boxes_same(self):
        box1 = cryolo.utils.BoundBox(x=100, y=100, w=50, h=50, c=1, classes=[1])
        box2 = cryolo.utils.BoundBox(x=100, y=100, w=50, h=50, c=1, classes=[1])
        iou = cryolo.utils.bbox_iou(box1, box2)
        self.assertEqual(iou, 1.0)

    def test_merging_3D_filaments_3(self):
        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 2
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=dy, bsize=5)
        filb = create_filament(
            flength=10, ystart=5 * dy, z=1, numbox=10, dy=dy, bsize=5
        )
        filc = create_filament(flength=1, ystart=0, z=2, numbox=10, dy=dy, bsize=5)

        merged = cryolo.utils.merge_filaments_3d(
            [fila, filb, filc],
            iou_threshold=0.3,
            merge_threshold=0.4,
            window_radius=dy,
            box_distance=dy,
        )

        self.assertEqual(1, len(merged))
        self.assertEqual(15, len(merged[0].boxes))

    def test_merging_3D_filaments_posweight(self):
        def printfil(fil):
            for box in fil.boxes:
                print(box.x, box.y, box.z, box.c)

        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 5
        fila = create_filament(flength=10, ystart=0, z=0, numbox=2, dy=dy, bsize=6)
        filb = create_filament(flength=10, ystart=0, z=3, numbox=8, dy=dy, bsize=6)

        merged = cryolo.utils.merge_filaments_3d(
            [fila, filb],
            iou_threshold=0.3,
            merge_threshold=0.4,
            window_radius=3 * dy,
            box_distance=dy,
        )

        self.assertEqual(10, merged[0].boxes[0].meta["num_boxes"])
        self.assertEqual(2.4, merged[0].boxes[0].z)

    def test_merging_3D_filaments_partialmerge(self):
        def printfil(fil):
            for box in fil.boxes:
                print(box.x, box.y, box.z)

        def create_filament(flength, ystart, z, numbox, dy=1, bsize=10):
            fboxes = []
            for i in range(flength):
                box = cryolo.utils.BoundBox(
                    x=0,
                    y=ystart + i * dy,
                    z=z,
                    w=bsize,
                    h=bsize,
                    depth=bsize,
                    c=1,
                    classes=[1],
                )
                box.meta["num_boxes"] = numbox
                fboxes.append(box)
            return cryolo.utils.Filament(fboxes)

        dy = 2
        fila = create_filament(flength=10, ystart=0, z=0, numbox=10, dy=dy, bsize=3)
        filb = create_filament(
            flength=20, ystart=5 * dy, z=1, numbox=10, dy=dy, bsize=3
        )

        merged = cryolo.utils.merge_filaments_3d(
            [fila, filb],
            iou_threshold=0.3,
            merge_threshold=0,
            window_radius=dy,
            box_distance=dy,
            partial=True,
        )

        import numpy as np

        print("Found:", len(merged), len(merged[0].boxes), len(merged[1].boxes))
        printfil(merged[0])
        print(" ")
        printfil(merged[1])
        sorted = np.sort([len(merged[0].boxes), len(merged[1].boxes)])
        self.assertEqual(20, sorted[1])
        self.assertEqual(5, sorted[0])


if __name__ == "__main__":
    unittest.main()
