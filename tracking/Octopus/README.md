# Additions for Z and X axis movements

This document briefly explains what was added to the code to allow the Octupus to move on the Z and X axes. 

## palmPosition 

palmPositions is the variable in the file server.py that contains the distance between the center of the LeapMotion and the hand on the three axes x,y and z. We only need X and Z for now so we take these two values into another variable, projections[10]. If this variable is not empty it is copied to the output vector and sent.

## controller.py

This file is the client that receives the output vector mentionned earlier and is where the information is going to be treated, sent to the simulation on Sofa and then sent to the Arduino to activate the motors necessary. 

## Z-axis

The distance between the LeapMotion and the hand is expressed in millimeters. The code below does the followig; from 0 to 150mm we consider that the user wants the lowest position of the Octupus (so that they would have enough space to fold their fingers), starting at 400mm and onwards the highest position is chosen and otherwise an intermediate heigh is chosen. An exponential filter is used to avoid having huge changes to the values sent to the motors. 

```
global interZ
global lastValueZ
if vectors[10][1] <= 150:
    interZ = 0
elif vectors[10][1] >= 400:
    interZ = 250
else:
    interZ = vectors[10][1]-150
outputVector[12] = lastValueZ * (1-alpha) + interZ * alpha
lastValueZ = outputVector[12]
```

The value added of ouputVector[12] is then added to the other motors to allow the Octupus to be lifted to dropped and keep its simulated shape, to a certain limit of course. 

```
for i in range(0,12):
    if outputVector[i] < 0:
        outputVector[i] = 0
    outputVector[i] = 255/116*outputVector[i]
    #adding an offset to compensate for lifting the robot
    outputVector[i] += (outputVector[12])
    if outputVector[i] > 250:
        outputVector[i] = 250
```
## X-axis

We only have 18cm to play with when it comes to the X-axis so we limited the measurements to -200 and 200. When the value respects our condition, it will be mapped between the values 4 and 22cm which are our minimum and maximum respectively. 

```
if vectors[10][0] > -200 and vectors[10][0] < 200:
    outputVector[13] = (vectors[10][0]+200)*18/400+4
elif vectors[10][0] < -200:
    outputVector[13] = 4
else:
    outputVector[13] = 22
```
## Arduino

The Arduino gets a table of values through the serial that it then treats to move each of the 13 servo motors connected to it. There is also an Ultrasound sensor to measure the distance between it and and the motor plate. This distance is used to activate the stepper motor for the X-axis movement, the speed of the motor is proportional to the difference between the desired position and the current position of the plate.

