from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style

COMMANDS = NestedCompleter.from_nested_dict({
    'help': None,
    'ls': None,
    'poll': None,
    'wizard': None,
    'dir': None,
    'cat': None,
    'version': None,
    'cd': {
        'version': None,
        'clock': None,
        'ip': {
            'interface': {'brief'}
        }
    },
    'exit': None,
})

#cCOMMANDS = ['help', 'ls', 'poll', 'wizard', 'exit', 'dir', 'cat']

path = "~"
# Terminal Color Formatting
bold = "\033[0m\033[97m\033[1m"  # reset - bright white - bold
subbold = "\033[0m\033[32m" # reset - green 
normal = "\033[97m\033[0m" # bright white - normal
dim = "\033[0m\033[97m\033[2m"  # reset - bright white - faint
alert = "\033[0m\033[91m\033[1m" # reset - bright red - bold
alertdim = "\033[0m\033[91m\033[2m" # reset - bright red - faint

style = Style.from_dict({
    # User input (default text).
    '':          'ansiwhite',

    # Prompt.
    'tuya':     'ansigreen',
    'colon':    'ansiwhite',
    'path':     'ansidarkgray',
    'pound':    'ansiwhite',
})

message = [
    ('class:tuya', 'Tuya'),
    ('class:colon',    ':'),
    ('class:path',     path),
    ('class:pound',    '> '),
]

text = prompt(message, style=style, completer=completer)

COMMANDS = ['help', 'ls', 'poll', 'wizard', 'exit', 'dir', 'cat']

# pmt = subbold + "Tuya" + bold + ":" + dim + path + normal + "> "
# text = prompt(pmt, completer=completer)

print('You said: %s' % text)
