#include <Herkulex.h>

void setup() {
  // put your setup code here, to run once:
  Herkulex.begin(57600, 12, 11); //open serial port software
  Herkulex.reboot(1); //reboot first motor
  Herkulex.reboot(2); //reboot second motor
  Herkulex.reboot(3);
  Herkulex.reboot(4);
  Herkulex.reboot(5);
  Herkulex.reboot(6);
  Herkulex.reboot(7);
  Herkulex.reboot(8);
  Herkulex.reboot(9);
  Herkulex.reboot(10);
  Herkulex.reboot(11);
  Herkulex.reboot(12);
  Herkulex.reboot(13);
  delay(500); 
  Herkulex.initialize();
  //Herkulex.moveAllAngle(1, 125.0, LED_GREEN);
  Herkulex.moveAllAngle(1, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(2, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(3, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(4, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(5, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(6, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(7, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(8, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(9, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(10, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(11, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(12, random(-160,160), LED_GREEN);
  Herkulex.moveAllAngle(13, random(-160,160), LED_GREEN);
  Herkulex.actionAll(2500);
}

void loop() {
  // put your main code here, to run repeatedly:

}
