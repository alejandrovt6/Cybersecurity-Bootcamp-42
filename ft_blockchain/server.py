# Libraries
from ft_blockchain import Blockchain
from flask import Flask, jsonify, request

# Program
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "Mining a new Block"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "Adding a new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
