import json 
import requests
from urllib.request import urlopen
import pandas as pd
import numpy as np
import datetime
from geopy.geocoders import Nominatim
from datetime import timedelta


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return distance_v



def earthquake_longitude(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return longitude_v



def earthquake_latitude(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return latitude_v



def earthquake_magnitude(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return magnitude_v


def earthquake_place(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return place_v



def earthquake_time(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return time_v

def earthquake_df(place):    


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
    magnitudelist = []
    placelist = []
    timelist = []
    distance_from_earthquake = []

    for row in json_dict:
        ab = row['geometry']
        rd = ab.get('coordinates')
        ac = row['properties']
        re = ac.get('mag')
        rf = ac.get('place')
        rg = ac.get('time')
        longitude = rd[0]
        latitude = rd[1]
        magnitude = re
        place = rf
        time = rg
        distance = haversine_distance(latitude, longitude, loc.latitude, loc.longitude)
        longlist.append(longitude)
        latlist.append(latitude)
        magnitudelist.append(magnitude)
        placelist.append(place)
        timelist.append(time)
        distance_from_earthquake.append(distance)

    d = {'longitude':longlist,'latitude':latlist,'distance':distance_from_earthquake,'magnitude': magnitudelist,'place': placelist,'time': timelist }

    #turned the dictionary into a pandas dataframe
    df = pd.DataFrame(d)
    

    column = df["distance"]
    min_value = column.min()
    
    all = df.loc[df['distance'] == min_value]
    
    
    
    
    longitude_v = all["longitude"].iloc[0]
    latitude_v = all["latitude"].iloc[0]
    distance_v = all["distance"].iloc[0]
    magnitude_v = all["magnitude"].iloc[0]
    place_v = all["place"].iloc[0]
    time_v = all["time"].iloc[0]
    # can also return df as dataframe
    
    return df

