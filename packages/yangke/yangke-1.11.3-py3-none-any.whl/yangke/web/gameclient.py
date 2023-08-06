import socket


def connect_to_server(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8890))
    data = str(data)
    client.send(data.encode('utf-8'))
    receive_data = client.recv(1024)
    print('recv:', receive_data.decode())
    data = str(data) + 'again'
    client.send(data.encode('utf-8'))


for i in range(10):
    connect_to_server(str(i))
