#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, json, re, tweepy
from bs4 import BeautifulSoup

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

f = open("posted.txt", "r+")
posted = f.read().strip()
quakeData = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_hour.geojson").json()
hashTag = ""

if quakeData["metadata"]["count"] != 0:
    for quake in quakeData["features"]:
        place = quake["properties"]["place"].replace(" ", "")
        mag = quake["properties"]["mag"]
        quakeID = quake["properties"]["ids"].strip(',')
        if (quakeID not in posted):
            if "ofthe" in place or "of" in place:
                location = re.search("ofthe(.*)", place)
                try:
                    hashTag = " #" + location.group(1) + "Earthquake"
                except AttributeError:
                    location = re.search("of(.*),", place)
                    try:
                        hashTag = " #" + location.group(1) + "Earthquake"
                    except AttributeError:
                        location = re.search("of(.*)", place)
                        hashTag = " #" + location.group(1) + "Earthquake"
            
            baseMessage = "A magnitude " + str(mag) + " #earthquake has occurred at " + quake["properties"]["place"] + "."
            tsunamiWarning = " Possible #tsunami warning, please seek higher ground immediately."
            safetyInfo = " See https://bit.ly/2Un5VUR for safety info."
            warning = u'\U00002757' + u'\U00002757' + "WARNING" + u'\U00002757' + u'\U00002757'
            
            if "region" in baseMessage:
                baseMessage.replace(" region", "")
            if quake["properties"]["tsunami"] == 1 and mag >= 6:
                baseMessage = warning + baseMessage + tsunamiWarning + safetyInfo + hashTag
            api.update_status(baseMessage)
            f.write(quakeID + "\n")
