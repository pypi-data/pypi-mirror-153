# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doxysphinx', 'doxysphinx.utils']

package_data = \
{'': ['*'], 'doxysphinx': ['resources/*']}

install_requires = \
['click-log>=0.4.0,<0.5.0',
 'click>=8.0.0,<9.0.0',
 'json5>=0.9.6,<0.10.0',
 'lxml>=4.7.1,<5.0.0']

extras_require = \
{':sys_platform == "windows"': ['colorama>=0.4.4,<0.5.0']}

entry_points = \
{'console_scripts': ['doxysphinx = doxysphinx.cli:cli']}

setup_kwargs = {
    'name': 'doxysphinx',
    'version': '2.1.9',
    'description': 'Integrates doxygen html documentation with sphinx.',
    'long_description': None,
    'author': 'Nirmal Sasidharan',
    'author_email': 'nirmal.sasidharan@de.bosch.com',
    'maintainer': 'Nirmal Sasidharan',
    'maintainer_email': 'nirmal.sasidharan@de.bosch.com',
    'url': 'https://github.com/boschglobal/doxysphinx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
