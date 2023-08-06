import threading

import numpy as np


class Coordinates(np.ndarray):
    def __new__(cls, input_array):
        return np.asarray(input_array).view(cls)

    @property
    def x(self): return self[0]

    @x.setter
    def x(self, value): self[0] = value

    @property
    def y(self): return self[1]

    @y.setter
    def y(self, value): self[1] = value

    @property
    def z(self): return self[2]

    @z.setter
    def z(self, value): self[2] = value

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not (self == other)


class Size(np.ndarray):
    def __new__(cls, input_array):
        return np.asarray(input_array).view(cls)

    @property
    def width(self): return self[0]

    @width.setter
    def width(self, value): self[0] = value

    @property
    def height(self): return self[1]

    @height.setter
    def height(self, value): self[1] = value

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not (self == other)


def separate_thread(fn):
    def _fn(*args, **kwargs):
        thread = threading.Thread(target=lambda: fn(*args, **kwargs))
        thread.daemon = True
        thread.start()
    return _fn
