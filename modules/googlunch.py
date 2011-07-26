#!/usr/bin/env python

"""
googlunch.py - Phenny lunch selection module using google maps API
By Youssef Attalla
Ref. Ori Rawlings
"""
import random
import os
import urllib2
import json

default = 'Cafe Baci'

def choose_lunch(phenny, input):
    lat,lng,choice=load_places_from_google()
    tiny_url=get_directions(lat,lng)
    #print tiny_url
    phenny.say(' '.join(('Why not eat at',choice,'for lunch today?')))
    phenny.say(tiny_url)
choose_lunch.commands = ['googlunch', 'googfood','gl']

def get_directions(lat,lng):
    big_url='http://maps.google.com/maps?saddr=500+W+Madison+St,+Chicago,+IL+60606&daddr='+lat+','+lng+'&dirflg=w'
    return urllib2.urlopen("http://tinyurl.com/api-create.php?url="+big_url).read()



def ensure(path):
    if os.path.isfile(path):
        return True
    print path, 'does not exist as file'
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        try:
            print 'Creating directory:', d
            os.makedirs(d)
        except OSError as e:
            print e
            return False
    print 'Opening', path, 'for writing'
    try:
        f = open(path, 'w+')
    except IOError as e:
        print e
        return False
    try:
        f.write(default)
    except IOError as e:
        print e
        return False
    finally:
        f.close()
    return True

#Having only the Api Key in the Conf File for now
#To be changed later with more configuration items
def load_api_key():
    conf_file = os.path.join(os.path.expanduser('~/.phenny'),'googlunch_config.txt')
    if ensure(conf_file):
        return [l.strip() for l in open(conf_file)] 
    else:
        return null   

def load_places_from_google():
    api_key=load_api_key()
    url='https://maps.googleapis.com/maps/api/place/search/json?location=41.882199,-87.640493&radius=500&types=food&sensor=false&key='+api_key[0]
    places = urllib2.urlopen(url).read()
    jplaces=json.loads(places)
    #print places
    list_geo = [result['geometry'] for result in jplaces['results']]
    list_names = [result['name'] for result in jplaces['results']]
    index = int(random.uniform(0,len(list_geo)))
    name = list_names[index] 
    lat = list_geo[index]['location']['lat']
    lng = list_geo[index]['location']['lng']
    str_lat="%10.15f"%lat
    str_lng="%10.15f"%lng
    return (str_lat,str_lng,name) 

if __name__ == '__main_': 
   print __doc__.strip()
