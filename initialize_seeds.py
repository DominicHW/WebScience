from random import random
import json

"""
This program initializes the seeds for the k-Means clustering. It takes random tweet IDs as the seeds and saves them to initialSeeds.txt
"""

with open("output/tweets.json", "r", encoding="utf-8") as f:
    num_lines = sum(1 for line in f)
    percentage = input("Number of clusters as percentage of total tweets: ")
    clusters = round(num_lines * (int(percentage)/100))

print("Initializing random seeds for", clusters, "clusters...")

with open("output/tweets.json", "r", encoding="utf-8") as f:
    seeds = []
    lines = 0
    for line in f:
        tweet = json.loads(line)
        num = random()
        if num >= 0.5 and len(seeds) != clusters:
            seeds.append(tweet["_id"]["$numberLong"])
        elif len(seeds) == clusters:
            break

# Write seeds to file
seeds_file = open("output/initialSeeds.txt", "w", encoding='utf-8')

for seed in seeds:
    print(seed+",", file=seeds_file)

print("***Finished computing seeds, saved to initialSeeds.txt file***\nPass this file to kmeans.py to perform clustering.")
