import os, time, random

def loadReminders(fn):
    result = {}
    f = open(fn)
    for line in f:
        line = line.strip()
        if line:
            try:
                tellee, teller, verb, timenow, msg = line.split('\t', 4)
            except ValueError:
                continue # @@ hmm
            result.setdefault(tellee, []).append((teller, verb, timenow, msg))
    f.close()
    return result

def dumpReminders(fn, data):
    f = open(fn, 'w')
    for tellee in data.iterkeys():
        for remindon in data[tellee]:
            line = '\t'.join((tellee,) + remindon)
            try:
                f.write(line + '\n')
            except IOError:
                break
    try:
        f.close()
    except IOError:
        pass
    return True

def setup(self):
    fn = self.nick + '-' + self.config.host + '.tell.db'
    self.tell_filename = os.path.join(os.path.expanduser('~/.ircbot'), fn)
    if not os.path.exists(self.tell_filename):
        try:
            f = open(self.tell_filename, 'w')
        except OSError:
            pass
        else:
            f.write('')
            f.close()
    self.reminders = loadReminders(self.tell_filename) # @@ tell

def f_remind(ircbot, input):
    teller = input.nick

    # @@ Multiple comma-separated tellees? Cf. Terje, #swhack, 2006-04-15
    verb, tellee, msg = input.groups()
    verb = verb.encode('utf-8')
    tellee = tellee.encode('utf-8')
    msg = msg.encode('utf-8')

    tellee_original = tellee.rstrip('.,:;')
    tellee = tellee_original.lower()

    if not os.path.exists(ircbot.tell_filename):
        return

    if len(tellee) > 20:
        return ircbot.reply('That nickname is too long.')

    timenow = time.strftime('%d %b %H:%MZ', time.gmtime())
    if not tellee in (teller.lower(), ircbot.nick, 'me'):
        # @@ <deltab> and year, if necessary
        if not ircbot.reminders.has_key(tellee):
            ircbot.reminders[tellee] = [(teller, verb, timenow, msg)]
        else:
            ircbot.reminders[tellee].append((teller, verb, timenow, msg))
        # @@ Stephanie's augmentation
        response = "I'll pass that on when %s is around." % tellee_original

        rand = random.random()
        if rand > 0.9999:
            response = "yeah, yeah"
        elif rand > 0.999:
            response = "yeah, sure, whatever"

        ircbot.reply(response)
    elif teller.lower() == tellee:
        ircbot.say('You can %s yourself that.' % verb)
    else:
        ircbot.say("Hey, I'm not as stupid as Monty you know!")

    dumpReminders(ircbot.tell_filename, ircbot.reminders) # @@ tell
f_remind.rule = ('$nick', ['tell', 'ask'], r'(\S+) (.*)')

def getReminders(ircbot, channel, key, tellee):
    lines = []
    template = "%s: %s <%s> %s %s %s"
    today = time.strftime('%d %b', time.gmtime())

    for (teller, verb, datetime, msg) in ircbot.reminders[key]:
        if datetime.startswith(today):
            datetime = datetime[len(today)+1:]
        lines.append(template % (tellee, datetime, teller, verb, tellee, msg))

    try:
        del ircbot.reminders[key]
    except KeyError:
        ircbot.msg(channel, 'Er...')
    return lines

def message(ircbot, input, maximum=4):
    if not input.sender.startswith('#'):
        return

    tellee = input.nick
    channel = input.sender

    if not os.path.exists(ircbot.tell_filename):
        return

    reminders = []
    remkeys = list(reversed(sorted(ircbot.reminders.keys())))
    for remkey in remkeys:
        if not remkey.endswith('*') or remkey.endswith(':'):
            if tellee.lower() == remkey:
                reminders.extend(getReminders(ircbot, channel, remkey, tellee))
        elif tellee.lower().startswith(remkey.rstrip('*:')):
            reminders.extend(getReminders(ircbot, channel, remkey, tellee))

    for line in reminders[:maximum]:
        ircbot.say(line)

    if reminders[maximum:]:
        ircbot.say('Further messages sent privately')
        for line in reminders[maximum:]:
            ircbot.msg(tellee, line)

    if len(ircbot.reminders.keys()) != remkeys:
        dumpReminders(ircbot.tell_filename, ircbot.reminders) # @@ tell
message.rule = r'(.*)'
message.priority = 'low'

