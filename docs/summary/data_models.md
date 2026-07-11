# Data Models

## Overview

teslajsonpy works with several categories of data:
1. **Vehicle Data** - Complete state from Tesla API
2. **Energy Data** - Power and status from energy sites
3. **Command Responses** - Results from control commands
4. **Authentication Data** - Tokens and credentials

All data is structured as dictionaries parsed from JSON, wrapped in domain objects (TeslaCar, EnergySite).

## Vehicle Data Model

### Root Vehicle Object

```python
{
    "id": 12345,              # Unique ID for this vehicle record
    "vehicle_id": 67890,      # Vehicle-specific ID (different per car)
    "vin": "5YJ3E1EA2JF123456", # Vehicle Identification Number
    "display_name": "My Model 3",
    "option_codes": "...",    # Comma-separated vehicle options
    "color": null,
    "tokens": ["token1", "token2"],  # For WebSocket identification
    "state": "online",        # "online", "offline", "sleeping", "unknown"
    "in_service": false,
    "id_s": "12345",
    "calendar_enabled": true,
    "api_version": 43,
}
```

### Vehicle Data (from `/vehicles/{id}/data`)

Returned by `/api/1/vehicles/{id}/data` endpoint. Contains all vehicle state.

```python
{
    "id": 12345,
    "vehicle_id": 67890,
    "vin": "5YJ3E1EA2JF123456",
    "display_name": "My Model 3",
    "state": "online",
    
    # Compound data objects (see below)
    "charge_state": {...},
    "climate_state": {...},
    "drive_state": {...},
    "gui_settings": {...},
    "vehicle_state": {...},
    "vehicle_config": {...},
}
```

### charge_state

Battery and charging configuration.

```python
{
    "charging_state": "Stopped",           # "Charging", "Discharging", "Stopped", "Complete"
    "fast_charger_type": "Supercharger2",  # Type of charger
    "fast_charger_brand": "Tesla",
    "fast_charger_present": true,
    "battery_range": 234.5,                # Estimated range in miles
    "battery_level": 75,                   # 0-100
    "usable_battery_level": 72,            # Usable percentage
    "max_range_charge_counter": 0,
    "time_to_full_charge": 0.0,            # Hours to full charge
    "charge_rate": 0.0,                    # Miles/km added per hour
    "charge_limit_soc": 80,                # Target charge level (50-100)
    "charge_limit_soc_min": 50,
    "charge_limit_soc_max": 100,
    "charge_limit_soc_std": 90,
    "charge_port_door_open": false,
    "charge_port_latch": "Engaged",        # "Engaged", "Disengaged"
    "charger_actual_current": 0,
    "charger_phases": null,                # null, 1, or 3
    "charger_pilot_current": 32,
    "charger_power": 0,                    # kW
    "charger_voltage": 0,
    "conn_charge_cable": "Locked",         # "Locked", "Unlocked", etc.
    "est_battery_range": 234.5,
    "ideal_battery_range": 267.0,
    "managed_charging_active": false,
    "managed_charging_start_time": null,
    "managed_charging_user_canceled": false,
    "max_range_charge_counter": 0,
    "not_enough_power_to_heat": false,
    "off_peak_charging_enabled": false,
    "off_peak_charging_times": "weeknights",
    "preconditioning_enabled": false,
    "preconditioning_times": "weeknights",
    "scheduled_charging_mode": "Off",      # "Off", "StartAt", "DepartAt"
    "scheduled_charging_pending": false,
    "scheduled_charging_start_time": null,
    "scheduled_departure_time": 0,
    "scheduled_departure_time_minutes": 500,
    "supercharger_session_trip_planner": false,
    "time_to_full_charge": 0.0,
    "timestamp": 1625000000000,
}
```

### climate_state

Temperature and HVAC configuration.

```python
{
    "inside_temp": 21.5,                 # °C, interior temperature
    "outside_temp": 25.0,                # °C, exterior temperature
    "driver_temp_setting": 21.0,         # °C, desired temperature
    "passenger_temp_setting": 21.0,      # °C
    "left_temp_setting": 21.0,
    "right_temp_setting": 21.0,
    "is_climate_on": false,
    "is_preconditioning": false,
    "climate_keeper_mode": "off",        # "off", "on", "dog", "camp"
    "defrost_mode": 0,                   # 0 (off) or 1 (on)
    "fan_status": 0,                     # 0-6, HVAC fan level
    "is_auto_conditioning_on": false,
    "is_battery_heater_on": false,
    "is_battery_preconditioning": false,
    "is_front_defroster_on": false,
    "is_preconditioning": false,
    "is_rear_defroster_on": false,
    "left_seat_heater": 0,               # 0-3
    "right_seat_heater": 0,              # 0-3
    "seat_cooler_left": 0,               # 0-3
    "seat_cooler_right": 0,              # 0-3
    "seat_heater_left": 0,               # 0 (off) to 3 (high)
    "seat_heater_rear_left": 0,
    "seat_heater_rear_right": 0,
    "seat_heater_rear_center": 0,
    "seat_heater_third_row_left": 0,
    "seat_heater_third_row_right": 0,
    "third_row_heaters": [0, 0],
    "steering_wheel_heater": false,
    "wiper_blade_defrost": false,
    "cabin_overheat_protection": "off",  # "off", "On", "ForcedOn"
    "cabin_overheat_protection_actively_cooling": false,
    "cop_activation_temperature": "Medium",
    "timestamp": 1625000000000,
}
```

### drive_state

Position and motion information.

```python
{
    "shift_state": "D",                  # "P", "R", "N", "D", or null
    "speed": 0,                          # MPH or KPH
    "latitude": 40.7128,
    "longitude": -74.0060,
    "heading": 180,                      # 0-359 degrees
    "gps_as_of": 1625000000000,          # Timestamp
    "native_latitude": 40.7128,          # GPS in vehicle's coordinate system
    "native_longitude": -74.0060,
    "native_type": "wgs",
    "native_heading": 180,
    "active_route_traffic_minutes_delay": 0,
    "active_route_minutes_to_arrival": 0,
    "active_route_miles_to_arrival": 0.0,
    "active_route_destination": "",
    "active_route_energy_at_arrival": 50,
    "power": 0,                          # kW (positive = accelerating, negative = braking)
    "timestamp": 1625000000000,
}
```

### vehicle_state

Physical state of doors, windows, etc.

```python
{
    "api_version": 43,
    "autopark_state_v2": "standby",
    "autopark_style": "standard",
    "body_color_rgb": "255,255,255",     # RGB color code
    "body_type": "Model3",
    "brake_type_rear": "Regen",
    "brick_in_gp_u": false,
    "cabin_overheat_protection": "off",
    "cabin_overheat_protection_actively_cooling": false,
    "car_type": "model3",
    "carplay_state": 0,
    "center_display_state": 2,
    "charge_port_door_open": false,
    "charge_port_latch": "Engaged",
    "charging_cable_type": "IEC",        # Type of charging cable
    "charging_state": "Stopped",
    "chest_door_state": null,
    "climate_keeper_mode": "off",
    "dashcam_state": "Recording",        # Sentry/dashcam state
    "dashcam_video_mode": 0,
    "defrost_mode": 0,
    "door_df": 0,                        # Doors: 0 = closed, 1 = open
    "door_dr": 0,
    "door_pf": 0,
    "door_pr": 0,
    "door_rp": 0,                        # Rear passenger
    "door_rd": 0,                        # Rear driver
    "doors_state": [[0, 0], [0, 0], [0, 0], [0, 0]],  # [[front_left, front_right], ...]
    "dt1_state": null,
    "dt2_state": null,
    "epic_type": "ICE",
    "exterior_color": "White",
    "fd_window": 0,                      # Windows: 0 = closed
    "fp_window": 0,
    "front_drive_unit": "Model3DU",
    "front_drive_unit_version": "1AC",
    "front_seat_heaters": 0,
    "front_seat_leg_rests": 0,
    "ft": 0,
    "ft_distance": 0.0,
    "front_torque_sensor": 0.0,
    "front_wheel_type": "Aero18",
    "ft_prl_count": 0,
    "ft_prl_shift": false,
    "gd_state": null,
    "gp_u_version": null,
    "gps_as_of": 1625000000000,
    "gps_signal_strength": null,
    "gt_door_est_pos": null,
    "guest_mode": false,
    "guarded_charge_port_detected": false,
    "has_air_suspension": false,
    "has_ludicrous_mode": false,
    "has_seat_cooling": true,
    "has_seat_heating": true,
    "homelink_device_count": 0,           # Garage door openers
    "homelink_nearby": true,              # Can trigger homelink
    "hood": 0,                            # Frunk
    "hood_state": "Closed",
    "is_user_present": false,
    "last_autopark_error": "no_error",
    "left_drive_unit": "Model3DU",
    "left_drive_unit_version": "1AC",
    "left_power_display": "None",
    "left_seat_belt_status": 0,
    "left_seat_cooler": 0,
    "left_seat_heat_level": 0,
    "left_seat_heater": 0,
    "left_shoulder_camera": "Unknown",
    "left_steering_wheel_heat": 0,
    "left_steering_wheel_heater": false,
    "locked": true,                      # Vehicle locked
    "media_state": {"remote_control_enabled": true},
    "met": "Model3DU",
    "middle_display_state": 0,
    "middle_row_seats": "None",
    "milestone": 5,
    "minor_version": 11,
    "misc_state": 0,
    "model_3": "Std Range",               # Model/variant
    "mp_body_type": "sedan",
    "mute_footwell_lights": false,
    "odometer": 12345.6,                 # Miles/km driven
    "odometer_unit": "mi",
    "opened_doors": [],                  # Names of open doors
    "origin": "5,0",
    "parsed_calendar_supported": true,
    "passenger_seat_belt_status": 0,
    "passenger_temp_setting": 21.0,
    "perf_mode": false,
    "pf_window": 0,
    "pinned_set_group_left": "Unknown",
    "pinned_set_group_right": "Unknown",
    "pr_window": 0,
    "powertrain": "RWD",
    "power_reading_left": 0,
    "power_reading_right": 0,
    "power_state": "Sleep",              # "Drive", "Charge", "Sleep"
    "rd_window": 0,
    "rear_drive_unit": "Model3DU",
    "rear_drive_unit_version": "1AC",
    "rear_power_display": "None",
    "rear_seat_heaters": 1,              # 0-3 or array
    "rear_seat_type": "Heated2Seat",
    "rear_seats": "None",
    "rear_shoulder_camera": "Unknown",
    "rear_trunk_open": 0,                # 1 = open
    "rear_view_mirror_on_rtc": false,
    "remote_start": false,               # Remote start active
    "remote_start_enabled": true,        # Can use remote start
    "remote_start_supported": true,
    "right_drive_unit": "Model3DU",
    "right_drive_unit_version": "1AC",
    "right_power_display": "None",
    "right_seat_belt_status": 0,
    "right_seat_cooler": 0,
    "right_seat_heat_level": 0,
    "right_seat_heater": 0,
    "right_shoulder_camera": "Unknown",
    "right_steering_wheel_heat": 0,
    "right_steering_wheel_heater": false,
    "roof_color": "Colored",
    "roof_state": "Closed",              # "Open", "Closed", "Vent", "Comfort"
    "seat_type": "Heated5Seat",
    "sentry_mode": true,                 # Sentry mode enabled
    "sentry_mode_available": true,       # Can enable sentry
    "service_mode": false,
    "service_mode_plus": false,
    "set_favorite_available": true,
    "side_mirror_heaters": false,
    "side_mirror_state": "normal",
    "software_update": {"install_perc": 0, "status": "", "download_perc": 0},
    "sp_range": 100,
    "speed": 0,
    "stabilimp": false,
    "start_boost_available": false,
    "steering_angle": 0.0,               # Degrees, positive = right
    "steering_wheel_type": "Yoke",
    "sub_type": "A",
    "supercharger_session_trip_planner": false,
    "sun_roof_installed": false,
    "sun_roof_percent_open": null,
    "supports_qr_pairing": true,
    "temperature_unit": "C",
    "third_row_seats": "None",
    "third_row_seating": "None",
    "tint_version": "1.0",
    "touchscreen_enabled": true,
    "touchscreen_version": "MCU3",
    "trailer_connected": null,
    "trunk": 0,                          # Trunk: 0 = closed, 1 = open
    "trunk_state": "Closed",
    "turn_signal_stat": 0,
    "turntable_bound_type": 0,
    "turntable_move_available": false,
    "two_hand_regen": false,
    "type": "vehicle",
    "universal_home_bridge_device_count": 0,
    "updates_available": false,
    "user_notes": "",
    "utc_offset_s": -14400,
    "vehicle_color": "White",
    "vehicle_config": {...},             # See vehicle_config below
    "vehicle_name": "My Tesla",
    "vehicle_self_diagnostics_available": false,
    "vehicle_speed_mph": 0,
    "vins": "5YJ3E1EA2JF123456",
    "vmotion_state": 0,
    "wh_type": "WheelType15",
    "wheel_type": "Aero18",
    "windows_open": [],                  # Names of open windows
    "windshield_wipers": 0,
    "wiper_blade_defrost": false,
    "timestamp": 1625000000000,
}
```

### vehicle_config

Vehicle configuration and capabilities.

```python
{
    "aux_park_latch": "Engaged",
    "badge_version": 0,
    "body_color_rgb": "255,255,255",
    "body_type": "Model3",
    "brake_type_rear": "Regen",
    "cabin_overheat_protection": "Off",
    "cabin_overheat_protection_type": "FAN_ONLY",
    "can_accept_navigation_requests": true,
    "can_store_and_retrieve_drafts_supported": true,
    "car_special_type": "standard",
    "car_type": "model3",
    "dashcam_clip_save_supported": true,
    "default_radar_object_size": "Medium",
    "driver_assist_type": "AutopilotHardware3",
    "epic_type": "ICE",
    "eu_vehicle": false,
    "exterior_color": "White",
    "exterior_trim": "Stealth",
    "exterior_trim_override": "",
    "has_air_suspension": false,
    "has_ludicrous_mode": false,
    "has_seat_cooling": true,
    "has_seat_heating": true,
    "has_spoiler": false,
    "has_third_row_seats": false,
    "headlamp_type": "LED",
    "headlamp_version": "",
    "interior_trim_type": "Black",
    "key_version": 9,
    "motorized_charge_port": true,
    "paint_color_override": "Solid Black",
    "parking_brake_type": "ElectricParking",
    "plg": false,
    "power_liftgate": true,
    "production_date": "2020-06",
    "rear_drive_unit": "Model3DU",
    "rear_seat_heaters": 1,
    "rear_seat_type": "Heated2Seat",
    "rear_seats": "None",
    "release_type": "Release",
    "rear_view_mirror": "HomeLink",
    "reseal_cabin_during_preconditioning": true,
    "right_hand_drive": false,
    "roof_color": "Colored",
    "roof_type": "Metal",
    "seat_type": "Heated5Seat",
    "spoiler_type": "None",
    "steering_wheel_type": "Yoke",
    "sun_roof_installed": false,
    "supports_qr_pairing": true,
    "third_row_seating": "None",
    "touchscreen_version": "MCU3",
    "tpms_hard_warning_fw": "21.37.5",
    "tpms_soft_warning_fw": "21.37.5",
    "trim_badging": "RWD",
    "trim_badging_override": "",
    "use_range_state": "Rated",
    "utc_offset_s": -14400,
    "vehicle_color": "White",
    "wheel_type": "Aero18",
    "windows_type": "AllGlass",
    "wiper_blade_type": "Tesla",
}
```

### gui_settings

Display and interface preferences.

```python
{
    "gui_24_hour_time": false,           # 24-hour time format
    "gui_charge_rate_units": "mi/hr",    # "mi/hr" or "km/hr"
    "gui_distance_units": "mi",          # "mi" or "km"
    "gui_favorite_places": true,
    "gui_range_display": "Rated",        # "Rated", "Ideal", "RangeMode"
    "gui_tiered_charging_enabled": true,
    "gui_tiered_charging_override": "off",
    "show_range_units": true,
    "timestamp": 1625000000000,
}
```

## Energy Data Model

### Energy Site (from `/products` endpoint)

```python
{
    "energy_site_id": 12345,
    "resource_type": "battery",          # "battery", "solar", etc.
    "site_name": "My Home",
    "battery_backup_reserve_percent": 20,
    "backup_reserve_percent": 20,
    "components": {
        "battery": true,
        "solar": true,
        "load_meter": true,
        "grid": true,
    },
    "id": "67890",
    "gateway": {
        "id": "11111",
        "user_id": "22222",
        "password_last_changed_date": "",
        "dipSwitch": {
            "nvmw_rev_major": 3,
            "nvmw_rev_minor": 3,
            "load_shed_enable": true,
            "sync_date_time": true,
        },
        "serial_number": "ABCD1234",
        "type": "Neurio",
        "enumerator": {
            "serial_number": "EFGH5678",
            "type": "Neurio",
        },
    },
}
```

### Energy Site Data (from `/sites/{site_id}/live_status`)

Live power data for energy site.

```python
{
    "solar_power": 2500.5,               # Watts (from solar)
    "battery_power": -500.0,             # Watts (negative = charging, positive = discharging)
    "load_power": 1200.0,                # Watts (home consumption)
    "grid_power": -750.0,                # Watts (negative = exporting, positive = importing)
    "grid_services_power": 0,
    "generator_power": 0,
    "island_status": "not_islanded",
    "timestamp": "2023-07-11T12:00:00-04:00",
    "backup_reserve_percent": 20,
    "percentage_charged": 85,              # For battery
    "energy_left": 45000.0,                # Wh remaining in battery
}
```

## Command Response Model

All command methods return a dictionary with this structure:

```python
{
    "response": {
        "result": true,                  # Success indicator
        "reason": ""                     # Error reason if failed
    }
}
```

Example responses:

```python
# Successful command
{"response": {"result": true, "reason": ""}}

# Unavailable vehicle
{"response": {"result": false, "reason": "could_not_wake_buses"}}

# Mobile access disabled
{"response": null, "error": "mobile access disabled", "error_description": ""}
```

## OAuth Token Model

```python
{
    "access_token": "Bearer token string...",
    "token_type": "Bearer",
    "expires_in": 3600,                  # Seconds until expiration
    "refresh_token": "Refresh token string...",
    "id_token": "JWT ID token string..."
}
```

Stored and tracked by Controller:
```python
{
    "access_token": "...",
    "refresh_token": "...",
    "expiration": 1625003600,            # Unix timestamp
    "token_refreshed": False,             # True if just refreshed
}
```
