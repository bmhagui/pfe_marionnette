#include <Herkulex.h>

#include <Herkulex.h>
#define PINstep 10
#define PINdir 8
const long int stepspermm = 800;
const int periode = 28;
long int stepperposition = 0;
byte header;
unsigned char positions[13] = {
  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0
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
  
  for (int i = 1; i < 13; i++)
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

  for (int i = 1; i < 13; i++)
  {
    Herkulex.writeRegistryRAM(i, 6, 80);
    delay(10);
    Herkulex.moveAllAngle(i, map(positions[i], 0, 255, -75, 75 ), LED_GREEN);
    delay(10);
  }
  Herkulex.actionAll(2500);
  delay(2000);
  for (int i = 1; i < 13; i++)
  {
    Herkulex.moveAllAngle(i, map(positions[i], 0, 255, -150, 150 ), LED_BLUE);
    delay(10);
  }
  Herkulex.actionAll(2500);
  delay(2000);
  // analogWrite(PINstep,0);


}

void loop()
{
  if (Serial.available())
  {
    header = Serial.read();
    while (header != 245)
    {
      while (!Serial.available());
      header = Serial.read();
    }
    for (int i = 1; i < 13; i++)
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
  for (int i = 1; i < 13; i++)
  {
    Herkulex.moveAllAngle(i, map(positions[i], 0, 255, -150, 150 ), LED_GREEN);
  }
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



