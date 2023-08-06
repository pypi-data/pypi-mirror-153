# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['query_flow',
 'query_flow.parsers',
 'query_flow.utils',
 'query_flow.vizualizers',
 'tests',
 'tests.parsers',
 'tests.parsers.data.athena',
 'tests.parsers.data.postgres',
 'tests.vizualizers']

package_data = \
{'': ['*'],
 'tests.parsers.data.athena': ['parse/*', 'parse/detailed_example/*'],
 'tests.parsers.data.postgres': ['multi_parse/multiple_queries/*',
                                 'parse/detailed_example/*',
                                 'parse/identify_duplications/*',
                                 'parse/ineffective_operation/*',
                                 'parse/missing_records/*']}

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'query-flow',
    'version': '0.1.0',
    'description': 'A library for visualizing your Queries as Sankey-diagrams..',
    'long_description': '# QueryFlow\n\n\n[comment]: <> ([![pypi]&#40;https://img.shields.io/pypi/v/query-flow.svg&#41;]&#40;https://pypi.org/project/query-flow/&#41;)\n\n[comment]: <> ([![python]&#40;https://img.shields.io/pypi/pyversions/query-flow.svg&#41;]&#40;https://pypi.org/project/query-flow/&#41;)\n\n[comment]: <> ([![Build Status]&#40;https://github.com/eyaltrabelsi/query-flow/actions/workflows/dev.yml/badge.svg&#41;]&#40;https://github.com/eyaltrabelsi/query-flow/actions/workflows/dev.yml&#41;)\n\nQueryFlow, is a query visualization tool that provides insights into common problems in your SQL query.\nQueryFlow visualizes the query execution using the Sankey diagram, a technique that allows one to illustrate complex processes, with a focus on a single aspect or resource that you want to highlight.\nThis allow to tackle the following problems:\n\n* [Identifying missing records.](https://github.com/eyaltrabelsi/query-flow/blob/master/examples/Identifying%20the%20operation%20that%20caused%20the%20return%20of%20zero%20records%20.ipynb)\n* [Identifying Ineffective operations.](https://github.com/eyaltrabelsi/query-flow/blob/master/examples/Identifying%20Ineffective%20operations.ipynb)\n* [Identifying duplications in a query.](https://github.com/eyaltrabelsi/query-flow/blob/master/examples/Identifying%20duplications.ipynb)\n* Comparing optimizer planned metrics to actual metrics.\n* Identifying performance bottlenecks in a single query.\n* Identifying performance bottlenecks in multiple queries.\n\nCurrently QueryFlow support the following databases/data-engines:\n* Athena\n* PostgreSQL\n\n* Documentation: <https://eyaltrabelsi.github.io/query-flow>\n* GitHub: <https://github.com/eyaltrabelsi/query-flow>\n* PyPI: <https://pypi.org/project/query-flow/>\n* Free software: MIT\n\n\n## Installing #\nThe best way to install query-flow is:\n```\n$ pip install query-flow\n```\nIn case you want to use another way go to the [installation page.](https://eyaltrabelsi.github.io/query-flow/installation/)\n\n\n[comment]: <> (## Publications #)\n\n[comment]: <> (**Title**: Visualizing Database Execution Plans using)\n\n[comment]: <> (Sankey. **Authors**: Eyal Trabelsi/Ehud Gudes [<a href="link">pdf</a>])\n\n[comment]: <> (*Authors contributed equally to this paper.)\n',
    'author': 'Eyal Trabelsi',
    'author_email': 'eyaltrabelsi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyaltrabelsi/query-flow',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
