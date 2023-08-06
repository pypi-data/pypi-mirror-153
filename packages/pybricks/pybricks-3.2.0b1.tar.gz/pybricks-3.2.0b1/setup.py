# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['micropython',
 'pybricks',
 'pybricks.ev3dev',
 'pybricks.media',
 'uerrno',
 'uio',
 'umath',
 'urandom',
 'uselect',
 'usys']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybricks',
    'version': '3.2.0b1',
    'description': 'Documentation and user-API stubs for Pybricks MicroPython',
    'long_description': "Pybricks end-user API & Documentation\n=====================================\n\nThis repository documents the Pybricks end-user MicroPython API.\n\nEach `Pybricks firmware`_ comes with the `Pybricks package`_. All modules,\nclasses, methods, and functions in that package have optimized implementations\nin C for high performance and reduced memory footprint.\n\nThis repository provides an empty, pure Python blueprint of that package. It is\nused to generate the `official documentation`_.\nSee the `contributor's guide <CONTRIBUTING.md>`_ for acceptable changes and\ninstructions to build the documentation locally.\n\nFor general discussion, please visit the `support`_ issue tracker.\n\n.. _Pybricks package: pybricks\n.. _Pybricks firmware: https://github.com/pybricks/pybricks-micropython\n.. _official documentation: https://docs.pybricks.com/\n.. _support: https://github.com/pybricks/support/issues\n",
    'author': 'The Pybricks Authors',
    'author_email': 'dev@pybricks.com',
    'maintainer': 'Laurens Valk',
    'maintainer_email': 'laurens@pybricks.com',
    'url': 'https://pybricks.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
