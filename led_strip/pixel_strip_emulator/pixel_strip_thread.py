# -*- coding: utf-8 -*-
"""
Wrap the strip emulator so it runs in its own thread.
"""

# Import python modules.
import threading
import time

# Import the pixel strip object.
from .pixel_strip import PixelStrip as PixelStripBase


# Global values to set colors of strip.
UPDATE = False
COLORS = []


class PixelStrip(object):
    """
    Wrap the PixelStrip object, so it runs in a thread.
    """

    def __init__(self, n_led, _, channel=None):
        """
        Initialize the strip and start the display thread.
        """

        # Initialize colors.
        global COLORS
        self.n_led = n_led
        COLORS = [(0, 0, 0) for _i in range(n_led)]

        # Start strip kernel.
        kernel = threading.Thread(target=update_strip, daemon=True,
            args=[n_led])
        kernel.start()

    def begin(self):
        """Dummy method."""
        pass

    def numPixels(self):
        """Return the number of leds in the strip."""
        return self.n_led

    def setPixelColor(self, i, color):
        """Set a single LED color of the strip."""
        global COLORS
        COLORS[i] = color

    def show(self):
        """Show the strip."""
        global UPDATE
        UPDATE = True


def update_strip(n_led):
    """
    Function to run in an own thread that handles the actual visualization of
    the led strip.
    """

    global UPDATE, COLOR

    # Initialize the pixel strip.
    strip = PixelStripBase(n_led)
    strip.begin()

    while True:
        # Check for updates at 60 fps.
        time.sleep(1.0 / 60.0)
        if UPDATE:
            for i in range(len(COLORS)):
                strip.setPixelColor(i, COLORS[i])
            strip.show()
            UPDATE = False
        else:
            pass
