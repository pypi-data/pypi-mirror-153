"""Dorian's data

It expects below directory structure:
    root_dir
    └── data_folder
        ├── exp0
        │   ├── cond0
        │   └── cond1
        └── exp1
            ├── cond0
            └── cond1

For example:
    Hvo-analyse
    └── data_folder
        ├── H26 GQUAD
        │   ├── Test_Gullermo_2022-12-01
        │   │   ├── FOV1
        │   │   │   └── BG4
        │   │   │       └── fov1-dapi
        │   │   ├── FOV2
        │   │   │   └── BG4
        │   │   │       └── fov2-dapi
        │   │   └── FOV3
        │   │       └── BG4
        │   │           └── fov3-dapi
        │   └── Test_Gu_Untreated
        │       ├── FOV1
        │       │   └── BG4
        │       ├── FOV2
        │       │   └── BG4
        │       └── FOV3
        │           └── BG4
        └── strain_A
            ├── condition_A
            │   ├── fov_A
            │   │   ├── protein_A
            │   │   │   └── ROI1-DAPI
            │   │   └── protein_B
            │   │       └── ROI1-DAPI
            │   └── fov_B
            │       ├── protein_A
            │       │   └── ROI1-DAPI
            │       └── protein_B
            │           └── ROI1-DAPI
            └── condition_B
                ├── fov_A
                │   └── protein_B
                │       └── ROI1-DAPI
                └── fov_B
                    ├── protein_A
                    │   └── ROI1-DAPI
                    └── protein_B
                        └── ROI1-DAPI

"""
import os.path
from functools import cached_property, partial
from pathlib import Path
from typing import List, Optional

import albumentations
import numpy as np
import tifffile

from bioimageloader.base import Dataset


class Dorian(Dataset):
    """Dorian's data

    Parameters
    ----------
    root_dir : str
        Path to root directory
    transforms : albumentations.Compose, optional
        An instance of Compose (albumentations pkg) that defines augmentation in
        sequence.
    num_samples : int, optional
        Useful when ``transforms`` is set. Define the total length of the
        dataset. If it is set, it overwrites ``__len__``.
    exp : str, optional
        First parent
    cond : str, optional
        Second parent

    Notes
    -----
    - root_dir is "Hvo-analyse". It will search for "data_folder" in __init__()
    - I named ["H26 GQUAD", "strain_A"] ``exp``, plz find more appropriate name
    - I named ["condition_A", "condition_B"] ``cond``, plz find more appropriate
      name for this one too
    - No FOV selection for now, do you need it?

    Examples
    --------
    Method 3 will be the most useful one for napari integration

    Method 1
    >>> dataset = Dorian('Data/Dorian/Hvo-analyse')  # path to `root_dir`
    >>> print(dataset.exp_list)
    ['H26 GQUAD', 'strain_A']
    >>> print(dataset.cond_list)
    ['H26 GQUAD/Test_Gu_Untreated',
     'H26 GQUAD/Test_Gullermo_2022-12-01',
     'strain_A/condition_A',
     'strain_A/condition_B']
    >>> print(dataset.file_list)
    [PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV1/BG4/fov1 BG4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV1/BG4/fov1-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV2/BG4/fov2 BG4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV2/BG4/fov2-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV3/BG4/fov3 BG4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gu_Untreated/FOV3/BG4/fov3-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV1/BG4/fov1-G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV1/BG4/fov1-G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV1/BG4/fov1-dapi/fov1-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV2/BG4/fov2 G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV2/BG4/fov2 G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV2/BG4/fov2-dapi/fov2-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV3/BG4/fov3 G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV3/BG4/fov3 G4-dy755-vecta20pc_1_MMStack_Default.ome_DOM_dedrift.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/H26 GQUAD/Test_Gullermo_2022-12-01/FOV3/BG4/fov3-dapi/fov3-dapi_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif')]

    Method 2: initialize `exp` or `cond` (static way)
    >>> dataset = Dorian('Data/Dorian/Hvo-analyse', exp='strain_A')
    >>> print(dataset.cond_list)  # dynamic change depending on `exp`
    ['condition_A', 'condition_B']
    >>> print(dataset.file_list)
    [PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif')]

    Method 3: dynamic `exp` and `cond`
    >>> dataset = Dorian('Data/Dorian/Hvo-analyse')
    >>> dataset.exp = 'strain_A'
    >>> dataset.cond = 'condition_A'
    >>> print(dataset.file_list)
    [PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_A/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif')]
    >>> dataset.cond = 'condition_B'  # change `cond`
    >>> print(dataset.file_list)
    [PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_A/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_A/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/FOV1-DY755 vecta3_1_MMStack_Default.ome.tif'),
     PosixPath('Data/Dorian/Hvo-analyse/data_folder/strain_A/condition_B/fov_B/protein_B/ROI1-DAPI/ROI1-DAPI_MMStack_Default.ome.tif')]

    See Also
    --------
    MaskDataset : Super class
    DatasetInterface : Interface

    """
    # Set acronym
    acronym = 'Dorian'

    def __init__(
        self,
        root_dir: str,
        *,  # only keyword param
        transforms: Optional[albumentations.Compose] = None,
        num_samples: Optional[int] = None,
        # specific to this dataset
        cond: Optional[str] = None,
        exp: Optional[str] = None,
        **kwargs
    ):
        self._root_dir = os.path.join(root_dir, 'data_folder')
        self._transforms = transforms
        self._num_samples = num_samples
        # specific to this one here
        self._cond = cond
        self._exp = exp

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, val):
        self._exp = val
        if hasattr(self, 'file_list'):
            delattr(self, 'file_list')
        if hasattr(self, 'cond_list'):
            delattr(self, 'cond_list')

    @property
    def cond(self):
        return self._cond

    @cond.setter
    def cond(self, val):
        self._cond = val
        if hasattr(self, 'file_list'):
            delattr(self, 'file_list')

    def get_image(self, p: Path) -> np.ndarray:
        return tifffile.imread(p)

    @staticmethod
    def _fk_contain(p: Path, s: str):
        """filter key"""
        return s in p.as_posix()

    def _filter_file_list_with_keyword(self, file_list: List[Path], keyword: str) -> List[Path]:
        return list(filter(partial(self._fk_contain, s=keyword), self.file_list))

    @cached_property
    def file_list(self) -> List[Path]:
        # Important to decorate with `cached_property` in general
        _file_list = self.root_dir.rglob('*.tif')
        if self.exp is not None:
            _file_list = filter(partial(self._fk_contain, s=self.exp), _file_list)
        if self.cond is not None:
            _file_list = filter(partial(self._fk_contain, s=self.cond), _file_list)
        return sorted(_file_list)

    @cached_property
    def exp_list(self) -> List[str]:
        return [p.name for p in self.root_dir.glob('*')]

    @cached_property
    def cond_list(self) -> List[str]:
        if self.exp is not None:
            subdir = self.root_dir / self.exp
            return [p.relative_to(subdir).as_posix() for p in subdir.glob('*')]
        return [p.relative_to(self.root_dir).as_posix()
                for p in self.root_dir.glob('*/*')]
