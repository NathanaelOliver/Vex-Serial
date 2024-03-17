#python -m serial.tools.miniterm

import serial
import time

j=0
i = 0
ser = serial.Serial('/dev/ttyACM1', 9600)

if ser.isOpen():
	ser.close()
ser.open()
ser.isOpen()
#while j < 100:
ser.write("CreamyCocks \r".encode())

#j+=1
print("after While")

while True:
	print("In While")
	ser.write("1 \r".encode())
	print("after while")
	
	data = ser.readLine()
	print(data)
	
ser.close()
