## GPD: Get Popular Dependents

Want to know which popular projects use a GitHub library? GPD helps you find how popular projects use your favourite library.  

## Install

```
$: pip install gpd
```

## Usage

```
$: gpd --help
usage: gpd [-h] -o OWNER -n NAME [-m [MAX_PAGE]]

optional arguments:
  -h, --help            show this help message and exit
  -o OWNER, --owner OWNER
                        Project owner. For example 'github' in 'https://github.com/github/advisory-database'.
  -n NAME, --name NAME  Project name. For example 'advisory-database' in 'https://github.com/github/advisory-database'.
  -m [MAX_PAGE], --max_page [MAX_PAGE]
                        How many pages of dependents do you want to parse before finishing. Default is sys.maxsize, infinity.
```

```
$: poetry run gpd -o  samuelcolvin -n pydantic
name                             stars    forks  author          url
-----------------------------  -------  -------  --------------  ---------------------------------------------------------
ansible                          53318    21956  ansible         https://github.com/ansible/ansible
spaCy                            23504     3840  explosion       https://github.com/explosion/spaCy
ray                              20707     3597  ray-project     https://github.com/ray-project/ray
jina                             14697     1919  jina-ai         https://github.com/jina-ai/jina
rasa                             14068     4004  RasaHQ          https://github.com/RasaHQ/rasa
aiohttp                          12471     1768  aio-libs        https://github.com/aio-libs/aiohttp
OpenBBTerminal                   12086     1295  OpenBB-finance  https://github.com/OpenBB-finance/OpenBBTerminal
dgl                               9702     2287  dmlc            https://github.com/dmlc/dgl
pandas-profiling                  9037     1319  ydataai         https://github.com/ydataai/pandas-profiling
full-stack-fastapi-postgresql     9027     1622  tiangolo        https://github.com/tiangolo/full-stack-fastapi-postgresql
label-studio                      8943     1065  heartexlabs     https://github.com/heartexlabs/label-studio
ludwig                            8340      986  ludwig-ai       https://github.com/ludwig-ai/ludwig
PySyft                            8140     1818  OpenMined       https://github.com/OpenMined/PySyft
sqlmodel                          7466      304  tiangolo        https://github.com/tiangolo/sqlmodel
vaex                              7094      548  vaexio          https://github.com/vaexio/vaex
robotframework                    7008     1977  robotframework  https://github.com/robotframework/robotframework
airbyte                           6924     1359  airbytehq       https://github.com/airbytehq/airbyte
doccano                           6230     1315  doccano         https://github.com/doccano/doccano
edx-platform                      6017     3277  openedx         https://github.com/openedx/edx-platform
DeepPavlov                        5754     1034  deepmipt        https://github.com/deepmipt/DeepPavlov
```

Note: you can only search libraries published on GitHub. For example, you cannot find which GitHub projects use Python's [asyncio](https://docs.python.org/3/library/asyncio.html).  

## Development

```
# Note: Install Python 3
# Update pip and install virtualenv (dependency encapsulator) and black (linter; IDE needs to be restarted)

# Note: install Poetry for Linux
$: curl -sSL https://install.python-poetry.org | python3 -

# Note: install Poetry for Windows
$: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

$: curl -sSL https://install.python-poetry.org | python3 - --uninstall
```

```
$: poetry install  # install all dependencies
```

### dist

```
$: pip install dist/gpd-1.0.1-py3-none.any.whl

$: gpd
```

### docs

```
$: poetry shell
$: cd docs
# Note: review source/conf.py and source/index.rst
$: make html
# Note: see docs in docs/build/apidocs/index.html
```

### gpd

```
$: poetry run gpd --help
```

### tests

```
$: poetry run pytest --durations=0
```

```
$: poetry run pytest --cov=gpd --cov-report=html tests
# Note: see coverage report in htmlcov/index.html
# Note: exclude directories from coverage report through .coveragerc
```

### poetry.lock

Dependencies, Python version and the virtual environment are managed by `Poetry`.

```
$: poetry search Package-Name
$: poetry add [-D] Package-Name[==Package-Version]
```

### pyproject.toml

Define project entry point and metadata.

### Linters

```
$: poetry run black .
```

### MyPy

```
$: poetry run mypy ./gpd ./tests
```

### cProfile

```
$: poetry run python ./gpd/profiler.py
```

### Build and publish

```
$: poetry build

# Note: get the token from your PiPy account
$: poetry config pypi-token.pypi PyPI-Api-Access-Token
```

```
$: poetry publish --build
```

```
https://pypi.org/project/gpd/
```
