# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goon_parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['generate = goon_parser.cli:generate',
                     'json = goon_parser.cli:json',
                     'python = goon_parser.cli:py']}

setup_kwargs = {
    'name': 'goon-parser',
    'version': '0.2.0',
    'description': 'A python package used to parse ss13 dm files into json',
    'long_description': "\n# Goon Parser\n\n## Installation\n#### Using Pip\n    pip install goon_parser\n\n#### Using Poetry\n    poetry add goon_parser\n\n\n## Usage\n##### CLI\n    - Poetry\n    poetry run generate json './path/to/file.dm' './path/to/output.json'\n\n##### Parser\n    from goon_parser.parser import get_dict, get_json\n\n    chemistry_recipes_dict = get_dict('./Chemistry_Recipes.dm')\n    chemistry_recipes_json = get_json('./Chemistry_Recipes.dm')\n\n",
    'author': 'Kyle Oliver',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
