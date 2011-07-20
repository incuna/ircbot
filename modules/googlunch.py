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
    choice=load_places_from_google()
    phenny.say(' '.join(('Why not eat at',choice,'for lunch today?')))
choose_lunch.commands = ['googlunch', 'googfood']

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

def load_places_from_google():
    places = urllib2.urlopen('https://maps.googleapis.com/maps/api/place/search/json?location=41.882199,-87.640493&radius=500&types=food&sensor=false&key=AIzaSyAAsPseZ3FuqJysqlic-qo4EUD5PqxY0Yw').read()
    jplaces=json.loads(places)
    #print places
    return random.choice([result['name'] for result in jplaces['results']])


if __name__ == '__main_': 
   print __doc__.strip()
