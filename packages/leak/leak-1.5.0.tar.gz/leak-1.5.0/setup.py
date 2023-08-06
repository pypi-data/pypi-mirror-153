# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leak']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'packaging>=21.3,<22.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['leak = leak.cli:cli']}

setup_kwargs = {
    'name': 'leak',
    'version': '1.5.0',
    'description': 'Show release information about packages on PyPI',
    'long_description': '## leak\n\n[![PyPI](https://img.shields.io/pypi/v/leak?style=flat-square)](https://pypi.org/project/leak/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/leak?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/leak?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/leak?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/leak?style=flat-square)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)\n![Unittests](https://github.com/bmwant/leak/actions/workflows/unittests.yml/badge.svg)\n\nShow info about package releases on PyPI.\n\nIf you need to install specific version of package it is useful to know all available versions to have a choice.\n\nJust run\n\n```bash\n$ leak <package_name>\n# e.g.\n$ leak pyramid\n```\n\nand you will see all releases and some useful statistic about package specified. It will show most recent version, most popular (with highest number of downloads) and some additional information.\n\n### How to install\n\nInstall using pip\n\n```bash\n$ pip install leak\n\n# or to make sure the proper interpreter is used\n$ python -m pip install leak\n```\n\nor upgrade existing version\n\n```bash\n$ pip install --upgrade leak\n\n# or with pip invoked as a module\n$ python -m pip install --upgrade leak\n$ leak --version\n```\n\n### Contribution\n\nSee [DEVELOP.md](https://github.com/bmwant/leak/blob/main/DEVELOP.md) to setup your local development environment and create pull request to this repository once new feature is ready.\n\n### Releases\n\nSee [CHANGELOG.md](https://github.com/bmwant/leak/blob/main/CHANGELOG.md) for the new features included within each release.\n\n### License\n\nDistributed under [MIT License](https://tldrlegal.com/license/mit-license).\n\n### Acknowledgement\n\n🇺🇦 🇺🇦 🇺🇦 We would also thank the Armed Forces of Ukraine for providing security to perform this work. This work has become possible only because of resilience and courage of the Ukrainian Army.\n',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bmwant/leak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
