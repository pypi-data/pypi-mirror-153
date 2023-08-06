import os.path
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

import albumentations
import numpy as np
import tifffile
from PIL import Image

from bioimageloader.collections import DigitalPathology


class DigitalPathologyNUnet(DigitalPathology):
    """Deep learning for digital pathology image analysis: A comprehensive
    tutorial with selected use cases (Adopted for NU-Net)

    Notes
    -----
    - Annotation is partial, thus `output='image'` by default.

    References
    ----------
    .. [1] A. Janowczyk and A. Madabhushi, “Deep learning for digital pathology
       image analysis: A comprehensive tutorial with selected use cases,” J
       Pathol Inform, vol. 7, Jul. 2016, doi: 10.4103/2153-3539.186902.
    """
    # Dataset's acronym
    acronym = 'DigitPath'

    def __init__(
        self,
        # Interface requirement
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        grayscale: bool = False,
        grayscale_mode: Union[str, Sequence[float]] = 'cv2',
        # NU-Net args
        invt: bool = True,
        **kwargs
    ):
        """
        Parameters
        ----------
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
        DigitalPathology : Super class
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
        tif = tifffile.imread(p)
        if self.invt:
            return ~tif
        return tif
