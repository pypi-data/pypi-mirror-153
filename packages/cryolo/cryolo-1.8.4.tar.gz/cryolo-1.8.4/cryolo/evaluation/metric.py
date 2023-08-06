from abc import ABC, abstractmethod
import numpy as np
from typing import Dict
class Metric(ABC):

    @abstractmethod
    def eval(self, boxes : np.array, boxesgt : np.array) -> Dict[str,float]:
        """
        :param boxes: Predicted data
        :param boxesgt: Ground truth data
        :return: List with evaluation result
        """
        pass