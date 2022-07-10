"""
Genesis
{
    index: 0,
    timestamp: 0,
    data: "",
    proof: 0,
    previous_hash: "0"
} -> hashfxn -> xxxxxx

1
{
    index: 1,
    timestamp: 1,
    data: "one",
    proof: 1,
    previous_hash: xxxxxx
} -> hashfxn -> yyyyyy

2
{
    index: 2,
    timestamp: 2,
    data: "two",
    proof: 2,
    previous_hash: yyyyyy
}

"""

import datetime as _datetime
import hashlib as _hashlib
import json as _json
import string

class Void:
    def __init__(self) -> None:
        self.chain = list()
        genesis = self._create_block(data="void", proof=1, previous_hash="void", index=1)
        self.chain.append(genesis)

    def mine(self, data: str) -> dict:
        previous_block = self.previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._work(previous_proof, index, data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(data=data, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block

    def _hash(self, block: dict) -> string: 
        encoded = _json.dumps(block, sort_keys=True, default=str).encode()
        return _hashlib.sha256(encoded).hexdigest()

    def previous_block(self) -> dict:
        return self.chain[-1]

    def _digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        digest = str(new_proof + previous_proof + index) + data
        return digest.encode()

    def _work(self, previous_proof: int, index: int, data: str) -> int:

        new_proof = 1
        check = False

        while not check:
            #print(new_proof)
            digest = self._digest(new_proof=new_proof, previous_proof=previous_proof, index=index, data=data)
            value = _hashlib.sha256(digest).hexdigest()

            if value[:3] == "000":
                check = True
            else: 
                new_proof += 1
        return new_proof

    def _create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": _datetime.datetime.now(),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash
        } 
        return block

    def real(self) -> bool:
        current_block = self.chain[0]
        block_index = current_block.get("index")
        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block["previous_hash"] != self._hash(block=current_block):
                return False
            current_proof = current_block["proof"]
            
            next_index, next_data, next_proof = (
                next_block["index"],
                next_block["data"],
                next_block["proof"]
            )
            hash_value = _hashlib.sha256(self._digest(new_proof=next_proof, previous_proof=current_proof, index=next_index, data=next_data)).hexdigest()
            if hash_value[:3] != "000":
                return False
            
            current_block = next_block
            block_index += 1

        return True


