from flask import Flask
from flask import render_template
from flask import request
import requests
from pprint import pprint
import random

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/loggedin")
def welcome():

    code = request.args.get('code', '')
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    post_data = "code=%s&client_secret=%s&client_id=%s&grant_type=authorization_code" % (
        code,
        'EKGPOCDDNCLLUCXYL3T6Y36GLKS6AF3WQ7BMRKPPHLYHM2ZRQT',
        'BOIHE6CFAPR5PW2H5Y')


    response = requests.post('https://www.eventbrite.com/oauth/token',
                            data=post_data,
                             headers=headers).json()

    access_token = response['access_token']

    response = requests.get(
    "https://www.eventbriteapi.com/v3/users/me/orders/",
    headers = {
        "Authorization": "Bearer " + access_token,
    },
    verify = True,  # Verify SSL certificate
    ).json()


    upcoming_events = requests.get(
    "https://www.eventbriteapi.com/v3/events/search/?start_date.range_start=2016-01-01T00:00:00Z&start_date.range_end=2016-01-30T00:00:00Z",
    headers = {
        "Authorization": "Bearer " + access_token,
    },
    verify = True,  # Verify SSL certificate
    ).json()


    random_index = random.randint(0, 49)
    random_event_url = upcoming_events['events'][random_index]['url']
    random_event_name = upcoming_events['events'][random_index]['name']['html']


    events = 0
    total_cost = 0
    for event in response['orders']:
        if (event['created']).startswith('2015'):
            events += 1
            event_cost = event['costs']['gross']['value']
            total_cost += float(event_cost)

    total_cost /= 100


    return render_template('loggedin.html', int_cost=total_cost, total_cost="%.2f" % total_cost, events=events, random_event_url=random_event_url, random_event_name=random_event_name)

if __name__ == "__main__":
    app.run()
