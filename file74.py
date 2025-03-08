from .node import Node
from models.block import Block
from models.blockchain import Blockchain
from socket import *
import random
import pickle
import time
from threading import Thread
import datetime

# Message types for communication between nodes
REQUEST_NEIGHBORS = 1
REPLY_NEIGHBORS = 2
TRANSACTION = 3
BLOCK = 4
REQUEST_BLOCKCHAIN = 5
REPLY_BLOCKCHAIN = 6

class Server(Thread):

	def __init__(self, node):

		"""
		Constructor for Server
		@param node - Node object
		"""

		Thread.__init__(self)
		self.port = node.port_recv
		self.host = node.get_ip_addr()
		self.name = node.get_name()
		self.bufsize = 4096
		self.addr = (self.host, self.port)
		self.node_id = node.get_id()
		self.node = node
		self.socket = socket(AF_INET , SOCK_STREAM)
		self.socket.bind(self.addr)

	def run(self):
		self.socket.listen(5)
		print('Node {} is up...'.format(self.node.node_id))
		while True:
			client, caddr = self.socket.accept()

			serializedData = client.recv(self.bufsize)
			data = pickle.loads(serializedData)
			if data:
				messageType, payload = data
				if messageType == REQUEST_NEIGHBORS:
					self.node.sendData((REPLY_NEIGHBORS, self.node.peer_list), payload)
				if messageType == REPLY_NEIGHBORS:
					newPeers = set(self.node.peer_list)
					newPeers.update(payload)
					self.node.peer_list = list(newPeers)
				if messageType == TRANSACTION:
					if payload.hash not in self.node.unSpentTransactions:
						if payload.isValid(self.node.unSpentTransactions):
							self.node.unSpentTransactions[payload.hash] = payload
							self.node.currBlock.addTransaction(payload, self.node.unSpentTransactions)
							for peer in self.node.get_peer_list():
								self.node.sendData((TRANSACTION, payload), peer)
				if messageType == BLOCK:
					if self.node.blockChain.isValidBlock(payload, self.node.unSpentTransactions):
						for hash in payload.transactions:
							inputs = payload.transactions[hash].inputs
							for input in inputs:
								if input.hash != 'BLOCK-REWARD':
									transaction = self.node.unSpentTransactions[input.hash]
									transaction.outputs[input.index] = None
									self.node.unSpentTransactions[input.hash] = transaction

						self.node.blockChain.addBlock(payload, self.node.unSpentTransactions)
						self.node.currBlock = Block(payload.index+1, payload.currHash, datetime.datetime.utcnow().__str__())
						for peer in self.node.get_peer_list():
							self.node.sendData((BLOCK, payload), peer)
			client.close()
