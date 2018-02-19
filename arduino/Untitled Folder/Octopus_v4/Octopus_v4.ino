
#include <Herkulex.h>
#define PINstep 10
#define PINdir 8
//With the current settings the stepper motor has a pwm with a 20kHz signal and 40% duty cycle
const int periode = 50;
byte header;
unsigned char positions[15] = {
  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0
};

const int trigPin = 13;
const int echoPin = 9;
// defines variables
long duration;
int distance;

void setup()
{
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  OCR1A = periode;
  TCCR1B = TCCR1B & 0b11111000 | 0x12;
  pinMode (PINdir, OUTPUT);
  analogWrite(PINstep,0);
  Serial.begin(115200);    // Open serial communications
  Herkulex.begin(57600, 12, 11); //open serial port software
  
  for (int i = 1; i <= 13; i++)
  {
    Herkulex.reboot(i);
    delay(10);
  }
  delay(500);
  Herkulex.initialize(); //initialize motors


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
  //Only going upto 130 for security measures and to avoid having the rail come off the motor.
  for (int i = 1; i < 13; i++)
  {
    Herkulex.moveAllAngle(i, map(positions[i], 0, 255, -150, 130 ), LED_GREEN);
  }
  Herkulex.moveAllAngle(13, map(positions[13], 0, 255, -150, 130 ), LED_GREEN);
  Herkulex.actionAll(200);


  //Serial.println(positions[14]);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  Serial.println(distance);
  Serial.println(duration);

  //The first three conditions are for security, making sure that the platform is not at its maximum positions and that the user's hand is in range of the LeapMotion
  //The other three are to detect that the platform is in the right position with a margin of error of 1 cm
  
  if (distance >= 25 || distance <= 5 || positions[14]==0 || distance == positions[14] || distance == positions[14]+1 || distance == positions[14]-1)
  {
    analogWrite(PINstep,0);
  }
  else if (distance > positions[14] && distance > 4)
  {
    if (distance-positions[14] >= 4)
    {
      OCR1A = 50;
    }
    else
    {
      OCR1A = 70;
    }
    digitalWrite(PINdir, HIGH);
    analogWrite(PINstep,30);
  }
  else if (distance < positions[14] && distance < 25)
  {
    if (positions[14]-distance >= 4)
    {
      OCR1A = 50;
    }
    else
    {
      OCR1A = 70;
    }
    digitalWrite(PINdir, LOW);
    analogWrite(PINstep,30);
  }

}
