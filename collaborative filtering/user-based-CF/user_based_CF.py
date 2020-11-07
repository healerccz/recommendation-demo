"""
@description: a demo for user-based collaborative filtering
@author: Chengcheng Zhao
@date: 2020-11-15 15:21:13
"""
import numpy as py
import random
import operator


class UserBasedCF:
    def __init__(self):
        self.N = {}  # number of items user interacted, N[u] = the number of items user u interacted
        self.W = {}  # similarity of user u and user v

        self.train = {}
        self.test = {}

        self.item_users = {}

        # recommend n items from the k most similar users
        self.k = 20
        self.n = 10


    def get_data(self, file_path, threshold):
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 0):
                if i != 0:  # remove the title of the first line
                    line = line.strip('\n')
                    user, item, rating, timestamp = line.split(',')
                    if random.random() < threshold:
                        self.train.setdefault(user, [])
                        self.train[user].append([item, rating])
                        self.item_users.setdefault(item, [])
                        self.item_users[item].append(user) 
                    else:
                        self.test.setdefault(user, [])
                        self.test[user].append([item, rating])


    def similarity(self):
        for item, users in self.item_users.items():
            for u in users:
                self.N.setdefault(u, 0)
                self.N[u] += 1
                for v in users:
                    if u != v:
                        self.W.setdefault(u, {})
                        self.W[u].setdefault(v, 0)
                        self.W[u][v] += 1
        for u, user_cnts in self.W.items():
            for v, cnt in user_cnts.items():
                self.W[u][v] = self.W[u][v] / (self.N[u] * self.N[v]) ** 0.5
 

    def recommendation(self, user):
        watched = [i[0] for i in self.train[user]]
        rank = {}
        rec = []
        for v, similar in sorted(self.W[user].items(), key=operator.itemgetter(1), reverse=True)[0:self.k]:
            for item_rating in self.train[v]:
                if item_rating[0] not in watched:
                    rank.setdefault(item_rating[0], 0.)
                    rank[item_rating[0]] += similar * float(item_rating[1])
        for item, rating in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
            if self.n != 0:
                self.n -= 1
                rec.append([item, rating])    
        print(rec)
        return rec
        

file_path = "C:\\Users\\DELL\\Desktop\\code\\python\\dataset\\ml-latest-small\\ratings.csv"
userBasedCF = UserBasedCF()
userBasedCF.get_data(file_path, 0.75)
userBasedCF.similarity()
userBasedCF.recommendation("1")