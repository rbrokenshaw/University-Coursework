'''
Student Number: C1772582
Twitter streaming with Tweepy technique from Tweepy documentation: http://www.tweepy.org/
Textblob used for sentiment analysis: https://textblob.readthedocs.io/en/dev/
Some additional reading for approach: http://www.dataengineering.life/python_twitter_streaming/
'''

import sqlite3, os
import tweepy
import json
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#Create the Database if it doesn't already exist
def create_db(filename):
    needcreate = not os.path.exists(filename)
    db = sqlite3.connect(filename)
    if needcreate:
        cursor = db.cursor()
        cursor.execute ("CREATE TABLE trump ("
            "my_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
            "tweet_id INTEGER NOT NULL,"
            "tweet_text TEXT NOT NULL,"
            "created_at TEXT NOT NULL,"
            "location TEXT NOT NULL,"
            "coordinates TEXT NOT NULL,"
            "followers INTEGER NOT NULL,"
            "friends_count INTEGER NOT NULL,"
            "sentiment TEXT)")
        db.commit()
        cursor.close()
        print ("Database table", filename, "successfully created!")

create_db("Q3_sqlite_1772582.db")

#Twitter Authentication
consumer_key="JAMXPDH5pm7mHQ8GJlqjswo7c"
consumer_secret="0S4yNIdBn8bsF6KcP68vAUYMByLzgbymuTUGPSQfbHNBe63lDK"
access_token="295650933-yZkM6xzU29zX6btE77ICaFNNMOaPbSyd0s3X6UMf"
access_token_secret="GYcBRrtL0jqm87Ihe26gnn5bYFywTDoayU5tm6XH7RexV"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Database
db = sqlite3.connect('Q3_sqlite_1772582.db')
cursor = db.cursor()

#Tweet object for storing tweet data
class Tweet():

    def __init__(self, tweet_id, tweet_text, created_at, location, coordinates, followers, friends_count, sentiment):
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text
        self.created_at = created_at
        self.location = location
        self.coordinates = coordinates
        self.followers = followers
        self.friends_count = friends_count
        self.sentiment = sentiment

    #Function for storing tweets in the database
    def insertTweet(self):

        cursor.execute("INSERT INTO trump (tweet_id, tweet_text, created_at, location, coordinates, followers, friends_count, sentiment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (self.tweet_id, self.tweet_text, self.created_at, self.location, self.coordinates, self.followers, self.friends_count, self.sentiment))
        db.commit()


#Tweepy Stream listener
class TweetStreamListener(tweepy.StreamListener):

    def on_data(self, data):

        try:
            tweet = json.loads(data)

            #Ignore Retweets and Tweets with no location
            if not tweet['retweeted'] and 'RT @' not in tweet['text']:
                if tweet['user']['location'] is not None:

                    #Get Tweet Coordinates
                    if tweet['coordinates'] is not None:
                        coordinates = str(tweet['coordinates']['coordinates'])
                    else:
                        coordinates = "geo not enabled"

                    #Get Tweet Sentiment
                    tweet_s = TextBlob(tweet['text'])
                    tweet_s.sentiment
                    tweet_s.sentiment.polarity
                    if tweet_s.sentiment.polarity <0:
                        tweet_sentiment = "negative"
                    elif tweet_s.sentiment.polarity == 0:
                        tweet_sentiment = "neutral"
                    elif tweet_s.sentiment.polarity > 0:
                        tweet_sentiment = "positive"


                    #Assign all data to tweet object
                    tweet_data = Tweet(
                    tweet['id'],
                    tweet['text'],
                    tweet['created_at'],
                    tweet['user']['location'],
                    coordinates,
                    tweet['user']['followers_count'],
                    tweet['user']['friends_count'],
                    tweet_sentiment)

                    # Insert tweet data into the DB
                    tweet_data.insertTweet()
                    print("tweet added to database!")
               
        except Exception as error:
            print(error)
            pass

#Run the stream and choose the filter keyword
def runstream():

    listener = TweetStreamListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['Trump'])

runstream()

