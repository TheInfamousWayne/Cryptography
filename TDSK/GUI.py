from tkinter import *
import time
import pandas as pd
import numpy as np
import os

UPDATE_RATE = 500

class GUI(Frame):
    def __init__(self):
        super(GUI, self).__init__()
        self.root = Tk()
        self.root.geometry('500x400+0+0')
        self.counter = 1

        #Textbox
        self.left = Frame(self.root, borderwidth=2, relief="solid")
        self.right = Frame(self.root, borderwidth=2, relief="solid")
        self.buy_order = Text(self.left, width=25, height=10, bg='yellow')
        self.sell_order = Text(self.right, width=25, height=10, bg='lightblue')

        # Packing
        self.left.pack(side="left", expand=True, fill="both")
        self.right.pack(side="right", expand=True, fill="both")
        self.buy_order.pack(expand=True, fill="both", padx=5, pady=5)
        self.sell_order.pack(expand=True, fill="both", padx=5, pady=5)

        #
        self.buy_cid_msg = []
        self.buy_price_msg = []
        self.buy_vol_msg = []
        self.sell_cid_msg = []
        self.sell_price_msg = []
        self.sell_vol_msg = []

        #######
        self.buy_cid = Message(self.buy_order, text=self.buy_cid_msg, bg='orange')
        self.buy_price = Message(self.buy_order, text=self.buy_price_msg, bg='orange')
        self.buy_vol = Message(self.buy_order, text=self.buy_vol_msg, bg='orange')
        #########
        self.buy_label = Label(self.buy_order, text="BUY")
        self.buy_cid_label = Label(self.buy_cid, text="CID")
        self.buy_price_label = Label(self.buy_price, text="Price")
        self.buy_vol_label = Label(self.buy_vol, text="Volume")
        ######
        self.sell_cid = Message(self.sell_order, text=self.sell_cid_msg, bg='blue')
        self.sell_price = Message(self.sell_order, text=self.sell_price_msg, bg='blue')
        self.sell_vol = Message(self.sell_order, text=self.sell_vol_msg, bg='blue')
        #################
        self.sell_label = Label(self.sell_order, text="SELL")
        self.sell_cid_label = Label(self.sell_cid, text="CID")
        self.sell_price_label = Label(self.sell_price, text="Price")
        self.sell_vol_label = Label(self.sell_vol, text="Volume")

    def auto_destruct(self):
        self.roor.after(3000, lambda: self.root.destroy())

    def fill_buy_order(self):

        #########
        self.buy_label.pack(fill="both")
        self.buy_cid_label.pack(fill="both")
        self.buy_price_label.pack(fill="both")
        self.buy_vol_label.pack(fill="both")
        #########
        self.buy_cid.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.buy_price.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.buy_vol.pack(side="right", expand=True, fill="both", padx=5, pady=5)


    def fill_sell_order(self):

        #################
        self.sell_label.pack(fill="both")
        self.sell_cid_label.pack(fill="both")
        self.sell_price_label.pack(fill="both")
        self.sell_vol_label.pack(fill="both")
        ################
        self.sell_cid.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.sell_price.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.sell_vol.pack(side="right", expand=True, fill="both", padx=5, pady=5)


    def Msg(self, list):
        msg = ""
        for item in list:
            msg += str(item) + "\n"
        return msg


    def create_window(self):
        self.counter += 1
        t = Toplevel(self)
        t.geometry('500x300+0+400')
        t.wm_title("Window #%s" % self.counter)
        frame = Frame(t, borderwidth=2, relief="solid")
        self.match_msg_text = "Buy_CID\t Sell_CID\t Price\tVolume\n"
        self.match_msg = Message(frame, text=self.match_msg_text, width=200 , bg='lightgreen')
        l = Label(frame, text="This is window #%s" % self.counter)
        frame.pack(side="left", expand=True, fill="both")
        l.pack(side="top", fill="both", padx=5, pady=5)
        self.match_msg.pack(side="bottom", expand=True, fill="both")


    def refresh_message(self):
        msg = self.Msg(self.buy_cid_msg)
        self.buy_cid["text"] = msg
        msg = self.Msg(self.buy_price_msg)
        self.buy_price.config(text=msg)
        msg = self.Msg(self.buy_vol_msg)
        self.buy_vol["text"] = msg
        ###############################################
        msg = self.Msg(self.sell_cid_msg)
        self.sell_cid["text"] = msg
        msg = self.Msg(self.sell_price_msg)
        self.sell_price["text"] = msg
        msg = self.Msg(self.sell_vol_msg)
        self.sell_vol["text"] = msg


    def update_lists(self):
        if os.path.exists("./temp.csv"):
            try:
                data = pd.read_csv("./temp.csv", header=None, delimiter=',')
            except Exception:
                data = pd.DataFrame()
            os.remove("./temp.csv")
            if not data.empty:
                data = np.array(data)[0]
                type = data[0]
                id = data[1]
                price = data[2]
                vol = data[3]
                if type == -1:
                    self.auto_destruct()
                if type == 1:
                    self.buy_cid_msg.append(id)#self.buy_cid_file[index])
                    self.buy_price_msg.append(price)#self.buy_price_file[index])
                    self.buy_vol_msg.append(vol)#self.buy_vol_file[index])
                if type == 2:
                    self.sell_cid_msg.append(id)#self.sell_cid_file[index])
                    self.sell_price_msg.append(price)#self.sell_price_file[index])
                    self.sell_vol_msg.append(vol)#self.sell_vol_file[index])
        ###############################################
        # msg = self.Msg(self.buy_cid_msg)
        # self.buy_cid["text"] = msg
        # msg = self.Msg(self.buy_price_msg)
        # self.buy_price.config(text=msg)
        # msg = self.Msg(self.buy_vol_msg)
        # self.buy_vol["text"] = msg
        # ###############################################
        # msg = self.Msg(self.sell_cid_msg)
        # self.sell_cid["text"] = msg
        # msg = self.Msg(self.sell_price_msg)
        # self.sell_price["text"] = msg
        # msg = self.Msg(self.sell_vol_msg)
        # self.sell_vol["text"] = msg
        self.refresh_message()
        ###############################################
        for item in self.buy_vol_msg:
            idx = next((i for i,x in enumerate(self.sell_vol_msg) if x==item), None)
            if idx:
                idx2 = self.buy_vol_msg.index(item)
                self.match_msg_text = self.match_msg_text + "   {}\t    {}\t  {}\t   {}\n".format(self.buy_cid_msg[idx2], self.sell_cid_msg[idx], self.sell_price_msg[idx], self.sell_vol_msg[idx])
                self.match_msg["text"] = self.match_msg_text
                print(self.buy_vol_msg)
                print(self.sell_vol_msg)
                print('***')
                del self.sell_cid_msg[idx]
                del self.sell_price_msg[idx]
                del self.sell_vol_msg[idx]
                del self.buy_cid_msg[idx2]
                del self.buy_price_msg[idx2]
                del self.buy_vol_msg[idx2]
                self.refresh_message()
        ################################################
        self.root.after(UPDATE_RATE, self.update_lists)




    def start(self):
        buy_msg = pd.read_csv("./buy_msg.csv", header=None)
        sell_msg = pd.read_csv("./sell_msg.csv", header=None)
        buy_msg = np.array(buy_msg)
        sell_msg = np.array(sell_msg)
        #####
        self.buy_cid_file, self.buy_price_file, self.buy_vol_file = zip(*buy_msg)
        self.sell_cid_file, self.sell_price_file, self.sell_vol_file = zip(*sell_msg)
        print(type(self.buy_price_file[0]))
        print(self.buy_price_file)
        ######
        #####
        self.fill_buy_order()
        self.fill_sell_order()
        self.create_window()
        self.update_lists()
        self.root.mainloop()

if __name__=='__main__':
    gui = GUI()
    gui.start()
