#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="seread",
    description="Script to read serial port and store to file/influxdb",
    url="http://gitlab.com/jaromrax/seread",
    author="jaromrax",
    author_email="jaromrax@gmail.com",
    license="GPL2",
#    version='__version__',
    version=get_version("seread/version.py"),
    packages=['seread'],
#    packagedata={'seread': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/seread'],
    install_requires = ['fire','influxdb','pyserial_asyncio','thread6','pantilthat'],
)
# pyserial_asyncio
