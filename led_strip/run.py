# -*- coding: utf-8 -*-
"""
The main script to run the led strip controls.
"""

# Python modules.
import math
import threading
import time
import copy

# Import LED driver.
from rpi_ws281x import PixelStrip, Color


class Control(object):

    def __init__(self):
        self.mode = None
        self.color = None
        self.frequency = None

    def set_state(self):
        mode = input('mode: ')
        r = int(input('red: '))
        g = int(input('green: '))
        b = int(input('blue: '))
        frequency = 1.0 / float(input('period: '))
        with lock:
            self.mode = mode
            self.color = [r, g, b]
            self.frequency = frequency
            input('set state')


def strip_off():
    """
    Turn off the strip.
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def strip_single_color():
    """
    This set the strip to a single color.
    """

    # Get the current control state.
    with lock:
        control_data = copy.deepcopy(data)

    # Set the color.
    color = Color(control_data.color[0], control_data.color[1],
        control_data.color[2])
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


def strip_color_pulse():
    """
    This function creates a pulse effect for a single color.
    """

    # Number of frames for the pulse.
    n_frames = 100

    # Get the current control state.
    with lock:
        control_data = copy.deepcopy(data)

    while True:
        for j in range(n_frames):

            if not lock.locked():
                with lock:
                    control_data = copy.deepcopy(data)
                if not control_data.mode == 'pulse':
                    return

            factor = 0.5 * (-math.cos(j / n_frames * 2 * math.pi) + 1.0)
            color = Color(
                int(factor * control_data.color[0]),
                int(factor * control_data.color[1]),
                int(factor * control_data.color[2]))
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            time.sleep(1.0 / control_data.frequency / n_frames)
            strip.show()


def strip_rainbow():
    """
    Create a moving rainbow animation.
    """

    def wheel(pos):
        """
        Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    # Get the current control state.
    with lock:
        control_data = copy.deepcopy(data)

    while True:
        for j in range(256):

            if not lock.locked():
                with lock:
                    control_data = copy.deepcopy(data)
                if not control_data.mode == 'rainbow':
                    return

            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel(
                    (int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(1.0 / control_data.frequency / 256)


if __name__ == "__main__":

    strip = PixelStrip(60, 13, channel=1)
    strip.begin()

    data = Control()

    lock = threading.Lock()

    # By default the strip is turned off.
    last_mode = 'off'
    kernel = threading.Thread(target=strip_off, daemon=True)
    kernel.start()

    while True:

        # Get new state.
        data.set_state()

        if last_mode == data.mode:
            # The mode did not change, keep the mode running. Changed options
            # like color or frequency are handled inside the kernel.
            pass
        else:
            # The mode changed, wait for the kernel to finish.
            last_mode = data.mode
            kernel.join()

            # Start the new kernel, depending on which function is selected.
            if data.mode == 'off':
                kernel = threading.Thread(target=strip_off, daemon=True)
                kernel.start()
            elif data.mode == 'single_color':
                kernel = threading.Thread(target=strip_single_color,
                    daemon=True)
                kernel.start()
            elif data.mode == 'pulse':
                kernel = threading.Thread(target=strip_color_pulse,
                    daemon=True)
                kernel.start()
            elif data.mode == 'rainbow':
                kernel = threading.Thread(target=strip_rainbow, daemon=True)
                kernel.start()
