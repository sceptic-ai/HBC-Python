import hashlib
import json
from datetime import datetime
class Transaction():
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
class Block():
    def __init__(self, tstamp, transactionsList, prevhash=''):
        self.nonce = 0
        self.tstamp = tstamp
        self.transactionsList = transactionsList
        self.prevhash = prevhash
        self.hash = self.calcHash()
    def calcHash(self):
        block_string = json.dumps({"nonce": self.nonce, 'tstamp': str(self.tstamp), 'transaction': self.transactionsList[0].amount, 'prevhash': self.prevhash}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self, diffic):
        while(self.hash[:diffic] != str('').zfill(diffic)):
            self.nonce += 1
            self.hash = self.calcHash()
        print('Block mined', self.hash)

    # def printHashes(self):
    #     print('prevhash', self.prevhash)
    #     print('hash', self.hash)
    def __str__(self):
        string = 'nonce: ' + str(self.nonce) + '\n'
        string += 'tstamp: ' + str(self.tstamp) + '\n'
        string += 'transaction: ' + str(self.transactionsList) + '\n'
        string += 'prevhash: ' + str(self.prevhash) + '\n'
        string += 'hash: ' + str(self.hash) + '\n'

        return string

# bblock = Block(1, '01/02/2018', 100)
# bblock.printHashes()

class BlockChain():
    def __init__(self):
        self.chain = [self.generateGenesisBlock(),]
        self.pendingTransactions = []
        self.mining_reward = 100
        self.difficulty = 2
    def generateGenesisBlock(self):
        return Block('01/01/2017', [Transaction(None, None, 0)])
    def getLastBlock(self):
        return self.chain[-1]
    # def addBlock(self, newBlock):
    #     newBlock.prevhash = self.getLastBlock().hash
    #     newBlock.mineBlock(self.difficulty)
    #     self.chain.append(newBlock)
    def minePendingTransaction(self, mining_reward_address):
        block = Block(datetime.now(), self.pendingTransactions)
        block.mineBlock(self.difficulty)
        print('BLock is mined you got reward', self.mining_reward)
        self.chain.append(block)
        self.pendingTransactions=[Transaction(None, mining_reward_address, self.mining_reward)]

    def createTransaction(self, T):
        self.pendingTransactions.append(T)
    def getBalance(self, address):
        balance = 0
        for b in self.chain:
            for t in b.transactionsList:
                if t.to_address == address:
                    balance += t.amount
                if t.from_address == address:
                    balance -= t.amount
        return balance
    def isChainValid(self):
        for i in range(1, len(self.chain)):
            prevb = self.chain[i-1]
            currb = self.chain[i]
            if(currb.hash != currb.calcHash()):
                print('Invalid block')
                return False
            if(currb.prevhash != prevb.hash):
                print('Invalid chain')
                return False
        return True
        


semCoin = BlockChain()
# print('Adding the first block')
# semCoin.addBlock(Block(1, '05/20/2017', 100))
# print('Adding the second block')
# semCoin.addBlock(Block(2, '05/21/2017', 20))
semCoin.createTransaction(Transaction('address1', 'address2', 100))
semCoin.createTransaction(Transaction('address2', 'address1', 50))
print('Starting mining')
semCoin.minePendingTransaction('semaddress')
print('Sem miner balance is ', semCoin.getBalance('semaddress'))

semCoin.createTransaction(Transaction('address1', 'address2', 200))
semCoin.createTransaction(Transaction('address2', 'address1', 150))
print('Starting mining again')
semCoin.minePendingTransaction('semaddress')
print('Sem miner balance is ', semCoin.getBalance('semaddress'))
