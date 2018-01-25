from time import sleep
import serial
ser = serial.Serial("/dev/ttyACM1", 9600) # Establish the connection on a specific port


sleep(2)
ser.write("1")

f = open('log.txt','w')
while True:
	f.write(ser.readline()) # Read the newest output from the Arduino
ser.close()
f.close()
