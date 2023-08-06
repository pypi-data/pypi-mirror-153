from pathlib import Path
from typing import Optional, Sequence, Union

import albumentations
import numpy as np
from PIL import Image

from bioimageloader.collections import TNBC


class TNBCNUnet(TNBC):
    """TNBC Nuclei Segmentation Dataset (Adopted for NU-Net)

    References
    ----------
    Segmentation of Nuclei in Histopathology Images by Deep Regression of
    the Distance Map [1]_

    .. [1] https://ieeexplore.ieee.org/document/8438559

    """

    # Dataset's acronym
    acronym = 'TNBC'

    def __init__(
        self,
        # Interface requirement
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        grayscale: bool = True,
        grayscale_mode: Union[str, Sequence[float]] = 'cv2',
        # NU-Net args
        invt: bool = True,
        **kwargs
    ):
        """
        Parameters
        ---------
        root_dir : str
            Path to root directory
        output : {'image','mask','both'} (default: 'both')
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
        invt : bool (default: True)
            Invert image pixel values

        See Also
        --------
        MaskDataset : Super class
        DatasetInterface : Interface
        """
        super().__init__(
            root_dir=root_dir,
            output=output,
            transforms=transforms,
            num_samples=num_samples,
            grayscale=grayscale,
            grayscale_mode=grayscale_mode,
            **kwargs
        )
        self.invt = invt

    def get_image(self, p: Path) -> np.ndarray:
        img = Image.open(p)
        if img.mode == 'RGBA':
            img = img.convert(mode='RGB')
        if self.invt:
            return ~np.asarray(img)
        return np.asarray(img)
