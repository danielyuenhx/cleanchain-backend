from flask import Flask, request
from flask_cors import CORS
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from geopy.geocoders import Nominatim
from random import *
import json

app = Flask(__name__)
CORS(app)

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
    # sample_point_url = "https://environment.data.gov.uk/water-quality/id/sampling-point/" + location
    # sample_point = requests.get(sample_point_url).json()['items'][0]

    sample_point = sample_points_dict[location]

    geolocator = Nominatim(user_agent="geoapiExercises")
    sample_point['location'] = geolocator.reverse(str(sample_point["lat"])+","+str(sample_point["long"])).raw['address']

    return sample_point

@app.route("/closeBounty/<location>", methods=['POST'])
def closeBounty(location):
    sample_points_dict[location]['isClaimed'] = 1
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/updateBounty/<location>", methods = ['POST'])
def updateBounty(location):
    sample_points_dict[location]["bounty"] += request.get_json()['donation']
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    sample_points_url = "http://environment.data.gov.uk/water-quality/id/sampling-point/AN-BUR140"
    sample_points = requests.get(sample_points_url).json()['items']

    sample_points_dict = dict()
    for sample_point in sample_points:
        sample_point['bounty'] = 0
        sample_point['isClaimed'] = 0
        sample_point['isConfirmed'] = 0
        sample_points_dict[sample_point['notation']] = sample_point

    app.run(host='localhost', port=8000, debug=True)