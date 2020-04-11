import tweepy
import datetime, time
import sqlite3
from candidates import *
from authentication import consumer_key, consumer_secret, access_key, access_secret, auth, api


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

def get_tweets_by_hashtag(api, hashtag, table_name, date_until=None, date_since=None):
    print(hashtag)
    for tweet in tweepy.Cursor(api.search,
                               q= hashtag,
                                since = date_since,
                                until = date_until,
                                rpp=10,
                                count= 10
                               ).items():
        if 'RT @' not in tweet.text:
            id = tweet.id
            is_tweet_in_base = "SELECT tweet_id from {} where tweet_id = {}".format(table_name, id)
            c.execute(is_tweet_in_base)
            id_in_base = c.fetchall()
            if not id_in_base:
                author_name = tweet.author.name
                print(tweet.created_at)
                str = "INSERT INTO {}(tweet_id, hashtag) VALUES ({}, \"{}\")"
                str = str.format(table_name, id, hashtag)
                #print(str)
                c.execute(str)
                conn.commit()


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


def get_tweets_by_journalist_account(api, table_name, journalist):
    print(table_name)
    print(journalist)
    page = 1
    end = False

    while True:
        tweets = api.user_timeline(journalist, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days  <= 31:
                if 'RT @' not in tweet.text and any(word in tweet.text for word in ELECTION_KEYWORDS):
                    ''' Handle unique  '''
                    id = tweet.id
                    is_tweet_in_base = "SELECT tweet_id from journalist_tweets where tweet_id = {}".format(id)
                    c.execute(is_tweet_in_base)
                    id_in_base = c.fetchall()
                    if not id_in_base:
                        #author_name = tweet.author.name
                        print(tweet.created_at)
                        str = "INSERT INTO journalist_tweets(tweet_id, author_name) VALUES ({}, \"{}\")"
                        str = str.format(id, journalist)
                        print(str)
                        c.execute(str)
                        conn.commit()
            else:
                end = True
                return

        if not end:
             page = page + 1
            #time.sleep(10)


def get_tweets_by_candidates_accounts():
    accounts_list = DUDA_ACCOUNTS + KIDAWA_ACCOUNTS + KOSINIAK_HASHTAGS \
                    + BIEDRON_HASHTAGS + HOLOWNIA_ACCOUNTS + BOSAK_HASHTAGS
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


def get_tweets_by_hashtag_start():
    table_name = "election_tweets"
    for hashtag in ELECTION_HASHTAGS:
        get_tweets_by_hashtag(api, hashtag, table_name=table_name, date_until="2020-04-06")


def get_tweets_by_candidates_hashtags_start():
    hashtag_list =  KIDAWA_HASHTAGS + KOSINIAK_HASHTAGS +\
                    BIEDRON_HASHTAGS + HOLOWNIA_HASHTAGS + BOSAK_HASHTAGS
    for hashtag in hashtag_list:
        if hashtag in DUDA_HASHTAGS:
            table_name = "duda_hashtags"
        elif hashtag in KIDAWA_HASHTAGS:
            table_name = "kidawa_hashtags"
        elif hashtag in KOSINIAK_HASHTAGS:
            table_name = "kosiniak_hashtags"
        elif hashtag in BIEDRON_HASHTAGS:
            table_name = "biedron_hashtags"
        elif hashtag in HOLOWNIA_HASHTAGS:
            table_name = "holownia_hashtags"
        elif hashtag in BOSAK_HASHTAGS:
            table_name = "bosak_hashtags"
        get_tweets_by_hashtag(api, hashtag, table_name=table_name, date_until="2020-04-05")



def get_tweets_by_journalists_account_start():
    table_name = "journalist_tweets"
    for journalist in JOURNALISTS_ACCOUNTS:
        get_tweets_by_journalist_account(api, table_name, journalist)

if __name__ == '__main__':
    t = api.get_status(1248538479048491008)
    print(t.text)
    print(t.author)
    print(t.author.screen_name)
    #get_tweets_by_hashtag_start()
    #get_tweets_by_candidates_hashtags_start()
    get_tweets_by_journalists_account_start()



