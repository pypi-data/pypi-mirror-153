# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatsapie',
 'whatsapie.ext',
 'whatsapie.ext.message',
 'whatsapie.schema_generator']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'whatsapie',
    'version': '0.1.7',
    'description': "Unofficial Python wrapper for Meta's whatsapp cloud API",
    'long_description': "# whatsapie\n\nUnofficial wrapper for Meta's [**Whatsapp Cloud API**](https://developers.facebook.com/docs/whatsapp/cloud-api) written in Python\n\n## INSTALL\n\n```console\n$ pip install whatsapie\n```\n\n!!! note\n\n    whatsapie requires python 3.10 or above\n\n## PREREQUISITES\n\n-   Follow Meta's [Whatsapp Cloud API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api) and obtain, meta business app [ACCESS_TOKEN](#) and [PHONE_NUMBER_ID]()\n\n## Documentation\n\n-   Get started [here](https://advrxh.github.io/whatsapie/get-started/)\n\n## CONTRIBUTION\n\nThis repo is open for contribution. I'd love some contribution [here](https://github.com/advrxh/whatsapie)\n\nMaintained by [Aadil Varsh](https://advrxh.github.io)\n",
    'author': 'Aadil Varsh',
    'author_email': 'aadilvarshofficial@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://advrxh.github.io/whatsapie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
