# aioAseko package 
[![PyPI](https://img.shields.io/pypi/v/aioaseko)](https://pypi.org/project/aioaseko/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioaseko) [![PyPI - License](https://img.shields.io/pypi/l/aioaseko?color=blue)](https://github.com/milanmeu/aioaseko/blob/main/COPYING)

An async Python wrapper for the Aseko Pool Live API.

The library supports Aseko ASIN AQUA devices.
The Aseko ASIN Pool is partially supported.
The library is currently limited to a selection of features available on aseko.cloud.


## Installation
```bash
pip install aioaseko
```

## Usage
### Import
```python
from aioaseko import Aseko
```

### Create an `Aseko` instance and login
```python
api = Aseko("aioAseko@example.com", "passw0rd")
await api.login()
```

## Example
```python
from asyncio import run

from aioaseko import Aseko, InvalidCredentials, Unit

async def main():
    api = Aseko("aioAseko@example.com", "passw0rd")
    try:
        await api.login()
    except InvalidCredentials:
        print("The username or password is wrong.")
        return
    units = await api.get_units()
    for unit in units:
        if isinstance(unit, Unit):
            print(f"Unit: {unit.name} ({unit.serial_number})")
            print(f"Air temperature: {unit.air_temperature}")
            print(f"Water flow to probes: {unit.water_flow_to_probes}")
run(main())
```
