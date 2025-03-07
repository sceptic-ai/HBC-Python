import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # creates a genesis block
        self.new_block(previous_hash=1, proof=100)
        
        
    def new_block(self, proof, previous_hash=None):
        # creates a new block in the Blockchain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        
        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new tansaction to go into next mined block
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # return the last block in the chain
        return self.chain[-1]
    
    
    @staticmethod
    def hash(block):
        """ 
        creates a SHA-256 hash of a block
        :param block: <dict> Block
        :return: <str>
        """
        
        # We must make sure that the Dictionary is ordered or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
        
        
    def proof_of_work(self, last_proof):
        """
        Simpe proof of work algorith:
        - Find a number p such that hash(pp') contains leading 4 zeroes
        - p is the previous proof, and p' is the new proof
        
        :param last_proof: <int>
        :return: <int>
        """
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validtes proof of work
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    

# Instantiate our node
app = Flask(__name__)

# generate a globally unique address for this
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorith to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    # We must recieve a reward for finding the proof.
    # the sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        )
    
    # Forge the new block by adding it to chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transaction': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    
    # Check that new required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message': f'Transaction will be addedd to block {index}'}
    
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain),
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
