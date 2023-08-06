# Copyright (c) Vyoma Systems Private Limited
# See LICENSE.vyoma for details

from setuptools import setup, find_packages
import os

root = os.path.abspath(os.path.dirname(__file__))

def read_requires():
    with open(os.path.join(root, "reporg/requirements.txt"),"r") as reqfile:
        return reqfile.read().splitlines()

#Long Description
with open("README.rst", "r") as fh:
    readme = fh.read()

setup(
    name='reporg',
    version='1.0.3',
    description="Repo organizer",
    long_description=readme + '\n\n',
    classifiers=[
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    url='https://gitlab.com/riscv_verification/reporg',
    author="vsys",
    author_email='vsys2021@gmail.com',
    license="MIT license",
    packages=find_packages(),
    package_dir={'reporg': 'reporg'},
    package_data={
        'reporg': [
            'requirements.txt'
            ]
        },
    install_requires=read_requires(),
    python_requires='>=3.8.5',
    entry_points={
        'console_scripts': [
            'reporg=reporg.main:cli',
        ],
    },
    include_package_data=True,
    keywords='reporg',
    test_suite='tests',
    zip_safe=False,
)
