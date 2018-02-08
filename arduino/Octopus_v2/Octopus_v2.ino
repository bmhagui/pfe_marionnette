
#include <Herkulex.h>
#define PINstep 10
#define PINdir 8
const long int stepspermm = 800;
const int periode = 28;
long int stepperposition = 0;
byte header;
unsigned char positions[15] = {
  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0
};
long int steps;
void setup()
{

  OCR1A = periode;
  TCCR1B = TCCR1B & 0b11111000 | 0x12;
  pinMode (PINdir, OUTPUT);
  //analogWrite(PINstep,0);
  Serial.begin(115200);    // Open serial communications
  Herkulex.begin(57600, 12, 11); //open serial port software
  
  for (int i = 1; i <= 13; i++)
  {
    Herkulex.reboot(i);
    delay(10);
  }
  delay(500);
  Herkulex.initialize(); //initialize motors

//  for (int i = 1; i < 13; i++)
//  {
//    Herkulex.setLed(i,LED_RED);
//    delay(500);
//  }

  for (int i = 1; i <= 13; i++)
  {
    delay(10);
    Herkulex.moveAllAngle(i, -100, LED_GREEN);
    delay(10);
    
  }
  Herkulex.actionAll(2500);
  delay(2000);

  for (int i = 1; i <= 13; i++)
  {
    delay(10);
    Herkulex.moveAllAngle(i, -150, LED_BLUE);
    delay(10);
    
  }
  Herkulex.actionAll(2500);
  delay(2000);      
  // analogWrite(PINstep,0);


}

void loop()
{
  //Last two values of the table positions are coordinates for the z axis and x axis respectively
  if (Serial.available())
  {
    header = Serial.read();
    while (header != 245)
    {
      while (!Serial.available());
      header = Serial.read();
    }
    for (int i = 1; i < 15; i++)
    {
      while (!Serial.available());
      positions[i] = Serial.read();
    }
  }
  //  steps=stepspermm*(positions[0]-stepperposition);
  //  if (steps>0)
  //  {
  //    digitalWrite(PINdir, LOW);
  //  }
  //  else
  //  {
  //    digitalWrite(PINdir, HIGH);
  //  }
  //Only going upto 130 for security measures and to avoid having the rail come off the motor.
  for (int i = 1; i < 13; i++)
  {
    Herkulex.moveAllAngle(i, map(positions[i], 0, 255, -150, 130 ), LED_GREEN);
  }
  //240 different angles to handle
  Herkulex.moveAllAngle(13, map(positions[13], 0, 255, -150, 130 ), LED_GREEN);
  //Serial.print( map(positions[13], 0, 600, -150, 90 ));
  Herkulex.actionAll(200);
  //  if (steps)
  //  {
  //    analogWrite(PINstep,periode>>1);
  //    for (long int i=1; i<abs(steps);i++)
  //    {
  //      delayMicroseconds(periode);
  //    }
  //  analogWrite(PINstep,0);
  //  }
  //  stepperposition+=(steps/stepspermm);
}
/*TODO:

motors 4 and 5 have same ID
Positions to "unsigned": inverted signs

*/



