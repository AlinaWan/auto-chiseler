# -*- coding: utf-8 -*-
"""
theme.py
"""
import tkinter as tk

from app.config import THEME

# Theme definitions
THEMES = {
    "light": {
        "bg": "#ffffff",
        "label_fg": "#000000",
        "entry_bg": "#eeeeee",
        "entry_fg": "#111111",
        "btn_bg": "#dddddd",
        "btn_fg": "#000000",
    },
    "dark": {
        "bg": "#222222",
        "label_fg": "#ffffff",
        "entry_bg": "#333333",
        "entry_fg": "#ffffff",
        "btn_bg": "#444444",
        "btn_fg": "#dddddd",
    },
    "amoled": {
        "bg": "#000000",
        "label_fg": "#ffffff",
        "entry_bg": "#1a1a1a",
        "entry_fg": "#ffffff",
        "btn_bg": "#111111",
        "btn_fg": "#dddddd",
    },
    "pink": {
        "bg": "#ffc5d3",
        "label_fg": "#000000",
        "entry_bg": "#424242",
        "entry_fg": "#ffffff",
        "btn_bg": "#444444",
        "btn_fg": "#dddddd",
    },
    "high_contrast": {
        "bg": "#000000",
        "label_fg": "#ffff00",
        "entry_bg": "#000000",
        "entry_fg": "#ffff00",
        "btn_bg": "#000000",
        "btn_fg": "#00ffff",
    },
    "solarized_light": {
        "bg": "#fdf6e3",
        "label_fg": "#657b83",
        "entry_bg": "#eee8d5",
        "entry_fg": "#586e75",
        "btn_bg": "#eee8d5",
        "btn_fg": "#586e75",
    },
    "solarized_dark": {
        "bg": "#002b36",
        "label_fg": "#839496",
        "entry_bg": "#073642",
        "entry_fg": "#93a1a1",
        "btn_bg": "#073642",
        "btn_fg": "#93a1a1",
    },
}

# Use the chosen theme, fallback to 'dark' if invalid
theme = THEMES.get(THEME, THEMES["dark"])

# Create global variables for each theme key
for key, value in theme.items():
    globals()[key] = value

def make_label(text, **kwargs):
    return tk.Label(**{"text": text, "fg": theme["label_fg"], "bg": theme["bg"]}, **kwargs)

def is_light_color(hex_color):
    """Return True if the color is light, False if dark."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Standard luminance formula (ITU-R BT.709)
    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return brightness > 160  # threshold can be tuned

def adjust_color(hex_color, factor=0.7):
    """
    Adjusts the color for contrast: darkens light colors, lightens dark colors.
    `factor < 1` makes bigger changes; defaults to 0.7 (30% shift).
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
    is_light = brightness > 160

    if is_light:
        # Darken bright colors
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
    else:
        # Lighten dark colors — including pure black
        min_light = int(255 * (1 - factor))  # Prevent black staying black
        r = int(max(min_light, r / factor))
        g = int(max(min_light, g / factor))
        b = int(max(min_light, b / factor))

    r = min(255, r)
    g = min(255, g)
    b = min(255, b)

    return f"#{r:02x}{g:02x}{b:02x}"
