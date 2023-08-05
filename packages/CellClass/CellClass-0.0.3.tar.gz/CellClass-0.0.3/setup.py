from setuptools import setup, find_packages
import os

def parse_requirements():
    with open("requirements.txt", "r") as r:
        lines = r.readlines()
        lines = [l.strip() for l in lines if not "MapMet" in l]
        return lines

# must be changed before upload
VERSION = '0.0.3'
DESCRIPTION = 'CellClass'
LONG_DESCRIPTION = ''

setup(
    name="CellClass",
    version=VERSION,
    author="Simon Gutwein",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires = parse_requirements(),
    keywords=['python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)

