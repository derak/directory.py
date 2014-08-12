#!/usr/bin/env python

from distutils.core import setup


def read(filename):
    return open(filename).read()

setup(name="directory",
      version="0.0.1",
      description="LDAP Directory Management, wrapper for python-ldap (http://www.python-ldap.org). This module provides high level control over an LDAP Directory.",
      long_description=read("README.md"),
      author="Derak Berreyesa",
      author_email="derak.berreyesa@gmail.com",
      maintainer="Derak Berreyesa",
      maintainer_email="derak.berreyesa@gmail.com",
      url="https://github.com/derak/directory.py",
      download_url="https://github.com/derak/directory.py",
      classifiers=("Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2.6",
                   "Programming Language :: Python :: 2.7"),
      license=read("LICENSE"),
      py_modules=['directory'],
      )
