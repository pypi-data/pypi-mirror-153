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
$: pip install dist/gpd-1.0.0-py3-none.any.whl

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
