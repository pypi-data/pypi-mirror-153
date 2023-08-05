# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_matplotlib']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7.1',
 'markdown!=3.3.5',
 'mkdocs-material>=8.1.9',
 'mkdocs>=1.1.1',
 'psutil>=5.9.1',
 'seaborn>=0.10.0']

entry_points = \
{'mkdocs.plugins': ['mkdocs_matplotlib = '
                    'mkdocs_matplotlib.plugin:RenderPlugin']}

setup_kwargs = {
    'name': 'mkdocs-matplotlib',
    'version': '0.10.0',
    'description': 'Live rendering of python code using matplotlib',
    'long_description': '# Mkdocs-Matplotlib\n\n[![PyPI version](https://badge.fury.io/py/mkdocs-matplotlib.svg)](https://badge.fury.io/py/mkdocs-matplotlib)\n[![Test](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/test.yml/badge.svg)](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/test.yml)\n[![Release Pipeline](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/release.yml/badge.svg)](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/release.yml)\n[![Code Quality](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/conde_quality.yml/badge.svg)](https://github.com/AnHo4ng/mkdocs-matplotlib/actions/workflows/conde_quality.yml)\n[![Documentation Status](https://readthedocs.org/projects/mkdocs-matplotlib/badge/?version=latest)](https://mkdocs-matplotlib.readthedocs.io/en/latest/?badge=latest)\n[![Python version](https://img.shields.io/badge/python-3.8-blue.svg)](https://pypi.org/project/kedro/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AnHo4ng/mkdocs-matplotlib/blob/master/LICENCE)\n![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n**Mkdocs-Matplotlib** is a plugin for [mkdocs](https://www.mkdocs.org/) which allows you to automatically generate matplotlib figures and add them to your documentation.\nSimply write the code as markdown into your documention.\n\n![screenshot](docs/assets/screenshot.png)\n\n## Quick Start\n\nThis plugin can be installed with `pip`\n\n```shell\npip install mkdocs-matplotlib\n```\nTo enable this plugin for mkdocs you need to add the following lines to your `mkdocs.yml`.\n\n```yaml\nplugins:\n  - mkdocs_matplotlib\n```\n\nTo render a code cell using matplotlib you simply have to add the comment `# mkdocs: render` at the top of the cell.\n\n```python\n# mkdocs: render\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nxpoints = np.array([1, 8])\nypoints = np.array([3, 10])\n\nplt.plot(xpoints, ypoints)\n```\n\nIn addition you can add the comment `# mkdocs: hidecode` to hide  the code and and `# mkdocs: hideoutput` to hide the output image of the cell.\n',
    'author': 'An Hoang',
    'author_email': 'an.hoang@statworx.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mkdocs-matplotlib.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
