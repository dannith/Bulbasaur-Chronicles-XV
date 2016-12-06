#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Networking boilerplate fyrir Pygame
"""

import pickle
import pygame
import socket
import struct
import sys

# Some nice colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)
purple = (255,0,255)

class Player():
	def __init__(self):
		self.x = 36
		self.y = 16
		self.width = 12
		self.height = 12
		self.updateRect()
		self.key_pressed = False

	# Display player on screen
	def display(self):
		pygame.draw.rect(screen, white, self.rect)
		return self.rect # We'll send rect information through socket

	# Basic movements
	def move(self):
		self.key = pygame.key.get_pressed()
		if self.key[pygame.K_RIGHT]: self.x += 2; self.key_pressed = True
		if self.key[pygame.K_LEFT]: self.x += -2; self.key_pressed = True
		if self.key[pygame.K_UP]: self.y += -2; self.key_pressed = True
		if self.key[pygame.K_DOWN]: self.y += 2; self.key_pressed = True

		# Update rect position
		self.updateRect()

	def updateRect(self):
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

# Initialize pygame
pygame.init()
pygame.display.set_caption("Bulbatown")
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()

class Socket():
	def __init__(self):
		self.server_addr = ("127.0.0.1", 5000)
		self.client_addr = ("0.0.0.0", 0) # Pick any free port currently on computer		
		self.buff_size = 1024
		self.clients = {}
		
		# Create socket
		self.ttl = struct.pack("b",1)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket object
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl) # 
		self.sock.settimeout(0.2)
		self.send(">>JOIN","") # Send initial data to server (join signal)

	def recv(self):
		# Attempt to receive data
		try:
			self.data = self.sock.recv(self.buff_size)
		except socket.timeout:
			print("timed out, no more responses")
			#print("timed out, no more responses")
		# Receive data
		else:
			self.data = pickle.loads(self.data) # Deserialize bytes to data
			#print("Received \"{}\" from server".format(self.data))
			self.recvHandler(**self.data) # Send to handler

	# Interpret and handle data received
	def recvHandler(self, signal, data):
		"""
		print("Signal: {}".format(signal))
		print("Data: {}".forrmat(data))
		print("type(data): {}".format(type(data)))
		"""

		# Server accepts join request
		if signal == ">>JOIN":
			self.clients = data # Receive clients list from server
			#print("Clients list after accept: {}".format(self.clients))

		# Server sent new gamestate
		elif signal == ">>UPDATE":
			self.clients[data[0]] = data[1]
			"""
			print("Updated positioning for {} to {}".format(data[0],data[1]))
			print("Clients list after update: {}".format(self.clients))
			"""

		# Server signals user who has left server
		elif signal == ">>EXIT":
			del self.clients[data]
			#print("Clients list after exit: {}".format(self.clients))

	def send(self, signal, data):
		msg = { 
			"signal": signal,
			 "data": data
			 }
		data = pickle.dumps(msg) # Serialize data to bytes before sending
		sent = self.sock.sendto(data, self.server_addr) # Send over socket
		#print("Sent {} bytes to server".format(sent))

	def close(self):
		self.send(">>EXIT","") # Send exit signal to server
		self.sock.close() # Close socket
		sys.exit()

sock = Socket()
player = Player()

while True:
	# Refill screen
	screen.fill(black)
	clock.tick(70)

	# Event handling
	event = pygame.event.poll()

	# Exit loop and game
	if event.type == pygame.QUIT: sock.close()

	rect = player.display()
	player.move()

	# Receive data from server
	sock.recv()

	if player.key_pressed == True:
		sock.send(">>UPDATE", rect)
		player.key_pressed = False

	for c in sock.clients:
		try:
			pygame.draw.rect(screen, red, sock.clients[c])
		except:
			pass
	pygame.display.flip()
s.close()
