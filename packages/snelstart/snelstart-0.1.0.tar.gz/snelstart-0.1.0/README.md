<p align="center">
  <img alt="logo" src="https://www.zypp.io/static/assets/img/logos/zypp/white/500px.png"  width="200"/>
</p>

SnelStart
===
> Package for pulling datasets using the Snelstart API and exporting them to a pandas dataframe.


[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/snelstart)](https://pypi.org/project/snelstart/)
[![Latest release](https://badgen.net/github/release/zypp-io/snelstart)](https://github.com/zypp-io/snelstart/releases)


## Installation
```commandline
pip install snelstart
```

## Usage
for an extensive list of examples, please refer to the [Snelstart test suite](snelstart/tests/test_snelstart.py).
for snelstart api documentation, see [Snelstart developers portal](https://b2bapi-developer.snelstart.nl/docs/services)

### request any endpoint from the documentation.
This operation will return a json dataset.

```python
from snelstart import SnelStart

snel = SnelStart(module="artikelen")
data = snel.request_data()
```

### use preformatted sets
These will return a pandas DataFrame

```python
from snelstart import SnelStart

snel = SnelStart(module="artikelen")
df = snel.get_data()
```

## environment variables
The following environment variables need to be set:
- SNELSTART_CLIENT_KEY: the client key of the administration
- SNELSTART_SUBSCRIPTION_KEY: the subscription key of the application supplier.
