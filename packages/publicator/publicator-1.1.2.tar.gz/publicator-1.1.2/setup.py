# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['publicator']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'parse>=1.19.0,<2.0.0',
 'semmy>=1.0.0,<2.0.0',
 'tomli==2.0.1',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['publicator = publicator.cli:app']}

setup_kwargs = {
    'name': 'publicator',
    'version': '1.1.2',
    'description': 'A better poetry publish experience.',
    'long_description': '<h1>🗞 Publicator</h1>\n\n> A better `poetry publish` experience.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/publicator)\n![PyPI](https://img.shields.io/pypi/v/publicator)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/publicator)\n![PyPI - License](https://img.shields.io/pypi/l/publicator)\n[![Application Test Suite](https://github.com/nikoheikkila/publicator/actions/workflows/python-package.yml/badge.svg)](https://github.com/nikoheikkila/publicator/actions/workflows/python-package.yml)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/publicator)\n\nWhile [Poetry](https://python-poetry.org) finally brings us a sane solution for publishing and maintaining Python packages, many developers crave for a more _enhanced_ and safer user experience. Publicator aims to offer a convenient method for publishing your everyday libraries.\n\nPublicator has been inspired by Sindre Sorhus\' excellent [`np`](https://github.com/sindresorhus/np) package for Node.js ecosystem and graciously funded by [**Futurice Spice Program**](https://spiceprogram.org).\n\n<h2>Table of Contents</h2>\n\n* [Features](#features)\n* [Prerequisites](#prerequisites)\n* [Install](#install)\n* [Usage](#usage)\n  * [Configuration](#configuration)\n  * [Preview Mode (Dry-Run)](#preview-mode-dry-run)\n  * [Shell Completion](#shell-completion)\n* [Contributing](#contributing)\n\n## Features\n\n* Ensures you are publishing from your release branch (`main` and `master` by default)\n* Ensures the working directory is clean and latest changes are pulled\n* Reinstalls dependencies to ensure your project works with the latest dependency tree\n* Ensures your Python version is supported by the project and its dependencies\n* Runs the tests with custom test script\n* Bumps the version in `pyproject.toml` and creates a Git tag based on it\n* Publishes the new version to [Python Package Index](https://pypi.org) or custom repository\n* Pushes commits and tags (newly & previously created) to your Git server\n* If the project is hosted on GitHub opens a prefilled GitHub Releases draft after publishing\n* Fully configurable via command-line arguments or the `pyproject.toml` file\n* See what will be executed with preview mode, without pushing or publishing anything remotely\n\n## Prerequisites\n\n* **Python 3.8** or later\n* **Poetry 1.1** or later\n* **Git 2.11** or later\n\n## Install\n\nInstall or run directly using `pipx`, which manages an isolated virtual environment for you.\n\n```sh\npipx install publicator\npipx run publicator <version>\n```\n\nAlternatively, add it as dependency to your Poetry project.\n\n```sh\npoetry add --dev publicator\npoetry run publicator <version>\n```\n\n## Usage\n\nPublicator takes one command-line argument indicating the suitable version bump. It follows semantic versioning rules accurately.\n\n```sh\n# Release a new patch version (e.g. 1.0.0 -> 1.0.1)\npublicator patch\n\n# Release a new minor version (e.g. 1.0.1 -> 1.1.0)\npublicator minor\n\n# Release a new major version (e.g. 1.1.0 -> 2.0.0)\npublicator major\n```\n\nRun `publicator --help` to see the full list of supported options:\n\n```plain\n$ publicator --help\n\nUsage: publicator [OPTIONS] version\n\n  Handles publishing a new Python package via Poetry safely and conveniently.\n\nArguments:\n  version  can be a valid semver or one of: patch, minor, major, prepatch,\n           preminor, premajor, prerelease  [required]\n\nOptions:\n  -V, --version\n  --repository name               Custom repository for publishing (must be\n                                  specified in pyproject.toml)\n  --any-branch / --no-any-branch  Allow publishing from any branch  [default:\n                                  no-any-branch]\n  --clean / --no-clean            Ensure you\'re working with the latest\n                                  changes  [default: clean]\n  --tag / --no-tag                Create a new tag for Git  [default: tag]\n  --publish / --no-publish        Publish the package to the registry\n                                  [default: publish]\n  --push / --no-push              Push commits and tags to Git  [default:\n                                  push]\n  --test-script TEXT              Name of the test script to run under the\n                                  current virtual environment  [default:\n                                  pytest -x --assert=plain]\n  --template TEXT                 Commit message template (`%s` will be\n                                  replaced with the new version tag)\n                                  [default: release: %s]\n  --release-draft / --no-release-draft\n                                  Opens a pre-filled GitHub release page with\n                                  browser if the current project is hosted on\n                                  GitHub  [default: release-draft]\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n\n### Configuration\n\nPublicator follows the pleasantly Pythonic way of specifying the configuration within `pyproject.toml` file. Below are the default configuration values.\n\n```toml\n[tool.publicator]\nany-branch    = false\nclean         = true\npublish       = true\npush          = true\nrelease-draft = true\ntag           = true\ntemplate      = "release: %s"\n```\n\nValues passed as command-line arguments take precedence over configuration file values.\n\nConfiguration enables for more granular usage. For example, in CI/CD pipelines you might want to disable publishing the package to registry or disable creating Git tags depending on your use case.\n\n### Preview Mode (Dry-Run)\n\nIf you\'d rather skip on everything and check what would be executed, you can activate a preview mode via environment variable like so:\n\n```sh\nPUBLICATOR_PREVIEW=true publicator <version>\n```\n\n### Shell Completion\n\nPublicator stands on the shoulders of [Typer](https://typer.tiangolo.com), which is a robust CLI library for Python. You can generate <kbd>TAB</kbd> completions for common shells such as Bash, ZSH, Fish, and Powershell.\n\n```sh\npublicator --install-completion <shell>\n```\n\n## Contributing\n\nSee [**here**](CONTRIBUTING.md) for instructions.\n',
    'author': 'Niko Heikkilä',
    'author_email': 'niko.heikkila@futurice.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/publicator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
