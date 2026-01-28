from flask import Flask, render_template, request, url_for, flash, redirect
from flask_limiter import Limiter
from geopy.geocoders import Nominatim
import json
import requests
from datetime import datetime
import calendar

from dotenv import load_dotenv
import os

from flask_limiter.util import get_remote_address

from models import LocationForm

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)

def checkAPI(response):
    if (response.status_code != requests.codes.ok):
        print("Error: ", response.status_code)

@app.route('/', methods=['GET','POST'])
@app.route('/weather', methods=['GET','POST'])
def weather():
    locator = Nominatim(user_agent="weatherAPI.py")
    form = LocationForm()
    print(form.location.data)

    if form.validate_on_submit():
        #Get the info and replace city with it
        givenLocation = form.location.data
        location = locator.geocode(givenLocation)

    else:
        #Replace city with initial placeholder
        givenLocation = "New York City"
        location = locator.geocode(givenLocation)

    if location is None:
        flash("Inputted location could not be found")
        return redirect(url_for('weather'))
    
    #This first hashmap is for calling the api
    info = {
        "Location": location,
        "lat": round(location.latitude, 2),
        "long": round(location.longitude, 2)
    }

    #get the weather
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,apparent_temperature,wind_speed_10m&daily=apparent_temperature_max,apparent_temperature_min,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7".format(round(info.get("lat"),2),round(info.get("long"),2))
    weather_response = requests.get(weather_url)
    checkAPI(weather_response)
    
    results = json.loads(weather_response.text)

    #This second hashmap is for frontend display purposes
    info = {
        "Location": givenLocation,
        "date": results.get("daily").get("time"),
        "maxTemp": [round(num,2) for num in results.get("daily").get("apparent_temperature_max")]
    }

    days_of_week = []
    for x in range(len(info['date'])):
        my_date = datetime.strptime(info['date'][x], "%Y-%m-%d")
        days_of_week.append(calendar.day_name[my_date.weekday()])
    
    info["days"] = days_of_week

    return render_template('weather.html', info = info, form = form)

#urlBuild = 'https://api.api-ninjas.com/v1/geocoding?city=' + city + '&country=' + country
#open data from api
if __name__ == "__main__":
    app.run(debug = True)


"""
NOTE:
1. Add error screen
    - I think you can just use flask alerts, 
"""