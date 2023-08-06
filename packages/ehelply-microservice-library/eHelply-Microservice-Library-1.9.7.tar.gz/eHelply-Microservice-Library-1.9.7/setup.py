# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_microservice_library',
 'ehelply_microservice_library.cli',
 'ehelply_microservice_library.integrations',
 'ehelply_microservice_library.realtime',
 'ehelply_microservice_library.routers',
 'ehelply_microservice_library.utils',
 'ehelply_microservice_library.utils.constants']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'coverage>=6.3.2,<7.0.0',
 'ehelply-bootstrapper>=0.16.0,<0.17.0',
 'ehelply-generator>=0.1.2,<0.2.0',
 'ehelply-python-sdk>=1.1.53,<2.0.0',
 'ehelply-updater>=0.2.0,<0.3.0',
 'pytest-mock>=3.7.0,<4.0.0']

entry_points = \
{'console_scripts': ['ehelply_microservice_library = '
                     'ehelply_microservice_library.cli.self_cli:cli_main']}

setup_kwargs = {
    'name': 'ehelply-microservice-library',
    'version': '1.9.7',
    'description': '',
    'long_description': '## Building\n* `poetry publish --build`\n\n## Development\n* `ehelply_microservice_library dev export-code-docs`\n* Clear cache: `poetry cache clear pypi --all`',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
