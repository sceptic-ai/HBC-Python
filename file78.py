# Import and load modules

from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date

# Run the flask server node

node = Flask(__name__)

# Block definition of the BitCent coin

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()

# Generate the Genesis Block

def create_genesis_block():

# Create a block using index zero and arbitrary previous hash

  return Block(0, date.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
  }, "0")

# A random made up address for the miner

miner_address = "bc012s&s&-random-miner-address-872sdsp*@"

# This section creates the blockchain on the local node

blockchain = []
blockchain.append(create_genesis_block())

# Store transactions in a list

this_nodes_transactions = []

# URLs of all nodes in the network are recorded

peer_nodes = []

# This variable stores the value of the mining status

mining = True

@node.route('/txion', methods=['POST'])
def transaction():

# During POST request transaction data is collected

  new_txion = request.get_json()
  # Transaction new_txion is added to the list
  this_nodes_transactions.append(new_txion)
  # Log data into console on the running node
  print "New transaction"
  print "FROM: {}".format(new_txion['from'].encode('ascii','replace'))
  print "TO: {}".format(new_txion['to'].encode('ascii','replace'))
  print "AMOUNT: {}\n".format(new_txion['amount'])

  return "Transaction submission successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain

  # Blocks are converted to dictionaries so they can be sent as JSON objects

  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    chain_to_send[i] = {
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send

def find_new_chains():
  # Get the blockchains of the other nodes
  other_chains = []
  for node_url in peer_nodes:
    # GET request
    block = requests.get(node_url + "/blocks").content
    # JSON object conversion to a Python dictionary
    block = json.loads(block)
    # Add to the chain
    other_chains.append(block)
  return other_chains

def consensus():
  # Get blocks from other nodes
  other_chains = find_new_chains()

  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain

  blockchain = longest_chain

#This section defines the function for the consensus mechanism

def proof_of_work(last_proof):

  incrementor = last_proof + 1

  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain -- Note: This was borrowed from Snakecoin project

  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1

  # Proof of Work

  return incrementor

@node.route('/mine', methods = ['GET'])
def mine():

  # Get the last proof of work

  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['proof-of-work']

  # Find poW of block

  proof = proof_of_work(last_proof)

  # Tx is added to the block

  this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )

  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash

  # Transaction list is emptied

  this_nodes_transactions[:] = []

  # New block creation

  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)


  # Send info back to client

  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"

#This sets the IP address of the node to it's public IP
node.run(host='0.0.0.0')
