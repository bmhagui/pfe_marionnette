#include <Herkulex.h>
int i;

void setup() {
  
  Serial.begin(115200); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
  Herkulex.begin(57600, 12, 11);
}
void loop() {
  if(Serial.available()){
    Serial.println("Serial available");  
    int i = Serial.read()-96; 
    Serial.print("Value read i = ");
    Serial.println(i);
    
    Herkulex.reboot(i);
    delay(500); 
    Herkulex.initialize();
    Herkulex.moveOne(i, random(0,1023), 2000, LED_BLUE); 
  } 
  delay(100); // delay for 1/10 of a second
}

