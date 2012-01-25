def replaced(ircbot, input):
    command = input.group(1)
    responses = {
        'cp': '.cp has been replaced by .u',
        'pc': '.pc has been replaced by .u',
        'unicode': '.unicode has been replaced by .u',
        'compare': '.compare has been replaced by .gcs (googlecounts)',
        'acronym': 'the .acronym command has been removed; ask sbp for details',
        'v': '.v has been replaced by .val',
        'validate': '.validate has been replaced by .validate',
        'web': 'the .web command has been removed; ask sbp for details',
        'origin': ".origin hasn't been ported to my new codebase yet"
    }
    try:
        response = responses[command]
    except KeyError:
        return
    else:
        ircbot.reply(response)

replaced.commands = (
    'cp', 'pc', 'unicode', 'compare', 'map', 'acronym',
    'v', 'validate', 'thesaurus', 'web', 'mangle', 'origin',
    'swhack'
)
replaced.priority = 'low'
