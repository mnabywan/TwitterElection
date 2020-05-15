import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3


from datetime import date, timedelta


def candidate_sum(table, date, candidate,  conn):

    hash_pop = ("SELECT  sum(favorite_count) as favourites,sum(retweet_count) as retweets "
                "FROM {} WHERE candidate_name = \'{}\' AND created_at LIKE \'{}\'".format(table, candidate, date))
    print(hash_pop)
    df = pd.read_sql_query(hash_pop, conn)
    return df


conn = sqlite3.connect('../db/Twitter.db')
cur = conn.cursor()


sdate = date(2020, 3, 30)   # start date
edate = date(2020, 5, 7)   # end date

delta = edate - sdate       # as timedelta

duda_favorites = []
biedron_favorites = []
kidawa_favorites = []
bosak_favorites = []
holownia_favorites = []
kosiniak_favorites = []

candidates = {
    "Duda": duda_favorites,
    "Biedron": biedron_favorites,
    "Bosak": bosak_favorites,
    # "Holownia": holownia_favorites,
    # "Kidawa": kidawa_favorites,
    # "Kosiniak": kosiniak_favorites
}

days_list = []

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    day = str(day)
    days_list.append(day)

for candidate in candidates.keys():
    for day in days_list:
        df = candidate_sum('candidates_tweets',  day + ' %', candidate, conn )
        candidates.get(candidate).append(df['favourites'])



dates = [pd.to_datetime(d) for d in days_list]


for item in candidates.keys():
    fav_list = candidates.get(item)
    plt.scatter(dates, fav_list, s =10, )
    plt.xlabel("Date")
    plt.ylabel("Favorite count")
    plt.title("Favorite count for date for accounts connected to each candidate ")
    plt.plot(dates, fav_list, label=item )

plt.legend()
plt.show()