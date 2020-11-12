"""
@description: a demo for item_based collaborative filtering
@author: Chengcheng Zhao
@date: 2020-11-11 21:19:00
"""
import random
import operator

class ItemBasedCF:
    def __init__(self):
        self.N = {} # number of item user have interacted
        self.W = {} # similarity matrix to store similarity of item i and item j

        self.train = {}
        self.item_users = {}

        self.k = 30
        self.n = 10

    
    def get_data(self, file_path):
        """
        docstring
        """
        with open(file_path, "r") as f:
            for i, line in enumerate(f, 0):
                if i != 0:
                    line = line.strip('\r')
                    user, item, rating, timestamp = line.split(',')
                    self.train.setdefault(user, [])
                    self.train[user].append([item, rating])

                    self.item_users.setdefault(item, [])
                    self.item_users[item].append(user)
                

    def similarity(self):
        for item, users in self.item_users.items():
            self.N.setdefault(item, 0)
            for i in item:
                self.N[item] += 1
                for v in item:
                    if u != v:
                        self.W.setdefault(u, {})
                        self.W[u].setdefault(v, 0)
                        self.W[u][v] += 1
        for i, j_cnt in self.W.items():
            for j, cnt in j_cnt.items():
                self.W[i][j] = self.W[i][j] / self.N[i] * self.N[j] ** 0.5
      

file_path = "C:\\Users\\DELL\\Desktop\\code\\python\\dataset\\ml-latest-small\\ratings.csv"
itemBasedCF = ItemBasedCF()
itemBasedCF.get_data(file_path)
itemBasedCF.similarity()
print(itemBasedCF.W)