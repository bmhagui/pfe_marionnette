import serial

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

port.write("5")

port.close()
