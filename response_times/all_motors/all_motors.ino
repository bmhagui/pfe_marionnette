#include <Herkulex.h>
unsigned long time;

int positions[13] = {0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0};

void setup() {
  
  Serial.begin(50200); // set the baud rate
  //Serial.println("Ready"); // print "Ready" once
  Herkulex.begin(57600, 12, 11);
  Herkulex.initialize();

}
void loop() {

  char inByte = ' ';
  if(Serial.available()){
    Serial.println("Serial available");
    time = millis();
    Serial.println(time);
    
    char inByte = Serial.read(); // read the incoming data
    int i = atoi(&inByte);
    Serial.print("Value read i = ");
    Serial.println(i);
    time = millis();
    Serial.println(time);
    
    
    Herkulex.moveOne(i, 500, 2000, LED_BLUE);
    Serial.println("Command sent to motor");
    time = millis();
    Serial.println(time);  
  }
  
  //delay(100); // delay for 1/10 of a second
}
