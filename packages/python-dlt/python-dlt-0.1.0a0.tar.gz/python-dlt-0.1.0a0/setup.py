# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt',
 'dlt.common',
 'dlt.common.configuration',
 'dlt.common.storages',
 'dlt.dbt_runner',
 'dlt.extractors',
 'dlt.extractors.generator',
 'dlt.loaders',
 'dlt.loaders.dummy',
 'dlt.loaders.gcp',
 'dlt.loaders.redshift',
 'dlt.pipeline',
 'dlt.unpacker']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'hexbytes>=0.2.2,<0.3.0',
 'json-logging==1.4.1rc0',
 'jsonlines>=2.0.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'requests>=2.26.0,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.4.3,<2.0.0',
 'simplejson>=3.17.5,<4.0.0']

extras_require = \
{'dbt': ['GitPython[dbt]>=3.1.26,<4.0.0',
         'dbt-core[dbt]==1.0.6',
         'dbt-redshift[dbt]==1.0.1',
         'dbt-bigquery[dbt]==1.0.0'],
 'gcp': ['grpcio==1.43.0', 'google-cloud-bigquery>=2.26.0,<3.0.0'],
 'postgres': ['psycopg2-binary>=2.9.1,<3.0.0'],
 'redshift': ['psycopg2-binary>=2.9.1,<3.0.0']}

setup_kwargs = {
    'name': 'python-dlt',
    'version': '0.1.0a0',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': '![](docs/DLT-Pacman-Big.gif)\n\n<p align="center">\n\n[![PyPI version](https://badge.fury.io/py/python-dlt.svg)](https://pypi.org/project/python-dlt/)\n[![LINT Badge](https://github.com/scale-vector/dlt/actions/workflows/lint.yml/badge.svg)](https://github.com/scale-vector/dlt/actions/workflows/lint.yml)\n\n</p>\n\n# DLT\nDLT enables simple python-native data pipelining for data professionals.\n\nDLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.\n\n## [Quickstart guide](QUICKSTART.md)\n\n## How does it work?\n\nDLT aims to simplify data loading for everyone.\n\n\nTo achieve this, we take into account the progressive steps of data pipelining:\n\n![](docs/DLT_Diagram_1.jpg)\n### 1. Data discovery, typing, schema, metadata\n\nWhen we create a pipeline, we start by grabbing data from the source.\n\nUsually, the source metadata is lacking, so we need to look at the actual data to understand what it is and how to ingest it.\n\nIn order to facilitate this, DLT includes several features\n* Auto-unpack nested json if desired\n* generate an inferred schema with data types and load data as-is for inspection in your warehouse.\n* Use an ajusted schema for follow up loads, to better type and filter your data after visual inspection (this also solves dynamic typing of Pandas dfs)\n\n### 2. Safe, scalable loading\n\nWhen we load data, many things can intrerupt the process, so we want to make sure we can safely retry without generating artefacts in the data.\n\nAdditionally, it\'s not uncommon to not know the data size in advance, making it a challenge to match data size to loading infrastructure.\n\nWith good pipelining design, safe loading becomes a non-issue.\n\n* Idempotency: The data pipeline supports idempotency on load, so no risk of data duplication.\n* Atomicity: The data is either loaded, or not. Partial loading occurs in the s3/storage buffer, which is then fully committed to warehouse/catalogue once finished. If something fails, the buffer is not partially-commited further.\n* Data-size agnostic: By using generators (like incremental downloading) and online storage as a buffer, it can incrementally process sources of any size without running into worker-machine size limitations.\n\n\n### 3. Modelling and analysis\n\n* Instantiate a dbt package with the source schema, enabling you to skip the dbt setup part and go right to SQL modelling.\n\n\n### 4. Data contracts\n\n* If using an explicit schema, you are able to validate the incoming data against it. Particularly useful when ingesting untyped data such as pandas dataframes, json from apis, documents from nosql etc.\n\n### 5. Maintenance & Updates\n\n* Auto schema migration: What do you do when a new field appears, or if it changes type? With auto schema migration you can default to ingest this data, or throw a validation error.\n\n## Why?\n\nData loading is at the base of the data work pyramid.\n\nThe current ecosystem of tools follows an old paradigm where the data pipeline creator is a software engineer, while the data pipeline user is an analyst.\n\nIn the current world, the data analyst needs to solve problems end to end, including loading.\n\nCurrently there are no simple frameworks to achieve this, but only clunky applications that need engineering and devops expertise to run, install, manage and scale. The reason for this is often an artificial monetisation insert (open source but pay to manage).\n\nAdditionally, these existing loaders only load data sources for which somebody developed an extractor, requiring a software developer once again.\n\nDLT aims to bring loading into the hands of analysts with none of the unreasonable redundacy waste of the modern data platform.\n\nAdditionally, the source schemas will be compatible across the community, creating the possiblity to share reusable analysis and modelling back to the open source community without creating tool-based vendor locks.\n\n\n\n\n\n',
    'author': 'ScaleVector',
    'author_email': 'services@scalevector.ai',
    'maintainer': 'Marcin Rudolf',
    'maintainer_email': 'marcin@scalevector.ai',
    'url': 'https://github.com/scale-vector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
