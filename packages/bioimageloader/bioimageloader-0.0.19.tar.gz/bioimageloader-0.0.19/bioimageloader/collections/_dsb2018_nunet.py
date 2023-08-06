from pathlib import Path
from typing import Optional, Sequence, Union

import albumentations
import numpy as np
from PIL import Image

from bioimageloader.collections import DSB2018


class DSB2018NUnet(DSB2018):
    """Data Science Bowl 2018 (Adopted for NU-Net)

    Each entry is a pair of an image and a mask.
    By default, it applies `base_transform`, which makes an image Tensor and
    have data range of uint8 [0, 255].

    Returns a dictionary, whose key is determined by `output` argument.
    """

    # Set acronym
    acronym = 'DSB2018'

    def __init__(
        self,
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        grayscale: bool = False,
        grayscale_mode: Union[str, Sequence[float]] = 'cv2',
        # specific to this dataset
        training: bool = True,
        # NU-Net args
        idx_invt: Optional[Sequence[int]] = None,
        **kwargs
    ):
        """
        Parameters
        ----------
        root_dir : str
            Path to root directory
        output : {'image', 'mask', 'both'} (default: 'both')
            Change outputs. 'both' returns {'image': image, 'mask': mask}.
        transforms : albumentations.Compose, optional
            An instance of Compose (albumentations pkg) that defines
            augmentation in sequence.
        num_samples : int, optional
            Useful when ``transforms`` is set. Define the total length of the
            dataset. If it is set, it overwrites ``__len__``.
        grayscale : bool (default: False)
            Convert images to grayscale
        grayscale_mode : {'cv2', 'equal', Sequence[float]} (default: 'cv2')
            How to convert to grayscale. If set to 'cv2', it follows opencv
            implementation. Else if set to 'equal', it sums up values along
            channel axis, then divides it by the number of expected channels.
        training : bool (default: True)
            Load training set if True, else load testing one
        idx_invt : sequence of int, optional
            Given indices of images, invert pixel values within their data type.
            e.g. in case of uint8, 0 -> 255, 254 -> 1.

        See Also
        --------
        DSB2018 : Super class
        MaskDataset : Super class of DSB2018
        DatasetInterface : Interface

        """
        super().__init__(
            root_dir=root_dir,
            output=output,
            transforms=transforms,
            num_samples=num_samples,
            grayscale=grayscale,
            grayscale_mode=grayscale_mode,
            training=training,
            **kwargs
        )
        self.idx_invt = idx_invt

    def get_image(self, p: Path) -> np.ndarray:
        img = Image.open(p)
        img = img.convert(mode='RGB')

        ind = self.file_list.index(p)
        if self.idx_invt is not None:
            if ind in self.idx_invt:
                img = ~np.asarray(img)
                return img
        return np.asarray(img)
