import hashlib
import json
from time import time
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
import pickledb


class Blockchain(object):
    def __init__(self, port):
        # 初始化数据库和相关参数
        self.chain = []  # 区块链
        self.current_transactions = []  # 交易池
        self.nodes = set()  # 节点集
        self.port = port  # 端口号
        database_name = str(port) + "blockchain.db"  # 每个端口对应的数据库名称
        self.db = pickledb.load(f'{database_name}', True)  # 加载端口对应数据库
        # 检查数据库是否有区块数据
        if self.db.get('total'):  # 有
            for b in range(1, self.db.get('total') + 1):  # 数据库数据填充到变量中
                self.chain.append(eval(self.db.get(str(b))))
        else:  # 无
            self.db.set('total', 0)
            self.new_block(previous_hash=1, proof=100)  # 创建创世区块
        # 检查数据库是否有交易数据
        if self.db.get('ct'):  # 有
            self.current_transactions = eval(self.db.get('ct'))   # 数据库数据填充到变量
            self.pool_status = True
        # 检查数据库是否有节点数据
        if self.db.get('nodes'):  # 有
            for node in eval(self.db.get('nodes')):  # 数据库数据填充到变量
                self.nodes.add(node)

    def restart(self):  # 重置区块链
        self.db.deldb()  # 清空数据库
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
        return "区块链数据已清空，重启一条新的区块链成功"

    def new_block(self, proof, previous_hash=None):  # 生成新区块
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.chain[-1]['hash']
        }
        # 获得merkle tree根节点
        roottemp = self.get_merkle_root(self.current_transactions)
        block["merkle_root"] = roottemp
        # 获得自身hash
        block['hash'] = self.hash(block)
        # 重置交易池
        self.current_transactions = []
        # 重置数据库交易池
        if self.db.get('ct'):
            self.db.rem('ct')
        # 添加新区块到链上
        self.chain.append(block)
        # 数据库操作 总区块数更新
        self.db.set('total', len(self.chain))
        # 数据库操作 新增区块
        self.db.set(str(block['index']), json.dumps(block, sort_keys=True))
        return block

    def new_transactions(self, sender, recipient, amount):  # 生成新交易
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # 数据库操作 交易池更新
        self.db.set('ct', json.dumps(self.current_transactions, sort_keys=True))
        return int(self.last_block['index'])+1

    @staticmethod
    def hash(block):  # 哈希 SHA-256加密
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @property
    def last_block(self):  # 返回最后一个区块/最新区块
        return self.chain[-1]

    def proof_of_work(self, pool):  # 工作量证明
        proof = 0
        while self.valid_proof(pool, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(pool, proof):  # 工作量验证
        guess = json.dumps(pool, sort_keys=True) + str(proof)  # 池子数据+nounce组成的字符串
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        return guess_hash[:5] == '00000'  # 难度值为5

    @staticmethod
    def get_merkle_root(transaction):  # 获得merkle tree根节点
        # 0个叶子
        if len(transaction) == 0:
            return hashlib.sha256(json.dumps(transaction, sort_keys=True).encode()).hexdigest()
        listoftransaction = transaction.copy()  # 复制变量，值传递
        # 有序排序
        for i in range(0, len(listoftransaction)):
            listoftransaction[i] = json.dumps(listoftransaction[i], sort_keys=True)
        # 若叶子为奇数，复制一份最后的叶子
        if len(listoftransaction) % 2 != 0:
            listoftransaction.append(listoftransaction[-1])
        while 1:  # 建树
            temp_transaction = []
            for index in range(0, len(listoftransaction), 2):  # 两叶一组
                current = listoftransaction[index]  # 左叶
                if index + 1 != len(listoftransaction):
                    current_right = listoftransaction[index + 1]  # 右叶
                else:
                    current_right = ''
                current_hash = hashlib.sha256(current.encode())
                if current_right != '':
                    current_right_hash = hashlib.sha256(current_right.encode())
                if current_right != '':
                    temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())
                else:
                    temp_transaction.append(current_hash.hexdigest() + current_hash.hexdigest())
            listoftransaction = temp_transaction  # 树的下一层所需参数
            # 跳出条件 当前一层只有一个节点 表示已经到了根节点，建树完成
            if len(listoftransaction) == 1:
                break
        return hashlib.sha256(listoftransaction[-1].encode()).hexdigest()  # 返回根节点

    def register_node(self, address):  # 节点/端口/用户注册
        self.nodes.add(urlparse(address).netloc)
        # 数据库节点集更新
        self.db.set('nodes', str(self.nodes))

    def valid_chain(self, chain):  # 区块链验证
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):  # 链的长度大于1
            last_block_temp = last_block.copy()  # 区块信息复制
            last_block_temp.pop('hash')  # 剔除hash值
            block = chain[current_index]
            # 链是否有断裂检验
            if block['previous_hash'] != self.hash(last_block_temp):
                return False
            # 检查merkle root是否正确 即该区块交易数据有无被篡改
            if not self.get_merkle_root(block["transactions"]) == block["merkle_root"]:
                return False
            # 检查proof
            if not self.valid_proof(block["transactions"], block["proof"]):
                return False
            # 下一对区块
            last_block = block
            current_index = current_index + 1
        return True

    def resolve_conflicts(self):  # 共识算法 只承认一条最长的链，所有节点只有一个共同的交易池
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)
        # 遍历所有网络中的节点
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')  # 获得目标节点的区块链数据
            response_pool = requests.get(f'http://{node}/pool')  # 获得目标节点的交易池数据
            if response.status_code == 200:
                length = response.json()['length']  # 目标节点区块链长度
                chain = response.json()['chain']  # 目标节点区块链数据
                pool = response_pool.json()['pool']  # 目标节点交易池数据
                if length >= max_length and self.valid_chain(chain):  # 只有对方的区块链长度大于等于我的时候，才需要共识
                    if length > max_length:  # 有比我更长的区块链
                        max_length = length
                        new_chain = chain  # 用它的链
                        self.current_transactions = pool  # 用它的交易池
                        self.db.set('ct', json.dumps(self.current_transactions, sort_keys=True))
                    elif length == max_length and len(self.current_transactions) == 0:  # 有跟我一样长的区块链 并且我本身没有交易池数据
                        self.current_transactions = pool  # 用它的交易池
                        self.db.set('ct', json.dumps(self.current_transactions, sort_keys=True))
                    elif length == max_length and len(self.current_transactions) > 0:  # 有跟我一样长的区块链 并且我本身有交易池数据
                        # 合并双方的交易池
                        dict_temp = []
                        for t in pool:
                            for my_t in self.current_transactions:
                                if json.dumps(t, sort_keys=True) == json.dumps(my_t, sort_keys=True):
                                    continue
                                else:
                                    dict_temp.append(t)
                        for t in dict_temp:
                            self.current_transactions.append(t)
                        self.db.set('ct', json.dumps(self.current_transactions, sort_keys=True))
        #  区块链发生更新
        if new_chain:
            self.chain = new_chain
            self.db.set('total', len(self.chain))
            # 数据库区块信息更新
            for block in self.chain:
                self.db.set(str(block['index']), json.dumps(block, sort_keys=True))
            return True
        # 区块链没有发生更新 但交易池可能有更新
        return False

    def inv(self):  # 告诉请求方自己本身的数据信息
        inv_values = []
        for b in self.chain:
            value_temp = {
                'type': 'block',
                'value': b['hash']
            }
            inv_values.append(value_temp)
        for t in self.current_transactions:
            value_temp = {
                'type': 'transaction',
                'value': t
            }
            inv_values.append(value_temp)
        return inv_values

    def getblocks(self):  # 向其它节点请求其数据信息
        neighbors = self.nodes
        hash_values = []
        for node in neighbors:
            if str(node).split(":")[1] == str(self.port):  # 不需要自己找自己要数据信息
                continue
            response = requests.get(f'http://{node}/inv')
            if response.status_code == 200:
                hash_value = {
                    'node': node,
                    'values': response.json()['values']
                }
                hash_values.append(hash_value)
        return hash_values


# 初始化节点
app = Flask(__name__)


def launchbc(porttemp):  # 启动
    global blockchain
    blockchain = Blockchain(porttemp)


@app.route('/restart', methods=['GET'])  # 路由：重置自己的区块链
def restart():
    message = blockchain.restart()
    response = {
        'message': message,
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])  # 路由：挖矿
def mine():
    ct = blockchain.current_transactions
    proof = blockchain.proof_of_work(ct)  # 挖矿进行
    block = blockchain.new_block(proof)
    response = {
        'message': '挖掘新区块成功',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'merkle_root': block['merkle_root'],
        'previous_hash': block['previous_hash'],
        'timestamp': block['timestamp'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])  # 路由：新交易创建
def new_transactions():
    values = request.get_json()
    # 需要的参数
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):  # 参数不对
        return '参数错误', 400
    index = blockchain.new_transactions(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'该交易已添加到交易池，被挖掘后将会添加到区块{index}中'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])  # 路由：查看自己的区块链信息
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])  # 路由：节点/用户注册
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return '请先提供节点数据', 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': '新节点添加成功',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])  # 路由：共识
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': '区块链发生更新',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': '区块链没有发生更新',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/pool', methods=['GET'])  # 路由：查看自己的交易池信息数据
def cts():
    response = {
        'pool': blockchain.current_transactions,
        'pool_length': len(blockchain.current_transactions),
    }
    return jsonify(response), 200


@app.route('/getblocks', methods=['GET'])  # 路由：获取他人的信息数据
def othersblock():
    response = {
        'information:': blockchain.getblocks()
    }
    return jsonify(response), 200


@app.route('/inv', methods=['GET'])  # router: inform its information to other nodes
def getinv():
    response = {
        'values': blockchain.inv()
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port  # 获取登录者的端口号
    launchbc(port)  # 使用端口号启动对应区块链
    app.run(host='127.0.0.1', port=port)
