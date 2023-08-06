from pathlib import Path
from typing import Optional, Sequence, Union

import albumentations
import numpy as np
import tifffile

from bioimageloader.collections import UCSB


class UCSBNUnet(UCSB):
    """A biosegmentation benchmark for evaluation of bioimage analysis methods
    (Adopted for NU-Net)

    Notes
    -----
    - 32 'benign', 26 'malignant' images (58 images in total)
    - 58x768x896 -> ~600 patches. Thus, the defulat `num_samples=900` (x1.5).
    - Images are not fully annotated

    References
    ----------
    .. [1] E. Drelie Gelasca, B. Obara, D. Fedorov, K. Kvilekval, and B.
       Manjunath, “A biosegmentation benchmark for evaluation of bioimage
       analysis methods,” BMC Bioinformatics, vol. 10, p. 368, Nov. 2009, doi:
       10.1186/1471-2105-10-368.
    """
    # Dataset's acronym
    acronym = 'UCSB'

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
        category: Sequence[str] = ('malignant',),
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
        category : {'benign', 'malignant'} (default: ('malignant',))
            Select which category of output you want
        invt : bool (default: True)
            Invert image pixel values

        See Also
        --------
        UCSB : Super class
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
            category=category,
            **kwargs
        )
        self.invt = invt

    def get_image(self, p: Path) -> np.ndarray:
        tif = tifffile.imread(p)
        return ~tif
