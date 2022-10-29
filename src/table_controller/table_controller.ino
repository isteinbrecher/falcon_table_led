#include <Wire.h>
# define I2C_SLAVE_ADDRESS 11 // 12 pour l'esclave 2 et ainsi de suite
//#define PAYLOAD_SIZE 2
void setup()
{
  Wire.begin(I2C_SLAVE_ADDRESS);
  Serial.begin(9600);
  Serial.println("-------------------------------------I am Slave1");
  delay(1000);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);
}
void loop() {}

int n = 10;
void requestEvents()
{
  Wire.write(61);
  Wire.write(62);
  Wire.write(63);
  Wire.write(64);
  Wire.write(65);
}
void receiveEvents(int numBytes)
{
  if (numBytes == 1) {
    Wire.read();
  }
  else
  {
    int i = 0;
    while (Wire.available()) {
      int data = Wire.read();
      if (i == 0) {}
      else if (i == 1 && data == 1)
      {}
      else if (i == 2 && data == 2)
      {}
      else if (i == 3 && data == 3)
      {}
      else if (i == 4 && data == 4)
      {}
      else if (i == 5 && data == 5)
      {}
      else {
        Serial.print("error i:");
        Serial.print(i);
        Serial.print(" = ");
        Serial.print(data);
        Serial.print("\n");
      }
      i++;
    }
  }
}
