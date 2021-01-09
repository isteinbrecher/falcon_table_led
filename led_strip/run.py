# -*- coding: utf-8 -*-
"""
The main script to run the led strip controls.
"""

# Python modules.
import math
import threading
import time

# Import LED driver.
from rpi_ws281x import PixelStrip, Color


def strip_kernel():
    """
    This function keeps the strip going and creates the lightning effects.
    """

    strip = PixelStrip(60, 13, channel=1)
    strip.begin()

    # Get the initial color for the strip.
    with lock:
        color_list = data.copy()

    while True:
        for j in range(100):
            if not lock.locked():
                with lock:
                    color_list = data.copy()
            factor = 0.5 * (-math.cos(j / 100 * 2 * math.pi) + 1.0)
            color = Color(
                int(factor * color_list[0]),
                int(factor * color_list[1]),
                int(factor * color_list[2]))
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            time.sleep(0.01)
            strip.show()


def get_color():

    global data

    # Ask for a color.
    print('Enter new color:')
    r = int(input('red: '))
    g = int(input('green: '))
    b = int(input('blue: '))
    with lock:
        input('Set color to ({}, {}, {})'.format(r, g, b))
        data = [r, g, b]


if __name__ == "__main__":

    lock = threading.Lock()
    get_color()

    x = threading.Thread(target=strip_kernel, daemon=True)
    x.start()

    while True:
        get_color()
