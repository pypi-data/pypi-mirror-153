# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpd', 'gpd.models', 'gpd.parsers']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.9.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['gpd = gpd.runner:run']}

setup_kwargs = {
    'name': 'gpd',
    'version': '1.0.1',
    'description': 'Get a list of popular projects that use a library.',
    'long_description': "## GPD: Get Popular Dependents\n\nWant to know which popular projects use a GitHub library? GPD helps you find how popular projects use your favourite library.  \n\n## Install\n\n```\n$: pip install gpd\n```\n\n## Usage\n\n```\n$: gpd --help\nusage: gpd [-h] -o OWNER -n NAME [-m [MAX_PAGE]]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OWNER, --owner OWNER\n                        Project owner. For example 'github' in 'https://github.com/github/advisory-database'.\n  -n NAME, --name NAME  Project name. For example 'advisory-database' in 'https://github.com/github/advisory-database'.\n  -m [MAX_PAGE], --max_page [MAX_PAGE]\n                        How many pages of dependents do you want to parse before finishing. Default is sys.maxsize, infinity.\n```\n\n```\n$: poetry run gpd -o  samuelcolvin -n pydantic\nname                             stars    forks  author          url\n-----------------------------  -------  -------  --------------  ---------------------------------------------------------\nansible                          53318    21956  ansible         https://github.com/ansible/ansible\nspaCy                            23504     3840  explosion       https://github.com/explosion/spaCy\nray                              20707     3597  ray-project     https://github.com/ray-project/ray\njina                             14697     1919  jina-ai         https://github.com/jina-ai/jina\nrasa                             14068     4004  RasaHQ          https://github.com/RasaHQ/rasa\naiohttp                          12471     1768  aio-libs        https://github.com/aio-libs/aiohttp\nOpenBBTerminal                   12086     1295  OpenBB-finance  https://github.com/OpenBB-finance/OpenBBTerminal\ndgl                               9702     2287  dmlc            https://github.com/dmlc/dgl\npandas-profiling                  9037     1319  ydataai         https://github.com/ydataai/pandas-profiling\nfull-stack-fastapi-postgresql     9027     1622  tiangolo        https://github.com/tiangolo/full-stack-fastapi-postgresql\nlabel-studio                      8943     1065  heartexlabs     https://github.com/heartexlabs/label-studio\nludwig                            8340      986  ludwig-ai       https://github.com/ludwig-ai/ludwig\nPySyft                            8140     1818  OpenMined       https://github.com/OpenMined/PySyft\nsqlmodel                          7466      304  tiangolo        https://github.com/tiangolo/sqlmodel\nvaex                              7094      548  vaexio          https://github.com/vaexio/vaex\nrobotframework                    7008     1977  robotframework  https://github.com/robotframework/robotframework\nairbyte                           6924     1359  airbytehq       https://github.com/airbytehq/airbyte\ndoccano                           6230     1315  doccano         https://github.com/doccano/doccano\nedx-platform                      6017     3277  openedx         https://github.com/openedx/edx-platform\nDeepPavlov                        5754     1034  deepmipt        https://github.com/deepmipt/DeepPavlov\n```\n\nNote: you can only search libraries published on GitHub. For example, you cannot find which GitHub projects use Python's [asyncio](https://docs.python.org/3/library/asyncio.html).  \n\n## Development\n\n```\n# Note: Install Python 3\n# Update pip and install virtualenv (dependency encapsulator) and black (linter; IDE needs to be restarted)\n\n# Note: install Poetry for Linux\n$: curl -sSL https://install.python-poetry.org | python3 -\n\n# Note: install Poetry for Windows\n$: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -\n\n$: curl -sSL https://install.python-poetry.org | python3 - --uninstall\n```\n\n```\n$: poetry install  # install all dependencies\n```\n\n### dist\n\n```\n$: pip install dist/gpd-1.0.1-py3-none.any.whl\n\n$: gpd\n```\n\n### docs\n\n```\n$: poetry shell\n$: cd docs\n# Note: review source/conf.py and source/index.rst\n$: make html\n# Note: see docs in docs/build/apidocs/index.html\n```\n\n### gpd\n\n```\n$: poetry run gpd --help\n```\n\n### tests\n\n```\n$: poetry run pytest --durations=0\n```\n\n```\n$: poetry run pytest --cov=gpd --cov-report=html tests\n# Note: see coverage report in htmlcov/index.html\n# Note: exclude directories from coverage report through .coveragerc\n```\n\n### poetry.lock\n\nDependencies, Python version and the virtual environment are managed by `Poetry`.\n\n```\n$: poetry search Package-Name\n$: poetry add [-D] Package-Name[==Package-Version]\n```\n\n### pyproject.toml\n\nDefine project entry point and metadata.\n\n### Linters\n\n```\n$: poetry run black .\n```\n\n### MyPy\n\n```\n$: poetry run mypy ./gpd ./tests\n```\n\n### cProfile\n\n```\n$: poetry run python ./gpd/profiler.py\n```\n\n### Build and publish\n\n```\n$: poetry build\n\n# Note: get the token from your PiPy account\n$: poetry config pypi-token.pypi PyPI-Api-Access-Token\n```\n\n```\n$: poetry publish --build\n```\n\n```\nhttps://pypi.org/project/gpd/\n```\n",
    'author': 'Mislav Jaksic',
    'author_email': 'jaksicmislav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MislavJaksic/get-popular-dependents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
