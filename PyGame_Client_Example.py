#Imports
import pygame
from pygame.locals import *
import socket
import time

#Client Setup
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 49637
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Client.connect((SERVER_HOST, SERVER_PORT))
SERVER_PORT = str(SERVER_PORT)
print("Connected to server at " + SERVER_HOST + ":" + SERVER_PORT)
SERVER_PORT = int(SERVER_PORT)

#Game Variables
Running = True
Timer = False
Do_Once = False
P1X = False
P1Y = False
P2X = False
P2Y = False
TimerStartTime = 0
TimerCurrentTime = 0
IsPlayer = 0
Player1Color = (255, 0, 0)
Player2Color = (0, 0, 255)
MovementSpeed = 5
Player1X = 50
Player1Y = 50
Player2X = 200
Player2Y = 200
print("All game variables have been set")

#PyGame Setup
pygame.init()
Screen_Background = (150,150,150)
TrueScreen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
ObjectScreen = TrueScreen.copy()
pygame.display.set_caption("PyGame Client Test")
print("PyGame has been initialized and set up")

#Game
print("Game logic starting ")

class PlayerOne(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
  
        self.image = pygame.Surface((100, 100))
        self.image.fill(Player1Color)
Player1 = PlayerOne()

class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
  
        self.image = pygame.Surface((100, 100))
        self.image.fill(Player2Color)
Player2 = PlayerTwo()
print("Objects created")

SERVER_SENDING = "AttemptJoin"
Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
SERVER_RECIEVED, SERVER_ADDR = Client.recvfrom(1024)
SERVER_RECIEVED_STRING = str(SERVER_RECIEVED, 'utf-8')
print(SERVER_RECIEVED_STRING)

if SERVER_RECIEVED_STRING == "IsP1":
    IsPlayer = 1

elif SERVER_RECIEVED_STRING == "IsP2":
    IsPlayer = 2

while Running:
    
    if SERVER_RECIEVED_STRING == "ServerShutdown":
        Running = False
    
    if IsPlayer == 1:
        if pygame.key.get_pressed()[pygame.K_a]:
            SERVER_SENDING = "Player1Left"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player1X = int(Player1X)
            Player1X -= MovementSpeed

        if pygame.key.get_pressed()[pygame.K_d]:
            SERVER_SENDING = "Player1Right"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player1X = int(Player1X)
            Player1X += MovementSpeed

        if pygame.key.get_pressed()[pygame.K_w]:
            SERVER_SENDING = "Player1Up"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player1Y = int(Player1Y)
            Player1Y -= MovementSpeed
    
        if pygame.key.get_pressed()[pygame.K_s]:
            SERVER_SENDING = "Player1Down"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player1Y = int(Player1Y)
            Player1Y += MovementSpeed

    elif IsPlayer == 2:
        if pygame.key.get_pressed()[pygame.K_a]:
            SERVER_SENDING = "Player2Left"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player2X = int(Player2X)
            Player2X -= MovementSpeed

        if pygame.key.get_pressed()[pygame.K_d]:
            SERVER_SENDING = "Player2Right"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player2X = int(Player2X)
            Player2X += MovementSpeed

        if pygame.key.get_pressed()[pygame.K_w]:
            SERVER_SENDING = "Player2Up"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player2Y = int(Player2Y)
            Player2Y -= MovementSpeed
    
        if pygame.key.get_pressed()[pygame.K_s]:
            SERVER_SENDING = "Player2Down"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            Player2Y = int(Player2Y)
            Player2Y += MovementSpeed
    
    if P1X == True:
        Player1X = LatestRecievedDataStr
        P1X = False

    if P1Y == True:
        Player1Y = LatestRecievedDataStr
        P1Y = False
        
    if P2X == True:
        Player2X = LatestRecievedDataStr
        P2X = False

    if P2Y == True:
        Player2Y = LatestRecievedDataStr
        P2Y = False
    
    if IsPlayer == 1:
        SERVER_RECIEVED_STRING = str(SERVER_RECIEVED, 'utf-8')
        if SERVER_RECIEVED_STRING == "Player2X":
            P2X = True
        elif SERVER_RECIEVED_STRING == "Player2Y":
            P2Y = True
    elif IsPlayer == 2:
        SERVER_RECIEVED_STRING = str(SERVER_RECIEVED, 'utf-8')
        if SERVER_RECIEVED_STRING == "Player1X":
            P1X = True
        elif SERVER_RECIEVED_STRING == "Player1Y":
            P1Y = True
    
    if SERVER_RECIEVED_STRING == "Player1DC":
        Running = False
    
    elif SERVER_RECIEVED_STRING == "Player2DC":
        Running = False
    
    elif SERVER_RECIEVED_STRING == "ServerShutdown":
        Running = False
    
    if Timer == False:
        TimerStartTime = time.time()
        Timer = True

    TimerCurrentTime = time.time()
    TimerLength = TimerCurrentTime - TimerStartTime

    if TimerLength > 10.05:
        print("Timer reset")
        TimerStartTime = 0
        TimerCurrentTime = 0
        TimerLength = 0
        Timer = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exit button clicked")
            if IsPlayer == 1:
                SERVER_SENDING = "P1Disconnect"
                Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            
            elif IsPlayer == 2:
                SERVER_SENDING = "P2Disconnect"
                Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            
            Running = False
    
    if TimerLength > 10:
        if IsPlayer == 1:
            print("Attemping to send player position to server")
            SERVER_SENDING = "Player1PositionX"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = str(Player1X)
            print(SERVER_SENDING)
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = "Player1PositionY"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = str(Player1Y)
            print(SERVER_SENDING)
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))

        elif IsPlayer == 2:
            print("Attempting to send player position to server")
            SERVER_SENDING = "Player2PositionX"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = str(Player2X)
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = "Player2PositionY"
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
            SERVER_SENDING = str(Player2Y)
            Client.sendto(SERVER_SENDING.encode(), (SERVER_HOST, SERVER_PORT))
    
    ObjectScreen.fill(Screen_Background)
    ObjectScreen.blit(Player2.image, (Player2X, Player2Y))
    ObjectScreen.blit(Player1.image, (Player1X, Player1Y))
    TrueScreen.blit(pygame.transform.scale(ObjectScreen, TrueScreen.get_rect().size), (0, 0))
    pygame.display.flip()

pygame.quit()
print("Game logic stopped")
