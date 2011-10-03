"""
googlunch.py - Phenny lunch selection module using google maps API
By Youssef Attalla
Ref. Ori Rawlings
"""
import random
import os
import urllib2
import json

from textwrap import dedent as trim

default = """\
    {
        'address': '',
        'api_key': '',
        'latitude': '',
        'longtitude': ''
    }
    # EOF
    """

def choose_lunch(ircbot, input):
    lat,lng,choice=load_places_from_google()
    tiny_url=get_directions(lat,lng)
    ircbot.say(' '.join(('Why not eat at',choice,'for lunch today?')))
    ircbot.say(tiny_url)
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
        f.write(default)
    except IOError as e:
        print e
        return False
    finally:
        f.close()
    return True

def get_places_list():
    url = 'https://maps.googleapis.com/maps/api/place/search/json?location=%s,%s&radius=500&types=food&sensor=false&key=%s'
    conf = json.loads(os.path.join(os.path.expanduser('~/.ircbot'), 'googlunch.json'))
    if ensure(conf):
        url % (conf.latitude, conf.longitude, conf.api_key)
        return urllib2.urlopen(url).read()
    else:
        return None

def load_places_from_google():
    jplaces = json.loads(get_places_list())
    list_geo = [result['geometry'] for result in jplaces['results']]
    list_names = [result['name'] for result in jplaces['results']]
    index = int(random.uniform(0,len(list_geo)))
    name = list_names[index]
    lat = list_geo[index]['location']['lat']
    lng = list_geo[index]['location']['lng']
    str_lat = "%10.15f" % lat
    str_lng = "%10.15f" % lng
    return (str_lat,str_lng,name)

