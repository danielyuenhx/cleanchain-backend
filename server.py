from flask import Flask
from flask_cors import CORS
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from geopy.geocoders import Nominatim
from random import *

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/getSamplePoints")
def samplePoints():
    # sample_points_url = "https://environment.data.gov.uk/water-quality/id/sampling-point?samplingPointStatus=open"
    # sample_points = requests.get(sample_points_url).json()['items']

    # # loop through items and check samples up to 3 months ago
    # cutoff_date = datetime.now() - relativedelta(months = 3)
    # for sample in sample_points:
    #     sample_url = sample["@id"]
    
    return sample_points

@app.route("/getSamplePoint/<location>")
def samplePoint(location):
    geolocator = Nominatim(user_agent="geoapiExercises")

    print(location)
    return "ok"

    # for point in sample_points: 
    #     location = geolocator.reverse(str(point["lat"])+","+str(point["long"]))

if __name__ == '__main__':
    sample_points_url = "https://environment.data.gov.uk/water-quality/id/sampling-point?samplingPointStatus=open"
    sample_points = requests.get(sample_points_url).json()['items']

    for sample in sample_points:
        sample['bounty'] = randint(500,2000)

    app.run(host='localhost', port=8000, debug=True)