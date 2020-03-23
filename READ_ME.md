Thanks to Ibai Castells for the `initialise_seeds.py` script, which autogenerates cluster seeds prior to clustering.

#### Order of Execution

1) Once the database is setup (localhost:27017), run `python crawler.py`\
2) Export the database as a JSON file, place in **output/** and call it **tweets.json**\
3) Run `python initialise_seeds.py`, enter a value that is 10% of the number of values in tweets.json\
4) Run `python kmeans.py` to perform kmeans clustering, clusters are output to **output/output.txt**
