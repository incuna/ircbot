# coding=utf-8
import re

from ircbot import web

r_result = re.compile(r'(?i)<A NAME=results>(.*?)</A>')
r_tag = re.compile(r'<\S+.*?>')

subs = [
    (' in ', ' -> '),
    (' over ', ' / '),
    (u'£', 'GBP '),
    (u'€', 'EUR '),
    ('\$', 'USD '),
    (r'\bKB\b', 'kilobytes'),
    (r'\bMB\b', 'megabytes'),
    (r'\bGB\b', 'kilobytes'),
    ('kbps', '(kilobits / second)'),
    ('mbps', '(megabits / second)')
]

def calc(ircbot, input):
    """Use the Frink online calculator."""
    q = input.group(2)
    if not q:
        return ircbot.say('0?')

    query = q[:]
    for a, b in subs:
        query = re.sub(a, b, query)
    query = query.rstrip(' \t')

    precision = 5
    if query[-3:] in ('GBP', 'USD', 'EUR', 'NOK'):
        precision = 2
    query = web.urllib.quote(query.encode('utf-8'))

    uri = 'http://futureboy.us/fsp/frink.fsp?fromVal='
    bytes = web.get(uri + query)
    m = r_result.search(bytes)
    if m:
        result = m.group(1)
        result = r_tag.sub('', result) # strip span.warning tags
        result = result.replace('&gt;', '>')
        result = result.replace('(undefined symbol)', '(?) ')

        if '.' in result:
            try:
                result = str(round(float(result), precision))
            except ValueError:
                pass

        if not result.strip():
            result = '?'
        elif ' in ' in q:
            result += ' ' + q.split(' in ', 1)[1]

        ircbot.say(q + ' = ' + result[:350])
    else:
        ircbot.reply("Sorry, can't calculate that.")
    ircbot.say('Note that .calc is deprecated, consider using .c')
calc.commands = ['calc']
calc.example = '.calc 5 + 3'

def c(ircbot, input):
    """Google calculator."""
    if not input.group(2):
        return ircbot.reply("Nothing to calculate.")
    q = input.group(2).encode('utf-8')
    q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
    q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
    uri = 'http://www.google.com/ig/calculator?q='
    bytes = web.get(uri + web.urllib.quote(q))
    parts = bytes.split('",')
    answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
    if answer:
        answer = answer.decode('unicode-escape')
        answer = ''.join(chr(ord(c)) for c in answer)
        answer = answer.decode('utf-8')
        answer = answer.replace(u'\xc2\xa0', ',')
        answer = answer.replace('<sup>', '^(')
        answer = answer.replace('</sup>', ')')
        answer = web.decode(answer)
        ircbot.say(answer)
    else:
        ircbot.say('Sorry, no result.')
c.commands = ['c']
c.example = '.c 5 + 3'

def py(ircbot, input):
    query = input.group(2).encode('utf-8')
    uri = 'http://tumbolia.appspot.com/py/'
    answer = web.get(uri + web.urllib.quote(query))
    if answer:
        ircbot.say(answer)
    else:
        ircbot.reply('Sorry, no result.')
py.commands = ['py']

def wa(ircbot, input):
    if not input.group(2):
        return ircbot.reply("No search term.")
    query = input.group(2).encode('utf-8')
    uri = 'http://tumbolia.appspot.com/wa/'
    answer = web.get(uri + web.urllib.quote(query))
    if answer:
        ircbot.say(answer)
    else:
        ircbot.reply('Sorry, no result.')
wa.commands = ['wa']

