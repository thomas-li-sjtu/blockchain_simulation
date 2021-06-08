import blockchain
import threading
import random
import time

num_miners = 20  # 矿工数目
miner_chain = {index: blockchain.BlockChain()
               for index, _ in enumerate(range(num_miners))}
possibility = 0.01  # 每次挖矿成功率
interval = 1 / possibility

pub_chain = blockchain.BlockChain()  # 公共的链
adv_chain = blockchain.BlockChain()  # 分叉攻击的链

increase_rate = []  # 增长率
throughput = []  # 吞吐量


def miner(miner_id: int):  # 诚实节点挖矿行为
    private_chain = blockchain.BlockChain()
    blockchain.copy_chain(pub_chain, private_chain)  # 更新信息
    rand_int = random.randint(0, 100000000)
    if rand_int % interval == 1:  # 挖到
        private_chain.add(miner_id)
        # print("miner: {} generate block # {}".format(miner_id, private_chain.get_head()))
    blockchain.copy_chain(private_chain, miner_chain[miner_id])  # 计入当前miner的链


def adversary(adv_id: int):  # 恶意节点挖矿行为
    private_chain = blockchain.BlockChain()
    blockchain.copy_chain(adv_chain, private_chain)  # 更新信息
    rand_int = random.randint(0, 100000)
    if rand_int % interval == 1:  # 挖到
        private_chain.add(adv_id)
        # print("adv miner: {} generate adv block # {}".format(adv_id, private_chain.get_head()))
    blockchain.copy_chain(private_chain, miner_chain[adv_id])  # 计入当前miner的链


def normal_maxChain(miner_chains: dict):  # 正常情况下计算最长链
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


def attack_maxChain(miner_chains: dict, attack_num: int):  # 分叉攻击情况下计算最长链
    max_chain, attack_max_chain = blockchain.BlockChain(), blockchain.BlockChain()
    blockchain.copy_chain(miner_chains[attack_num], max_chain)
    blockchain.copy_chain(miner_chains[0], attack_max_chain)
    more_found = False
    attack_more_found = False
    for key, chain in miner_chains.items():
        if key < attack_num:  # 查找攻击节点最长的链，返回给pub_chain
            if attack_max_chain.get_height() < chain.get_height() and chain.verify():
                blockchain.copy_chain(chain, attack_max_chain)
                attack_more_found = True
                continue
            if attack_max_chain.get_height() == chain.get_height():  # 上一轮有两个miner同时挖到，取hash小的
                if attack_more_found and chain.verify() and \
                        attack_max_chain.get_head_hash() > chain.get_head_hash():
                    blockchain.copy_chain(chain, attack_max_chain)
        else:  # 查找诚实节点最长的链，返回给pub_chain
            if max_chain.get_height() < chain.get_height() and chain.verify():
                blockchain.copy_chain(chain, max_chain)
                more_found = True
                continue
            if max_chain.get_height() == chain.get_height():  # 上一轮有两个miner同时挖到，取hash小的
                if more_found and chain.verify() and \
                        max_chain.get_head_hash() > chain.get_head_hash():
                    blockchain.copy_chain(chain, max_chain)

    blockchain.copy_chain(attack_max_chain, adv_chain)
    blockchain.copy_chain(max_chain, pub_chain)


def normal():  # 正常挖矿模拟
    total_round = 1
    threads = [0]*num_miners

    while pub_chain.get_height() < 20:
        # print("round: {}".format(total_round))
        normal_maxChain(miner_chain)
        # print("height of public chain: {}".format(pub_chain.get_height()))

        for i in range(num_miners):
            threads[i] = threading.Thread(target=miner, args=(i,))
        for i in threads:
            i.start()
            i.join()

        time.sleep(1)
        total_round += 1

        # 吞吐量计算
        # throughput.append(round(sum([chain.get_height() for key, chain in miner_chain.items()])/total_round, 4))
        # print('round: {}, throughput: {}'.format(total_round, throughput[-1]))
        # 增长速度计算
        increase_rate.append(round(pub_chain.get_height()/total_round, 4))
    print('round: {}, increase rate: {}'.format(total_round, increase_rate[-1]))



def adv():  # 含恶意挖矿模拟
    total_round = 1
    attack_num = 5
    adv_rate = 0.4
    advers = int(num_miners * adv_rate)
    print(advers)
    # assert advers == attack_num
    threads = [0]*num_miners

    while pub_chain.get_height() < 5:
        print("round: {}".format(total_round))
        normal_maxChain(miner_chain)
        print("height of public chain: {}".format(pub_chain.get_height()))

        for i in range(num_miners):
            threads[i] = threading.Thread(target=miner, args=(i,))
        for i in threads:
            i.start()
            i.join()
        time.sleep(1)
        total_round += 1

    # 挖出第五个块后开始进行分叉攻击，前advers个节点为恶意节点
    while adv_chain.get_height() < 5 + attack_num:
        print("round: {}".format(total_round))
        attack_maxChain(miner_chain, advers)
        for i in range(advers):
            threads[i] = threading.Thread(target=adversary, args=(i,))
        for i in range(advers, num_miners):
            threads[i] = threading.Thread(target=miner, args=(i,))

        for i in threads:
            i.start()
            i.join()
        time.sleep(1)
        total_round += 1
        print(adv_chain.get_height(), pub_chain.get_height())

    # 判断攻击是否成功
    if adv_chain.get_height() < pub_chain.get_height():
        print("Attack failed")
    elif adv_chain.get_height() > pub_chain.get_height():
        print("Attack succeeded")
    elif adv_chain.get_head_hash() < pub_chain.get_head_hash():
        print("Attack succeeded")
    else:
        print("Attack failed")
    print(adv_chain.block_chain)
    print(pub_chain.block_chain)


if __name__ == '__main__':
    # print(miner_chain)
    normal()
    # adv()

# 10, 0.01: [0.0893, 0.0649, 0.1429, 0.093, 0.1081]  0.09963
# 20, 0.01: [0.198, 0.202, 0.2326, 0.146, 0.2083]  0.19738
# 30, 0.01: [0.2299, 0.3279, 0.3509, 0.2532, 0.2299]  0.27836
# 40, 0.01: [0.3175, 0.303, 0.2985, 0.3571, 0.4444]  0.3440

# 20, 0.01: [0.198, 0.202, 0.2326, 0.146, 0.2083]  0.197380
# 20, 0.02: [0.3774, 0.4082, 0.2817, 0.2899, 0.339, 0.3125, 0.303]  0.33024
# 20, 0.025: [0.3922, 0.4, 0.556, 0.3922, 0.4255, 0.3704, 0.4444, 0.339]  0.4149
# 20, 0.04: [0.4878, 0.6667, 0.4545, 0.5128, 0.5128, 0.5714, 0.5714]  0.53962

# 10% 1 [105/1000]  0.105
# 10% 2 [37/1000]  0.037
# 10% 3 [7/1000]  0.007
# 10% 4 [3/1000]  0.003

# 20% 1 [(351-59)/1000]  0.292
# 20% 2 [71/500, 69/500]  0.142
# 20% 3 [9/300, 29/500]   0.058
# 20% 4 [14/300, 10/300, 9/300]  0.046

# 30% 1 [36]  0.36
# 30% 2 [23, 24]  0.235
# 30% 3 [17, 26, 15,]  0.193
# 30% 4 [16, 18, 21, 11, 18]  0.168

# 40% 1 [489]
# 40% 2 [42]
# 40% 3 [396(351)/1000]
# 40% 4 [346/1000]
