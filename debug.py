import socket
import serial
import time
import os
import subprocess
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

def upload_code():
	build_process = subprocess.Popen("pros build", shell=True)
	build_process.wait()

	upload_process = subprocess.Popen("pros upload", shell=True)
	upload_process.wait()


upload_code()
ser = serial.Serial('/dev/ttyACM1', 9600)
if ser.isOpen():
	ser.close()
ser.open()
ser.isOpen()

count = 0;

data = ser.readline().decode()

while True:
	
	

	print("data/data" + str(count) + ".jpg")
	ret, frame = cap.read()
	cv2.imwrite("data/data" + str(count) + ".jpg", frame)
	count += 1
	time.sleep(0.5)
	

ser.close()
cap.release()
cv2.destroyAllWindows()
