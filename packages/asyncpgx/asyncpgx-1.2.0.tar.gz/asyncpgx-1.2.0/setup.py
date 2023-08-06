# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncpgx', 'asyncpgx.tests']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.21,<0.26']

setup_kwargs = {
    'name': 'asyncpgx',
    'version': '1.2.0',
    'description': 'User-friendly extensions for asyncpg',
    'long_description': "# asyncpgx\n[![Build passed](https://img.shields.io/github/workflow/status/laukhin/asyncpgx/CI)](https://github.com/laukhin/asyncpgx/actions?query=workflow%3ACI)\n[![Test coverage](https://img.shields.io/codecov/c/github/laukhin/asyncpgx)](https://codecov.io/gh/laukhin/asyncpgx)\n[![Version](https://img.shields.io/pypi/v/asyncpgx)](https://pypi.org/project/asyncpgx/)\n\nExtensions for asyncpg.\n\nBased on the [asyncpg](https://github.com/MagicStack/asyncpg) and highly inspired by the [sqlx](https://github.com/jmoiron/sqlx) package\n\nThis package supports 3.6+ python versions\n\n## Setup\nUse `pip install asyncpgx`\n\n## Purpose\nThis is a thin wrapper on the `asyncpg` package.\nOur purpose is to provide convenient extensions to the original package.\nWe're trying to delegate as much work as we can to the asyncpg (basically our extension methods are high-level proxies to the underlying ones)\nand make only converting job.\nOriginal asyncpg API stays the same, you can see it in the [asyncpg documentation](https://magicstack.github.io/asyncpg/current/).\n\n## Functionality\n* queries with named parameters, i.e.\n```python\nimport asyncpgx\n\nconnection = await asyncpgx.connect('postgresql://127.0.0.1:5432')\nawait connection.named_fetch('''SELECT field FROM some_table WHERE id <= :id;''', {'id': 1})\n```\n* prepared statements with named parameters, i.e.\n```python\nimport asyncpgx\n\nconnection = await asyncpgx.connect('postgresql://127.0.0.1:5432')\nprepared_statement = await connection.named_prepare('''SELECT field FROM some_table WHERE id <= :id;''')\nawait prepared_statement.named_fetch({'id': 1})\n```\n\n## Documentation\nYou can find project documentation [here](https://laukhin.github.io/asyncpgx/index.html)\n\n## Changelog\nYou can find all releases description [here](https://github.com/laukhin/asyncpgx/releases)\n",
    'author': 'Vladislav Laukhin',
    'author_email': 'laukhin97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laukhin/asyncpgx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<=3.10',
}


setup(**setup_kwargs)
