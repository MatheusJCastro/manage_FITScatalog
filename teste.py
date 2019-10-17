import ctypes
import os

def matplot():
    import matplotlib.pyplot as plt


def c():
    c_lib = ctypes.cdll.LoadLibrary(os.path.abspath("test.so"))
    c_lib.python_script.restype = ctypes.c_int
    # c_lib.main.argtypes = (None)
    c_lib.python_script()


if __name__ == '__main__':
    c()
