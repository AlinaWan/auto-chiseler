# -*- coding: utf-8 -*-
"""
config.py
"""
THEME = "dark"  # Theme names are listed in theme.py (defaults to dark if invalid)

# [DEBUG] Enable/disable logging
ENABLE_LOGGING = False  # Set to True to enable logging

# Discord Rich Presence configuration
ENABLE_DISCORD_RPC = True  # Set to True to enable Discord Rich Presence

# [FUN] Enable/disable object forwarding from processor.py to slots.py
ENABLE_SLOTS_SOCKET = False # Set to True to enable slots socket functionality (Required to pass objects to slots.py over IPC)
SLOTS_SOCKET_PORT = 54171 # Port for the slots socket connection