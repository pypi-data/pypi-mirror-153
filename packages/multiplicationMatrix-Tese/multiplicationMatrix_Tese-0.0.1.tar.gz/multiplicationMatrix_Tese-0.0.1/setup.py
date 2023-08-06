from setuptools import setup, find_packages

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name ="multiplicationMatrix_Tese",
    version = '0.0.1',
    description = 'Basic multuplication!',
    py_modules = ["multiplicationMatrix_Tese"],
    package_dir = {'': 'src'},
    author = "Joao Rodrigues",
    author_email = "joao_manuel1999@hotmail.com",
    classifiers = [
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Environment :: GPU :: NVIDIA CUDA :: 11.2",
    ],
    long_description = long_description,
    install_requires = [
        'numpy',
        'scipy',
        'cupy-cuda112',
    ],
)