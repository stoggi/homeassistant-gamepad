import evdev
import os
from homeassistant_api import Client

# Read configuration from environment variables, set in docker compose
homeassistant_url = os.environ.get("HOMEASSISTANT_URL", default="http://127.0.0.1:8123/api")
homeassistant_token = os.environ.get("HOMEASSISTANT_TOKEN", default="")
homeassistant_entity = os.environ.get("HOMEASSISTANT_ENTITY", default="light.office_lights")
input_device = os.environ.get("INPUT_DEVICE", default="/dev/input/event0")

# Connect to the linux input device
device = evdev.InputDevice(input_device)

# Using the home assistant API
with Client(homeassistant_url, homeassistant_token) as client:
    light = client.get_domain(homeassistant_entity.split(".")[0])
    # Poll for events from the linux input device
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.value:
                # For key press down events, toggle the home assistant device
                light.toggle(entity_id=homeassistant_entity)
