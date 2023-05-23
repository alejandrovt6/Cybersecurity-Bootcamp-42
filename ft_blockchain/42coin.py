import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Creating a block chain
class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.transactions = []
        self.create_block(proof= 1 , previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block={'index' : len(self.chain) + 1,
                'timestamp' : str(datetime.datetime.now()),
                'proof' : proof,
                'previous_hash' : previous_hash,
                'transactions' : self.transactions}

        self.transactions = []
        self.chain.append(block)
        
        return block
    
    def get_previous_block(self):
        
        return self.chain[-1]
    
    # Our proof of work for mining the block
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        
        # Create a hash
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof =  True
            else:
                new_proof +=1
                
        return new_proof
            
    # Hashing 
    def hash(self,block):
        
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Checking if a block is valid or not
    def is_chain_valid(self, block):
        
        previous_block = self.chain[0]
        block_index=1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            
            # Check if the prev hash in current block does not match with the original hash of the prev block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Check if the resultant hash of the proof**2 - previous_proof**2 does not have 4 leading 0s
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] !='0000':
                return False
            
            # Update the block and increase the index
            previous_block=block
            block_index +=1
        return True

    # Add transactions
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender' : sender,
                           'receiver' : receiver,
                           'amount' : amount})
        previous_block = self.get_previous_block()

        return previous_block['index'] + 1
    
    # Adding the node
    def add_node(self,address):
        # parsed_url = urlparse('http://127.0.0.1:5000/')
        # parsed_url.netloc - '127.0.0.1:5000'
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    # Replacing the chain with the longest chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        # max_length is set to the current length
        max_length = len(self.chain)
        # go through all of the nodes and see all of their chains
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            
            # if chain is valid
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
# Creating a web app
app = Flask(__name__)


# Creating an address for the node on the port 5000
# uuid4() creates a random universally unique identifier (UUID - generated using synchronization methods that ensure no two processes can obtain the same UUID)
node_address = str(uuid4()).replace('-', '')

# Creating a blockchain
blockchain=Blockchain()

# Mining a block
@app.route('/mine_block', methods = ['GET'])
def mine_block():

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Alejandro', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    
    # Return the response
    response = {'message' : 'Congrats, you just mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}
    # Response with the JSON representation of the given arguments with an application/json mimetype(Multipurpose Internet Mail Extensions or MIME type).
    return jsonify(response), 200
    
# Getting the blockchain
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    
    # Return the response
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200
    
# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'We have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():

    json = request.get_json()

    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        
        return 'Some elements of the transactions are missing', 400

    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message' : f'This transaction will be added to the Block {index}'}
    
    return jsonify(response), 201

# Decentralizing our blockchain

#Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    # Connecting all of the others nodes manually 
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        
        return 'No node', 400

    # Our nodes is a set so even if it is done for all the nodes seperately it will contain only unique values
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'All the nodes are now connected. The 42coin blockchain now contains the node',
                'total_nodes' : list(blockchain.nodes)}
    # HTTP 201 created
    return jsonify(response), 201

# Replacing the chain by the longest chain
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes are different so the chain is replaced by the longest chain.',
                    'new_chain' : blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one',
                    'new_chain' : blockchain.chain}
        
    return jsonify(response), 200

# Running the app on the port
app.run(host = '0.0.0.0', port = 5000)