# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nueramic_mathml']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0', 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'nueramic-mathml',
    'version': '0.0.1.1',
    'description': 'Math algorithms in ML on torch',
    'long_description': '## mathml\n\nMath algorithms in ML on torch\n',
    'author': 'Victor Barbarich',
    'author_email': 'vktrbr@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nueramic/mathml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
