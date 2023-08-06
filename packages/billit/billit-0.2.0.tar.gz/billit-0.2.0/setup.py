# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['billit', 'billit.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'billit',
    'version': '0.2.0',
    'description': 'Python SDK for https://billit.io',
    'long_description': '# Billit\nPython SDK for Billit (https://billit.io/).\n\n## Gettings started\nComing soon.\n\n## License\nThis project is [MIT licensed](./LICENSE).\n',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@withlogic.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
