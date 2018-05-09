import datetime
import hashlib
from P2P import Order

# everytime a match happens, a new contract is added to the contract list
# everytime a price update happens, margin calculation and transfer of funds is calculated for each contract
class Contract:
    def __init__(self, contractId, buyerId, sellerId, volume):
        self.contractId = contractId
        self.buyerId = buyerId
        self.sellerId = sellerId
        self.volume = volume
    def __str__(self):
        return "["+str(self.contractId)+", "+str(self.buyerId) +", "+str(self.sellerId)+", "+str(self.volume)+"]"

class Block:
    blockNo = 0
    contract = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, contract):
        self.contract = contract
        # self.hash = self.hash()s

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.contract).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock contract: " + str(self.contract) + "\nHashes: " + str(self.nonce) + "\n--------------"

class Blockchain:
    #stores all the matching orders and mines block whenever price changes
    contractList = []

    # to make it hard to mine, increase diff!
    diff = 1
    maxNonce = 2**32
    target = 2 ** (256-diff)
    size = 1
    block = Block(Contract(-1, -1, -1, -1))
    dummy = head = block

    def add(self, block):

        # block.hash = block.hash() ###########
        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                self.size += 1
                #print(block)
                break
            else:
                block.nonce += 1
    # def __str__(self):
    #     dummmy = temp = self.head
    #     while temp != None:
    #         return temp.__str__()
    #         temp = temp.next
    def validateBlockchain(self):
        valid = 1
        dummmy = prev = self.head
        curr = prev.next
        while curr!=None:
            # print("curr.prev hash: "+ str(curr.previous_hash) + ', prev.hash: '+ str(prev.hash()))
            if curr.previous_hash != prev.hash():
                valid = 0
            prev = curr
            curr = curr.next

        if valid == 0:
            print("Blockchain is INVALID")
        else:
            print("Blockchain is VALID")

    def printBlockchain(self):
        dummmy = temp = self.head
        while temp != None:
            print(temp)
            temp = temp.next
        self.validateBlockchain()


    #
    # ################################ TODO #########################
    # #need a change in price to calculate the money transfer
    # def updateAndValidate(self, del_price):
    #     #if del_price is +ve, check for every buyer, else for every seller
    #     #if any contract has margin below threshold, (remove contract?) and return the id of buyer and seller to inform closure of contract
    #     #start with a fixed initial virtual margin.
    #     # for each client involved:
    #         # for each contract, update buyer and seller margin account balance, with respect to the latest price
    #         # if the balance is below a threshold, indicate contract termination.
    #
    #     if float(del_price) >= 0:
    #         for contract in self.contractList:
    #             buyerId = contract.buyerId
    #
    #             curr = self.head
    #             while curr:
    #                 if curr.contract.fromId == buyerId :
    #                     curr = curr.next




if __name__ == "__main__":
    blockchain = Blockchain()

    for n in range(10):
        blockchain.mine(Block("Block " + str(n+1)))

    while blockchain.head != None:
        print(blockchain.head)
        blockchain.head = blockchain.head.next
