from setuptools import find_packages, setup
from argparse import ArgumentParser
import os

name = "matplottikz"
version = "0.0.1"

setup(
    name=name,
    include_package_data=True,
    packages=find_packages(include=[name]),
    version=version,
    description='Generate tikz figures using python',
    author='Ryan Seah Meng Yong',
)