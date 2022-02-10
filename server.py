import socket
import string
import threading
import sys
import argparse
from socket import AF_INET, SOCK_STREAM
import time
import multiprocessing

# TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents


def receive(username, connectionSocket, address):

    while True:
        receive = connectionSocket.recv(1024).decode()
        if receive == ":Exit":
            exitMessage = username+" left the chatroom"
            print(exitMessage)
            sys.stdout.flush()
            for key in connectionDict:  # Send received message to other clients
                if connectionDict[key] != connectionSocket:
                    connectionDict[key].send(exitMessage.encode())
            connectionSocket.close()
            break
        elif receive == ":)":
            message = username+": [feeling happy]"
        elif receive == ":(":
            message = username+": [feeling sad]"
        else:
            message = username+': '+receive

        print(message)
        sys.stdout.flush()
        for key in connectionDict:  # Send received message to other clients
            if connectionDict[key] != connectionSocket:
                connectionDict[key].send(message.encode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-start', action="store_true")
    parser.add_argument('-port', type=int)
    parser.add_argument('-passcode', type=str)
    args = parser.parse_args()

    serverPort = args.port
    serverSocket = socket.socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('Server started on port ' + str(args.port)+'. Accepting connections')
    sys.stdout.flush()
    connectionDict = {}
    id = 0
    while True:
        connectionSocket, addr = serverSocket.accept()
        connectionDict[id] = connectionSocket
        id = id+1
        # Login
        passcode = connectionSocket.recv(1024).decode()
        if passcode == args.passcode:
            login = "success"
        else:
            login = "fail"
        connectionSocket.send(login.encode())

        if login == "success":
            username = connectionSocket.recv(1024).decode()
            join = username+" joined the chatroom"
            print(join)
            sys.stdout.flush()
            for key in connectionDict:  # Send join message to other clients
                if connectionDict[key] != connectionSocket:
                    connectionDict[key].send(join.encode())
            chat = threading.Thread(
                target=receive, args=(username, connectionSocket, addr))
            chat.start()

        # connectionSocket.close()
