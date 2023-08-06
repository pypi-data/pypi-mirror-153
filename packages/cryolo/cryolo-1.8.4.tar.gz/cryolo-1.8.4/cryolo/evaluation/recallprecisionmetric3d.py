from .metric import Metric
from typing import Dict
import numpy as np
from cryolo.utils import bbox_iou_vec_3d
import tqdm

class RecallPrecisionMetric3D(Metric):

    def __init__(self, iou_thresh : float = 0.6):
        self.iou_thresh = iou_thresh

    def eval(self, boxes : np.array, boxesgt : np.array) -> Dict[str,float]:
        """
        :param boxes: Nx6 array with N boxes. The columns are x,y,z,width,height,depth. Can be none if not boxes were measured.
        :param boxesgt: Mx6 array with M boxes. The columns are x,y,z,width,height,depth. Can be non if no GT boxes are available.
        :return: Dictonary with Recall and Precision
        """

        if boxesgt is None or boxes is None:
            return {"recall" : 0, "precision" : 0}

        true_positive = 0
        num_gt_boxes = boxesgt.shape[0]
        num_measured = boxes.shape[0]
        for row in tqdm.tqdm(boxes,desc="Calculate recall and precision"):
            boxMatrix = np.array([row] * num_gt_boxes)
            ious = bbox_iou_vec_3d(boxMatrix, boxesgt)
            true_positive += np.any(ious > self.iou_thresh)

        false_negative = num_gt_boxes - true_positive
        false_positive = num_measured - true_positive

        recall = true_positive/(true_positive + false_negative)
        precision = true_positive/(true_positive + false_positive)
        result = {"recall" : recall, "precision" : precision}

        return result