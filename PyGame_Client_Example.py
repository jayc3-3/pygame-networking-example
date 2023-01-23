#Imports
import pygame
from pygame.locals import *
import socket

#Client Setup
SERVER_HOST = ""
SERVER_PORT = 0
SERVER_SENDING = ""
SERVER_RECIEVED = ""
SERVER_RECIEVED_STRING = ""
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Setup of networked client complete")
#Server things for future reference:
    #Client.connect((SERVER_HOST, SERVER_PORT)) to connect to a server
    #Client.sendto(data_stuff.encode(), (SERVER_HOST, SERVER_PORT))
    #ServerMessage = Client.recv(1024)

#Game Variables
running = True
print("All game variables have been set")

#PyGame Setup
pygame.init()
Screen_Background = (0,0,0)
Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("PyGame Client Test")
print("PyGame has been initialized and set up")

#Game
print("Game logic starting ")
while running:
    SERVER_RECIEVED_STRING = str(SERVER_RECIEVED, 'utf-8')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
print("Game logic stopped")
