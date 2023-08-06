# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyelab',
 'eyelab.commands',
 'eyelab.dialogs',
 'eyelab.dialogs.help',
 'eyelab.models',
 'eyelab.models.treeview',
 'eyelab.tools',
 'eyelab.views',
 'eyelab.views.ui',
 'eyelab.views.ui.cursors',
 'eyelab.views.ui.icons']

package_data = \
{'': ['*']}

install_requires = \
['PySide6==6.1.3',
 'eyepie>=0.6.7,<0.7.0',
 'qimage2ndarray==1.9.0',
 'requests>=2.27.1,<3.0.0',
 'scikit-image>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'eyelab',
    'version': '0.3.2',
    'description': 'Multi-modal annotation tool for eye imaging data',
    'long_description': None,
    'author': 'Olivier Morelle',
    'author_email': 'oli4morelle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
