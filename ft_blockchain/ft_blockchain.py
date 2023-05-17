# This program is not finished
# Libraries
import hashlib

# Program
class GeekCoinBlock:
    # Constructor
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        # Concatenate transactions and previous hash
        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}"
        # self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.block_hash = None

    def mine_block(self, difficulty):
        nonce = 0
        # Difficulty test work
        prefix = "0" * difficulty # Must be 4242
        while True:
            # Calculate block_data hash
            block_data = f"{self.block_data}-{nonce}"
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            # Verify difficulty
            if block_hash[:difficulty] == prefix:
            # if block_hash[:difficulty] == "0" * difficulty and block_hash[-2:] == prefix:
                self.block_hash = block_hash
                break
            nonce += 1

class Blockchain:
    # Constructor
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    # Genesis block (the first)
    def generate_genesis_block(self):
        # Previous is 0. Add this
        self.chain.append(GeekCoinBlock("0", ['Genesis Block'])) 
    # Create blocks

    def create_block_from_transaction(self, transaction_list, difficulty):
        # Obtain previus block
        previous_block_hash = self.last_block.block_hash
        # Create new block
        block = GeekCoinBlock(previous_block_hash, transaction_list)
        block.mine_block(difficulty)
        self.chain.append(block)

    # Display blockchain information
    def display_chain(self):
        for i, block in enumerate(self.chain):
            print(f"Data {i + 1}: {block.block_data}")
            print(f"Hash {i + 1}: {block.block_hash}\n")
            
    # It is a property, not a method. Return last chain
    @property
    def last_block(self):
        return self.chain[-1]

# Create transactions
t1 = "George sends 3.1 42coin to Joe"
t2 = "Joe sends 2.5 42coin to Adam"
t3 = "Adam sends 1.2 42coin to Bob"
t4 = "Bob sends 0.5 42coin to Charlie"
t5 = "Charlie sends 0.2 42coin to David"
t6 = "David sends 0.1 42coin to Eric"

# Create instance
myblockchain = Blockchain()

# Create blocks
myblockchain.create_block_from_transaction([t1, t2], 4)  # Work test lvl 4
myblockchain.create_block_from_transaction([t3, t4], 4)
myblockchain.create_block_from_transaction([t5, t6], 4)

# Display blockchain
myblockchain.display_chain()
