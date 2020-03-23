import tweepy
import pymongo
import json
import time
from datetime import datetime

# Twitter Dev Account Keys
auth = tweepy.OAuthHandler("01GoAHqiLgFvbBEgQPTDFHjBW", "69C7UQ0J6PA604kYbUxMxBkZCaQu786kj6XlhEv1d0TDo1UxYK")
auth.set_access_token("1233433156101005312-vD2zl5VPgH8kFjnl1zRRuN3ed7YfSA", "jbmc1cDwdz5Z0WGZeFw10riX8t4IkvKn1y9jrGJf4JKHf")
api = tweepy.API(auth)

# # MongoDB Database setup
# client = pymongo.MongoClient("mongodb://2253422h:40002011@130.209.247.2:27017")
# db  = client["2253422hdb"]
# collection = db['tweets']

# MongoDB Database setup
client = pymongo.MongoClient('127.0.0.1',27017)
db  = client.twitter_crawler
collection = db['tweets']
keyword = "corona"

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        username = status.user.screen_name
        text = status.text.strip()
        date = status.created_at
        _id = status.id

        tweet = {"_id": _id, "username": username, "text": text, "date": date}
        print(tweet)
        insertion = collection.insert_one(tweet)

###### REST API call
rest = api.search(keyword, lang=["en"])

for obj in rest:
    # Grab tweet info from REST call
    username = obj._json["user"]["screen_name"]
    text = obj._json["text"]
    created_at = obj._json["created_at"]
    _id = obj._json["id"]

    # Format the date
    date = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    #print(date)

    tweet = {"_id": _id, "username": username, "text": text, "date": date}
    print(tweet)
    insertion = collection.insert_one(tweet)

print("------------REST API Call Complete!")

###### Stream call
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
# Filter tweets on the word 'brexit'
myStream.filter(track=[keyword], languages=["en"])

# Filter tweets on a certain person
# myStream.filter(follow=["2211149702"])

# print(myStream)
