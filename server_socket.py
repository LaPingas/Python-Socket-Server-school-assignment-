import random, shutil, glob, os, datetime, subprocess, socket, sys, time
from PIL import ImageGrab
from socket import *
from socket_usage import *


def main():
    server_socket = Server_Socket(1729)
    server_socket.bind()
    while True:
        server_socket.listen()
        accept = server_socket.accept()
        command = ""
        while command != "exit":
            command = server_socket.receive()
            if command == "screenshot":
                screenshot = ImageGrab.grab()
                screenshot.save(f"{os.getcwd()}\\screenshot.jpg")

            elif command.startswith("send"):
                if os.path.exists(command[5:]):
                    with open(command[5:], "rb") as file:
                        data = file.read()
                        i = 0
                        while i < len(data) - len(data) % 1024:
                            server_socket.send(data[i:i+1024], 'b')
                            i += 1024
                        server_socket.send(data[i:len(data)], 'b')
                        time.sleep(0.1)
                        server_socket.send("done", 's')
                else:
                    server_socket.send("done", 's')

            elif command.startswith("dir"):
                directory = command[4:] + '\\*.*'
                server_socket.send(f"{glob.glob(directory)}")

            elif command.startswith("delete"):
                try:
                    os.remove(command[7:])
                    server_socket.send("File deleted successfully")
                except:
                    server_socket.send("File doesn't exist")

            elif command.startswith("copy"):
                try:
                    src, dst = command[5:].split("|")
                    shutil.copy(src, dst)
                    server_socket.send("File copied successfully")
                except:
                    server_socket.send("File/directory doesn't exist")

            elif command.startswith("execute"):
                try:
                    subprocess.call(command[8:])
                    server_socket.send("Process executed successfully")
                except:
                    server_socket.send("Process doesn't exist")

            elif command == "exit":
                server_socket.send("Exiting...")
                server_socket.close_client()

            elif command == "close_server":
                server_socket.send("Exiting...")
                server_socket.close_server()
                sys.exit()

            else:
                server_socket.send("Command not recognized")


if __name__ == "__main__":
    main()