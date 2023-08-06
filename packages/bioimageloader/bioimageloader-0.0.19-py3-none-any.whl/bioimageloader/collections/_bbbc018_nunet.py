from pathlib import Path
from typing import List, Optional, Sequence, Union

import albumentations
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes

from ..utils import stack_channels
from bioimageloader.collections import BBBC018


class BBBC018NUnet(BBBC018):
    """Human HT29 colon-cancer cells (diverse phenotypes) (Adopted for NU-Net)

    The image set consists of 56 fields of view (4 from each of 14 samples).
    Because there are three channels, there are 168 image files. (The samples
    were stained with Hoechst 33342, pH3, and phalloidin. Hoechst 33342 is a DNA
    stain that labels the nucleus. Phospho-histone H3 indicates mitosis.
    Phalloidin labels actin, which is present in the cytoplasm.) The samples are
    the top-scoring sample from each of Jones et al.'s classifiers, as listed in
    the file SamplesScores.zip in their supplement. The files are in DIB format,
    as produced by the Cellomics ArrayScan instrument at the Whitehead–MIT
    Bioimaging Center. We recommend using Bio-Formats to read the DIB files.
    Each image is 512 x 512 pixels.

    The filenames are of the form wellidx-channel.DIB, where wellidx is the
    five-digit well index (from Jones et al.'s supplement) and channel is either
    DNA, actin, or pH3, depending on the channel.

    Notes
    -----
    - BBBC018_v1_images/10779 annotation is missing. len(anno_dict) =
      len(file_list) - 1; ind={26}
        [PosixPath('images/bbbc/018/BBBC018_v1_images/10779-DNA.DIB'),
         PosixPath('images/bbbc/018/BBBC018_v1_images/10779-actin.DIB'),
         PosixPath('images/bbbc/018/BBBC018_v1_images/10779-pH3.DIB')]
    - Every DIB has 3 channels (Order = (DNA,actin,pH3)). The second one is the
      object.
    - DNA -> Nuceli
    - Actin -> Cell
    - Annotation is outline one, but every anno is closed so binary_fill_holes
      works fine
    - For some reason annotation is y inverted

    References
    ----------
    .. [1] https://bbbc.broadinstitute.org/BBBC018
    """

    # Dataset's acronym
    acronym = 'BBBC018'

    def __init__(
        self,
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        grayscale: bool = False,
        grayscale_mode: Union[str, Sequence[float]] = 'equal',
        # specific to this dataset
        anno_ch: Sequence[str] = ('DNA',),
        drop_missing_pairs: bool = True,
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
        grayscale : bool (default: False)
            Convert images to grayscale
        grayscale_mode : {'cv2', 'equal', Sequence[float]} (default: 'equal')
            How to convert to grayscale. If set to 'cv2', it follows opencv
            implementation. Else if set to 'equal', it sums up values along
            channel axis, then divides it by the number of expected channels.
        anno_ch : {'DNA', 'actin'} (default: ('DNA',))
            Which channel(s) to load as annotation. Make sure to give it as a
            Sequence when choose a single channel.
        drop_missing_pairs : bool (default: True)
            Valid only if `output='both'`. It will drop images that do not have
            mask pairs.
        fill_holes : bool (default: True)
            Fill outline annotation using `scipy.ndimage.binary_fill_holes()`

        See Also
        --------
        BBBC018 : Super class
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
            anno_ch=anno_ch,
            drop_missing_pairs=drop_missing_pairs,
            **kwargs
        )
        self.fill_holes = fill_holes

    def get_mask(self, p: Union[Path, List[Path]]) -> np.ndarray:
        if isinstance(p, Path):
            mask = np.asarray(Image.open(p))
            if self.fill_holes:
                mask = binary_fill_holes(mask)
        else:
            mask = stack_channels(Image.open, p)
            if self.fill_holes:
                for c in range(mask.shape[-1]):
                    mask[..., c] = binary_fill_holes(mask[..., c])
        # For some reason mask is -y
        return np.ascontiguousarray(mask[::-1, ...]).astype(np.float32)
