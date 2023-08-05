__author__ = "Shreejaa Talla"

from datetime import datetime
from filament_augmentation.utils import file_utilities, timestamp_utilites


class FilamentMetadata:
    """
    This class provides  metadata about filaments based on the start and end timestamps.
    """
    def __init__(self, ann_file: str, start_time: str, end_time: str):
        """
        This constructor generates the list of images in between the start_time and end_time from BBSO data.
        Timestamp value in the format YYYY-MM-DD HH:MM:SS
        :param start_time: start_index time
        :param end_time: end time
        """
        self.start_time: datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        self.end_time: datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        if self.start_time > self.end_time:
            raise Exception("start time provided can't be greater than end time")
        self.bbso_json: dict = file_utilities.read_json(ann_file)

    def parse_data(self):
        """
        based on the timestamp values, the annotation json file is parsed to find the closest timestamps
        available and initialize the images.
        """
        self.timestamp_dict: dict = timestamp_utilites.get_timestamp_dict(self.bbso_json)
        start_index: int = timestamp_utilites.find_closest(self.start_time, self.timestamp_dict)
        end_index: int = timestamp_utilites.find_closest(self.end_time, self.timestamp_dict)
        self.bbso_img_ids: list = list(self.timestamp_dict.keys())[start_index: end_index+1]

    def get_chirality_distribution(self) -> (int, int, int):
        """
        This method counts the number of left, right, and unidentified chirality f
        filaments in the given time interval, from BBSO data.

        :return: the number of left, right, and undefined filaments in the given time interval.
        """
        n_l = 0
        n_r = 0
        n_u = 0
        self.parse_data()
        annotations = self.bbso_json['annotations']
        for anno in annotations:
            if anno['image_id'] in self.bbso_img_ids:
                if anno['category_id'] == 0:
                    n_u += 1
                if anno['category_id'] == 1:
                    n_r += 1
                if anno['category_id'] == -1:
                    n_l += 1
        return n_l, n_r, n_u

