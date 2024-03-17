#!/usr/bin/env python
import time
import serial
import socket

serverMACAddress = '98:5F:D3:3E:54:44'
port = 4
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))

ser = serial.Serial(
	port = '/dev/ttyACM0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while 1:
	x = ser.readline()
	s.send(x)
s.close()