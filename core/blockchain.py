import hashlib
import json
from time import time
from django.conf import settings

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class A121Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4  # Número de zeros iniciais necessários no hash
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return None

        new_block = Block(
            len(self.chain),
            self.pending_transactions,
            time(),
            self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def get_balance(self, user_id):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction['sender'] == user_id:
                    balance -= transaction['amount']
                if transaction['receiver'] == user_id:
                    balance += transaction['amount']
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True