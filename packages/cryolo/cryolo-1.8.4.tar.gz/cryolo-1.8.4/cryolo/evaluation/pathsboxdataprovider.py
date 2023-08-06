
from .boxdataprovider import BoxDataProvider, ImageBoxData
from cryolo.utils import BoundBox
from typing import Callable, List

class PathsDataProvider(BoxDataProvider):

    def __init__(self, paths : List[str],
                 reading_method : Callable[..., List[BoundBox]],
                 group_method : Callable[[str], str]):
        '''
        :param paths: List of filepaths.
        :param reading_method: Reading method for files in filepath.
        :param group_method: Extract the group out of the filename
        '''
        self.paths = paths
        self.reading_method = reading_method
        self.group_method = group_method

    def get_boxes(self) -> List[ImageBoxData]:
        result = []
        for file in self.paths:
            boxes = self.reading_method(file)
            group = self.group_method(file)
            arr = BoxDataProvider.boxes_to_nparray(boxes)
            dat = ImageBoxData(indentifer=file, data=arr, group=group)
            result.append(dat)

        return result
