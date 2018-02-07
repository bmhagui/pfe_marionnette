#include <Herkulex.h>
int i;
int n;

void setup() {
  Serial.begin(9600); // set the baud rate
  Herkulex.begin(57600, 12, 11);
  for (n=1;n<13;n++){
  Herkulex.reboot(n);
  //Herkulex.reboot(9);
  delay(10);
  }
  delay(500);
  Herkulex.initialize();
  delay(200);
  //Herkulex.moveAllAngle(9, -150, LED_BLUE);
  Herkulex.moveAllAngle(n, -150, LED_BLUE);
  Herkulex.actionAll(2500);
}
void loop() {
  while (Serial.available()<=0){}
  i = Serial.read();
  Serial.println(i);
  for (n=1;n<13;n++){
  Herkulex.moveAllAngle(n, 150, LED_GREEN);
  }
  Herkulex.actionAll(2500);
}
