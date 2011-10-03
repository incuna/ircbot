def startup(ircbot, input):
    if hasattr(ircbot.config, 'serverpass'):
        ircbot.write(('PASS', ircbot.config.serverpass))

    if hasattr(ircbot.config, 'password'):
        ircbot.msg('NickServ', 'IDENTIFY %s' % ircbot.config.password)
        __import__('time').sleep(5)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in ircbot.channels:
        ircbot.write(('JOIN', channel))
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

