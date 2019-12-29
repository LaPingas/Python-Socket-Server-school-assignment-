from socket_usage import *
from io import BytesIO
import sys


def main():
    client_socket = Client_Socket('127.0.0.1', 1729)
    client_socket.connect()
    command = ""
    while command != "exit":
        command = input("Enter a command: ")
        client_socket.send(command)
        if not command.startswith("send"):
            print(client_socket.receive())
            if command == "close_server":
                sys.exit()
        else:
            byte = client_socket.receive('b')
            if byte == b'done':
                print("File doesn't exist")
            else:
                with open(command[command.rfind('\\') + 1:], 'wb') as result:
                    while byte != b'done':
                        result.write(byte)
                        byte = client_socket.receive('b')


if __name__ == "__main__":
    main()