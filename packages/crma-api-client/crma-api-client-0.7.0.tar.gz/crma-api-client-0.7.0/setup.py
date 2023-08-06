# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crma_api_client', 'crma_api_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0', 'httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'crma-api-client',
    'version': '0.7.0',
    'description': 'CRM Analytics REST API Client',
    'long_description': '# crma-api-client\n[![](https://img.shields.io/pypi/v/crma_api_client.svg)](https://pypi.org/pypi/crma_api_client/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\nCRM Analytics REST API Client\n\nFeatures:\n\n- Execute SAQL queries\n- List dataset versions\n\nTable of Contents:\n\n- [Installation](#installation)\n- [Guide](#guide)\n- [Development](#development)\n\n## Installation\n\ncrma-api-client requires Python 3.9 or above.\n\n```bash\npip install crma-api-client\n# or\npoetry add crma-api-client\n```\n\n## Guide\n\nFirst, you need to create a new client instance. To do that, you either need to have credentials for an OAuth app or an existing access token handy:\n\n```python\nfrom crma_api_client.client import ConnectionInfo, CRMAAPIClient\n\n# Generate connection info if you don\'t already have an access token\nconn = await ConnectionInfo.generate(\n    client_id="abc123",\n    client_secret="***",\n    username="me@salesforce.com",\n    password="***"\n)\n\n# If you already have an instance URL and access token, you can instantiate directly\nconn = ConnectionInfo(instance_url="https://company.my.salesforce.com", access_token="XYZ123")\n\n# Create the client, passing in the connection object\nclient = CRMAAPIClient(conn)\n```\n\nNext, you can use methods on the client to make requests:\n\n```python\nresponse = await client.list_dataset_versions("Sample_Superstore_xls_Orders")\nversion = response.versions[0]\nquery = "\\n".join(\n    [\n        f"""q = load "{version.dataset.id}/{version.id}";""",\n        """q = group q by \'Category\';""",\n        """q = foreach q generate q.\'Category\' as \'Category\', sum(q.\'Sales\') as \'Sales\';""",\n        """q = order q by \'Category\' asc;""",\n    ]\n)\nresponse = await client.query(query)\nassert response.results.records == [\n    {"Category": "Furniture", "Sales": 741999.7953},\n    {"Category": "Office Supplies", "Sales": 719047.032},\n    {"Category": "Technology", "Sales": 836154.033},\n]\n```\n\n## Development\n\nTo develop crma-api-client, install dependencies and enable the pre-commit hook:\n\n```bash\npip install pre-commit poetry\npoetry install\npre-commit install -t pre-commit -t pre-push\n```\n\nTo run tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Jonathan Drake',
    'author_email': 'jon.drake@salesforce.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NarrativeScience/crma-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
