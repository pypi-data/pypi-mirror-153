# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deci_common',
 'deci_common.abstractions',
 'deci_common.auto_logging',
 'deci_common.aws_connection',
 'deci_common.data_connection',
 'deci_common.data_interfaces',
 'deci_common.data_types',
 'deci_common.data_types.enum',
 'deci_common.decorators',
 'deci_common.environment',
 'deci_common.serializaion']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1,<2',
 'botocore>=1,<2',
 'cryptography==3.4.7',
 'gdown>=4,<5',
 'numpy>=1.19,<2.0',
 'pydantic>=1.9,<2.0',
 'pymongo>=4,<5',
 'python-json-logger==2.0.2',
 'python-magic>=0,<1',
 'stringcase>=1,<2']

setup_kwargs = {
    'name': 'deci-common',
    'version': '0.5.0',
    'description': "A package for Deci's common data types, connections and interfaces",
    'long_description': '# deci-common\nCommon data types, connections and interfaces\n',
    'author': 'Deci AI',
    'author_email': 'rnd@deci.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.9',
}


setup(**setup_kwargs)
