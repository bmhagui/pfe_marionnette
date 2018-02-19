#define PINstep 10
#define PINdir 8
const long int stepspermm = 800;
const int periode = 200;
//long int steps;

    const int trigPin = 13;
    const int echoPin = 9;
    // defines variables
    long duration;
    int distance;

void setup()
{
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    Serial.begin(115200); // Starts the serial communication
  
  OCR1A = periode;
  TCCR1B = TCCR1B & 0b11111000 | 0x12;
  pinMode (PINdir, OUTPUT);
  analogWrite(PINstep,0);

}

void loop()
{

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance= duration*0.034/2;
    // Prints the distance on the Serial Monitor
    Serial.print("Distance: ");
    Serial.println(distance);

/*if (distance<20){
  digitalWrite(PINdir, HIGH);
      analogWrite(PINstep,2);
  }
  else{
    analogWrite(PINstep,0);
    }*/


  if (distance == 10 || distance == 10+1 || distance == 10-1)
  {
    analogWrite(PINstep,0);
  }
  else if (distance > 10)
  {
    digitalWrite(PINdir, HIGH);
    analogWrite(PINstep,2);
  }
  else if (distance < 10)
  {
    digitalWrite(PINdir, LOW);
    analogWrite(PINstep,2);
  }
  
}



