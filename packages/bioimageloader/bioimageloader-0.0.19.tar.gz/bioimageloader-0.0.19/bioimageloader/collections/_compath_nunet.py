from pathlib import Path
from typing import Optional, Sequence, Union

import albumentations
import numpy as np
from PIL import Image

from bioimageloader.collections import ComputationalPathology


class ComputationalPathologyNUnet(ComputationalPathology):
    """A Dataset and a Technique for Generalized Nuclear Segmentation for
    Computational Pathology [1]_ (Adopted for NU-Net)

    Notes
    -----
    - Resolution of all images is (1000,1000)
    - gt is converted from annotation recorded in xml format
    - gt has dtype of torch.float64, converted from numpy.uint16, and it has
      value 'num_objects' * 255 because it is base-transformed
    - The origianl dataset provides annotation in xml format, which takes
      long time to parse and to reconstruct mask images dynamically during
      training. Drawing masks beforehand makes training much faster. Use
      `mask_tif` in that case.
    - When `augmenters` is provided, set the `num_samples` argument
      30x1000x1000 -> 16x30=480 patches. Thus, the default `num_samples=720`
      (x1.5)
    - dtype of 'gt' is int16. However, to make batching easier, it will be
      casted to float32
    - Be careful about types of augmenters; avoid interpolation

    References
    ----------
    .. [1] N. Kumar, R. Verma, S. Sharma, S. Bhargava, A. Vahadane, and A.
       Sethi, “A Dataset and a Technique for Generalized Nuclear Segmentation
       for Computational Pathology,” IEEE Transactions on Medical Imaging, vol.
       36, no. 7, pp. 1550–1560, Jul. 2017, doi: 10.1109/TMI.2017.2677499.

    """

    # Dataset's acronym
    acronym = 'ComPath'
    # Hard code resolution to parse annotation (.xml)
    _resolution = (1000, 1000)

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
        # Specific to this dataset
        mask_tif: bool = False,
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
        mask_tif : bool (default: False)
            Instead of parsing every xml file to reconstruct mask image arrays,
            use pre-drawn mask tif files which should reside in the same folder
            as annotation xml files.
        invt : bool (default: True)
            Invert image pixel values

        See Also
        --------
        ComputationalPathology : Super class
        MaskDataset : Super class
        MaskDatasetInterface : Interface of the super class

        """
        super().__init__(
            root_dir=root_dir,
            output=output,
            transforms=transforms,
            num_samples=num_samples,
            grayscale=grayscale,
            grayscale_mode=grayscale_mode,
            mask_tif=mask_tif,
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
