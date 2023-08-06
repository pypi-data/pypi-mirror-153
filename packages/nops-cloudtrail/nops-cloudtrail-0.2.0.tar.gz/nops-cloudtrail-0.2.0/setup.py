# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nops_cloudtrail', 'nops_cloudtrail.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.102',
 'orjson>=3.6.9',
 'pydantic>=1.8.0',
 'pyrsistent>=0.17.3',
 'python-dateutil>=2.8.2']

setup_kwargs = {
    'name': 'nops-cloudtrail',
    'version': '0.2.0',
    'description': 'Pull cloudtrail logs from S3 bucket.',
    'long_description': None,
    'author': 'nOps Engineers',
    'author_email': 'eng@nops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
