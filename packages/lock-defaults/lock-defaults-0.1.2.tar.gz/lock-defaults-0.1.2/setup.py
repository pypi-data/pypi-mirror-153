# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lock_defaults',
 'lock_defaults.with_paramspec',
 'lock_defaults.without_paramspec']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lock-defaults',
    'version': '0.1.2',
    'description': 'Helper decorator to lock default mutable values',
    'long_description': "# lock-defaults\n[![PyPI](https://img.shields.io/pypi/v/lock-defaults.svg)](https://pypi.org/project/lock-defaults/)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/inkleby/lock-defaults/blob/main/LICENSE.md)\n[![Copy and Paste](https://img.shields.io/badge/Copy%20%2B%20Paste%3F-yes!-blue)](#install)\n\nThis decorator is small and only relies on the standard library, so can just be copied into a project.\n\nPython has a weird behaviour around default values for functions. If you use an empty list as a default argument, things added to the list during the function can hang around for next time the function is called. A common pattern of dealing with this is the following:\n\n```python\ndef func(foo = None):\n    if foo is None:\n        foo = []\n```\n\nBut this looks rubbish! And gets worse when you add typing:\n\n```python\ndef func(foo: list | None = None):\n    if foo is None:\n        foo = []\n```\n\nYou don't need that workaround for any other of default value. Why does the list parameter have to pretend it can be None, when that's not the intention at all?\n\nThe `lockmutabledefaults` decorator fixes this by introducing what *should* be the default approach, and default values that are lists, dictionaries or sets are isolated in each re-run.\n\n```python\n@lockmutabledefaults\ndef func(foo: list = []):\n    pass\n```\n\n## Install\n\nYou can install from pip: `python -m pip install lock-defaults`\n\nOr you can copy the function directly into your projects.\n\n* For python 3.10+: [with_paramspec/lock_defaults.py](/src/lock_defaults/with_paramspec/lock_defaults.py)\n* For python 3.8, 3.9: [without_paramspec/lock_defaults.py](/src/lock_defaults/without_paramspec/lock_defaults.py)\n",
    'author': 'Alex Parsons',
    'author_email': 'alex@alexparsons.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajparsons/lock-defaults',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
