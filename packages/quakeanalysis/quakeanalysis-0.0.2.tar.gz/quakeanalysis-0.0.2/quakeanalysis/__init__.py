import json 
import requests
from urllib.request import urlopen
import pandas as pd
import numpy as np
import datetime
from geopy.geocoders import Nominatim


def earthquake_distance(place):    


    #https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4

    def haversine_distance(lat1, lon1, lat2, lon2):
       r = 6371
       phi1 = np.radians(lat1)
       phi2 = np.radians(lat2)
       delta_phi = np.radians(lat2 - lat1)
       delta_lambda = np.radians(lon2 - lon1)
       a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
       res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
       return np.round(res, 2)


    #https://stackoverflow.com/questions/25888396/how-to-get-latitude-longitude-with-python
    
    geolocator = Nominatim(user_agent="my_user_agent")
    city = place
    loc = geolocator.geocode(city)

    today = datetime.datetime.today()
    yesterday = today - timedelta(days=1)

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime='+ str(today) +'&endtime=' + str(yesterday)

    json_url = urlopen('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2022-05-23&endtime=2022-05-25')
    data = json.loads(json_url.read())

    json_dict = data.get('features')

    latlist = []
    longlist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        longitude = rd[0]
        latitude = rd[1]
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)

    column = df["distance"]
    min_value = column.min()

    return min_value

