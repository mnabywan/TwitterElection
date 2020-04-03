import tweepy

consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"
access_key = "***REMOVED***"
access_secret = "***REMOVED***"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)