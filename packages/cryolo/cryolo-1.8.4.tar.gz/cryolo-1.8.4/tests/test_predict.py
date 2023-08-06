import unittest
import os
import cryolo.predict
import cryolo.utils


class MyTestCase(unittest.TestCase):

    #
    # To Do:
    #  - Add prediction test for filaments
    #  - Replace the weights with compressed weights

    def test_run_prediction(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        config_path = os.path.join(
            os.path.dirname(__file__), "../resources/config_model_toxin.json"
        )
        weights_path = os.path.join(
            os.path.dirname(__file__), "../resources/cryolo_model_toxin.h5"
        )
        input_path = [
            os.path.join(
                os.path.dirname(__file__), "../resources/TcdA1-0155_frames_sum.mrc"
            )
        ]
        res, _ = cryolo.predict.do_prediction(
            config_path=config_path,
            weights_path=weights_path,
            input_path=input_path,
            num_patches=1,
        )
        self.assertEqual(
            157,
            len(res[0]["boxes"][0]),
            "crYOLO did not picked the expected number of particles",
        )

    def test_find_not_fully_immersed_particles(self):
        boxes = []
        boxes.append(cryolo.utils.BoundBox(512, 512, 50, 50))  # Fully immersed
        boxes.append(cryolo.utils.BoundBox(-5, -5, 50, 50))  # Not Fully immersed
        boxes.append(cryolo.utils.BoundBox(0, 0, 50, 50))  # Fully immersed
        boxes.append(
            cryolo.utils.BoundBox(1023 - 50, 1023 - 50, 50, 50)
        )  # Fully immersed
        boxes.append(cryolo.utils.BoundBox(1010, 1010, 50, 50))  # Not Fully immersed
        indices = cryolo.predict.get_not_fully_immersed_box_indices(boxes, 1024, 1024)
        print(indices)
        self.assertEqual(len(indices), 2, "Removed more than necessary")
        self.assertEqual(indices[0], 1, "Removed wrong box")
        self.assertEqual(indices[1], 4, "Removed wrong box")
