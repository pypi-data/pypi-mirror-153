# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoricaan_cli',
 'aoricaan_cli.src',
 'aoricaan_cli.src.api',
 'aoricaan_cli.src.enpoints',
 'aoricaan_cli.src.lambdas',
 'aoricaan_cli.src.layers',
 'aoricaan_cli.src.models',
 'aoricaan_cli.src.project',
 'aoricaan_cli.src.utils',
 'aoricaan_cli.templates',
 'aoricaan_cli.templates.layers',
 'aoricaan_cli.templates.layers.core',
 'aoricaan_cli.templates.layers.core.python',
 'aoricaan_cli.templates.layers.core.python.core_api',
 'aoricaan_cli.templates.layers.core.python.core_aws',
 'aoricaan_cli.templates.layers.core.python.core_db',
 'aoricaan_cli.templates.layers.core.python.core_utils',
 'aoricaan_cli.templates.project',
 'aoricaan_cli.templates.templates']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.10,<0.2.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'fastapi>=0.71.0,<0.72.0',
 'mangum>=0.12.3,<0.13.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer[all]>=0.4.1,<0.5.0',
 'uvicorn>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['apm = aoricaan_cli.cli:app']}

setup_kwargs = {
    'name': 'aoricaan-cli',
    'version': '0.3.0',
    'description': '',
    'long_description': '# aoricaan-cli\n\nA cli for manage a project.\n\n\nfor use:\n\nRecommendation: \n\nCreate and activate a virtual environment.\n````commandline\npython -m venv venv\n````\n\n````commandline\nsorurce ./venv/Scripts/activate\n\nor\n\n./venv/Scripts/activate\n````\n\nnow you can install the CLI\n\n````commandline\npip install aoricaan-cli\n````\n\nfor start to work\n\n````commandline\napm init\npip install -r requirements.txt\napm project install\n````\n\nAll ready!\n\nYou can start developing you api.\n\nfor more information read the readme created within your project.\n\n\n',
    'author': 'carlos',
    'author_email': 'carlosaarivera23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
