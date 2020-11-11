"""
@description: a demo for user-based collaborative filtering
@author: Chengcheng Zhao
@date: 2020-11-15 15:21:13
"""
import random
import operator


class UserBasedCF:
    def __init__(self):
        self.N = {}  # number of items user interacted, N[u] = the number of items user u interacted
        self.W = {}  # similarity of user u and user v

        self.train = {} # train = { user : [item, rating], …… }
        self.item_users = {}    # item_users = { item : [user1, user2, …]， …… }

        # recommend n items from the k most similar users
        self.k = 30
        self.n = 10


    def get_data(self, file_path):
        """
        @description: load data from dataset
        @file_path: path of dataset
        """
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 0):
                if i != 0:  # remove the title of the first line
                    line = line.strip('\n')
                    user, item, rating, timestamp = line.split(',')
                    self.train.setdefault(user, [])
                    self.train[user].append([item, rating])

                    self.item_users.setdefault(item, [])
                    self.item_users[item].append(user) 


    def similarity(self):
        """
        @description: calculate similarity between user u and user v
        """
        for item, users in self.item_users.items():
            for u in users:
                self.N.setdefault(u, 0)
                self.N[u] += 1
                for v in users:
                    if u != v:
                        self.W.setdefault(u, {})
                        self.W[u].setdefault(v, 0)
                        self.W[u][v] += 1   # number of items which both user u and user v have interacted
        for u, user_cnts in self.W.items():
            for v, cnt in user_cnts.items():
                self.W[u][v] = self.W[u][v] / (self.N[u] * self.N[v]) ** 0.5    # similarity between user u and user v
 

    def recommendation(self, user):
        """
        @description: recommend items for user
        @param user : the user who is recommended, we call this user u
        @return : items recommended for user u
        """
        watched = [i[0] for i in self.train[user]]  # items that user have interacted
        rank = {}
        for v, similar in sorted(self.W[user].items(), key=operator.itemgetter(1), reverse=True)[0:self.k]: # order user v by similarity between user v and user u
            for item_rating in self.train[v]:   # items user v have interacted
                if item_rating[0] not in watched:   # item user hvae not interacted
                    rank.setdefault(item_rating[0], 0.)
                    rank[item_rating[0]] += similar * float(item_rating[1])
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:self.n]
        

file_path = "C:\\Users\\DELL\\Desktop\\code\\python\\dataset\\ml-latest-small\\ratings.csv"
userBasedCF = UserBasedCF()
userBasedCF.get_data(file_path)
userBasedCF.similarity()
user = random.sample(list(userBasedCF.train), 1)
rec = userBasedCF.recommendation(user[0])
print(rec)
