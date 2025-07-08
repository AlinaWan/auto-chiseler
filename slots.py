# -*- coding: utf-8 -*-
"""
slots.py

Set enable_slots_socket to True in the config.py module
to allow processor.py to forward detected objects over IPC port
54171, then run this file by itself
"""
import tkinter as tk
import socket
import threading
import json
import random

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

RANK_TK_HEX = {rank: bgr_to_rgb_hex(bgr) for rank, bgr, _ in RANKS}

class SlotMachineApp:
    """
    A Tkinter-based GUI application that displays a dynamic slot machine interface.

    The application listens on a TCP socket for incoming JSON-encoded rank data,
    which it animates and displays across a configurable number of slot columns.
    Users can toggle the visibility of a control panel to adjust how many columns
    are shown in the interface (between 1 and 4) without restarting the app.
    A subtle hint label guides users to press 'C' to show or hide this control panel.

    The slot machine visualizes rank symbols with color coding, animating
    slot spins and final rank display upon receiving new data.

    :ivar root: The Tkinter root window reference.
    :vartype root: tkinter.Tk

    :ivar visible_columns: Number of slot columns currently visible (default is 4).
    :vartype visible_columns: int

    :ivar slot_labels: List of Tkinter Label widgets representing each slot column.
    :vartype slot_labels: list[tk.Label]

    :ivar label_fg: Foreground color used for labels in the control frame.
    :vartype label_fg: str

    :ivar entry_bg: Background color used for the input entry widget.
    :vartype entry_bg: str

    :ivar entry_fg: Foreground color used for the input entry widget text.
    :vartype entry_fg: str

    :ivar btn_bg: Background color for the update button.
    :vartype btn_bg: str

    :ivar btn_fg: Foreground color for the update button text.
    :vartype btn_fg: str

    :ivar control_frame: Tkinter Frame containing the column adjustment input and button.
    :vartype control_frame: tk.Frame

    :ivar columns_var: Tkinter StringVar linked to the input entry for column count.
    :vartype columns_var: tk.StringVar

    :ivar columns_entry: Tkinter Entry widget for column count input.
    :vartype columns_entry: tk.Entry

    :ivar slots_frame: Tkinter Frame holding the slot label widgets.
    :vartype slots_frame: tk.Frame

    :ivar hint_label: Small label displayed at the bottom, guiding users to toggle control visibility.
    :vartype hint_label: tk.Label
    """
    def __init__(self, root):
        """
        Initialize the SlotMachineApp instance.

        Sets up the main window styling, creates slot label widgets (maximum 4),
        and initializes the hidden control frame with an entry and update button
        for adjusting visible slot columns. Starts a background thread that listens
        for incoming rank data over a TCP socket and triggers animations accordingly.

        The method also sets up key bindings to toggle the visibility of the control
        frame when the user presses the 'C' key and adds a small hint label at the
        bottom of the window to inform users about this feature.

        :param root: The root Tkinter window for the GUI.
        :type root: tkinter.Tk
        """
        self.root = root
        self.root.configure(bg="#222222")
        self.visible_columns = 4  # default visible columns
        self.slot_labels = []

        # Colors for input styling
        self.label_fg = "#eeeeee"
        self.entry_bg = "#333333"
        self.entry_fg = "#ffffff"
        self.btn_bg = "#444444"
        self.btn_fg = "#dddddd"

        # Control frame for input + button (hidden by default)
        self.control_frame = tk.Frame(root, bg="#222222")
        self.control_frame.pack(pady=(10, 0))
        self.control_frame.pack_forget()  # hide initially

        tk.Label(self.control_frame, text="Columns (1-4):", fg=self.label_fg, bg="#222222").pack(side="left")
        self.columns_var = tk.StringVar(value=str(self.visible_columns))
        self.columns_entry = tk.Entry(self.control_frame, textvariable=self.columns_var, width=3,
                                      bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.columns_entry.pack(side="left", padx=5)

        update_btn = tk.Button(self.control_frame, text="Update", command=self.update_columns,
                               bg=self.btn_bg, fg=self.btn_fg, activebackground="#555555", activeforeground="#ffffff")
        update_btn.pack(side="left")

        # Frame for slots
        self.slots_frame = tk.Frame(root, bg="#222222")
        self.slots_frame.pack(padx=20, pady=40)

        # Create all 4 labels but only show some
        for _ in range(4):
            lbl = tk.Label(self.slots_frame, text="", width=5, height=2,
                           font=("Courier New", 24, "bold"), bg="#000000", fg="#FFFFFF", bd=3, relief="sunken")
            lbl.pack(side="left", padx=10)
            self.slot_labels.append(lbl)

        self.apply_column_visibility()

        # Tiny hint label at bottom
        self.hint_label = tk.Label(root, text="Press C to configure columns",
                                   fg="#888888", bg="#222222", font=("Arial", 8))
        self.hint_label.pack(side="bottom", pady=4)

        # Bind C key press to toggle control frame visibility
        root.bind("<c>", self.toggle_control_frame)
        root.bind("<C>", self.toggle_control_frame)  # also uppercase C

        threading.Thread(target=self.listen_for_data, daemon=True).start()

    def toggle_control_frame(self, event=None):
        """
        Toggle the visibility of the control frame that allows column configuration.
    
        If the control frame is currently visible, hide it by unpacking.
        If hidden, show it and set keyboard focus to the input entry field.
    
        This method is typically bound to the 'C' key press event.
    
        :param event: Optional Tkinter event object (default is None).
        :type event: tkinter.Event or None
        :rtype: None
        """
        if self.control_frame.winfo_ismapped():
            self.control_frame.pack_forget()
        else:
            self.control_frame.pack(pady=(10, 0))
            self.columns_entry.focus_set()

    def update_columns(self):
        """
        Update the number of visible slot columns based on user input.
    
        Reads the value from the input entry, validates it as an integer within
        the allowed range [1, 4]. If invalid or out of range, it clamps to the nearest
        boundary or falls back to 4 by default.
    
        After updating `self.visible_columns`, it calls `apply_column_visibility`
        to reflect the change immediately in the GUI.

        :rtype: None
        """
        try:
            n = int(self.columns_var.get())
            if n < 1:
                n = 1
            elif n > 4:
                n = 4
        except ValueError:
            n = 4  # fallback if invalid input

        self.visible_columns = n
        self.apply_column_visibility()

    def apply_column_visibility(self):
        """
        Adjust the visibility of slot labels based on the current visible columns count.
    
        Shows the first `self.visible_columns` slot labels by packing them,
        and hides the rest by unpacking. This controls how many slot columns
        are visible in the interface at any time.

        :rtype: None
        """
        # Show only the first N labels, hide the rest
        for i, lbl in enumerate(self.slot_labels):
            if i < self.visible_columns:
                lbl.pack(side="left", padx=10)
            else:
                lbl.pack_forget()

    def listen_for_data(self):
        """
        Continuously listen for incoming TCP connections carrying JSON-encoded slot rank data.
    
        Binds and listens on localhost port 54171. For each accepted connection,
        it receives data, attempts to parse it as JSON list of ranks, pads the list
        to 4 items if shorter, then schedules the `animate_slots` method call
        on the main Tkinter thread.
    
        Logs parse errors to the console but continues listening indefinitely.

        :rtype: None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 54171))
            s.listen(1)
            print("Slot Machine Display: Listening on port 54171")
            while True:
                conn, _ = s.accept()
                with conn:
                    data = conn.recv(1024)
                    try:
                        ranks = json.loads(data.decode("utf-8"))
                        # pad to 4 if less
                        ranks += [""] * (4 - len(ranks))
                        self.root.after(0, lambda r=ranks: self.animate_slots(r))
                    except Exception as e:
                        print(f"IPC parse error: {e}")

    def animate_slots(self, final_ranks):
        """
        Animate the slot columns spinning and display the final ranks.
    
        Performs a short spin animation cycling through random ranks in the visible columns,
        then updates the visible slot labels with the final ranks. Hidden slot labels
        (beyond the visible columns) are cleared.
    
        :param final_ranks: List of rank strings representing the final result to display.
                            Should contain at least 4 items; excess are ignored,
                            and missing ranks are padded externally.
        :type final_ranks: list[str]
        :rtype: None
        """
        def _spin_step(frame_count):
            if frame_count >= 10:
                # Final ranks - only show visible columns
                for i in range(self.visible_columns):
                    rank = final_ranks[i]
                    color = RANK_TK_HEX.get(rank, "#444444")
                    self.slot_labels[i].config(text=rank, fg=color)
                # Clear hidden labels
                for i in range(self.visible_columns, 4):
                    self.slot_labels[i].config(text="", fg="#222222")
                return

            # Spin effect: random ranks on visible columns only
            for i in range(self.visible_columns):
                rand_rank = random.choice(list(RANK_TK_HEX.keys()))
                self.slot_labels[i].config(text=rand_rank, fg=RANK_TK_HEX[rand_rank])
            # Hide rest during spin
            for i in range(self.visible_columns, 4):
                self.slot_labels[i].config(text="", fg="#222222")

            self.root.after(100, _spin_step, frame_count + 1)

        _spin_step(0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pip Reroller Slot Machine")
    root.attributes("-topmost", True)
    app = SlotMachineApp(root)
    root.mainloop()

