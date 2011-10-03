def join(ircbot, input):
    """Join the specified channel. This is an admin-only command."""
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'):
        return
    if input.admin:
        channel, key = input.group(1), input.group(2)
        if not key:
            ircbot.write(['JOIN'], channel)
        else:
            ircbot.write(['JOIN', channel, key])
join.rule = r'\.join (#\S+)(?: *(\S+))?'
join.priority = 'low'
join.example = '.join #example or .join #example key'

def part(ircbot, input):
    """Part the specified channel. This is an admin-only command."""
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'):
        return
    if input.admin:
        ircbot.write(['PART'], input.group(2))
part.commands = ['part']
part.priority = 'low'
part.example = '.part #example'

def quit(ircbot, input):
    """Quit from the server. This is an owner-only command."""
    # Can only be done in privmsg by the owner
    if input.sender.startswith('#'):
        return
    if input.owner:
        ircbot.write(['QUIT'])
        __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'

def msg(ircbot, input):
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'):
        return
    a, b = input.group(2), input.group(3)
    if (not a) or (not b):
        return
    if input.admin:
        ircbot.msg(a, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.priority = 'low'

def me(ircbot, input):
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'):
        return
    if input.admin:
        msg = '\x01ACTION %s\x01' % input.group(3)
        ircbot.msg(input.group(2), msg)
me.rule = (['me'], r'(#?\S+) (.*)')
me.priority = 'low'

