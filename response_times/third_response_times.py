from time import sleep
import serial
ser = serial.Serial("/dev/ttyACM0", 9600) # Establish the connection on a specific port

ser.write("5")
print ser.readline() # Read the newest output from the Arduino
ser.close()
