import os
import hashlib
import time

transactions = []
miners_to_add = []

nonce = 0
block_number = 0
my_mac = ""
os.system("ifconfig en0 | awk '/ether/{print $2}' > tmp")
with open('tmp', 'r') as file:
	my_mac = file.read()
	my_mac = my_mac[:-2]
previousHash = ""

difficulty = 2



def updateBlockNumber():
	global block_number
	with open('blocks.csv', 'r') as file:
		all_blocks = file.readlines()
		if len(all_blocks) > 1:
			last_block_number = all_blocks[-1][1:all_blocks[-1].index(']')]
			if block_number != last_block_number:
				block_number = last_block_number
				return True
		else:
			block_number = 1

	return False

def updatePreviousHash():
	global previousHash
	with open('blocks.csv', 'r') as file:
		all_blocks = file.readlines()
		if len(all_blocks) > 1:
			last_block_reversed = all_blocks[-1][::-1]
			last_parenthesis_index = last_block_reversed.index('[')
			last_hash = all_blocks[-1][-last_parenthesis_index:-2]
			if previousHash != last_hash:
				previousHash = last_hash
				return True
		else:
			previousHash = "0000000000"

	return False

def updateTxList():
	global transactions
	final_txs = []
	with open('new_transactions.log', 'r') as file:
		txs = file.readlines()
	for tx in txs:
		final_txs.append(tx[:-1])
	if final_txs != transactions:
		transactions = final_txs[:]
		return True
	return False

def updateMinersList():
	global miners_to_add
	final_miners = []
	with open('new_miners.log', 'r') as file:
		miners = file.readlines()
	for m in miners:
			final_miners.append(m[:-1])
	if final_miners != miners_to_add:
		miners_to_add = final_miners[:]
		return True
	return False

while True:
	try:
		updateNonce = False
		#update them and check if they have changed
		if updateBlockNumber():
			updateNonce = True
		elif updatePreviousHash():
			updateNonce = True
		elif updateMinersList():
			updateNonce = True
		elif updateTxList():
			updateNonce = True

		if updateNonce:
			nonce = 0
			print("Updating nonce")
		#small delay
		time.sleep(0.01)
		if len(transactions) > 0 or len(miners_to_add) > 0:
			hashable_block = "[{0}][{1}][{2}][{3}][{4}][{5}]".format(block_number, previousHash, nonce, my_mac, transactions, miners_to_add)
			final_hash = hashlib.sha256(hashable_block).hexdigest()
			if final_hash[:difficulty] == "0"*difficulty:
				print("Block found")
				with open('blocks.csv', 'a') as file:
					file.write("{0}[{1}]\n".format(hashable_block, final_hash))
				nonce = 0
				open('new_transactions.log', 'w').close()
				open('new_miners.log', 'w').close()
				nonce = 0
			else:
				nonce += 1
	except KeyboardInterrupt:
		print("Ending programm")
		sys.exit()




