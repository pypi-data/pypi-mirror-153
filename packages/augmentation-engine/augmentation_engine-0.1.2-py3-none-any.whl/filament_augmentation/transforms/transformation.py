__author__ = "Shreejaa Talla"

import PIL
import random
from torchvision import transforms as torchvision_transforms


class _Transformation:
    """
    This class transforms the image by applying a method.
    """
    def __init__(self, image: PIL, transforms):
        """
        :param image: Image object
        :param transforms: the method applied to transforms the image.
        """
        self.image: PIL = image
        self._transforms = transforms

    def transform_image(self) -> PIL:
        """
        Gets the image from given image path and performs transformation.
        :return: transformed image.
        """
        transformed_img = self._transforms(self.image)
        return transformed_img


def get_transform(transforms: list) -> torchvision_transforms.Compose:
    """
    This method forms a list of filter of randomly with random intensities using
    torch vision transformations.
    :return: the composed transforms using torchvision transforms.
    """
    random.shuffle(transforms)
    return torchvision_transforms.Compose(transforms)
