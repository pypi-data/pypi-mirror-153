# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tibian', 'tibian.sources', 'tibian.targets']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'jira>=3.1.1,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'types-PyYAML>=6.0.5,<7.0.0',
 'types-python-dateutil>=2.8.10,<3.0.0',
 'types-requests>=2.27.14,<3.0.0']

entry_points = \
{'console_scripts': ['tibian = tibian.main:main']}

setup_kwargs = {
    'name': 'tibian',
    'version': '1.0.0',
    'description': 'Ticket birthday announcer: A package to announce all creation birthdays of your tickets that live (too) long enough',
    'long_description': "Tibian\n======\n\nProject 'tibian', also known as the 'TIcket Birthday Announcer',\nis a project to announce tickets that it's birthday today.\nThat means it announces ticket titles and summaries that were created a few\nyears ago and are still open to a number of channels that you specified before.\nFor example, the Jira tickets of a project can be published to a Teams channel\nregularly and make some people happy (or angry).\n\nRight now, the project is in a very early stage and it's not fully functional.\n\n\nUsage\n-----\n\nTo use this project, you need to create a configuration file in the same directory.\nTo start, copy the `config.example.yaml` file to `config.yaml` and edit it.\nThe name is important here, because it's used to identify the configuration file.\nFor details about configuration, visit section `Configuration`.\n\nTo install the project, run one of the following command::\n\n    poetry install --no-dev # or\n    pip install tibian\n\nLater one is preferred, as it installs the project with the same versions\nas we tested before release and in a virtual environment.\n\nAfterwards, you can start the project by running the `tibian` command::\n\n    tibian\n\nAfterwards, it should announce the birthdays of tickets of the current date\nas specified.\n\nConfiguration\n-------------\n\nThe configuration file for the project must be located in the root folder\nof the execution command. A short (any maybe not complete) description of\nthe configuration file is given in `config.example.yaml` on GitHub.\n\nCopy this output to a file `config.yaml` in the current directory, add your credentials\nand remove parts you don't need.\n\nDetailed information about all config options will be given soon,\nbut for this version most of the configuration should be self-explanatory.\n\n'type' is the type of source or target you have,\n'name' is an internal used name for the source/target, and\n'config' is a type-dependant dictionary of types as shown.\n\n\nVersioning\n-----------\n\nWe use `semantic versioning`_ to version the project. As we are in some sort of 'beta',\nwe may (but try not to) do some breaking changes between minor versions to fix some obvious\nmisbehavior of the project. For example, we may change the configuration file format or\nadd new options to the configuration file. As we try to prevent this and add a backlog how to\nupgrade to newer versions, you maybe want to check the changelog before updating to new versions.\n\n\nDevelopment\n-----------\n\nWe are always happy about active support. If you want to actively develop on tibian, follow the next few commands.\nWe use poetry_ for the development of tibian. You can install it with the following command::\n\n    pip install poetry\n\nTo install all development dependencies, run::\n\n    poetry install\n\nAfterwards, you have all dependencies (including dev dependencies) installed in a virtualenv, and are able to develop.\n\nTo add new dependencies, run::\n\n    poetry add <package>\n\nTo activate your virtualenv, run::\n\n    poetry shell\n\nAfterwards, you can run all following commands in the virtualenv. In case you don't, you have to add 'poetry run' before each\nof the next commands to execute it in the virtualenv, or you will get missing requirements errors.\n\nTo run the style checker, run::\n\n    ./scripts/lint.sh\n\nTo run the tests and get some coverage information, run::\n\n    ./scripts/run_tests.sh\n\n.. _poetry: https://python-poetry.org/\n.. _semantic versioning: https://semver.org/\n",
    'author': 'Stefan Kraus',
    'author_email': 'dev@stefankraus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AliceMurray/tibian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
