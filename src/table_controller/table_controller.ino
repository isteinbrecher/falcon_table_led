

// Setup data for the LED strip
#include <NeoPixelBrightnessBus.h>
constexpr size_t pin_strip = 3;
constexpr size_t led_strip_num_pixels = 10;
using LedStrip = NeoPixelBrightnessBus<NeoGrbFeature, Neo800KbpsMethod>;
LedStrip led_strip(led_strip_num_pixels, pin_strip);


// Global data that is exchanged via IO
constexpr size_t n_data = 5;
uint8_t global_data[n_data] = {0, 0, 0, 0, 0};
bool global_data_updated = true;

// This include has to be defined after the data variables are initialized
#include "io.h"


// Get the active mode
inline uint8_t get_global_mode() { return global_data[3]; }

// Get the overall brightness
inline uint8_t get_global_brightness() { return global_data[4]; }

// Get the global color value
inline RgbColor get_global_color() { return {global_data[0], global_data[1], global_data[2]}; }


// Other global variables
constexpr int min_delay = 10;

/**
 * \brief Turn of the strip
 */
void strip_off()
{
  const uint8_t my_mode = get_global_mode();

  while (true)
  {
    if (global_data_updated)
    {
      if (my_mode != get_global_mode()) return;
    }
  }
}

/**
 * \brief Display the strip with a constant color
 */
void constant_color_mode()
{
  const uint8_t my_mode = get_global_mode();

  while (true)
  {
    if (global_data_updated)
    {
      if (my_mode != get_global_mode()) return;

      // The strip has to be redrawn, also set the brightness since that could have also changed
      led_strip.SetBrightness(get_global_brightness());
      for (size_t i = 0; i < led_strip.PixelCount(); i++)
      {
        led_strip.SetPixelColor(i, get_global_color());
      }
      led_strip.Show();

      global_data_updated = false;
    }
  }
}

/**
 * \brief Setup and initialise variables
 */
void setup()
{
  // Todo
  Serial.begin(9600);

  // Set up the i2c device
  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);

  // Start the led strip
  led_strip.Begin();
  led_strip.Show();
}

/**
 * \brief Main execution loop
 */
void loop()
{
  switch (get_global_mode())
  {
    case 0:
    {
      strip_off();
      break;
    }
    case 1:
    {
      constant_color_mode();
      break;
    }
  }
}