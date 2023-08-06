# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/py-devtools-builtin'}

packages = \
['py-devtools-builtin']

package_data = \
{'': ['*']}

install_requires = \
['devtools[pygments]']

setup_kwargs = {
    'name': 'py-devtools-builtin',
    'version': '1.1.0',
    'description': 'Add devtools.debug() to python builtins',
    'long_description': '===================\npy-devtools-builtin\n===================\n\n**Add devtools.debug() to python builtins**\n\n.. image:: https://img.shields.io/badge/Maintenance%20Intended-✖-red.svg?style=flat-square\n    :target: http://unmaintained.tech/\n    :alt: Maintenance - not intended\n\n.. image:: https://img.shields.io/github/license/Cielquan/py-devtools-builtin.svg?style=flat-square&label=License\n    :target: https://github.com/Cielquan/py-devtools-builtin/blob/master/LICENSE.txt\n    :alt: License\n\n.. image:: https://img.shields.io/pypi/v/py-devtools-builtin.svg?style=flat-square&logo=pypi&logoColor=FBE072\n    :target: https://pypi.org/project/py-devtools-builtin/\n    :alt: PyPI - Package latest release\n\n.. image:: https://img.shields.io/pypi/pyversions/py-devtools-builtin.svg?style=flat-square&logo=python&logoColor=FBE072\n    :target: https://pypi.org/project/py-devtools-builtin/\n    :alt: PyPI - Supported Python Versions\n\n.. image:: https://img.shields.io/pypi/implementation/py-devtools-builtin.svg?style=flat-square&logo=python&logoColor=FBE072\n    :target: https://pypi.org/project/py-devtools-builtin/\n    :alt: PyPI - Supported Implementations\n\n`python-devtools <https://github.com/samuelcolvin/python-devtools>`__ is a tool with\nmultiple debug functionality. As described in the\n`docs <https://python-devtools.helpmanual.io/usage/#usage-without-import>`__ you can\nadd its toolset to the python builtins with a little trick. But instead of adding the\nimport to ``sitecustomize.py`` or ``usercustomize.py`` you can also write it to a\n``*.py`` file in the ``site-packages`` directory and also add a ``*.pth`` file which\nthen imports the first file. This package does exactly that.\n\nSimply install this package alongside ``devtools`` and you have its toolset available\nwithout an explicit import::\n\n    $ pip install devtools py-devtools-builtin\n\nIf you do not have ``devtools`` installed, ``py-devtools-builtin`` will installed it for you.\n',
    'author': 'Cielquan',
    'author_email': 'cielquan@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cielquan/py-devtools-builtin',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
