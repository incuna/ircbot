import re, urllib

from ircbot import web

r_li = re.compile(r'(?ims)<li>.*?</li>')
r_tag = re.compile(r'<[^>]+>')
r_parens = re.compile(r'(?<=\()(?:[^()]+|\([^)]+\))*(?=\))')
r_word = re.compile(r'^[A-Za-z0-9\' -]+$')

uri = 'http://encarta.msn.com/dictionary_/%s.html'
r_info = re.compile(
    r'(?:ResultBody"><br /><br />(.*?)&nbsp;)|(?:<b>(.*?)</b>)'
)

def dict(ircbot, input):
    if not input.group(2):
        return ircbot.reply("Nothing to define.")
    word = input.group(2)
    word = urllib.quote(word.encode('utf-8'))

    def trim(thing):
        if thing.endswith('&nbsp;'):
            thing = thing[:-6]
        return thing.strip(' :.')

    bytes = web.get(uri % word)
    results = {}
    wordkind = None
    for kind, sense in r_info.findall(bytes):
        kind, sense = trim(kind), trim(sense)
        if kind:
            wordkind = kind
        elif sense:
            results.setdefault(wordkind, []).append(sense)
    result = input.group(2).encode('utf-8') + ' - '
    for key in sorted(results.keys()):
        if results[key]:
            result += (key or '') + ' 1. ' + results[key][0]
            if len(results[key]) > 1:
                result += ', 2. ' + results[key][1]
            result += '; '
    result = result.rstrip('; ')
    if result.endswith('-') and (len(result) < 30):
        ircbot.reply('Sorry, no definition found.')
    else:
        ircbot.say(result)
dict.commands = ['dict']

