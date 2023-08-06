from setuptools import setup, find_packages

setup(
    name ="multiplicationMatrix_Tese",
    version = '0.0.3',
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
    long_description = open("README.txt").read() + '\n\n' + open("CHANGELOG.txt").read(),
    install_requires = [
        'numpy',
        'scipy',
        'cupy-cuda112',
    ],
)