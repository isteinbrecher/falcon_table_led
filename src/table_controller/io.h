/**
 * Functionality to get IO over i2c
 */

#include <Wire.h>
#include <CRC8.h>


/**
 * \brief This function is called when a message is requested
 */
void requestEvents()
{
  // Calculate the checksum, this is the first value we send
  CRC8 crc;
  for (size_t i_data = 0; i_data < n_data; i_data++) crc.add(global_data[i_data]);
  Wire.write(crc.getCRC());

  // Send the data
  for (size_t i_data = 0; i_data < n_data; i_data++) Wire.write(global_data[i_data]);
}


/**
 * \brief This function is called when a message is received
 */
void receiveEvents(int n_bytes)
{
  if (n_bytes != n_data + 1)
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

    // Get the submitted bytes values
    uint32_t local_data[n_data];
    CRC8 crc;
    for (size_t i_data = 0; i_data < n_data; i_data++)
    {
      local_data[i_data] = Wire.read();
      crc.add(local_data[i_data]);
    }

    // Check the checksum
    const bool is_crc_ok = checksum == crc.getCRC();

    // If everything is ok, change the global data
    if (is_crc_ok)
      for (size_t i_data = 0; i_data < n_data; i_data++) global_data[i_data] = local_data[i_data];

    // Todo: Make better debug output
    if (is_crc_ok)
      Serial.print("Checksum ok");
    else
      Serial.print("Checksum WRONG");
    if (Wire.available()) Serial.print("Error, more bytes available");
  }
}
