===================
py-devtools-builtin
===================

**Add devtools.debug() to python builtins**

.. image:: https://img.shields.io/badge/Maintenance%20Intended-✖-red.svg?style=flat-square
    :target: http://unmaintained.tech/
    :alt: Maintenance - not intended

.. image:: https://img.shields.io/github/license/Cielquan/py-devtools-builtin.svg?style=flat-square&label=License
    :target: https://github.com/Cielquan/py-devtools-builtin/blob/master/LICENSE.txt
    :alt: License

.. image:: https://img.shields.io/pypi/v/py-devtools-builtin.svg?style=flat-square&logo=pypi&logoColor=FBE072
    :target: https://pypi.org/project/py-devtools-builtin/
    :alt: PyPI - Package latest release

.. image:: https://img.shields.io/pypi/pyversions/py-devtools-builtin.svg?style=flat-square&logo=python&logoColor=FBE072
    :target: https://pypi.org/project/py-devtools-builtin/
    :alt: PyPI - Supported Python Versions

.. image:: https://img.shields.io/pypi/implementation/py-devtools-builtin.svg?style=flat-square&logo=python&logoColor=FBE072
    :target: https://pypi.org/project/py-devtools-builtin/
    :alt: PyPI - Supported Implementations

`python-devtools <https://github.com/samuelcolvin/python-devtools>`__ is a tool with
multiple debug functionality. As described in the
`docs <https://python-devtools.helpmanual.io/usage/#usage-without-import>`__ you can
add its toolset to the python builtins with a little trick. But instead of adding the
import to ``sitecustomize.py`` or ``usercustomize.py`` you can also write it to a
``*.py`` file in the ``site-packages`` directory and also add a ``*.pth`` file which
then imports the first file. This package does exactly that.

Simply install this package alongside ``devtools`` and you have its toolset available
without an explicit import::

    $ pip install devtools py-devtools-builtin

If you do not have ``devtools`` installed, ``py-devtools-builtin`` will installed it for you.
