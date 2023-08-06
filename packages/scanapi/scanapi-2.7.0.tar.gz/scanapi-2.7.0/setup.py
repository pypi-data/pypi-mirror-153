# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scanapi', 'scanapi.evaluators', 'scanapi.tree']

package_data = \
{'': ['*'], 'scanapi': ['templates/*']}

install_requires = \
['Jinja2>=3.1.0,<3.2.0',
 'MarkupSafe==2.0.1',
 'PyYAML>=6.0,<6.1',
 'appdirs>=1.4.4,<2.0.0',
 'click==8.0.3',
 'curlify2>=1.0.1,<2.0.0',
 'requests==2.26.0',
 'rich==12.1.0']

entry_points = \
{'console_scripts': ['scanapi = scanapi:main']}

setup_kwargs = {
    'name': 'scanapi',
    'version': '2.7.0',
    'description': 'Automated Testing and Documentation for your REST API',
    'long_description': '![](https://github.com/scanapi/design/raw/main/images/github-hero-dark.png)\n\n<p align="center">\n  <a href="https://app.circleci.com/pipelines/github/scanapi/scanapi?branch=main">\n    <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/scanapi/scanapi">\n  </a>\n  <a href="https://codecov.io/gh/scanapi/scanapi">\n    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/scanapi/scanapi">\n  </a>\n  <a href="https://github.com/scanapi/scanapi/actions/workflows/lint.yml/badge.svg">\n    <img alt="LintCheck" src="https://github.com/scanapi/scanapi/workflows/Lint%20check/badge.svg?event=push">\n  </a>\n  <a href="https://github.com/scanapi/scanapi/actions/workflows/run-examples.yml/badge.svg">\n    <img alt="Examples" src="https://github.com/scanapi/scanapi/workflows/ScanAPI%20Examples/badge.svg?event=push">\n  </a>\n  <a href="https://badge.fury.io/py/scanapi">\n    <img alt="PyPI version" src="https://badge.fury.io/py/scanapi.svg">\n  </a>\n\n  <a href="https://discord.scanapi.dev">\n    <img alt="Discord" src="https://img.shields.io/discord/847208162993242162?color=7389D8&label=discord&logo=6A7EC2&logoColor=ffffff&style=flat-square">\n  </a>\n</p>\n\nA library for **your API** that provides:\n\n- Automated Integration Testing\n- Automated Live Documentation\n\nGiven an API specification, written in YAML/JSON format, ScanAPI hits the specified\nendpoints, runs the test cases, and generates a detailed report of this execution - which can also\nbe used as the API documentation itself.\n\nWith almost no Python knowledge, the user can define endpoints to be hit, the expected behavior\nfor each response and will receive a full real-time diagnostic report of the API!\n\n## Contents\n\n- [Contents](#contents)\n- [Requirements](#requirements)\n- [How to install](#how-to-install)\n- [Basic Usage](#basic-usage)\n- [Documentation](#documentation)\n- [Examples](#examples)\n- [Contributing](#contributing)\n\n## Requirements\n\n- [pip][pip-installation]\n\n## How to install\n\n```bash\n$ pip install scanapi\n```\n\n## Basic Usage\n\nYou will need to write the API\'s specification and save it as a **YAML** or **JSON** file.\nFor example:\n\n```yaml\nendpoints:\n  - name: scanapi-demo # The API\'s name of your API\n    path: http://demo.scanapi.dev/api/v1 # The API\'s base url\n    requests:\n      - name: list_all_users # The name of the first request\n        path: users/ # The path of the first request\n        method: get # The HTTP method of the first request\n        tests:\n          - name: status_code_is_200 # The name of the first test for this request\n            assert: ${{ response.status_code == 200 }} # The assertion\n```\n\nAnd run the scanapi command\n\n```bash\n$ scanapi run <file_path>\n```\n\nThen, the lib will hit the specified endpoints and generate a `scanapi-report.html` file with the report results.\n\n<p align="center">\n  <img\n    src="https://raw.githubusercontent.com/scanapi/scanapi/main/images/report-print-closed.png"\n    width="700",\n    alt="An overview screenshot of the report."\n  >\n  <img\n    src="https://raw.githubusercontent.com/scanapi/scanapi/main/images/report-print-opened.png"\n    width="700"\n    alt="A screenshot of the report showing the request details."\n  >\n</p>\n\n## Documentation\n\nThe full documentation is available at [scanapi.dev][website]\n\n## Examples\n\nYou can find complete examples at [scanapi/examples][scanapi-examples]!\n\nThis tutorial helps you to create integration tests for your REST API using ScanAPI\n\n[![Watch the video](https://raw.githubusercontent.com/scanapi/scanapi/main/images/youtube-scanapi-tutorial.png)](https://www.youtube.com/watch?v=JIo4sA8LHco&t=2s)\n\n## Contributing\n\nCollaboration is super welcome! We prepared the [Newcomers Guide][newcomers-guide] to help you in the first steps. Every little bit of help counts! Feel free to create new [GitHub issues][github-issues] and interact here.\n\nLet\'s build it together 🚀🚀\n\n[github-issues]: https://github.com/scanapi/scanapi/issues\n[newcomers-guide]: https://github.com/scanapi/scanapi/wiki/Newcomers\n[pip-installation]: https://pip.pypa.io/en/stable/installing/\n[scanapi-examples]: https://github.com/scanapi/examples\n[website]: https://scanapi.dev\n',
    'author': 'Camila Maia',
    'author_email': 'cmaiacd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://scanapi.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.13,<4.0.0',
}


setup(**setup_kwargs)
