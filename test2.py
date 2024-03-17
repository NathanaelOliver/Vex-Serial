
import socket

adapter_addr = 'CC:F9:E4:9B:77:A0'
port = 7  # Normal port for rfcomm?
buf_size = 1024

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((adapter_addr, port))
s.listen(1)
try:
    print('Listening for connection...')
    client, address = s.accept()
    print(f'Connected to {address}')

    while True:
        data = client.recv(buf_size).decode()
        if data:
            print(data)
            if (data == "break"):
                break
except Exception as e:
    print(f'Something went wrong: {e}')
    s.close()