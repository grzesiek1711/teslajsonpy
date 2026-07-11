#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Optional, Tuple

from teslajsonpy.exceptions import HomelinkError, TeslaException

_LOGGER = logging.getLogger(__name__)

CLIMATE_KEEPER_ID_MAP = {
    0: "off",
    1: "on",
    2: "dog",
    3: "camp",
}

SEAT_ID_MAP = {
    0: "left",
    1: "right",
    2: "rear_left",
    4: "rear_center",
    5: "rear_right",
    6: "third_row_left",
    7: "third_row_right",
}

DAY_SELECTION_MAP = {
    "all_week": False,
    "weekdays": True,
}


class TeslaCar:
    #  pylint: disable=too-many-public-methods
    """Represents a Tesla car.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_car_objects`.
    """

    def __init__(self, car: dict, controller, vehicle_data: dict) -> None:
        """Initialize TeslaCar."""
        self._car = car
        self._controller = controller
        self._vehicle_data = vehicle_data

        self._previous_driver_temp = self.driver_temp_setting
        self._previous_fan_status = self.fan_status
        self._previous_passenger_temp = self.passenger_temp_setting

    @property
    def display_name(self) -> str:
        """Return display name."""
        return self._car.get("display_name")

    @property
    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return id."""
        return self._car.get("id")

    @property
    def state(self) -> str:
        """Return car state."""
        return self._car.get("state")

    @property
    def vehicle_id(self) -> int:
        """Return car id."""
        return self._car.get("vehicle_id")

    @property
    def vin(self) -> str:
        """Return car vin."""
        return self._car.get("vin")

    @property
    def data_available(self) -> bool:
        """Return if data from VEHICLE_DATA endpoint is available."""
        # self._vehicle_data gets updated with some data from VEHICLE_LIST endpoint
        # Only return True if data specifically from VEHICLE_DATA endpoint is available
        # vehicle_state is only from the VEHICLE_DATA endpoint
        if self._vehicle_data.get("vehicle_state", {}):
            return True
        return None

    @property
    def battery_level(self) -> float:
        """Return car battery level (SOC). This is not affected by temperature."""
        return self._vehicle_data.get("charge_state", {}).get("battery_level")

    @property
    def usable_battery_level(self) -> float:
        """Return car usable battery level (uSOE). This is the value used in the app and car."""
        return self._vehicle_data.get("charge_state", {}).get("usable_battery_level")

    @property
    def battery_range(self) -> float:
        """Return car battery range."""
        return self._vehicle_data.get("charge_state", {}).get("battery_range")

    @property
    def cabin_overheat_protection(self) -> str:
        """Return cabin overheat protection."""
        return self._vehicle_data.get("climate_state", {}).get(
            "cabin_overheat_protection"
        )

    @property
    def car_type(self) -> str:
        """Return car type."""
        return f"Model {str(self.vin[3]).upper()}"

    @property
    def car_version(self) -> str:
        """Return installed car software version."""
        return self._vehicle_data.get("vehicle_state", {}).get("car_version")

    @property
    def charger_actual_current(self) -> int:
        """Return charger actual current."""
        return self._vehicle_data.get("charge_state", {}).get("charger_actual_current")

    @property
    def charge_current_request(self) -> int:
        """Return charge current request."""
        return self._vehicle_data.get("charge_state", {}).get("charge_current_request")

    @property
    def charge_current_request_max(self) -> int:
        """Return charge current request max."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_current_request_max"
        )

    @property
    def charge_port_latch(self) -> str:
        """Return charger port latch state.

        Returns
            str: Engaged

        Other states?

        """
        return self._vehicle_data.get("charge_state", {}).get("charge_port_latch")

    @property
    def charge_energy_added(self) -> float:
        """Return charge energy added."""
        return self._vehicle_data.get("charge_state", {}).get("charge_energy_added")

    @property
    def charge_limit_soc(self) -> int:
        """Return charge limit soc."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc")

    @property
    def charge_limit_soc_max(self) -> int:
        """Return charge limit soc max."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc_max")

    @property
    def charge_limit_soc_min(self) -> int:
        """Return charge limit soc min."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc_min")

    @property
    def charge_miles_added_ideal(self) -> float:
        """Return charge ideal miles added."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_miles_added_ideal"
        )

    @property
    def charge_miles_added_rated(self) -> float:
        """Return charge rated miles added."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_miles_added_rated"
        )

    @property
    def charger_phases(self) -> int:
        """Return charger phase."""
        return self._vehicle_data.get("charge_state", {}).get("charger_phases")

    @property
    def charger_power(self) -> int:
        """Return charger power."""
        return self._vehicle_data.get("charge_state", {}).get("charger_power")

    @property
    def charge_rate(self) -> str:
        """Return charge rate."""
        return self._vehicle_data.get("charge_state", {}).get("charge_rate")

    @property
    def charging_state(self) -> str:
        """Return charging state.

        Returns
            str: Charging, Stopped, Complete, Disconnected, NoPower
            None: When car is asleep

        """
        return self._vehicle_data.get("charge_state", {}).get("charging_state")

    @property
    def charger_voltage(self) -> int:
        """Return charger voltage."""
        return self._vehicle_data.get("charge_state", {}).get("charger_voltage")

    @property
    def bioweapon_mode(self) -> bool:
        """Return bioweapon defense mode."""
        return self._vehicle_data.get("climate_state", {}).get("bioweapon_mode")

    @property
    def climate_keeper_mode(self) -> str:
        """Return climate keeper mode mode.

        Returns
            str: dog, camp, on, off

        Not supported on all Tesla models.

        """
        return self._vehicle_data.get("climate_state", {}).get("climate_keeper_mode")

    @property
    def conn_charge_cable(self) -> str:
        """Return charge cable connection."""
        return self._vehicle_data.get("charge_state", {}).get("conn_charge_cable")

    @property
    def defrost_mode(self) -> int:
        """Return defrost mode.

        Returns
            int: 2 (on), 0 (off)

        """
        return self._vehicle_data.get("climate_state", {}).get("defrost_mode", 0)

    @property
    def driver_temp_setting(self) -> float:
        """Return driver temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("driver_temp_setting")

    @property
    def fan_status(self) -> int:
        """Return fan status setting."""
        return self._vehicle_data.get("climate_state", {}).get("fan_status")

    @property
    def fast_charger_present(self) -> bool:
        """Return fast charger present."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_present")

    @property
    def fast_charger_brand(self) -> str:
        """Return fast charger brand."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_brand")

    @property
    def fast_charger_type(self) -> str:
        """Return fast charger type."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_type")

    @property
    def door_df(self) -> int:
        """Return driver front door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("df")

    @property
    def door_dr(self) -> int:
        """Return driver rear door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("dr")

    @property
    def door_pf(self) -> int:
        """Return passenger front door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("pf")

    @property
    def door_pr(self) -> int:
        """Return passenger rear door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("pr")

    @property
    def gui_distance_units(self) -> str:
        """Return gui distance units."""
        return self._vehicle_data.get("gui_settings", {}).get("gui_distance_units")

    @property
    def gui_range_display(self) -> str:
        """Return range display."""
        return self._vehicle_data.get("gui_settings", {}).get("gui_range_display")

    @property
    def heading(self) -> int:
        """Return heading."""
        return self._vehicle_data.get("drive_state", {}).get("heading")

    @property
    def homelink_device_count(self) -> int:
        """Return Homelink device count."""
        return self._vehicle_data.get("vehicle_state", {}).get("homelink_device_count")

    @property
    def homelink_nearby(self) -> bool:
        """Return Homelink nearby."""
        return self._vehicle_data.get("vehicle_state", {}).get("homelink_nearby")

    @property
    def ideal_battery_range(self) -> float:
        """Return car ideal battery range."""
        return self._vehicle_data.get("charge_state", {}).get("ideal_battery_range")

    @property
    def in_service(self) -> bool:
        """Return car in_service."""
        if self.data_available:
            return self._vehicle_data.get("in_service")
        return None

    @property
    def inside_temp(self) -> float:
        """Return inside temperature."""
        return self._vehicle_data.get("climate_state", {}).get("inside_temp")

    @property
    def is_charge_port_door_open(self) -> bool:
        """Return charger port door open."""
        return self._vehicle_data.get("charge_state", {}).get("charge_port_door_open")

    @property
    def is_climate_on(self) -> bool:
        """Return climate is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_climate_on")

    @property
    def is_frunk_closed(self) -> bool:
        """Return car frunk is closed.

        Returns
            bool: True (0), False (255)

        """
        response = self._vehicle_data.get("vehicle_state", {}).get("ft")
        return response == 0

    @property
    def is_in_gear(self) -> bool:
        """Return car is gear (i.e. drive or reverse)."""
        return self.shift_state in ["D", "R"]

    @property
    def is_locked(self) -> bool:
        """Return car is locked."""
        return self._vehicle_data.get("vehicle_state", {}).get("locked")

    @property
    def is_steering_wheel_heater_on(self) -> bool:
        """Return steering wheel heater."""
        return self._vehicle_data.get("climate_state", {}).get("steering_wheel_heater")

    @property
    def is_trunk_closed(self) -> bool:
        """Return car trunk is closed.

        Returns
            bool: True (0), False (1-255)

        """
        response = self._vehicle_data.get("vehicle_state", {}).get("rt")
        return response == 0

    @property
    def is_on(self) -> bool:
        """Return car is on."""
        return self._controller.is_car_online(vin=self.vin)

    @property
    def longitude(self) -> float:
        """Return longitude."""
        return self._vehicle_data.get("drive_state", {}).get("longitude")

    @property
    def latitude(self) -> float:
        """Return latitude."""
        return self._vehicle_data.get("drive_state", {}).get("latitude")

    @property
    def max_avail_temp(self) -> float:
        """Return max available temperature."""
        return self._vehicle_data.get("climate_state", {}).get("max_avail_temp")

    @property
    def min_avail_temp(self) -> float:
        """Return min available temperature."""
        return self._vehicle_data.get("climate_state", {}).get("min_avail_temp")

    @property
    def native_heading(self) -> int:
        """Return native heading."""
        return self._vehicle_data.get("drive_state", {}).get("native_heading")

    @property
    def native_location_supported(self) -> int:
        """Return native location supported."""
        return self._vehicle_data.get("drive_state", {}).get(
            "native_location_supported"
        )

    @property
    def native_longitude(self) -> float:
        """Return native longitude."""
        return self._vehicle_data.get("drive_state", {}).get("native_longitude")

    @property
    def native_latitude(self) -> float:
        """Return native latitude."""
        return self._vehicle_data.get("drive_state", {}).get("native_latitude")

    @property
    def native_type(self) -> float:
        """Return native type."""
        return self._vehicle_data.get("drive_state", {}).get("native_type")

    @property
    def odometer(self) -> float:
        """Return odometer."""
        return self._vehicle_data.get("vehicle_state", {}).get("odometer")

    @property
    def outside_temp(self) -> float:
        """Return outside temperature."""
        return self._vehicle_data.get("climate_state", {}).get("outside_temp")

    @property
    def passenger_temp_setting(self) -> float:
        """Return passenger temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("passenger_temp_setting")

    @property
    def left_temp_setting(self) -> float:
        """Return left seat temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("left_temp_setting")

    @property
    def right_temp_setting(self) -> float:
        """Return right seat temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("right_temp_setting")

    @property
    def is_preconditioning(self) -> bool:
        """Return if preconditioning is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_preconditioning")

    @property
    def is_auto_conditioning_on(self) -> bool:
        """Return if auto conditioning is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_auto_conditioning_on")

    @property
    def is_battery_heater_on(self) -> bool:
        """Return if battery heater is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_battery_heater_on")

    @property
    def is_battery_preconditioning(self) -> bool:
        """Return if battery preconditioning is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_battery_preconditioning")

    @property
    def is_front_defroster_on(self) -> bool:
        """Return if front defroster is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_front_defroster_on")

    @property
    def is_rear_defroster_on(self) -> bool:
        """Return if rear defroster is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_rear_defroster_on")

    @property
    def seat_cooler_left(self) -> int:
        """Return left seat cooler level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_cooler_left")

    @property
    def seat_cooler_right(self) -> int:
        """Return right seat cooler level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_cooler_right")

    @property
    def seat_heater_rear_left(self) -> int:
        """Return rear left seat heater level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_heater_rear_left")

    @property
    def seat_heater_rear_right(self) -> int:
        """Return rear right seat heater level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_heater_rear_right")

    @property
    def seat_heater_rear_center(self) -> int:
        """Return rear center seat heater level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_heater_rear_center")

    @property
    def seat_heater_third_row_left(self) -> int:
        """Return third row left seat heater level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_heater_third_row_left")

    @property
    def seat_heater_third_row_right(self) -> int:
        """Return third row right seat heater level."""
        return self._vehicle_data.get("climate_state", {}).get("seat_heater_third_row_right")

    @property
    def third_row_heaters(self) -> list:
        """Return third row heaters state."""
        return self._vehicle_data.get("climate_state", {}).get("third_row_heaters")

    @property
    def cabin_overheat_protection_actively_cooling(self) -> bool:
        """Return if cabin overheat protection is actively cooling."""
        return self._vehicle_data.get("climate_state", {}).get(
            "cabin_overheat_protection_actively_cooling"
        )

    @property
    def cop_activation_temperature(self) -> str:
        """Return cabin overheat protection activation temperature."""
        return self._vehicle_data.get("climate_state", {}).get("cop_activation_temperature")

    @property
    def power(self) -> int:
        """Return power."""
        return self._vehicle_data.get("drive_state", {}).get("power")

    @property
    def powered_lift_gate(self) -> bool:
        """Return True if car has power lift gate."""
        return self._vehicle_data.get("vehicle_config", {}).get("plg")

    @property
    def rear_seat_heaters(self) -> int:
        """Return if car has rear (second row) heated seats.

        Returns
            int: 0 (no rear heated seats), int: ? (rear heated seats)

        """
        return self._vehicle_data.get("vehicle_config", {}).get("rear_seat_heaters")

    @property
    def has_seat_cooling(self) -> bool:
        """Return if car has cooled seats."""
        return self._vehicle_data.get("vehicle_config", {}).get("has_seat_cooling")

    @property
    def sentry_mode(self) -> bool:
        """Return sentry mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("sentry_mode")

    @property
    def sentry_mode_available(self) -> bool:
        """Return sentry mode available."""
        return self._vehicle_data.get("vehicle_state", {}).get("sentry_mode_available")

    @property
    def shift_state(self) -> str:
        """Return shift state."""
        return self._vehicle_data.get("drive_state", {}).get("shift_state")

    @property
    def speed(self) -> float:
        """Return speed."""
        return self._vehicle_data.get("drive_state", {}).get("speed")

    @property
    def software_update(self) -> dict:
        """Return software update version information."""
        return self._vehicle_data.get("vehicle_state", {}).get("software_update")

    @property
    def steering_wheel_heater(self) -> bool:
        """Return steering wheel heater option."""
        return (
            self._vehicle_data.get("climate_state", {}).get("steering_wheel_heater")
            is not None
        )

    @property
    def pedestrian_speaker(self) -> Optional[bool]:
        """Return pedestrian warning speaker option."""
        if self._vehicle_data.get("option_codes", {}) is None:
            return None
        if "P3WS" in self._vehicle_data.get("option_codes", {}):
            return True
        return False

    @property
    def tpms_pressure_fl(self) -> float:
        """Return tire pressure sensor for front left tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_fl")

    @property
    def tpms_pressure_fr(self) -> float:
        """Return tire pressure sensor for front right tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_fr")

    @property
    def tpms_pressure_rl(self) -> float:
        """Return tire pressure sensor for rear left tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_rl")

    @property
    def tpms_pressure_rr(self) -> float:
        """Return tire pressure sensor for rear right tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_rr")

    @property
    def third_row_seats(self) -> str:
        """Return third row seats option.

        Returns
            str: None

        """
        return self._vehicle_data.get("vehicle_config", {}).get("third_row_seats")

    @property
    def time_to_full_charge(self) -> float:
        """Return time to full charge."""
        return self._vehicle_data.get("charge_state", {}).get("time_to_full_charge")

    @property
    def window_fd(self) -> int:
        """Return front driver window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("fd_window")

    @property
    def window_fp(self) -> int:
        """Return front passenger window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("fp_window")

    @property
    def window_rd(self) -> int:
        """Return rear driver window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rd_window")

    @property
    def window_rp(self) -> int:
        """Return rear passenger window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rp_window")

    @property
    def is_window_closed(self) -> bool:
        """Return all car windows are close."""
        if (
            self._vehicle_data.get("vehicle_state", {}).get("fd_window")
            or self._vehicle_data.get("vehicle_state", {}).get("fp_window")
            or self._vehicle_data.get("vehicle_state", {}).get("rd_window")
            or self._vehicle_data.get("vehicle_state", {}).get("rp_window")
        ):
            return False
        return True

    @property
    def is_remote_start(self) -> bool:
        """Return if remote start active."""
        return self._vehicle_data.get("vehicle_state", {}).get("remote_start")

    @property
    def is_valet_mode(self) -> bool:
        """Return state of valet mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("valet_mode")

    @property
    def center_display_state(self) -> int:
        """Return center display state."""
        return self._vehicle_data.get("vehicle_state", {}).get("center_display_state")

    @property
    def middle_display_state(self) -> int:
        """Return middle display state."""
        return self._vehicle_data.get("vehicle_state", {}).get("middle_display_state")

    @property
    def carplay_state(self) -> int:
        """Return carplay state."""
        return self._vehicle_data.get("vehicle_state", {}).get("carplay_state")

    @property
    def api_version(self) -> int:
        """Return API version."""
        return self._vehicle_data.get("vehicle_state", {}).get("api_version")

    @property
    def autopark_state_v2(self) -> str:
        """Return autopark state v2."""
        return self._vehicle_data.get("vehicle_state", {}).get("autopark_state_v2")

    @property
    def autopark_style(self) -> str:
        """Return autopark style."""
        return self._vehicle_data.get("vehicle_state", {}).get("autopark_style")

    @property
    def body_color_rgb(self) -> str:
        """Return body color RGB."""
        return self._vehicle_data.get("vehicle_state", {}).get("body_color_rgb")

    @property
    def body_type(self) -> str:
        """Return body type."""
        return self._vehicle_data.get("vehicle_state", {}).get("body_type")

    @property
    def brake_type_rear(self) -> str:
        """Return rear brake type."""
        return self._vehicle_data.get("vehicle_state", {}).get("brake_type_rear")

    @property
    def charging_cable_type(self) -> str:
        """Return charging cable type."""
        return self._vehicle_data.get("vehicle_state", {}).get("charging_cable_type")

    @property
    def dashcam_state(self) -> str:
        """Return dashcam state."""
        return self._vehicle_data.get("vehicle_state", {}).get("dashcam_state")

    @property
    def dashcam_video_mode(self) -> int:
        """Return dashcam video mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("dashcam_video_mode")

    @property
    def door_rp(self) -> int:
        """Return rear passenger door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rp")

    @property
    def door_rd(self) -> int:
        """Return rear driver door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rd")

    @property
    def doors_state(self) -> list:
        """Return doors state."""
        return self._vehicle_data.get("vehicle_state", {}).get("doors_state")

    @property
    def epic_type(self) -> str:
        """Return epic type."""
        return self._vehicle_data.get("vehicle_state", {}).get("epic_type")

    @property
    def exterior_color(self) -> str:
        """Return exterior color."""
        return self._vehicle_data.get("vehicle_state", {}).get("exterior_color")

    @property
    def front_drive_unit(self) -> str:
        """Return front drive unit."""
        return self._vehicle_data.get("vehicle_state", {}).get("front_drive_unit")

    @property
    def front_drive_unit_version(self) -> str:
        """Return front drive unit version."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "front_drive_unit_version"
        )

    @property
    def front_seat_heaters(self) -> int:
        """Return front seat heaters."""
        return self._vehicle_data.get("vehicle_state", {}).get("front_seat_heaters")

    @property
    def front_seat_leg_rests(self) -> int:
        """Return front seat leg rests."""
        return self._vehicle_data.get("vehicle_state", {}).get("front_seat_leg_rests")

    @property
    def gps_as_of(self) -> int:
        """Return GPS timestamp."""
        return self._vehicle_data.get("vehicle_state", {}).get("gps_as_of")

    @property
    def gps_signal_strength(self) -> int:
        """Return GPS signal strength."""
        return self._vehicle_data.get("vehicle_state", {}).get("gps_signal_strength")

    @property
    def guest_mode(self) -> bool:
        """Return guest mode state."""
        return self._vehicle_data.get("vehicle_state", {}).get("guest_mode")

    @property
    def guarded_charge_port_detected(self) -> bool:
        """Return if guarded charge port detected."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "guarded_charge_port_detected"
        )

    @property
    def has_air_suspension(self) -> bool:
        """Return if vehicle has air suspension."""
        return self._vehicle_data.get("vehicle_state", {}).get("has_air_suspension")

    @property
    def has_ludicrous_mode(self) -> bool:
        """Return if vehicle has ludicrous mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("has_ludicrous_mode")

    @property
    def has_seat_heating(self) -> bool:
        """Return if vehicle has seat heating."""
        return self._vehicle_data.get("vehicle_state", {}).get("has_seat_heating")

    @property
    def hood_state(self) -> str:
        """Return hood state."""
        return self._vehicle_data.get("vehicle_state", {}).get("hood_state")

    @property
    def is_user_present(self) -> bool:
        """Return if user is present."""
        return self._vehicle_data.get("vehicle_state", {}).get("is_user_present")

    @property
    def last_autopark_error(self) -> str:
        """Return last autopark error."""
        return self._vehicle_data.get("vehicle_state", {}).get("last_autopark_error")

    @property
    def left_drive_unit(self) -> str:
        """Return left drive unit."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_drive_unit")

    @property
    def left_drive_unit_version(self) -> str:
        """Return left drive unit version."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "left_drive_unit_version"
        )

    @property
    def left_seat_belt_status(self) -> int:
        """Return left seat belt status."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_seat_belt_status")

    @property
    def left_seat_cooler(self) -> int:
        """Return left seat cooler level."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_seat_cooler")

    @property
    def left_seat_heat_level(self) -> int:
        """Return left seat heat level."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_seat_heat_level")

    @property
    def left_seat_heater(self) -> int:
        """Return left seat heater level."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_seat_heater")

    @property
    def left_steering_wheel_heat(self) -> int:
        """Return left steering wheel heat level."""
        return self._vehicle_data.get("vehicle_state", {}).get("left_steering_wheel_heat")

    @property
    def left_steering_wheel_heater(self) -> bool:
        """Return if left steering wheel heater available."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "left_steering_wheel_heater"
        )

    @property
    def media_state(self) -> dict:
        """Return media state."""
        return self._vehicle_data.get("vehicle_state", {}).get("media_state")

    @property
    def met(self) -> str:
        """Return MET (motor/drivetrain identifier)."""
        return self._vehicle_data.get("vehicle_state", {}).get("met")

    @property
    def minor_version(self) -> int:
        """Return minor software version."""
        return self._vehicle_data.get("vehicle_state", {}).get("minor_version")

    @property
    def misc_state(self) -> int:
        """Return misc state."""
        return self._vehicle_data.get("vehicle_state", {}).get("misc_state")

    @property
    def model_name(self) -> str:
        """Return model name."""
        return self._vehicle_data.get("vehicle_state", {}).get("model_3")

    @property
    def mp_body_type(self) -> str:
        """Return MP body type."""
        return self._vehicle_data.get("vehicle_state", {}).get("mp_body_type")

    @property
    def mute_footwell_lights(self) -> bool:
        """Return if footwell lights are muted."""
        return self._vehicle_data.get("vehicle_state", {}).get("mute_footwell_lights")

    @property
    def odometer_unit(self) -> str:
        """Return odometer unit."""
        return self._vehicle_data.get("vehicle_state", {}).get("odometer_unit")

    @property
    def opened_doors(self) -> list:
        """Return list of open door names."""
        return self._vehicle_data.get("vehicle_state", {}).get("opened_doors")

    @property
    def passenger_seat_belt_status(self) -> int:
        """Return passenger seat belt status."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "passenger_seat_belt_status"
        )

    @property
    def perf_mode(self) -> bool:
        """Return performance mode state."""
        return self._vehicle_data.get("vehicle_state", {}).get("perf_mode")

    @property
    def powertrain(self) -> str:
        """Return powertrain type."""
        return self._vehicle_data.get("vehicle_state", {}).get("powertrain")

    @property
    def power_reading_left(self) -> int:
        """Return left power reading."""
        return self._vehicle_data.get("vehicle_state", {}).get("power_reading_left")

    @property
    def power_reading_right(self) -> int:
        """Return right power reading."""
        return self._vehicle_data.get("vehicle_state", {}).get("power_reading_right")

    @property
    def power_state(self) -> str:
        """Return power state (Drive, Charge, Sleep)."""
        return self._vehicle_data.get("vehicle_state", {}).get("power_state")

    @property
    def rear_drive_unit(self) -> str:
        """Return rear drive unit."""
        return self._vehicle_data.get("vehicle_state", {}).get("rear_drive_unit")

    @property
    def rear_drive_unit_version(self) -> str:
        """Return rear drive unit version."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "rear_drive_unit_version"
        )

    @property
    def rear_seat_type(self) -> str:
        """Return rear seat type."""
        return self._vehicle_data.get("vehicle_state", {}).get("rear_seat_type")

    @property
    def rear_seats(self) -> str:
        """Return rear seats configuration."""
        return self._vehicle_data.get("vehicle_state", {}).get("rear_seats")

    @property
    def rear_trunk_open(self) -> int:
        """Return rear trunk open state."""
        return self._vehicle_data.get("vehicle_state", {}).get("rear_trunk_open")

    @property
    def rear_view_mirror_on_rtc(self) -> bool:
        """Return if rear view mirror on RTC."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "rear_view_mirror_on_rtc"
        )

    @property
    def remote_start_enabled(self) -> bool:
        """Return if remote start is enabled."""
        return self._vehicle_data.get("vehicle_state", {}).get("remote_start_enabled")

    @property
    def remote_start_supported(self) -> bool:
        """Return if remote start is supported."""
        return self._vehicle_data.get("vehicle_state", {}).get("remote_start_supported")

    @property
    def right_drive_unit(self) -> str:
        """Return right drive unit."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_drive_unit")

    @property
    def right_drive_unit_version(self) -> str:
        """Return right drive unit version."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "right_drive_unit_version"
        )

    @property
    def right_seat_belt_status(self) -> int:
        """Return right seat belt status."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_seat_belt_status")

    @property
    def right_seat_cooler(self) -> int:
        """Return right seat cooler level."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_seat_cooler")

    @property
    def right_seat_heat_level(self) -> int:
        """Return right seat heat level."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_seat_heat_level")

    @property
    def right_seat_heater(self) -> int:
        """Return right seat heater level."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_seat_heater")

    @property
    def right_steering_wheel_heat(self) -> int:
        """Return right steering wheel heat level."""
        return self._vehicle_data.get("vehicle_state", {}).get("right_steering_wheel_heat")

    @property
    def right_steering_wheel_heater(self) -> bool:
        """Return if right steering wheel heater available."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "right_steering_wheel_heater"
        )

    @property
    def roof_color(self) -> str:
        """Return roof color."""
        return self._vehicle_data.get("vehicle_state", {}).get("roof_color")

    @property
    def roof_state(self) -> str:
        """Return roof state."""
        return self._vehicle_data.get("vehicle_state", {}).get("roof_state")

    @property
    def seat_type(self) -> str:
        """Return seat type."""
        return self._vehicle_data.get("vehicle_state", {}).get("seat_type")

    @property
    def service_mode(self) -> bool:
        """Return if vehicle is in service mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("service_mode")

    @property
    def service_mode_plus(self) -> bool:
        """Return if vehicle is in service mode plus."""
        return self._vehicle_data.get("vehicle_state", {}).get("service_mode_plus")

    @property
    def set_favorite_available(self) -> bool:
        """Return if set favorite is available."""
        return self._vehicle_data.get("vehicle_state", {}).get("set_favorite_available")

    @property
    def side_mirror_heaters(self) -> bool:
        """Return if side mirror heaters available."""
        return self._vehicle_data.get("vehicle_state", {}).get("side_mirror_heaters")

    @property
    def side_mirror_state(self) -> str:
        """Return side mirror state."""
        return self._vehicle_data.get("vehicle_state", {}).get("side_mirror_state")

    @property
    def steering_angle(self) -> float:
        """Return steering angle in degrees."""
        return self._vehicle_data.get("vehicle_state", {}).get("steering_angle")

    @property
    def steering_wheel_type(self) -> str:
        """Return steering wheel type."""
        return self._vehicle_data.get("vehicle_state", {}).get("steering_wheel_type")

    @property
    def sun_roof_installed(self) -> bool:
        """Return if sunroof is installed."""
        return self._vehicle_data.get("vehicle_state", {}).get("sun_roof_installed")

    @property
    def sun_roof_percent_open(self) -> int:
        """Return sunroof percent open."""
        return self._vehicle_data.get("vehicle_state", {}).get("sun_roof_percent_open")

    @property
    def touchscreen_enabled(self) -> bool:
        """Return if touchscreen is enabled."""
        return self._vehicle_data.get("vehicle_state", {}).get("touchscreen_enabled")

    @property
    def touchscreen_version(self) -> str:
        """Return touchscreen version."""
        return self._vehicle_data.get("vehicle_state", {}).get("touchscreen_version")

    @property
    def trunk(self) -> int:
        """Return trunk open state."""
        return self._vehicle_data.get("vehicle_state", {}).get("trunk")

    @property
    def trunk_state(self) -> str:
        """Return trunk state."""
        return self._vehicle_data.get("vehicle_state", {}).get("trunk_state")

    @property
    def turn_signal_stat(self) -> int:
        """Return turn signal state."""
        return self._vehicle_data.get("vehicle_state", {}).get("turn_signal_stat")

    @property
    def two_hand_regen(self) -> bool:
        """Return if two hand regen is available."""
        return self._vehicle_data.get("vehicle_state", {}).get("two_hand_regen")

    @property
    def universal_home_bridge_device_count(self) -> int:
        """Return universal home bridge device count."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "universal_home_bridge_device_count"
        )

    @property
    def updates_available(self) -> bool:
        """Return if updates are available."""
        return self._vehicle_data.get("vehicle_state", {}).get("updates_available")

    @property
    def user_notes(self) -> str:
        """Return user notes."""
        return self._vehicle_data.get("vehicle_state", {}).get("user_notes")

    @property
    def utc_offset_s(self) -> int:
        """Return UTC offset in seconds."""
        return self._vehicle_data.get("vehicle_state", {}).get("utc_offset_s")

    @property
    def vehicle_color(self) -> str:
        """Return vehicle color."""
        return self._vehicle_data.get("vehicle_state", {}).get("vehicle_color")

    @property
    def vehicle_name(self) -> str:
        """Return vehicle name."""
        return self._vehicle_data.get("vehicle_state", {}).get("vehicle_name")

    @property
    def vehicle_self_diagnostics_available(self) -> bool:
        """Return if vehicle self diagnostics available."""
        return self._vehicle_data.get("vehicle_state", {}).get(
            "vehicle_self_diagnostics_available"
        )

    @property
    def vehicle_speed_mph(self) -> float:
        """Return vehicle speed in mph."""
        return self._vehicle_data.get("vehicle_state", {}).get("vehicle_speed_mph")

    @property
    def vmotion_state(self) -> int:
        """Return vmotion state."""
        return self._vehicle_data.get("vehicle_state", {}).get("vmotion_state")

    @property
    def wh_type(self) -> str:
        """Return wheel type."""
        return self._vehicle_data.get("vehicle_state", {}).get("wh_type")

    @property
    def wheel_type(self) -> str:
        """Return wheel type."""
        return self._vehicle_data.get("vehicle_state", {}).get("wheel_type")

    @property
    def windows_open(self) -> list:
        """Return list of open window names."""
        return self._vehicle_data.get("vehicle_state", {}).get("windows_open")

    @property
    def windshield_wipers(self) -> int:
        """Return windshield wiper state."""
        return self._vehicle_data.get("vehicle_state", {}).get("windshield_wipers")

    @property
    def wiper_blade_defrost(self) -> bool:
        """Return wiper blade defrost state."""
        return self._vehicle_data.get("vehicle_state", {}).get("wiper_blade_defrost")

    @property
    def is_auto_seat_climate_left(self) -> bool:
        """Return state of auto seat climate left."""
        return self._vehicle_data.get("climate_state", {}).get("auto_seat_climate_left")

    @property
    def is_auto_seat_climate_right(self) -> bool:
        """Return state of auto seat climate right."""
        return self._vehicle_data.get("climate_state", {}).get(
            "auto_seat_climate_right"
        )

    @property
    def is_auto_steering_wheel_heat(self) -> bool:
        """Return the state of auto steering wheel heat."""
        return self._vehicle_data.get("climate_state", {}).get(
            "auto_steering_wheel_heat"
        )

    @property
    def active_route_destination(self) -> Optional[str]:
        """Return active route destination."""
        if "active_route_destination" in self._vehicle_data.get("drive_state", {}):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_destination"
            )
        return None

    @property
    def active_route_energy_at_arrival(self) -> Optional[int]:
        """Return active route latitude."""
        if "active_route_energy_at_arrival" in self._vehicle_data.get(
            "drive_state", {}
        ):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_energy_at_arrival"
            )
        return None

    @property
    def active_route_latitude(self) -> Optional[float]:
        """Return active route latitude."""
        if "active_route_latitude" in self._vehicle_data.get("drive_state", {}):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_latitude"
            )
        return None

    @property
    def active_route_longitude(self) -> Optional[float]:
        """Return active route longitude."""
        if "active_route_longitude" in self._vehicle_data.get("drive_state", {}):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_longitude"
            )
        return None

    @property
    def active_route_miles_to_arrival(self) -> Optional[float]:
        """Return active route latitude."""
        if "active_route_miles_to_arrival" in self._vehicle_data.get("drive_state", {}):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_miles_to_arrival"
            )
        return None

    @property
    def active_route_minutes_to_arrival(self) -> Optional[float]:
        """Return active route minutes to arrival."""
        if "active_route_minutes_to_arrival" in self._vehicle_data.get(
            "drive_state", {}
        ):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_minutes_to_arrival"
            )
        return None

    @property
    def active_route_traffic_minutes_delay(self) -> Optional[float]:
        """Return active route traffic minutes delay."""
        if "active_route_minutes_to_arrival" in self._vehicle_data.get(
            "drive_state", {}
        ):
            return self._vehicle_data.get("drive_state", {}).get(
                "active_route_traffic_minutes_delay"
            )
        return None

    @property
    def scheduled_departure_time(self) -> int:
        """Return the scheduled departure time."""
        return self._vehicle_data.get("charge_state", {}).get(
            "scheduled_departure_time"
        )

    @property
    def scheduled_departure_time_minutes(self) -> int:
        """Return the scheduled departure time in minutes after midnight."""
        return self._vehicle_data.get("charge_state", {}).get(
            "scheduled_departure_time_minutes"
        )

    @property
    def is_off_peak_charging_enabled(self) -> bool:
        """Return if peak charging is enabled for scheduled departure."""
        return self._vehicle_data.get("charge_state", {}).get(
            "off_peak_charging_enabled"
        )

    @property
    def is_off_peak_charging_weekday_only(self) -> bool:
        """Return if off off peak charging is weekday only for scheduled departure."""
        return DAY_SELECTION_MAP.get(
            self._vehicle_data.get("charge_state", {}).get("off_peak_charging_times")
        )

    @property
    def off_peak_hours_end_time(self) -> int:
        """Return end of off peak hours in minutes after midnight for scheduled departure."""
        return self._vehicle_data.get("charge_state", {}).get("off_peak_hours_end_time")

    @property
    def is_preconditioning_enabled(self) -> bool:
        """Return if preconditioning is enabled for scheduled departure."""
        return self._vehicle_data.get("charge_state", {}).get("preconditioning_enabled")

    @property
    def is_preconditioning_weekday_only(self) -> bool:
        """Return if preconditioning is weekday only for scheduled departure."""
        return DAY_SELECTION_MAP.get(
            self._vehicle_data.get("charge_state", {}).get("preconditioning_times")
        )

    @property
    def scheduled_charging_mode(self) -> str:
        """Return 'Off', 'DepartBy', or 'StartAt' for schedule disabled, scheduled departure, and scheduled charging respectively."""
        return self._vehicle_data.get("charge_state", {}).get("scheduled_charging_mode")

    @property
    def is_scheduled_charging_pending(self) -> bool:
        """Return if scheduled charging is pending."""
        return self._vehicle_data.get("charge_state", {}).get(
            "scheduled_charging_pending"
        )

    @property
    def scheduled_charging_start_time_app(self) -> int:
        """Return the scheduled charging start time."""
        return self._vehicle_data.get("charge_state", {}).get(
            "scheduled_charging_start_time_app"
        )

    async def _send_command(
        self,
        name: str,
        *,
        additional_path_vars: dict = None,
        wake_if_asleep: bool = True,
        **kwargs,
    ) -> Optional[dict]:
        """Wrap commands sent to Tesla API.

        Args
            name: Name of command to send, from endpoints.json
            additional_path_vars: Additional URI variables ('vehicle_id' already included)
            wake_if_asleep: (default True) Wake car if it's asleep before sending the command
            **kwargs: Any additional parameters for the api call

        """
        path_vars = {"vehicle_id": self.id}
        if additional_path_vars:
            path_vars.update(additional_path_vars)

        _LOGGER.debug("Sending command: %s", name)
        try:
            data = await self._controller.api(
                name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
            )
            _LOGGER.debug("Response from command %s: %s", name, data)
            return data
        except TeslaException as ex:
            if ex.code == 408 and not wake_if_asleep and not self.is_on:
                # 408 due to being asleep and we didn't try to wake it
                _LOGGER.debug(
                    "Vehicle unavailable for command: %s, car state: %s, wake_if_asleep: %s",
                    name,
                    self.state,
                    wake_if_asleep,
                )
                return None
            raise ex

    def _get_lat_long(self) -> Tuple[Optional[float], Optional[float]]:
        """Get current latitude and longitude."""
        lat = None
        long = None

        if self.native_location_supported:
            long = self.native_longitude
            lat = self.native_latitude
        else:
            long = self.longitude
            lat = self.latitude

        return lat, long

    def _get_active_route_lat_long(self) -> Tuple[Optional[float], Optional[float]]:
        """Get active route latitude and longitude."""
        lat = None
        long = None

        if self.active_route_longitude and self.active_route_latitude:
            lat = self.active_route_latitude
            long = self.active_route_longitude

        return lat, long

    def update_car_info(self, car: dict) -> None:
        """Update the car info dict from the vehicle_list api."""
        if not car:
            _LOGGER.debug("Attempted to update car id %d with empty car info", self.id)
            return
        if car["vin"] != self.vin:
            _LOGGER.error(
                "Failed updating car info: new VIN (%s) doesn't match existing vin (%s)",
                car["vin"][-5:],
                self.vin[-5:],
            )
            return
        self._car.update(car)

    async def change_charge_limit(self, value: float) -> None:
        """Send command to change charge limit."""
        # Only wake car if the value is different
        wake_if_asleep = value != self.charge_limit_soc
        data = await self._send_command(
            "CHANGE_CHARGE_LIMIT", percent=int(value), wake_if_asleep=wake_if_asleep
        )

        if data and data["response"]["result"] is True:
            params = {"charge_limit_soc": int(value)}
            self._vehicle_data["charge_state"].update(params)

    async def charge_port_door_close(self) -> None:
        """Send command to close charge port door."""
        data = await self._send_command("CHARGE_PORT_DOOR_CLOSE")

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": False}
            self._vehicle_data["charge_state"].update(params)

    async def charge_port_door_open(self) -> None:
        """Send command to open charge port door."""
        data = await self._send_command("CHARGE_PORT_DOOR_OPEN")

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": True}
            self._vehicle_data["charge_state"].update(params)

    async def flash_lights(self) -> None:
        """Send command to flash lights."""
        await self._send_command("FLASH_LIGHTS", on=True)

    async def honk_horn(self) -> None:
        """Send command to honk horn."""
        await self._send_command("HONK_HORN", on=True)

    async def lock(self) -> None:
        """Send lock command."""
        data = await self._send_command("LOCK")
        if data and data["response"]["result"] is True:
            params = {"locked": True}
            self._vehicle_data["vehicle_state"].update(params)

    async def remote_seat_heater_request(self, level: int, seat_id: int) -> None:
        """Send command to change seat heat.

        Args
            level: 0 (off), 1 (low), 2 (medium), 3 (high)
            seat_id: 0 (front left), 1 (front right), 2 (rear left), 4 (rear center)
            5 (rear right), 6 (third row left), 7 (third row right)

        """
        # If car is asleep the heater is already off
        wake_if_asleep = level > 0
        data = await self._send_command(
            "REMOTE_SEAT_HEATER_REQUEST",
            seat_position=seat_id,
            level=level,
            wake_if_asleep=wake_if_asleep,
        )
        if data and data["response"]["result"] is True:
            params = {f"seat_heater_{SEAT_ID_MAP[seat_id]}": level}
            self._vehicle_data["climate_state"].update(params)

    def get_seat_heater_status(self, seat_id: int) -> int:
        """Return status of seat heater for a given seat."""
        seat_id = f"seat_heater_{SEAT_ID_MAP[seat_id]}"
        if self.data_available:
            return self._vehicle_data.get("climate_state", {}).get(seat_id)
        return None

    async def remote_seat_cooler_request(self, level: int, seat_id: int) -> None:
        """Send command to change seat cooler.

        Args
            level: 1 (off), 2 (low), 3 (medium), 4 (high)
            seat_id: 1 (front left), 2 (front right)

        """
        # If car is asleep the cooler is already off
        wake_if_asleep = level > 1
        data = await self._send_command(
            "REMOTE_SEAT_COOLING_REQUEST",
            seat_position=seat_id,
            seat_cooler_level=level,
            wake_if_asleep=wake_if_asleep,
        )
        if data and data["response"]["result"] is True:
            params = {f"seat_fan_front_{SEAT_ID_MAP[seat_id]}": level}
            self._vehicle_data["climate_state"].update(params)

    def get_seat_cooler_status(self, seat_id: int) -> int:
        """Return status of seat heater for a given seat."""
        seat_id = f"seat_fan_front_{SEAT_ID_MAP[seat_id]}"
        if self.data_available:
            return self._vehicle_data.get("climate_state", {}).get(seat_id)
        return None

    async def schedule_software_update(self, offset_sec: Optional[int] = 0) -> None:
        """Send command to install software update."""
        await self._send_command("SCHEDULE_SOFTWARE_UPDATE", offset_sec=offset_sec)

    async def set_charging_amps(self, value: float) -> None:
        """Send command to set charging amps."""
        # Only wake car if the value is different
        wake_if_asleep = value != self._vehicle_data.get("charge_state", {}).get(
            "charge_current_request"
        )
        data = await self._send_command(
            "CHARGING_AMPS", charging_amps=int(value), wake_if_asleep=wake_if_asleep
        )
        # A second API call allows setting below 5 Amps
        if value < 5:
            data = await self._send_command(
                "CHARGING_AMPS", charging_amps=int(value), wake_if_asleep=wake_if_asleep
            )

        if data and data["response"]["result"] is True:
            params = {
                "charge_amps": int(value),
                "charge_current_request": int(value),
            }
            self._vehicle_data["charge_state"].update(params)

    async def set_cabin_overheat_protection(self, option: str) -> None:
        """Send command to set cabin overheat protection.

        Args
            option: "Off", "No A/C", "On"

        """

        if option == "Off":
            body_on = False
            fan_only = False
        elif option == "No A/C":
            body_on = True
            fan_only = True
        elif option == "On":
            body_on = True
            fan_only = False

        data = await self._send_command(
            "SET_CABIN_OVERHEAT_PROTECTION", on=body_on, fan_only=fan_only
        )
        if data and data["response"]["result"] is True:
            params = {"cabin_overheat_protection": option}
            self._vehicle_data["climate_state"].update(params)

    async def set_climate_keeper_mode(self, keeper_id: int) -> None:
        """Send command to set climate keeper mode.

        Args
            keeper_id: 1 (keep on), 2 (dog mode), 3 (camp mode)

        """
        # If car is asleep, climate is already off
        wake_if_asleep = keeper_id > 0
        data = await self._send_command(
            "SET_CLIMATE_KEEPER_MODE",
            climate_keeper_mode=keeper_id,
            wake_if_asleep=wake_if_asleep,
        )
        if data and data["response"]["result"] is True:
            params = {
                "climate_keeper_mode": CLIMATE_KEEPER_ID_MAP[keeper_id],
                "is_climate_on": True,
            }
            self._vehicle_data["climate_state"].update(params)

    async def set_bioweapon_mode(self, enable: bool) -> None:
        """Send command to set bioweapon mode.

        Args
            enable: 'True' to enable, 'False' to disable

        """
        # If car is asleep, bioweapon is already off
        data = await self._send_command(
            "HVAC_BIOWEAPON_MODE",
            on=enable,
            manual_override=True,
        )
        if data and data["response"]["result"] is True:
            params = {
                "bioweapon_mode": enable,
                "is_climate_on": True,
            }
            self._vehicle_data["climate_state"].update(params)

    async def remote_auto_seat_climate_request(
        self, seat_id: int, enable: bool
    ) -> None:
        """Send command to change seat climate to auto.

        Args
            seat_id: 0 (front left), 1 (front right)
            enable: 'True' to enable, 'False' to disable

        """

        data = await self._send_command(
            "REMOTE_AUTO_SEAT_CLIMATE_REQUEST",
            auto_seat_position=seat_id,
            seat_position=seat_id,
            auto_climate_on=enable,
        )
        if data and data["response"]["result"] is True:
            params = {f"auto_seat_climate_{SEAT_ID_MAP[seat_id]}": enable}
            self._vehicle_data["climate_state"].update(params)

    async def remote_auto_steering_wheel_heat_climate_request(
        self, enable: bool
    ) -> None:
        """Send command to enable or disable auto steering wheel heat.

        Args
            enable: True to enable auto steering wheel heat, False to disable.

        """

        data = await self._send_command(
            "REMOTE_AUTO_STEERING_WHEEL_HEAT_CLIMATE_REQUEST", on=enable
        )
        if data and data["response"]["result"] is True:
            params = {"auto_steering_wheel_heat": enable}
            self._vehicle_data["climate_state"].update(params)

    async def set_heated_steering_wheel(self, value: bool) -> None:
        """Send command to set heated steering wheel."""
        data = await self._send_command(
            "REMOTE_STEERING_WHEEL_HEATER_REQUEST", on=value
        )

        if data and data["response"]["result"] is True:
            params = {"steering_wheel_heater": value}
            self._vehicle_data["climate_state"].update(params)

    async def set_heated_steering_wheel_level(self, level: int) -> None:
        """Send command to set the heated steering wheel level."""
        data = await self._send_command(
            "REMOTE_STEERING_WHEEL_HEAT_LEVEL_REQUEST", level=level
        )

        if data and data["response"]["result"] is True:
            params = {"steering_wheel_heat_level": level}
            self._vehicle_data["climate_state"].update(params)

    def get_heated_steering_wheel_level(self) -> int:
        """Return the status of the heated steering wheel."""
        if self.data_available:
            return self._vehicle_data.get("climate_state", {}).get(
                "steering_wheel_heat_level"
            )
        return None

    async def set_hvac_mode(self, value: str) -> None:
        """Send command to set HVAC mode.

        Args
            value: on, off

        """
        if value == "off":
            # If car is asleep, climate is already off
            data = await self._send_command("CLIMATE_OFF", wake_if_asleep=False)
            if data and data["response"]["result"] is True:
                # Set additional values if turning HVAC off after defrost max
                params = {
                    "defrost_mode": 0,
                    "driver_temp_setting": self._previous_driver_temp,
                    "is_climate_on": False,
                    "is_front_defroster_on": False,
                    "is_rear_defroster_on": False,
                    "passenger_temp_setting": self._previous_passenger_temp,
                }
                self._vehicle_data["climate_state"].update(params)

        elif value == "on":
            data = await self._send_command("CLIMATE_ON")
            if data and data["response"]["result"] is True:
                params = {"is_climate_on": True}
                self._vehicle_data["climate_state"].update(params)

    async def set_max_defrost(self, state: int) -> None:
        """Send command to set max defrost.

        Args
            state: 2 = on, 0 = off

        """
        # If car is asleep, climate is already off
        wake_if_asleep = state > 0
        data = await self._send_command(
            "MAX_DEFROST", on=state, wake_if_asleep=wake_if_asleep
        )
        if data and data["response"]["result"] is True:
            self._previous_driver_temp = self.driver_temp_setting
            self._previous_passenger_temp = self.passenger_temp_setting
            self._previous_fan_status = self.fan_status

            if state == 2:
                params = {
                    "defrost_mode": state,
                    "driver_temp_setting": self.max_avail_temp,
                    "fan_status": 7,
                    "is_climate_on": True,
                    "is_front_defroster_on": True,
                    "is_rear_defroster_on": True,
                    "passenger_temp_setting": self.max_avail_temp,
                }
            if state == 0:
                params = {
                    "defrost_mode": state,
                    "driver_temp_setting": self._previous_driver_temp,
                    "fan_status": self._previous_fan_status,
                    "is_climate_on": True,
                    "is_front_defroster_on": False,
                    "is_rear_defroster_on": False,
                    "passenger_temp_setting": self._previous_passenger_temp,
                }
            self._vehicle_data["climate_state"].update(params)

    async def set_sentry_mode(self, value: bool) -> None:
        """Send command to set sentry mode."""
        # If car is asleep, sentry is already off
        data = await self._send_command(
            "SET_SENTRY_MODE", on=value, wake_if_asleep=value
        )

        if data and data["response"]["result"] is True:
            params = {"sentry_mode": value}
            self._vehicle_data["vehicle_state"].update(params)

    async def set_temperature(self, temp: float) -> None:
        """Send command to set temperature."""
        data = await self._send_command(
            "CHANGE_CLIMATE_TEMPERATURE_SETTING", driver_temp=temp, passenger_temp=temp
        )
        if data and data["response"]["result"] is True:
            params = {"driver_temp_setting": temp}
            self._vehicle_data["climate_state"].update(params)

    async def start_charge(self) -> None:
        """Send command to start charge."""
        data = await self._send_command("START_CHARGE")

        if data and data["response"]["result"] is True:
            params = {"charging_state": "Charging"}
            self._vehicle_data["charge_state"].update(params)

    async def stop_charge(self) -> None:
        """Send command to stop charge."""
        # If car is asleep, it's not charging
        data = await self._send_command("STOP_CHARGE", wake_if_asleep=False)

        if data and data["response"]["result"] is True:
            params = {"charging_state": "Stopped"}
            self._vehicle_data["charge_state"].update(params)

    async def wake_up(self) -> None:
        """Send command to wake up."""
        await self._controller.wake_up(car_id=self.id)

    async def toggle_trunk(self) -> None:
        """Actuate rear trunk."""
        prev_is_trunk_closed = self.is_trunk_closed
        data = await self._send_command("ACTUATE_TRUNK", which_trunk="rear")
        if data and data["response"]["result"] is True:
            if not prev_is_trunk_closed:
                params = {"rt": 0}
                self._vehicle_data["vehicle_state"].update(params)
            if prev_is_trunk_closed:
                params = {"rt": 255}
                self._vehicle_data["vehicle_state"].update(params)

    async def toggle_frunk(self) -> None:
        """Actuate front trunk."""
        prev_is_frunk_closed = self.is_frunk_closed
        data = await self._send_command("ACTUATE_TRUNK", which_trunk="front")
        if data and data["response"]["result"] is True:
            if not prev_is_frunk_closed:
                params = {"ft": 0}
                self._vehicle_data["vehicle_state"].update(params)
            if prev_is_frunk_closed:
                params = {"ft": 255}
                self._vehicle_data["vehicle_state"].update(params)

    async def trigger_homelink(self) -> None:
        """Send command to trigger homelink."""
        if self.homelink_device_count is None:
            raise HomelinkError(f"No homelink devices added to {self.display_name}.")

        if self.homelink_nearby is not True:
            raise HomelinkError(f"No homelink devices near {self.display_name}.")

        lat, long = self._get_lat_long()

        data = await self._send_command("TRIGGER_HOMELINK", lat=lat, lon=long)

        if data and data["response"]:
            _LOGGER.debug("Homelink response: %s", data["response"])
            result = data["response"]["result"]
            reason = data["response"]["reason"]
            if result is False:
                raise HomelinkError(f"Error calling trigger_homelink: {reason}")

    async def unlock(self) -> None:
        """Send unlock command."""
        data = await self._send_command("UNLOCK")
        if data and data["response"]["result"] is True:
            params = {"locked": False}
            self._vehicle_data["vehicle_state"].update(params)

    async def vent_windows(self) -> None:
        """Vent Windows."""
        data = await self._send_command("WINDOW_CONTROL", command="vent", lat=0, long=0)
        if data and data["response"]["result"] is True:
            params = {
                "fd_window": 1,
                "fp_window": 1,
                "rd_window": 1,
                "rp_window": 1,
            }
            self._vehicle_data["vehicle_state"].update(params)

    async def close_windows(self) -> None:
        """Close Windows."""
        data = await self._send_command(
            "WINDOW_CONTROL", command="close", lat=self.latitude, long=self.longitude
        )
        if data and data["response"]["result"] is True:
            params = {
                "fd_window": 0,
                "fp_window": 0,
                "rd_window": 0,
                "rp_window": 0,
            }
            self._vehicle_data["vehicle_state"].update(params)

    async def valet_mode(self, enable, pin=None) -> None:
        """Set Valet Mode.

        Args
            enable: True to activate, False to deactivate.
            pin: optional, pin not required to activate or deactivate valet mode.
                Even with a previous PIN set. If you clear the PIN and activate Valet Mode
                without the parameter, you will only be able to deactivate it from your
                car's screen by signing into your Tesla account.

        """
        if pin:
            data = await self._send_command("SET_VALET_MODE", on=enable, password=pin)
        else:
            data = await self._send_command("SET_VALET_MODE", on=enable)

        if data and data["response"]:
            _LOGGER.debug("Valet mode response: %s", data["response"])
            result = data["response"]["result"]
            reason = data["response"]["reason"]
            if result is False:
                _LOGGER.debug("Error calling valet mode: %s", reason)
            else:
                if enable:
                    params = {"valet_mode": True}
                else:
                    params = {"valet_mode": False}
                self._vehicle_data["vehicle_state"].update(params)

    async def remote_start(self) -> None:
        """Remote start."""
        data = await self._send_command("REMOTE_START")

        if data and data["response"]:
            _LOGGER.debug("Remote start response: %s", data["response"])
            result = data["response"]["result"]
            reason = data["response"]["reason"]
            if result is False:
                _LOGGER.debug("Error calling remote start: %s", reason)
            else:
                self._vehicle_data["vehicle_state"].update({"remote_start": True})

    async def set_scheduled_departure(
        self,
        enable: bool,
        departure_time: int,
        preconditioning_enabled: bool,
        preconditioning_weekdays_only: bool,
        off_peak_charging_enabled: bool,
        off_peak_charging_weekdays_only: bool,
        end_off_peak_time: int,
    ) -> None:
        """Send command to set departure time.

        Args
            enable: Turn on (True) or turn off (False) the scheduled departure.
            departure_time: Time in minutes after midnight (local time) for the departure.
            preconditioning_enabled: Enable (True) or disable (False) the climate preconditioning.
            preconditioning_weekdays_only: Precondition climate for departure time on weekdays only (True) or all days (False).
            off_peak_charging_enabled: Complete charging during off peak hours (True) or complete charging just before departure time (False).
            off_peak_charging_weekdays_only: Complete off peak charging only on weekdays only (True) or all days (False).
            end_off_peak_time: Time in minutes after midnight when the off peak rate ends.

        """
        data = await self._send_command(
            "SCHEDULED_DEPARTURE",
            enable=enable,
            departure_time=departure_time,
            preconditioning_enabled=preconditioning_enabled,
            preconditioning_weekdays_only=preconditioning_weekdays_only,
            off_peak_charging_enabled=off_peak_charging_enabled,
            off_peak_charging_weekdays_only=off_peak_charging_weekdays_only,
            end_off_peak_time=end_off_peak_time,
        )

        if data and data["response"]["result"] is True:
            if enable:
                mode_str = "DepartBy"
            else:
                mode_str = "Off"

            params = {
                "scheduled_charging_mode": mode_str,
                "scheduled_departure_time_minutes": departure_time,
                "preconditioning_enabled": preconditioning_enabled,
                "preconditioning_weekdays_only": list(DAY_SELECTION_MAP.values()).index(
                    preconditioning_weekdays_only
                ),
                "off_peak_charging_enabled": off_peak_charging_enabled,
                "off_peak_charging_weekdays_only": list(
                    DAY_SELECTION_MAP.values()
                ).index(off_peak_charging_weekdays_only),
                "end_off_peak_time": end_off_peak_time,
            }
            self._vehicle_data["charge_state"].update(params)

    async def set_scheduled_charging(self, enable: bool, time: int) -> None:
        """Send command to set scheduled charging time.

        Args
            enable: Turn on (True) or turn off (False) the scheduled charging.
            time: Time in minutes after midnight (local time) to start charging.

        """
        data = await self._send_command("SCHEDULED_CHARGING", enable=enable, time=time)

        if data and data["response"]["result"] is True:
            if enable:
                mode_str = "StartAt"
            else:
                mode_str = "Off"
                time = None
            params = {
                "scheduled_charging_mode": mode_str,
                "scheduled_charging_start_time": time,
                "scheduled_charging_pending": enable,
            }
            self._vehicle_data["charge_state"].update(params)

    async def remote_boombox(self) -> None:
        """Remote boombox."""
        data = await self._send_command("REMOTE_BOOMBOX")

        if data and data["response"]:
            result = data["response"]["result"]
            reason = data["response"]["reason"]
            if result is False:
                _LOGGER.debug("Error calling remote boombox: %s", reason)
            else:
                _LOGGER.debug("Remote boombox called successfully.")
