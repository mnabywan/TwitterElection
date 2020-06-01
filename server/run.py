from flask import Flask, render_template
import datetime
from sys import path as modules_directories
from os import path

scripts_path = path.abspath('../scripts')
modules_directories.append(scripts_path)
import authentication
import analysis

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/charts/likes_rts")
def likes_rts_chart():
    return render_template('charts.html', chart='/static/charts/likes_and_rts.svg', title='Wykres Liczby polubień i reetweetów wpisów kandydatów')

@app.route("/charts/candidate_tweets")
def candidate_tweets_chart():
    return render_template('charts.html', chart='/static/charts/candidate_tweets.svg', title='Wykres liczby tweetów napisanych przez każdego kandydata')

@app.route("/charts/followers")
def followers_chart():
    return render_template('charts.html', chart='/static/charts/followers.svg', title='Liczba obserwujących każdego kandydata')

@app.route("/charts/friends")
def friends_chart():
    return render_template('charts.html', chart='/static/charts/friends.svg', title='Liczba przyjaciół każdego kandydata')


@app.route("/charts/retweet_count")
def retweet_count():
    return render_template('charts.html', chart='/static/charts/retweet_count.svg', title='Liczba retweetów zsumowana wg dat dla wszystkich kont kandydatów')


@app.route("/charts/tweet_count")
def tweet_count():
    return render_template('charts.html', chart='/static/charts/tweets_count.svg', title='Liczba tweetów zsumowana wg dat dla wszystkich kont kandydatów')

@app.route("/charts/favourite_count")
def favourite_count():
    return render_template('charts.html', chart='/static/charts/favourite_count.svg', title='Liczba tweetów zsumowana wg dat dla wszystkich kont kandydatów')

@app.route("/wordclouds/biedron_words")
def biedron_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Biedron_common_words.png', title='Wordcloud - Biedron')

@app.route("/wordclouds/bosak_words")
def bosak_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Bosak_common_words.png', title='Wordcloud - Bosak')

@app.route("/wordclouds/duda_words")
def duda_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Duda_common_words.png', title='Wordcloud - Duda')

@app.route("/wordclouds/holownia_words")
def holownia_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Holownia_common_words.png', title='Wordcloud - Holownia')

@app.route("/wordclouds/kidawa_words")
def kidawa_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Kidawa_common_words.png', title='Wordcloud - Kidawa')

@app.route("/wordclouds/kosiniak_words")
def kosiniak_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/Kosiniak_common_words.png', title='Wordcloud - Kosiniak')

@app.route("/wordclouds/all_words")
def all_wordcloud():
    return render_template('charts.html', chart='/static/wordclouds/words/all_common_words.png', title='Wordcloud - wszystkie słowa')

if __name__ == '__main__':
    app.run(debug=True)