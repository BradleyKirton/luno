# Luno Python Library

Sync and Async Python 3 clients for the Luno API

# Quickstart

This library includes 2 types of clients, a sync client built using the [requests](https://github.com/requests/requests) library and an async library built with [treq](https://github.com/twisted/treq) and [twisted](https://github.com/twisted/twisted).

## Sync client

```python
from luno.clients.sync import LunoSyncClient

api_key = ''
api_secret = ''

client = LunoSyncClient(api_key=api_key, secret=api_secret)
client.ticker('XBTZAR')
```


## Async client

```python
from typing import Dict
from twisted.internet import reactor
from luno.clients.async import LunoAsyncClient

api_key = ''
api_secret = ''

client = LunoAsyncClient(api_key=api_key, secret=api_secret)
d = client.ticker('XBTZAR') # returns a twisted deferred

def print_data(data: Dict) -> None:
    """prints the json response from an API call"""
    print(data)
        
d.addCallback(print_data)

reactor.run()
```

# Installation

The library can be installed from PyPi as follows.

```bash
pip install luno
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

- Write documentation
- Write test suite for async client