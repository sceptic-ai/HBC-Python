# import Python modules
import datetime as dt
import hashlib
from flask import Flask, render_template, request, Response

# standard Flask declarations
app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')


# block class with attributes set at runtime
class Block:

    # attributes set at runtime (standard function)
    def __init__(self, index, timestamp, data, prevHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prevHash = prevHash
        self.hash = self.hash()

    # create hash
    def hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode() + str(self.timestamp).encode() + str(self.data).encode() + str(
            self.prevHash).encode())
        return sha.hexdigest()


# genesis block is the first block chain
# sets 0 index to genesis block
def createGBlock():
    return [Block(0, dt.datetime.now(), "Genesis Block", "0")]


# Initialize block chain with the genesis block. Start index 0
blockchain = createGBlock()
data = []  # empty to start


# add block to block chain based on data provided by user
def addBlock(form, data, blockchain):
    data.append([])
    i = 1
    while form.get("attendance{}".format(i)):
        data[-1].append(form.get("attendance{}".format(i)))
        i += 1
    prevBlock = blockchain[-1]
    addBlock = nxBlock(prevBlock, data)
    blockchain.append(addBlock)
    prevBlock = addBlock
    return "Block #{} has been added.".format(addBlock.index)


# function to get next block
def nxBlock(block, data):
    tempIndex = block.index + 1
    tempdt = dt.datetime.now()

    # A one level deep copy of data has been created since data is modified repeatedly
    # in the calling function and if data is a direct pointer, it leads to modification
    # of old data in the chain.
    tempData = data[:]
    tempHash = block.hash
    return Block(tempIndex, tempdt, tempData, tempHash)


# return data of block with specific data entered by user
def returnRecord(form, blockchain):
    # for each block of block chain, check to see if data provided matches data array of block chain
    # index 0 is name, 1 is date, 2 is course, 3 is year, 4 is number
    for block in blockchain:
        print(block.data)
        condition = (block.data[0] == form.get("name") and
                     block.data[1] == form.get("date") and
                     block.data[2] == form.get("course") and
                     block.data[3] == form.get("year") and
                     len(block.data[4]) == int(form.get("number")))

        # return number if match condition
        if condition:
            return block.data[4]
    return -1


# check if block in block chain has been modified
def checkIntegrity(chain):
    for i, block in enumerate(chain):
        if i < len(chain) - 1:
            print("Checking integrity of block {}".format(i))
            if block.hash() != chain[i + 1].prevHash:
                return "Chain has been modified at block index {}".format(i)
        else:
            return "No modification to block chain."


# Default Landing page index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Get Form input
@app.route('/', methods=['POST'])
def parse_request():
    if request.form.get("name"):
        while len(data) > 0:
            data.pop()
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template('class.html',
                               name=request.form.get("name"),
                               date=dt.date.today())

    elif request.form.get("number"):
        while len(data) > 2:
            data.pop()
        data.append(request.form.get("course"))
        data.append(request.form.get("year"))
        return render_template('attendance.html',
                               name=data[0],
                               course=request.form.get("course"),
                               year=request.form.get("year"),
                               number=int(request.form.get("number")))
    elif request.form.get("attendance1"):
        while len(data) > 4:
            data.pop()
        return render_template('result.html', result=addBlock(request.form, data, blockchain))

    else:
        return "Invalid POST request. This incident has been recorded."


# Show page to get information for fetching records
@app.route('/view.html', methods=['GET'])
def view():
    return render_template('class.html')


# Process form input for fetching records from the block chain
@app.route('/view.html', methods=['POST'])
def displayRecords():
    data = []
    data = returnRecord(request.form, blockchain)
    if data == -1:
        return "Records not found"
    return render_template('view.html',
                           name=request.form.get("name"),
                           course=request.form.get("course"),
                           year=request.form.get("year"),
                           status=data,
                           number=int(request.form.get("number")),
                           date=request.form.get("date"))


# Show page with result of checking block chain integrity
@app.route('/result.html', methods=['GET'])
def check():
    return render_template('result.html', result=checkIntegrity(blockchain))


# Start the flask app when program is blockchain.py is run
app.run()
