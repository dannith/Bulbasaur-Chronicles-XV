#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create a socket with the socket() system call
Connect the socket to the address of the server using the connect() system call
Send and receive data. There are a number of ways to do this, but the simplest is to use the read() and write() system calls.
"""

import pickle, pygame, socket, struct, sys


# Some nice colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)
purple = (255,0,255)

class BulbRender(pygame.sprite.Sprite):

	def __init__(self, pos, angle, name, color):
		pygame.sprite.Sprite.__init__(self)
		self.angle = angle
		self.animInterval = 0
		self.animIntervalMax = 10
		self.animating = False
		self.frame = 0
		self.name = pygame.font.Font(None, 22).render(name, True, (0, 255, 255))
		self.color = int(color)
		self.rotation = self.getSprite()
		self.render = self.rotation[self.frame]
		self.rect = self.render.get_rect()
		self.rect.x, self.rect.y = pos

	def getSprite(self):
		i = bulbSprites[self.color]["frames"]
		self.flip = False
		if self.angle > 338 or self.angle <= 23:
			self.flip = True
			return i["side"]
		elif self.angle > 23 and self.angle <= 68:
			self.flip = True
			return i["sideBack"]
		elif self.angle > 68 and self.angle <= 113:
			return i["back"]
		elif self.angle > 113 and self.angle <= 158:
			return i["sideBack"]
		elif self.angle > 158 and self.angle <= 203:
			return i["side"]
		elif self.angle > 203 and self.angle <= 248:
			return i["sideFront"]
		elif self.angle > 248 and self.angle <= 293:
			return i["front"]
		elif self.angle > 293 and self.angle <= 338:
			self.flip = True
			return i["sideFront"]

	def refresh(self, pos, angle):
		if (self.rect.x, self.rect.y) != pos:
			self.animating = True
		self.rect.x, self.rect.y = pos
		self.angle = angle
		self.rotation = self.getSprite()

	def update(self):
		if self.animating:
			self.animInterval += 1
			if self.animInterval == self.animIntervalMax:
				self.animInterval = 0
				self.frame += 1
				if self.frame == 4:
					self.frame = 0
					self.animating = 0
		if self.flip: self.image = pygame.transform.flip(self.rotation[self.frame], True, False)
		else: self.image = self.rotation[self.frame]
		textW = self.name.get_width()
		textLoc = 1 + self.rect.x - (textW - 22) / 2
		screen.blit(self.name, (textLoc, self.rect.y - 10))

bulbSprites = [
	{"sheet" : pygame.image.load("grafix/bulba-sprite0.png"), "frames" : {}},
	{"sheet" : pygame.image.load("grafix/bulba-sprite1.png"), "frames" : {}},
	{"sheet" : pygame.image.load("grafix/bulba-sprite2.png"), "frames" : {}},
	{"sheet" : pygame.image.load("grafix/bulba-sprite3.png"), "frames" : {}}
]

for name in bulbSprites:
	name["frames"]["front"] = [
		name["sheet"].subsurface(0, 0, 26, 22),
		name["sheet"].subsurface(0, 26, 26, 22),
		name["sheet"].subsurface(0, 50, 26, 22),
		name["sheet"].subsurface(0, 76, 26, 22)
	]
	name["frames"]["sideFront"] = [
		name["sheet"].subsurface(41, 0, 26, 22),
		name["sheet"].subsurface(41, 26, 26, 22),
		name["sheet"].subsurface(41, 50, 26, 22),
		name["sheet"].subsurface(41, 76, 26, 22)
	]
	name["frames"]["side"] = [
		name["sheet"].subsurface(80, 0, 26, 22),
		name["sheet"].subsurface(80, 26, 26, 22),
		name["sheet"].subsurface(80, 50, 26, 22),
		name["sheet"].subsurface(80, 76, 26, 22)
	]
	name["frames"]["sideBack"] = [
		name["sheet"].subsurface(117, 0, 26, 22),
		name["sheet"].subsurface(117, 26, 26, 22),
		name["sheet"].subsurface(117, 50, 26, 22),
		name["sheet"].subsurface(117, 76, 26, 22)
	]
	name["frames"]["back"] = [
		name["sheet"].subsurface(153, 0, 26, 22),
		name["sheet"].subsurface(153, 26, 26, 22),
		name["sheet"].subsurface(153, 50, 26, 22),
		name["sheet"].subsurface(153, 76, 26, 22)
	]


# Initialize pygame
pygame.init()
pygame.display.set_caption("Bulbatown")
userName = ""
color = True

while userName == "":
	userName = input("Whats your name?")
while color:
	userColor = input("Select a color: 0 - Classic, 1 - Purple, 2 - Orange, 3 - Blue")
	if userColor in ["0", "1", "2", "3"]: color = False
	else: print("Please select wisely.")

screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

class Socket():
	def __init__(self, name, color):
		self.server_addr = ("127.0.0.1", 5000)
		self.client_addr = ("0.0.0.0", 0) # Pick any free port currently on computer
		self.buff_size = 1024
		self.clients = {}

		# Create socket
		self.ttl = struct.pack("b",1)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket object
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl) #
		self.sock.settimeout(0.2)
		msg = {
			"name" : name,
			"color" : color
		}
		self.send(">>JOIN", msg) # Send initial data to server (join signal)

	def recv(self):
		# Attempt to receive data
		try:
			self.data = self.sock.recv(self.buff_size)
		except socket.timeout:
			pass
			#print("timed out, no more responses")
			#print("timed out, no more responses")
		# Receive data
		else:
			self.data = pickle.loads(self.data) # Deserialize data
			#print("Received \"{}\" from server".format(self.data))
			self.recvHandler(**self.data) # Send to handler

	# Interpret and handle data received
	def recvHandler(self, signal, data):
		"""
		print("Signal: {}".format(signal))
		print("Data: {}".format(data))
		print("type(data): {}".format(type(data)))
		"""

		# Server accepts join request
		if signal == ">>JOIN":
			for newRender in data:
				self.clients[newRender] = BulbRender(data[newRender]["pos"], data[newRender]["angle"], data[newRender]["name"], data[newRender]["color"])
				players.add(self.clients[newRender])

			#self.clients = data # Receive clients list from server
			#print("Clients list after accept: {}".format(self.clients))

		# Server sent new gamestate
		elif signal == ">>UPDATE":
			if data[0] in self.clients:
				self.clients[data[0]].refresh(data[1]["pos"], data[1]["angle"])
			else:
				self.clients[data[0]] = BulbRender(data[1]["pos"], data[1]["angle"], data[1]["name"], data[1]["color"])
				players.add(self.clients[data[0]])
			#print(self.clients)
			#self.clients[data[0]] = data[1]
			"""
			print("Updated positioning for {} to {}".format(data[0],data[1]))
			print("Clients list after update: {}".format(self.clients))
			"""

		# Server is checking for disconnection
		elif signal == ">>STATUS":
			self.send(">>STATUS","")

		# Server signals user who has left server
		elif signal == ">>EXIT":
			players.remove(self.clients[data])
			del self.clients[data]
			print("Clients list after exit: {}".format(self.clients))

	def send(self, signal, info):
		msg = {
			"signal": signal,
			 "data": info
			 }
		data = pickle.dumps(msg) # Serialize data before sending
		sent = self.sock.sendto(data, self.server_addr) # Send over socket
		#print("Sent {} bytes to server".format(sent))

	def close(self):
		self.send(">>EXIT","") # Send exit signal to server
		self.sock.close() # Close socket
		sys.exit()

sock = Socket(userName, userColor)

def move():
	key = pygame.key.get_pressed()
	sending = False
	update = []
	for player in sock.clients:
		print(sock.clients[player].angle)
	if key[pygame.K_UP]:
		sending = True
		update.append("calcPos")
	if key[pygame.K_RIGHT]:
		sending = True
		update.append("-angle")
	if key[pygame.K_LEFT]:
		sending = True
		update.append("+angle")
	if sending:
		return update
	else:
		return False

players = pygame.sprite.Group()
bg = pygame.image.load("grafix/bg.jpg")

while True:
	# Refill screen
	screen.fill(green)
	screen.blit(bg, (0,0))
	clock.tick(70)

	# Event handling
	event = pygame.event.poll()

	# Exit loop and game
	if event.type == pygame.QUIT: sock.close()

	if move():
		sock.send(">>UPDATE", move())

	# Receive data from server
	sock.recv()

	players.update()
	players.draw(screen)



	pygame.display.flip()
s.close()