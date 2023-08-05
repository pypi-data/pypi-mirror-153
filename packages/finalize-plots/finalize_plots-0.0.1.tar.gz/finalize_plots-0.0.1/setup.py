#!/usr/bin/env python

from setuptools import setup, find_packages
with open("README.md", 'r') as f:
    long_description = f.read()
    
setup(
    name='finalize_plots',
    version='0.0.1',
    python_requires='>3.6.0',
    description='essential on laptops',
    author='Frédéric Dux',
    author_email="duxfrederic@gmail.com",
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "opencv-python"
    ],
    download_url="https://github.com/duxfrederic/finalize_plot/archive/refs/tags/v0.0.1.tar.gz"
)

