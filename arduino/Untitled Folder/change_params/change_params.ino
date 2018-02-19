#include <Herkulex.h>

void setup()  
{
  Serial.begin(115200);    // Open serial communications
  Herkulex.beginSerial1(57600); //open serial port 1 
  Herkulex.reboot(6); //reboot first motor
  delay(500); 
  Herkulex.initialize(); //initialize motors
  delay(200);  
  Herkulex.clearError(6);
  //Herkulex.set_ID(253, 6);
  //Herkulex.writeRegistryRAM(6, 6, 0x51);
  //Herkulex.writeRegistryEEP(6, 4, 0x22);
  //Herkulex.reboot(6); 
}

void loop(){
  Herkulex.moveOne(6, random(0,1023), 2000, LED_BLUE);
  delay(2000);
}
