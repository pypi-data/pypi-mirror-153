# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydagogy_brent']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.0.0,<13.0.0']

setup_kwargs = {
    'name': 'pydagogy-brent',
    'version': '0.0.1',
    'description': "Brent's algorithm",
    'long_description': "# Brent algorithm\n\n## To install\n\nBrent's algorithm requires `Python 3.8` and the [rich](https://github.com/Textualize/rich) library.\n\nTo install the library, run:\n\n```bash\npip install pydagogy-brent\n```\n\nThen run the following in a Python shell:\n\n```python\nfrom pydagogy_brent import Settings, brent\nimport math\nsettings = Settings(x_rel_tol=1e-12, x_abs_tol=1e-12, y_tol=1e-12, verbose=True)\nf = math.cos\nbrent(f, 0.0, 3.0, settings)\n```\n\n\n## To develop\n\nWe use the [Poetry](https://python-poetry.org/) dependency management system.\n\nWe use [VS Code](https://code.visualstudio.com/), the Black/isort/pylint tools. To install them, run:\n\n```bash\npoetry install \n```\n",
    'author': 'Denis Rosset',
    'author_email': 'physics@denisrosset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/denisrosset/brent-level-2.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
