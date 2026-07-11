# teslajsonpy

[![Version status](https://img.shields.io/pypi/status/teslajsonpy)](https://pypi.org/project/teslajsonpy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python version compatibility](https://img.shields.io/pypi/pyversions/teslajsonpy)](https://pypi.org/project/teslajsonpy)
[![Version on Github](https://img.shields.io/github/v/release/zabuldon/teslajsonpy?include_prereleases&label=GitHub)](https://github.com/zabuldon/teslajsonpy/releases)
[![Version on PyPi](https://img.shields.io/pypi/v/teslajsonpy)](https://pypi.org/project/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dd/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dw/teslajsonpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/teslajsonpy)

Async python module for Tesla API primarily for enabling Home-Assistant.

## Quick Start

```python
import asyncio
from httpx import AsyncClient
from teslajsonpy import Controller

async def main():
    async with AsyncClient() as session:
        controller = Controller(
            websession=session,
            email="user@example.com",
            password="password",
        )
        
        await controller.connect()
        vehicles = await controller.get_vehicles()
        
        if vehicles:
            car = vehicles[0]
            print(f"Vehicle: {car.display_name}")
            print(f"Battery: {car.battery_level}%")
            
            # Start charging
            await car.start_charge()

asyncio.run(main())
```

## Features

### Vehicle Control
- 35+ command methods: start/stop charge, lock/unlock, climate control, seat heaters, doors, windows
- 100+ read-only properties: battery level, temperature, location, charging state, etc.
- Automatic vehicle wake-up before commands
- Retry logic with exponential backoff

### Energy Management
- Monitor solar production, battery power, grid power
- Control Powerwalls and solar systems
- Manage battery reserve, operation mode, export rules

### Real-Time Updates
- WebSocket streaming for live vehicle events
- Or poll with adaptive intervals (60s driving → 660s sleeping)
- Automatic token refresh

### Authentication
- OAuth2 with PKCE for secure authentication
- Token refresh and storage
- Support for Fleet API (HTTP proxy) for modern vehicles

## Installation

```bash
pip install teslajsonpy
```

or with Poetry:

```bash
poetry add teslajsonpy
```

## Documentation

### For Users

- **API Reference**: [Detailed API documentation](docs/summary/interfaces.md)
- **Usage Workflows**: [Common patterns and workflows](docs/summary/workflows.md)
- **Data Structures**: [What the API returns](docs/summary/data_models.md)

### For Developers

- **Architecture Guide**: [System design and components](docs/summary/architecture.md)
- **Component Reference**: [Detailed component APIs](docs/summary/components.md)
- **Dependencies**: [External libraries and integrations](docs/summary/dependencies.md)
- **AI Assistant Guide**: [For AI coding assistants](AGENTS.md)
- **Full Sphinx Docs**: [API docs](https://teslajsonpy.readthedocs.io/en/latest/)

### Documentation Index

For a comprehensive guide to all documentation, see [docs/summary/index.md](docs/summary/index.md)

## Common Tasks

### Get Vehicle State

```python
await controller.update()  # Poll all vehicles
car = (await controller.get_vehicles())[0]

print(f"Battery: {car.battery_level}%")
print(f"Charging: {car.charging_state}")
print(f"Location: {car.latitude}, {car.longitude}")
```

### Execute Command

```python
# Commands automatically wake sleeping vehicles
result = await car.start_charge()
```

### Monitor Real-Time Updates

```python
async def on_update(msg):
    print(f"Vehicle update: {msg}")

await controller.register_websocket_callback(on_update)
```

### Manage Energy

```python
sites = await controller.get_energysites()
site = sites[0]

print(f"Solar: {site.solar_power}W")
print(f"Battery: {site.battery_power}W")

await site.set_reserve_percent(20)
await site.set_operation_mode("self_consumption")
```

## Requirements

- Python 3.7+
- aiohttp, httpx, orjson, tenacity, beautifulsoup4, authcaptureproxy

## Contributing

1.  [Check for open features/bugs](https://github.com/zabuldon/teslajsonpy/issues)
    or [initiate a discussion on one](https://github.com/zabuldon/teslajsonpy/issues/new).
2.  [Fork the repository](https://github.com/zabuldon/teslajsonpy/fork/new).
3.  Install the dev environment: `make init`.
4.  Enter the virtual environment: `poetry shell`
5.  Code your new feature or bug fix. [Developers Reference](DEVELOPERS.md)
6.  Write a test that covers your new functionality.
7.  Update `README.md` with any new documentation.
8.  Run tests and ensure 100% code coverage for your contribution: `make coverage`
9.  Ensure you have no linting errors: `make lint`
10. Ensure you have typed your code correctly: `make typing`
11. Add yourself to `AUTHORS.md`.
12. Submit a [pull request](https://github.com/zabuldon/teslajsonpy/pulls)!

## Credits

Originally inspired by [this code.](https://github.com/gglockner/teslajson)
Also thanks to [Tim Dorr](https://tesla-api.timdorr.com/) for documenting the API. Additional repo scaffolding from [simplisafe-python.](https://github.com/bachya/simplisafe-python)

## License

[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0.
This code is provided as-is with no warranty. Use at your own risk.
