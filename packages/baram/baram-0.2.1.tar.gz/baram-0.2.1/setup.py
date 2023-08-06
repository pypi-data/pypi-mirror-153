# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baram']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'boto3==1.18.65',
 'fire>=0.4.0,<0.5.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'baram',
    'version': '0.2.1',
    'description': 'AWS Framework for python',
    'long_description': '## Baram\n\nCloud Framework for AWS Framework.\n\nBaram means "wind" in Korean which makes cloud move conveniently.  \n\n## For Framework Developer\n\nYou can build and install the package as below.\n\n```commandline\n\n$ ./build.sh\n```',
    'author': 'Kwangsik Lee',
    'author_email': 'lks21c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
