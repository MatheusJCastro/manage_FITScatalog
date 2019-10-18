import ctypes
import os
import matplotlib.pyplot as plt


c_lib = ctypes.cdll.LoadLibrary(os.path.abspath("./test.so"))
c_lib.main.restype = ctypes.c_int
# c_lib.main.argtypes = (None)
c_lib.main()

