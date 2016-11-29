#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle, socket, struct, sys, time, threading, math, pygame

"""

TODO:
Bæta við ping pong falli til að tékka á disconnects
Prufa hosta remotely

"""

class LogicBulb(pygame.sprite.Sprite):
    def __init__(self, name, color):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface([22, 26])
        self.rect = self.image.get_rect()
        self.locX, self.locY = (250, 250)
        self.rect.x, self.rect.y = (self.locX, self.locY)
        self.angle = 180
        self.color = color

    def updateAngle(self, n):
        self.angle += n
        if self.angle >= 360:
            self.angle = self.angle - 360
        elif self.angle < 0:
            self.angle = 360 + self.angle

    def calcPos(self, speed):
        rad = math.radians(self.angle)
        x = math.cos(rad) * speed
        y = math.sin(rad) * speed

        self.locX += x
        self.locY -= y
        if self.locX < -20:
            self.locX = 505
        elif self.locX > 505:
            self.locX = -20
        if self.locY < -20:
            self.locY = 505
        elif self.locY > 505:
            self.locY = -20
        self.rect.x = self.locX
        self.rect.y = self.locY

    def getMail(self):
        mail={
            "name" : self.name,
            "pos" : (int(self.rect.x),int(self.rect.y)),
            "angle" : self.angle,
            "color" : self.color
        }
        return mail

class Server():
    def __init__(self):
        self.server_addr = ("127.0.0.1", 5000)
        self.buff_size = 1024
        self.clients = {} # Stores address and rect

        # Create, bind and set options for server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_addr)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # enables duplicate address and port bindings
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # enables permission to transmit broadcast messages
        print("Server started on {}:{}".format(*self.server_addr))

    # Receive messages from clients
    def recv(self):
        # Receive data and address from client socket
        self.data, self.addr = self.sock.recvfrom(self.buff_size)
        #print(self.addr)
        #print("Received {} bytes from {}".format(len(self.data),self.addr))

        # Deserialize data from client socket
        self.data = pickle.loads(self.data)
        #print("Received {} from {}".format(self.data, self.addr))

        self.recvHandler(self.addr, **self.data)

	# Interpret and handle data received
    def recvHandler(self, addr, signal, data):
        #print("Addr: {}".format(addr))
        #print("Signal: {}".format(signal))
        #print("Data: {}".format(data))
        #print("Clients: {}".format(self.clients))

        # Receive join signal from client
        if signal == ">>JOIN":
        #	print("{} has joined the game".format(data))
            self.clients[addr] = LogicBulb(data["name"], data["color"])# Add to clients dictionary list
            spitDict = {}
            for cli in self.clients:
                spitDict[cli] = self.clients[cli].getMail()
            msg = {
                "signal": ">>JOIN",
                "data": spitDict # Send active user list
            }
            #print("Clients after join: {}".format(self.clients))
            self.send(msg, addr)
            msg = {
                "signal": ">>UPDATE",
                "data": (addr, self.clients[addr].getMail())
            }
            self.broadcast(msg)


        # Update gamestate
        elif signal == ">>UPDATE":
            if "calcPos" in data:
                self.clients[addr].calcPos(2)
            if "+angle" in data:
                self.clients[addr].updateAngle(6)
            if "-angle" in data:
                self.clients[addr].updateAngle(-6)

            msg = {
                "signal": ">>UPDATE",
                "data": (addr, self.clients[addr].getMail())
            }
            self.broadcast(msg) # Broadcast updated information

        # Player has exited the game
        elif signal == ">>EXIT":
            #print("{} has left the game".format(addr))
            del self.clients[addr] # Remove from clients list
            msg = {
                "signal": ">>EXIT",
                "data": addr # Address information of client
            }
            self.broadcast(msg) # Broadcast exit status of user
            #print("Clients after exit: {}".format(self.clients))

	# Send data to one user
    def send(self, data, addr):
        data = pickle.dumps(data) # Serialize data before sending
        self.sock.sendto(data, addr)

    # Send data to all users
    def broadcast(self, data):
        #print("Broadcasting {}".format(data))
        data = pickle.dumps(data) # Serialize data before sending
        for client in self.clients:
            print(client)
            sent = self.sock.sendto(data, client)
            #print("Sent {} bytes to {}".format(sent, client))


sock = Server()

while True:
	sock.recv()