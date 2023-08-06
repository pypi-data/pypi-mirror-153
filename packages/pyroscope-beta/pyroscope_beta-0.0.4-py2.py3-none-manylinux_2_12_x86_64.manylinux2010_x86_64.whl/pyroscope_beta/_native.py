# auto-generated file
__all__ = ['lib', 'ffi']

import os
from pyroscope_beta._native__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_native__lib.cpython-37m-x86_64-linux-gnu.so'), 2)
del os
