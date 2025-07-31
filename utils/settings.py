import os
import json
from utils.resource_manager import get_config_directory

USER_SETTINGS_PATH = os.path.join(get_config_directory(), "user_settings.json")

# Load once at import time
def load_settings():
    if os.path.exists(USER_SETTINGS_PATH):
        with open(USER_SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {
        "max_orbs": 0,
        "use_revive_candles": False,
        "debug_mode": False,
        "auto_set_boost_to_max": False,
        "auto_collect_ticket_from_giftbox": False,
        "max_tickets": -1,
        "brave_battles_tickets": 5
    }

def save_settings():
    with open(USER_SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)

# Global settings dictionary
settings = load_settings()