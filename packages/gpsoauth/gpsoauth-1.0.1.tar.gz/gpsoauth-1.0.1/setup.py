# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpsoauth']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodomex>=3.0', 'requests>=2.0.0']

setup_kwargs = {
    'name': 'gpsoauth',
    'version': '1.0.1',
    'description': 'A python client library for Google Play Services OAuth.',
    'long_description': '# gpsoauth\n\n[![CI](https://github.com/simon-weber/gpsoauth/actions/workflows/ci.yaml/badge.svg)](https://github.com/simon-weber/gpsoauth/actions/workflows/ci.yaml)\n[![PyPI version](https://badge.fury.io/py/gpsoauth.svg)](https://pypi.org/project/gpsoauth/)\n[![repominder](https://img.shields.io/badge/dynamic/json.svg?label=release&query=%24.status&maxAge=43200&uri=https%3A%2F%2Fwww.repominder.com%2Fbadge%2FeyJmdWxsX25hbWUiOiAic2ltb24td2ViZXIvZ3Bzb2F1dGgifQ%3D%3D%2F&link=https%3A%2F%2Fwww.repominder.com%2F)](https://www.repominder.com)\n\n**Python client library for Google Play Services OAuth.**\n\n`gpsoauth` allows python code to use the "master token" flow that KB Sriram described at\n<http://sbktech.blogspot.com/2014/01/inside-android-play-services-magic.html>.\n\nThis can be useful when writing code that poses as a Google app, like\n[gmusicapi does here](https://github.com/simon-weber/gmusicapi/blob/87a802ab3a59a7fa2974fd9755d59a55275484d9/gmusicapi/session.py#L267-L278).\n\nMany thanks to Dima Kovalenko for reverse engineering the EncryptedPasswd signature in\n<https://web.archive.org/web/20150814054004/http://codedigging.com/blog/2014-06-09-about-encryptedpasswd/>.\n\nFor an explanation of recent changes, see [the changelog](https://github.com/simon-weber/gpsoauth/blob/master/CHANGELOG.md).\n\n## Ports\n\n- C\\#: <https://github.com/vemacs/GPSOAuthSharp>\n- Ruby: <https://github.com/bryanmytko/gpsoauth>\n- Java: <https://github.com/svarzee/gpsoauth-java>\n- C++: <https://github.com/dvirtz/gpsoauth-cpp> and <https://github.com/Iciclelz/gpsoauthclient>\n\n## Contributing\n\nSee [Contributing guidelines](https://github.com/simon-weber/gpsoauth/blob/master/CONTRIBUTING.md).\nThis is an open-source project and all countributions are highly welcomed.\n',
    'author': 'Simon Weber',
    'author_email': 'simon@simonmweber.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simon-weber/gpsoauth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
