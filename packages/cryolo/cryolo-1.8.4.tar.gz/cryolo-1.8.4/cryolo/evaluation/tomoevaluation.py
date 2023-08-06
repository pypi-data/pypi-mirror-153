from .metric import Metric

from dataclasses import dataclass
from .boxdataprovider import BoxDataProvider, ImageBoxData
from .pathsboxdataprovider import PathsDataProvider
from cryolo.evaluation.pathsfilamentprovider import PathsFilamentProvider
from .recallprecisionmetric3d import RecallPrecisionMetric3D
from cryolo import CoordsIO
from typing import List, Callable, Tuple

import argparse
import numpy as np
import os
import glob


@dataclass
class EvaluationResult:
    metric : str
    value : float
    number_datapoints : int
    dataset : str
    threshold : float = None

from cryolo.evaluation.resultsview import SimpleView, ResultsView

def make_imageboxdata_pairs(
    seta: List[ImageBoxData],
    setb: List[ImageBoxData],
    identifier_matching_method: Callable[[str, str], bool],
) -> List[Tuple[ImageBoxData, ImageBoxData]]:
    pairs = []
    index_a_found = []
    index_b_found = []
    for index_a, boxdataA in enumerate(seta):
        for index_b, boxdataB in enumerate(setb):

            if identifier_matching_method(boxdataA.indentifer, boxdataB.indentifer):
                if index_a not in index_a_found and index_b not in index_b_found:

                    pairs.append((boxdataA, boxdataB))
                    index_a_found.append(index_a)
                    index_b_found.append(index_b)

    for index_a, boxdataA in enumerate(seta):
        if index_a not in index_a_found:
            pairs.append((boxdataA, ImageBoxData(None,None)))
    for index_b, boxdataB in enumerate(setb):
        if index_b not in index_b_found:
            pairs.append((ImageBoxData(None,None), boxdataB))

    return pairs


def group_evaluation_results(results : List[EvaluationResult]) -> List[EvaluationResult]:
    groups = set([e.dataset for e in results])
    group_result = []
    for group in groups:
        results_same_group = [e for e in results if e.dataset == group]
        metrics = set([e.metric for e in results_same_group])
        for metric in metrics:
            values = [e.value for e in results_same_group if e.metric == metric]
            res = EvaluationResult(
                metric=metric,
                value=np.mean(values),
                number_datapoints=len(values),
                dataset=group
            )
            group_result.append(res)

    return group_result

def evaluate(
    gtProvider: BoxDataProvider,
    measuredProvider: BoxDataProvider,
    metrics: List[Metric],
    identifier_matching_method=BoxDataProvider.path_matching_filename_eq,
) -> List[EvaluationResult]:
    """
    :return: Dictionary of averages and dictionary of number of datapoints.
    """

    imageboxdataGT = gtProvider.get_boxes()
    imageboxdataM = measuredProvider.get_boxes()

    pairs = make_imageboxdata_pairs(imageboxdataGT, imageboxdataM, identifier_matching_method=identifier_matching_method)

    # Calculate all evaluation results
    eval_results = []
    for gtData, mData in pairs:
        for metric in metrics:
            evaluation_result = metric.eval(mData.data, gtData.data)
            for metricResult in evaluation_result:
                eres = EvaluationResult(metric=metricResult,
                                 value=evaluation_result[metricResult],
                                 dataset=mData.group,
                                 number_datapoints=1) # 1 because it is only one image.
                eval_results.append(eres)

    return group_evaluation_results(eval_results)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluation script for Tomography")

    parser.add_argument(
        "-gtb",
        "--groundtruth",
        type=str,
        required=True,
        help="Path box files with ground truth box files",
    )

    parser.add_argument(
        "-pb",
        "--predicted",
        type=str,
        required=True,
        help="Path box files with ground truth cbox files",
    )

    parser.add_argument(
        "--filament",
        action="store_true",
        help="Use this flag if your data is filament data",
    )

    parser.add_argument(
        "-bd",
        "--boxdistance",
        type=int,
        help="(FIlAMENTS ONLY) Box distance when resampling should be used.",
    )

    return parser


def run(args : List[str], metrics : List[Metric], view : ResultsView) -> List[EvaluationResult]:

    # Get path path to ground truth boxes and measured boxes
    mask_gt = "*.cbox"
    path_gt = args.groundtruth

    mask_measured = "*.cbox"
    path_measured = args.predicted

    is_filament = args.filament
    filament_box_distance = args.boxdistance

    # Get relevant files
    measured_boxfile_paths = glob.glob(os.path.join(path_measured, mask_measured))
    gt_boxfile_paths = glob.glob(os.path.join(path_gt, mask_gt))

    # Find file pairs
    if is_filament:
        mProvider = PathsFilamentProvider(
            paths=measured_boxfile_paths,
            reading_method=CoordsIO.read_cbox_boxfile,
            group_method=BoxDataProvider.group_method_lastfolder,
            resampling_distance=filament_box_distance,
        )

        gtProvider = PathsFilamentProvider(
            paths=gt_boxfile_paths,
            reading_method=CoordsIO.read_cbox_boxfile,
            group_method=BoxDataProvider.group_method_lastfolder,
            resampling_distance=filament_box_distance,
        )
    else:
        mProvider = PathsDataProvider(
            paths=measured_boxfile_paths,
            reading_method=CoordsIO.read_cbox_boxfile,
            group_method=BoxDataProvider.group_method_lastfolder,
        )

        gtProvider = PathsDataProvider(
            paths=gt_boxfile_paths,
            reading_method=CoordsIO.read_cbox_boxfile,
            group_method=BoxDataProvider.group_method_lastfolder,
        )


    # Evaluate all metric on the box pairs
    results = evaluate(gtProvider, mProvider, metrics)

    # Print statistics ( ResultsView )
    view.run(results)

    return results

def _main_():

    parser = create_parser()
    args = parser.parse_args()

    view = SimpleView()

    metrics = []
    metrics.append(RecallPrecisionMetric3D(iou_thresh=0.5))

    run(args, view=view, metrics=metrics)




if __name__ == "__main__":
    _main_()
