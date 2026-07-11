# AGENTS.md: teslajsonpy Codebase Guide for AI Coding Assistants

This file provides AI coding assistants with the essential information needed to understand and work with the teslajsonpy codebase. For detailed information, consult the files in `docs/summary/`.

## Quick Navigation

- **Orientation**: See project overview below
- **API Usage**: See Public API section
- **How Things Work**: See Architecture & Workflows
- **Specific Answers**: Consult `docs/summary/index.md` - it has a detailed navigation guide

---

## Project Overview

**teslajsonpy** is an async Python library for controlling Tesla vehicles and energy systems through the Tesla REST API.

- **Language**: Python 3.7+
- **Version**: 3.13.2
- **License**: Apache-2.0
- **Primary Use**: Home Assistant integration
- **Architecture**: Async layered design with low-level HTTP and high-level orchestration

### Core Concept

```
User Application
        ↓
Controller (orchestrates, caches, throttles)
    ↙       ↓       ↘
TeslaCar  EnergySite  Connection (HTTP/OAuth)
                ↓
        Tesla REST API + WebSocket
```

---

## Directory Organization

```
teslajsonpy/
├── connection.py      (HTTP/OAuth - 645 LOC)
├── controller.py      (Orchestration - 1460 LOC)
├── car.py             (Vehicle model - 1395 LOC)
├── energy.py          (Energy models - 289 LOC)
├── exceptions.py      (Error handling - 142 LOC)
├── teslaproxy.py      (OAuth proxy - 204 LOC)
├── const.py           (Constants - 36 LOC)
├── endpoints.json     (API endpoint definitions)
└── __init__.py        (Public exports)

tests/
├── unit_tests/        (Test files)
└── tesla_mock.py      (Mock implementation)

docs/
├── summary/           (Comprehensive documentation)
│   ├── index.md       ← START HERE for detailed navigation
│   ├── codebase_info.md
│   ├── architecture.md
│   ├── components.md
│   ├── interfaces.md
│   ├── data_models.md
│   ├── workflows.md
│   ├── dependencies.md
│   └── review_notes.md
└── (Sphinx-generated docs)
```

---

## 7 Primary Components

### 1. Connection (connection.py)
Low-level HTTP and WebSocket with OAuth authentication.
- **Key responsibility**: API communication
- **Key methods**: `get_authorization_code_link()`, `post()`, `get()`, `websocket_connect()`
- **Key state**: `access_token`, `refresh_token`, `expiration`

### 2. Controller (controller.py)
High-level orchestration, caching, and polling.
- **Key responsibility**: Vehicle/site management, polling throttling
- **Key methods**: `connect()`, `get_vehicles()`, `update()`, `register_websocket_callback()`
- **Polling strategy**: Adaptive intervals (60s driving, 300s parked, 660s sleeping)

### 3. TeslaCar (car.py)
Vehicle state and command interface.
- **Key responsibility**: Vehicle operations
- **Provides**: 100+ read-only properties (battery, climate, doors, location, etc.)
- **Commands**: 35+ async methods (charge, lock, climate, etc.)

### 4. EnergySite (energy.py)
Energy resource models (Solar, Powerwall, combined).
- **Subclasses**: SolarSite, PowerwallSite, SolarPowerwallSite
- **Provides**: Power data, reserve percent, operation mode
- **Commands**: `set_reserve_percent()`, `set_operation_mode()`, etc.

### 5. Exceptions (exceptions.py)
Custom exception hierarchy and retry decorators.
- **Exceptions**: `TeslaException` (base), `IncompleteCredentials`, `RetryLimitError`
- **Decorators**: `@custom_retry()`, `@custom_retry_except_unavailable()`
- **Error codes**: Maps HTTP status to meaningful messages

### 6. TeslaProxy (teslaproxy.py)
OAuth proxy for authentication flow.
- **Purpose**: Capture OAuth authorization code
- **Key method**: `test_url()` - verify successful authorization

### 7. Constants (const.py)
Application-wide configuration.
- **Polling intervals**: `DRIVING_INTERVAL=60s`, `UPDATE_INTERVAL=300s`, `SLEEP_INTERVAL=660s`
- **API URLs**: Owner API, China regional, WebSocket, OAuth
- **Resource types**: "vehicles", "energy_sites", "battery", "solar"

---

## Public API Quick Reference

### Initialization & Connection

```python
from httpx import AsyncClient
from teslajsonpy import Controller

async with AsyncClient() as session:
    controller = Controller(
        websession=session,
        email="user@example.com",
        password="password",
    )
    await controller.connect()
    vehicles = await controller.get_vehicles()
```

### Vehicle Commands

```python
car = vehicles[0]

# Climate
await car.set_temperature(20)
await car.set_hvac_mode("cool")

# Charging
await car.start_charge()
await car.set_charging_amps(16)

# Access control
await car.lock()
await car.unlock()

# Doors/windows
await car.toggle_frunk()
await car.close_windows()

# Lighting
await car.flash_lights()
await car.honk_horn()
```

### Vehicle Properties (Read-Only)

```python
car.battery_level         # 0-100
car.charging_state        # "Charging", "Complete", "Stopped"
car.inside_temp           # °C
car.is_locked             # bool
car.latitude, longitude   # coordinates
car.speed                 # mph/kph
car.state                 # "online", "offline", "sleeping"
# ...100+ more
```

### Energy Management

```python
sites = await controller.get_energysites()
site = sites[0]

site.solar_power          # Watts
site.battery_power        # Watts
site.grid_power           # Watts

await site.set_reserve_percent(20)
await site.set_operation_mode("self_consumption")
```

---

## Key Patterns

### Pattern 1: Polling Loop

```python
await controller.connect()

while True:
    await controller.update()  # Polls all vehicles
    
    for car in vehicles:
        print(f"{car.display_name}: {car.battery_level}%")
    
    await asyncio.sleep(10)
```

### Pattern 2: Error Handling

```python
try:
    await car.start_charge()
except TeslaException as e:
    if e.code == 408:        # Vehicle unavailable
        await controller.wake_up(vin)
    elif e.code == 401:      # Unauthorized
        await controller.connect()  # Re-authenticate
    elif e.code == 429:      # Rate limited
        await asyncio.sleep(15)
```

### Pattern 3: Real-Time Updates

```python
async def on_update(msg):
    print(f"Update: {msg}")

await controller.register_websocket_callback(on_update)
# Now receive live vehicle updates via WebSocket
```

### Pattern 4: Command with Wake-Up

TeslaCar command methods automatically wake sleeping vehicles before execution.

```python
# If vehicle is sleeping, automatically:
# 1. Wake it up
# 2. Wait for wake (timeout 60s)
# 3. Send command
# 4. Retry on failure (3 times with exponential backoff)
result = await car.start_charge()
```

---

## Important Implementation Details

### Async/Await Requirement
All I/O operations are async. Must be called within `async` context:

```python
async def main():
    # Your code here
    pass

asyncio.run(main())
```

### Polling Strategy (Adaptive)

- **Driving**: 60 seconds
- **Parked, recent activity**: 300 seconds (5 min)
- **Parked, idle**: 600 seconds (10 min)
- **Sleeping**: 660 seconds (don't poll - let vehicle sleep)

### Caching

Controller maintains multi-level cache:
- Full vehicle data from `/vehicles/{id}/data`
- Extracted subsets: `get_climate_params()`, `get_charging_params()`, etc.
- WebSocket updates bypass polling for real-time response

### Authentication

1. **OAuth2 Flow**: 
   - Get authorization URL: `await controller.get_oauth_url()`
   - User grants access
   - Exchange code: `await controller.set_authorization_code(code)`

2. **Token Refresh**:
   - Automatic when expires
   - Check if refreshed: `await controller.is_token_refreshed()`
   - Store for next session: `await controller.get_tokens()`

### Error Recovery

Built-in retry with exponential backoff:
```python
@custom_retry(retries=3, wait_time=1)
async def post(command, **kwargs):
    # Retries: 1s, 2s, 4s wait
```

### Vehicle Wake-Up

Before commands, vehicle is automatically woken if sleeping:
```python
# If vehicle is sleeping:
# 1. POST /api/1/vehicles/{id}/command/wake_up
# 2. Poll every 2 seconds for up to 60 seconds
# 3. Then execute command
```

---

## Common Development Tasks

### Task: Add a New Command

1. Add method to `TeslaCar` class in `car.py`
2. Use `self._send_command(command_name, **params)` pattern
3. Returns dict with `response: {result: bool, reason: str}`
4. Add tests in `tests/unit_tests/test_car.py`

Example:
```python
async def custom_command(self, param1: str) -> dict:
    return await self._send_command(
        "custom_command_endpoint",
        param1=param1
    )
```

### Task: Add a New Property

1. Parse from vehicle_data dict
2. Add `@property` method to `TeslaCar` class
3. Extract from nested structure (charge_state, climate_state, etc.)
4. Return appropriate type

Example:
```python
@property
def my_new_property(self) -> str:
    return self._vehicle_data.get("charge_state", {}).get("my_field", "default")
```

### Task: Handle New Error Code

1. Add mapping to `TeslaException` in `exceptions.py`
2. Map HTTP status code to meaningful message
3. Add retry logic if applicable

### Task: Modify Polling Behavior

1. Adjust intervals in `const.py`
2. Update `_calculate_next_interval()` in `controller.py`
3. Test with multiple vehicle states

---

## Testing Structure

Location: `tests/unit_tests/`

- `test_car.py`: TeslaCar methods and properties
- `test_energy.py`: Energy site operations
- `test_polling_interval.py`: Polling strategy
- `test_exceptions.py`: Error handling

Mock available: `tests/tesla_mock.py` - Use `TeslaMock` for testing without real API

```python
from tests.tesla_mock import TeslaMock

mock = TeslaMock()
controller = Controller(websession=mock.websession, ...)
```

---

## Technology Stack

### Runtime
- **aiohttp**: HTTP with WebSocket
- **httpx**: Async HTTP client
- **orjson**: Fast JSON parsing
- **tenacity**: Retry logic
- **beautifulsoup4**: HTML parsing (OAuth)
- **authcaptureproxy**: OAuth proxy framework

### Development
- **pytest**: Testing
- **mypy**: Type checking
- **black**: Formatting
- **flake8, pylint**: Linting
- **Sphinx**: Documentation

---

## Repo-Specific Tools & Patterns

### Build & Test Commands

```bash
make init      # Install poetry
make coverage  # Run tests with coverage (100% required)
make lint      # Run flake8, pylint, pydocstyle
make typing    # Run mypy type checking
```

### Configuration Files

- `pyproject.toml`: Poetry, black, semantic release config
- `setup.cfg`: pytest, flake8, coverage config
- `pylintrc`: pylint configuration
- `tox.ini`: tox testing environments
- `.coveragerc`: coverage exclusions

### CI/CD

- GitHub Actions workflows in `.github/workflows/`
- Automatic tests on PR
- Semantic versioning enabled
- Auto-deploy to PyPI on release

### Special Patterns

1. **Pattern: Version handling**
   - Single source: `teslajsonpy/__version__.py`
   - Used in: `pyproject.toml` for automatic sync

2. **Pattern: Logging**
   - Module-level logger: `_LOGGER = logging.getLogger(__name__)`
   - Used throughout for debug/info logging

3. **Pattern: Polling interval calculation**
   - Per-vehicle adaptive timing
   - Prevents hammering API
   - Respects sleep state

---

## Configuration & Constants

### API Endpoints

```python
API_URL = "https://owner-api.teslamotors.com"
AUTH_DOMAIN = "https://auth.tesla.com"
WS_URL = "wss://streaming.vn.teslamotors.com/streaming"
```

### Optional: Fleet API (HTTP Proxy)

For modern vehicles:
```python
controller = Controller(
    ...,
    client_id="your_client_id",
    api_proxy_url="https://your-proxy:4430",
    cert_path="/path/to/cert.pem"  # if self-signed
)
```

### Resource Types

```python
RESOURCE_TYPE_BATTERY = "battery"
RESOURCE_TYPE_SOLAR = "solar"
PRODUCT_TYPE_VEHICLES = "vehicles"
PRODUCT_TYPE_ENERGY_SITES = "energy_sites"
```

---

## For Detailed Information

Consult `docs/summary/`:

| File | Contains |
|------|----------|
| **index.md** | Navigation guide for all docs |
| **codebase_info.md** | Project overview, statistics |
| **architecture.md** | System design, data flows, caching |
| **components.md** | Component API reference |
| **interfaces.md** | Public API with usage examples |
| **data_models.md** | Data structures (vehicle, energy, tokens) |
| **workflows.md** | 12 major usage workflows with diagrams |
| **dependencies.md** | All dependencies, why chosen, compatibility |
| **review_notes.md** | Documentation quality assessment |

---

## Custom Instructions

<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->

