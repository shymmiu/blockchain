"""
Basic Blockchain Implementation

This module provides a simple blockchain implementation with:
- Block class: Represents individual blocks in the chain
- Blockchain class: Manages the chain of blocks
- Proof of Work: Simple mining mechanism
"""

import hashlib
import json
import time
from typing import List, Optional, Dict, Any


class Block:
    """Represents a block in the blockchain."""
    
    def __init__(self, index: int, timestamp: float, data: Any, 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the SHA-256 hash of the block."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary representation."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, block_dict: Dict[str, Any]) -> 'Block':
        """Create a Block from a dictionary."""
        block = cls(
            index=block_dict["index"],
            timestamp=block_dict["timestamp"],
            data=block_dict["data"],
            previous_hash=block_dict["previous_hash"],
            nonce=block_dict["nonce"]
        )
        return block


class Blockchain:
    """Manages a chain of blocks."""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_data: List[Any] = []
        self._create_genesis_block()
    
    def _create_genesis_block(self) -> None:
        """Create the first block in the chain."""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data="Genesis Block",
            previous_hash="0"
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]
    
    def add_data(self, data: Any) -> None:
        """Add data to pending list for next block."""
        self.pending_data.append(data)
    
    def mine_pending_data(self) -> Optional[Block]:
        """Mine a new block with pending data."""
        if not self.pending_data:
            return None
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=self.pending_data.copy(),
            previous_hash=self.get_latest_block().hash
        )
        
        new_block = self._proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_data = []
        return new_block
    
    def _proof_of_work(self, block: Block) -> Block:
        """Perform proof of work to mine a block."""
        target = "0" * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_chain_data(self) -> List[Dict[str, Any]]:
        """Get the entire chain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]
    
    def replace_chain(self, new_chain_data: List[Dict[str, Any]]) -> bool:
        """Replace the chain if the new one is longer and valid."""
        new_chain = []
        for block_data in new_chain_data:
            new_chain.append(Block.from_dict(block_data))
        
        # Validate the new chain
        temp_blockchain = Blockchain(self.difficulty)
        temp_blockchain.chain = new_chain
        
        if len(new_chain) > len(self.chain) and temp_blockchain.is_chain_valid():
            self.chain = new_chain
            return True
        return False
    
    def __len__(self) -> int:
        return len(self.chain)
    
    def __str__(self) -> str:
        return json.dumps(self.get_chain_data(), indent=2)


if __name__ == "__main__":
    # Demo usage
    print("Creating blockchain...")
    bc = Blockchain(difficulty=2)
    
    print("\nAdding transactions...")
    bc.add_data({"from": "Alice", "to": "Bob", "amount": 50})
    bc.add_data({"from": "Bob", "to": "Charlie", "amount": 25})
    
    print("Mining block 1...")
    bc.mine_pending_data()
    
    bc.add_data({"from": "Charlie", "to": "Alice", "amount": 10})
    
    print("Mining block 2...")
    bc.mine_pending_data()
    
    print("\nBlockchain:")
    print(bc)
    
    print(f"\nBlockchain valid: {bc.is_chain_valid()}")
    print(f"Chain length: {len(bc)}")
