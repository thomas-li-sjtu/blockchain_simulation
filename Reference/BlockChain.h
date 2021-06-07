#pragma once

struct Block
{
	size_t hashCode;	// 前一个block的hash
	int ID;		// 该区块提供者的ID
	int level;	// 该块所在的高度
	Block* next;

	Block(size_t h, int id, int l, Block* n)
		:hashCode(h), ID(id), level(l), next(n) {}
	Block() { hashCode = 00000000; ID = 0; level = 0; next = nullptr; }
};

size_t myHash(Block block);

class BlockChain
{
	friend void copy(const BlockChain &chainA, BlockChain &chainB);

private:
	Block* head;
	int height;

public:
	BlockChain();
	~BlockChain();
	void add(int id);	// 矿工挖出一个block，链增长
	bool verify() const;	// 验证该区块链是否符合要求
	Block& getHead() const;		// 获取区块链头部的block，即最新的block
	size_t getHeadHash() const;		// 获取区块链最新块的hash值
	int getHeight() const;	// 获取区块链的长度
	void clear();	// 清空区块链，只剩起始块
};