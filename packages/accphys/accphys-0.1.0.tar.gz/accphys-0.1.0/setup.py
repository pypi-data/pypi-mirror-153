# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['accphys',
 'accphys..ipynb_checkpoints',
 'accphys.solver',
 'accphys.solver..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=5.5.5,<6.0.0',
 'latticeadaptor>=0.3.9',
 'lieops>=0.1.1,<0.2.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'accphys',
    'version': '0.1.0',
    'description': 'Analyze non-linear single-particle storage ring dynamics',
    'long_description': None,
    'author': 'Malte Titze',
    'author_email': 'mtitze@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
