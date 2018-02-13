#include <Herkulex.h>
unsigned long time;
int positions[13] = {100,200,300,400,500,600,700,800,900,1000,650,750,850};

void setup() {
  
  Serial.begin(115200); // set the baud rate
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
    
    char inByte = Serial.read();
    
    int i = atoi(&inByte);
    Serial.print("Value read i = ");
    Serial.println(i);
    time = millis();
    Serial.println(time);
    
    
    Herkulex.moveOne(i, 1000, 2000, LED_BLUE);
    Serial.println("Command sent to motor");
    time = millis();
    Serial.println(time);  
  }
  
  //delay(100); // delay for 1/10 of a second
}

