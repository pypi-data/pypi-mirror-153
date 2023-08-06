from functools import cached_property
from pathlib import Path
from typing import Dict, Optional

import albumentations
import numpy as np
from PIL import Image

from bioimageloader.collections import MurphyLab


class MurphyLabNUnet(MurphyLab):
    """Nuclei Segmentation In Microscope Cell Images: A Hand-Segmented Dataset
    And Comparison Of Algorithms (Adopted for NU-Net)

    Mask variation. Manually filled boundary labels with a bucket tool and saved
    in .png format.


    IMPORTANT
    ---------
    This dataset has many issues whose details can be found below. The simpleset
    way is to drop those that cause isseus. It is recommended to not opt out
    `drop_missing_pairs()` and `drop_broken_files()`. Otherwise, it will meet
    exceptions.

    If one wants filled hole, `fill_save_mask()` function will fill holes with
    some tricks to handle edge cases and save them as .png format. Then set
    `filled_mask` argument to True to load them.


    Notes
    -----
    - Two annotation formats; Photoshop and GIMP. It seems that two annotators
      worked separately. segmented-ashariff will be ignored. In total, 97
      segmented images (out of 100)
    - 3 missing segmentations: ind={31, 43, 75}
        ./data/images/dna-images/gnf/dna-31.png
        ./data/images/dna-images/gnf/dna-43.png
        ./data/images/dna-images/ic100/dna-25.png
    - Manually filled annotation to make masks using GIMP
    - 2009_ISBI_2DNuclei_code_data/data/images/segmented-lpc/ic100/dna-15.xcf
      does not have 'borders' layer like the others.  This one alone has
      'border' layer.

    .. [1] L. P. Coelho, A. Shariff, and R. F. Murphy, “Nuclear segmentation in
       microscope cell images: A hand-segmented dataset and comparison of
       algorithms,” in 2009 IEEE International Symposium on Biomedical Imaging:
       From Nano to Macro, Jun. 2009, pp. 518–521, doi:
       10.1109/ISBI.2009.5193098.
    """

    # Dataset's acronym
    acronym = 'MurphyLab'

    def __init__(
        self,
        # Interface requirement
        root_dir: str,
        *,
        output: str = 'both',
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        # Specific to this dataset
        drop_missing_pairs: bool = True,
        drop_broken_files: bool = False,
        filled_mask: bool = True,
        **kwargs
    ):
        """
        Parameters
        ---------
        root_dir : str or pathlib.Path
            Path to root directory
        output : {'image','mask','both'} (default: 'both')
            Change outputs. 'both' returns {'image': image, 'mask': mask}.
        transforms : albumentations.Compose, optional
            An instance of Compose (albumentations pkg) that defines
            augmentation in sequence.
        num_samples : int, optional
            Useful when ``transforms`` is set. Define the total length of the
            dataset. If it is set, it overwrites ``__len__``.
        drop_missing_pairs : bool (default: True)
            Valid only if `output='both'`. It will drop images that do not have
            mask pairs.
        drop_broken_files : bool (default: False)
            Drop broken files that cannot be read
        filled_mask : bool (default: True)
            Use saved filled masks through `fill_save_mask()` method instead of
            default boundary masks. If one would want to use manually modified
            masks, the annotation files should have the same name as '*.xcf'
            with modified suffix by '.png'.

        See Also
        --------
        MurphyLab : Super class
        MaskDataset : Super class
        DatasetInterface : Interface

        """
        super().__init__(
            root_dir=root_dir,
            output=output,
            transforms=transforms,
            num_samples=num_samples,
            drop_missing_pairs=drop_missing_pairs,
            drop_broken_files=drop_broken_files,
            filled_mask=filled_mask,
            **kwargs
        )

    def get_mask(self, p: Path) -> np.ndarray:
        mask = Image.open(p)
        # Red channel is where anno is
        return np.asarray(mask)[..., 0]

    @cached_property
    def anno_dict(self) -> Dict[int, Path]:
        ext = '.png' if self.filled_mask else '.xcf'
        anno_dict = {}
        for i, p in enumerate(self.file_list):
            p_anno = '/'.join([p.parent.stem, p.stem + '-filled' + ext])
            # Ignore 'segmented-ashariff`. It seems that Ashariff got bored
            # after 10 images.
            anno = p.parents[2] / 'segmented-lpc' / p_anno
            if anno.exists():
                anno_dict[i] = anno
        return anno_dict
