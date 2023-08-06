# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygenomeviz']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0', 'matplotlib>=3.2.2,<4.0.0', 'numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'pygenomeviz',
    'version': '0.0.6',
    'description': 'A genome visualization python package for comparative genomics',
    'long_description': '# pyGenomeViz\nGenome visualization package\n',
    'author': 'moshi4',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moshi4/pyGenomeViz/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
