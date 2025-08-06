# -*- coding: utf-8 -*-
"""
processor.py
"""
import threading
import time

import cv2

from app.capture import ScreenCapture
from app.config import ENABLE_LOGGING, ENABLE_SLOTS_SOCKET, SLOTS_SOCKET_PORT
from app.constants import RANKS, RANK_ORDER

class ImageProcessor(threading.Thread):
    """
    Thread that continuously captures screenshots, detects pips, and signals when reroll conditions are met.

    This class runs as a daemon thread to perform background image processing tasks
    independently from the main application flow. It captures screen regions, processes
    them to detect pip counts or ranks, updates shared state safely using threading locks,
    and can signal the main reroll loop to stop based on detection results.

    :ivar app: Reference to the main application instance, used for interaction and callbacks.
    :vartype app: object

    :ivar stop_event: Event used to signal this thread to stop execution gracefully.
    :vartype stop_event: threading.Event

    :ivar current_rank_counts: Dictionary mapping ranks to their current detected counts.
    :vartype current_rank_counts: dict

    :ivar lock: Lock to synchronize access to shared data like rank counts.
    :vartype lock: threading.Lock

    :ivar screen_capturer: Instance of the ScreenCapture class used for optimized screenshot capture.
    :vartype screen_capturer: ScreenCapture
    """
    def __init__(self, app_ref):
        """
        Initializes the ImageProcessor thread.
    
        :param object app_ref: Reference to the main application instance.
        :rtype: None
        """
        super().__init__(daemon=True) # Daemon thread exits when main program exits
        self.app = app_ref # Reference to the main app instance
        self.stop_event = threading.Event() # Event to signal this thread to stop
        self.current_rank_counts = {rank: 0 for rank, _, _ in RANKS}
        self.lock = threading.Lock() # Lock for safely accessing shared data (rank counts)
        self.screen_capturer = ScreenCapture() # Instantiate the optimized screen capturer

        self.pending_stop = None  # Stores a tuple (timestamp, detected_objs) or None
        self.delay_ms = 50  # Delay in ms before confirming stop

        self.ipc_host = None
        self.ipc_port = None

        # IPC (Inter-Process Communication) settings for slots display
        if ENABLE_SLOTS_SOCKET:
            ipc_host = "localhost"
            ipc_port = SLOTS_SOCKET_PORT
            self.ipc_host = ipc_host
            self.ipc_port = ipc_port

    def run(self):
        """
        Main loop for continuous image capturing and pip detection.
    
        This method runs in a dedicated daemon thread and performs the following:
        - Continuously captures screenshots of the defined game area.
        - Processes the captured images to detect and classify pips.
        - Updates shared rank counts with thread-safe locking.
        - Signals the main reroll loop to stop based on configurable stop conditions.
        - Updates the GUI asynchronously using Tkinter's `after` method.
        - Logs events if logging is enabled and conditions are met.
    
        The loop respects a polling delay and handles exceptions gracefully
        by logging errors and preventing tight looping on repeated failures.
    
        The thread will stop running when `stop_event` is set or when the stop
        conditions are satisfied and the main loop is signaled to stop.
    
        :rtype: None
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        
        while not self.stop_event.is_set():
            if self.app.game_area is None:
                time.sleep(0.1) # Wait if area not set by user
                continue

            try:
                # Capture screenshot using the optimized ScreenCapture class
                frame = self.screen_capturer.capture(bbox=self.app.game_area)
                if frame is None:
                    # Handle capture failure (e.g., invalid area, GDI error)
                    self.app.root.after(0, lambda: self.app.message_var.set("Screenshot capture failed. Retrying..."))
                    time.sleep(0.1) # Short delay before retrying capture
                    continue

                # Perform pip detection and classification
                detected_objs = self.app.detect_and_classify(frame)

                # Send detected ranks to slot display if IPC is enabled
                if self.ipc_host and self.ipc_port:
                    rank_list = [obj['rank'] for obj in detected_objs[:4]]
                    self.send_to_slot_display(rank_list)

                # Update shared rank counts safely for the GUI
                with self.lock:
                    new_counts = {rank: 0 for rank, _, _ in RANKS}
                    for obj in detected_objs:
                        new_counts[obj['rank']] += 1
                    self.current_rank_counts = new_counts
                    
                # Schedule GUI update on the main thread (Tkinter is not thread-safe)
                self.app.root.after(0, lambda: self.app.update_rank_counts_gui(detected_objs))

                # Check stop conditions based on detected pips
                min_rank_idx = RANK_ORDER[self.app.min_quality]
                filtered_objs = [obj for obj in detected_objs if RANK_ORDER[obj['rank']] >= min_rank_idx]
                ss_objs = [obj for obj in detected_objs if obj['rank'] == "SS"]

                should_stop = False
                if self.app.stop_at_ss > 0:
                    if len(filtered_objs) >= self.app.min_objects and len(ss_objs) >= self.app.stop_at_ss:
                        should_stop = True
                else:
                    if len(filtered_objs) >= self.app.min_objects:
                        should_stop = True

                # If conditions are met AND the main loop is currently running, signal it to stop
                now = time.time()
                
                # Check if a stop condition is freshly detected
                if should_stop and self.pending_stop is None:
                    self.pending_stop = (now, detected_objs)
                
                # If a stop is pending, and delay has passed, re-evaluate
                if self.pending_stop:
                    initial_time, initial_objs = self.pending_stop
                    if now - initial_time >= self.delay_ms / 1000:
                        # Re-capture and re-check conditions
                        frame = self.screen_capturer.capture(bbox=self.app.game_area)
                        recheck_objs = self.app.detect_and_classify(frame)
                
                        # Evaluate stop conditions again
                        min_rank_idx = RANK_ORDER[self.app.min_quality]
                        filtered_objs = [obj for obj in recheck_objs if RANK_ORDER[obj['rank']] >= min_rank_idx]
                        ss_objs = [obj for obj in recheck_objs if obj['rank'] == "SS"]
                
                        still_should_stop = False
                        if self.app.stop_at_ss > 0:
                            if len(filtered_objs) >= self.app.min_objects and len(ss_objs) >= self.app.stop_at_ss:
                                still_should_stop = True
                        else:
                            if len(filtered_objs) >= self.app.min_objects:
                                still_should_stop = True
                
                        if still_should_stop and self.app.running:
                            if ENABLE_LOGGING and recheck_objs:
                                self.app.log_event(
                                    recheck_objs,
                                    self.current_rank_counts.copy(),
                                    {
                                        "min_quality": self.app.min_quality,
                                        "min_objects": self.app.min_objects,
                                        "stop_at_ss": self.app.stop_at_ss,
                                        "tolerance": self.app.tolerance,
                                        "object_tolerance": self.app.object_tolerance,
                                        "click_delay_ms": self.app.click_delay_ms,
                                        "post_reroll_delay_ms": self.app.post_reroll_delay_ms,
                                        "image_poll_delay_ms": self.app.image_poll_delay_ms,
                                        "game_area": self.app.game_area,
                                        "chisel_button_pos": self.app.chisel_button_pos,
                                        "buy_button_pos": self.app.buy_button_pos,
                                    },
                                    decision="StopConditionMetAfterDelay: Confirmed stop after delay"
                                )
                            self.app.root.after(0, lambda: self.app.message_var.set(
                                f"Confirmed after {self.delay_ms}ms: Min {self.app.min_quality} x{self.app.min_objects}" +
                                (f", SS: {self.app.stop_at_ss}" if self.app.stop_at_ss > 0 else "") +
                                " met. Signalling stop."
                            ))
                            self.app.stop_running_async()
                            self.stop_event.set()
                            break
                        else:
                            # Condition no longer valid — cancel pending stop
                            self.pending_stop = None

                # Small delay to control the image polling rate
                time.sleep(self.app.image_poll_delay_ms / 1000)

            except Exception as e:
                # Log errors and prevent tight looping on continuous errors
                self.app.root.after(0, lambda: self.app.message_var.set(f"ImageProc Error: {e}"))
                time.sleep(0.5) # Prevent tight loop on error

    def get_current_rank_counts(self):
        """
        Retrieve a thread-safe copy of the latest detected rank counts.
    
        This method acquires a lock to safely access the shared rank counts dictionary
        and returns a copy to avoid race conditions.
    
        :returns: A copy of the current rank counts mapping ranks to their detected counts.
        :rtype: dict[str, int]
        """
        with self.lock:
            return self.current_rank_counts.copy()

    def stop(self):
        """
        Signals the image processing thread to stop and releases resources.
    
        This method sets the internal stop event, which causes the thread's
        main loop to exit gracefully. It also closes the screen capturer,
        cleaning up any allocated GDI resources.
    
        :rtype: None
        """
        self.stop_event.set()
        self.screen_capturer.close() # Close the screen capturer resources

    def send_to_slot_display(self, ranks):
        """
        Send the current detected ranks to the slot machine display application via IPC socket.
    
        This method attempts to establish a TCP connection to the configured IPC host and port,
        then serializes the provided list of rank strings as JSON and sends it over the socket.
    
        If IPC host or port are not set (None or falsy), the method returns immediately without sending.
    
        Handles `ConnectionRefusedError` silently, which typically means the slot machine
        display is not running or not listening, so no error is raised in that case.
    
        Any other exceptions during socket connection or send are caught and logged to the console.
    
        :param ranks: List of rank strings to send to the slot display.
        :type ranks: list[str]
        :rtype: None
        """
        import socket
        import json
        if not self.ipc_host or not self.ipc_port:
            return  # IPC is disabled
    
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ipc_host, self.ipc_port))
                s.sendall(json.dumps(ranks).encode('utf-8'))
        except ConnectionRefusedError:
            pass  # Slot machine not running
        except Exception as e:
            print(f"IPC send error: {e}")
