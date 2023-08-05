# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Osyris contributors (https://github.com/osyris-project/osyris)
import numpy as np
from .tools import bytes_to_human_readable


class Datagroup:
    def __init__(self, data=None, parent=None):
        self._container = {}
        self._parent = parent
        self._name = ""
        self.shape = None
        if data is not None:
            for key, array in data.items():
                self[key] = array

    def __iter__(self):
        return self._container.__iter__()

    def __len__(self):
        return self._container.__len__()

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._container[key]
        else:
            if isinstance(key, int):
                key = slice(key, key + 1, 1)
            d = self.__class__()
            for name, val in self.items():
                d[name] = val[key]
            return d

    def __setitem__(self, key, value):
        if len(value.shape) > 0:
            shape = value.shape[0]
        else:
            shape = 1
        if self.shape is None:
            self.shape = shape
        else:
            if self.shape != shape:
                raise RuntimeError(
                    "Size mismatch on element insertion. Item "
                    "shape is {} while container accepts shape {}.".format(
                        shape, self.shape))
        value.name = key
        value.parent = self
        self._container[key] = value

    def __delitem__(self, key):
        return self._container.__delitem__(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        output = "Datagroup: {} {}\n".format(self.name, self.print_size())
        for key, item in self.items():
            output += str(item) + "\n"
        return output

    def __eq__(self, other):
        if self.keys() != other.keys():
            return False
        for key, value in self.items():
            if all(value != other[key]):
                return False
        return True

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.__class__(data={key: array.copy() for key, array in self.items()})

    def copy(self):
        return self.__class__(data=self._container.copy())

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent_):
        self._parent = parent_

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_):
        self._name = name_

    def keys(self):
        return self._container.keys()

    def items(self):
        return self._container.items()

    def values(self):
        return self._container.values()

    def nbytes(self):
        return np.sum([item.nbytes for item in self.values()])

    def print_size(self):
        return bytes_to_human_readable(self.nbytes())

    def sortby(self, key):
        if key is not None:
            if isinstance(key, str):
                key = np.argsort(self[key]).values
            for var in self.keys():
                self[var] = self[var][key]

    def clear(self):
        self._container.clear()
        self.shape = None

    def get(self, key, default):
        return self._container.get(key, default)

    def pop(self, key):
        return self._container.pop(key)

    def update(self, d):
        for key, value in d.items():
            self[key] = value
