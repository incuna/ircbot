def doc(ircbot, input):
    """Shows a command's documentation, and possibly an example."""
    name = input.group(1)
    name = name.lower()

    if ircbot.doc.has_key(name):
        ircbot.reply(ircbot.doc[name][0])
        if ircbot.doc[name][1]:
            ircbot.say('e.g. ' + ircbot.doc[name][1])
doc.rule = ('$nick', '(?i)(?:help|doc) +([A-Za-z]+)(?:\?+)?$')
doc.example = '$nickname: doc tell?'
doc.priority = 'low'

def commands(ircbot, input):
    # This function only works in private message
    if input.sender.startswith('#'):
        return
    names = ', '.join(sorted(ircbot.doc.iterkeys()))
    ircbot.say('Commands I recognise: ' + names + '.')
    ircbot.say(("For help, do '%s: help example?' where example is the " +
                    "name of the command you want help for.") % ircbot.nick)
commands.commands = ['commands']
commands.priority = 'low'

def help(ircbot, input):
    response = (
        'Hi, I\'m a bot. Say ".commands" to me in private for a list ' +
        'of my commands. My owner is %s.'
    ) % ircbot.config.owner
    ircbot.reply(response)
help.rule = ('$nick', r'(?i)help(?:[?!]+)?$')
help.priority = 'low'

def stats(ircbot, input):
    """Show information on command usage patterns."""
    commands = {}
    users = {}
    channels = {}

    ignore = set(['f_note', 'startup', 'message', 'noteuri'])
    for (name, user), count in ircbot.stats.items():
        if name in ignore:
            continue
        if not user:
            continue

        if not user.startswith('#'):
            try:
                users[user] += count
            except KeyError:
                users[user] = count
        else:
            try:
                commands[name] += count
            except KeyError:
                commands[name] = count

            try:
                channels[user] += count
            except KeyError:
                channels[user] = count

    comrank = sorted([(b, a) for (a, b) in commands.iteritems()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.iteritems()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.iteritems()], reverse=True)

    # most heavily used commands
    creply = 'most used commands: '
    for count, command in comrank[:10]:
        creply += '%s (%s), ' % (command, count)
    ircbot.say(creply.rstrip(', '))

    # most heavy users
    reply = 'power users: '
    for count, user in userank[:10]:
        reply += '%s (%s), ' % (user, count)
    ircbot.say(reply.rstrip(', '))

    # most heavy channels
    chreply = 'power channels: '
    for count, channel in charank[:3]:
        chreply += '%s (%s), ' % (channel, count)
    ircbot.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'

