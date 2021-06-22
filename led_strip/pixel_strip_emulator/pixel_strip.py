# -*- coding: utf-8 -*-
"""
The main script to run the led strip controls.
"""

# Import python modules.
import os
import pyglet


class PixelStrip(pyglet.window.Window):
    """
    Emulator for a pixel strip.
    """

    # How the individual LEDs are placed.
    led_placement = [
        {'n_led': 60, 'direction': 'east', 'position': [1, 0]},
        {'n_led': 40, 'direction': 'south', 'position': [61, 1]},
        {'n_led': 60, 'direction': 'west', 'position': [60, 41]},
        {'n_led': 40, 'direction': 'north', 'position': [0, 40]}
        ]

    def __init__(self, n_led, window_w=1130, window_h=730):
        """
        Initialize the strip.
        """

        super().__init__(width=window_w, height=window_h)
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.color_sprites = []
        self.led_group = pyglet.graphics.OrderedGroup(0)
        self.color_group = pyglet.graphics.OrderedGroup(1)
        self.alive = 1
        self.n_led = n_led

    def begin(self):
        """
        Initialize the graphics.
        """

        def get_pixel_pos(i_x, i_y):
            """
            Convert a LED position to the pixel position.
            """
            x = i_x * 18
            y = self.height - 17 - i_y * 17
            return x, y

        # Load the images.
        my_dir = os.path.dirname(__file__)
        img_ws2812 = pyglet.image.load(os.path.join(my_dir, 'ws2812b.png'))
        img_circle = pyglet.image.load(os.path.join(my_dir, 'circle.png'))

        # Initialize the led strips.
        for led_strip in self.led_placement:
            position = led_strip['position']
            for i_led in range(led_strip['n_led']):

                if led_strip['direction'] == 'east':
                    x, y = get_pixel_pos(position[0] + i_led, position[1])
                elif led_strip['direction'] == 'south':
                    x, y = get_pixel_pos(position[0], position[1] + i_led)
                elif led_strip['direction'] == 'west':
                    x, y = get_pixel_pos(position[0] - i_led, position[1])
                elif led_strip['direction'] == 'north':
                    x, y = get_pixel_pos(position[0], position[1] - i_led)
                else:
                    raise ValueError('Wrong direction')

                self.sprites.append(
                    pyglet.sprite.Sprite(
                        img=img_ws2812,
                        batch=self.batch,
                        group=self.led_group,
                        x=x, y=y))
                self.color_sprites.append(
                    pyglet.sprite.Sprite(
                        img=img_circle,
                        batch=self.batch,
                        group=self.color_group,
                        x=x, y=y - 5))
                self.sprites[-1].scale = 0.05
                self.color_sprites[-1].color = (0, 0, 0)
                self.color_sprites[-1].scale = 0.5

        # Safety checks.
        if ((not self.n_led == len(self.sprites))
                or (not self.n_led == len(self.sprites))):
            raise ValueError('Number of LEDs does not match.')

        # We have to call render twice here.
        for _ in range(2):
            self.render()

    def numPixels(self):
        return self.n_led

    def setPixelColor(self, i, color):
        """Set a single color of the strip."""
        blue = color & 255
        color = color >> 8
        green = color & 255
        color = color >> 8
        red = color & 255
        self.color_sprites[i].color = (red, green, blue)

    def show(self):
        """Display the current state of the strip."""
        self.render()

    def render(self):
        """Render the pyglet window."""
        self.clear()
        self.batch.draw()
        self.dispatch_events()
        self.flip()
