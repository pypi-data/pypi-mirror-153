__author__ = "Shreejaa Talla"


import PIL
from CONSTANTS import _LEFT_CHIRALITY, _RIGHT_CHIRALITY, _UNDEFINED_CHIRALITY
from filament_augmentation.generator._filament_generator import _FilamentGenerator
from filament_augmentation.transforms import _transformation
from filament_augmentation.transforms._transformation import _Transformation


class _Augmentation:

    def __init__(self, filament_generator: _FilamentGenerator, batch_size: int, counts_per_batch: tuple,
                 total_filaments: int, _counter: dict, _removed: set, transforms: list):
        """
        Initializes the following parameters and throws exception if filament ratios are negative.
        :param filament_generator: Filament generator object
        :param batch_size: batch size for each iteration
        :param counts_per_batch: filament ratio in the format(L, R, U).
        :param total_filaments: total number of filaments, i.e, batch_size * number of batchs
        :param _counter: a dict of index and counts from previous iteration, else declares new one.
        :param _removed: a list of removed index from previous iteration or declares new one.
        """
        self.filament_cutouts: _FilamentGenerator = filament_generator
        self.ratio: tuple = counts_per_batch
        self.batch_size: int = batch_size
        self.dataset: list = self.filament_cutouts.filament_data
        self.n_l, self.n_r, self.n_u = counts_per_batch
        self.total_filaments: int = total_filaments
        if self.n_l < 0 or self.n_r < 0 or self.n_u < 0:
            raise Exception("Number of chiralities cannot be negative")
        self.augmented_data: list = list()
        self._counter: dict = _counter
        self._removed: set = _removed
        self.transforms: list = transforms

    def save_filaments(self):
        """
        For each chirality type based on batch and ratio,
         generate_filaments function is called.

        :return : counter dict and removed list.
        """
        n_times = self.batch_size // sum(self.ratio)
        if self.n_l != 0:
            self.__generate_filaments_each_type(_LEFT_CHIRALITY, n_times * self.n_l)
        if self.n_r != 0:
            self.__generate_filaments_each_type(_RIGHT_CHIRALITY, n_times * self.n_r)
        if self.n_u != 0:
            self.__generate_filaments_each_type(_UNDEFINED_CHIRALITY, n_times * self.n_u)
        return self._counter, self._removed

    def __get_filament_list(self, chirality_type: int) -> list:
        """
        This method get the list of annotation index for a chirality type.

        :param chirality_type: Left, right or undefined chiralities

        :return: list of index of annotations.
        """
        type_filaments = list()
        for x in self.dataset:
            if x[1] == chirality_type:
                type_filaments.append(x[0])
        return type_filaments

    def __cal_total_augments(self, chirality_type: int) -> float:
        """
        Calculate total number of filaments that should be augmented for each type.

        :param chirality_type: Left, right or unidentified

        :return: total augmentations
        """
        total = 0
        if chirality_type == _UNDEFINED_CHIRALITY:
            total = (self.n_u * self.total_filaments) / sum(self.ratio)
        elif chirality_type == _LEFT_CHIRALITY:
            total = (self.n_l * self.total_filaments) / sum(self.ratio)
        elif chirality_type == _RIGHT_CHIRALITY:
            total = (self.n_r * self.total_filaments) / sum(self.ratio)
        return total

    def __generate_filaments_each_type(self, chirality_type, n: int) -> None:
        """
        generates the extra filaments by performing transformations
        provided based on their types.

        :param chirality_type: Left, right or undefined chiralities.
        :param n: number of filament.

        :return: None.
        """
        count, filament_list, n_image_copies, remain = self.__initial_calculations(chirality_type)
        """
        Initializing counter for each chirality type.
        """
        if len(self._counter) == 0:
            self._counter.update({str(idx) + "_" + str(chirality_type): 0 for idx in filament_list})
        else:
            for idx in filament_list:
                if str(idx)+"_"+str(chirality_type) not in self._counter:
                    self._counter[str(idx) + "_" + str(chirality_type)] = 0
        if remain != 0 and n_image_copies == 0:
            """
            This part generated the remaining images, i.e., after all n_image_copies are 
            generated, sum of all n_image_copies is less than required copies then this part
            will be executed.
            """
            idx = [[k.split("_")[0], v] for k, v in self._counter.items()
                   if v < 1 and k.split("_")[1] == str(chirality_type)]
            for id, c in idx:
                count = self.__generate_image(c, chirality_type, count, id)
                if count >= n:
                    return
        idx = [[k.split("_")[0], v] for k, v in self._counter.items()
               if v < n_image_copies and k.split("_")[1] == str(chirality_type)]
        count, idx = self.__image_augments_original(chirality_type, count, idx, n, n_image_copies)
        self.__images_augments_remove_list(chirality_type, count, idx, n, n_image_copies)

    def __initial_calculations(self, chirality_type: int) -> int:
        """
        before augmentation, some calculations are made based on each type.
        :param chirality_type: left, right or unidentified.
        :return : total augmentations, n_image_copies, remain, count.
        """
        filament_list = self.__get_filament_list(chirality_type)
        length = len(filament_list)
        total = self.__cal_total_augments(chirality_type)
        n_image_copies = total // length
        remain = total % length
        count = 0
        return count, filament_list, n_image_copies, remain

    def __image_augments_original(self, chirality_type: int, count: int, idx: int, n: int, n_image_copies: int) -> int:
        """
        For each original filament cutout, n_image_copies are augmented and
        the counter is increase by 1 every time the same image index is called.
        For every loop only the indexes whose counter is not more than or equal to
        n_image_copies are used to generate images. This loop breaks when required
        left, right and unidentified augmentations are done based on batch_size.

        :param chirality_type: left, right or unidentified
        :param count: count_max == batch_size
        :param idx: index of annotation object.
        :param n: number of left/right/unidentified filaments generated for each batch.
        :param n_image_copies: number of copies/augmentations for each image.

        :return : count, idx
        """
        for i in range(count, n):
            if count >= n:
                break
            idx = [[k.split("_")[0], v] for k, v in self._counter.items()
                   if v < n_image_copies and k.split("_")[1] == str(chirality_type)]
            for id, c in idx:
                count = self.__generate_image(c, chirality_type, count, id)
                i += 1
                if count >= n:
                    break
        return count, idx

    def __images_augments_remove_list(self, chirality_type: int, count: int, idx: int, n: int, n_image_copies: int):
        """
        Remaining images are augmented from the removed list, i.e, after all n_image_copies are generated.
        At minimum 0 images are augmented from each image or at maximum 1 image.
        For every iteration counter picks up indexes which are augmented n_image_copies times.

        :param chirality_type: left, right or unidentified chirality.
        :param count: count_max == batch_size.
        :param idx: removed index of annotation object.
        :param n: number of left/right/unidentified filaments generated for each batch.
        :param n_image_copies: number of copies/augmentations for each image.
        """
        rm_idx = set(k.split("_")[0] for k, v in self._counter.items()
                     if v == n_image_copies and k.split("_")[1] == str(chirality_type))
        self._removed = self._removed.union(rm_idx)
        if len(idx) == 0 and count < n:
            for rm in rm_idx:
                c = self._counter.get(rm + "_" + str(chirality_type))
                count = self.__generate_image(c, chirality_type, count, rm)
                if count >= n:
                    break

    def __generate_image(self, c: int, chirality_type: int, count, id: int) -> int:
        """
        1. Updates the counter for each image augmentation.
        2. Gets the filament image based on the index.
        3. Transforms the image and append it to the main data.

        :param c: number of times an image is used for augmentation.
        :param chirality_type: left, right or unidentified chirality.
        :param count: number of images are being augmented.
        :param id: index of annotation object.

        :return : count
        """
        self._counter.update({str(id) + "_" + str(chirality_type): c + 1})
        image = self.filament_cutouts.get_filament_cutouts(int(id))
        self.augmented_data.append(self.__perform_transformations
                                   (chirality_type, image))
        count += 1
        return count

    def __perform_transformations(self, chirality_type: int, image: PIL) -> list:
        """
            This method performs the transformations on image based on the list of
            transforms functions provided.

            :param chirality_type: Left, right or undefined chirality.
            :param image: image file.

            :return: list of transformed image and type
            """
        transform = _Transformation(image, _transformation.get_transform(self.transforms))
        transformed_image = transform.transform_image()
        return [image, transformed_image, chirality_type]
