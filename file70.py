#!/usr/bin/env python3
import time
import hashlib

class Block:
    def __init__(self, index, prevHash, timestamp):
        """
        Constructor for Block

        @param index - Index in Chain
        @param prevHash - Hash of previous block in chain
        @param timestamp - Timestamp for when mining occurred
        """
        self.index = index
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.transactions = {}
        self.nonce = 0
        self.currHash = self.calculateHash()

    def calculateHash(self):
        """
        Calculate Hash for Block

        @return Digest - Hash of the Block
        """
        value = str(self.index) + str(self.prevHash) + str(self.timestamp) + str(self.nonce)
        for hash in self.transactions:
            value += self.transactions[hash].calculateHash()
        sha = hashlib.sha256(value.encode('utf-8'))
        return str(sha.hexdigest())


    def addTransaction(self, transaction, unSpentTransactions):
        """
        Add Transaction to Block

        @param transaction - New TX to Add
        @param unSpentTransactions - Dictionary of TXs with unused Outputs

        @return Boolean - True if Transaction added, False otherwise
        """
        if transaction.isValid(unSpentTransactions):
            self.transactions[transaction.hash] = transaction
            self.currHash = self.calculateHash()
            return True
        return False

    def removeTransaction(self, transaction):
        """
        Remove Transaction from Block

        @param transaction - TX to Remove

        @return Boolean - True if Transaction removed, False otherwise
        """
        if transaction.hash in self.transactions:
            del self.transactions[transaction.hash]
            self.currHash = self.calculateHash()
            return True
        return False

    def isValid(self, unSpentTransactions):
        """
        Check if Block is Valid

        @param unSpentTransactions - Dictionary of TXs with unused Outputs

        @return Boolean - True if Block valid, False otherwise
        """
        rewardCount = 0
        for hash in self.transactions:
            transaction = self.transactions[hash]
            if not transaction.isValid(unSpentTransactions):
                return False
            for input in transaction.inputs:
                if input.hash == 'BLOCK-REWARD':
                    rewardCount += 1
            if rewardCount > 1:
                return False
        return self.currHash == self.calculateHash()


    def __eq__(self, other):
        """
        Overrides the "=" operator for Block

        @param other - Other Block to compare to

        @return Boolean - True if Block is equal, False otherwise
        """
        if self.index != other.index:
            return False
        if self.prevHash != other.prevHash:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.transactions != other.transactions:
            return False
        if self.currHash != other.currHash:
            return False
        return True
