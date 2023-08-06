# auto-generated file
__all__ = ['lib', 'ffi']

import os
from pyroscope_beta._native__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_native__lib.cpython-39-darwin.so'), 130)
del os
