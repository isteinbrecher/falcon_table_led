#include <CRC8.h>
#include <NeoPixelBrightnessBus.h>


// For i2c
#include <Wire.h>


#define I2C_SLAVE_ADDRESS 11


const unsigned int pin_strip = 3;

// led strip constants
const unsigned int led_strip_num_pixels = 10;


using LedStrip = NeoPixelBrightnessBus<NeoGrbFeature, Neo800KbpsMethod>;
LedStrip led_strip(led_strip_num_pixels, pin_strip);


CRC8 crc;

uint32_t color[3] = {0, 10, 0};

void setup()
{
  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onReceive(receiveEvents);

  Serial.begin(9600);

  // start the led strip
  led_strip.Begin();
  led_strip.Show();



  // Perform a CRC check
  crc.add(1);
  crc.add(23);
  crc.add(8);
  crc.add(254);
  crc.add(0);
  crc.add(124);

  Serial.print(crc.getCRC());
}

void loop()
{
  for (unsigned int i = 0; i < led_strip_num_pixels; i++)
  {
    led_strip.SetPixelColor(i, RgbColor(color[0], color[1], color[2]));
  }
  led_strip.Show();

  delay(100);
}

void receiveEvents(int n_bytes)
{
  if (n_bytes != 4)
  {
    // We expect exactly 4 bytes, everything else indicates an error, i.e., do nothing and empty the
    // read stack
    while (Wire.available())
    {
      Wire.read();
    }
  }
  else
  {
    // The first byte is the checksum
    const uint32_t checksum = Wire.read();

    // Get the color values
    uint32_t r = Wire.read();
    uint32_t g = Wire.read();
    uint32_t b = Wire.read();

    // Check the checksum
    CRC8 crc;
    crc.add(r);
    crc.add(g);
    crc.add(b);
    const bool is_crc_ok = checksum == crc.getCRC();

    if (is_crc_ok)
    {
      color[0] = r;
      color[1] = g;
      color[2] = b;
    }

    if (is_crc_ok)
      Serial.print("Checksum ok");
    else
      Serial.print("Checksum WRONG");

    if (Wire.available()) Serial.print("Error, more bytes available");
  }
}
