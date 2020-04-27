from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def template_test():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)