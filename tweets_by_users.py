import tweepy
import datetime, time
import sqlite3
from candidates import *

consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"
access_key = "***REMOVED***"
access_secret = "***REMOVED***"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

conn = sqlite3.connect('Twitter.db')
c = conn.cursor()


# table_create = """CREATE TABLE "candidates_tweets" (
# 	"tweet_id"	INTEGER NOT NULL,
# 	"candidate_name"	TEXT NOT NULL,
# 	"author_name"	TEXT NOT NULL,
# 	PRIMARY KEY("tweet_id")
# );"""
# c.execute(table_create)
# conn.commit()


def get_tweets_by_user(api, username, candidate):
    print(username)
    print(candidate)
    page = 1
    end = False

    while True:
        tweets = api.user_timeline(username, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days  <= 31:
                if 'RT @' not in tweet.text:
                    ''' Handle unique  '''
                    id = tweet.id
                    is_tweet_in_base = "SELECT tweet_id from candidates_tweets where tweet_id = {}".format(id)
                    c.execute(id_in_base)
                    id_in_base = c.fetchall()
                    if not id_in_base:
                        author_name = tweet.author.name
                        print(tweet.created_at)
                        str = "INSERT INTO candidates_tweets(tweet_id, candidate_name, author_name) VALUES ({}, \"{}\", \"{}\")"
                        str = str.format(id, candidate, author_name)
                        print(str)
                        c.execute(str)
                        conn.commit()
            else:
                end = True
                return

        if not end:
             page = page + 1
             time.sleep(10)



if __name__ == '__main__':
    accounts_list = ['michalkobosko']

    print(accounts_list)
    for user in accounts_list:
        if user in DUDA_ACCOUNTS:
            candidate = DUDA
        elif user in KIDAWA_ACCOUNTS:
            candidate = KIDAWA
        elif user in KOSINIAK_ACCOUNTS:
            candidate = KOSINIAK
        elif user in BIEDRON_ACCOUNTS:
            candidate = BIEDRON
        elif user in BOSAK_ACCOUNTS:
            candidate = BOSAK
        elif user in HOLOWNIA_ACCOUNTS:
            candidate = HOLOWNIA

        get_tweets_by_user(api, user, candidate)
