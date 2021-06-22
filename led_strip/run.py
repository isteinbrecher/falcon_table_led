# -*- coding: utf-8 -*-
"""
The main script to run the led strip controls.
"""

# Python modules.
import math
import threading
import time
import copy
from flask import Flask, request, render_template, redirect, url_for
import os

if os.uname()[4][:3] == 'arm':
    # Import LED driver.
    from rpi_ws281x import PixelStrip, Color
elif os.uname()[4][:3] == 'x86':
    # Import LED driver emulator.
    from rpi_ws281x import Color
    from pixel_strip_emulator.pixel_strip_thread import PixelStrip
else:
    raise ValueError('Unknown system type')


class Control(object):
    """
    Object to store selected state of the strip.
    """

    def __init__(self):
        """
        Setup default values.
        """
        self.mode = None
        self.last_mode = None
        self.color = [255, 255, 255]
        self.frequency = 1.0
        self.brightness = 1.0

    def get_color_hex(self):
        """
        Return the color as a hex string.
        """
        return '#%02x%02x%02x' % tuple(val for val in self.color)

    def set_color_hex(self, hex_value):
        """
        Set the color from a hex string.
        """
        h = hex_value.lstrip('#')
        self.color = [int(h[i:i + 2], 16) for i in (0, 2, 4)]


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


def strip_color_pulse_single(control_data, calling_type='single_pulse'):
    """
    This function creates a single pulse effect for a single color.
    """

    # Number of frames for the pulse.
    n_frames = 100

    for j in range(n_frames):

        if not lock.locked():
            with lock:
                control_data = copy.deepcopy(data)
            if not control_data.mode == calling_type:
                return False

        factor = 0.5 * (-math.cos(j / n_frames * 2 * math.pi) + 1.0)
        color = Color(
            int(factor * control_data.color[0]),
            int(factor * control_data.color[1]),
            int(factor * control_data.color[2]))
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        time.sleep(1.0 / control_data.frequency / n_frames)
        strip.show()

    return True


def strip_color_pulse():
    """
    This function creates a endless effect for a single color.
    """

    # Get the current control state.
    with lock:
        control_data = copy.deepcopy(data)

    while True:
        if not strip_color_pulse_single(control_data, calling_type='pulse'):
            return


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


# Setup flask.
app = Flask(__name__)


@app.route('/mode/<name>', methods=['POST'])
def set_mode(name):

    global kernel

    with lock:
        # Lock the global data and set the new values.
        data.frequency = 1.0 / float(request.form['period'])
        data.set_color_hex(request.form['color'])
        data.brightness = float(request.form['brightness']) / 10.0
        data.mode = name

    if data.last_mode == data.mode and kernel.is_alive():
        # The mode did not change, keep the mode running. Changed options like
        # color or frequency are handled inside the kernel. This branch is only
        # executed if the thread is still running. Otherwise it will be started
        # again.
        pass
    else:
        # The mode changed, wait for the kernel to finish.
        data.last_mode = data.mode
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

    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html',
        host=request.host,
        color=data.get_color_hex(),
        brightness=int(10 * data.brightness),
        period=1.0 / data.frequency)


if __name__ == "__main__":
    """
    Execution part of script.
    """

    # Setup the script.
    strip = PixelStrip(200, 13, channel=1)
    strip.begin()

    # Setup the data container.
    data = Control()
    data.mode = 'single_pulse'
    data.last_mode = 'single_pulse'
    data.frequency = 1

    # Setup the lock object for threading.
    lock = threading.Lock()

    # Setup the kernel.
    kernel = threading.Thread(target=strip_color_pulse_single, daemon=True,
        args=[copy.deepcopy(data)],
        kwargs={'calling_type': 'single_pulse'})
    kernel.start()

    # Run the web server.
    app.run(host='0.0.0.0', debug=True)
