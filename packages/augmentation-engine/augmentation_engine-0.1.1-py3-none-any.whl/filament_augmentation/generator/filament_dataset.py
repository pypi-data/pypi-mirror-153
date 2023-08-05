__author__ = "Shreejaa Talla"


import torch
from torch.utils.data import Dataset

from filament_augmentation.generator._filament_generator import _FilamentGenerator
from filament_augmentation.metadata.filament_metadata import FilamentMetadata


class FilamentDataset(Dataset):

    def __init__(self, bbso_path: str, ann_file: str, start_time: str, end_time: str):
        """
        The constructor gets the image ids based on start and end time.
        based on the image ids, filaments annotation index and their respective class labels
        are initialized to dataset.
        :param bbso_path: path to bsso full disk images.
        :param ann_file: path to annotations file.
        :param start_time: start time in YYYY:MM:DD HH:MM:SS.
        :param end_time: end time in YYYY:MM:DD HH:MM:SS.
        """
        filament_metadata = FilamentMetadata(ann_file,start_time, end_time)
        filament_metadata.parse_data()
        self.bbso_img_ids: list = filament_metadata.bbso_img_ids
        self.filament_cutouts_data: _FilamentGenerator = _FilamentGenerator(ann_file, bbso_path, self.bbso_img_ids)
        self.data: list = self.filament_cutouts_data.filament_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        anno, class_name = self.data[idx]
        anno_tensor = torch.from_numpy(anno)
        class_id = torch.tensor(class_name)
        return anno_tensor, class_id
