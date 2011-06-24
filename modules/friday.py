#!/usr/bin/env python
"""
friday.py - A module about the best day of the week
Copyright (c) 2011 Dafydd Crosby - http://www.dafyddcrosby.com

Licensed under the Eiffel Forum License 2.
"""
import random

lines = [
    "Gotta get down on Friday",
    "Everybody's lookin' forward to the weekend",
    "Gettin' down on Friday",
    "Which seat can I take?",
    "Gotta have my bowl, gotta have cereal",
    "Tickin' on and on, everybody's rushin'",
    "Fun, fun, fun, fun",
    "Fun, fun, think about fun",
    "Partyin', partyin'",
    "Yesterday was Thursday, Thursday",
    "We so excited",
    "We gonna have a ball today",
    "Tomorrow is Saturday, and Sunday comes afterwards",
    "Lookin' forward to the weekend",
]

def friday(phenny,input):
    phenny.say(random.choice(lines))
friday.rule = r'(.*)(?i)friday(.*)'
friday.priority = 'low'
