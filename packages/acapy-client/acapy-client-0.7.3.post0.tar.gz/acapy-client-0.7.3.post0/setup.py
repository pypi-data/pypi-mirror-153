# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acapy_client',
 'acapy_client.api',
 'acapy_client.api.action_menu',
 'acapy_client.api.basicmessage',
 'acapy_client.api.connection',
 'acapy_client.api.credential_definition',
 'acapy_client.api.credentials',
 'acapy_client.api.did_exchange',
 'acapy_client.api.discover_features',
 'acapy_client.api.discover_features_v2_0',
 'acapy_client.api.endorse_transaction',
 'acapy_client.api.introduction',
 'acapy_client.api.issue_credential_v1_0',
 'acapy_client.api.issue_credential_v2_0',
 'acapy_client.api.jsonld',
 'acapy_client.api.ledger',
 'acapy_client.api.mediation',
 'acapy_client.api.multitenancy',
 'acapy_client.api.out_of_band',
 'acapy_client.api.present_proof_v1_0',
 'acapy_client.api.present_proof_v2_0',
 'acapy_client.api.resolver',
 'acapy_client.api.revocation',
 'acapy_client.api.schema',
 'acapy_client.api.server',
 'acapy_client.api.trustping',
 'acapy_client.api.wallet',
 'acapy_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'httpx>=0.15.4,<0.23.0', 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'acapy-client',
    'version': '0.7.3.post0',
    'description': 'A client library for accessing Aries Cloud Agent',
    'long_description': '# acapy-client\nA client library for accessing Aries Cloud Agent\n\n## Usage\nFirst, create a client:\n\n```python\nfrom acapy_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom acapy_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom acapy_client.models import MyDataModel\nfrom acapy_client.api.my_tag import get_my_data_model\nfrom acapy_client.types import Response\n\nmy_data: MyDataModel = get_my_data_model.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom acapy_client.models import MyDataModel\nfrom acapy_client.api.my_tag import get_my_data_model\nfrom acapy_client.types import Response\n\nmy_data: MyDataModel = await get_my_data_model.asyncio(client=client)\nresponse: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)\n```\n\nBy default, when you\'re calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com", \n    token="SuperSecretToken",\n    verify_ssl="/path/to/certificate_bundle.pem",\n)\n```\n\nYou can also disable certificate validation altogether, but beware that **this is a security risk**.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com", \n    token="SuperSecretToken", \n    verify_ssl=False\n)\n```\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but the async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `acapy_client.api.default`\n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
