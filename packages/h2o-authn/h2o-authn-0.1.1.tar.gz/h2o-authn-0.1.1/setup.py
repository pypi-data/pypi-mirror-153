# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['h2o_authn']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16']

setup_kwargs = {
    'name': 'h2o-authn',
    'version': '0.1.1',
    'description': 'H2O Python Clients Authentication Helpers',
    'long_description': '# `h2o-authn`\n\n[![licence](https://img.shields.io/github/license/h2oai/authn-py?style=flat-square)](https://github.com/h2oai/authn-py/main/LICENSE)\n[![pypi](https://img.shields.io/pypi/v/h2o-authn?style=flat-square)](https://pypi.org/project/h2o-authn/)\n\nH2O Python Clients Authentication Helpers.\n\n## Installation\n\n```sh\npip install h2o-authn\n```\n\n## Usage\n\nPackage provides two top level classes `h2o_authn.TokenProvider` and `h2o_authn.AsyncTokenProvider` with identical constructors accepting following arguments:\n\n- `refresh_token`: Refresh token which will used for the access token exchange.\n- `client_id`: OAuth 2.0 client id that will be used or the access token\n    exchange.\n- `issuer_url` or `token_endpoint_url` **needs to be provided**\n  - `issuer_url`: Base URL of the issuer. This URL will be used for the discovery\n        to obtain token endpoint. Mutually exclusive with the\n        token_endpoint_url argument.\n  - `token_endpoint_url`: URL of the token endpoint that should be used for the\n        access token exchange. Mutually exclusive with the issuer_url argument.\n- `client_secret`: Optional OAuth 2.0 client secret for the confidential\n    clients. Used only when provided.\n- `scope`: Optionally sets the the scope for which the access token should be\n    requested.\n- `expiry_threshold`: How long before token expiration should token be\n    refreshed when needed. This does not mean that the token will be\n    refreshed before it expires, only indicates the earliest moment before\n    the expiration when refresh would occur. (default: 5s)\n- `expires_in_fallback`: Fallback value for the expires_in value. Will be used\n    when token response does not contains expires_in field.\n- `minimal_refresh_period`: Optionally minimal period between the earliest token\n    refresh exchanges.\n\nBoth classes has identical interface in sync or async variant.\n\n```python\nprovider = h2o_authn.TokenProvider(...)\naprovider = h2o_authn.AsyncTokenProvider(...)\n\n\n# Calling the providers directly makes sure that fresh access token is available\n# and returns it.\naccess_token = provider()\naccess_token = await aprovider()\n\n\n# Calling the token() returns h2o_authn.token.Token instance.\ntoken = provider.token()\ntoken = await aprovider.token()\n\n# It can used as str.\nassert token == access_token\n\n# And contains additional attributes when available.\ntoken.exp  # Is expiration of the token as datetime.datetime\ntoken.scope  # Is scope of the token if server provided it.\n\n\n# Sync/Async variants can be converted from one to another.\nprovider = aprovider.as_sync()\naprovider = provider.as_async()\n\n\n# When access token with different scope is needed new instance can cloned from\n# the current with different scope.\nprovider = provider.with_scope("new scopes")\naprovider = aprovider.with_scope("new scopes")\n```\n\n### Examples\n\n#### Example: Use with H2O.ai MLOps Python CLient\n\n```python\nimport h2o_authn\nimport h2o_mlops_client as mlops\n\nprovider = h2o_authn.TokenProvider(...)\nmlops_client = mlops.Client(\n    gateway_url="https://mlops-api.cloud.h2o.ai",\n    token_provider=provider,\n)\n...\n```\n\n#### Example: Use with H2O.ai Drive Python Client within the Wave App\n\n```python\nimport h2o_authn\nimport h2o_drive\nfrom h2o_wave import Q, app, ui\nfrom h2o_wave import main\n\n@app("/")\nasync def serve(q: Q):\n    provider = h2o_authn.AsyncTokenProvider(\n        refresh_token=q.auth.refresh_token,\n        issuer_url=os.getenv("H2O_WAVE_OIDC_PROVIDER_URL"),\n        client_id=os.getenv("H2O_WAVE_OIDC_CLIENT_ID"),\n        client_secret=os.getenv("H2O_WAVE_OIDC_CLIENT_SECRET"),\n    )\n    my_home = await h2o_drive.MyHome(token=provider)\n\n    ...\n```\n\n#### Example: Use with H2O.ai Enterprise Steam Python Client\n\n```python\nimport h2o_authn\nimport h2osteam\nimport h2osteam.clients\n\nprovider = h2o_authn.TokenProvider(...)\n\nh2osteam.login(\n    url="https://steam.cloud-dev.h2o.ai", access_token=provider()\n)\nclient = h2osteam.clients.DriverlessClient()\n\n...\n```\n',
    'author': 'H2O.ai',
    'author_email': 'support@h2o.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/h2oai/authn-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
