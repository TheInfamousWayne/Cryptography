# if the server disconnects, one of the clients becomes the server
# and every client that doesnot become the server will try to
# connect to the new server

import os
import socket
import threading
import sys
sys.path.append("D:\\Python Codes\\Cryptography\\New folder\\BlockChain.py")
from BlockChain import *
import time
from random import randint
import pickle
import pandas as pd
import numpy as np
import csv
from GUI import GUI
import datetime
import hashlib
import subprocess
import sys
import platform
from subprocess import Popen
#from BlockChain import *

I_AM_NEW = 1

class Constants:
    port = 10000
    buf_size = 65536
    #stores the client_ID with respect to a connection
    clientDictionary = {}

class P2P:
    peers = ['127.0.0.1']
    contracts = []
    blockchain = None
    connections = []



class Server:
    connections = []
    peers = []
    orders = []

    def guiFunction(self):
        proc = subprocess.call("start python ./GUI.py", shell=True)


####################### lolololol ##########################
    def save_contracts(self):
        for item in self.buy:
            idx = next((i for i,x in enumerate(self.sell) if x[2]==item[2]), None)
            if idx:
                idx2 = self.buy.index(item)
                #print("Indices: ", idx," ", idx2)
                # self.contracts.append([self.buy[idx2][0], self.sell[idx][0], self.sell[idx][1], self.sell[idx][2]])
                P2P.contracts.append([self.buy[idx2][0], self.sell[idx][0], self.sell[idx][1], self.sell[idx][2]])

                ################# todo ####################
                print('Started mining new block\n')
                P2P.blockchain.mine(Block(P2P.contracts[-1]))
                print('new block added, The current Blockchain is:\n\n')
                P2P.blockchain.printBlockchain()
                print('\n\t\t*****************\n')
                ##########################################

                del self.sell[idx]
                del self.buy[idx2]
                print("Present Contracts:-\n")
                for item in P2P.contracts:
                    print(item)
        #self.sendBlockchain()

    #sends the blockchain to all the nodes
    def sendBlockchain(self):
        blockchan_str = pickle.dumps(P2P.blockchain)
        for connection in P2P.connections:
            connection.sendall(b'\x15' + blockchan_str)
            # connection.sendall(b'\x15' + bytes("this is my temp blockchain", "utf-8"))
        print("sent blockchain to all connections")
        print("\nraw data sent =")
        print(blockchan_str)

#############oxooxxoxo#
    def sampleFunction(self):
        buy_msg = pd.read_csv("./buy_msg.csv", header=None)
        sell_msg = pd.read_csv("./sell_msg.csv", header=None)
        buy_msg = np.array(buy_msg)
        sell_msg = np.array(sell_msg)
        #####
        buy_cid_file, buy_price_file, buy_vol_file = zip(*buy_msg)
        sell_cid_file, sell_price_file, sell_vol_file = zip(*sell_msg)
        for a,b,c, i,j,k in zip(buy_cid_file, buy_price_file, buy_vol_file, sell_cid_file, sell_price_file, sell_vol_file):
            self.buy.append([a,b,c])
            self.sell.append([i,j,k])
            while not os.path.exists("./temp.csv"):
                with open('./temp.csv', 'w') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',')
                    filewriter.writerow([1,a,b,c])
                break
            time.sleep(2)
            while not os.path.exists("./temp.csv"):
                with open('./temp.csv', 'w') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',')
                    filewriter.writerow([2,i,j,k])
                break
            time.sleep(2)
        self.save_contracts()

    def __init__(self, IS_NEW):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buy = []
        self.sell = []
        self.contracts = []

        P2P.blockchain = Blockchain()

        sock.bind(('0.0.0.0', Constants.port))
        sock.listen(1)
        print('Server is running')
        if IS_NEW:
            guiThread = threading.Thread(target=self.guiFunction)
            guiThread.daemon = True
            guiThread.start()
            sample = threading.Thread(target=self.sampleFunction)
            sample.daemon = True
            sample.start()

        # SERVER SEND
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target = self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            P2P.connections.append(c)
            #a[0] has the ip address of the connection
            self.peers.append(a[0])
            # print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()


    # SERVER RECEIVE
    def handler(self, c, a):
        while True:
            try:
                data = c.recv(Constants.buf_size)
                if not data:
                    print(str(a[0]) + ':' + str(a[1]), "disconnected")
                    self.peers.remove(a[0])
                    c.close()
                    self.sendPeers()
                    break

                #client sends cid the server
                if data[0:1] == b'\x14':
                    # insert entry into dictionary
                    try:
                        str_connection = str(a[0]) + ":" + str(a[1])# pickle.dumps(c)  # str(pickle.dumps(c), "utf-8")
                        Constants.clientDictionary[str_connection] = str(data[1:], "utf-8")
                        print("updated dictionary is:\n")
                        print(Constants.clientDictionary)
                    except Exception as e:
                        print(e)

                #client sent an order object
                if data[0:1] == b'\x12':
                    order = pickle.loads(data[1:])
                    #print("received an order: ", data[1:])
                    #appended the order to the orders list
                    order.id = Constants.clientDictionary[str(a[0])+":"+str(a[1])]
                    sendThread = threading.Thread(target=self.sendOrder, args=(order,))
                    sendThread.daemon = True
                    sendThread.start()
                    self.orders.append(order)
                    #sends the list of all orders to all the peers in the network
                    self.sendOrders()
                    ############ todo remove this ##########
                    # print("new orders = ")
                    # for myOrder in self.orders:
                    #     myOrder.printOrder()

            except ConnectionResetError as e:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.peers.remove(a[0])
                P2P.connections.remove(c)##
                del Constants.clientDictionary[str(a[0]) + ":" + str(a[1])]##
                c.close()
                self.sendPeers()
                break
            except Exception as e:
                print(e)
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.peers.remove(a[0])
                P2P.connections.remove(c)##
                del Constants.clientDictionary[str(a[0]) + ":" + str(a[1])]##
                c.close()
                self.sendPeers()
                break


    def sendOrder(self, order):
        if int(order.type) == 1:
            self.buy.append([int(order.id), int(order.price), int(order.qty)])
        else:
            self.sell.append([int(order.id), int(order.price), int(order.qty)])
        while not os.path.exists("./temp.csv"):
            with open('./temp.csv', 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')
                filewriter.writerow([int(order.type), int(order.id), int(order.price), int(order.qty)])
            break
        self.save_contracts()

    # sends the updated list of peers to every connected peer (client)
    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ','

        for connection in P2P.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))

    #sends the updated list of orders to every connected peer (clients)
    def sendOrders(self):
        order_str = pickle.dumps(self.orders)
        for connection in P2P.connections:
            connection.send(b'\x13'+order_str)
        #print("Server sent orderlist to all peers\n")

class Order:
    def __init__(self, type = "bid", price = 0.0, qty = 0, id = None):
        self.id = id
        self.type = type
        self.price = price
        self.qty = qty

    def printOrder(self):
        print("type = ", self.type, " price = ", self.price, "qty =", self.qty, "\n")

class Client:
    orders = []
    #Client SEND TO Server
    def sendMsg(self, sock):
        #first send your id to the server, then enter into loop to send orders
        cid = randint(0,100)
        sock.send(b'\x14'+ bytes(str(cid), "utf-8"))

        while True:
            print("press 1 for buyer and press 2 for seller\n")
            type = input()
            if type == "1":
                # print("enter price of the bid\n")
                #price = input()
                price = 1000 ################################
                print("enter the quantity of the bid in units\n")
                qty = input()
                order = Order(type, price, qty)
                print("enter 1 to confirm the order: ")
                order.printOrder()
                confirm = input()
                if confirm == "1":
                    str_order = pickle.dumps(order)
                    # print("this is the serialized order:", str_order)
                    sock.send(b'\x12' + str_order)

            elif type == "2":
                # print("enter price of the bid\n")
                # price = input()
                price = 1000 ##############################
                print("enter the quantity of the ask in units\n")
                qty = input()
                order = Order(type, price, qty)
                print("enter 1 to confirm the order: ")
                order.printOrder()
                confirm = input()
                if confirm == "1":
                    str_order = pickle.dumps(order)
                    print("this is the serialized order:", str_order)
                    sock.send(b'\x12' + str_order)

            else:
                print('enter a valid order, lets try this again!\n')
            #sock.send(bytes(input(), "utf-8"))

    def __init__(self):
        pass

    def main_function(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, Constants.port))
        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        # CLIENT RECEIVE
        while True:
            try:
                data = sock.recv(Constants.buf_size)
                #break when server disconnects
                if not data:
                    break
                # if the data is updated list of connected peers in p2p
                if data[0:1] == b'\x11':
                    #print('updated peers')
                    self.updatePeers(data[1:])
                # if the data is the updated list of the orders
                if data[0:1] == b'\x13':
                    self.orders = pickle.loads(data[1:])
                    #print("got the updated orders from server, length = \n", len(self.orders))
                if data[0:1] == b'\x15':
                    print('raw data received = ' + data[1:])
                    P2P.blockchain = pickle.loads(data[1:])
                    print("received blockchain as:\n")
                    P2P.blockchain.printBlockchain
            except Exception as e:
                break

    def updatePeers(self, peerData):
        #remove last item since the string ended in a ","
        P2P.peers = str(peerData, "utf-8").split(",")[:-1]



if __name__ == "__main__":
    #when server disconnects
    if os.path.exists("./temp.csv"):
        os.remove("./temp.csv")
    while True:
        try:
            print("Trying to connect ...")
            time.sleep(randint(1,5))
            client = Client()
            #assuming that one of the peers has already become the server
            for peer in P2P.peers:
                try:
                    client.main_function(peer)
                    I_AM_NEW = 0
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass
            time.sleep(randint(1,5))
            # assuming that one of the peers has already become the server
            for peer in P2P.peers:
                try:
                    client.main_function(peer)
                    # client.connect((peer,Constants.port))
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass
            #if none of the peers became the server we want to become the server
            try:
                server = Server(I_AM_NEW)
            except KeyboardInterrupt:
                if os.path.exists("./temp.csv"):
                    os.remove("./temp.csv")
                with open('./temp.csv', 'w') as csvfile:
                    filewriter = csv.writer(csvfile, delimiter=',')
                    filewriter.writerow([-1,-1,-1,-1])
                sys.exit(0)
            except Exception as e:
                print(e)
                print("could not start the server ...")

        except KeyboardInterrupt:
            sys.exit(0)

    #this is a small addition
