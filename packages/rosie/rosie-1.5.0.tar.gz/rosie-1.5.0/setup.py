from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.sdist import sdist
from distutils.command.build import build
from distutils.command.clean import clean
import subprocess, os, sys, shutil

ROSIE_VERSION = '1.3.0'
TAG = 'v' + ROSIE_VERSION

setup(
    name="rosie",
    # The version of THIS PYTHON PACKAGE (independent of Rosie version):
    version="1.5.0",

    include_package_data=True,

    packages = ['rosie'],

    install_requires=['cffi >= 1.9'],

    # metadata for upload to PyPI
    author="Jenna Shockley, Jamie A. Jennings",
    author_email="rosie.pattern.language@gmail.com",
    description="Rosie Pattern Language (replaces regex for data mining and text search)",

    long_description="""
Prerequisites:
    Rosie installation (see https://gitlab.com/rosie-pattern-language/rosie)

Rosie and the Rosie Pattern Language (RPL)

RPL expressions are patterns for matching text, similar to regex but
more powerful.  You can use RPL for text pattern matching the way you
might use PCRE or regex in Perl, Python, or Java.  Unlike regex, RPL
is readable and maintainable, and packages of rpl are easily shared.

The Rosie project provides a library so you can use RPL from a variety
of programming languages.  We also provide an interactive read-eval-
print loop for pattern development and debugging, and an RPL compiler.
The Rosie matching engine is very small and reasonably fast.

Rosie's home page:
  https://rosie-lang.org

The repository of record for the Rosie project is located at:
  https://gitlab.com/rosie-pattern-language/rosie

Open issues are at:
  https://gitlab.com/rosie-pattern-language/rosie/issues

Before opening an issue with a bug report or an enhancement request,
please check the current open issues.
""",

    license="MIT",
    keywords="rosie pattern language PEG regex regexp data mining text search",
    url="https://rosie-lang.org",
    project_urls={
        "Issue page": "https://gitlab.com/rosie-pattern-language/rosie/issues",
        "Documentation": "https://gitlab.com/rosie-pattern-language/rosie/tree/master/doc",
        "Source Code": "https://gitlab.com/rosie-pattern-language",
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
    ],

    zip_safe=False,
)
