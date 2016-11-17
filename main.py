#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
World of Bulbasaur Client v.0.2 

(17.11.16)
Keyrist mjög hægt ef bara einn client tengist servernum. 
Byrjar að glitcha ef fleiri en tveir clientar eru online,
sjá "receive and display data from the socket" try/except 
neðst í while lykkunni. 

Þarf að laga bulbasaur hreyfingarnar í Player.move() og
kannski Sprite fallinu.

"""

import pickle # For serializing and deserializing bytes
import pygame
import socket
import struct
import sys

def Sprite(direction):
    spritesheet = pygame.image.load("grafix/bulba-sprite.png").convert_alpha()
    frames = {
        "north" : [
            spritesheet.subsurface(159, 0, 17, 22),
            spritesheet.subsurface(159, 26, 17, 22),
            spritesheet.subsurface(159, 50, 17, 22),
            spritesheet.subsurface(159, 76, 17, 22)
        ],
        "west" : [
            spritesheet.subsurface(80, 0, 24, 22),
            spritesheet.subsurface(80, 26, 24, 22),
            spritesheet.subsurface(80, 50, 24, 22),
            spritesheet.subsurface(80, 76, 24, 22)
        ],
        "south" : [
            spritesheet.subsurface(4, 0, 21, 22),
            spritesheet.subsurface(4, 26, 21, 22),
            spritesheet.subsurface(4, 50, 21, 22),
            spritesheet.subsurface(4, 76, 21, 22)
        ],
        # Flip west subsurface horizontally to receive east direction
        "east" : [
            pygame.transform.flip(spritesheet.subsurface(80, 0, 24, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(80, 26, 24, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(80, 50, 24, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(80, 76, 24, 22), True, False)
        ],
        "southwest" : [
            spritesheet.subsurface(42, 0, 26, 22),
            spritesheet.subsurface(42, 26, 26, 22),
            spritesheet.subsurface(42, 50, 26, 22),
            spritesheet.subsurface(42, 76, 26, 22)
        ],
        # Flip southwest horizontally to receive southeast direction
        "southeast" : [
            pygame.transform.flip(spritesheet.subsurface(42, 0, 26, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(42, 26, 26, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(42, 50, 26, 22), True, False),
            pygame.transform.flip(spritesheet.subsurface(42, 76, 26, 22), True, False)
        ],
        "northwest" : [
            spritesheet.subsurface(120, 0, 26, 22),
            spritesheet.subsurface(120, 26, 26, 22),
            spritesheet.subsurface(120, 50, 26, 22),
            spritesheet.subsurface(120, 76, 26, 22)
        ],
        # Flip southwest subsurface horizontally and vertically to receive northeast direction
        "northeast" : [
            pygame.transform.flip(spritesheet.subsurface(42, 0, 26, 22), True, True),
            pygame.transform.flip(spritesheet.subsurface(42, 26, 26, 22), True, True),
            pygame.transform.flip(spritesheet.subsurface(42, 50, 26, 22), True, True),
            pygame.transform.flip(spritesheet.subsurface(42, 76, 26, 22), True, True)
        ]
    }
    return frames[direction]

class Socket():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.sock.settimeout(0.2) # Set a timeout so socket wont block indefinitely when trying to recv data
        #self.ttl = struct.pack('b',1) # Set time-to-live for data to 1 so they dont past the local network segment

    # Send data through socket
    def send(self, data, direction):
        #print("sending {!r} to {}:{}".format(data,self.host,self.port))
        data = (data, direction)
        self.byte_data = pickle.dumps(data) # Serialize data to bytes before sending
        self.sock.sendto(self.byte_data, (self.host, self.port))

    # Receive data from socket
    def receive(self, buff):
        try:
            self.data, self.server = self.sock.recvfrom(buff)
        except socket.timeout:
            #print("Timed out, no more responses")
            pass
        else:
            self.data = pickle.loads(self.data) # Deserialize data from socket
            #print("received {!r} from {}".format(self.data, self.server))
            return self.data

    # Close socket
    def close(self):
        self.sock.sendto("exit", (self.host, self.port)) # Send exit signal to server
        self.sock.close()
# end class Socket

class Player():
    def __init__(self):
        self.x = 36
        self.y = 16
        self.width = 22
        self.height = 22
        self.updateRect()

    # Display player on screen
    def display(self, direction="south"):
        self.sprite = Sprite(direction)
        for s in self.sprite:
            screen.blit(s, (self.x, self.y))
        return self.rect, direction # We'll send this information through the socket

    def move(self):
        # Key handling
        self.key = pygame.key.get_pressed()
        self.up = self.key[pygame.K_UP]
        self.down = self.key[pygame.K_DOWN]
        self.left = self.key[pygame.K_LEFT]
        self.right = self.key[pygame.K_RIGHT]

        # Örugglega einhver miklu fallegri leið til að gera þetta....
        # Moves player in a certain direction and displays corresponding sprites
        # Upwards movement
        if self.up: 
            self.y += -2
            self.display("north")
        elif self.up and self.left:
            self.x += -2
            self.y += -2
            self.display("northwest")
        elif self.up and self.right:
            self.x += 2
            self.y += -2
            self.display("northeast")

        # Downwards movement
        if self.down: 
            self.y += 2
            self.display("south")
        elif self.down and self.left:
            self.x += -2
            self.y += 2
            self.display("southwest")
        elif self.down and self.right:
            self.x += 2
            self.y += 2
            self.display("southeast")  

        # Left and right movement 
        if self.left: 
            self.x += -2 
            self.display("west")
        if self.right: 
            self.x += 2 
            self.display("east")

        # Update rect position
        self.updateRect()

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
# end class Player

# Some nice colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)
purple = (255,0,255)

# Initialize pygame
pygame.init()
pygame.display.set_caption("Oskar Client")
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
player = Player()

# Networking information
host = "224.3.29.71" # Address reserved for multicasting
port = 10000 # Unreserved port number
sock = Socket(host, port)
buff = 4096

# Display other players on screen
def display(rect, direction="south"):
    sprite = Sprite(direction)
    for s in sprite:
        screen.blit(s, rect)

while True:
    # Refill screen
    screen.fill(black)
    clock.tick(100)

    # Event handling
    event = pygame.event.poll()

    # Exit loop and game
    if event.type == pygame.QUIT:
        sock.close()
        pygame.quit()
        sys.exit

    # Get player rect value and send through socket
    rect, direction = player.display()
    sock.send(rect, direction)

    # Move the player around
    player.move()

    # Receive and display rect data from the socket 
    recv = sock.receive(buff)   
    try:
        display(recv[0],recv[1])
        #pygame.draw.rect(screen,red,recv)
    # We wont make any fuss about dropped packets
    except:
        pass

    # Update display    
    pygame.display.update()