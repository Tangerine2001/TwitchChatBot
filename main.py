import signal
from twitchBot import Bot

twitchBot = Bot()

# Catch the Ctrl+C to do a final commit to the database
def handler(signum, frame):
    res = input("Ctrl-C was pressed. Do you really want to exit? y/n ")
    exit(1)


signal.signal(signal.SIGINT, handler)

twitchBot.run()
