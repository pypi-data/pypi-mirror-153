from pathlib import Path
from typing import List, Optional, Sequence, Union

import albumentations
import numpy as np
import scipy.ndimage as ndi
import tifffile

from bioimageloader.collections import BBBC007
from bioimageloader.utils import stack_channels


class BBBC007NUnet(BBBC007):
    """Drosophila Kc167 cells (Adopted for NU-Net)

    NU-Net needs outline to be filled and only need DNA annotation.

    Outline annotation

    Images were acquired using a motorized Zeiss Axioplan 2 and a Axiocam MRm
    camera, and are provided courtesy of the laboratory of David Sabatini at the
    Whitehead Institute for Biomedical Research. Each image is roughly 512 x 512
    pixels, with cells roughly 25 pixels in dimeter, and 80 cells per image on
    average. The two channels (DNA and actin) of each image are stored in
    separate gray-scale 8-bit TIFF files.

    Notes
    -----
    - [4, 5, 11, 14, 15] have 3 channels but they are just all gray scale
        images. Extra work is required in get_image().

    .. [1] Jones et al., in the Proceedings of the ICCV Workshop on Computer
       Vision for Biomedical Image Applications (CVBIA), 2005.
    .. [2] [BBBC007](https://bbbc.broadinstitute.org/BBBC007)
    """
    # Dataset's acronym
    acronym = 'BBBC007'

    def __init__(
        self,
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        # specific to this dataset
        image_ch: Sequence[str] = ('DNA', 'actin',),
        anno_ch: Sequence[str] = ('DNA',),
        fill_holes: bool = True,
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
        image_ch : {'DNA', 'actin'} (default: ('DNA', 'actin'))
            Which channel(s) to load as image. Make sure to give it as a
            Sequence when choose a single channel.
        anno_ch : {'DNA', 'actin'} (default: ('DNA',))
            Which channel(s) to load as annotation. Make sure to give it as a
            Sequence when choose a single channel.
        fill_holes : bool (default: True)
            Fill outline annotation using `scipy.ndimage.binary_fill_holes()`

        See Also
        --------
        BBBC007 : Super class
        MaskDataset : Super class
        DatasetInterface : Interface
        """
        super().__init__(
            root_dir=root_dir,
            output=output,
            transforms=transforms,
            num_samples=num_samples,
            image_ch=image_ch,
            anno_ch=anno_ch,
            **kwargs
        )
        self.fill_holes = fill_holes

    def get_mask(self, p: Union[Path, List[Path]]) -> np.ndarray:
        if isinstance(p, Path):
            mask = tifffile.imread(p)
        else:
            mask = stack_channels(tifffile.imread, p)
        # dtype=bool originally and bool is not well handled by albumentations
        if self.fill_holes:
            mask = ndi.binary_fill_holes(mask)
        return mask.astype(np.float32)
