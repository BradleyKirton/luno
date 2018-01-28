# ICE3X Python Library

This ice3x library is a Python package compliant with the ICE3X APi version 2.

This package is essentially a port of the official [PHP client](https://github.com/ICE3X/v2-PHP).

# Quickstart

The ICE3X API has two broad categories of resources, protected and unprotected resources.

In order to access protected resources one needs to create a private and public key under the [account management](https://ice3x.com/account/api) section of their platform.

## Sync client

```python
from ice3x.clients.sync import IceCubedSyncClient

api_key = 'public key'
secret = 'private key'

client = IceCubedSyncClient(api_key=api_key, secret=secret)
client.get_public_trade_list()
```


## Async client

```python
from ice3x.clients.async import IceCubedAsyncClient


api_key = 'public key'
secret = 'private key'

client = IceCubedAsyncClient(api_key=api_key, secret=secret)

def print_data(data: Dict) -> None:
    """prints the json response from an API call"""
    print(data)

d = client.get_public_trade_list()
d.addCallback(print_data)
```

# Installation

The library can be installed from PyPi as follows.

```bash
pip install ice3x
```

The async client is an optional extra and may be installed as follows.

```bash
pip install ice3x[async]
```

To install the version on this repository follow the steps below.

```bash
git clone https://github.com/BradleyKirton/ice3x
cd ice3x
python -m venv env # virtualenv env
source env/bin/activate
pip install . #pip install .[async] for the async client
```


# Developement

Clone the repo and install the package with it's development requirements.

```bash
git clone https://github.com/BradleyKirton/ice3x
cd ice3x
python -m venv env # virtualenv env
source env/bin/activate
pip install -e .[dev]
pytest
```

# TODO

Note this library is still in beta.

- Write documentation
- Write test suite for async client