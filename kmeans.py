import sys
import json
import re
import copy
import math
import matplotlib.pyplot as plt
import numpy as np


# intial data cleaning and preprocessing using regular expressions
regex_str = [
    r'<[^>]+>',
    r'(?:@[\w_]+)',
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
    r"(?:[a-z][a-z'\-_]+[a-z])",
    r'(?:[\w_]+)',
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


# defining the Jaccard distance
def jaccard(a, b):
    inter = list(set(a) & set(b))
    I = len(inter)
    union = list(set(a) | set(b))
    U = len(union)
    return round(1 - (float(I) / U), 4)


# k-means implementation
def kmeans(id, centroids, terms_all, l, k = 25):
    count = 0
    for h in range(k):
        count = count + 1
        indices = [id.index(item) for item in centroids]
        cen_txt = [terms_all[x] for x in indices]
        cluster = []
        for i in range(l):
            d = [jaccard(terms_all[i], cen_txt[j]) for j in range(k)]
            ans = d.index(min(d))
            cluster.append(ans)

        centroids1 = up_date(id, cluster, terms_all, l, k)
        sum = 0
        for i in range(k):
            if (centroids1[i] == centroids[i]):
                sum = sum + 1
        if (sum == k):
            break;
        centroids = copy.deepcopy(centroids1)
    output(cluster, k, id)
    sse(cluster, centroids, terms_all, k, l)
    f.close()


# output in the form of cluster# and the array of the tweetids in that cluster.
def output(cluster, k, id):
    final = []
    cluster_set = []
    cluster_count = []
    for i in range(k):
        final.append([j for j, u in enumerate(cluster) if u == i])
        t = [x for x in final[i]]
        print(i + 1, [id[x] for x in t] , file = f)
        cluster_set.append(i+1)
        cluster_count.append(len([id[x] for x in t]))
    #
    # # Graph representation for tweet clustering
    # clusters_arg = int(sys.argv[1])
    # plt.figure()
    # plt.bar(np.arange(clusters_arg), cluster_count, label="Total Tweets")
    # plt.xticks(range(clusters_arg))
    # plt.title("Tweet Clustering")
    # plt.xlabel("Cluster Number")
    # plt.ylabel("Number of Tweets")
    # plt.savefig("output/cluster_count.png")
    # plt.tight_layout()



# computing the sum of squared errors
def sse(cluster, centroids, terms_all, k, l):
    indices1 = []
    indices = [id.index(item) for item in centroids]
    cen_txt = [terms_all[x] for x in indices]
    sum = 0
    for i in range(k):
        indices1.append([j for j, u in enumerate(cluster) if u == i])
        t = [terms_all[x] for x in indices1[i]]
        for j in range(len(indices1[i])):
            sum = sum + math.pow(jaccard(t[j], cen_txt[i]), 2)
    print('sse', sum, file=f)


# updating the centroids at every iteration
def up_date(id, cluster, terms_all, l, k):
    indices = []
    new_centxt_index = []
    new_centroid = []
    for i in range(k):
        indices.append([j for j, u in enumerate(cluster) if u == i])
        m = indices[i]
        # m gives the indices if the elements of every cluster k

        if (len(m) != 0):
            txt = [terms_all[p] for p in m]
            sim = [[jaccard(txt[i], txt[j]) for j in range(len(m))] for i in range(len(m))]
            f1 = [sum(i) for i in sim]
        # lower triangular matrix
        if len(m) != 0:
            new_centxt_index.append(
                m[(f1.index(min([sum(i) for i in sim])))])  # index of the point closer to all the other points
    new_centroid = [id[x] for x in new_centxt_index]
    return new_centroid


terms_all = []
id = []
with open(str(sys.argv[3]), 'r', encoding='utf-8') as f:
    for line in f:
        tweet = json.loads(line)
        t = tweet['text']

        tokens = preprocess(t)
        terms_all.append([term for term in tokens])

        d = tweet['_id']['$numberLong']
        id.append(int(d))

l = len(terms_all)
# Seeds
text_file = open(str(sys.argv[2]), "r")
centroids = text_file.read().split(',')
centroids = [x.strip('\n') for x in centroids]
centroids = centroids[:-1]
centroids = [int(x) for x in centroids]  # ids of centroids
k = int(sys.argv[1])
f = open("output/output.txt", 'w')
# print("Cluster Number [tweet_ids...]" , file = f)
kmeans(id, centroids, terms_all, l, k)
print("Clustering Complete! See output.txt for results.")
