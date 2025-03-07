#!/usr/bin/env python3

from .block import Block

class Blockchain:
    def __init__(self):
        """
        Constructor for Blockchain
        """
        self.chain = {}
        self.genesisBlock = Block(0, 'kek', 1518809761.5113006)
        self.chain[self.genesisBlock.currHash] = self.genesisBlock
        self.tailBlockHash = self.genesisBlock.currHash


    def addBlock(self, block, unSpentTransactions):
        """
        Add Block to Blockchain

        @param block - Block to be added to the chain

        @return Boolean - True if block was added, False otherwise
        """
        if self.isValidBlock(block, unSpentTransactions):
            self.chain[block.currHash] = block
            self.tailBlockHash = block.currHash
            return True
        return False

    def getBlock(self, hash):
        """
        Get Block from Blockchain

        @param hash - Hash of Block to get

        @return Block - The Block in question, or None
        """
        if hash in self.chain:
            return self.chain[hash]
        return None

    def getTransaction(self, hash):
        """
        Get Transaction from Blockchain

        @param hash - Hash of Transaction to get

        @return Block - The Transaction in question, or None
        """
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            for o_hash in currBlock.transactions:
                if hash == o_hash:
                    return currBlock.transactions[hash]
            currBlock = self.getBlock(currBlock.prevHash)
        return None

    def isValidBlock(self, block, unSpentTransactions):
        """
        Checks if Block is Valid

        @param block - Block to be checked

        @return Boolean - True if block is valid, False otherwise
        """

        prevBlock = self.getBlock(self.tailBlockHash)
        if prevBlock.index+1 != block.index:
            return False
        elif prevBlock.currHash != block.prevHash:
            return False
        elif block.calculateHash() != block.currHash:
            return False
        return block.isValid(unSpentTransactions)

    def isValid(self):
        """
        Check if Blockchain is Valid

        @return Boolean - True if Blockchain is Valid, False otherwise
        """
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            if not self.isValidBlock(currBlock):
                return False
            currBlock = self.getBlock(currBlock.prevHash)
        return True

    def __str__(self):
        string = ""
        currBlock = self.getBlock(self.tailBlockHash)
        while currBlock != self.genesisBlock:
            hash_str = currBlock.currHash[:4]
            hash_str += "..."
            hash_str += currBlock.currHash[-4:]
            string += "{} -> ".format(hash_str)
            currBlock = self.getBlock(currBlock.prevHash)
        return string[:-4]
