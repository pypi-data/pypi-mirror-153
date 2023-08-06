# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_project_status']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0', 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['git_project_status = git_project_status.__main__:cli']}

setup_kwargs = {
    'name': 'git-project-status',
    'version': '0.0.12',
    'description': 'Check subdirectories for dirty repos.',
    'long_description': '# git_project_status\n\nReal simple, just iterates through the first-level subdirectories and does the equivalent of git status, only uglier.\n\nIf you want more logs, set an environment variable of `LOGURU_LOG_LEVEL=DEBUG`.\n\nInstallation: `pip install git-project-status`\n\nWhich will create a console script `git_project_status`.\n\n## Changelog\n\n * 0.0.6 - Fixed handling detached heads.\n * 0.0.7 - 2022-01-08 - Updated build tooling, broke the script name. Whoops! Pulled.\n * 0.0.8 - 2022-01-08 - Fixed the script name. Whoops! Pulled.\n * 0.0.9 - 2022-01-08 - Fixed the script config.\n * 0.0.10 - 2022-01-08 - Added the option to specify a directory.\n * 0.0.11 - 2022-01-08 - Cleaned up some formatting, using pathlib for checking.\n * 0.0.12 - 2022-06-02 - Shaved the yak, moved packaging tools, added more type-checking.\n',
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
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
