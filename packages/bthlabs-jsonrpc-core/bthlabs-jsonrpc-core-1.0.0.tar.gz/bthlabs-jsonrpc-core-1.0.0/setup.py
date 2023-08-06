# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bthlabs_jsonrpc_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bthlabs-jsonrpc-core',
    'version': '1.0.0',
    'description': 'BTHLabs JSONRPC - Core',
    'long_description': 'bthlabs-jsonrpc-core\n====================\n\nExtensible framework for Python JSONRPC implementations.\n\n`Docs`_ | `Source repository`_\n\nOverview\n--------\n\nBTHLabs JSONRPC is a set of Python libraries that provide extensible framework\nfor adding JSONRPC interfaces to existing Python Web applications.\n\nThe *core* package acts as a foundation for framework-specific integrations.\n\nIntegrations\n------------\n\nBTHLabs JSONRPC provides integration packages for specific Web frameworks.\n\n**Django**\n\nDjango integration is provided by ``bthlabs-jsonrpc-django`` package.\n\n+-------------------+-----------------------------------------------------+\n| PyPI              | https://pypi.org/project/bthlabs-jsonrpc-django/    | \n+-------------------+-----------------------------------------------------+\n| Docs              | https://projects.bthlabs.pl/bthlabs-jsonrpc/django/ |\n+-------------------+-----------------------------------------------------+\n| Source repository | https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/ |\n+-------------------+-----------------------------------------------------+\n\n**aiohttp**\n\naiohttp integration is provided by ``bthlabs-jsonrpc-aiohttp`` package.\n\n+-------------------+------------------------------------------------------+\n| PyPI              | https://pypi.org/project/bthlabs-jsonrpc-aiohttp/    |\n+-------------------+------------------------------------------------------+\n| Docs              | https://projects.bthlabs.pl/bthlabs-jsonrpc/aiohttp/ |\n+-------------------+------------------------------------------------------+\n| Source repository | https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/  |\n+-------------------+------------------------------------------------------+\n\nAuthor\n------\n\n*bthlabs-jsonrpc-core* is developed by `Tomek Wójcik`_.\n\nLicense\n-------\n\n*bthlabs-jsonrpc-core* is licensed under the MIT License.\n\n.. _Docs: https://projects.bthlabs.pl/bthlabs-jsonrpc/core/\n.. _Source repository: https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/\n.. _Tomek Wójcik: https://www.bthlabs.pl/\n',
    'author': 'Tomek Wójcik',
    'author_email': 'contact@bthlabs.pl',
    'maintainer': 'BTHLabs',
    'maintainer_email': 'contact@bthlabs.pl',
    'url': 'https://projects.bthlabs.pl/bthlabs-jsonrpc/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
