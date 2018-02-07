#include <Herkulex.h>
unsigned long time;
int positions[13];

void setup() {
  
  Serial.begin(9600); // set the baud rate
  Herkulex.begin(57600, 12, 11);
  
  for (int n = 0; n < 13; n++)
  {
    Herkulex.reboot(n+1);
    delay(10);
  }
  delay(500);
  Herkulex.initialize();

    for (int n=0; n<13; n++){
    positions[n]=random(-160,160);
    //Serial.println(positions[n]);
  }

while (Serial.available() <= 0){}

      for (int n=0; n<13; n++){
      Serial.println("Sending");
      time = millis();
      Serial.println(time);
      //delay(10);
      Herkulex.moveAllAngle(n+1, positions[n], LED_GREEN);
      //delay(10);
      time = millis();
      Serial.println(time);      
      Serial.print("Command sent to motor ");
      Serial.println(n+1);
    }
    Serial.println("Action all");
    time = millis();
    Serial.println(time);
    
    Herkulex.actionAll(2000);
    //delay(2000);
    
    Serial.println("Action all done");
    time = millis();
    Serial.println(time);

}
  

void loop() {
  

}

