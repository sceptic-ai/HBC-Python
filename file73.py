# Planning
from models.block import Block
from models.blockchain import Blockchain

from .peer import Peer

from ecdsa import SigningKey, NIST384p
from socket import *
from threading import Thread
import sys
import time
import select
import pickle
import datetime
import random

class Node:

	def __init__(self, configFileName):

		"""
		Constructor for Node
		@param configFileName - Configuration file for the node

		"""
		self.peers_file = ''
		self.port_recv = 0
		self.sport = 0
		self.ip_addr = ''
		self.name = ''
		self.unSpentTransactions = {}
		self.blockChain = Blockchain()
		index = self.blockChain.getBlock(self.blockChain.tailBlockHash).index+1
		prevHash = self.blockChain.tailBlockHash
		timestamp = datetime.datetime.utcnow().__str__()
		self.currBlock = Block(index, prevHash, timestamp)

		self.priv_key = SigningKey.generate(curve=NIST384p)
		self.pub_key = self.priv_key.get_verifying_key()

		f = open('nodes/' + configFileName)
		for row in f:
			line = row.split('=')
			if (line[0] == 'listeningPort'):
				self.port_recv = int(line[1].rstrip('\n'))
			if (line[0] == 'node_ip'):
				self.ip_addr = line[1].rstrip('\n')
			if (line[0] == 'node_id'):
				self.node_id = line[1].rstrip('\n')
			if (line[0] == 'node_name'):
				self.name = line[1].rstrip('\n')
			if (line[0] == 'neighbors'):
				self.peers_file = line[1].rstrip('\n')
		f.close()
		self.peer_list = self.peer_info()


	def peer_info(self):

		"""
		Reads info about its peers
		@return peers - list of neighbors
		"""
		f = open('peers/' + self.peers_file)
		peers = []
		header = True
		for neighbor in f:
			if header:
				header = False
			else:
				v = neighbor.split(',')
				if v[0] != self.node_id:
					peer = Peer(v[0], v[1], v[2], v[3])
					peers.append(peer)
		f.close()
		return peers

	def get_ip_addr(self):

		"""
		Get the node's IP
		@retun ip_addr 
		"""
		return self.ip_addr

	def get_name(self):
		"""
		Get the node's name
		@retun name
		"""
		return self.name

	def get_id(self):
		"""
		Get the node's id
		@retun node_id
		"""
		return self.node_id

	def get_peer_list(self):
		"""
		Get the node's peer list
		@retun peer_list 
		"""
		return self.peer_list

	def sendTransaction(self, transaction):
		"""
		Sends transaction
		@param transaction - Transaction object
		"""
		inputs = transaction.inputs
		for input in inputs:
			if input.hash != 'BLOCK-REWARD':
				transaction_i = self.unSpentTransactions[input.hash]
				transaction_i.outputs[input.index] = None
				self.unSpentTransactions[input.hash] = transaction_i
		self.unSpentTransactions[transaction.hash] = transaction
		for peer in self.get_peer_list():
			self.sendData((3, transaction), peer)

	def signData(self, data):
		return self.priv_key.sign(data)

	def sendBlock(self):
		print("Block {} being sent...".format(self.currBlock.currHash))
		for peer in self.get_peer_list():
			self.sendData((4, self.currBlock), peer)
		self.blockChain.addBlock(self.currBlock, self.unSpentTransactions)
		self.currBlock = Block(self.currBlock.index+1, self.currBlock.currHash, datetime.datetime.utcnow().__str__())

	def sendData(self, data, recv):
		"""
		@param data - compsed of messageType and payload
		@param recv - node that recives the data
		"""
		print("sending data:", data, "To:", recv.name,"IP:", recv.ip_addr, "Port:", recv.port_recv,"From:", self.name, "IP:", self.ip_addr)
		time.sleep(1)
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((recv.ip_addr, int(recv.port_recv)))
		s.send(pickle.dumps(data))
		s.close()
