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


if __name__ == '__main__':
    app.run(debug=True)