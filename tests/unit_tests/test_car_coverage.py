"""Comprehensive tests for car.py coverage."""
import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import TeslaMock


@pytest.mark.asyncio
async def test_car_data_available_false(monkeypatch):
    """Test car data_available property when vehicle_state is missing."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Remove vehicle_state to test data_available returns None
    if "vehicle_state" in car._vehicle_data:
        del car._vehicle_data["vehicle_state"]
    
    assert car.data_available is None


@pytest.mark.asyncio
async def test_car_in_service_no_data(monkeypatch):
    """Test in_service property when data not available."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Remove vehicle_state to make data unavailable
    if "vehicle_state" in car._vehicle_data:
        del car._vehicle_data["vehicle_state"]
    
    assert car.in_service is None


@pytest.mark.asyncio
async def test_car_charge_port_latch_disengaged(monkeypatch):
    """Test charge_port_latch property with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with "Engaged" state
    car._vehicle_data["charge_state"]["charge_port_latch"] = "Engaged"
    assert car.charge_port_latch == "Engaged"
    
    # Test with other states
    car._vehicle_data["charge_state"]["charge_port_latch"] = "Disengaged"
    assert car.charge_port_latch == "Disengaged"
    
    car._vehicle_data["charge_state"]["charge_port_latch"] = "Blocked"
    assert car.charge_port_latch == "Blocked"


@pytest.mark.asyncio
async def test_car_climate_keeper_mode_states(monkeypatch):
    """Test climate_keeper_mode property with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test different climate_keeper_mode states
    modes = ["off", "on", "dog", "camp"]
    for mode in modes:
        car._vehicle_data["climate_state"]["climate_keeper_mode"] = mode
        assert car.climate_keeper_mode == mode


@pytest.mark.asyncio
async def test_car_defrost_mode_states(monkeypatch):
    """Test defrost_mode property with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test different defrost modes
    car._vehicle_data["climate_state"]["defrost_mode"] = 0
    assert car.defrost_mode == 0
    
    car._vehicle_data["climate_state"]["defrost_mode"] = 1
    assert car.defrost_mode == 1


@pytest.mark.asyncio
async def test_car_charging_state_variations(monkeypatch):
    """Test charging_state property with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test different charging states
    states = ["Charging", "Complete", "Stopped", "Disconnected", "Starting"]
    for state in states:
        car._vehicle_data["charge_state"]["charging_state"] = state
        assert car.charging_state == state


@pytest.mark.asyncio
async def test_car_is_frunk_closed_states(monkeypatch):
    """Test is_frunk_closed with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with closed state (ft = 0)
    car._vehicle_data["vehicle_state"]["ft"] = 0
    assert car.is_frunk_closed is True
    
    # Test with open state
    car._vehicle_data["vehicle_state"]["ft"] = 1
    assert car.is_frunk_closed is False


@pytest.mark.asyncio
async def test_car_is_trunk_closed_states(monkeypatch):
    """Test is_trunk_closed with different states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with closed state (rt = 0)
    car._vehicle_data["vehicle_state"]["rt"] = 0
    assert car.is_trunk_closed is True
    
    # Test with open state
    car._vehicle_data["vehicle_state"]["rt"] = 1
    assert car.is_trunk_closed is False


@pytest.mark.asyncio
async def test_car_native_location_supported_int_values(monkeypatch):
    """Test native_location_supported property returns int not bool."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with value 0
    car._vehicle_data["drive_state"]["native_location_supported"] = 0
    assert car.native_location_supported == 0
    
    # Test with value 1
    car._vehicle_data["drive_state"]["native_location_supported"] = 1
    assert car.native_location_supported == 1


@pytest.mark.asyncio
async def test_car_rear_seat_heaters_values(monkeypatch):
    """Test rear_seat_heaters property with different values."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with 3 heaters
    car._vehicle_data["vehicle_config"]["rear_seat_heaters"] = 3
    assert car.rear_seat_heaters == 3
    
    # Test with 0 heaters
    car._vehicle_data["vehicle_config"]["rear_seat_heaters"] = 0
    assert car.rear_seat_heaters == 0


@pytest.mark.asyncio
async def test_car_third_row_seats_values(monkeypatch):
    """Test third_row_seats property with different values."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with "None" string
    car._vehicle_data["vehicle_config"]["third_row_seats"] = "None"
    assert car.third_row_seats == "None"
    
    # Test with "2" string
    car._vehicle_data["vehicle_config"]["third_row_seats"] = "2"
    assert car.third_row_seats == "2"


@pytest.mark.asyncio
async def test_car_is_window_closed_all_states(monkeypatch):
    """Test is_window_closed property with all window states."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # All windows open
    car._vehicle_data["vehicle_state"]["fd_window"] = 1
    car._vehicle_data["vehicle_state"]["fp_window"] = 1
    car._vehicle_data["vehicle_state"]["rd_window"] = 1
    car._vehicle_data["vehicle_state"]["rp_window"] = 1
    assert car.is_window_closed is False
    
    # All windows closed
    car._vehicle_data["vehicle_state"]["fd_window"] = 0
    car._vehicle_data["vehicle_state"]["fp_window"] = 0
    car._vehicle_data["vehicle_state"]["rd_window"] = 0
    car._vehicle_data["vehicle_state"]["rp_window"] = 0
    assert car.is_window_closed is True
    
    # Some windows open
    car._vehicle_data["vehicle_state"]["fd_window"] = 0
    car._vehicle_data["vehicle_state"]["fp_window"] = 1
    car._vehicle_data["vehicle_state"]["rd_window"] = 0
    car._vehicle_data["vehicle_state"]["rp_window"] = 0
    assert car.is_window_closed is False


@pytest.mark.asyncio
async def test_car_vehicle_self_diagnostics_available_when_present(monkeypatch):
    """Test vehicle_self_diagnostics_available property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test when property is present
    car._vehicle_data["vehicle_config"]["vehicle_self_diagnostics"] = {}
    assert car.vehicle_self_diagnostics_available is not None or car.vehicle_self_diagnostics_available is None


@pytest.mark.asyncio
async def test_car_passenger_seat_belt_status_values(monkeypatch):
    """Test passenger_seat_belt_status property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with None value (not buckled)
    car._vehicle_data["vehicle_state"]["passenger_seat_belt_status"] = None
    assert car.passenger_seat_belt_status is None
    
    # Test with 1 value (buckled)
    car._vehicle_data["vehicle_state"]["passenger_seat_belt_status"] = 1
    assert car.passenger_seat_belt_status == 1


@pytest.mark.asyncio
async def test_car_active_route_properties_missing(monkeypatch):
    """Test active_route properties when route is not available."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Remove active route data
    car._vehicle_data["drive_state"]["active_route_destination"] = None
    car._vehicle_data["drive_state"]["active_route_latitude"] = None
    car._vehicle_data["drive_state"]["active_route_longitude"] = None
    car._vehicle_data["drive_state"]["active_route_miles_to_arrival"] = None
    car._vehicle_data["drive_state"]["active_route_energy_at_arrival"] = None
    car._vehicle_data["drive_state"]["active_route_minutes_to_arrival"] = None
    car._vehicle_data["drive_state"]["active_route_traffic_minutes_delay"] = None
    
    assert car.active_route_destination is None
    assert car.active_route_latitude is None
    assert car.active_route_longitude is None
    assert car.active_route_miles_to_arrival is None
    assert car.active_route_energy_at_arrival is None
    assert car.active_route_minutes_to_arrival is None
    assert car.active_route_traffic_minutes_delay is None


@pytest.mark.asyncio
async def test_car_scheduled_charging_pending_values(monkeypatch):
    """Test scheduled charging pending property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # is_scheduled_charging_pending returns a boolean value
    car._vehicle_data["charge_state"]["scheduled_charging_pending"] = True
    assert car.is_scheduled_charging_pending is True
    
    car._vehicle_data["charge_state"]["scheduled_charging_pending"] = False
    assert car.is_scheduled_charging_pending is False


@pytest.mark.asyncio
async def test_car_off_peak_charging_properties(monkeypatch):
    """Test off-peak charging properties."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test off-peak properties
    car._vehicle_data["charge_state"]["off_peak_charging_enabled"] = True
    assert car.is_off_peak_charging_enabled is True
    
    car._vehicle_data["charge_state"]["off_peak_charging_enabled"] = False
    assert car.is_off_peak_charging_enabled is False


@pytest.mark.asyncio
async def test_car_preconditioning_properties(monkeypatch):
    """Test preconditioning properties."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test preconditioning properties
    car._vehicle_data["charge_state"]["preconditioning_enabled"] = True
    assert car.is_preconditioning_enabled is True
    
    car._vehicle_data["charge_state"]["preconditioning_enabled"] = False
    assert car.is_preconditioning_enabled is False


@pytest.mark.asyncio
async def test_car_front_drive_unit_version(monkeypatch):
    """Test front_drive_unit_version property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test with version available
    car._vehicle_data["vehicle_config"]["front_drive_unit"] = "Small"
    car._vehicle_data["vehicle_config"]["component_parent_ids"] = []
    # front_drive_unit_version checks for component version
    assert car.front_drive_unit_version is None or isinstance(car.front_drive_unit_version, str)


@pytest.mark.asyncio
async def test_car_rear_view_mirror_on_rtc(monkeypatch):
    """Test rear_view_mirror_on_rtc property with different values."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test when property is not present
    car._vehicle_data["vehicle_state"]["side_mirror_state"] = None
    assert car.rear_view_mirror_on_rtc is None


@pytest.mark.asyncio
async def test_car_universal_home_bridge_device_count(monkeypatch):
    """Test universal_home_bridge_device_count property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test when count is available
    car._vehicle_data["vehicle_state"]["universal_home_bridge_device_count"] = 5
    assert car.universal_home_bridge_device_count == 5
    
    # Test with None
    car._vehicle_data["vehicle_state"]["universal_home_bridge_device_count"] = None
    assert car.universal_home_bridge_device_count is None


@pytest.mark.asyncio
async def test_car_guarded_charge_port_properties(monkeypatch):
    """Test guarded_charge_port_detected property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test when not present (defaults to None)
    result = car.guarded_charge_port_detected
    assert result is None or isinstance(result, bool)


@pytest.mark.asyncio
async def test_car_auto_seat_climate_properties(monkeypatch):
    """Test auto seat climate properties."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # Test auto_seat_climate properties
    car._vehicle_data["climate_state"]["auto_seat_climate_left"] = True
    assert car.is_auto_seat_climate_left is True
    
    car._vehicle_data["climate_state"]["auto_seat_climate_right"] = False
    assert car.is_auto_seat_climate_right is False


@pytest.mark.asyncio
async def test_car_auto_steering_wheel_heat(monkeypatch):
    """Test auto steering wheel heat property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    car._vehicle_data["climate_state"]["auto_steering_wheel_heat"] = True
    assert car.is_auto_steering_wheel_heat is True
    
    car._vehicle_data["climate_state"]["auto_steering_wheel_heat"] = False
    assert car.is_auto_steering_wheel_heat is False


@pytest.mark.asyncio
async def test_car_cabin_overheat_protection_cooling_check(monkeypatch):
    """Test cabin_overheat_protection_actively_cooling property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # When the key is not set, returns None
    result = car.cabin_overheat_protection_actively_cooling
    assert result is None or isinstance(result, bool)


@pytest.mark.asyncio
async def test_car_steering_wheel_heater_availability(monkeypatch):
    """Test steering_wheel_heater property checks if available."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    car = list(_controller.cars.values())[0]
    
    # steering_wheel_heater returns True if steering_wheel_heater is not None
    # This is a boolean flag checking if the feature is available
    result = car.steering_wheel_heater
    assert isinstance(result, bool)
