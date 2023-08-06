# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data49']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'thefuzz[speedup]>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'data49',
    'version': '0.4.0',
    'description': 'A gold rush-themed data mining library',
    'long_description': "# data49\n\n> A data mining library\n\nWIP\n\n<!-- It is split into the following sections:\n\n - **General utilities** for stuff like functional programming, utility functions, parallel jobs, caching to a file, etc. Wraps `joblib`. Found in the default namespace (`*`)\n  - **Web-related utilities** wrapping web scraping with Beautiful Soup and requests or browser automation with Selenium. Found in the `web` namespace\n  - **Logging** Logging made super easy. Found in the `log` namespace\n\nCurrently, only the web-related utilities are implemented\n\n## Features\n\n - Simple API w/automatic logging\n - Fully type hinted\n - Typo-resistant\n\n\n## FAQ\n\n### Why the name?\n\nThis library's name was taken from the 18**49** gold rush. In the modern world, data is gold. -->\n",
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
