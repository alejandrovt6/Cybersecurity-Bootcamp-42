# 💲 Blockchain ⛓️
## 📝 Description
The workflow is to add different transactions to the current block and mine the block to append it to the chain.

The proof-of-work algorithm should be simple, for example, finding the number that, when concatenated with the previous proof of work, results in a SHA-256 hash ending in 4242. The blockchain will not be persistent and will be stored in the server's memory, without being connected to any specific database software. When developing the mining process, three things should be done:

- Calculate the proof of work
- Reward the miners (one transaction)
- Create the new block and add it to the chain

Once the blockchain is created, it can be interacted with through different HTTP requests:

- [POST] /transactions/new: Sends a new transaction to be added to the next block.
- [GET] /mine: Executes the proof-of-work algorithm and creates a new block.
- [GET] /chain: Returns information about the blockchain (blocks, transactions, etc.).

## 🔍 Requirements
* Python 3.x or later
* hashlib library
  
In creation ...
## 🛠️ Usage

## 💡 Examples