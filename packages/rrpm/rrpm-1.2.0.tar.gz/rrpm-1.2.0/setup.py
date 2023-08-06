# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrpm',
 'rrpm.ext',
 'rrpm.presets',
 'rrpm.presets.js',
 'rrpm.presets.py',
 'rrpm.presets.ts']

package_data = \
{'': ['*']}

install_requires = \
['questionary>=1.10.0,<2.0.0',
 'rich>=12.4.4,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['rrpm = rrpm.rrpm:cli']}

setup_kwargs = {
    'name': 'rrpm',
    'version': '1.2.0',
    'description': 'A tool to manage all your projects easily!',
    'long_description': '<br/>\n<p align="center">\n    <a href="https://github.com/pybash1/rrpm" target="_blank">\n        <img width="50%" src="https://raw.githubusercontent.com/pybash1/rrpm/master/extra/banner.png" alt="RRPM logo">\n    </a>\n</p>\n<br/>\n<p align="center">\n    <a href="LICENSE" target="_blank">\n        <img src="https://img.shields.io/github/license/pybash1/rrpm.svg" alt="GitHub license">\n    </a>\n    <a href="https://github.com/pybash1/rrpm/releases" target="_blank">\n        <img src="https://img.shields.io/github/tag/pybash1/rrpm.svg" alt="GitHub tag (latest SemVer)">\n    </a>\n    <a href="https://github.com/pybash1/rrpm/commits/" target="_blank">\n        <img src="https://img.shields.io/github/commit-activity/y/pybash1/rrpm.svg" alt="GitHub commit activity">\n    </a>\n    <a href="https://github.com/pybash1/rrpm/graphs/contributors" target="_blank">\n        <img src="https://img.shields.io/github/contributors-anon/pybash1/rrpm.svg" alt="GitHub contributors">\n    </a>\n</p>\n<br/>\n\n[**RRPM**](https://github.com/pybash1/rrpm) is the **all-in-one project and remote repository management tool**. A \nsimple CLI tool that supports project generation for multiple languages, along with support for generating projects\nusing different package managers and/or environments. This repository contains the **core CLI source code**.\n\n## 🚀 Installation && Documentation\n\n`rrpm` can be installed from PyPI\n\n```bash\npip install rrpm\n```\n\nComplete documentation is still unavailable! Feel free to contribute it!\n\n## Usage\n\n```bash\nUsage: python -m rrpm [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n\nCommands:\n  create  Generate a project from any of the presets and/or its variations\n  get     Clone a remote repository to directory specified in config\n  list    List all cloned repositories and generated projects\n```\n\n## ❤️ Community and Contributions\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## 📫 Have a question? Want to chat? Ran into a problem?\nWe are happy to welcome you in our official [Discord server](https://discord.gg/FwsGkZAqcZ) or answer your questions via [GitHub Discussions](https://github.com/pybash1/rrpm/discussions)!\n\n## 🤝 Found a bug? Missing a specific feature?\nFeel free to **file a new issue** with a respective title and description on the the [pybash1/rrpm](https://github.com/pybash1/rrpm/issues) repository. If you already found a solution to your problem, **we would love to review your pull request**!\n\n## ✅ Requirements\nRRPM requires Python >=3.7\n\n## Presets\n - [ ] Python\n   - [x] Pip\n     - [x] Python Package\n     - [x] FastAPI\n     - [x] Flask\n   - [x] Poetry\n     - [x] Python Package\n     - [x] FastAPI\n     - [x] Flask\n   - [ ] Virtual Environments\n     - [ ] Python Package\n     - [ ] FastAPI\n     - [ ] Flask\n - [ ] JavaScript\n    - [ ] NPM\n      - [ ] NodeJS\n      - [x] ReactJS\n        - [x] create-react-app\n        - [x] Vite\n      - [x] NextJS\n    - [ ] Yarn\n      - [ ] NodeJS\n      - [x] ReactJS\n        - [x] create-react-app\n        - [x] Vite\n      - [x] NextJS\n    - [ ] Pnpm\n      - [ ] NodeJS\n      - [ ] ReactJS\n        - [ ] create-react-app\n        - [x] Vite\n      - [x] NextJS\n - [ ] TypeScript\n     - [ ] NPM\n       - [ ] NodeJS\n       - [x] ReactJS\n         - [x] create-react-app\n         - [x] Vite\n       - [x] NextJS\n     - [ ] Yarn\n       - [ ] NodeJS\n       - [x] ReactJS\n         - [x] create-react-app\n         - [x] Vite\n       - [x] NextJS\n     - [ ] Pnpm\n       - [ ] NodeJS\n       - [ ] ReactJS\n         - [ ] create-react-app\n         - [x] Vite\n       - [x] NextJS\n\n## 📘 License\n\nThe RRPM tool is released under the under terms of the [MIT License](https://choosealicense.com/licenses/mit/).\n',
    'author': 'pybash1',
    'author_email': 'example@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pybash.gitbook.io/rrpm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
