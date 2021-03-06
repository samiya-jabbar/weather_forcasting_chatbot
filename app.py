# import flask dependencies
import requests
from flask import Flask, request, make_response, jsonify

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'WELCOME TO WEATHER TEMPERATURE APP'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    intent_name = req.get('queryResult').get('intent').get('displayName')
    if intent_name=='temperature':
        city = req.get('queryResult').get('parameters').get('city')
        API_KEY = '3f3483997cd121c26d7ad4b025150044'  # initialize your key here

        # call API and convert response into Python dictionary
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        temp_object = requests.get(url).json()
        temp=float(temp_object["main"]["temp"])-273.15
        temp = round(temp, 2)
        fehren = (temp * 9/5) + 32
        fehren = round(fehren, 2)
        celsius_fulfilmenttext=f"Temperature of {city} is {temp} °C & {fehren} °F"

    # return a fulfillment response
        return {
    'fulfillmentMessages': [
        {
            'text': {
                'text': [
                
                celsius_fulfilmenttext
                
                ]
            }
        }
        ]
    }

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


# run the app
if __name__ == '__main__':
   app.run()