#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# to combine autotools and setuptools, see:
# https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html
# Thank you!

import os
import glob
from setuptools import setup
from setuptools.command.install import install as _install
from babel.messages import frontend as babel

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

def get_langs():
    return [os.path.basename(x).replace('.po', '') for x in glob.iglob('po/*.po')]

setup(
    name = "Armadito antivirus indicator",
    version = "0.10.0",
    author = "François Déchelle",
    author_email = "fdechelle@teclib.com",
    description = ("Application indicator for the Armadito antivirus"),
    license = "GPLv3",
    keywords = "antivirus indicator",
    url = "https://github.com/armadito/armadito-systray-ui",
    long_description = read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv3 License",
    ],
    setup_requires = ['babel'],
    packages = ['armadito'],
    scripts = ['bin/indicator-armadito'],
    data_files = [('share/icons/hicolor/scalable/apps', ['icons/scalable/indicator-armadito-dark.svg',
                                                         'icons/scalable/indicator-armadito-desactive.svg',
                                                         'icons/scalable/indicator-armadito-down.svg',
                                                         'icons/scalable/indicator-armadito-missing.svg',
                                                         'icons/scalable/indicator-armadito.svg']),
    ],
)

#
#
# reminder: for user local installation
# ./setup.py install --user
# ./setup.py install_data --install-dir=/home/fdechelle/.local
#
#
