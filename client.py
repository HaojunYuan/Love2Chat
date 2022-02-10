import socket
import threading
import sys
import argparse
from socket import AF_INET, SOCK_STREAM
import time

exit = False
# TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents


def receive(clientSocket,):

    while True:
        if exit:
            clientSocket.close()
            break
        else:
            message = clientSocket.recv(1024).decode()  # listen for messages
            print(message)
            sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', action="store_true")
    parser.add_argument('-host', type=str)
    parser.add_argument('-port', type=int)
    parser.add_argument('-username', type=str)
    parser.add_argument('-passcode', type=str)
    args = parser.parse_args()

    serverName = args.host
    serverPort = args.port
    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # Login
    passcode = args.passcode
    clientSocket.send(passcode.encode())
    login = clientSocket.recv(1024).decode()
    if login == "success":
        clientSocket.send(args.username.encode())
        print("Connected to "+serverName+" on port "+str(serverPort))
        sys.stdout.flush()
        while True:
            listen = threading.Thread(
                target=receive, args=(clientSocket,))  # listen from server
            listen.start()

            words = input()  # input
            if words == ":Exit":
                clientSocket.send(words.encode())
                exit = True
                # clientSocket.close()
                # listen.terminate()
                break
            elif words == ":mytime":
                t = time.localtime()
                current_time = time.asctime(t)
                clientSocket.send(current_time.encode())
            elif words == ":+1hr":
                t = time.time()
                t = t+3600
                s = time.localtime(t)
                current_time = time.asctime(s)
                clientSocket.send(current_time.encode())
            else:
                clientSocket.send(words.encode())

    else:
        print("Incorrect passcode")
        sys.stdout.flush()
