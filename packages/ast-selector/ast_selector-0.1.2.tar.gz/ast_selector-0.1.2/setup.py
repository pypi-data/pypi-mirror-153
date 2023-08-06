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
    'version': '0.1.2',
    'description': 'Query AST elements by using CSS Selector-like syntax',
    'long_description': '# AST Selector\n\n<p align="center">\n    <img src="https://raw.githubusercontent.com/guilatrova/ast_selector/main/img/logo.png">\n</p>\n\n<h2 align="center">Query AST elements by using CSS Selector-like syntax</h2>\n\n<p align="center">\n  <a href="https://github.com/guilatrova/ast_selector/actions"><img alt="Actions Status" src="https://github.com/guilatrova/ast_selector/workflows/CI/badge.svg"></a>\n  <a href="https://pypi.org/project/ast-selector/"><img alt="PyPI" src="https://img.shields.io/pypi/v/ast_selector"/></a>\n  <img src="https://badgen.net/pypi/python/ast_selector" />\n  <a href="https://github.com/relekang/python-semantic-release"><img alt="Semantic Release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg"></a>\n  <a href="https://github.com/guilatrova/ast_selector/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/guilatrova/ast_selector"/></a>\n  <a href="https://pepy.tech/project/ast-selector/"><img alt="Downloads" src="https://static.pepy.tech/personalized-badge/ast_selector?period=total&units=international_system&left_color=grey&right_color=blue&left_text=%F0%9F%A6%96%20Downloads"/></a>\n  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>\n  <a href="https://github.com/guilatrova/tryceratops"><img alt="try/except style: tryceratops" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black" /></a>\n  <a href="https://twitter.com/intent/user?screen_name=guilatrova"><img alt="Follow guilatrova" src="https://img.shields.io/twitter/follow/guilatrova?style=social"/></a>\n</p>\n\n> "Query AST elements 🌲 by using CSS Selector-like 💅 syntax."\n\n## Installation and usage\n\n### Installation\n\n```\npip install ast_selector\n```\n\n### Usage\n\n```py\nfrom ast_selector import AstSelector\n\ntree = load_python_code_as_ast_tree()\nquery = "FunctionDef Raise $FunctionDef"\n# Query all functions that raises at least an exception\n\nfunctions_raising_exceptions = AstSelector(query, tree).all()\n```\n\n### Use Cases\n\n#### Functions that return int\n\n```py\nfrom ast_selector import AstSelector\n\ntree = load_python_code_as_ast_tree()\nquery = "FunctionDef.returns[id=int] $FunctionDef"\n# Query all functions that return ints e.g. def sum() -> int\n\nfunction_element = AstSelector(query, tree).first()\n```\n\n## License\n\nMIT\n\n## Credits\n\nIt\'s extremely hard to keep hacking on open source like that while keeping a full-time job. I thank God from the bottom of my heart for both the inspiration and the energy.\n',
    'author': 'Guilherme Latrova',
    'author_email': 'hello@guilatrova.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guilatrova/ast_selector',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
