#define PINstep 10
#define PINdir 9
const int periode = 70;
int i;

void setup()
{
  Serial.begin(9600);
  OCR1A = periode;
  TCCR1B = TCCR1B & 0b11111000 | 0x12;
  //TCCR1B = 0b00010001;
  pinMode (PINdir, OUTPUT);
  analogWrite(PINstep,0);
  


}

void loop()
{
  //while (Serial.available()<=0){}
  i = Serial.read();
  Serial.println(i);
  
    //steps=stepspermm*(positions[0]-stepperposition);
    //steps=stepspermm*(1-stepperposition);
    
    /*if (steps>0)
    {
      digitalWrite(PINdir, LOW);
    }
    else
    {
      digitalWrite(PINdir, HIGH);
    }*/

    /*if (i=51)
    {
      digitalWrite(PINdir, LOW);
      analogWrite(PINstep,1);
    }
    else if (i=49)
    {
      digitalWrite(PINdir, HIGH);
      analogWrite(PINstep,1);
    }
    else if (i=50)
    {
      analogWrite(PINstep,0);
    }*/

     digitalWrite(PINdir, LOW);
      analogWrite(PINstep,30);
      delay(1000);
      analogWrite(PINstep,0);
    
    /*if (steps)
    {
      analogWrite(PINstep,periode>>1);
      for (long int i=1; i<abs(steps);i++)
      {
        delayMicroseconds(periode);
      }
    analogWrite(PINstep,0);
    }
    stepperposition+=(steps/stepspermm);*/
}



