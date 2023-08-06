# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0

"""Code coverage measurement plugin for Python"""
import re
import codecs
from os import path

from setuptools import setup


classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Programming Language :: Python :: Implementation :: Jython",
    "Programming Language :: Python :: Implementation :: IronPython",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
]

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='exclude-until-coverage-plugin',
    version=find_version('src', 'exclude_until_coverage_plugin', 'exclude_until.py'),
    author='Hugh Sorby',
    author_email='h.sorby@auckland.ac.nz',
    packages=['exclude_until_coverage_plugin'],
    package_dir={'': 'src'},
    url='https://github.com/hsorby/exclude_until_coverage_plugin/',
    license='Apache Software License',
    description='Plugin for code coverage excluding lines until marker found.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    zip_safe=False,
    classifiers=classifiers,
    install_requires=['coverage >= 6.4.1']
)
