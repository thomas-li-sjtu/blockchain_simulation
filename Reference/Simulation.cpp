#include <iostream>
#include <functional>
#include <thread>
#include <stdlib.h>
#include <ctime>
#include <Windows.h>
#include "BlockChain.h"

using namespace std;

#define DEFAULT_NUM_OF_MINERS 20

BlockChain* minerChain = new BlockChain[DEFAULT_NUM_OF_MINERS];		// 每个矿工存放链备份
double possibility = 0.01;		// 每轮挖矿成功概率
int interval = 1 / possibility;
BlockChain publicChain;
BlockChain advChain;

void miner(int id);		// 诚实节点挖矿行为
void adversary(int id);		// 恶意节点挖抗行为
void maxChain(BlockChain *chain, int num, BlockChain &publicChain);		//计算最长链
/*--------------------------------------------------------------------------------
----------------------------------------------------------------------------------
--------------------------------------------------------------------------------*/


/*------------------------------------------------------------------------------*/
/*---------- part1: 无恶意攻击者的情况下，各节点都按照协议诚实挖矿 ----------*/
/*------------------------------------------------------------------------------*/
// /*
int main(int argc, char **argv)
{
	// static BlockChain publicChain;
	thread mthread[DEFAULT_NUM_OF_MINERS];
	int round = 1;
	
	while (publicChain.getHeight() < 20) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain, DEFAULT_NUM_OF_MINERS, publicChain);
		cout << "Height of the public chain: " << publicChain.getHeight() << endl;

		for (int i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}
		
		for (int k = 0; k < DEFAULT_NUM_OF_MINERS; k++) {
			mthread[k].join();
		}
		Sleep(1000);
		round++;
	}

	return 0;
}
// */


/*------------------------------------------------------------------------------*/
/*---------- part2: 有恶意节点进行分叉攻击 ----------*/
/*------------------------------------------------------------------------------*/
/*
int main(int argc, char **argv)
{
	thread mthread[DEFAULT_NUM_OF_MINERS];
	int round = 1;
	int attackNum = 5;
	double advRate = 0.4;
	int advers = DEFAULT_NUM_OF_MINERS * advRate;
	
	while (publicChain.getHeight() < 5) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain, DEFAULT_NUM_OF_MINERS, publicChain);

		for (int i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}

		for (int k = 0; k < DEFAULT_NUM_OF_MINERS; k++) {
			mthread[k].join();
		}
		Sleep(1000);
		round++;
	}

	// 从挖出第五个块后开始进行分叉攻击，前advers个节点为恶意节点
	while (advChain.getHeight() < 5 + attackNum) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain + advers, DEFAULT_NUM_OF_MINERS - advers, publicChain);
		maxChain(minerChain, advers, advChain);

		int i = 0;
		for (i = 0; i < advers; i++) {
			mthread[i] = thread(adversary, i + 1);
		}
		for (i = advers; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}

		for (i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i].join();
		}
		Sleep(1000);
		round++;
	}
	// 判断攻击是否成功
	if (advChain.getHeight() < publicChain.getHeight())
		cout << "Attack failed, 000" << endl;
	else if (advChain.getHeight() > publicChain.getHeight()) {
		cout << "Attack succeeded, 111" << endl;
	}
	else if (advChain.getHeadHash() < publicChain.getHeadHash()) {
		cout << "Attack succeeded, 111" << endl;
	}
	else cout << "Attack failed, 000" << endl;

	return 0;
}
*/


/*------------------------------------------------------------------------------*/
/*---------- part3: 有恶意节点进行自私挖矿 ----------*/
/*------------------------------------------------------------------------------*/
/*
int main(int argc, char **argv)
{
	thread mthread[DEFAULT_NUM_OF_MINERS];
	int round = 1;
	int attackNum = 5;
	double advRate = 0.4;
	int advers = DEFAULT_NUM_OF_MINERS * advRate;

	while (publicChain.getHeight() < 5) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain, DEFAULT_NUM_OF_MINERS, publicChain);

		for (int i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}

		for (int k = 0; k < DEFAULT_NUM_OF_MINERS; k++) {
			mthread[k].join();
		}
		Sleep(1000);
		round++;
	}

	// 从挖出第五个块后开始进行自私挖矿，前advers个节点为恶意节点
	// 坏人节点先与主链同步，直到取得优势
	while (advChain.getHeight() <= publicChain.getHeight()) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain + advers, DEFAULT_NUM_OF_MINERS - advers, publicChain);
		maxChain(minerChain, DEFAULT_NUM_OF_MINERS, advChain);

		int i = 0;
		for (i = 0; i < advers; i++) {
			mthread[i] = thread(adversary, i + 1);
		}
		for (i = advers; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}

		for (i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i].join();
		}
		Sleep(1000);
		round++;
	}
	int attackHeight = publicChain.getHeight();
	
	// 坏人节点不再与好人节点同步区块
	// 当有任意节点再挖出一个块后停止，比较好人与坏人链的长度，分析自私挖矿收益
	while (publicChain.getHeight() < attackHeight + 1 || advChain.getHeight() < attackHeight + 2) {
		cout << endl << "round " << round << endl;
		maxChain(minerChain + advers, DEFAULT_NUM_OF_MINERS - advers, publicChain);
		maxChain(minerChain, advers, advChain);

		int i = 0;
		for (i = 0; i < advers; i++) {
			mthread[i] = thread(adversary, i + 1);
		}
		for (i = advers; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i] = thread(miner, i + 1);
		}

		for (i = 0; i < DEFAULT_NUM_OF_MINERS; i++) {
			mthread[i].join();
		}
		Sleep(1000);
		round++;
	}
	if (advChain.getHeight() == attackHeight + 2)
		cout << "收益： " << 2 << endl;
	else if (advChain.getHeadHash() < publicChain.getHeadHash())
		cout << "收益： " << 1 << endl;
	else 
		cout << "收益： " << 0 << endl;

	return 0;
}
*/


/*--------------------------------------------------------------------------------
----------------------------------------------------------------------------------
--------------------------------------------------------------------------------*/
void miner(int id) {
	BlockChain privateChain;
	copy(publicChain, privateChain);

	srand(id * (int)time(0));
	if (rand() % interval == 1) {
		privateChain.add(id);
		cout << "miner " << id << " generate block #" << myHash(privateChain.getHead()) << endl;
	}
	copy(privateChain, minerChain[id - 1]);

	return;
}

void adversary(int id) {
	BlockChain privateChain;
	copy(advChain, privateChain);

	srand(id * (int)time(0));
	if (rand() % interval == 1) {
		privateChain.add(id);
		cout << "miner " << id << " generate block #" << myHash(privateChain.getHead()) << endl;
	}
	copy(privateChain, minerChain[id - 1]);

	return;
}

void maxChain(BlockChain *chain, int num, BlockChain &publicChain) {
	BlockChain maxChain;
	bool changed = false;
	copy(chain[0], maxChain);

	for (int i = 1; i < num; i++) {
		if (maxChain.getHeight() < chain[i].getHeight() && chain[i].verify()) {
			copy(chain[i], maxChain);
			changed = true;
			continue;
		}
		
		if (maxChain.getHeight() == chain[i].getHeight()) {
			if (changed && chain[i].verify()) {
				if (maxChain.getHeadHash() > chain[i].getHeadHash() ) {
					copy(chain[i], maxChain);
					changed = true;
				}
			}
		}
	}
	copy(maxChain, publicChain);

	return;
}