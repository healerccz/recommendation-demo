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

        self.k = 30
        self.n = 10

    
    def get_data(self, file_path):
        """
        @description: load data from file
        @param file_path: path of file
        """
        print('start loading data from ', file_path)
        with open(file_path, "r") as f:
            for i, line in enumerate(f, 0):
                if i != 0:  # remove the first line that is title
                    line = line.strip('\r')
                    user, item, rating, timestamp = line.split(',')
                    self.train.setdefault(user, [])
                    self.train[user].append([item, rating])
        print('loading data successfully')
                

    def similarity(self):
        """
        @description: caculate similarity between item i and item j
        """
        print('start caculating similarity matrix ...')
        for user, item_ratings in self.train.items():
            items = [x[0] for x in item_ratings]    # items that user have interacted
            for i in items:
                self.N.setdefault(i, 0)
                self.N[i] += 1  # number of users who have interacted item i
                for j in items:
                    if i != j:
                        self.W.setdefault(i, {})
                        self.W[i].setdefault(j, 0)
                        self.W[i][j] += 1   # number of users who have interacted item i and item j
        for i, j_cnt in self.W.items():
            for j, cnt in j_cnt.items():
                self.W[i][j] = self.W[i][j] / (self.N[i] * self.N[j]) ** 0.5    # similarity between item i and item j
        print('caculating similarity matrix successfully')
      

    def recommendation(self, user):
        """
        @description: recommend n item for user
        @param user: recommended user
        @return items recommended for user
        """
        print('start recommending items for user whose userId is ', user)
        rank = {}
        watched_items = [x[0] for x in self.train[user]]
        for i in watched_items:
            for j, similarity in sorted(self.W[i].items(), key=operator.itemgetter(1), reverse=True)[0:self.k]:
                if j not in watched_items:
                    rank.setdefault(j, 0.)
                    rank[j] += float(self.train[user][watched_items.index(i)][1]) * similarity  # rating that user rate for item i * similarity between item i and item j
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:self.n]


if __name__ == "__main__":
    file_path = "C:\\Users\\DELL\\Desktop\\code\\python\\dataset\\ml-latest-small\\ratings.csv"
    itemBasedCF = ItemBasedCF()
    itemBasedCF.get_data(file_path)
    itemBasedCF.similarity()
    user = random.sample(list(itemBasedCF.train), 1)
    rec = itemBasedCF.recommendation(user[0])
    print('\nitems recommeded for user whose userId is', user[0], ':')
    print(rec)