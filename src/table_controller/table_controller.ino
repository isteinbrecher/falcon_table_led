
#include <NeoPixelBrightnessBus.h>


// Global data that is exchanged via IO
constexpr size_t n_data = 3;
uint32_t global_data[n_data] = {};

// This include has to be defined after the data variables are initialized
#include "io.h"



#define I2C_SLAVE_ADDRESS 11



// led strip constants
const unsigned int pin_strip = 3;
const unsigned int led_strip_num_pixels = 10;


using LedStrip = NeoPixelBrightnessBus<NeoGrbFeature, Neo800KbpsMethod>;
LedStrip led_strip(led_strip_num_pixels, pin_strip);



void setup()
{
  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);

  Serial.begin(9600);

  // start the led strip
  led_strip.Begin();
  led_strip.Show();
}

void loop()
{
  for (unsigned int i = 0; i < led_strip_num_pixels; i++)
  {
    led_strip.SetPixelColor(i, RgbColor(global_data[0], global_data[1], global_data[2]));
  }
  led_strip.Show();

  delay(100);
}
