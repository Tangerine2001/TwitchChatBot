from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QListWidgetItem, QListView, QLineEdit, QPushButton
from twitchio import Message, Channel

chatWidgetStyleSheet = """
QListWidget {
    background-color: rgb(115, 115, 115);
    color: black;
}

QListWidget::item {
    background-color: pink;
    border-bottom: 0.5px solid skyblue;
}

QListWidget::item:alternate {
    background-color: purple;
    border-bottom: 0.5px solid skyblue;
    color: lightgrey;
}
"""

qLineEditStyleSheet = """
QLineEdit {
    background-color: grey;
    border: 0.5px solid black;
    color: white;
}

QLineEdit:focus {
    border: 0.5px solid blue;
}

QLineEdit:hover {
    border: 0.5px solid pink;
}
"""


class ChatWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ChatWidget")

        self.setGeometry(0, 0, 741, 611)
        self.setStyleSheet(chatWidgetStyleSheet)
        self.setAlternatingRowColors(True)

        self.inputMsg = QLineEdit(self)
        # self.inputMsg.setStyleSheet(qLineEditStyleSheet)
        self.inputMsg.setGeometry(10, 545, 571, 47)
        # self.inputMsg.setGeometry(10, 560, 571, 45)

        self.sendButton = QPushButton(self)
        self.sendButton.setText('Send')
        self.sendButton.setGeometry(580, 540, 130, 58)
        # self.sendButton.setGeometry(557, 555, 130, 58)

    def addMessage(self, message: Message):
        self.addItem(ChatMessage(message))
        self.scrollToBottom()

    def sendMsg(self, lilCrossBot):
        text = self.inputMsg.text()
        if len(text) > 0:
            lilCrossBot.sendMessage(text)
            self.addMessage(text)
        self.inputMsg.setText('')
        # self.show()

    #     self.retranslateUi(self)
    #     QtCore.QMetaObject.connectSlotsByName(self)
    #
    # def retranslateUi(self, ChatWidget):
    #     _translate = QtCore.QCoreApplication.translate
    #     ChatWidget.setWindowTitle(_translate("ChatWidget", "Form"))


class ChatMessage(QListWidgetItem):
    def __init__(self, message):
        super().__init__()
        if type(message) == Message:
            self.setText(f'{message.author.name}: {message.content}')
        # This means that we executed the addMessage ourselves
        else:
            self.setText(f'LilCrossBot: {message}')

