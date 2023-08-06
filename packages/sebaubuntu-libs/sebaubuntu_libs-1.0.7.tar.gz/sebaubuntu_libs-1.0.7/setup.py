# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sebaubuntu_libs',
 'sebaubuntu_libs.libaik',
 'sebaubuntu_libs.libandroid',
 'sebaubuntu_libs.libexception',
 'sebaubuntu_libs.libfstab',
 'sebaubuntu_libs.libgofile',
 'sebaubuntu_libs.libgofile.raw_api',
 'sebaubuntu_libs.liblineage',
 'sebaubuntu_libs.liblocale',
 'sebaubuntu_libs.liblogging',
 'sebaubuntu_libs.libnekobin',
 'sebaubuntu_libs.libprop',
 'sebaubuntu_libs.libreorder',
 'sebaubuntu_libs.libsed',
 'sebaubuntu_libs.libtyping',
 'sebaubuntu_libs.libvintf']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0']

setup_kwargs = {
    'name': 'sebaubuntu-libs',
    'version': '1.0.7',
    'description': "SebaUbuntu's shared libs",
    'long_description': '# sebaubuntu_libs\n\n[![PyPi version](https://img.shields.io/pypi/v/sebaubuntu_libs)](https://pypi.org/project/sebaubuntu_libs/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/383072c93d5b4fa293237d42360e2170)](https://www.codacy.com/gh/SebaUbuntu/sebaubuntu_libs/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/sebaubuntu_libs&amp;utm_campaign=Badge_Grade)\n\nA collection of code shared between my projects\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/sebaubuntu_libs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
