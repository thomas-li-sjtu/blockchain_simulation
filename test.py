from utils import *
import ctypes

chain_a = BlockChain()
chain_b = BlockChain()

chain_a.add(1)

chain_a.add(2)

chain_a.add(3)

print(chain_a.block_chain)
print(ctypes.cast(chain_a.block_chain[1]['block_ahead'], ctypes.py_object).value)
print(chain_a.verify())
print(copy_chain(chain_a, chain_b).block_chain)
print(copy_chain(chain_a, chain_b).verify())
