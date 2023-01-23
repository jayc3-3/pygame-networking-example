#This module sends a message to a server to initiate a shutdown
import socket

HOST = "127.0.0.1"
PORT = 49637

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Client:
    Client.connect((HOST, PORT))
    ShutDownMSG = "Shutdown"
    Client.sendto(ShutDownMSG.encode(), (HOST, PORT))
    print("Server shutdown order sent")