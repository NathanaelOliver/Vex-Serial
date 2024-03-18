import socket
import serial
import time
import os
import subprocess


def upload_code():
	build_process = subprocess.Popen("pros build", shell=True)
	build_process.wait()

	upload_process = subprocess.Popen("pros upload", shell=True)
	upload_process.wait()



ser = serial.Serial('/dev/ttyACM1', 9600)
if ser.isOpen():
	ser.close()
ser.open()
ser.isOpen()

port = 7


while True:
	data = ser.readline().decode()
	
	print(data)
	if data == "quit":
		break

ser.close()
