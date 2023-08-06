# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getdeck',
 'getdeck.api',
 'getdeck.deckfile',
 'getdeck.provider',
 'getdeck.provider.k3d',
 'getdeck.provider.kubectl',
 'getdeck.sources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'docker>=5.0.3,<6.0.0',
 'kubernetes>=23.3.0,<24.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'semantic-version>=2.9.0,<3.0.0']

entry_points = \
{'console_scripts': ['deck = getdeck.__main__:main',
                     'setversion = version:set_version']}

setup_kwargs = {
    'name': 'getdeck',
    'version': '0.8.0',
    'description': 'Deck, a CLI that creates reproducible Kubernetes environments for development and testing',
    'long_description': '<div id="top"></div>\n\n<!-- PROJECT SHIELDS -->\n[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n[![Coverage Information][coveralls-shield]][coveralls-url]\n\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/Getdeck/getdeck">\n    <img src="https://github.com/Schille/getdeck/raw/main/docs/static/img/logo.png" alt="Getdeck Logo"/>\n  </a>\n\n  <h3 align="center">Getdeck</h3>\n\n  <p align="center">\n    A CLI that creates reproducible Kubernetes environments for development and testing!\n    <br />\n    <a href="https://getdeck.dev/docs/deck/intro"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://getdeck.dev/docs/deck/getting-started">Getting started</a>\n    ·\n    <a href="https://github.com/Getdeck/getdeck/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/Getdeck/getdeck/issues">Request Feature</a>\n  </p>\n</div>\n\n<!-- TABLE OF CONTENTS -->\n<details>\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n        <li><a href="#running-getdeck">Running Getdeck</a></li>\n        <li><a href="#cleaning-up">Cleaning up</a></li>\n      </ul>\n    </li>\n    <li><a href="#license">License</a></li>\n    <li><a href="#acknowledgments">Acknowledgments</a></li>\n  </ol>\n</details>\n\n<!-- ABOUT THE PROJECT -->\n## About the project\nGetdeck is like docker-compose for Kubernetes: Find a Deckfile that is describing your setup, \nrun `deck get ...` and you are ready to work. No Kubernetes knowledge required.\n\n**Simple to use**  \nJust install the binary executable deck and you are good to go.\n\n**All dependencies managed**  \nHelm, kustomize, k3d, kubectl? Getdeck manages all dependencies for your setup so you don\'t have to.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n### Built with\nGetdeck builds on top of the following popular open-source technologies:\n\n### Docker\n[*Docker*](https://docker.io) is currently used to run all the required tooling from the Kubernetes ecosystem, so you\ndon\'t have to install _everything_ yourself.\n\n### k3d\n[*k3d*](https://k3d.io) is supported to run local Kubernetes cluster. \n\n### kind\n[*kind*](https://kind.sigs.k8s.io/) is supported to run local Kubernetes cluster. \n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- GETTING STARTED -->\n## Getting Started\nYou can easily try Getdeck yourself following this small example.\n\n### Prerequisites\n1) Follow the [installation](https://getdeck.dev/docs/deck/installation) for your preferred platform.\n\n### Running Getdeck\nWe provide a sophisticated demo project you can deploy locally using `Getdeck`:\n\n```bash\ndeck get https://github.com/gefyrahq/gefyra-demos.git\n```\n\nThis might take a few minutes. When it\'s done, open your browser at\n[http://dashboard.127.0.0.1.nip.io:8080/#/workloads?namespace=oauth2-demo](http://dashboard.127.0.0.1.nip.io:8080/#/workloads?namespace=oauth2-demo).\nYou should see a kubernetes dashboard with some information about the namespace we just deployed using `deck`!\n\n### Cleaning up\nTo clean it up (i.e. remove the cluster), just run the following command:\n\n```bash\ndeck remove --cluster https://github.com/gefyrahq/gefyra-demos.git\n```\n\nNow go and write your own [Deckfile](https://getdeck.dev/docs/deckfile/specs)!  \n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## Usage\nThe following actions are available in Getdeck\'s CLI:\n- `get`: setup local development infrastructure, install a [deck](https://getdeck.dev/docs/deck/)\n- `remove`: remove Getdeck\'s development infrastructure and/or just the deck\n- `list`: list the available decks of a [Deckfile](https://getdeck.dev/docs/deckfile/specs)\n- `version`: print the current version and exit\n\n_For more examples, please refer to the [CLI documentation](https://getdeck.dev/docs/deck/for-devs/cli-reference)_\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- LICENSE -->\n## License\nDistributed under the Apache License 2.0. See `LICENSE` for more information.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## Reporting Bugs\nIf you encounter issues, please create a new issue on GitHub or talk to us on the\n[Unikube Slack channel](https://unikubeworkspace.slack.com/). \nWhen reporting a bug please include the following information:\n\nGetdeck version or Git commit that you\'re running (`deck version`),\ndescription of the bug and logs from the relevant `deck` command (if applicable),\nsteps to reproduce the issue, expected behavior.  \nIf you\'re reporting a security vulnerability, please follow the process for reporting security issues.\n\n## Acknowledgments\nGetdeck is sponsored by the [Blueshoe GmbH](https://blueshoe.de).\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/Getdeck/getdeck.svg?style=for-the-badge\n[contributors-url]: https://github.com/Getdeck/getdeck/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/Getdeck/getdeck.svg?style=for-the-badge\n[forks-url]: https://github.com/Getdeck/getdeck/network/members\n[stars-shield]: https://img.shields.io/github/stars/Getdeck/getdeck.svg?style=for-the-badge\n[stars-url]: https://github.com/Getdeck/getdeck/stargazers\n[issues-shield]: https://img.shields.io/github/issues/Getdeck/getdeck.svg?style=for-the-badge\n[issues-url]: https://github.com/Getdeck/getdeck/issues\n[license-shield]: https://img.shields.io/github/license/Getdeck/getdeck.svg?style=for-the-badge\n[license-url]: https://github.com/Getdeck/getdeck/blob/master/LICENSE.txt\n[coveralls-shield]: https://img.shields.io/coveralls/github/Getdeck/getdeck/main?style=for-the-badge\n[coveralls-url]: https://coveralls.io/github/Getdeck/getdeck\n\n\n',
    'author': 'Michael Schilonka',
    'author_email': 'michael@unikube.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://getdeck.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
