from abc import ABC, abstractmethod

import numpy as np


class AugmentationMethod(ABC):

    @abstractmethod
    def transform_image(self, image : np.array) -> np.array:
        pass

    @abstractmethod
    def transform_coords(self, object_coords : list, image_dims : list) -> list:
        pass