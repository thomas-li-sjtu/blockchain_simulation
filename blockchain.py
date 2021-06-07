import copy
import ctypes


block = {
    'hash_code': 00000000,  # 前一个block的hash（hash()的返回值为int）
    'id': 0,  # 该区块提供者的ID
    'height': 0,  # 该块所在的高度
    'block_ahead': None  # 上一个block地址
}
# block = copy.deepcopy(block)  深拷贝
# value = {'id': 'Helloworld'}  # 定义一个字符串变量
# address = id(value)  # 获取value的地址，赋给address
# get_value = ctypes.cast(address, ctypes.py_object).value  # 读取地址中的变量
# print(get_value)


def block_hash(tmp_block: dict):  # 计算当前block的hash
    hash_res = hash(str(tmp_block['hash_code'])) \
               ^ hash(str(tmp_block['id']*100)) \
               ^ hash(str(tmp_block['height']))
    return hash(str(hash_res))


class BlockChain:
    def __init__(self):
        self.start = copy.deepcopy(block)  # 头节点
        self.block_chain = [self.start]
        self.height = 0

    def get_head(self):  # 获取区块链头部的block，即最新的block
        # 可能不太对
        return self.block_chain[-1]

    def get_head_hash(self):  # 获取区块链最新块的hash值
        return block_hash(self.block_chain[-1])

    def get_height(self):  # 获取区块链的长度
        return self.height

    def clear(self):  # 清空区块链，只剩起始块
        self.block_chain.clear()
        self.block_chain = [self.start]
        self.height = 0

    def add(self, blockid: int):  # 矿工挖出一个block，链增长
        self.height += 1
        hash_tmp = block_hash(self.block_chain[-1])
        tmp_block = copy.deepcopy(block)
        address = id(self.block_chain[-1])

        tmp_block['id'] = blockid
        tmp_block['hash_code'] = hash_tmp
        tmp_block['height'] = self.height
        tmp_block['block_ahead'] = address  # 存储前一个块的地址
        self.block_chain.append(tmp_block)

    def verify(self):  # 验证该区块链是否符合要求(从后往前验证)
        tmp_block = self.block_chain[-1]

        while tmp_block['block_ahead']:
            # 计算当前块的 hash_code 是否等于前一个块的哈希
            isValid = (tmp_block['hash_code'] ==
                       block_hash(ctypes.cast(tmp_block['block_ahead'], ctypes.py_object).value))
            if not isValid:
                return False
            tmp_block = ctypes.cast(tmp_block['block_ahead'], ctypes.py_object).value
        return True


def copy_chain(chain_A: BlockChain, chain_B: BlockChain):  # 复制区块链A到区块链B
    chain_B.clear()
    chain_B.height = chain_A.height

    # 深拷贝
    for index, block_a in enumerate(chain_A.block_chain):
        if index == 0:
            continue
        tmp_block = copy.deepcopy(block_a)
        chain_B.block_chain.append(tmp_block)
        if index != 0:
            chain_B.block_chain[-1]['block_ahead'] = id(chain_B.block_chain[-2])

    return chain_B
