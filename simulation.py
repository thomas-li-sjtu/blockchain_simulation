import blockchain
import threading
import random
import time

num_miners = 5  # 矿工数目
miner_chain = {index: blockchain.BlockChain()
               for index, _ in enumerate(range(num_miners))}
possibility = 0.1  # 每次挖矿成功率
interval = 1 / possibility

pub_chain = blockchain.BlockChain()  # 公共的链
adv_chain = blockchain.BlockChain()  # 公共的链


def miner(miner_id: int):  # 诚实节点挖矿行为
    private_chain = blockchain.BlockChain()
    blockchain.copy_chain(pub_chain, private_chain)  # 更新信息
    rand_int = random.randint(0, 100000000)
    if rand_int % interval == 1:  # 挖到
        private_chain.add(miner_id)
        print("miner: {} generate block # {}".format(miner_id, private_chain.get_head()))
    blockchain.copy_chain(private_chain, miner_chain[miner_id])  # 计入当前miner的链


def adversary(adv_id: int):  # 恶意节点挖抗行为
    pass


def maxChain(miner_chains: dict, num: int):  # 计算最长链
    max_chain = blockchain.BlockChain()
    blockchain.copy_chain(miner_chains[0], max_chain)

    more_found = False
    for key, chain in miner_chains.items():  # 查找最长的链，返回给pub_chain
        if max_chain.get_height() < chain.get_height() and chain.verify():
            blockchain.copy_chain(chain, max_chain)
            more_found = True
            continue

        if max_chain.get_height() == chain.get_height():  # 上一轮有两个miner同时挖到，取hash小的
            if more_found and chain.verify() and \
                    max_chain.get_head_hash() > chain.get_head_hash():
                blockchain.copy_chain(chain, max_chain)
    blockchain.copy_chain(max_chain, pub_chain)


def normal():  # 正常挖矿模拟
    total_round = 1
    threads = [0]*num_miners

    while pub_chain.get_height() < 20:
        print("round: {}".format(total_round))
        maxChain(miner_chain, num_miners)
        print("height of public chain: {}".format(pub_chain.get_height()))

        for i in range(num_miners):
            threads[i] = threading.Thread(target=miner, args=(i,))
        for i in threads:
            i.start()
            i.join()

        time.sleep(1)
        total_round += 1

        # 增长速度


def adv():  # 含恶意挖矿模拟
    pass


if __name__ == '__main__':
    # print(miner_chain)
    normal()
