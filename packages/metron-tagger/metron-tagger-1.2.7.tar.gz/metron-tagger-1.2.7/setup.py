# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metrontagger']

package_data = \
{'': ['*']}

install_requires = \
['darkseid>=1.2.0,<2.0.0',
 'mokkari>=2.1.0,<3.0.0',
 'questionary>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['metron-tagger = metrontagger.cli:main']}

setup_kwargs = {
    'name': 'metron-tagger',
    'version': '1.2.7',
    'description': 'A program to write metadata from metron.cloud to a comic archive',
    'long_description': "=============\nMetron-Tagger\n=============\n\n.. image:: https://img.shields.io/pypi/v/metron-tagger.svg\n    :target: https://pypi.org/project/metron-tagger/\n\n.. image:: https://img.shields.io/pypi/pyversions/metron-tagger.svg\n    :target: https://pypi.org/project/metron-tagger/\n\n.. image:: https://img.shields.io/github/license/bpepple/metron-tagger\n    :target: https://opensource.org/licenses/GPL-3.0\n\n.. image:: https://codecov.io/gh/bpepple/metron-tagger/branch/master/graph/badge.svg?token=d8TyzWM2Uz\n    :target: https://codecov.io/gh/bpepple/metron-tagger\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\nQuick Description\n-----------------\n\nA command-line tool to tag comic archives with metadata from metron.cloud_.\n\n.. _metron.cloud: https://metron.cloud\n\nInstallation\n------------\n\nPyPi\n~~~~\n\nOr install it yourself:\n\n.. code:: bash\n\n  $ pip install --user metron-tagger\n\nGitHub\n~~~~~~\n\nInstalling the latest version from Github:\n\n.. code:: bash\n\n  $ git clone https://github.com/bpepple/metron-tagger.git\n  $ cd metron-tagger\n  $ python3 setup.py install\n\nFAQ\n---\n\n**Why no .cbr (rar) support?**\n\n- I'm not aware of any provider (Comixology, Humble Bundle, DriveThru Comics, etc.) of legally downloadable DRM-free comics that use the rar format.\n- It's a non-free software file format.\n- It is trivial to convert to cbz (zip) format.\n\nHelp\n----\n\n::\n\n    usage: metron-tagger [-h] [-r] [-o] [--id ID] [-d] [--ignore-existing]\n                         [--missing] [-u USER] [-p PASSWORD] [--set-metron-user]\n                         [-s] [--sort-dir SORT_DIR] [--set-sort-dir] [--version]\n                         path [path ...]\n\n    Read in a file or set of files, and return the result.\n\n    positional arguments:\n        path                  Path of a file or a folder of files.\n\n    optional arguments:\n        -h, --help            show this help message and exit\n        -r, --rename          Rename comic archive from the files metadata. (default: False)\n        -o, --online          Search online and attempt to identify comic archive. (default: False)\n        --id ID               Identify file for tagging with the Metron Issue Id. (default: None)\n        -d, --delete          Delete the metadata tags from the file. (default: False)\n        --ignore-existing     Ignore files that have existing metadata tag. (default: False)\n        --missing             List files without metadata. (default: False)\n        -u USER, --user USER  Metron user identity (default: None)\n        -p PASSWORD, --password PASSWORD\n                              Metron user password (default: None)\n        --set-metron-user     Save the Metron user settings (default: False)\n        -s, --sort            Sort files that contain metadata tags. (default: False)\n        --sort-dir SORT_DIR   Directory wher files should be sorted to. This should\n                              not have a trailing path serparator. (default: None)\n        --set-sort-dir        Set the directory where files should be sorted. (default: False)\n        --version             Show the version number and exit\n\nBugs/Requests\n-------------\n\nPlease use the `GitHub issue tracker <https://github.com/bpepple/metron-tagger/issues>`_ to submit bugs or request features.\n\nLicense\n-------\n\nThis project is licensed under the `GPLv3 License <LICENSE>`_.\n\n",
    'author': 'Brian Pepple',
    'author_email': 'bdpepple@gmail.com',
    'maintainer': 'Brian Pepple',
    'maintainer_email': 'bdpepple@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
