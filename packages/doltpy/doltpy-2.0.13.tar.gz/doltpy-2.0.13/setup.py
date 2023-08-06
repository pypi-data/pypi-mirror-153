# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doltpy',
 'doltpy.cli',
 'doltpy.etl',
 'doltpy.shared',
 'doltpy.sql',
 'doltpy.sql.sync',
 'doltpy.types']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.3.18',
 'attrs==19.3.0',
 'decorator==4.4.2',
 'doltcli>=0.1.14,<0.2.0',
 'more-itertools>=8.6.0,<9.0.0',
 'mysql-connector-python>=8.0.20,<9.0.0',
 'numpy>=1.19.0',
 'packaging==20.4',
 'pandas>=1.0.5',
 'pluggy==0.13.1',
 'protobuf==3.12.2',
 'psutil==5.7.2',
 'pyarrow>=6.0.0',
 'pyparsing==2.4.7',
 'python-dateutil==2.8.1',
 'pytz==2021.3',
 'retry==0.9.2',
 'six==1.15.0',
 'wcwidth==0.2.5']

entry_points = \
{'console_scripts': ['dolt-load = doltpy.etl:dolt_loader_main',
                     'dolthub-load = doltpy.etl:dolthub_loader_main']}

setup_kwargs = {
    'name': 'doltpy',
    'version': '2.0.13',
    'description': 'A Python package for using Dolt database via Python.',
    'long_description': "## DoltPy\nThis is DoltPy, the Python API for [Dolt](https://github.com/dolthub/dolt). Python is the language of choice for data science and data engineering, and thus we thought it would be wise to publish an API for building automated workflows on top of Dolt and [DoltHub](https://www.dolthub.com/), a collaboration platform for Dolt databases.\n\n## Installation\nYou need to install Dolt, which is documented [here](https://docs.dolthub.com/introduction/installation). It's easy for *nix users:\n```\n$ sudo bash -c 'curl -L https://github.com/liquidata-inc/dolt/releases/latest/download/install.sh | sudo bash'\n```\nWe also distribute Dolt as a Homebrew formula:\n```\n$ brew install dolt\n```\nFinally, for Windows users our release page has `.zip` and `.msi` files.\n\nOnce Dolt is installed you can install Doltpy using `pip`:\n```\n$ pip install doltpy\n```\n\n## Overview\nDoltpy is broken up into modules. \n\n### `doltpy.cli`\nThis is the most important module. It effectively wraps the Dolt command-line-interface (CLI) that is exposed by the Go binary. The CLI is exposed more or less exactly as it is implemented, returning wrapper objects where appropriate.\n\nIt's implementation has moved to a separate repository [here](https://github.com/dolthub/doltcli)\n\n#### `doltpy.cli.read` and `doltpy.cli.write`\nThese modules provide basic read and write interfaces for reading and writing a variety of tabular data formats, including:\n- CSV files\n- `pandas.DataFrame`\n- columns, that is dictionaries of lists, i.e. `{'col': [...vals...], ...}`\n- rows, that is lists of dictionaries, i.e. `[{'col': val, ...}, ...]`\n\n### `doltpy.sql`\nThis module provides tools for interacting with Dolt via a Python based SQL connector. The most important class is `DoltSQLContext`, which has concrete subclasses `DoltSQLServerContext` and `DoltSQLEngineContext`. `DoltSQLServerContext` is for users that want to write Python scripts that use and manage the Dolt SQL Server instance as a child process. `DoltSQLEngineContext` is for users who want to interact with a remote Dolt SQL Server.\n\nThese classes have equivalents of the read and write functions in `doltpy.cli.read` and `doltpy.cli.write` for writing CSV files, `pandas.DataFrame` objects, rows, and columns.\n\n#### `doltpy.sql.sql_sync`\nThis package provides tools for syncing data to and from Dolt, and other relational databases. Currently there is support for MySQL, Postgres, and Oracle. You can find a more detailed description of how to use SQL Sync tools [here](https://docs.dolthub.com/guides/sql-sync).\n\n### `doltpy.etl`\nThis module provides a set of tools for scripting ETL/ELT workflows. At Liquidata we use it internally to push datasets onto DoltHub.\n\n## More Information\nAs alluded to above, you can find a more detailed description of Doltpy [here](https://docs.dolthub.com/guides/python/doltpy).\n",
    'author': 'Oscar Batori',
    'author_email': 'oscar@dolthub.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dolthub/doltpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
