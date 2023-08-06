# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mypyliex', 'mypyliex.classes']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'apischema>=0.17.5,<0.18.0', 'jsonschema>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'mypyliex',
    'version': '22.6.1.post13',
    'description': 'Project description',
    'long_description': '# MLE README file',
    'author': 'Tadeusz Miszczyk',
    'author_email': 'tadeusz.miszczyk@bshg.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/8tm/my_python_library_example',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
