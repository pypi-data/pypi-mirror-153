#!/usr/bin/python3
import io
import os
from petra_viewer.version import __version__

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'petra_viewer'
DESCRIPTION = 'Simple viewer of data, acquired by xray-detectors at PETRA3'
EMAIL = 'yury.matveev@desy.de'
AUTHOR = 'Yury Matveyev'
REQUIRES_PYTHON = '>=3.7'

# What packages are required for this module to be executed?
REQUIRED = [
    'attrs', 'pyqtgraph >= 0.11', 'psutil', 'numpy', 'scipy', 'h5py >= 2.5', 'python-dateutil'
]

EXTRA_REQUIRED = {'ASAPO': ['hdf5plugin'],
                  'CONVERTER': ['xrayutilities'],
                  'SILX': ['silx'],
                  '3D': ['PyOpenGL']
                  }

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
about['__version__'] = __version__

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_dir={'petra_viewer': 'petra_viewer',},
    package_data={'petra_viewer': ['petra_viewer/*.py', 'petra_viewer/*.ini'],},
    install_requires=REQUIRED,
    extras_require=EXTRA_REQUIRED,
    include_package_data=True,
    license='GPLv3',
    entry_points={'console_scripts': ['petra_viewer = petra_viewer:main',],},
    scripts=['petra_viewer/petra_viewer.sh'],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 3 - Alpha'
    ],
)
