import hashlib
from time import time

import json
import logging
import asyncio
import socket
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

	def new_block(self, previous_hash, current_hash, nonce, transactions):
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

#Set up logging for debuging and demo purposes
#Print and shows what is happening on the network
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

#Set for the first node of the network at port 8468
server = Server()
server.listen(8468)

#Set up an asyncio loop to use functions from the network
loop = asyncio.get_event_loop()
loop.set_debug(True)

#set up a second node to store the genesis block on the network
temp_server = Server()
temp_server.listen(8469)
#intialize the key for the chain
key = "chain"
#intialize the genesis block
bc = Blockchain()

#convert the block to a json string
temp_chain = json.dumps(bc.chain).encode()
#get the localhost ip
ip = socket.gethostbyname(socket.gethostname())
#connect the second node to the first node
bootstrap_node = (ip, 8468)
loop.run_until_complete(temp_server.bootstrap([bootstrap_node]))
#Storing genesis block on the network 
loop.run_until_complete(temp_server.set(key, temp_chain))

#The list of transactions on the network
trans_key = "transactions"
transactions = "List of Transactions : "
loop.run_until_complete(temp_server.set(trans_key, transactions))

#Keep the nodes running indefinitely
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()
