# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bumbag']

package_data = \
{'': ['*']}

install_requires = \
['toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'bumbag',
    'version': '0.3.0',
    'description': 'A package for Python utility functions.',
    'long_description': '# BumBag\n\n[![pypi](https://img.shields.io/pypi/v/bumbag)](https://pypi.org/project/bumbag)\n[![python](https://img.shields.io/badge/python-%5E3.8-blue)](https://pypi.org/project/bumbag)\n[![license](https://img.shields.io/pypi/l/bumbag)](https://github.com/estripling/bumbag/blob/main/LICENSE)\n[![ci status](https://github.com/estripling/bumbag/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/estripling/bumbag/actions/workflows/ci.yml)\n[![docs](https://readthedocs.org/projects/bumbag/badge/?version=latest)](https://readthedocs.org/projects/bumbag/?badge=latest)\n[![coverage](https://codecov.io/github/estripling/bumbag/coverage.svg?branch=main)](https://codecov.io/gh/estripling/bumbag)\n[![downloads](https://pepy.tech/badge/bumbag)](https://pepy.tech/project/bumbag)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## About\n\nA package for Python utility functions.\n\nWhat is this package about?\nIs its aim to offer functionality like a multi-tool pocketknife?\nOr like the utility belt of a caped crusader?\nWell, the purpose of a bumbag is to put in all the things you need often!\nAs such, the BumBag package is a collection of frequently used Python functions.\n\n## Dictionary definition\n\nbumbag `/ˈbʌmbæg/` (*noun countable*) -\na small bag attached to a long strap that you fasten around your waist to keep money, keys, and other small things in.\n\n## Installation\n\n`bumbag` is available on [PyPI](https://pypi.org/project/bumbag/):\n\n```bash\npip install bumbag\n```\n\n## Usage\n\nQuickly compare two Python sets with [`two_set_summary`](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/math/index.html#bumbag.math.two_set_summary):\n\n```python\nfrom bumbag.math import two_set_summary\n\nx = {"a", "c", "b", "g", "h"}\ny = {"c", "d", "e", "f", "g"}\nsummary = two_set_summary(x, y)\nprint(summary["report"])\n```\n\n```text\n    x (n=5): {\'a\', \'b\', \'c\', ...}\n    y (n=5): {\'c\', \'d\', \'e\', ...}\nx | y (n=8): {\'a\', \'b\', \'c\', ...}\nx & y (n=2): {\'c\', \'g\'}\nx - y (n=3): {\'a\', \'b\', \'h\'}\ny - x (n=3): {\'d\', \'e\', \'f\'}\nx ^ y (n=6): {\'a\', \'b\', \'d\', ...}\njaccard = 0.25\noverlap = 0.4\ndisjoint?: False\nx == y: False\nx <= y: False\nx <  y: False\ny <= x: False\ny <  x: False\n```\n\nDon\'t forget to check out [more examples](https://bumbag.readthedocs.io/en/stable/example.html#) and the [API Reference](https://bumbag.readthedocs.io/en/stable/autoapi/index.html).\n\n\n## Contributing\n\nHave you ever caught yourself thinking: "Ahh ... I need *that function* again. I have to copy it from another project."?\nIf you have, why not sharing your awesome utility function with the rest of the world?\n\nTo do so, check out the [contributing guidelines](https://bumbag.readthedocs.io/en/latest/contributing.html) and the [guide for developer](https://bumbag.readthedocs.io/en/latest/developers.html).\nPlease note that this project is released with a [Code of Conduct](https://bumbag.readthedocs.io/en/latest/conduct.html).\nBy contributing to this project, you agree to abide by its terms.\n\n## License\n\n`bumbag` was created by BumBag Developers.\nIt is licensed under the terms of the BSD 3-Clause license.\n\n## Credits\n\n`bumbag` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the [`pypkgcookiecutter` template](https://github.com/estripling/pypkgcookiecutter).\n',
    'author': 'BumBag Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/estripling/bumbag',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
