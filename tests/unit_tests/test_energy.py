"""Test energy sites."""
import pytest

from teslajsonpy.const import DEFAULT_ENERGYSITE_NAME
from teslajsonpy.controller import Controller
from teslajsonpy.energy import SolarSite

from tests.tesla_mock import (
    SITE_SUMMARY,
    ENERGYSITES,
    SITE_CONFIG,
    SITE_DATA,
    TeslaMock,
)


@pytest.mark.asyncio
async def test_energysite_setup(monkeypatch):
    """Test setup of energysites in Controller.connect()."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    solar_site = _controller.energysites[12345]
    powerwall_site = _controller.energysites[67890]

    assert _controller.energysites is not None
    assert solar_site.resource_type == ENERGYSITES[0]["resource_type"]
    assert powerwall_site.resource_type == ENERGYSITES[1]["resource_type"]


@pytest.mark.asyncio
async def test_solar_site(monkeypatch):
    """Test SolarSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_site = _controller.energysites[12345]

    assert _solar_site._api is not None
    assert _solar_site._energysite is not None

    assert _solar_site.energysite_id == ENERGYSITES[0]["energy_site_id"]
    assert _solar_site.has_battery == ENERGYSITES[0]["components"]["battery"]
    assert _solar_site.has_load_meter == ENERGYSITES[0]["components"]["load_meter"]
    assert _solar_site.has_solar == ENERGYSITES[0]["components"]["solar"]
    assert _solar_site.id == ENERGYSITES[0]["id"]
    assert _solar_site.resource_type == ENERGYSITES[0]["resource_type"]
    assert _solar_site.site_name == SITE_CONFIG["site_name"]

    assert _solar_site.grid_power == SITE_DATA["grid_power"]
    assert _solar_site.load_power == SITE_DATA["load_power"]
    assert _solar_site.solar_power == SITE_DATA["solar_power"]
    assert _solar_site.solar_type == ENERGYSITES[0]["components"]["solar_type"]


@pytest.mark.asyncio
async def test_powerwall_site(monkeypatch):
    """Test PowerwallSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_powerwall_site = _controller.energysites[67890]

    assert _solar_powerwall_site._api is not None
    assert _solar_powerwall_site._energysite is not None

    assert _solar_powerwall_site.energysite_id == ENERGYSITES[1]["energy_site_id"]
    assert (
        _solar_powerwall_site.has_load_meter
        == ENERGYSITES[1]["components"]["load_meter"]
    )
    assert _solar_powerwall_site.id == ENERGYSITES[1]["id"]
    assert _solar_powerwall_site.has_battery == ENERGYSITES[1]["components"]["battery"]
    assert _solar_powerwall_site.has_solar == ENERGYSITES[1]["components"]["solar"]
    assert _solar_powerwall_site.resource_type == ENERGYSITES[1]["resource_type"]
    assert _solar_powerwall_site.site_name == ENERGYSITES[1]["site_name"]
    assert (
        _solar_powerwall_site.percentage_charged
        == SITE_SUMMARY["percentage_charged"]
    )
    assert (
        _solar_powerwall_site.battery_power
        == SITE_SUMMARY["battery_power"]
    )
    assert (
        _solar_powerwall_site.grid_power
        == SITE_DATA["grid_power"]
    )
    assert (
        _solar_powerwall_site.grid_status
        == SITE_DATA["grid_status"]
    )
    assert (
        _solar_powerwall_site.load_power
        == SITE_DATA["load_power"]
    )
    assert (
        _solar_powerwall_site.solar_power
        == SITE_DATA["solar_power"]
    )
    assert (
        _solar_powerwall_site.solar_type == ENERGYSITES[1]["components"]["solar_type"]
    )


@pytest.mark.asyncio
async def test_energysite_with_no_name(monkeypatch):
    """Test EnergySite base class with no name."""
    _mock = TeslaMock(monkeypatch)
    _api = Controller(None)
    _energysite = _mock.data_request_energysites()[0]
    _site_config = {12345: _mock.data_request_site_config()}
    _site_data = {12345: _mock.data_request_site_data()}
    _sensor = SolarSite(_api, _energysite, _site_config, _site_data)

    assert _sensor.site_name == DEFAULT_ENERGYSITE_NAME


@pytest.mark.asyncio
async def test_set_operation_mode(monkeypatch):
    """Test set operation mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_operation_mode("autonomous") is None


@pytest.mark.asyncio
async def test_set_reserve_percent(monkeypatch):
    """Test set reserve percent."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_reserve_percent(10) is None


@pytest.mark.asyncio
async def test_set_grid_charging(monkeypatch):
    """Test set grid charging."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_grid_charging(True) is None


@pytest.mark.asyncio
async def test_set_export_rule(monkeypatch):
    """Test set export rule."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()
    _energysite = _controller.energysites[67890]

    assert await _energysite.set_export_rule("pv_only") is None


@pytest.mark.asyncio
async def test_solar_site_data_available(monkeypatch):
    """Test SolarSite data_available property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_site = _controller.energysites[12345]
    
    # Test with data
    assert _solar_site.data_available is True
    
    # Test without data
    _solar_site._site_data = {}
    assert _solar_site.data_available is False


@pytest.mark.asyncio
async def test_powerwall_site_energy_left_no_nameplate(monkeypatch):
    """Test PowerwallSite energy_left when nameplate_energy is None."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _powerwall_site = _controller.energysites[67890]
    
    # Remove nameplate_energy to test None case
    _powerwall_site._site_config.pop("nameplate_energy", None)
    assert _powerwall_site.energy_left is None


@pytest.mark.asyncio
async def test_solar_powerwall_site_properties(monkeypatch):
    """Test SolarPowerwallSite additional properties."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_powerwall_site = _controller.energysites[67890]
    
    # Test that operation_mode property works (default_real_mode)
    _solar_powerwall_site._site_config["default_real_mode"] = "autonomous"
    assert _solar_powerwall_site.operation_mode == "autonomous"
    
    # Test solar_type (may be None if not in config)
    solar_type = _solar_powerwall_site.solar_type
    assert solar_type is None or isinstance(solar_type, str)
    
    # Test version  
    version = _solar_powerwall_site.version
    assert version is None or isinstance(version, (int, float, str))
    
    # Test backup_reserve_percent (may be None if not in config)
    backup_reserve = _solar_powerwall_site.backup_reserve_percent
    assert backup_reserve is None or isinstance(backup_reserve, int)


@pytest.mark.asyncio
async def test_powerwall_site_data_available(monkeypatch):
    """Test PowerwallSite data_available property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _powerwall_site = _controller.energysites[67890]
    
    # Test with data
    assert _powerwall_site.data_available is True
    
    # Test without data
    _powerwall_site._site_summary = {}
    assert _powerwall_site.data_available is False


@pytest.mark.asyncio
async def test_solar_powerwall_site_grid_charging(monkeypatch):
    """Test SolarPowerwallSite grid_charging property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_powerwall_site = _controller.energysites[67890]
    
    # Ensure components dict exists
    if "components" not in _solar_powerwall_site._site_config:
        _solar_powerwall_site._site_config["components"] = {}
    
    # Test grid_charging when disallow_charge_from_grid_with_solar_installed is False
    _solar_powerwall_site._site_config["components"][
        "disallow_charge_from_grid_with_solar_installed"
    ] = False
    assert _solar_powerwall_site.grid_charging is True
    
    # Test grid_charging when disallow_charge_from_grid_with_solar_installed is True
    _solar_powerwall_site._site_config["components"][
        "disallow_charge_from_grid_with_solar_installed"
    ] = True
    assert _solar_powerwall_site.grid_charging is False


@pytest.mark.asyncio
async def test_solar_powerwall_site_export_rule(monkeypatch):
    """Test SolarPowerwallSite export_rule property."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _solar_powerwall_site = _controller.energysites[67890]
    
    # Ensure components dict exists
    if "components" not in _solar_powerwall_site._site_config:
        _solar_powerwall_site._site_config["components"] = {}
    
    # Test with export rule set
    _solar_powerwall_site._site_config["components"]["customer_preferred_export_rule"] = "pv_only"
    assert _solar_powerwall_site.export_rule == "pv_only"
    
    # Test without export rule (should return None)
    del _solar_powerwall_site._site_config["components"]["customer_preferred_export_rule"]
    assert _solar_powerwall_site.export_rule is None


@pytest.mark.asyncio
async def test_powerwall_site_energy_left_with_nameplate(monkeypatch):
    """Test PowerwallSite energy_left calculation with nameplate_energy."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_energysite_objects()

    _powerwall_site = _controller.energysites[67890]
    
    # Set nameplate_energy and percentage_charged for calculation
    _powerwall_site._site_config["nameplate_energy"] = 14070
    _powerwall_site._site_summary["percentage_charged"] = 50
    
    expected = round(14070 * 50 / 100)
    assert _powerwall_site.energy_left == expected


# Test reponse with "grid_status" of "Unknown"
