# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notionapimanager']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'notionapimanager',
    'version': '0.1.8',
    'description': 'Python package for consulting, creating and editing Notion databases',
    'long_description': '# Notion API Manager\n\nThis package implements a wrapper class around the official [Notion API](https://developers.notion.com/).\n\nIt makes it easier to read databases as [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and to create new registries.\n\nGitHub [repository](https://github.com/rubchume/NotionApiManager).\n\n[Documentation](https://notionapimanager.readthedocs.io/en/latest/).\n\n[PyPI](https://pypi.org/project/notionapimanager/).\n\n# Steps\n\n## Obtain a Notion integration token\n\nYou can do it following the instructions in this [PrettyStatic blog article](https://prettystatic.com/notion-api-python/).\n\n## Install package\n\nInstall package from [PyPI](https://pypi.org/project/notionapimanager/).\n```shell\npip install notionapimanager\n```\n\n## Basic usage of the NotionDatabaseApiManager class\nNote: in Notion, a _database_ is what in SQL we would call a _table_.\nHence, a Notion _database_ will be returned as a Pandas DataFrame instance.\n\n```python\nfrom notionapimanager.notion_database_api_manager import NotionDatabaseApiManager\nfrom notionapimanager.notion_property_encoder import PropertyValue\n\nintegration_token = "secret_example_integration_token_3147cefa7cd20d4s45677dfasd34"\ndatabase_id_1 = "cc147cefa7cd20d4841469ddbd4cd893"\ndatabase_id_2 = "cc147cef20d456461469ddbd4das4593"\n\nmanager = NotionDatabaseApiManager(integration_token, [database_id_1, database_id_2])\nmanager.connect()\n\n# Get database 1\nmanager.get_database(database_id_1)\n\n# Insert a new entry on the database 2\nmanager.create_page(\n    database_id_2,\n    [\n        PropertyValue("Property Name", "Property value"),\n    ]\n)\n```\n\n',
    'author': 'Ruben Chulia Mena',
    'author_email': 'rubchume@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rubchume/NotionApiManager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
