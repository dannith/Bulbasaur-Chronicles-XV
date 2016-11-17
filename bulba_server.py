#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
World of Bulbasaur Server v.0.1

(17.11.16)
Multicast UDP server sem heldur utan um users lista,
tekur við gögnum frá clientum og sendir til þeirra allra.
Keyra þetta drasl áður en clientar tengjast

"""

import pickle
import socket
import struct
import sys

class Socket():
	def __init__(self, host, port, multicast):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket
		self.server_address = (host, port) # Host and port information
		self.buff_size = 4096 # Buffer size
		self.sock.bind(self.server_address) # Bind socket to the port
		self.players = []
		print("starting server on {}:{}".format(host,port))

		# Add socket to the multicast group on all interfaces (ath!)
		self.group = socket.inet_aton(multicast)
		self.mreq = struct.pack("4sL", self.group, socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)

	# Send data through socket
	def sendData(self, data, address):
		if self.data:
			self.data = pickle.dumps(self.data) # Serialize object before sending
			# Send data to all except the master sender
			for player in self.players:
				if player != address:
					self.sock.sendto(self.data, player)
					#print("sent {} bytes to {}".format(sent,player))

	# Receive data from socket
	def readData(self):
		# Read data from socket and print byte length
		self.data, self.address = self.sock.recvfrom(self.buff_size)
		#print("received {} bytes from {}".format(len(self.data),self.address))
		
		# Remove user from players list if we get exit signal from socket
		if self.data == "exit":
			del self.players[address]

		# Add to player list if not already there
		if self.address not in self.players:
			self.players.append(self.address)
			#self.sendData()

		# Deserialize and print data from socket
		self.data = pickle.loads(self.data)
		#print("received from {}: {}".format(self.address, self.data))
		return self.data, self.address

# Network information
host = ""
port = 10000
multicast_group = "224.3.29.71"
sock = Socket(host, port, multicast_group)

while True:
	data, addr = sock.readData()
	sock.sendData(data, addr)