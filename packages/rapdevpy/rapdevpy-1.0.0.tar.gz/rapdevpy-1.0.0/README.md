## Rapid Development Library for Python

* [sqlalchemy](https://www.sqlalchemy.org/): database object relationship mapping
* [lxml](https://lxml.de/): parsing XML and HTML
* [networkx](https://networkx.org/): graph, edge and vertex analysis

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
$: pip install dist/rapdevpy-1.0.0-py3-none.any.whl

$: rapdevpy
```

### docs

```
$: poetry shell
$: cd docs
# Note: review source/conf.py and source/index.rst
$: make html
# Note: see docs in docs/build/apidocs/index.html
```

### rapdevpy

```
$: poetry run python ./rapdevpy/runner.py
```

### tests

```
$: poetry run pytest --durations=0
```

```
$: poetry run pytest --cov=poetry_template --cov-report=html tests
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
$: poetry run mypy ./rapdevpy ./tests
```

### cProfile

```
$: poetry run python ./rapdevpy/profiler.py
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
https://pypi.org/project/rapdevpy/
```
