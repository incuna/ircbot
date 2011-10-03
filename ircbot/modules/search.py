import re

from ircbot import web

class Grab(web.urllib.URLopener):
    def __init__(self, *args):
        self.version = 'Mozilla/5.0 (ircbot)'
        web.urllib.URLopener.__init__(self, *args)
        self.addheader('Referer', 'https://github.com/incuna/ircbot')
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        return web.urllib.addinfourl(fp, [headers, errcode], "http:" + url)

def search(query):
    """Search using AjaxSearch, and return its JSON."""
    uri = 'http://ajax.googleapis.com/ajax/services/search/web'
    args = '?v=1.0&safe=off&q=' + web.urllib.quote(query.encode('utf-8'))
    handler = web.urllib._urlopener
    web.urllib._urlopener = Grab()
    bytes = web.get(uri + args)
    web.urllib._urlopener = handler
    return web.json(bytes)

def result(query):
    results = search(query)
    try:
        return results['responseData']['results'][0]['unescapedUrl']
    except IndexError:
        return None
    except TypeError:
        print results
        return False

def count(query):
    results = search(query)
    if not results.has_key('responseData'):
        return '0'
    if not results['responseData'].has_key('cursor'):
        return '0'
    if not results['responseData']['cursor'].has_key('estimatedResultCount'):
        return '0'
    return results['responseData']['cursor']['estimatedResultCount']

def formatnumber(n):
    """Format a number with beautiful commas."""
    parts = list(str(n))
    for i in range((len(parts) - 3), 0, -3):
        parts.insert(i, ',')
    return ''.join(parts)

def g(ircbot, input):
    """Queries Google for the specified input."""
    query = input.group(2)
    if not query:
        return ircbot.reply('.g what?')
    uri = result(query)
    if uri:
        ircbot.reply(uri)
        if not hasattr(ircbot.bot, 'last_seen_uri'):
            ircbot.bot.last_seen_uri = {}
        ircbot.bot.last_seen_uri[input.sender] = uri
    elif uri is False:
        ircbot.reply("Problem getting data from Google.")
    else:
        ircbot.reply("No results found for '%s'." % query)
g.commands = ['g']
g.priority = 'high'
g.example = '.g swhack'

def gc(ircbot, input):
    """Returns the number of Google results for the specified input."""
    query = input.group(2)
    if not query:
        return ircbot.reply('.gc what?')
    num = formatnumber(count(query))
    ircbot.say(query + ': ' + num)
gc.commands = ['gc']
gc.priority = 'high'
gc.example = '.gc extrapolate'

r_query = re.compile(
    r'\+?"[^"\\]*(?:\\.[^"\\]*)*"|\[[^]\\]*(?:\\.[^]\\]*)*\]|\S+'
)

def gcs(ircbot, input):
    if not input.group(2):
        return ircbot.reply("Nothing to compare.")
    queries = r_query.findall(input.group(2))
    if len(queries) > 6:
        return ircbot.reply('Sorry, can only compare up to six things.')

    results = []
    for i, query in enumerate(queries):
        query = query.strip('[]')
        n = int((formatnumber(count(query)) or '0').replace(',', ''))
        results.append((n, query))
        if i >= 2:
            __import__('time').sleep(0.25)
        if i >= 4:
            __import__('time').sleep(0.25)

    results = [(term, n) for (n, term) in reversed(sorted(results))]
    reply = ', '.join('%s (%s)' % (t, formatnumber(n)) for (t, n) in results)
    ircbot.say(reply)
gcs.commands = ['gcs', 'comp']

r_bing = re.compile(r'<h3><a href="([^"]+)"')

def bing(ircbot, input):
    """Queries Bing for the specified input."""
    query = input.group(2)
    if query.startswith(':'):
        lang, query = query.split(' ', 1)
        lang = lang[1:]
    else:
        lang = 'en-GB'
    if not query:
        return ircbot.reply('.bing what?')

    query = web.urllib.quote(query.encode('utf-8'))
    base = 'http://www.bing.com/search?mkt=%s&q=' % lang
    bytes = web.get(base + query)
    m = r_bing.search(bytes)
    if m:
        uri = m.group(1)
        ircbot.reply(uri)
        if not hasattr(ircbot.bot, 'last_seen_uri'):
            ircbot.bot.last_seen_uri = {}
        ircbot.bot.last_seen_uri[input.sender] = uri
    else:
        ircbot.reply("No results found for '%s'." % query)
bing.commands = ['bing']
bing.example = '.bing swhack'

