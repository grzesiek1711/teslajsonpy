# Interfaces & APIs

## Public API Surface

The primary entry point for external users is the `Controller` class, which orchestrates all interactions with the Tesla API.

## Controller API

### Initialization

```python
from httpx import AsyncClient
from teslajsonpy import Controller

async with AsyncClient() as session:
    controller = Controller(
        websession=session,
        email="user@example.com",
        password="password",  # Optional if using token
        access_token=None,     # Optional
        refresh_token=None,    # Optional
    )
```

### Authentication

```python
# OAuth flow
oauth_url = await controller.get_oauth_url()
# User visits URL, grants access
await controller.set_authorization_code(code)

# Or token-based
controller = Controller(
    websession=session,
    access_token=existing_token,
    refresh_token=existing_refresh_token,
    expiration=token_expiration_timestamp,
)
```

### Connection Management

```python
# Connect and start polling
await controller.connect()

# Get OAuth URL for user
oauth_url = await controller.get_oauth_url()

# Set authorization code after user grants
await controller.set_authorization_code(authorization_code)

# Disconnect and cleanup
await controller.disconnect()
```

### Vehicle Management

```python
# Get all vehicles
cars = await controller.get_vehicles()

# Access individual vehicle
car = cars[0]
print(car.display_name)
print(car.vin)

# Get vehicle data
vehicle_data = await controller.get_vehicle_data(vin=car.vin)

# Update all vehicles (polling)
await controller.update()
```

### Vehicle Properties (Read-Only)

```python
# Vehicle identification
car.vin              # str
car.vehicle_id       # int
car.id               # int
car.display_name     # str
car.state            # str ("online", "offline", "sleeping")

# Battery info
car.battery_level               # int (0-100)
car.usable_battery_level        # int (0-100)
car.battery_range               # float (miles/km)
car.ideal_battery_range         # float

# Charging state
car.charging_state              # str ("Charging", "Discharging", "Complete", "Stopped")
car.charge_rate                 # float (miles/km per hour)
car.charge_limit_soc            # int (50-100)
car.charge_energy_added         # float (kWh)
car.charge_miles_added_ideal    # float
car.charge_miles_added_rated    # float

# Climate
car.inside_temp                 # float (°C)
car.outside_temp                # float (°C)
car.is_climate_on               # bool
car.driver_temp_setting         # float
car.passenger_temp_setting      # float
car.defrost_mode                # int

# Location
car.latitude                    # float
car.longitude                   # float
car.heading                     # int (0-359 degrees)
car.speed                       # int (mph/kph)

# Door/Window status
car.is_locked                   # bool
car.is_frunk_closed             # bool
car.is_trunk_closed             # bool
car.door_df, car.door_dr, car.door_pf, car.door_pr  # door open status

# ... 70+ more properties available
```

### Vehicle Commands (Async Methods)

All commands are async and return dict with response from Tesla API.

```python
# Climate control
await car.set_temperature(19.5)
await car.set_hvac_mode("cool")
await car.set_max_defrost(True)
await car.set_climate_keeper_mode(1)
await car.set_cabin_overheat_protection("on")

# Charging
await car.start_charge()
await car.stop_charge()
await car.set_charging_amps(16)
await car.change_charge_limit(80)
await car.set_scheduled_charging(start_time_minutes, True)
await car.set_scheduled_departure(departure_minutes, True)

# Door/Window control
await car.lock()
await car.unlock()
await car.toggle_frunk()
await car.toggle_trunk()
await car.close_windows()
await car.vent_windows()
await car.charge_port_door_open()
await car.charge_port_door_close()

# Seat climate
await car.set_heated_steering_wheel(True)
await car.set_heated_steering_wheel_level(2)
await car.remote_seat_heater_request(seat_type, level)
await car.remote_seat_cooler_request(cooler_type, level)

# Lighting/sounds
await car.flash_lights()
await car.honk_horn()
await car.remote_boombox(sound_type)

# Other
await car.remote_start(password)
await car.wake_up()
await car.trigger_homelink()
await car.set_sentry_mode(True)
await car.set_valet_mode(True, pin="1234")
```

### Energy Site Management

```python
# Get energy sites
sites = await controller.get_energysites()

# Access site
site = sites[0]
print(site.site_name)
print(site.energysite_id)

# Get site data
site_data = await controller.get_site_data(site_id=site.energysite_id)
```

### Energy Site Properties (Read-Only)

```python
# For SolarSite
site.solar_power                # float (Watts)
site.grid_power                 # float (Watts, negative = exporting)
site.load_power                 # float (Watts)
site.site_name                  # str
site.data_available             # bool

# For PowerwallSite
site.battery_power              # float (Watts)
site.grid_status                # str ("Active")
site.backup_reserve_percent     # int (0-100)
site.percentage_charged         # int (0-100)
site.energy_left                # float (Wh)

# For all sites
site.energysite_id              # int
site.resource_type              # str ("solar", "battery")
site.has_solar                  # bool
site.has_battery                # bool
site.has_load_meter             # bool
```

### Energy Site Commands

```python
# Reserve percent (backup power)
await site.set_reserve_percent(20)

# Operation mode
await site.set_operation_mode("self_consumption")  # "self_consumption", "backup", "export"

# Export rule
rule = {
    "enabled": True,
    "export_limit_kw": 5.0,
}
await site.set_export_rule(rule)

# Grid charging
await site.set_grid_charging(enable=True, charge_amps=16)
```

### Real-Time Updates

```python
# Register callback for WebSocket updates
async def on_update(msg):
    print(f"Update received: {msg}")

await controller.register_websocket_callback(on_update)

# Now updates flow in real-time as they occur
```

### Data Access Methods

```python
# Full cached data (by VIN)
climate = await controller.get_climate_params(vin)
# Returns: {"inside_temp", "outside_temp", "is_climate_on", ...}

charging = await controller.get_charging_params(vin)
# Returns: {"charging_state", "charge_rate", "charge_limit_soc", ...}

state = await controller.get_state_params(vin)
# Returns: {"longitude", "latitude", "heading", "speed", ...}

config = await controller.get_config_params(vin)
# Returns: {"vehicle_config": {...}, "gui_settings": {...}}

drive = await controller.get_drive_params(vin)
# Returns drive-related parameters

gui = await controller.get_gui_params(vin)
# Returns: {"gui_distance_units", "gui_range_display", ...}
```

## Connection API (Low-Level)

Used internally by Controller, but available for advanced use cases.

```python
from teslajsonpy import Connection

connection = Connection(
    websession=session,
    email="user@example.com",
    password="password",
    client_id="ownerapi",
    auth_domain="https://auth.tesla.com",
)

# OAuth flow
oauth_url = await connection.get_authorization_code_link()
await connection.get_authorization_code(code)

# Token management
token = await connection.get_bearer_token()
await connection.refresh_access_token()

# API calls
response = await connection.get("/api/1/vehicles")
result = await connection.post(
    "/api/1/vehicles/{id}/command/charge_start",
    id=vehicle_id
)

# WebSocket
async def on_message(msg):
    print(msg)

task = await connection.websocket_connect(on_message, on_error=None)

# Cleanup
await connection.close()
```

## Exception Handling

```python
from teslajsonpy import TeslaException, IncompleteCredentials, RetryLimitError

try:
    await car.start_charge()
except TeslaException as e:
    print(f"Error {e.code}: {e.message}")
    if e.code == 401:  # Unauthorized
        # Refresh token or re-authenticate
        pass
    elif e.code == 408:  # Vehicle unavailable
        # Wake up vehicle
        pass
    elif e.code == 429:  # Rate limited
        # Wait before retrying
        pass
except IncompleteCredentials:
    # Need to authenticate
    pass
except RetryLimitError:
    # Max retries exceeded
    pass
```

## Polling Integration

```python
# Set polling intervals (override defaults)
controller.set_driving_interval_vin(vin, 30)  # 30s when driving
controller.set_update_interval_vin(vin, 120)  # 120s when parked

# Manual update
await controller.update()

# Get last update time
last_update = controller.get_last_update_time()

# Track vehicle online status
is_online = await controller.is_car_online(vin)
```

## OAuth/Token Management

```python
# Get tokens for storage
tokens = await controller.get_tokens()
# Returns: {
#     "access_token": "...",
#     "refresh_token": "...",
#     "expiration": 1234567890
# }

# Check if token refreshed
if await controller.is_token_refreshed():
    # Store new tokens
    pass

# Get expiration time
expiration = await controller.get_expiration()
```

## Fleet API (HTTP Proxy)

```python
# For vehicles requiring HTTP proxy (modern vehicles)
controller = Controller(
    websession=session,
    email=email,
    password=password,
    client_id="your_client_id",  # From Tesla developer portal
    api_proxy_url="https://your-proxy-server:4430",
    cert_path="/path/to/cert.pem",  # If self-signed
)

# Use identically to regular API
await controller.connect()
cars = await controller.get_vehicles()
```

## Typical Usage Pattern

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
        
        # Connect and authenticate
        await controller.connect()
        
        # Register for real-time updates
        await controller.register_websocket_callback(
            lambda msg: print(f"Update: {msg}")
        )
        
        # Get vehicles
        vehicles = await controller.get_vehicles()
        
        if vehicles:
            car = vehicles[0]
            print(f"Vehicle: {car.display_name}")
            print(f"Battery: {car.battery_level}%")
            
            # Start charging
            result = await car.start_charge()
            
            # Poll for updates
            for _ in range(10):
                await controller.update()
                print(f"Charging state: {car.charging_state}")
                await asyncio.sleep(60)
        
        # Cleanup
        await controller.disconnect()

asyncio.run(main())
```

## Import Surface

```python
# Main classes
from teslajsonpy import (
    Controller,
    TeslaCar,
    Connection,
    EnergySite,
    PowerwallSite,
    SolarSite,
    SolarPowerwallSite,
    TeslaProxy,
)

# Exceptions
from teslajsonpy import (
    TeslaException,
    IncompleteCredentials,
    RetryLimitError,
    UnknownPresetMode,
    HomelinkError,
)

# Version
from teslajsonpy import __version__
```
