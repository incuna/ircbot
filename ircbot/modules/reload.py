import sys, os.path, time, imp

def f_reload(ircbot, input):
    """Reloads a module, for use by admins only."""
    if not input.admin:
        return

    name = input.group(2)
    if name == ircbot.config.owner:
        return ircbot.reply('What?')

    if (not name) or (name == '*'):
        ircbot.setup()
        return ircbot.reply('done')

    if not sys.modules.has_key(name):
        return ircbot.reply('%s: no such module!' % name)

    # Thanks to moot for prodding me on this
    path = sys.modules[name].__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return ircbot.reply('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'):
        module.setup(ircbot)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    ircbot.register(vars(module))
    ircbot.bind_commands()

    ircbot.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'
f_reload.thread = False

