__author__ = "Shreejaa Talla"


import random
import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Sampler
from typing import Iterator
from torch.utils.data._utils.fetch import _BaseDatasetFetcher
from torch.utils.data.dataloader import _BaseDataLoaderIter
from filament_augmentation.augment._augmentation import _Augmentation


class FilamentDataLoader(DataLoader):

    def __init__(self, dataset, batch_size: int, filament_ratio: tuple, n_batchs: int,
                 transforms: list, image_dim: int, image_type: str = 'rgb'):
        """
        :param dataset: Filament Dataset object.
        :param batch_size: each batch size.
        :param filament_ratio: tuple of number of (L,R,U) chiralities for each batch.
        :param n_batchs: number of batches.
        :param transforms: transformations json file.
        :param image_dim: image dimensions ,i.e, square dimensions.
        :param _counter: dict of images and number of times the image is transformed.
        :param _removed: set of images that should not be used after a certain threshold.
        """
        if batch_size % sum(filament_ratio) != 0:
            raise Exception("batch size and filament ratio is not properly matched")
        self._dataset: list = dataset.data
        self.filament_cutout: list = dataset.filament_cutouts_data
        self.batch_size: int = batch_size
        self.n_l, self.n_r, self.n_u = filament_ratio
        if self.n_l < 0 or self.n_r < 0 or self.n_u < 0:
            raise Exception("ratio cannot be negative")
        self.filament_ratio: tuple = filament_ratio
        self._counter: dict = dict()
        self._removed: set = set()
        self.total_filaments: int = batch_size*n_batchs
        self.transforms: list = transforms
        self.image_dim: tuple  = (image_dim, image_dim)
        self.image_type = image_type
        super().__init__(dataset.data, batch_size, shuffle=False, collate_fn=self.collate_fn,
                         sampler=CustomSampler(self.total_filaments), drop_last=False)

    def collate_fn(self, batch):
        """
        Augments the filaments based on the batch size, filament ratio.
        """
        filament_augmentation = _Augmentation(self.filament_cutout, self.batch_size,
                                              self.filament_ratio, self.total_filaments,
                                              self._counter, self._removed, self.transforms)
        c, rm = filament_augmentation.save_filaments()
        """
        Counter and removed list are updated for next iteration.
        """
        # self._counter.update(c)
        # self._removed = self._removed.union(rm)
        # print(len(self._removed))
        # self._removed.clear()
        filament_list = filament_augmentation.augmented_data
        random.shuffle(filament_list)
        org_images = list()
        images = list()
        class_ids = list()
        """
        if image dimensions are -1 then the original image is stored in torch dataset
        else the image is resized based on the given image dimensions.
        """
        if self.image_dim != (-1, -1):
            for org_image,image, classes in filament_list:
                if self.image_type == 'rgb':
                    image = image.convert('RGB')
                org_image = cv2.resize(np.array(org_image), self.image_dim)
                org_images.append(torch.from_numpy(org_image))
                image = np.array(image, dtype = np.float32)
                image = cv2.resize(image, self.image_dim)
                images.append(torch.from_numpy(image).T)
                if classes == -1:
                    classes = 2
                class_ids.append(torch.tensor(classes))
            image_tensor = torch.stack(tuple(images))
            classes = torch.stack(tuple(class_ids))
        else:
            org_images, image_tensor, classes = zip(*filament_list)
        return org_images, image_tensor, classes

    def _get_iterator(self) -> '_BaseDataLoaderIter':
        """
        Iterates data loader for custom iteration class.
        """
        super(FilamentDataLoader, self)._get_iterator()
        if self.num_workers == 0:
            return _CustomSingleProcessDataLoaderIter(self)


class _CustomSingleProcessDataLoaderIter(_BaseDataLoaderIter):
    """
    This class is called when data loader is iterated.
    """
    def __init__(self, loader):
        super(_CustomSingleProcessDataLoaderIter, self).__init__(loader)
        assert self._timeout == 0
        assert self._num_workers == 0

        self._dataset_fetcher = _CustomDatasetKind.create_fetcher(
            0, self._dataset, self._auto_collation, self._collate_fn, self._drop_last)

    def _next_data(self):
        index = self._next_index()
        data = self._dataset_fetcher.fetch(index)
        return data


class CustomSampler(Sampler[int]):
    """
    Sampler defines number of iterations a data loader should perform.
    """
    def __init__(self, n_iterations) -> None:
        self.n_iterations = n_iterations

    def __iter__(self) -> Iterator[int]:
        return iter(range(1,self.n_iterations+1))

    def __len__(self) -> int:
        return self.n_iterations


class _CustomMapDatasetFetcher(_BaseDatasetFetcher):
    """
    This class is initialized everytime the dataset kind class is called for map dataset.
    """
    def __init__(self, dataset, auto_collation, collate_fn, drop_last):
        super(_CustomMapDatasetFetcher, self).__init__(dataset, auto_collation, collate_fn, drop_last)

    def fetch(self, idx):
        """
        Calls collate function every time iterator calls it.
        """
        if self.auto_collation:
            data = idx
        return self.collate_fn(data)


class _CustomDatasetKind(object):
    """
    Create_fetcher is called everytime the iter class initializes the datasetkind.
    """
    Map = 0
    @staticmethod
    def create_fetcher(kind, dataset, auto_collation, collate_fn, drop_last):
        if kind == _CustomDatasetKind.Map:
            return _CustomMapDatasetFetcher(dataset, auto_collation, collate_fn, drop_last)