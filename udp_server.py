#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Networking boilerplate fyrir Pygame

TODO:
Bæta við ping pong falli til að tékka á disconnects
"""

import pickle
import socket
import struct
import sys
import time
import threading


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
		print("Received {} bytes from {}".format(len(self.data),self.addr))

		# Deserialize bytes to data from client socket
		self.data = pickle.loads(self.data)
		print("Received {} from {}".format(self.data, self.addr))

		self.recvHandler(self.addr, **self.data)

	# Interpret and handle data received
	def recvHandler(self, addr, signal, data):
		print("Addr: {}".format(addr))
		print("Signal: {}".format(signal))
		print("Data: {}".format(data))
		print("Clients: {}".format(self.clients))

		# Receive join signal from client
		if signal == ">>JOIN":
			print("{} has joined the game".format(addr))
			self.clients[addr] = ""# Add to clients dictionary list
			self.msg = {
				"signal": ">>JOIN",
				"data": self.clients # Send active user list
			}
			print("Clients after join: {}".format(self.clients))
			self.send(self.msg, addr)

		# Update gamestate
		elif signal == ">>UPDATE":
			self.clients[addr] = data # Update to new rect 
			self.msg = {
				"signal": ">>UPDATE",
				"data": (addr, self.clients[addr])
			}
			print("Updated {} rect info to {}".format(addr,data))
			self.broadcast(self.msg) # Broadcast updated information

		# Player has exited the game
		elif signal == ">>EXIT":
			print("{} has left the game".format(addr))
			del self.clients[addr] # Remove from clients list
			self.msg = {
				"signal": ">>EXIT",
				"data": addr # Address information of client
			}
			self.broadcast(self.msg) # Broadcast exit status of user
			print("Clients after exit: {}".format(self.clients))

	# Send data to one user
	def send(self, data, addr):
		data = pickle.dumps(data) # Serialize data to bytes before sending
		self.sock.sendto(data, addr)

	# Send data to all users
	def broadcast(self, data):
		print("Broadcasting {}".format(data))
		data = pickle.dumps(data) # Serialize data before sending
		for client in self.clients:
			sent = self.sock.sendto(data, client)
			print("Sent {} bytes to {}".format(sent, client))


sock = Server()

while True:
	sock.recv()

# x = >>join
# print x[:2]
