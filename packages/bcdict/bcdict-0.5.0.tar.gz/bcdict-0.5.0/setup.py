# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcdict']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0'],
 'docs': ['myst-nb>=0.13.2,<0.14.0',
          'Sphinx>=4.5.0,<5.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-book-theme>=0.3.2,<0.4.0',
          'sphinx-copybutton>=0.5.0,<0.6.0',
          'sphinx-panels>=0.6.0,<0.7.0',
          'sphinxcontrib-mermaid>=0.7.1,<0.8.0'],
 'docs:python_version < "3.10" and implementation_name == "cpython"': ['pandas==1.3.1',
                                                                       'scikit-learn==1.0.2']}

setup_kwargs = {
    'name': 'bcdict',
    'version': '0.5.0',
    'description': 'Python dictionary with broadcast support.',
    'long_description': '[![Tests](https://github.com/mariushelf/bcdict/actions/workflows/cicd.yaml/badge.svg)](https://github.com/mariushelf/bcdict/actions/workflows/cicd.yaml)\n[![codecov](https://codecov.io/gh/mariushelf/bcdict/branch/master/graph/badge.svg)](https://codecov.io/gh/mariushelf/bcdict)\n[![PyPI version](https://badge.fury.io/py/bcdict.svg)](https://pypi.org/project/bcdict/)\n[![Documentation Status](https://readthedocs.org/projects/bcdict/badge/?version=latest)](https://bcdict.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n# Broadcast Dictionary\n\n\nPython dictionary with broadcast support.\n\nBehaves like a regular dictionary.\n\nAllows to apply operations to all its values at once.\nWhithout loops, whithout dict comprehension.\n\n## Installation\n\n```bash\npip install bcdict\n```\n\n## Usage\n\n```python\nfrom bcdict import BCDict\n>>> d = BCDict({"a": "hello", "b": "world!"})\n>>> d\n{\'a\': \'hello\', \'b\': \'world!\'}\n```\n\n\nRegular element access:\n```python\n>>> d[\'a\']\n\'hello\'\n```\n\n\nRegular element assignments\n```python\n>>> d[\'a\'] = "Hello"\n>>> d\n{\'a\': \'Hello\', \'b\': \'world!\'}\n```\n\nCalling functions:\n```python\n>>> d.upper()\n{\'a\': \'HELLO\', \'b\': \'WORLD!\'}\n```\n\nSlicing:\n```python\n>>> d[1:3]\n{\'a\': \'el\', \'b\': \'or\'}\n```\n\nApplying functions:\n```python\n>>> d.pipe(len)\n{\'a\': 5, \'b\': 6}\n```\n\nWhen there is a conflict between an attribute in the values and an attribute in\n`BCDict`, use the attribute accessor explicitly:\n\n```python\n>>> d.a.upper()\n{\'a\': \'HELLO\', \'b\': \'WORLD!\'}\n```\n\nSlicing with conflicting keys:\n```python\n>>> n = BCDict({1:"hello", 2: "world"})\n>>> n[1]\n\'hello\'\n>>> # Using the attribute accessor:\n>>> n.a[1]\n{1: \'e\', 2: \'o\'}\n```\n\n## Next steps\n\nSee the [introduction notebook](docs/source/examples/introduction.ipynb) and other\n[examples](docs/source/examples/examples.md).\n\nAlso check out the full documentation on\n[bcdict.readthedocs.io](https://bcdict.readthedocs.io/en/latest/).\n\n\n## Changelog\n\n### v0.5.0\n* feature: broadcast attribute and item assignment\n* fix: broadcast slicing with `.a` accessor\n\n### v0.4.3\n* fix: unpickling causes recursion error\n\n### v0.4.2\n* docs: improve the documenation\n\n### v0.4.1\n* fix: sphinxcontrib-mermaid gets installed as default dependency, should be dev dependency\n\n### v0.4.0\n* new functions `eq()` and `ne()` for equality/inequality with broadcast support\n\n### v0.3.0\n* new functions in `bcdict` package:\n  * `apply()`\n  * `broadcast()`\n  * `broadcast_arg()`\n  * `broadcast_kwarg()`\n* docs: write some documentation and host it on [readthedocs](https://bcdict.readthedocs.io/en/latest/)\n\n### v0.2.0\n* remove `item()` function. Use `.a[]` instead.\n\n### v0.1.0\n* initial release\n\n\nOriginal repository: [https://github.com/mariushelf/bcdict](https://github.com/mariushelf/bcdict)\n\nAuthor: Marius Helf\n([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n',
    'author': 'Marius Helf',
    'author_email': 'marius@happyyeti.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariushelf/bcdict',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
