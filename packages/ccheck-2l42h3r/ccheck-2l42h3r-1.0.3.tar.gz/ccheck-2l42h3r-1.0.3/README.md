# ccheck

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=2l42h3r_c-check&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=2l42h3r_c-check)

Tool for generating and checking simple C language exercises.

## Requirements
* at least Python 3.7
* Pip installed

## Install from pip
```python -m pip install ccheck-2l42h3r```

## Running from source without building

Install dependencies:

```python -m pip -r requirements.txt```

Add project to PYTHONPATH (this depends on OS)

Run project as module:

```python -m src.ccheck```

## Build from source

Install dependencies:

```python -m pip -r requirements.txt```

Install/update build tools:

```python -m pip install --upgrade build```

Build:

```python -m build```


Files will be outputted to dist/

## Install local package build

```python -m pip install dist/ccheck_2l42h3r-VERSION-*.whl```