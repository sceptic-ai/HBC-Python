import hashlib
from time import time

import logging
import asyncio
import sys
import socket
import json
from kademlia.network import Server

class Blockchain:
	def __init__(self):
		self.chain = []
		# Inialize genesis block
		self.index = 0
		self.genesis_block()

	
	def genesis_block(self):
		#The very first block on the chain with no transactions
		block = {
			'index': self.index,
			'nonce': 0,
			'previous_hash': 'JamesJiang',
			'current_hash': self.hashing('0JamesJiang',0),
			'transactions' : 'None',
		}
		self.chain.append(block)
		return block

	def new_block(self, previous_hash, current_hash, nonce,transactions):
		# Create a new block and append it to the end of the chain
		self.index += 1
		block = {
			'index': self.index,
			'nonce': nonce,
			'previous_hash': previous_hash,
			'current_hash': current_hash,
			'transactions' : transactions,
		}
		self.chain.append(block)
		return block
	

	def hashing(self, msg, nonce):
		#hash msg and nonce 
		string = str(nonce) + str(msg)
		hash = hashlib.sha256(string.encode()).hexdigest()
		return hash

def store(key, chain, loop, server):
	#-------------------------------------------------
	# Sending Blockchain Over network
	#-------------------------------------------------
	
	#convert the block to a json string
	temp_chain = json.dumps(chain).encode()
	#broadcasting the block over the network
	loop.run_until_complete(server.set(key, temp_chain))


def get(key, loop, server):
	#Geting chain from network

	chain_ret = loop.run_until_complete(server.get(key))
	
	#Check if we have received a chain
	if (chain_ret == None):
		return False
	#convert the block from json string
	chain_decoded = json.loads(chain_ret.decode())
	return chain_decoded
	
def mining(bc, previous_hash, length, goal,key, loop, server, user):
	#Set the nonce to 0
	nonce = 0
	#initialize result_hash
	result_hash = previous_hash
	#Check if there is a chain to work on, if not return error
	if (get(key, loop, server) == False):
		print("Error")
		sys.exit(1)
	#If there is a chain to work on start mining
	else:
		#Mine while we have not reached our goal and while the current target remains the unchanged
		while ((result_hash[:length] != goal) and ((length == len(get(key, loop, server))))):
			#Change the nonce with each loop
			nonce += 1
			#hash the previous hash and the nonce
			result_hash = bc.hashing(previous_hash, nonce)
		#If we have reached the target first add to the chain
		if (length == len(get(key, loop, server))):
			#Get the list of transactions from the waiting pool
			trans_key = "transactions"
			trans_ret = loop.run_until_complete(server.get(trans_key))

			#add the reward for mining transaction to the end of the transaction string
			mining_trans = "Server Rewards " + user + " with 1 Coin"
			transactions = str(trans_ret) + mining_trans
			#Create the new block with the transactions
			block = bc.new_block(previous_hash, result_hash, nonce,str(transactions))
	#Return the updated chain
	return bc
	
def get_goal(length):
	#Calculates our current target based on the length
	goal = '0'
	if (length > 1):
		for i in range (length-1):
			goal += '0'
	#print(goal)
	return goal

def main(loop, server):
	# Create an blockchain object
	bc = Blockchain()

	#initialize the key for the chain
	key = "chain"
	#initialize the length
	length = 0
	#initialize user id for the transactions
	user = "JamesJiang" 
	
	#Get the current chain from the network
	network_chain = get(key, loop, server)
	#-----------
	#Check if there is a network chain
	if (network_chain == False):
		#If not exit
		print("Error")
		sys.exit(1)
	#If there is an Existing chain get the information from the chain
	else:
		#Get the existing chain
		bc.chain = network_chain
		#calculate the length of the chain
		length = len(network_chain)-1
		#Get the index of the chain
		bc.index = length
		#Get the previous hash
		previous_hash = bc.chain[length]['current_hash']
	#Send the current chain, previous hash, target length and goal information, the network key and the ,loop and node information
	bc = mining(bc, previous_hash, length+1, get_goal(length+1),key, loop, server,user)
	
	#Get the current chain from the network
	current_chain = get(key, loop, server)
	#If not chain exit with error
	if(current_chain == False):
		print("Error")
		sys.exit(1)
	#If our new chain is longer update the network
	elif(len(bc.chain) > len(current_chain)):
		store(key, bc.chain, loop, server)
		#Clear the waiting pool of the previous transactions
		store("transactions", "List of Transactions : ", loop, server)

	



if __name__ == '__main__':
	#ip = socket.gethostbyname(socket.gethostname())
	#IP address of the first node
	ip = "128.153.187.178"
	
	#Create the asyncio to be able to run node functions
	loop = asyncio.get_event_loop()
	loop.set_debug(True)

	#Create the kademlia node
	server = Server()
	server.listen(8470)
	
	#connect the kademlia node to the network
	bootstrap_node = (ip, 8468)
	loop.run_until_complete(server.bootstrap([bootstrap_node]))
	
	#Run until process is Interrupted
	try:
		while(True):
			main(loop, server)
	except KeyboardInterrupt:
		pass
	finally:
		server.stop()
		loop.close()
