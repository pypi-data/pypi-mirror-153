# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kebab', 'kebab.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyyaml>=6.0,<7.0']

extras_require = \
{'ali': ['oss2>=2.15.0,<3.0.0'],
 'aws': ['boto3>=1.23.10,<2.0.0'],
 'k8s': ['kubernetes>=23.6.0,<24.0.0']}

entry_points = \
{'console_scripts': ['kebab = kebab.cli:run']}

setup_kwargs = {
    'name': 'pykebab',
    'version': '0.5.1',
    'description': '',
    'long_description': None,
    'author': 'Yangming Huang',
    'author_email': 'leonmax@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
