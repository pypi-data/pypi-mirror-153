# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fondat']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.16,<0.17',
 'iso8601>=0.1,<0.2',
 'multidict>=5.2,<6.0',
 'wrapt>=1.13,<2.0']

setup_kwargs = {
    'name': 'fondat',
    'version': '4.0a1',
    'description': 'A foundation for resource-oriented backend applications.',
    'long_description': '# fondat\n\n[![PyPI](https://img.shields.io/pypi/v/fondat)](https://pypi.org/project/fondat/)\n[![Python](https://img.shields.io/pypi/pyversions/fondat)](https://python.org/)\n[![GitHub](https://img.shields.io/badge/github-main-blue.svg)](https://github.com/fondat/fondat/)\n[![Test](https://github.com/fondat/fondat/workflows/test/badge.svg)](https://github.com/fondat/fondat/actions?query=workflow/test)\n[![License](https://img.shields.io/github/license/fondat/fondat.svg)](https://github.com/fondat/fondat/blob/main/LICENSE)\n\nA foundation for resource-oriented backend applications.\n\n## Introduction\n\nFondat is a foundation for resource-oriented backend applications in Python.\n\n## Install\n\n```\npip install fondat\n```\n\n## Develop\n\n```\npoetry install\npoetry run pre-commit install\n```\n\n## Test\n\n```\npoetry run pytest\n```',
    'author': 'fondat authors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fondat/fondat/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
