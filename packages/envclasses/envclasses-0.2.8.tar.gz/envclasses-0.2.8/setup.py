# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envclasses']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml', 'typing_inspect>=0.4.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

setup_kwargs = {
    'name': 'envclasses',
    'version': '0.2.8',
    'description': 'envclasses is a library to map fields on dataclass object to environment variables',
    'long_description': "# `envclasses`\n\n[![image](https://img.shields.io/pypi/v/envclasses.svg)](https://pypi.org/project/envclasses/)\n[![image](https://img.shields.io/pypi/pyversions/envclasses.svg)](https://pypi.org/project/envclasses/)\n![Test](https://github.com/yukinarit/envclasses/workflows/Test/badge.svg)\n\n*`envclasses` is a library to map fields on dataclass object to environment variables.*\n\n## Installation\n\n```bash\npip install envclasses\n```\n\n## Usage\n\nDeclare a class with `dataclass` and `envclass` decorators.\n\n```python\nfrom envclasses import envclass, load_env\nfrom dataclasses import dataclass\n\n@envclass\n@dataclass\nclass Foo:\n    v: int\n\nfoo = Foo(v=10)\nload_env(foo, prefix='foo')\nprint(foo)\n```\n\nRun the script\n\n```\n$ python foo.py\nFoo(v=10)\n```\n\nRun with environment variable\n\n```\n$ FOO_V=100 python foo.py\nFoo(v=100)\n```",
    'author': 'Yukinari Tani',
    'author_email': 'yukinarit84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yukinarit.github.io/envclasses/envclasses.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
