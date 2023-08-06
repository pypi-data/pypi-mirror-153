# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detamvc',
 'detamvc.templates.core',
 'detamvc.templates.core.static_pages',
 'detamvc.templates.scaffold']

package_data = \
{'': ['*'],
 'detamvc': ['templates/core/static_pages/static/css/*',
             'templates/core/static_pages/static/img/*',
             'templates/core/static_pages/templates/*',
             'templates/scaffold/templates/*',
             'templates/scaffold_helpers/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'deta>=1.1.0,<2.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'odetam>=1.2.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-multipart>=0.0.5,<0.0.6',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['detamvc = detamvc.main:app']}

setup_kwargs = {
    'name': 'detamvc',
    'version': '0.1.8',
    'description': '',
    'long_description': '# DetaMVC\n\n\nDetaMVC is a framework for rapidly developing web applications using:\n- [FastAPI](https://fastapi.tiangolo.com/)\n- [Jinja2](https://fastapi.tiangolo.com/advanced/templates/?h=jinja2)\n- [Deta](https://docs.deta.sh/docs/home)\n- [ODetaM](https://github.com/rickh94/ODetaM)\n\n## Work in Progress\nPlease note that DetaMVC is a work in progress currently. Some planned updates include:\n- Support for more data types when scaffolding\n- Implement Deta Auth when available\n- Generate with other front ends ? (may take significant restructuring)\n\n## Installation\n```\npip install detamvc\n```\n   \n\n## Basics\nIf you are familiar with Ruby on Rails, the commands are very similar for creating an application. \n\n```\ndetamvc new project\n\ncd project\n\ndetamvc scaffold post title:str content:str\n```\n\nBefore running your project, be sure to set your PROJECT_KEY for Deta. You can get this from your dashboard under \'settings\'.\n\n\n```\necho PROJECT_KEY="#######_#############" > .env\n```\n\n**NOTE**: Deta Base is used as your database. I would strongly recommend creating a new Project called \'development\' where you can play around with ideas while building. When you go to production, create a new project in Deta for this to be managed in.\n\n## Run a Server Manually\n\nThis assumes you have uvicorn installed. You can run with other servers as you wish - just set up like you would for a normal [FastAPI](https://fastapi.tiangolo.com/deployment/manually/ "Run a Server Manually - Uvicorn") application.\n```\ndetamvc s\n```\nor\n```\nuvicorn main:app --reload\n```\n\n## Deploy on Deta\nNow you can deploy this on Deta!\n```\ndeta new --project default\n```',
    'author': 'MBeebe',
    'author_email': 'grow.food.everywhere@gmail.com',
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
