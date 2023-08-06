# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv2http']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

entry_points = \
{'console_scripts': ['csv2http = csv2http.core:main',
                     'f2http = csv2http.core:main']}

setup_kwargs = {
    'name': 'csv2http',
    'version': '0.0.0a0',
    'description': 'Make http requests based on a CSV input file',
    'long_description': '# csv2http\n\n[![ci](https://github.com/Kilo59/csv2http/workflows/ci/badge.svg)](https://github.com/Kilo59/csv2http/actions)\n[![pypi version](https://img.shields.io/pypi/v/csv2http.svg)](https://pypi.org/project/csv2http/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nCLI tool and library for making a series of HTTP requests based on a CSV file input.\n\n## Quick start\n\nInstall\n\n```\npip install csv2http\n```\n\nCheck CLI usage\n\n```\n❯ csv2http --help\nusage: csv2http [-h] [-c CONCURRENCY] [--method {POST,PATCH,PUT}] file url\n\nHTTP request for every row of a CSV file\n\npositional arguments:\n  file                  payload csv file\n  url                   URL destination - called with `http` if scheme is absent\n\noptions:\n  -h, --help            show this help message and exit\n  -c CONCURRENCY, --concurrency CONCURRENCY\n                        Maximum number of concurrent requests (default: 25)\n  --method {POST,PATCH,PUT}\n                        HTTP method/verb (default: POST)\n```\n\n### Mockbin Example\n\nMake POST calls to http://mockbin.org from a local csv file.\n\nFirst setup a new `bin`, using [httpie](https://httpie.io/cli), curl or the [web ui](http://mockbin.com/bin/create) and get a bin id.\n\n```\n❯ http POST mockbin.com/bin/create status:=201 statusText=Created httpVersion=HTTP/1.1 headers:=\'[]\' cookies:=\'[]\' \'content[mimeType]\'=application/json --body\n"9e95289e-d048-4515-9a61-07f2c74810f5"\n```\n\nCreate your `my_file.csv` and pass it to `csv2http`.\nUse the returned bin id from before.\n\n```\n❯ csv2http my_file.csv mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5 --concurrency 3\n POST http://mockbin.org/bin/mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5\n  status codes - {200: 3}\n  status codes - {200: 3}\n  status codes - {200: 3}\n  status codes - {200: 1}\n```\n\nCheck the bin log from.\nhttps://mockbin.org/bin/9e95289e-d048-4515-9a61-07f2c74810f5/log\n\n## Roadmap\n\n- [x] As Library - Alpha\n  - [x] parse csv as dictionary/json - Alpha\n  - [x] accept mutator function - Alpha\n  - [x] HTTP POST request with json from csv - Alpha\n  - [x] limit concurrency - Alpha\n  - [ ] non-blocking file IO - ???\n  - [ ] hooks for response results - Beta\n  - [ ] mkdoc docs - Beta\n- [ ] As CLI - Beta\n  - [x] argparse - Alpha\n  - [ ] progress bar - ???\n  - [ ] use dedicated CLI library (typer, rich etc.) - Beta\n  - [ ] Nested fields - V1\n- [ ] Complete Docs - V1\n  - [ ] `create_mockbin.csv` and `example.csv` to use in quickstart - Beta\n  - [ ] examples for using as library\n- [x] GH Actions CI (lint, test, etc.)\n- [ ] GH Actions CD (publish to pypi)\n',
    'author': 'Gabriel Gore',
    'author_email': 'gabriel59kg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kilo59/csv2http',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
