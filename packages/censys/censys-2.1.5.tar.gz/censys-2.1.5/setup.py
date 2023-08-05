# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['censys',
 'censys.asm',
 'censys.asm.assets',
 'censys.asm.risks',
 'censys.cli',
 'censys.cli.commands',
 'censys.common',
 'censys.search',
 'censys.search.v1',
 'censys.search.v2']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.0.1,<3.0.0', 'requests>=2.26.0', 'rich>=10.16.2']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['censys = censys.cli:main']}

setup_kwargs = {
    'name': 'censys',
    'version': '2.1.5',
    'description': 'An easy-to-use and lightweight API wrapper for Censys APIs (censys.io).',
    'long_description': '# Censys Python Library\n\n[![PyPI](https://img.shields.io/pypi/v/censys?color=orange&logo=pypi&logoColor=orange)](https://pypi.org/project/censys/)\n[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue?logo=python)](https://www.python.org/downloads/)\n[![Read the Docs (version)](https://img.shields.io/readthedocs/censys-python/latest?logo=read%20the%20docs)](https://censys-python.readthedocs.io/en/stable/?badge=stable)\n[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-brightgreen?logo=github)](https://github.com/censys/censys-python/discussions)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-organge.svg?logo=git&logoColor=organge)](http://makeapullrequest.com)\n[![License](https://img.shields.io/github/license/censys/censys-python?logo=apache)](https://github.com/censys/censys-python/blob/main/LICENSE)\n\nAn easy-to-use and lightweight API wrapper for Censys APIs ([censys.io](https://censys.io/)). Python 3.7+ is currently supported.\n\n> **Notice:** The Censys Search v1 endpoints are deprecated as of Nov. 30, 2021. Please begin using v2 endpoints to query hosts and certificates and check out our [support center](https://support.censys.io/hc/en-us/sections/360013076551-Censys-Search-2-0) for resources.\n\n## Features\n\n- [Search Censys data](https://censys-python.readthedocs.io/en/stable/usage-v2.html)\n- [Bulk Certificate lookups](https://censys-python.readthedocs.io/en/stable/usage-v1.html#bulk)\n- [Download Bulk Data](https://censys-python.readthedocs.io/en/stable/usage-v1.html#data)\n- [Manage assets, events, and seeds in Censys ASM](https://censys-python.readthedocs.io/en/stable/usage-asm.html)\n- [Command-line interface](https://censys-python.readthedocs.io/en/stable/cli.html)\n\n<a href="https://asciinema.org/a/418153" target="_blank"><img src="https://asciinema.org/a/418153.svg" width="600"/></a>\n\n## Getting Started\n\nThe library can be installed using `pip`.\n\n```sh\npip install censys\n```\n\nTo upgraded using `pip`.\n\n```sh\npip install --upgrade censys\n```\n\nTo configure your search credentials run `censys config` or set both `CENSYS_API_ID` and `CENSYS_API_SECRET` environment variables.\n\n```sh\n$ censys config\n\nCensys API ID: XXX\nCensys API Secret: XXX\n\nSuccessfully authenticated for your@email.com\n```\n\nTo configure your ASM credentials run `censys asm config` or set the `CENSYS_ASM_API_KEY` environment variables.\n\n```sh\n$ censys asm config\n\nCensys ASM API Key: XXX\n\nSuccessfully authenticated\n```\n\n## API Reference and User Guide available on [Read the Docs](https://censys-python.readthedocs.io/)\n\n[![Read the Docs](https://raw.githubusercontent.com/censys/censys-python/main/docs/_static/readthedocs.png)](https://censys-python.readthedocs.io/)\n\n## Resources\n\n- [Source](https://github.com/censys/censys-python)\n- [Issue Tracker](https://github.com/censys/censys-python/issues)\n- [Changelog](https://github.com/censys/censys-python/releases)\n- [Documentation](https://censys-python.rtfd.io)\n- [Discussions](https://github.com/censys/censys-python/discussions)\n- [Censys Homepage](https://censys.io/)\n- [Censys Search](https://search.censys.io/)\n\n## Contributing\n\nAll contributions (no matter how small) are always welcome. See [Contributing to Censys Python](.github/CONTRIBUTING.md)\n\n## Development\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management. Please ensure you have [installed the latest version](https://python-poetry.org/docs/#installation).\n\n```sh\ngit clone git@github.com:censys/censys-python.git\ncd censys-python/\npoetry install\n```\n\n## Testing\n\n```sh\n# Run tests\npoetry run pytest\n# With coverage report\npoetry run pytest --cov-report html\n```\n\n## License\n\nThis software is licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)\n\n- Copyright (C) 2022 Censys, Inc.\n',
    'author': 'Censys, Inc.',
    'author_email': 'support@censys.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
