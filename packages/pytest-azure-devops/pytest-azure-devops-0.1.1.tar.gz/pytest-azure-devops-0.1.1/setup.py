#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-azure-devops',
    version='0.1.1',
    author='Francesc Elies',
    license='Mozilla Public License 2.0',
    url='https://github.com/FrancescElies/pytest-azure-devops',
    description=('Simplifies using azure devops parallel strategy '
                 '(https://docs.microsoft.com/en-us/azure/devops/pipelines/test/parallel-testing-any-test-runner) '
                 'with pytest.'),
    long_description=read('README.rst'),
    long_description_content_type="text/x-rst",
    py_modules=['pytest_azure_devops'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'pytest11': [
            'azure-devops = pytest_azure_devops',
        ],
    },
)
