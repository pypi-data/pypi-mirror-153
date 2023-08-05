__author__ = "Shreejaa Talla"


import os
import PIL
from PIL import Image
import torch



from torchvision.datasets.coco import CocoDetection


def _has_only_empty_bbox(anno):
    """
    Checking if all the bounding boxes corresponding to an image have a height or width of less than 1 unit.

    If all the bounding boxes have height or width of less than 1 unit then
    considering the image have no bounding boxes.

    :param anno: list of annotations (bounding boxes) for an image.
    :return: True if the image has no bounding boxes, False otherwise.
    """
    return all(any(o <= 1 for o in obj["bbox"][2:]) for obj in anno)


def _has_valid_annotation(anno):
    """
    Checks if the image has valid bounding boxes.
    :param anno: list of annotations (bounding boxes) for an image.
    :return: True if the annotation list has valid bounding boxes.
    """
    # if it's empty, there is no annotation
    if len(anno) == 0:
        return False
    if _has_only_empty_bbox(anno):
        return False
    if "keypoints" not in anno[0]:
        return True
    return False


class _FilamentGenerator(CocoDetection):

    def __init__(self, ann_file: str, root: str, ids: list):
        """
        The class constructor initiates the class instance variables. It meanwhile identifies and excludes invalid
        annotations and images without annotations.

        :param ann_file: The JSON file with images and annotation data.
        :param root: the path to BBSO images.
        :param ids: image ids generated for particular timestamp
        """
        super().__init__(root, ann_file)
        self.ids: list = sorted(ids)
        filament_data = []
        ids = []
        for idx, img_id in enumerate(self.ids):
            ann_ids = self.coco.getAnnIds(imgIds=img_id, iscrowd=None)
            anno = self.coco.loadAnns(ann_ids)
            if _has_valid_annotation(anno):
                if len(anno) == 1:
                    filament_data.append([idx, anno[0]["category_id"]])
                else:
                    for a in anno:
                        filament_data.append([idx, a["category_id"]])
                ids.append(img_id)
        self.ids: list = ids
        self.filament_data: list = filament_data

    def _load_image(self, id: int) -> Image.Image:
        year, month, day, image_path = self.coco.loadImgs(id)[0]["file_name"].split(',')
        return Image.open(os.path.join(self.root, year, month, day, image_path))

    def get_filament_cutouts(self, idx: int) -> PIL:
        """
        This method uses the annotation dict to crop the filaments from full disk bbso images
        for a particular index.

        :param idx: index of the image list.
        :param filament_dir: filament directory provided.
        :return: cropped image (filament image).
        """
        img, anno = super().__getitem__(idx)
        img = img.convert("L")
        anno = [obj for obj in anno if obj['iscrowd'] == 0]
        boxes = [obj["bbox"] for obj in anno]
        boxes_xyxy: list = [0] * len(boxes)
        for i in range(len(boxes)):
            a_bbox = boxes[i]
            x0, y0 = a_bbox[0], a_bbox[1]
            x1, y1 = x0 + a_bbox[2], y0 + a_bbox[3]
            boxes_xyxy[i] = [x0, y0, x1, y1]

        boxes_xyxy = torch.as_tensor(boxes_xyxy).reshape(-1, 4)  # guard against no boxes

        img_crop = img.crop(
            (int(boxes_xyxy[0][0]), int(boxes_xyxy[0][1]), int(boxes_xyxy[0][2]), int(boxes_xyxy[0][3])))
        return img_crop
