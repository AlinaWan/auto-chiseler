# -*- coding: utf-8 -*-
"""
utils.py
"""
import os
import ctypes
import tkinter as tk

class Tooltip:
    """
    Creates a tooltip for a given Tkinter widget that appears after a delay
    when the mouse hovers over the widget.

    The tooltip follows the mouse cursor while it is over the widget
    and disappears when the mouse leaves.
    """
    def __init__(self, widget, text, delay=500):
        """
        Initializes the Tooltip.

        :param widget: The Tkinter widget to attach the tooltip to.
        :type widget: tkinter.Widget
        :param text: The text to display inside the tooltip.
        :type text: str
        :param delay: Delay in milliseconds before showing the tooltip after mouse enters the widget.
        :type delay: int
        """
        self.widget = widget
        self.text = text
        self.delay = delay  # milliseconds
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hide)
        self.widget.bind("<Motion>", self.move)

    def schedule(self, event=None):
        """
        Schedule the tooltip to be shown after the specified delay.
        Cancels any previously scheduled show event.
        """
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        """
        Cancel any scheduled tooltip show event if it exists.
        """
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show(self, event=None):
        """
        Display the tooltip near the widget, unless it's already visible
        or there is no text to show.
        Positions the tooltip offset slightly from the widget or text insertion point.
        """
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") if self.widget.winfo_class() == 'Entry' else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#4d4d4d", fg="white", relief='solid', borderwidth=1,
                         font=("tahoma", "9", "normal"))
        label.pack(ipadx=4, ipady=2)

    def hide(self, event=None):
        """
        Hide and destroy the tooltip window, and cancel any scheduled show events.
        """
        self.unschedule()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

    def move(self, event):
        """
        Move the tooltip window to follow the mouse cursor,
        offset slightly from the cursor position.
        """
        if self.tipwindow:
            x = event.x_root + 10
            y = event.y_root + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

# --- DPI Awareness ---
# This should be called as early as possible in the script execution.
# DPI Awareness Constants
PROCESS_DPI_UNAWARE = 0
PROCESS_SYSTEM_DPI_AWARE = 1
PROCESS_PER_MONITOR_DPI_AWARE = 2

def set_dpi_awareness():
    """
    Sets the DPI awareness for the current process on Windows systems.

    This function configures the process to be DPI-aware, allowing it to scale
    properly on high-DPI displays. It attempts to use per-monitor DPI awareness
    on Windows 8.1 and later, falling back to system DPI awareness on earlier
    versions. If an error occurs, a warning message is printed and the process
    may experience display scaling issues.

    On non-Windows systems, this function does nothing.

    :raises Exception: If setting DPI awareness fails for an unexpected reason
                       (other than missing API on older Windows versions).
    :rtype: None
    """
    if os.name == 'nt':  # Check if the OS is Windows
        try:
            # For Windows 8.1 and later, use Per-Monitor DPI Awareness
            # This allows the application to scale correctly when moved between
            # monitors with different DPI settings.
            ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        except AttributeError:
            # Fallback for Windows versions prior to 8.1 (e.g., Windows 7, 8)
            # Use System DPI Aware, which scales based on the primary display's DPI
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception as e:
            print(f"Warning: Could not set DPI awareness. Error: {e}")
            print("This might lead to coordinate issues on high-DPI displays.")
