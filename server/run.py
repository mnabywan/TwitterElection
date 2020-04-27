from flask import Flask, render_template
import datetime
from sys import path as modules_directories
from os import path

scripts_path = path.abspath('../scripts')
modules_directories.append(scripts_path)
import authentication

app = Flask(__name__)


@app.route("/")
def template_test():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)