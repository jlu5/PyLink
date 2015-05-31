import string
import proto

global bot_commands
# This should be a mapping of command names to functions
bot_commands = {}

# From http://www.inspircd.org/wiki/Modules/spanningtree/UUIDs.html
chars = string.digits + string.ascii_uppercase
iters = [iter(chars) for _ in range(6)]
a = [next(i) for i in iters]

def next_uid(sid, level=-1):
    try:
        a[level] = next(iters[level])
        return sid + ''.join(a)
    except StopIteration:
        return UID(level-1)

def msg(irc, target, text, notice=False):
    command = 'NOTICE' if notice else 'PRIVMSG'
    proto._sendFromUser(irc, '%s %s :%s' % (command, target, text))

def add_cmd(func, name=None):
    if name is None:
        name = func.__name__
    name = name.lower()
    bot_commands[name] = func
