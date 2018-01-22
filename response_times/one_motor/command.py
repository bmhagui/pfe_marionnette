from time import sleep
import serial
ser = serial.Serial("/dev/ttyACM0", 9600) # Establish the connection on a specific port
f = open('log.txt','w')

ser.write("7")
sleep(1)
ser.write("4")

while True:
	f.write(ser.readline()) # Read the newest output from the Arduino
ser.close()
f.close()
