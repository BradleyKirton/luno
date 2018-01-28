# Luno Python Library

# Quickstart

## Sync client

```python
```


## Async client

```python
```

# Installation

The library can be installed from PyPi as follows.

```bash
```

The async client is an optional extra and may be installed as follows.

```bash
pip install luno[async]
```

To install the version on this repository follow the steps below.

```bash
git clone https://github.com/BradleyKirton/luno
cd luno
python -m venv env # virtualenv env
source env/bin/activate
pip install . #pip install .[async] for the async client
```


# Developement

Clone the repo and install the package with it's development requirements.

```bash
git clone https://github.com/BradleyKirton/luno
cd luno
python -m venv env # virtualenv env
source env/bin/activate
pip install -e .[dev]
pytest
```

# TODO

Note this library is still in beta.

- Write tests
- Write documentation
- Write test suite for async client