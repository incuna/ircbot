import random

def hello(ircbot, input):
    greeting = random.choice(('Hi', 'Hey', 'Hello'))
    punctuation = random.choice(('', '!'))
    ircbot.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) $nickname[ \t]*$'

def interjection(ircbot, input):
    ircbot.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

