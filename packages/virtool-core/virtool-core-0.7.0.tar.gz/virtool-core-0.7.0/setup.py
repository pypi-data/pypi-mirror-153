# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtool_core', 'virtool_core.data_model', 'virtool_core.models']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles==0.7.0',
 'aioredis>=1.3.0,<2.0.0',
 'arrow==0.15.5',
 'coloredlogs>=15.0.1,<16.0.0',
 'dictdiffer==0.8.1',
 'psutil>=5.8.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'virtool-core',
    'version': '0.7.0',
    'description': 'Core utilities for Virtool.',
    'long_description': '# virtool-core\n\nCore utilities for Virtool and associated packages.\n\n![Tests](https://github.com/virtool/virtool-core/workflows/Tests/badge.svg?branch=master&event=push)\n\n## Install\n\nInstall `virtool_core` with `pip`:\n\n```\npip install virtool-core\n```\n\n## Contributing\n\n### Commits\n\nAll commits must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0) specification.\n\nThese standardized commit messages are used to automatically publish releases using [`semantic-release`](https://semantic-release.gitbook.io/semantic-release)\nafter commits are merged to `main` from successful PRs.\n\n**Example**\n\n```text\nfeat: add API support for assigning labels to existing samples\n```\n\nDescriptive bodies and footers are required where necessary to describe the impact of the commit. Use bullets where appropriate.\n\nAdditional Requirements\n1. **Write in the imperative**. For example, _"fix bug"_, not _"fixed bug"_ or _"fixes bug"_.\n2. **Don\'t refer to issues or code reviews**. For example, don\'t write something like this: _"make style changes requested in review"_.\nInstead, _"update styles to improve accessibility"_.\n3. **Commits are not your personal journal**. For example, don\'t write something like this: _"got server running again"_\nor _"oops. fixed my code smell"_.\n\nFrom Tim Pope: [A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)\n\n### Tests\n\n1. Install Tox\n\n   `tox` is used to run the tests in a fresh virtual environment with all of the test dependencies. To install it use;\n\n   ```shell script\n   pip install tox tox-poetry\n   ```\n\n2. Run Tests\n\n   ```shell script\n   tox\n   ```\n\nAny arguments given to tox after a `--` token will be supplied to pytest:\n```shell script\ntox -- --log-cli-level=DEBUG\n```\n\n### Documentation\n\nFor docstrings, use the [**Sphinx** docstring format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).\n\nBuild the documentation with:\n```shell script\ncd sphinx && make html\n```\n\nThe rendered HTML files are found under `sphinx/build/html`\n\n\n',
    'author': 'Ian Boyes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/virtool/virtool-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
