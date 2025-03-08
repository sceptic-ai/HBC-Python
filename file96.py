import time
import os
import sys

minutes_passed = 0
public_address = ""
balance = 0
with open('account.log', 'r') as file:
	lines = file.readlines()
	public_address = lines[1]

def check_balance():
	balance = 0
	with open('blocks.csv', 'r') as file:
		blocks = file.readlines()
	for block in blocks:
		if public_address in block:
			#very complicated process for finding out if this address
			#has mined the block
			char1 = [pos for pos, char in enumerate(block) if char == "["][3]-1
			char2 = [pos for pos, char in enumerate(block) if char == "]"][3]
			miner = block[char1:char2]
			if public_address == miner:
				balance += 50
			#very complicated process for finding the 
			#block of transactions in the block
			if "[]" in block:
				index_end_tx = block.index("[]")
			else:	
				index_end_tx = block.index(':') - 4
			if block[idex_end_tx] != "]":
				index_end_tx += 1

			index_str_tx = block.index("[[") + 2

			transaction_block = block[index_str_tx:index_end_tx].split('], ')


			for transaction in transaction_block:
				if public_address in transaction:
					transaction_process = [s for s in transaction.split(', ')]
					quantity = int(transaction_process[2][:transaction_process[2].index('E')])
					if public_address in transaction_process[0] and public_address in transaction_process[2]:
						#if the address sends funds to itself nothing happens
						pass
					elif public_address in transaction_process[0]:
						balance -= quantity
					elif public_address in transaction_process[2]:
						balance += quantity


#will run constantly
try:
	while True:
		#time.sleep(60)
		#update the ip's of the miners
		print("Updating the list of available miners...")
		os.system('python mactoip.py')
		#download the blocks
		print("Trying to communicate to other miners...")
		os.system('python communicate_to_miners.py')
		balance = check_balance()
		print("Your balance is...")
		print(balance)
except KeyboardInterrupt:
	print("Closing...")


