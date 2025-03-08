import socket
import sys
import threading
import os

localhost = ""
#looking for your own ip address and printing the results into a temporary file
os.system("ifconfig en0 | egrep -o '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v 255 > tmp")
#access the temporary file
with open('tmp', 'r') as file:
	#save the value in localhost
	localhost = file.readline() #only once

#delete the tmp file
os.system("rm tmp")
localhost = localhost[:-1]


addresses = []
transactions = []
miners = []
miners_blockchains = []


#if that argument is not add, it means that we are sending a new transaction
#and not adding a miner to the network
if len(sys.argv) > 1:
	if sys.argv[1] != "add":
		#separates the String --> 25ECNAddress to 25ECN Address
		sending_address_string = "{0} {1}".format(sys.argv[3][:sys.argv[3].index('N')+1], sys.argv[3][sys.argv[3].index('N')+1:])
		#we append the tx information to the transactions list
		transactions = [[sys.argv[1], sys.argv[2], sending_address_string]]
	else:
		transactions = []
else:
	transactions = []

##########################################################################################
##########################################################################################
#check if there are any waiting transactions; transactions that failed to be sent before
try:
	with open('waiting_txs.log', 'r') as file:
		data = file.readlines()
		for transaction_string in data:
			transaction_list = [transaction_string[1:transaction_string.index(',')]]
			message_start_index = transaction_string[::-1].index(',')
			transaction_list.append(transaction_string[transaction_string.index(',')+2:-message_start_index-1])
			transaction_list.append(transaction_string[-message_start_index+1:-2])
			transactions.append(transaction_list)
except Exception as e:
	print(e)
	print("Something bad happened while reading waiting_list of transactions")

#check if there are any miners that are waiting to be sent
try:
	with open('waiting_mns.log', 'r') as file:
		data = file.readlines()
		miners
except Exception as e:
	print(e)
	print("Something bad happened while reading waiting_list of transactions")

#append all the miners we have listed
with open('miners_ip_addresses.log', 'r') as file:
	data = file.readlines()
	addresses = [ip[:-1] for ip in data]
##########################################################################################
##########################################################################################


class Client:

	def __init__(self, address, transaction=[], add_miner=False, miner_ip=""):
		#create a TCP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#be able to reuse te socket for more connections later
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.settimeout(5)
		#connect to the address via port 10000
		sock.connect((address, 10000))
		self.transaction = transaction
		self.miner_ip = miner_ip
		self.add_miner = add_miner

		iThread = threading.Thread(target=self.sendTransaction, args=(sock,))
		iThread.daemon = True
		iThread.start()

		#receive the data from the designated miner
		data = sock.recv(4096)
		data = data.decode('utf-8')
		miners_blockchains.append(data)

	def sendTransaction(self, s):
		if len(sys.argv) > 1 and not self.add_miner:
			transaction_string = "[{0}, {1}, {2}]".format(self.transaction[0], self.transaction[1], self.transaction[2])
		elif self.add_miner == True:
			transaction_string = "\a" + self.miner_ip
		else:
			#not send anything, just receive
			transaction_string = "\t"
		s.sendall(transaction_string.encode('utf-8'))

#sending all the data and receiving. If it's completed successfully,
#succesful_sending will equal True
succesful_sending = False

for address in addresses:
	if address != localhost:
		try:
			if len(sys.argv) == 1:
				client = Client(address)
			elif sys.argv[1] == "add":
				client = Client(address, add_miner=True, miner_ip=sys.argv[2])
			for transaction in transactions:
				#receive all the transactions
				client = Client(address, transaction)
			succesful_sending = True
		except Exception as e:
			print("Error 404!")
			print(e)


if succesful_sending:
	#if the sending was succesful, the transaction waiting list will be deleted
	print("Connection succesfully established with the miners")
	#deletes the waiting_list transactions list
	open('waiting_list_transactions.log', 'w').close()
	os.system("python verify_choose_blocks.py " + str(miners_blockchains))
else:
	with open('waiting_list_transactions.log', 'w') as file:
		if len(sys.argv) > 3:
			for transaction in transactions:
				transaction_string = "[{0}, {1}, {2}]".format(transaction[0], transaction[1], transaction[2])
				file.write(transaction_string+'\n')
			print("Your transaction couldnt be sent to any miner so it will be placed in the transactions waiting list and be sent when possible")


