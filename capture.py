# -*- coding: utf-8 -*-
"""
capture.py
"""
import win32gui
import win32ui
import win32con
import numpy as np
import cv2

class ScreenCapture:
    """
    Provides optimized screen capture functionality for Windows using ``win32gui`` and ``win32ui``.

    This class manages low-level Windows GDI resources such as Device Contexts (DC) and bitmaps
    to enable fast and efficient screen captures. It is designed for repeated capturing operations
    with minimal overhead.

    :ivar hwnd: Handle to the desktop window.
    :vartype hwnd: int

    :ivar hwindc: Handle to the window device context.
    :vartype hwindc: PyHANDLE or None

    :ivar srcdc: Source device context obtained from the window DC.
    :vartype srcdc: PyCDC or None

    :ivar memdc: Memory device context compatible with the source DC.
    :vartype memdc: PyCDC or None

    :ivar bmp: Bitmap object used for storing captured image data.
    :vartype bmp: PyCBitmap or None

    :ivar _initialized: Indicates whether the capture resources have been initialized.
    :vartype _initialized: bool

    :ivar _last_bbox: Stores the bounding box of the last capture (left, top, right, bottom).
    :vartype _last_bbox: tuple or None

    :ivar _last_width: Width of the last captured area in pixels.
    :vartype _last_width: int

    :ivar _last_height: Height of the last captured area in pixels.
    :vartype _last_height: int

    :raises win32gui.error: If obtaining the desktop window handle fails.
    :rtype: None
    """
    def __init__(self):
        """
        Initialize the ScreenCapture object and set up internal state.

        Obtains a handle to the desktop window using ``win32gui.GetDesktopWindow()``,
        and initializes internal attributes related to GDI device contexts and screen capture.
        Capture resources (DCs and bitmap) are not created until ``_initialize_dc`` is called.

        :raises win32gui.error: If obtaining the desktop window handle fails.
        :rtype: None
        """
        self.hwnd = win32gui.GetDesktopWindow() # Handle to the desktop window
        self.hwindc = None
        self.srcdc = None
        self.memdc = None
        self.bmp = None
        self._initialized = False
        self._last_bbox = None
        self._last_width = 0
        self._last_height = 0

    def _initialize_dc(self, width, height):
        """
        Initializes GDI device contexts and bitmap for screen capturing.
    
        This method sets up the required Windows GDI resources, including the source
        device context, a compatible memory DC, and a compatible bitmap of the given
        dimensions. These resources are required for fast and direct pixel access
        during screen capture operations.
    
        If initialization fails, it cleans up any partially created resources and
        returns False.
    
        :param int width: The width of the capture area in pixels.
        :param int height: The height of the capture area in pixels.
        :returns: True if initialization succeeded, False otherwise.
        :rtype: bool
        :raises Exception: If there is an unexpected error during GDI setup.
        """
        try:
            self.hwindc = win32gui.GetWindowDC(self.hwnd) # Get DC for the entire screen
            self.srcdc = win32ui.CreateDCFromHandle(self.hwindc) # Create a DC object from the screen DC
            self.memdc = self.srcdc.CreateCompatibleDC() # Create a compatible DC in memory
            self.bmp = win32ui.CreateBitmap() # Create a bitmap object
            # Create a compatible bitmap with the specified dimensions
            self.bmp.CreateCompatibleBitmap(self.srcdc, width, height)
            self.memdc.SelectObject(self.bmp) # Select the bitmap into the memory DC
            self._initialized = True
            self._last_width = width
            self._last_height = height
        except Exception as e:
            print(f"Error initializing DC: {e}")
            self._cleanup() # Ensure cleanup on initialization failure
            return False
        return True

    def _cleanup(self):
        """
        Releases and cleans up all allocated GDI resources.
    
        This method safely disposes of the memory DC, source DC, bitmap, and
        window DC used during screen capture operations. It ensures no
        resource leaks occur, even if some of the resources are already
        released or failed to initialize.
    
        Exceptions during cleanup are caught and printed, but do not stop
        the cleanup process. After execution, the internal state is marked
        as uninitialized.
    
        :rtype: None
        """
        try:
            if self.memdc:
                self.memdc.DeleteDC()
                self.memdc = None
        except Exception as e: print(f"Cleanup memdc error: {e}")
        try:
            if self.srcdc:
                self.srcdc.DeleteDC()
                self.srcdc = None
        except Exception as e: print(f"Cleanup srcdc error: {e}")
        try:
            if self.hwindc:
                win32gui.ReleaseDC(self.hwnd, self.hwindc)
                self.hwindc = None
        except Exception as e: print(f"Cleanup hwindc error: {e}")
        try:
            if self.bmp:
                win32gui.DeleteObject(self.bmp.GetHandle()) # Delete the bitmap object
                self.bmp = None
        except Exception as e: print(f"Cleanup bmp error: {e}")
        self._initialized = False

    def capture(self, bbox=None):
        """
        Captures a screenshot of the specified screen region.
    
        This method captures a portion of the screen defined by the given bounding box.
        It manages GDI resource re-initialization if the bounding box or its dimensions
        differ from the previous capture. The captured image is returned as a BGR NumPy
        array suitable for use with OpenCV.
    
        If `bbox` is `None`, or if width/height are invalid or capture fails,
        `None` is returned.
    
        :param tuple[int, int, int, int] bbox: Optional. The bounding box of the region to
            capture in the format (left, top, right, bottom).
        :returns: The captured image as a BGR NumPy array, or ``None`` if the capture failed.
        :rtype: numpy.ndarray or None
        :raises Exception: If a GDI call fails unexpectedly during capture.
        """
        if not bbox: return None
        left, top, right, bottom = bbox
        width, height = right - left, bottom - top
        if width <= 0 or height <= 0: return None

        # Re-initialize GDI objects if the bounding box or its dimensions change
        if (self._last_bbox != bbox or not self._initialized or
                width != self._last_width or height != self._last_height):
            self._cleanup()
            self._last_bbox = bbox # Update _last_bbox for the new region

        if not self._initialized:
            if not self._initialize_dc(width, height): return None

        try:
            # BitBlt copies the pixel data from the screen DC to the memory DC
            self.memdc.BitBlt((0, 0), (width, height), self.srcdc, (left, top), win32con.SRCCOPY)
            # Get the bitmap bits
            signedIntsArray = self.bmp.GetBitmapBits(True)
            # Convert to NumPy array and reshape to HxWx4 (BGRA)
            img = np.frombuffer(signedIntsArray, dtype='uint8').reshape((height, width, 4))
            # Convert BGRA to BGR for OpenCV compatibility
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            print(f"Capture error: {e}")
            self._cleanup() # Cleanup on error to force re-initialization next time
            return None

    def close(self):
        """
        Releases all screen capture resources.
    
        Public method that explicitly cleans up all allocated GDI handles and internal
        buffers used for capturing. This should be called when the `ScreenCapture`
        instance is no longer needed to avoid leaking system resources.
    
        :rtype: None
        """
        self._cleanup()
