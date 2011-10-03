import re, urllib

from ircbot import web

definitions = 'https://github.com/nslater/oblique/wiki'

r_item = re.compile(r'(?i)<li>(.*?)</li>')
r_tag = re.compile(r'<[^>]+>')

def mappings(uri):
    result = {}
    bytes = web.get(uri)
    for item in r_item.findall(bytes):
        item = r_tag.sub('', item).strip(' \t\r\n')
        if not ' ' in item:
            continue

        command, template = item.split(' ', 1)
        if not command.isalnum():
            continue
        if not template.startswith('http://'):
            continue
        result[command] = template.replace('&amp;', '&')
    return result

def service(ircbot, input, command, args):
    t = o.services[command]
    template = t.replace('${args}', urllib.quote(args.encode('utf-8'), ''))
    template = template.replace('${nick}', urllib.quote(input.nick, ''))
    uri = template.replace('${sender}', urllib.quote(input.sender, ''))

    info = web.head(uri)
    if isinstance(info, list):
        info = info[0]
    if not 'text/plain' in info.get('content-type', '').lower():
        return ircbot.reply("Sorry, the service didn't respond in plain text.")
    bytes = web.get(uri)
    lines = bytes.splitlines()
    if not lines:
        return ircbot.reply("Sorry, the service didn't respond any output.")
    ircbot.say(lines[0][:350])

def refresh(ircbot):
    if hasattr(ircbot.config, 'services'):
        services = ircbot.config.services
    else:
        services = definitions

    old = o.services
    o.serviceURI = services
    o.services = mappings(o.serviceURI)
    return len(o.services), set(o.services) - set(old)

def o(ircbot, input):
    """Call a webservice."""
    text = input.group(2)

    if (not o.services) or (text == 'refresh'):
        length, added = refresh(ircbot)
        if text == 'refresh':
            msg = 'Okay, found %s services.' % length
            if added:
                msg += ' Added: ' + ', '.join(sorted(added)[:5])
                if len(added) > 5:
                    msg += ', &c.'
            return ircbot.reply(msg)

    if not text:
        return ircbot.reply('Try %s for details.' % o.serviceURI)

    if ' ' in text:
        command, args = text.split(' ', 1)
    else:
        command, args = text, ''
    command = command.lower()

    if command == 'service':
        msg = o.services.get(args, 'No such service!')
        return ircbot.reply(msg)

    if not o.services.has_key(command):
        return ircbot.reply('Sorry, no such service. See %s' % o.serviceURI)

    if hasattr(ircbot.config, 'external'):
        default = ircbot.config.external.get('*')
        manifest = ircbot.config.external.get(input.sender, default)
        if manifest:
            commands = set(manifest)
            if (command not in commands) and (manifest[0] != '!'):
                return ircbot.reply('Sorry, %s is not whitelisted' % command)
            elif (command in commands) and (manifest[0] == '!'):
                return ircbot.reply('Sorry, %s is blacklisted' % command)
    service(ircbot, input, command, args)
o.commands = ['o']
o.example = '.o servicename arg1 arg2 arg3'
o.services = {}
o.serviceURI = None

def snippet(ircbot, input):
    if not o.services:
        refresh(ircbot)

    search = urllib.quote(input.group(2).encode('utf-8'))
    py = "BeautifulSoup.BeautifulSoup(re.sub('<.*?>|(?<= ) +', '', " + \
          "''.join(chr(ord(c)) for c in " + \
          "eval(urllib.urlopen('http://ajax.googleapis.com/ajax/serv" + \
          "ices/search/web?v=1.0&q=" + search + "').read()" + \
          ".replace('null', 'None'))['responseData']['resul" + \
          "ts'][0]['content'].decode('unicode-escape')).replace(" + \
          "'&quot;', '\x22')), convertEntities=True)"
    service(ircbot, input, 'py', py)
snippet.commands = ['snippet']

