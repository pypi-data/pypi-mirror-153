import os
from setuptools import setup, Extension, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name='nf9',
	version='1.01',
	description='High level interface to SAOImageDS9 using pyds9()',
	url='https://github.com/npirzkal/GRISMCONF',
	author='Nor Pirzkal',
	author_email='npirzkal@mac.com',
    package_dir = {
        'nf9': 'nf9',
        },
    packages=["nf9"],
    install_requires=[
    "pyds9 > 1.8"],
)
