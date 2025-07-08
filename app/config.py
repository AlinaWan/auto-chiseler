# -*- coding: utf-8 -*-
"""
config.py
"""
# [DEBUG] Enable/disable logging
ENABLE_LOGGING = False  # Set to True to enable logging

# [FUN] Enable/disable object forwarding from processor.py to slots.py
ENABLE_SLOTS_SOCKET = False # Set to True to enable slots socket functionality (Required to pass objects to slots.py over IPC)
SLOTS_SOCKET_PORT = 54171 # Port for the slots socket connection