import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Press the green button in the gutter to run the script.
# class Block
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
class Blockchain:
    def __init__(self):
        self.chain = []
        # Primero se agregan las transacciones para crear el blockchain
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        #  En segundo lugar agregamos los nodos
        self.nodes = set()
     
    # address va a ser la direccion y el puerto de nuestro nodo
    def add_nodes(self, address):
        # Mediante el analizador de urls de la libreria urllib comprobamos que
        # el address es correcto
        parsed_url = urlparse(address)
        # Seguidamente lo adjuntamos a nuestro conjunto nodes mediante .add()
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)
    def replace_chain(self):
        # Definiremos como network al conjunto de nodos que hemos obtenido 
        # al agregar los nodos
        network = self.nodes
        print(len(network))
        # Damos el valor de None a la variable longest_chain porque aun no hemos
        # comprobado ni analizados la longitud de cadena de bloques de cada nodo
        longest_chain = None
        # A continuacion definimos la longitud maxima de nuestra cadena de bloques
        max_length = len(self.chain)
        # Mediante el bucle for dentro de nuestra network recorremos todos los nodos
        print(max_length)
        for node in network:
            # Mandaremos una solicitud de estado de la siguiente manera
            response = requests.get(f'http://{node}/chain')
            
            print(node)
            print(response.status_code)
            # print(response.json(['length']))
            json_obj = response.json()
            if isinstance(json_obj,dict):
                print("hey")
                if "length" in json_obj:
                    print(json_obj["length"])
                if "chain" in json_obj:
                    print(json_obj["chain"])
                # for key in response.json:
                
            # print(response.json(['chain']))
            # En caso de que obtendramos un estado 200 seguiremos en buen camino
            if response.status_code == 200:
                # Response es un tipo json en el cual vamos a buscar los valores
                # longitud y cadena para comprobar cual es el mas largo y asi
                # despues reemplezar en todos los nodos con el predominante
                
                length = json_obj["length"]
                print(length)
                
                chain = json_obj["chain"]
                print(chain)
                # En caso de que la longitud(length) sea mayor que maxlength
                # Y que la cadena sea valida
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            # En caso de que la cadena larga tenga un valor
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
        # regresamos esta lista a estar vacia para que no haya duplicados
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        
        # Con esto agarramos el indice del bloque anterior
        previous_block = self.get_previous_block()
        
        return previous_block['index']+1

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # print(hash_operation)
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
            
            # check if the prev hash in current block does not match with the original hash of the prev block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Check if the resultant hash of the proof**2 - previous_proof**2 does not have 4 leading 0s
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if not hash_operation.endswith('4242'):
                return False
            
            # update the block and increase the index
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
    # Ahora vamos a agregar una llave mas al diccionario de nuestro blockchain 
    # que va a tener nuestras transacciones
    blockchain.add_transaction(sender= node_address, receiver='Is', amount=1)
    # 
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Felicidades, has minado un bloque!',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}
    # for node in blockchain.nodes:
    #     print(node)
    # is_chain_replaced = blockchain.replace_chain()
    # print(is_chain_replaced)
    # if is_chain_replaced:
    #     response3 = {'message':'The nodes had diferents chains so the chain was replaced by the longest one',
    #                 'new_chain':blockchain.chain}
    # else:
    #     response3 = {'message':'Everything is ok. The chain is the longest one',
    #                 'actual_chain':blockchain.chain}
    print(len(blockchain.nodes))
    # requests.get(url=f'http://127.0.0.1:5002/replace_chain')
    # requests.get(url=f'http://127.0.0.1:5003/replace_chain')
    for node in blockchain.nodes:
        print(type(node))
        requests.get(url=f'http://{node}/replace_chain')    
    return jsonify(response), 200
@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200
# Chekeamos la validez de la cadena de bloques
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'Todo bien. El Blockchain es valido'}
    else:
        response = {'message':'Something went wrong. El Blockchain no es valido'}
    return jsonify(response), 200
# Agregaremos una nueva transaccion al blockchain.
@app.route('/transactions/new', methods = ['POST'])
def add_transaction():
    # Obtenemos el json de nuestra solicitud
    json = request.get_json()
    # Seguidamente mediante una lista predefinida(llave de transacciones)
    transaction_keys = ['sender','receiver','amount']
    # Vamos a parsear el json y obtendremos el sender, receiver y la cantidad(amount)
    
    if not all (key in json for key in transaction_keys):
        return 'Some elements are missing', 400
        
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'The transaction will be added to the block {index}'}
    return jsonify(response), 201
# Conectamos los nuevos nodos
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    print(nodes)
    # vamos a comprobar que nuestros nodos no esten vacios
    if nodes is None:
        return 'No node', 401
    for node in nodes:
        blockchain.add_nodes(node)
    response = {'message':'The connection of the nodes is established.','total_nodes':list(blockchain.nodes)}
    return jsonify(response), 201 
# Vamos a remplazar la cadena por la cadena mas larga que ya hemos obtenido
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
