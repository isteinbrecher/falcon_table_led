#include <CRC8.h>
#include <NeoPixelBrightnessBus.h>


const unsigned int pin_strip = 3;
const unsigned int n_buttons = 3;
const unsigned int pin_button_bottom = 12;
const unsigned int pin_button_middle = 9;
const unsigned int pin_button_top = 2;

// led strip constants
const unsigned int led_strip_num_pixels = 10;


using LedStrip = NeoPixelBrightnessBus<NeoRgbFeature, Neo800KbpsMethod>;
LedStrip led_strip(led_strip_num_pixels, pin_strip);

void setup()
{
  Serial.begin(9600);

  // start the led strip
  led_strip.Begin();
  led_strip.Show();

  for (unsigned int i = 0; i < led_strip_num_pixels; i++)
  {
    led_strip.SetPixelColor(i, RgbColor(10, 10, 10));
  }
  led_strip.Show();


  // Perform a CRC check
  CRC8 crc;
  crc.add(1);
  crc.add(23);
  crc.add(8);
  crc.add(254);
  crc.add(0);
  crc.add(124);

  Serial.print(crc.getCRC());
}

void loop() {}