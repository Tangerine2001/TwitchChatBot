import signal
import sys

from PyQt5.QtWidgets import QApplication

from Widgets.MainWindow import MainWindow
from twitchBot import TwitchBot

twitchBot = TwitchBot()

# Catch the Ctrl+C to do a final commit to the database
def handler(signum, frame):
    res = input("Ctrl-C was pressed. Do you really want to exit? y/n ")
    twitchBot.db.commit()
    exit(1)


signal.signal(signal.SIGINT, handler)

twitchBot.run()
# app = QApplication(sys.argv)
# mainWindow = MainWindow()
# mainWindow.show()
# sys.exit(app.exec_())

