import asyncio
import sys

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from twitchio import Message, Channel

import helper
from Widgets.MainWindow import MainWindow
from twitchBot import TwitchBot


class TwitchBotWorker(QObject):
    """
    Worker object used to offload the twitch bot.
    """
    # message = pyqtSignal(str)
    # progress = pyqtSignal(int)
    # finished = pyqtSignal()

    def __init__(self, bot: TwitchBot, parent=None):
        super().__init__(parent)
        self.bot = bot

    def run(self):
        self.bot.run()


class LilCrossBot:
    def __init__(self):
        self.commands = helper.commands

        self.twitchBotThread = QThread()
        self.twitchBot = TwitchBot(self)

        # Create Worker and move it to separate thread
        self.worker = TwitchBotWorker(self.twitchBot)
        self.worker.moveToThread(self.twitchBotThread)

        # Establish necessary connections
        self.twitchBotThread.started.connect(self.worker.run)

        # Start the gathering process
        self.twitchBotThread.start()

        self.channel = None
        self.loop = None

        self.gui = MainWindow(self)
        self.gui.show()

    def sendMessage(self, msg: str):
        self.loop.create_task(self.channel.send(msg))

    def setChannel(self, channel: Channel):
        self.channel = channel
        self.loop = asyncio.get_event_loop()

    def receivedMessage(self, message: Message):
        self.gui.chatWidget.addMessage(message)

    def saveChanges(self):
        # self.twitchBot.db.commit()
        print('Changes saved!')

    def onClose(self):
        self.saveChanges()
        self.twitchBotThread.deleteLater()


app = QApplication(sys.argv)
lcb = LilCrossBot()
app.exec_()
lcb.onClose()


# Catch the Ctrl+C to do a final commit to the database
# def handler(signum, frame):
#     res = input("Ctrl-C was pressed. Do you really want to exit? y/n ")
#     exit(1)
#
#
# signal.signal(signal.SIGINT, handler)

# app = QApplication(sys.argv)
# mainWindow = MainWindow()
# mainWindow.show()
# sys.exit(app.exec_())

