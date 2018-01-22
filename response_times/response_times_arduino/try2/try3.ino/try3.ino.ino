#include <Herkulex.h>

void setup() {
  //Serial.begin(9600); // set the baud rate
  Herkulex.begin(57600, 12, 11);
 //Herkulex.begin(115200, 12, 11);
  //Herkulex.reboot(1);
  Herkulex.initialize();
}
void loop() {
  Herkulex.moveOne(7, 500, 2500, LED_BLUE);
  /*char inByte = ' ';
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    //Herkulex.moveSpeedOne(1, atoi(inByte), int pTime, int iLed)
    
    //Herkulex.moveOne(1, 555, 2500, LED_GREEN);
    
    //Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  }
  //delay(100); // delay for 1/10 of a second*/
}
