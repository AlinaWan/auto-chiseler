# -*- coding: utf-8 -*-
"""
config.py
"""
import configparser
import os
import sys

_DEFAULTS = {
    "THEME": "dark",                  # Theme names are listed in theme.py (defaults to dark if invalid)
    "ENABLE_LOGGING": False,          # Set to True to enable logging
    "ENABLE_DISCORD_RPC": False,      # Set to True to enable Discord Rich Presence
    "ENABLE_SLOTS_SOCKET": False,     # Set to True to enable slots socket functionality (Required to pass objects to slots.py over IPC)
    "SLOTS_SOCKET_PORT": 54171,       # Port for the slots socket connection
}

# Set module-level variables from the _DEFAULTS dictionary.
globals().update(_DEFAULTS)

# If __compiled__ is set in globals(), use the .ini file for configuration.
if '__compiled__' in globals():
    outer_exe = sys.argv[0]
    ini_path = os.path.join(os.path.dirname(outer_exe), 'config.ini')
    config = configparser.ConfigParser()

    print("Config file resolved to:", ini_path)

    # If the .ini file doesn't exist, create it using the defaults.
    if not os.path.exists(ini_path):
        # Write the defaults to the ini file.
        config['DEFAULT'] = {key: str(value) for key, value in _DEFAULTS.items()}
        with open(ini_path, 'w') as f:
            config.write(f)
    else:
        # Read the existing ini file.
        config.read(ini_path)

    # Update the module-level globals with values from the ini file,
    # preserving the type by referring to _DEFAULTS.
    for key, default_value in _DEFAULTS.items():
        if isinstance(default_value, bool):
            globals()[key] = config['DEFAULT'].getboolean(key, fallback=default_value)
        elif isinstance(default_value, int):
            globals()[key] = config['DEFAULT'].getint(key, fallback=default_value)
        else:
            globals()[key] = config['DEFAULT'].get(key, fallback=default_value)
