from abc import ABC, abstractmethod
from cryolo.evaluation.tomoevaluation import EvaluationResult
from typing import List

class ResultsView(ABC):

    @abstractmethod
    def run(self, results : List[EvaluationResult]):

        pass

class SimpleView(ResultsView):

    def run(self, results: List[EvaluationResult]):

        dataset_ids = set([r.dataset for r in results])

        for datid in dataset_ids:
            results_for_one_dataset = [r for r in results if r.dataset == datid]
            print("Dataset:", datid)
            # TODO This should also take care of thresholds
            for result in results_for_one_dataset:
                print("\t", result.metric, result.value)

