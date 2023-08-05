# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Osyris contributors (https://github.com/osyris-project/osyris)

from .map import map as _map
import warnings


def plane(*args, **kwargs):
    """
    Old deprecated alias for think map, will be removed soon.
    """
    warnings.warn("The plane function is deprecated and will be removed soon, "
                  "use map instead.")
    return _map(*args, dz=None, **kwargs)
