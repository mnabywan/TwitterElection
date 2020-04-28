import pandas as pd
from pandas import DataFrame
import sqlite3
import matplotlib.pyplot as plt
from time import sleep

#TODO: rename this function
def candidate_sum(table, conn):
    
    hash_pop=("""SELECT '"""+table[0]+"""' as "candidate", sum(favorite_count) as favourites,sum(retweet_count) as retweets 
                                  FROM """+table[1])

    df = pd.read_sql_query(hash_pop, conn)
    return df

def save_likes_and_rts(outfile='server/charts/likes_and_rts.svg'):
    conn = sqlite3.connect('db/Twitter.db')
    cur = conn.cursor() 
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=[]
    for name in res:
        tables.append(name[0])

    #TODO: fetch this from candidates file
    candidates={
        "Duda":'duda_hashtags',
        "Biedron":'biedron_hashtags',
        "Bosak":'bosak_hashtags',
        "Holownia":'holownia_hashtags',
        "Kidawa":'kidawa_hashtags',
        "Kosiniak":'kosiniak_hashtags'
    }

    #TODO: rename dfl
    dfl=[]
    for k in candidates.items():
        o=candidate_sum(k, conn)
        dfl.append(o)

    #TODO: rename df
    df = pd.concat(dfl)
    df.sort_values(by=['favourites'], inplace=True, ascending=False)
    df.reset_index()
    print(df)

    df.plot(x="candidate", y=["favourites", "retweets"], kind="bar")
    plt.tight_layout()
    plt.savefig(outfile)

if __name__ == '__main__':
    save_likes_and_rts()