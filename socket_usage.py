import socket

class Client_Socket():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket()


    def connect(self):
        self.client_socket.connect((self.ip, self.port))


    def disconnect(self):
        self.client_socket.close()


    def send(self, message, mode='s'):
        if mode == 's':
            self.client_socket.send(message.encode())
        else:
            self.client_socket.send(message)


    def receive(self, mode='s', bufsize=1024):
        received = self.client_socket.recv(bufsize)
        if mode == 's':
            return received.decode()
        else:
            return received


class Server_Socket():
    def __init__(self, port, ip_range='0.0.0.0'):
        self.ip_range = ip_range
        self.port = port
        self.server_socket = socket.socket()
        self.client_socket = None


    def bind(self):
        self.server_socket.bind((self.ip_range, self.port))


    def listen(self, clients=1):
        self.server_socket.listen(clients)


    def accept(self):
        client = self.server_socket.accept()
        self.client_socket = client[0]
        return client


    def send(self, message, mode='s'):
        if mode == 's':
            self.client_socket.send(message.encode())
        else:
            self.client_socket.send(message)


    def receive(self, mode='s', bufsize=1024):
        received = self.client_socket.recv(bufsize)
        if mode == 's':
            return received.decode()
        else:
            return received


    def close_client(self):
        self.client_socket.close()


    def close_server(self):
        self.server_socket.close()