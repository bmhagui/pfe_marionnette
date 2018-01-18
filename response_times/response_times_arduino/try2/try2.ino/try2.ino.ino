#include <Herkulex.h>
//int i =3;
int incomingByte = 0;

void setup() {
  Serial.begin(9600); // set the baud rate
  Herkulex.begin(57600, 12, 11);
  
  for (int i = 1; i < 253; i++)
  {
    Herkulex.reboot(i);
    delay(10);
  }
  delay(500);
  Herkulex.initialize();
  delay(200);  
}
void loop() {
  //Herkulex.moveSpeedOne(1, 200, 2000, LED_GREEN);
  
  //delay(1200);
  /* if (Serial.available() > 0) {
    incomingByte = Serial.read(); // read the incoming byte:
    Serial.print(" I received:");
    Serial.println(incomingByte-54);
    Herkulex.moveSpeedOne(incomingByte-54, 100, 2000, LED_BLUE);
    }*/
Herkulex.moveSpeedOne(13, 100, 2000, LED_BLUE);
  for (int i = 1; i < 253; i++)
  {
    //Herkulex.moveOne(i, 1023, 2500, LED_GREEN);
    //Herkulex.moveSpeedOne(i, 100, 2000, LED_BLUE);
    Serial.println(i);
    delay(500);
  }
    

  /*char inByte = ' ';
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    //Herkulex.moveSpeedOne(1, atoi(inByte), int pTime, int iLed)
    
    //Herkulex.moveOne(1, 555, 2500, LED_GREEN);
    
    //Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  }
  //delay(100); // delay for 1/10 of a second*/
}
