# teslajsonpy Example Application

This folder contains example applications demonstrating how to use the **teslajsonpy** library.

## Files

### `main.py` - Full-Featured Example
Interactive application demonstrating the read-oriented features of the library:
- **Get Vehicle State**: Print every available `TeslaCar` property (all parameters)
- **Monitor Real-Time Updates**: Stream live vehicle events via WebSocket

**Run it:**
```bash
python main.py
```

Then follow the interactive menu to explore features.

## How to Use

### 1. Install dependencies

From the project root:
```bash
pip install -e .
```

Or install httpx separately:
```bash
pip install httpx
```

### 2. Provide your tokens

`main.py` reads tokens from environment variables to avoid the terminal's 1024-character paste limit:

```bash
export TESLA_ACCESS_TOKEN='...'
export TESLA_REFRESH_TOKEN='...'
```

### 3. Run the example

```bash
python main.py
```

### 4. Explore features

The interactive menu lets you:
1. Print all vehicle parameters (battery, temperature, location, charging, doors, etc.)
2. Stream real-time updates from your vehicle

## Key Concepts

### Authentication
Pass existing OAuth tokens to the `Controller`:
```python
controller = Controller(
    websession=session,
    access_token="your_access_token",
    refresh_token="your_refresh_token",
)
await controller.connect()
```

### Building car and energy-site objects
`connect()` only fetches the raw product list. Generate the objects explicitly:
```python
await controller.connect()
await controller.generate_car_objects()
await controller.generate_energysite_objects()

cars = list(controller.cars.values())          # dict {vin: TeslaCar}
sites = list(controller.energysites.values())  # dict {id: EnergySite}
```

### Vehicle State
Once objects are generated, you can read 100+ properties:
```python
car = list(controller.cars.values())[0]
print(car.battery_level)      # 0-100
print(car.charging_state)     # "Charging", "Complete", "Stopped"
print(car.inside_temp)        # °C
print(car.latitude)           # coordinates
print(car.state)              # "online", "offline", "sleeping"
```

To print *every* available parameter, enumerate the read-only properties:
```python
for name in sorted(
    n for klass in type(car).__mro__
    for n, attr in vars(klass).items()
    if isinstance(attr, property)
):
    print(name, getattr(car, name))
```

### Polling vs WebSocket
- **Polling**: Call `await controller.update()` periodically
- **WebSocket**: Register a callback for real-time updates (streaming only starts
  while the vehicle is driving, and requires `enable_websocket=True`)
```python
async def on_update(msg):
    print(msg)

# register_websocket_callback is synchronous and returns the listener index
controller.register_websocket_callback(on_update)
```

### Energy Management
```python
sites = list(controller.energysites.values())
site = sites[0]
print(site.solar_power)   # Watts
print(site.battery_power) # Watts
print(site.grid_power)    # Watts
```

## A Note on Sending Commands

This example is intentionally **read-only** and does not send vehicle commands.

Modern Tesla vehicles (built after ~2021, except pre-2021 Model S/X) require the
**Tesla Vehicle Command Protocol**: commands must be cryptographically signed and
routed through Tesla's Fleet API HTTP proxy. Sending an unsigned command to the
legacy Owner API command endpoints returns **HTTP 403 Forbidden**, even though
read requests still succeed.

To send commands to such a vehicle you must:
1. Register a developer app to obtain a `client_id` with the `vehicle_cmds` scope.
2. Run Tesla's signing proxy ([`teslamotors/vehicle-command`](https://github.com/teslamotors/vehicle-command)).
3. Enroll the proxy's public key with the vehicle.
4. Point the `Controller` at the proxy:
   ```python
   controller = Controller(
       websession=session,
       access_token=access_token,
       refresh_token=refresh_token,
       client_id="your_developer_app_client_id",
       api_proxy_url="https://localhost:4443",
       api_proxy_cert="/path/to/proxy/cert.pem",
   )
   ```

## Error Handling

The library includes retry logic and error handling:
```python
from teslajsonpy import TeslaException

try:
    await controller.update()
except TeslaException as e:
    if e.code == 408:        # Vehicle unavailable
        await controller.wake_up(vin)
    elif e.code == 401:      # Unauthorized
        await controller.connect()  # Re-authenticate
    elif e.code == 429:      # Rate limited
        await asyncio.sleep(15)
```

## Documentation

For detailed documentation, see the project's docs:
- **API Reference**: `docs/summary/interfaces.md`
- **Architecture**: `docs/summary/architecture.md`
- **Workflows**: `docs/summary/workflows.md`
- **Data Models**: `docs/summary/data_models.md`

## Troubleshooting

### App hangs after entering the access token
Do not paste tokens at an interactive prompt. Terminals cap a single input line at
1024 bytes, and Tesla access tokens are longer. Provide tokens via environment
variables or a token file instead (see step 2 above).

### Vehicle shows as "offline" or "sleeping"
The library automatically wakes vehicles before sending commands. You can also manually wake:
```python
await controller.wake_up(vin)
```

### Commands return HTTP 403
Modern vehicles require the Fleet API signing proxy. See "A Note on Sending Commands" above.

### WebSocket updates not arriving
The vehicle must be online and actively driving, and the `Controller` must be
created with `enable_websocket=True`. Not all states support WebSocket streaming.

### Rate limiting (429 errors)
Tesla API has rate limits. The library includes retry logic with exponential backoff. If you hit limits, wait before retrying.

## Requirements

- Python 3.7+
- httpx (async HTTP client)
- Other dependencies installed automatically with `pip install -e .`

## Next Steps

1. Read the [full README.md](../README.md)
2. Check [API Reference](../docs/summary/interfaces.md)
3. Explore [Usage Workflows](../docs/summary/workflows.md)
4. Review [Architecture](../docs/summary/architecture.md)
