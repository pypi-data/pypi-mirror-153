import filecmp
import pathlib
import shutil
import time

import numpy as np
from PIL import Image

from .util import Size


def open_image(image_file, max_attempts=3):
    '''
    Attempt to load at most *max_attempts* times, return None on failure.
    '''
    for _ in range(max_attempts):
        try:
            return Image.open(image_file).convert('RGBA')
        except OSError:
            time.sleep(0.01)
            continue


class ImageComparator:
    def __init__(self, left_file, right_file):
        self.left_file = left_file
        self.right_file = right_file

    def clear(self, what='all'):
        self._diff_info = None
        self._diff = None
        self._hcdiff = None
        if what in {'all', 'left'}:
            self._left = None
        if what in {'all', 'right'}:
            self._right = None

    @property
    def left_file(self):
        return self._left_file

    @left_file.setter
    def left_file(self, file):
        self.clear('left')
        self._left_file = pathlib.Path(file) if file else None

    @property
    def left(self):
        if self._left is None:
            if self._left_file.is_file():
                self._left = open_image(self._left_file)
        return self._left

    @property
    def right_file(self):
        return self._right_file

    @right_file.setter
    def right_file(self, file):
        self.clear('right')
        self._right_file = pathlib.Path(file) if file else None

    @property
    def right(self):
        if self._right is None:
            if self._right_file.is_file():
                self._right = open_image(self._right_file)
        return self._right

    @property
    def diff(self):
        if self._diff is None:
            if self.left and self.right:
                left_size = Size((self.left.width, self.left.height))
                left_data = np.array(self.left)
                right_size = Size((self.right.width, self.right.height))
                if left_size == right_size:
                    right_data = np.array(self.right)
                else:
                    right_image_scaled = self.right.resize(left_size)
                    right_data = np.array(right_image_scaled)

                data = np.abs(left_data.astype(int) - right_data)
                data = data.sum(axis=-1)
                data = data.clip(0x00, 0xff).astype(np.uint8)

                self._diff = Image.fromarray(data)
        return self._diff

    @property
    def diff_info(self):
        if self._diff_info is None:
            if self.left_file and self.left_file.is_file():
                if self.right_file and self.right_file.is_file():
                    if filecmp.cmp(self.left_file, self.right_file, shallow=False):
                        self._diff_info = 'identical'
                    else:
                        try:
                            left_size = Size((self.left.width, self.left.height))
                            right_size = Size((self.right.width, self.right.height))
                            if left_size != right_size:
                                self._diff_info = 'different-size'
                            else:
                                left_data = np.array(self.left)
                                right_data = np.array(self.right)
                                errors = (left_data.astype(int) - right_data)
                                normalized_rmse = np.sqrt(np.mean(np.square(errors))) / 0xff
                                self._diff_info = normalized_rmse
                        except:
                            self._diff_info = 'failed-to-load'
                else:
                    self._diff_info = 'missing'
            elif self.right_file and self.right_file.is_file():
                if self.right:
                    self._diff_info = 'new'
                else:
                    self._diff_info = 'failed-to-load'
            else:
                self._diff_info = 'not-found'
        return self._diff_info

    @property
    def high_contrast_diff(self):
        if self._hcdiff is None and self.diff:
            diff_data = np.array(self.diff)
            imhist, bins = np.histogram(diff_data, 0xff, density=True)
            cdf = imhist.cumsum()
            cdf = 0xff * cdf / cdf[-1]
            data = np.interp(diff_data, bins[:-1], cdf)
            data[diff_data == 0] = 0
            self._hcdiff = Image.fromarray(data)
        return self._hcdiff

    def copy_left_to_right(self):
        if self.left_file.is_file():
            self.right_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.left_file, self.right_file)
            self.clear('right')

    def copy_right_to_left(self):
        if self.right_file.is_file():
            self.left_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.right_file, self.left_file)
            self.clear('left')

    def delete_files(self):
        if self.right_file.is_file():
            self.right_file.unlink()
            self.clear('right')
        if self.left_file.is_file():
            self.left_file.unlink()
            self.clear('left')
