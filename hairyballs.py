import socket

serverMAC = 'CC:F9:E4:9B:77:A0'

port = 7

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMAC, port))

while True:
	text = input()
	if text == "quit":
		break
	s.send(bytes(text, 'UTF-8'))
s.close()
