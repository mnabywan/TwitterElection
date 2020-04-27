# TwitterElection

## Installation
#### Linux
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
# set enviroment variables TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET
cd server
FLASK_APP=run.py flask run
```