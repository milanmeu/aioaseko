# aioAseko package 
[![PyPI](https://img.shields.io/pypi/v/aioaseko)](https://pypi.org/project/aioaseko/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioaseko) [![PyPI - License](https://img.shields.io/pypi/l/aioaseko?color=blue)](https://github.com/milanmeu/aioaseko/blob/main/COPYING)

An async Python wrapper for the Aseko Pool Live API.

The library is currently limited to the features available on pool.aseko.com.

## Account
The library provides a `MobileAccount` and `WebAccount` class to make authenticated requests to the mobile and web API, respectively.
In this version of aioAseko, `WebAccount` can only be used to obtain `AccountInfo` and retrieve the account units.
The mobile API does not provide `AccountInfo`, so `MobileAccount.login()` will return `None`.

## Installation
```bash
pip install aioaseko
```

## Usage
### Import
```python
from aioaseko import MobileAccount
```

### Create a `aiohttp.ClientSession` to make requests
```python
from aiohttp import ClientSession
session = ClientSession()
```

### Create a `MobileAccount` instance and login
```python
account = MobileAccount(session, "aioAseko@example.com", "passw0rd")
await account.login()
```

## Example
```python
from aiohttp import ClientSession
from asyncio import run

import aioaseko

async def main():
    async with ClientSession() as session:
        account = aioaseko.MobileAccount(session, "aioAseko@example.com", "passw0rd")
        try:
            await account.login()
        except aioaseko.InvalidAuthCredentials:
            print("The username or password you entered is wrong.")
            return
        units = await account.get_units()
        for unit in units:
            print(unit.name)
            await unit.get_state()
            print(f"Water flow: {unit.water_flow}")
            for variable in unit.variables:
                print(variable.name, variable.current_value, variable.unit)
        await account.logout()
run(main())
```
