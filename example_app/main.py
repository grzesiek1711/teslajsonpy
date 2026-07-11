"""
Example application demonstrating teslajsonpy library usage.

This example shows:
1. Basic authentication and connection
2. Getting the full vehicle state (all available parameters)
3. Monitoring real-time updates
"""

import asyncio
import calendar
import datetime
import logging
import os
from httpx import AsyncClient
from teslajsonpy import Controller
from teslajsonpy.exceptions import TeslaException

# Configure logging to see debug messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def load_tokens() -> tuple:
    """Load Tesla tokens from environment variables.

    Tesla access tokens are long JWTs that exceed the terminal's 1024-byte
    canonical input limit, which makes pasting them at an input() prompt hang.
    Tokens must be provided via environment variables:

    - TESLA_ACCESS_TOKEN
    - TESLA_REFRESH_TOKEN

    Returns:
        tuple: (access_token, refresh_token); values are None if not found.
    """
    access_token = os.environ.get("TESLA_ACCESS_TOKEN")
    refresh_token = os.environ.get("TESLA_REFRESH_TOKEN")

    return (
        access_token.strip() if access_token else None,
        refresh_token.strip() if refresh_token else None,
    )


async def wake_all_cars(controller: Controller) -> None:
    """Wake up every car on the account so that data requests succeed.

    Tesla returns HTTP 408 (VEHICLE_UNAVAILABLE) for ``vehicle_data`` requests
    when a car is asleep or offline. Waking the car first ensures subsequent
    polling/commands return live data.

    Note: waking a vehicle draws on the 12V battery and prevents the car from
    sleeping, so only do this when fresh data is actually needed.
    """
    vehicles = list(controller.cars.values())
    if not vehicles:
        logger.warning("No vehicles found to wake up.")
        return

    for car in vehicles:
        if car.is_on:
            logger.info("%s is already awake.", car.display_name)
            continue

        logger.info("Waking up %s (this can take up to 60s)...", car.display_name)
        try:
            awake = await controller.wake_up(car.id)
            if awake:
                logger.info("%s is now awake.", car.display_name)
            else:
                logger.warning(
                    "%s did not wake within the timeout; data may be unavailable.",
                    car.display_name,
                )
        except TeslaException as exc:
            logger.error("Failed to wake %s: %s", car.display_name, exc)


async def example_get_vehicle_state(controller: Controller) -> None:
    """Get and display every available vehicle state parameter.

    All read-only properties exposed by the ``TeslaCar`` object are
    enumerated dynamically, so this automatically reflects any properties
    added to the library over time.
    """
    logger.info("=== Getting Vehicle State ===")

    await controller.update()  # Poll all vehicles
    vehicles = list(controller.cars.values())

    if not vehicles:
        logger.warning("No vehicles found")
        return

    for car in vehicles:
        logger.info("--- Vehicle: %s (VIN: %s) ---", car.display_name, car.vin)

        # Collect every read-only property defined on TeslaCar (and any base
        # classes), then print its current value.
        property_names = set()
        for klass in type(car).__mro__:
            for name, attr in vars(klass).items():
                if isinstance(attr, property):
                    property_names.add(name)

        for name in sorted(property_names):
            try:
                value = getattr(car, name)
            except Exception as exc:  # pylint: disable=broad-except
                value = f"<unavailable: {exc}>"
            logger.info("  %s: %s", name, value)


async def example_monitor_realtime_updates(controller: Controller) -> None:
    """Monitor vehicle updates via WebSocket."""
    logger.info("=== Monitoring Real-Time Updates ===")
    
    update_count = 0
    
    async def on_update(msg):
        nonlocal update_count
        update_count += 1
        logger.info(f"Vehicle update #{update_count}: {msg}")
    
    # Register WebSocket callback
    # register_websocket_callback is synchronous; it returns the listener index.
    controller.register_websocket_callback(on_update)
    logger.info("WebSocket callback registered. Waiting for updates...")
    
    # Wait for a few updates (30 seconds max)
    for i in range(30):
        await asyncio.sleep(1)
        if update_count >= 3:
            logger.info(f"Received {update_count} updates, stopping")
            break
    
    if update_count == 0:
        logger.warning("No WebSocket updates received (vehicle may be offline)")



async def interactive_menu(controller: Controller) -> None:
    """Interactive menu for testing examples."""
    loop = asyncio.get_event_loop()
    
    while True:
        print("\n=== teslajsonpy Example Application ===")
        print("1. Get vehicle state")
        print("2. Monitor real-time updates")
        print("3. Exit")
        
        # Run input() in a thread pool to prevent blocking the event loop
        choice = await loop.run_in_executor(None, input, "\nSelect an option (1-3): ")
        choice = choice.strip()
        
        try:
            if choice == "1":
                await example_get_vehicle_state(controller)
            elif choice == "2":
                await example_monitor_realtime_updates(controller)
            elif choice == "3":
                logger.info("Exiting...")
                break
            else:
                print("Invalid option")
        except Exception as e:
            logger.error(f"Error: {e}")


async def main():
    """Main entry point."""
    loop = asyncio.get_event_loop()

    print("\n=== teslajsonpy Example Application ===\n")

    # Load tokens from environment variables
    access_token, refresh_token = load_tokens()

    if not (access_token and refresh_token):
        logger.error(
            "No tokens found. Provide tokens via environment variables:\n"
            "  export TESLA_ACCESS_TOKEN='...'\n"
            "  export TESLA_REFRESH_TOKEN='...'\n"
        )
        return

    logger.info("Loaded tokens from environment.")

    # Calculate expiration time - tokens typically last 8 hours (28800 seconds)
    # Set it to 1 hour in the future to be safe
    now = calendar.timegm(datetime.datetime.now().timetuple())
    expiration = now + 3600  # 1 hour from now

    async with AsyncClient(http2=True) as session:
        controller = Controller(
            websession=session,
            access_token=access_token,
            refresh_token=refresh_token,
            expiration=expiration,
            enable_websocket=True,
        )

        try:
            logger.info("Connecting to Tesla API...")
            await controller.connect()
            logger.info("Successfully connected!")

            # Build the TeslaCar / EnergySite objects from the account.
            # connect() only fetches the raw product list; the car and
            # car objects must be generated explicitly.
            await controller.generate_car_objects()

            # Wake sleeping cars so vehicle_data requests don't return
            # HTTP 408 (VEHICLE_UNAVAILABLE).
            await wake_all_cars(controller)

            # Show interactive menu
            await interactive_menu(controller)

        except Exception as e:
            logger.error(f"Connection failed: {e}")
        finally:
            logger.info("Disconnecting...")


if __name__ == "__main__":
    asyncio.run(main())
