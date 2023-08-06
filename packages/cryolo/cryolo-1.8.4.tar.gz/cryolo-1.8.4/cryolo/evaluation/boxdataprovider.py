from abc import ABC, abstractmethod
import numpy as np
from typing import List
from cryolo.utils import BoundBox
from dataclasses import dataclass
import os

@dataclass
class ImageBoxData:
    indentifer : str
    group : str
    data : np.array

class BoxDataProvider(ABC):

    @abstractmethod
    def get_boxes(self) -> List[ImageBoxData]:
        """
        :return: List of box coordinates as numpy array.
        """
        pass

    @staticmethod
    def path_matching_filename_eq(patha: str, pathb: str) -> bool:
        # FILL THAT TOMORROW
        filenamea = os.path.splitext(os.path.basename(patha))[0]
        filenameb = os.path.splitext(os.path.basename(pathb))[0]
        return filenamea == filenameb

    @staticmethod
    def group_method_lastfolder(path: str) -> str:
        return os.path.basename(os.path.dirname(path))

    @staticmethod
    def boxes_to_nparray(boxes : List[BoundBox]) -> np.array:
        """
        :param boxes: List of Bounding boxes
        :return: np aarray with columns x,y,z,width,height,depth for 3D and x,y width,height for 2D
        """

        is2D = np.any([b.z==None for b in boxes])

        if is2D:
            data = np.zeros(shape=(len(boxes), 4))
        else:
            data = np.zeros(shape=(len(boxes), 6))

        for boxi, box in enumerate(boxes):
            data[boxi, 0] = box.x
            data[boxi, 1] = box.y
            if is2D:
                data[boxi, 2] = box.w
                data[boxi, 3] = box.h
            else:
                data[boxi, 2] = box.z
                data[boxi, 3] = box.w
                data[boxi, 4] = box.h
                data[boxi, 5] = box.depth

        return data