# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['factorymind']

package_data = \
{'': ['*']}

install_requires = \
['bumpver>=2022.1116,<2023.0',
 'fastapi>=0.68.1,<0.69.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'factorymind',
    'version': '0.1.3',
    'description': 'Python module for the FactoryMind platform',
    'long_description': "Documentation\n=============\nThis is the documentation for the Python package\n``factorymind`` which makes it easier to interact with the data\non the FactoryMind platform.\n\n.. image:: https://github.com/factorymind/factorymind/blob/master/docs/logo.png\n   :width: 200px\n\n\n************\nInstallation\n************\nFrom PyPi:\n\n.. code:: bash\n\n    pip install factorymind\n\nFrom source:\n\n.. code:: bash\n\n    <TODO: Document>\n\n***\nUse\n***\nTo interact with your data on the FactoryMind platform,\nrun\n\n.. code:: python\n\n    >>> from factorymind.data_loader import FactoryDB\n\n    >>> mydb = FactoryDB(apikey=YOUR-API-KEY)\n    >>> mydb.list_data_sources()\n\n    ['example_data.energy_demand', 'example_data.sensors', 'sensor_data.sensors', 'sensor_data.sensors_metadata']\n\nSee the `official docs <https://factorymind.readthedocs.io>`_ for more information and examples.\n",
    'author': 'FactoryMind',
    'author_email': 'enquiry@factorymind.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://factorymind.ai',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
