"""
@description: a demo for user-based collaborative filtering
@author: Chengcheng Zhao
@date: 2020-11-15 15:21:13
"""
import numpy as py
import random

class UserBasedCF:
    def __init__(self):
        self.N = {}  # number of items user interacted, N[u] = the number of items user u interacted
        self.W = {}  # number of items which both u and v interacted, W[u][v] = the number of iterms which both u and v interacted
        self.similarity = [] # similarity of user u and user v

        # self.user_items_train = {}  # user_items for training
        # self.user_items_test = {}   # user_items for testing

        self.train = []
        self.test = []

        self.item_users = {}

    def get_data(self, file_path, threshold):
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                line = line.strip('\n')
                user, item, rating, timestamp = line.split(',')
                if random.random() < threshold:
                    self.train.append([user, item, rating])
                    self.item_users.setdefault(item, [])
                    self.item_users[item].append(user) 
                else:
                    self.test.append([user, item, rating])

    def similarity(self):
        print('hello')
        # print(self.item_users.items())
        # for item, users in self.item_users.items():
        #     for u in users:
        #         self.N.setdefault(u, 0)
        #         self.N[u] += 1
        #         for v in users:
        #             if u != v:
        #                 self.W.setdefault(u, [])
        #                 self.W.setdefault[u].setdefault(v, 0)
        #                 self.W[u][v] += 1


file_path = "C:\\Users\\DELL\\Desktop\\code\\python\\dataset\\ml-latest-small\\ratings.csv"
userBasedCF = UserBasedCF()
userBasedCF.get_data(file_path, 0.75)
print(userBasedCF.train)
# userBasedCF.similarity()
# print(userBasedCF.N[0])