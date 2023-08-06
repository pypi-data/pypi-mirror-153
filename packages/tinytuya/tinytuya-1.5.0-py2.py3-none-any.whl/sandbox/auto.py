import readline

path = "~"
# Terminal Color Formatting
bold = "\033[0m\033[97m\033[1m"
subbold = "\033[0m\033[32m"
normal = "\033[97m\033[0m"
dim = "\033[0m\033[97m\033[2m"
alert = "\033[0m\033[91m\033[1m"
alertdim = "\033[0m\033[91m\033[2m"
COMMANDS = ['help', 'ls', 'poll', 'wizard', 'exit', 'dir', 'cat']
commands_string = ",".join(COMMANDS)
commands_sorted = sorted(COMMANDS)
print(commands_sorted)
HELP = "\n" + bold + "Commands: " + commands_string

def complete(text, state):
    # try to auto-complete commands
    print("text = %s state = %r" % (text,state))
    response = None
    if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                matches = [s 
                                for s in commands_sorted
                                if s and s.startswith(text)]
            else:
                matches = commands_sorted[:]
    # Return the state'th item from the match list,
    # if we have that many.
    try:
        response = matches[state]
    except IndexError:
        response = None
    print("response = %r" % response)
    return response

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

line = input(subbold + "Tuya" + bold + ":" + dim + path + normal + "> ")
print(line)
print(line)
print(line)
print(line)