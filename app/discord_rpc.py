# -*- coding: utf-8 -*-
"""
discord_rpc.py

Set ENABLE_DISCORD_RPC to True in config.py to enable Discord Rich Presence integration.
"""
from pypresence import Presence
import time
import threading

DISCORD_CLIENT_ID = "1393968832342786068"  # Your app ID
_rpc = None
_start_time = None
_lock = threading.Lock()

def init():
    global _rpc, _start_time
    with _lock:
        if _rpc is not None:
            return
        try:
            _rpc = Presence(DISCORD_CLIENT_ID)
            _rpc.connect()
            _start_time = int(time.time())
            print("[Discord RPC] Connected.")
        except Exception as e:
            print("[Discord RPC] Failed to connect:", e)
            _rpc = None

def update(
    min_quality: str,
    min_objects: int,
    ss_count: int,
    stop_at_ss: int,
    rolling: bool,
    stopped_from_condition: bool = False
):
    with _lock:
        if _rpc is None:
            return
        try:
            # Compose stop conditions display
            stop_conditions = []
            if min_objects > 0:
                stop_conditions.append(f"{min_objects} ≥ {min_quality}")
            if stop_at_ss > 0:
                stop_conditions.append(f"{stop_at_ss} SS")

            stop_condition_text = ", ".join(stop_conditions) if stop_conditions else "None"

            details = f"Target: {stop_condition_text}"

            if rolling:
                state = "Rolling..."
            else:
                parts = ["Stopped"]
                if stop_at_ss > 0:
                    parts.append(f"SS: {ss_count}/{stop_at_ss}")
                state = " | ".join(parts)

            _rpc.update(
                details=details,
                state=state,
                start=_start_time,
                large_image="rerolling",
                large_text="Pip Reroller by Riri",
            )
        except Exception as e:
            print("[Discord RPC] Update failed:", e)

def clear():
    with _lock:
        if _rpc is None:
            return
        try:
            _rpc.clear()
            print("[Discord RPC] Cleared.")
        except Exception as e:
            print("[Discord RPC] Clear failed:", e)

def shutdown():
    with _lock:
        global _rpc
        if _rpc is None:
            return
        try:
            _rpc.close()
            print("[Discord RPC] Disconnected.")
        except Exception as e:
            print("[Discord RPC] Shutdown failed:", e)
        finally:
            _rpc = None
