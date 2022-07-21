from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QListWidgetItem
from twitchio import Message


class ChatWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ChatWidget")

        self.setGeometry(0, 0, 741, 611)
        self.setStyleSheet("alternate-background-color: rgb(57, 57, 57);\n"
                           "background-color: rgb(115, 115, 115);\n"
                           "color: white;")
        self.setAlternatingRowColors(True)

    def addMessage(self, message: Message):
        self.addItem(QListWidgetItem(f'{message.author.name}: {message.content}'))
        # self.show()

    #     self.retranslateUi(self)
    #     QtCore.QMetaObject.connectSlotsByName(self)
    #
    # def retranslateUi(self, ChatWidget):
    #     _translate = QtCore.QCoreApplication.translate
    #     ChatWidget.setWindowTitle(_translate("ChatWidget", "Form"))
