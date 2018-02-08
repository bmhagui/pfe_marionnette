#include <Herkulex.h>
unsigned long time;
int positions[13];

void setup() {
  
  Serial.begin(9600); // set the baud rate
  Herkulex.begin(57600, 12, 11);
  Herkulex.initialize();
  
  for (int n=0; n<13; n++){
    positions[n]=random(0,1023);
  }
}
void loop() {
  if (Serial.available() > 0){
    
    Serial.read();
    
    for (int n=0; n<13; n++){
      Serial.println("Sending");
      time = millis();
      Serial.println(time);
      Herkulex.moveOne(n+1, positions[n], 2000, LED_BLUE);
      time = millis();
      Serial.println(time);      
      Serial.print("Command sent to motor ");
      Serial.println(n+1);
    }
    
  }
  
}

