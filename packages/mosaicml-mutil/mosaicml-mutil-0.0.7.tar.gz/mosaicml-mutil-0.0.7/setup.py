""" Copyright 2022 MosaicML. All Rights Reserved. """

import os

import setuptools
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# pylint: disable-next=exec-used,consider-using-with
exec(open('mutil/version.py', 'r', encoding='utf-8').read())

install_requires = [
    # 'mcli==0.1.0a1',
]

extra_deps = {}


def package_files(directory: str):
    # from https://stackoverflow.com/a/36693250
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name='mosaicml-mutil',
    version=__version__,  # type: ignore pylint: disable=undefined-variable
    author='MosaicML',
    author_email='team@mosaicml.com',
    description='Util for stuff',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mosaicml/mutil',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['mutil = mutil.cli:main',],
    },
    extras_require=extra_deps,
    python_requires='>=3.8',
    ext_package='mutil',
)
