from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize(
        'tree.pyx',
        language_level='3'
    )
)
