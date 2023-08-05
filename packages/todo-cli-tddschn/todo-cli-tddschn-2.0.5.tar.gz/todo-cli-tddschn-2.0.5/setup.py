# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todo_cli_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'colorama==0.4.4',
 'fastapi[api]>=0.75.2,<0.76.0',
 'logging-utils-tddschn>=0.1.9,<0.2.0',
 'prompt-toolkit>=3.0.29,<4.0.0',
 'shellingham==1.4.0',
 'sqlmodel>=0.0.6,<0.0.7',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.1,<0.5.0',
 'uvicorn[api]>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['itodo = todo_cli_tddschn.todo_shell:main',
                     'todo = todo_cli_tddschn.cli:app']}

setup_kwargs = {
    'name': 'todo-cli-tddschn',
    'version': '2.0.5',
    'description': 'CLI Todo app made with typer, sqlite and a REST API',
    'long_description': "# todo-cli-tddschn\n\nA simple command-line Todo app made with typer, sqlite and a REST API.\n\n- [todo-cli-tddschn](#todo-cli-tddschn)\n  - [Features](#features)\n  - [Install, Upgrade and Uninstall](#install-upgrade-and-uninstall)\n    - [pipx (recommended)](#pipx-recommended)\n    - [pip](#pip)\n  - [Usage](#usage)\n    - [todo](#todo)\n    - [todo ls](#todo-ls)\n    - [todo serve](#todo-serve)\n    - [todo config](#todo-config)\n    - [todo info](#todo-info)\n    - [todo utils](#todo-utils)\n  - [Configuration](#configuration)\n  - [Changelog](#changelog)\n  - [Migration Guide](#migration-guide)\n  - [Why do you made this?](#why-do-you-made-this)\n  - [SQLite database schema](#sqlite-database-schema)\n  - [Screenshots](#screenshots)\n\n## Features\n- Creating, reading, updating, and deleting todos;\n- Nicely formatting the outputs (with color);\n- `todo ls` lists all todos, ordered by priority and due date, the todos without a due date are put last (nullslast).\n- Not only the command line interface - you can also CRUD your todos by making HTTP requests to the [REST API](#todo-serve).\n\n## Install, Upgrade and Uninstall\n\n### pipx (recommended)\n- Install\n  ```bash\n  pipx install todo-cli-tddschn\n  ```\n- Upgrade\n  ```bash\n  pipx upgrade todo-cli-tddschn\n  ```\n- Uninstall\n  ```bash\n  pipx uninstall todo-cli-tddschn\n  ```\n\nAbout [`pipx`](https://pypa.github.io/pipx)\n\n\n### [pip](https://pypi.org/project/todo-cli-tddschn)\n- Install\n  ```bash\n  pip install todo-cli-tddschn\n  ```\n- Upgrade\n  ```bash\n  pip install --upgrade todo-cli-tddschn\n  ```\n- Uninstall\n  ```bash\n  pip uninstall todo-cli-tddschn\n  ```\n\n\n## Usage\n\n### todo\n\nYou can add, modify, or remove (all) todos with the `todo` command:\n\n```\ntodo --help\n\nUsage: todo [OPTIONS] COMMAND [ARGS]...\n\n  tddschn's command line todo app\n\nOptions:\n  -v, --version         Show the application's version and exit.\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n\nCommands:\n  a        Add a new to-do with a DESCRIPTION.\n  clear    Remove all to-dos.\n  config   Getting and managing the config\n  g        Get a to-do by ID.\n  info     Get infos about todos\n  init     Initialize the to-do database.\n  ls       list all to-dos, ordered by priority and due date.\n  m        Modify a to-do by setting it as done using its TODO_ID.\n  re-init  Re-initialize the to-do database.\n  rm       Remove a to-do using its TODO_ID.\n```\n\n### todo ls\n\nList and filter the todos.\n\n```\ntodo ls --help\n\nUsage: todo ls [OPTIONS] COMMAND [ARGS]...\n\n  list all to-dos, ordered by priority and due date.\n\nOptions:\n  -d, --description TEXT\n  -p, --priority [low|medium|high]\n  -s, --status [todo|done|deleted|cancelled|wip]\n  -pr, --project TEXT\n  -t, --tags TEXT\n  -dd, --due-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]\n  -ddb, --due-date-before [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]\n  -dda, --due-date-after [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]\n  -dab, --date-added-before [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]\n  -daa, --date-added-after [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]\n  -fda, --full-date-added         Include time in the date_added column\n  --help                          Show this message and exit.\n\nCommands:\n  project  Filter to-dos by project.\n  tag      Filter to-dos by tag.\n```\n\n### todo serve\n\nServe the REST API (built with FastAPI)\n\n```\ntodo serve --help\nUsage: todo serve [OPTIONS]\n\n  serve REST API. Go to /docs for interactive documentation on API usage.\n\nOptions:\n  --host TEXT       [default: 127.0.0.1]\n  --port INTEGER    [default: 5000]\n  --log-level TEXT  [default: info]\n  --help            Show this message and exit.\n```\n\n### todo config\n\nGet or edit the configurations\n\n```\ntodo config --help\n\nUsage: todo config [OPTIONS] COMMAND [ARGS]...\n\n  Getting and managing the config\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  db-path  Get the path to the to-do database.\n  edit     Edit the config file. # Opens in default editor\n  path     Get the path to the config file.\n```\n\n### todo info\n\nGet the info and stats about the todos.\n\n```\ntodo info --help\n\nUsage: todo info [OPTIONS] COMMAND [ARGS]...\n\n  Get infos about todos\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count  Get todo counts\n```\n\n### todo utils\n\nUtility commands.\n\n```\ntodo utils --help\nUsage: todo utils [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  export                  Export todos to todo commands that can be used to re-construct your todo database\n  fill-date-added-column  fill date_added column with the current time if it's null # used for migrate to v1.0.0\n```\n\n## Configuration\n\nThe yaml configuration file is located at `todo config path`.\n\nSee [Configuration](migration.md#migrate-to-v200) for the details.\n\n## [Changelog](CHANGELOG.md)\n\n## Migration Guide\n\nYou may find the [migration guide](migration.md) useful if you've upgraded the major version, e.g. from v1.0.0 to v2.0.0.\n\n\n\n## Why do you made this?\n\nFor practicing my python and SQL skills.\n\nIf you're looking for an awesome CLI todo app, try [taskwarrior](https://taskwarrior.org/).\n## SQLite database schema\n\n![schema](images/todo-cli-tddschn-erd-v1.png)\n\n## Screenshots\n\nThanks to @gudauu for these screenshots.\n\n![screenshot](images/v2/ls-add-modify-info.png)\n![screenshot](images/v2/utils-export.png)\n![screenshot](images/v2/add-modify-info.png)\n![screenshot](images/v2/ls-ddb.png)\n![screenshot-2](images/v2/ls.png)\n\n![todo-serve](images/todo-serve.png)\n\n![api-docs](images/api-docs.png)",
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/todo-cli-tddschn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
