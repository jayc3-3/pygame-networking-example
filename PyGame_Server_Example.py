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
P1X = False
P1Y = False
P2X = False
P2Y = False
Player1X = 50
Player1Y = 50
Player2X = 200
Player2Y = 200
Player1Addr = ""
Player2Addr = ""

#Netcode
print("Server started")
while running:
    LatestRecievedData, Client_Address = Server.recvfrom(1024)
    LatestRecievedDataStr = str(LatestRecievedData, 'utf-8')    
    
    if LatestRecievedDataStr == "Player1Left":
        Player1X -= 5
    
    if LatestRecievedDataStr == "Player1Right":
        Player1X += 5
        
    if LatestRecievedDataStr == "Player1Up":
        Player1Y -= 5
        
    if LatestRecievedDataStr == "Player1Down":
        Player1Y += 5

    if LatestRecievedDataStr == "Player2Left":
        Player2X -= 5
    
    if LatestRecievedDataStr == "Player2Right":
        Player2X += 5
        
    if LatestRecievedDataStr == "Player2Up":
        Player2Y -= 5
        
    if LatestRecievedDataStr == "Player2Down":
        Player2Y += 5
    
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

    if PlayerAmount == 2:
        if P1X == True:
            Player1X = LatestRecievedDataStr
            DataToSend = str(Player1X)
            Server.sendto(DataToSend.encode(), Player2Addr)
            P1X = False

        if P1Y == True:
            Player1Y = LatestRecievedDataStr
            DataToSend = str(Player1Y)
            Server.sendto(DataToSend.encode(), Player2Addr)
            P1Y = False
        
        if P2X == True:
            Player2X = LatestRecievedDataStr
            P2X = False

        if P2Y == True:
            Player2Y = LatestRecievedDataStr
            DataToSend = str(Player2Y)
            Server.sendto(DataToSend.encode(), Player1Addr)
            P2Y = False

        if LatestRecievedDataStr == "Player1PositionX":
            P1X = True

        if LatestRecievedDataStr == "Player1PositionY":
            P1Y = True
        
        if LatestRecievedDataStr == "Player2PositionX":
            P2X = True
        
        if LatestRecievedDataStr == "Player2PositionY":
            P2Y = True
    
    if LatestRecievedDataStr == "Shutdown":
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
    
    if LatestRecievedDataStr == "P1Disconnect":
        Player1X = 50
        Player1Y = 50
        if PlayerAmount == 2:
            DataToSend = "Player1DC"
            Server.sendto(DataToSend.encode(), Player2Addr)
            Player1Addr = ""
            Player2Addr = ""
            PlayerAmount = 0
            Player2X = 200
            Player2Y = 200
            print("Player 1 disconnected; also kicked player 2")
        
        else:
            Player1Addr = ""
            PlayerAmount = 0
            print("Player 1 disconnected")

    if LatestRecievedDataStr == "P2Disconnect":
        if PlayerAmount == 2:
            DataToSend = "Player2DC"
            Server.sendto(DataToSend.encode(), Player1Addr)
            Player1Addr = ""
            Player2Addr = ""
            PlayerAmount = 0
            Player1X = 50
            Player1Y = 50
            Player2X = 200
            Player2Y = 200
            print("Player 2 disconnected; also kicked player 1")
    
    if PlayerAmount == 2:
        DataToSend = "Player1X"
        Server.sendto(DataToSend.encode(), Player2Addr)
        DataToSend = str(Player1X)
        Server.sendto(DataToSend.encode(), Player2Addr)
        DataToSend = "Player1Y"
        Server.sendto(DataToSend.encode(), Player2Addr)
        DataToSend  = str(Player1Y)
        Server.sendto(DataToSend.encode(), Player2Addr)

        DataToSend = "Player2X"
        Server.sendto(DataToSend.encode(), Player1Addr)
        DataToSend = str(Player2X)
        Server.sendto(DataToSend.encode(), Player1Addr)
        DataToSend = "Player2Y"
        Server.sendto(DataToSend.encode(), Player1Addr)
        DataToSend  = str(Player2Y)
        Server.sendto(DataToSend.encode(), Player1Addr)
    
print("Server stopped")
