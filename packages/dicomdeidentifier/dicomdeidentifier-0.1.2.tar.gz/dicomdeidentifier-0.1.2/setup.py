# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dicomdeidentifier']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'idiscore>=1.0.1,<2.0.0',
 'logdecoratorandhandler>=0.1.4,<0.2.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'dicomdeidentifier',
    'version': '0.1.2',
    'description': 'Deidentifies Dicom tags',
    'long_description': None,
    'author': 'barbara73',
    'author_email': 'barbara.jesacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
