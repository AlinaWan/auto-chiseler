# -*- coding: utf-8 -*-
"""
constants.py
"""
# --- Class ranks, order, and their colors (BGR for OpenCV, HEX for Tkinter) ---
RANKS = [
    ("F",   (182, 171, 165),  "#b6aba5"),
    ("D",   (243, 177, 149),  "#f3b195"),
    ("C",   (130, 255, 105),  "#82ff69"),
    ("B",   (255, 134, 148),  "#ff8694"),
    ("A",   (66, 201, 255),   "#42c9ff"),
    ("S",   (102, 56, 255),   "#6638ff"),
    ("SS",  (174, 130, 255),  "#ae82ff"),
]

def bgr_to_rgb_hex(bgr):
    """
    Converts a BGR color tuple to a hexadecimal RGB string.

    This function takes a color in BGR (Blue, Green, Red) format and returns
    the equivalent RGB hex string (e.g., ``#rrggbb``) commonly used in web and
    GUI color specifications.

    :param tuple[int, int, int] bgr: A tuple representing a BGR color, with each
        component in the range 0–255.
    :returns: A string representing the color in ``#rrggbb`` RGB hex format.
    :rtype: str
    :raises ValueError: If the input is not a tuple of three integers.
    """
    b, g, r = bgr
    return f'#{r:02x}{g:02x}{b:02x}'

RANK_ORDER = {rank: i for i, (rank, _, _) in enumerate(RANKS)}
RANK_HEX = {rank: hexcode for rank, _, hexcode in RANKS}
RANK_TK_HEX = {rank: bgr_to_rgb_hex(bgr) for rank, bgr, _ in RANKS}