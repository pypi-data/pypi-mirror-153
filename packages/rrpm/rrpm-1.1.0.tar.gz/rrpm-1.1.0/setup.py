# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrpm',
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
    'version': '1.1.0',
    'description': 'A tool to manage all your projects easily!',
    'long_description': '# rrpm\n\n**rrpm** is the all-in-one project and remote repository management tool. A simple CLI tool that supports project\ngeneration for multiple languages, along with support for generating projects using different package managers and/or\nenvironments\n\n## Installation\n\n`rrpm` can be installed from PyPI\n\n```bash\npip install rrpm\n```\n\n## Usage\n\n```bash\nUsage: python -m rrpm [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n\nCommands:\n  create  Generate a project from any of the presets and/or its variations\n  get     Clone a remote repository to directory specified in config\n  list    List all cloned repositories and generated projects\n```\n\n## Presets\n - [ ] Python\n   - [x] Pip\n     - [x] Python Package\n     - [x] FastAPI\n     - [x] Flask\n   - [x] Poetry\n     - [x] Python Package\n     - [x] FastAPI\n     - [x] Flask\n   - [ ] Virtual Environments\n     - [ ] Python Package\n     - [ ] FastAPI\n     - [ ] Flask\n - [ ] JavaScript\n    - [ ] NPM\n      - [ ] NodeJS\n      - [x] ReactJS\n        - [x] create-react-app\n        - [x] Vite\n      - [x] NextJS\n    - [ ] Yarn\n      - [ ] NodeJS\n      - [x] ReactJS\n        - [x] create-react-app\n        - [x] Vite\n      - [x] NextJS\n    - [ ] Pnpm\n      - [ ] NodeJS\n      - [ ] ReactJS\n        - [ ] create-react-app\n        - [x] Vite\n      - [x] NextJS\n - [ ] TypeScript\n     - [ ] NPM\n       - [ ] NodeJS\n       - [x] ReactJS\n         - [x] create-react-app\n         - [x] Vite\n       - [x] NextJS\n     - [ ] Yarn\n       - [ ] NodeJS\n       - [x] ReactJS\n         - [x] create-react-app\n         - [x] Vite\n       - [x] NextJS\n     - [ ] Pnpm\n       - [ ] NodeJS\n       - [ ] ReactJS\n         - [ ] create-react-app\n         - [x] Vite\n       - [x] NextJS\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'pybash1',
    'author_email': 'example@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pybash1/rrpm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
