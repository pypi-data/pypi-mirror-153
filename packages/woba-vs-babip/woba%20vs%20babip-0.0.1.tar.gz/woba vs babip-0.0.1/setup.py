# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause

from setuptools import setup
import os

def get_long_description() -> str:

    readme_filepath = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_filepath) as f:
        return f.read()

DESCRIPTION = "mlb statistics tools"
NAME = 'woba vs babip'
AUTHOR = 'Shunto Nakamura'
AUTHOR_EMAIL = 's2022024@stu.musashino-u.ac.jp'
URL = 'https://github.com/shuntonakamura0602/ds_special'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/shuntonakamura0602/ds_special'
VERSION = '0.0.1'
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'pandas>=1.2.4',
    'matplotlib>=3.3.4',
]

EXTRAS_REQUIRE = {
}

PACKAGES = [
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Multimedia :: Graphics',
    'Framework :: Matplotlib',
]

with open('README.md', 'r') as fp:
    readme = fp.read()


setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=get_long_description(),
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )