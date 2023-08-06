# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skit_labels']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=2.1.2,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'botocore>=1.23.24,<1.23.25',
 'docopt>=0.6.2,<0.7.0',
 'dvc[s3]>=2.9.5,<3.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydash>=5.1.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2020.5,<2021.0',
 'skit-fixdf>=0.1.12,<0.2.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.63.0,<5.0.0']

entry_points = \
{'console_scripts': ['skit-labels = skit_labels.cli:main']}

setup_kwargs = {
    'name': 'skit-labels',
    'version': '0.3.22',
    'description': 'Command line tool for interacting with labelled datasets at skit.ai.',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
