import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Press the green button in the gutter to run the script.

class Blockchain:
    def __init__(self):
        self.chain = []
        # Add transactions and nodes
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        
    # Adress: direction and port
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)
    def replace_chain(self):
        # We will define as network the set of nodes that we have obtained
        network = self.nodes
        print(len(network))
        # We give the value of None to the variable longest_chain
        longest_chain = None
        # We define the maximum length of our chain of blocks
        max_length = len(self.chain)
        # We go through  all the nodes
        print(max_length)

        for node in network:
            response = requests.get(f'http://{node}/chain')
            
            print(node)
            print(response.status_code)       
            json_obj = response.json()

            if isinstance(json_obj,dict):
                print("hey")

                if "length" in json_obj:
                    print(json_obj["length"])

                if "chain" in json_obj:
                    print(json_obj["chain"])
                
            if response.status_code == 200:
                
                length = json_obj["length"]
                print(length)
                
                chain = json_obj["chain"]
                print(chain)
                # In case of the maximun length is more than maxlenght and is valid
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

            if longest_chain:
                self.chain =longest_chain
                return True
            return False
            
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'transactions':self.transactions}

        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        
        previous_block = self.get_previous_block()

        return previous_block['index']+1

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation.endswith('4242'):  
                hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                check_proof = True
            else:
                new_proof +=1            
        return new_proof
        
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
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
            
            if not hash_operation.endswith('4242'):
                return False

            # Update the block and increase the index
            previous_block=block
            block_index +=1
        return True
   
app = Flask(__name__)

node_address = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_work(previous_proof)
    
    previous_hash = blockchain.hash(previous_block)
    # Now we are going to add one more key to the dictionary of our blockchain
    # that will have our transtactions 
    blockchain.add_transaction(sender= node_address, receiver='Ismael', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Congrats, you have mined a block!',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}
    
    print(len(blockchain.nodes))

    for node in blockchain.nodes:
        print(type(node))
        requests.get(url=f'http://{node}/replace_chain')    
    return jsonify(response), 200

# Method get for obtain the chain
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

# Check the validity of the chain of blocks
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'All right. Blockchain is valid.'}
    else:
        response = {'message':'Something went wrong. Blockchain is not valid.'}
    return jsonify(response), 200

# Add a new transaction to blockchain.
@app.route('/transactions/new', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    
    if not all (key in json for key in transaction_keys):
        return 'Some elements are missing', 400
        
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'The transaction will be added to the block {index}'}
    return jsonify(response), 201

# Connect new nodes
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    print(nodes)
    # Check the nodes are not empty

    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.add_nodes(node)
    response = {'message':'The connection of the nodes is established.','total_nodes':list(blockchain.nodes)}
    return jsonify(response), 201 

# Replace the current string with the longest
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    print(is_chain_replaced)

    if is_chain_replaced:
        response = {'message':'The nodes had diferents chains so the chain was replaced by the longest one',
                    'new_chain':blockchain.chain}
    else:
        response = {'message':'Everything is ok. The chain is the longest one',
                    'actual_chain':blockchain.chain}
        
    return jsonify(response), 200
app.run(host='0.0.0.0', port='5003',debug=True)