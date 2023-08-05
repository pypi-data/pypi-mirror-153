# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapr_httpx']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'dapr-httpx',
    'version': '0.2.5',
    'description': '✨dapr ➕ ✨httpx is awesome',
    'long_description': '# ✨dapr ➕ ✨httpx is awesome\n## dapr api 函式庫\n- [Service invocation API](./dapr_httpx/invoke_api.py)\n- [State management API](./dapr_httpx/state_api.py)\n- [Pub/Sub API](./dapr_httpx/pubsub_api.py)\n- [Secrets API](./dapr_httpx/secrets_api.py)\n## 範例程式\n- [example](./example.py)',
    'author': 'Ben',
    'author_email': 'moon791017@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Benknightdark/dapr-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
