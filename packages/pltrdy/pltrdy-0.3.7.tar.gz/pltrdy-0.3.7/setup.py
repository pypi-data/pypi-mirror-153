#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    path = os.path.join(os.path.dirname(__file__), 'pltrdy', '__init__.py')
    with open(path, 'r') as f:
        content = f.read()
    m = re.search(r'__version__\s*=\s*"(.+)"', content)
    assert m is not None
    return m.group(1)


setup(
    name='pltrdy',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=get_version(),
    packages=find_packages(),
    project_urls={
    },
    install_requires=[
        "pytz",
    ],
    entry_points={
        "console_scripts": [
            "gen_py=pltrdy.gen_script:main"
        ],
    }
)
