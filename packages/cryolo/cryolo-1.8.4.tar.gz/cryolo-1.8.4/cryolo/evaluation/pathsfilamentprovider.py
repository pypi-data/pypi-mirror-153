
from .boxdataprovider import BoxDataProvider, ImageBoxData
from cryolo.utils import BoundBox, Filament
from typing import Callable, List
from cryolo.utils import resample_filament
class PathsFilamentProvider(BoxDataProvider):

    def __init__(self, paths : List[str],
                 reading_method : Callable[..., List[Filament]],
                 group_method: Callable[[str], str],
                 resampling_distance : int = None):
        '''
        :param paths: List of filepaths.
        :param reading_method: Reading method for files in filepath.
        :param group_method: Extract the group out of the filename
        :param resampling_distance: If the filaments should get resampled before comparision, one can specifiy this here
        '''
        self.paths = paths
        self.reading_method = reading_method
        self.group_method = group_method
        self.resampling_distance = resampling_distance

    def get_boxes(self) -> List[ImageBoxData]:
        result = []
        for file in self.paths:
            filaments = self.reading_method(file)
            group = self.group_method(file)
            boxes = []

            for fil in filaments:
                if self.resampling_distance is not None:
                    fil = resample_filament(fil, self.resampling_distance)
                fil_boxes = [box for box in fil.boxes]
                boxes.extend(fil_boxes)
            arr = BoxDataProvider.boxes_to_nparray(boxes)
            dat = ImageBoxData(indentifer=file, data=arr, group=group)
            result.append(dat)

        return result
