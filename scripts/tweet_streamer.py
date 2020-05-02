import sys
import tweepy
import json
import sqlite3
import scripts.authentication as authentication

elections_hashtags = ["#wybory2020", "#WyboryPrezydenckie2020", "#wybory", "#PrzełożyćWybory",
                      "#IdziemyNaWybory", "#idźnawybory", "#GłosowanieKorespondencyjne", "#wyPAD2020"]

conn = sqlite3.connect('Twitter.db')
c = conn.cursor()
# table_create = """CREATE TABLE tweets (tweet_id)"""
# c.execute(table_create)
# conn.commit()


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        print(status_code)

    def on_data(self, data):
        tweets = json.loads(data)
        id = tweets['id']
        print(tweets['created_at'])
        str = "INSERT INTO tweets(tweet_id) VALUES ({})"
        str = str.format((id))
        c.execute(str)
        conn.commit()

if __name__ == '__main__':
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=authentication.auth, listener=stream_listener)

    stream.filter(track=elections_hashtags)
