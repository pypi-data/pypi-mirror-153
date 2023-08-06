# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==1.8.2', 'sqlparse==0.4.2']

setup_kwargs = {
    'name': 'odd-models',
    'version': '2.0.0',
    'description': 'Open Data Discovery Models',
    'long_description': "# Open Data Discovery Models Package\n\n## Models\nYou can use odd pydantic models:\n```python\nfrom odd_models.models import DataEntityList\n\ndata_entity_list = DataEntityList(data_source_oddrn='/postgresql/host/localhost/databases/opendatadiscovery', items=[])\n```\n\n## Adapter's Controller\nYou can inherit from base Adapter Controller for writing your own adapters:\n```python\nfrom odd_models.adapter.controllers import ODDController\n\nclass MyController(ODDController):\n    def get_data_entities(self, changed_since=None, )\n        pass\n```\n\n## ODD API Client\nYou can use ready API Client to send requests:\n```python\nfrom odd_models.api_client import ODDApiClient\n\napi_client = ODDApiClient(base_url='http://127.0.0.1:8080')\n\n# using pydantic objects:\nfrom odd_models.models import DataEntityList\ndata_entity_list = DataEntityList(data_source_oddrn='/postgresql/host/localhost/databases/opendatadiscovery', items=[])\n\nresponse = api_client.post_data_entity_list(data_entity_list)\nassert response.status_code == 200\n\n# using dict (validation will be in the client)\ndata_entity_list = {'data_source_oddrn': '/postgresql/host/localhost/databases/opendatadiscovery', 'items': []}\n\nresponse = api_client.post_data_entity_list(data_entity_list)\nassert response.status_code == 200\n```",
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opendatadiscovery/odd-models-packager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
