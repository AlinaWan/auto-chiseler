﻿# -*- coding: utf-8 -*-
__version__ = "2.0.0"
__author__ = "Riri"
__license__ = "MIT"

"""
main.pyw

Some detection and selection logic adapted from iamnotbobby <https://github.com/iamnotbobby> (MIT licensed).
This script is licensed under the MIT License.

MIT License

Copyright (c) 2025 Riri <https://github.com/AlinaWan>
Portions Copyright (c) 2025 bobby

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from tkinter import Tk

from app.utils import set_dpi_awareness
from app.app import PipRerollerApp

if __name__ == '__main__':
    # --- IMPORTANT: Call DPI awareness setup BEFORE Tkinter initialization ---
    set_dpi_awareness()
    root = Tk()
    app = PipRerollerApp(root)
    root.mainloop()
