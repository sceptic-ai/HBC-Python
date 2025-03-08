# CS 411 Project - Step 1
# Erdem Bozkurt - 15460

import math
import random, string
import sys, os
import hashlib

if sys.version_info < (3, 6):
    import sha3


def createTransaction(prevHash):
    serialNum = random.getrandbits(128)
    payer = "Erdem Bozkurt"
    payee = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    amount = random.randint(1,10000)
    if not prevHash: prevHash = "First transaction"
    transaction = '''*** Bitcoin transaction ***
Serial number: %d
Payer: %s
Payee: %s
Amount: %d Satoshi
Previous hash in the chain: %s
Nonce: ''' % (serialNum, payer, payee, amount, prevHash)
    #printPow(serialNum, payer, payee, amount, prevHash, nonce, pow)
    return generateChain(transaction)


def generateNonce(transaction):
    answer = str(random.getrandbits(128))

    textWithNonce = transaction + answer + '\n'
    return textWithNonce

def generateChain(transaction):
    found = False

    while found == False:
        textWithNonce = generateNonce(transaction)
        hash = hashlib.sha3_256(textWithNonce).hexdigest()
        if(hash.startswith('000000')):
            print hash
            found = True

    text_file = open("LongestChain.txt", "a")
    text_file.write(textWithNonce + 'Proof of Work: ' + hash + '\n')
    text_file.close()
    return hash

# not used
def printPow(serialNum, payer, payee, amount, prevHash, nonce, pow):
    print "*** Bitcoin transaction ***"
    print "Serial number:"
    print "Payer:"
    print "Payee:"
    print "Amount:"
    print "Previous hash in the chain:"
    print "Nonce:", nonce
    print "Proof of Work:"

#createTransaction()
hash = ""
for x in range (20):
    hash = createTransaction(hash)
