# IRCBot
An IRC bot written in Python with a plugins framework.

## History
IRCBot is a [standards](http://www.python.org/dev/peps/pep-0008/) [compliant](https://github.com/sbp/phenny/pull/9) fork of the popular [Phenny](https://github.com/sbp/phenny/) IRC Bot.

## Installation
### PyPi
`pip install ircbot`

### Source Code
1. `git clone git://github.com/incuna/ircbot.git`
2. `cd ircbot`
3. `python setup.py install`
3. `ircbot` The first time this runs it creates a default config file
3. Edit ~/.ircbot/default.py and set the path to your plugins director[y|ies]
4. Run `ircbot` again to use your settings

## Authors
* [Sean B. Palmer](http://inamidst.com/sbp), Original Author
* [George Hickman](http://ghickman.co.uk), Standards Compliance, Packaging, Rolled in some other Plugins
* Youssef Attalla, Google Lunch Plugin
* [Dafydd Crosby](http://github.com/dafyddcrosby), Friday Plugin

