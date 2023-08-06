# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ast_selector']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ast-selector',
    'version': '0.1.1',
    'description': 'Easily find and query AST elements by using CSS Selector-like syntax',
    'long_description': '# AST Selector\n',
    'author': 'Guilherme Latrova',
    'author_email': 'hello@guilatrova.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guilatrova/ast_selector',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
