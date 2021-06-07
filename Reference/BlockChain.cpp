#include "BlockChain.h"
#include <functional>

size_t myHash(Block block) {
	std::hash<size_t> sizet_hash;
	std::hash<int> int_hash;

	size_t hash_res = 
		sizet_hash(block.hashCode) ^ int_hash(block.ID * 100) ^ int_hash(block.level);
	hash_res = sizet_hash(hash_res);

	return hash_res;
}

BlockChain::BlockChain() { 
	head = new Block(00000000, 0, 0, nullptr);
	height = 0;
}

void BlockChain::add(int id) {
	height++;

	size_t hash_tmp = myHash(*head);
	Block* block_tmp;
	head = block_tmp = new Block(hash_tmp, id, height, head);
}

bool BlockChain::verify() const {
	Block* p = head;
	
	while (p->next != nullptr) {
		bool isValid = (p->hashCode == myHash(*p->next));
		if (!isValid) return false;
		p = p->next;
	}
	return true;
}

Block& BlockChain::getHead() const {
	return *head;
}

size_t BlockChain::getHeadHash() const {
	return myHash(*head);
}

int BlockChain::getHeight() const {
	return height;
}

void BlockChain::clear() {
	Block* p = head;

	while (p->next != nullptr) {
		head = head->next;
		delete p;
		p = head;
	}
	height = 0;
}

BlockChain::~BlockChain() {
	clear();
	delete head;
}

void copy(const BlockChain &chainA, BlockChain &chainB) {
	chainB.clear();
	chainB.height = chainA.height;

	Block* p = chainA.head;
	Block* block_tmp;
	if (p->next != nullptr) {
		chainB.head = block_tmp = new Block(p->hashCode, p->ID, p->level, chainB.head);
		p = p->next;
	}
	else return;
	
	Block* q = chainB.head;
	while (p->next != nullptr) {
		q->next = block_tmp = new Block(p->hashCode, p->ID, p->level, q->next);
		q = q->next;
		p = p->next;
	}
	return;
}