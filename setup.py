from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("manage_catalog.pyx"), requires=['numpy', 'astropy', 'matplotlib']
)
