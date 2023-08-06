# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tw_hooks', 'tw_hooks.base_hooks', 'tw_hooks.hooks', 'tw_hooks.scripts']

package_data = \
{'': ['*']}

install_requires = \
['bubop==0.1.8', 'tasklib']

entry_points = \
{'console_scripts': ['install-hook-shims = '
                     'tw_hooks.scripts.install_hook_shims:main']}

setup_kwargs = {
    'name': 'tw-hooks',
    'version': '0.1.1',
    'description': 'Collection of Taskwarrior hooks',
    'long_description': '# Taskwarrior Hooks\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/bergercookie/tw-hooks/master/misc/logo.png"/>\n</p>\n\nTODO Register app in coveralls - set COVERALLS_REPO_TOKEN\n\n<a href="https://github.com/bergercookie/tw-hooks/actions" alt="CI">\n<img src="https://github.com/bergercookie/tw-hooks/actions/workflows/ci.yml/badge.svg" /></a>\n<a href="https://github.com/pre-commit/pre-commit">\n<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>\n\n<a href=\'https://coveralls.io/github/bergercookie/tw-hooks?branch=master\'>\n<img src=\'https://coveralls.io/repos/github/bergercookie/tw-hooks/badge.svg?branch=master\' alt=\'Coverage Status\' /></a>\n<a href="https://github.com/bergercookie/tw-hooks/blob/master/LICENSE.md" alt="LICENSE">\n<img src="https://img.shields.io/github/license/bergercookie/tw-hooks.svg" /></a>\n<a href="https://pypi.org/project/tw_hooks/" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/tw-hooks.svg" /></a>\n<a href="https://badge.fury.io/py/tw_hooks">\n<img src="https://badge.fury.io/py/tw_hooks.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/tw_hooks">\n<img alt="Downloads" src="https://pepy.tech/badge/tw_hooks"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nThis is a collection of [Taskwarrior\nhooks](https://taskwarrior.org/docs/hooks_guide.html) that I use in my\nday-to-day workflows. It comes along a detection and easy-registration mechanism\nthat should make it easy to develop and then distribute your own hooks. The\nhooks are structured as classes under the `tw_hooks/hooks` directory.\n\n## Installation\n\nInstall it from `PyPI`:\n\n```sh\npip3 install --user --upgrade tw_hooks\n```\n\nTo get the latest version install directly from source:\n\n```sh\npip3 install --user --upgrade git+https://github.com/bergercookie/tw-hooks\n```\n\nAfter the installation, you have to run the `install_hook_shims` executable\n(which by this point should be in your `$PATH`). Running it will create shims\n(thin wrapper scripts) under `~/.task/hooks` in order to register all the hooks\nwith Taskwarrior.\n\n## Available hooks\n\nCurrently the following hooks are available:\n\nTODO\n\n## Structure of a Hook\n\nThe purpose of this package is to facilitate the development and distribution of\nTaskwarrior hooks. To this purpose `install_hook_shims` allows you to easily\nregister your own hooks, without having to manually copy items over to the\ntaskwarrior hooks location. `install_hook_shims` will install a shim which will\ncall your hook automatically when required.\n\nThis is an example of a Taskwarrior hook that will be executed on Taskwarrior\nexit:\n\n```python\nfrom tw_hooks import OnExitHook\nclass WarnOnTaskCongestion(OnExitHook):\n    """Warn the user if there are too many tasks."""\n    def _on_exit(self, _):  # <--- Mandatory to implement this signature\n      # ...\n      return 0\n```\n\nAssuming that this hook is in a module called `warn_on_task_congestion.py` and\nthat the directory of this module is in your python path (e.g., by adding it\nexplicitly to `$PYTHONPATH`), then you can run the following to register your\nhook with taskwarrior:\n\n```sh\ninstall_hook_shims -r warn_on_task_congestion\n```\n\nDuring your next Taskwarrior operation, if there are too many due:today tasks,\nyou should see something like this:\n\n```sh\nt add +test kalimera\nCreated task 719.\n[WarnOnTaskCongestion] Too many due:today tasks [threshold=9]\n```\n\n## Hooks API\n\nTODO\n\n## Usage instructions for `install_hook_shims`\n\nTODO\n\n## Miscellaneous\n\n- [Contributing Guide](CONTRIBUTING.md)\n\n## Self Promotion\n\nIf you find this tool useful, please [star it on\nGithub](https://github.com/bergercookie/tw-hooks)\nand consider donating.\n\n## Support\n\nIf something doesn\'t work, feel free to open an issue. You can also find me in\nthe [#taskwarrior Libera Chat](https://matrix.to/#/#taskwarrior:libera.chat).\n\n## TODO List\n\nSee [ISSUES\nlist](https://github.com/bergercookie/tw-hooks/issues)\nfor the things that I\'m currently either working on or interested in\nimplementing in the near future. In case there\'s something you are interesting\nin working on, don\'t hesitate to either ask for clarifications or just do it and\ndirectly make a PR.\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/tw-hooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
