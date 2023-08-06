from functools import cached_property

from ..base import MaskDataset


class Minimal(MaskDataset):

    acronym = 'Minimal'

    def __init__(self, root_dir):
        self._root_dir = root_dir

    @cached_property
    def file_list(self) -> list:
        return list('abc')

    def get_image(self):
        ...
