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
        "bg": "#fff5fd",
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