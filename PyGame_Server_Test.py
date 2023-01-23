#Imports
import socket

#Server
HOST = "127.0.0.1"
PORT = 49637
Server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server.bind((HOST, PORT))
print("Server setup complete")

#Variables
PlayerAmount = 0
running = True
Player1Name = ""
Player1Addr = ""
Player2Name = ""
Player2Addr = ""

#Netcode
print("Server started")
while running:
    LatestRecievedData, Client_Address = Server.recvfrom(1024)
    LatestRecievedDataStr = str(LatestRecievedData, 'utf-8')
    if LatestRecievedDataStr == "AttemptJoin":
        if PlayerAmount == 0:
            Player1Addr = Client_Address
            DataToSend = "IsP1"
            Server.sendto(DataToSend.encode(), Player1Addr)
            print("Player 1 joined server")
            print("Player 1 address:")
            print(Player1Addr)
            PlayerAmount = 1

        elif PlayerAmount == 1:
            Player2Addr = Client_Address
            DataToSend = "IsP2"
            Server.sendto(DataToSend.encode(), Player2Addr)
            print("Player 2 joined server")
            print("Player 2 address:")
            print(Player2Addr)
            PlayerAmount = 2

        elif PlayerAmount == 2:
            DataToSend = "ServerFull"
            Server.sendto(DataToSend.encode(), Client_Address)
            print("Client attempted to join while server was full")
    
    elif LatestRecievedDataStr == "Shutdown":
        if PlayerAmount == 0:
            print("Recieved shutdown order; shutting down server")
            running = False
        
        elif PlayerAmount == 1:
            print("Recieved shutdown order; shutting down server")
            DataToSend = "ServerShutdown"
            Server.sendto(DataToSend.encode(), Player1Addr)
            print("Told player 1 server is shutting down")
            running = False

        elif PlayerAmount == 2:
            print("Recieved shutdown order; shutting down server")
            DataToSend = "ServerShutdown"
            Server.sendto(DataToSend.encode(), Player1Addr)
            print("Told player 1 server is shutting down")
            Server.sendto(DataToSend.encode(), Player2Addr)
            print("Told player 2 server is shutting down")
            running = False
    
    elif LatestRecievedDataStr == "P1Disconnect":
        if PlayerAmount == 2:
            DataToSend = "Player1DC"
            Server.sendto(DataToSend.encode(), Player2Addr)
            Player1Addr = ""
            Player2Addr = ""
            PlayerAmount = 0
            print("Player 1 Disconnected; also kicked player 2")

    elif LatestRecievedDataStr == "P2Disconnect":
        if PlayerAmount == 2:
            DataToSend = "Player2DC"
            Server.sendto(DataToSend.encode(), Player1Addr)
            Player1Addr = ""
            Player2Addr = ""
            PlayerAmount = 0
            print("Player 2 Disconnected; also kicked player 1")

print("Server stopped")