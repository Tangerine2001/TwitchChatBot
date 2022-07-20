from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QListWidget, QStackedWidget, QLabel

import helper
from Widgets.ChatWidget import ChatWidget
from Widgets.CommandsTable import CommandsTable

qPushButtonStyle = """
QPushButton {
    border-radius: 0;
    background-color: #4287f5;
    transition: background-color 1.0s ease;
}

QPushButton:hover {
    border-radius: 10px;
    background-color: #639af2;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(800, 599)

        self.chatWidget = ChatWidget()
        self.commandsTable = CommandsTable(helper.commands)
        # self.chatWidget.setStyleSheet("alternate-background-color: rgb(57, 57, 57);\n"
        #                               "background-color: rgb(115, 115, 115);\n"
        #                               "font-color: white;")
        # self.chatWidget.setAlternatingRowColors(True)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.chatButton = QPushButton(self.centralwidget)
        self.chatButton.setGeometry(QtCore.QRect(0, 0, 61, 51))
        self.chatButton.setStyleSheet(qPushButtonStyle)
        self.chatButton.setObjectName("chatButton")
        self.chatButton.clicked.connect(lambda: self.setContentWidget(0))

        self.commandsButton = QPushButton(self.centralwidget)
        self.commandsButton.setGeometry(QtCore.QRect(0, 60, 61, 51))
        self.commandsButton.setStyleSheet(qPushButtonStyle)
        self.commandsButton.setObjectName("commandsButton")
        self.commandsButton.clicked.connect(lambda: self.setContentWidget(1))

        self.rulesButton = QPushButton(self.centralwidget)
        self.rulesButton.setGeometry(QtCore.QRect(0, 120, 61, 51))
        self.rulesButton.setStyleSheet(qPushButtonStyle)
        self.rulesButton.setObjectName("rulesButton")

        self.usersButton = QPushButton(self.centralwidget)
        self.usersButton.setGeometry(QtCore.QRect(0, 190, 61, 51))
        self.usersButton.setStyleSheet(qPushButtonStyle)
        self.usersButton.setObjectName("usersButton")

        self.contentWidget = QStackedWidget(self.centralwidget)
        self.contentWidget.setGeometry(QRect(60, 0, 800, 600))
        self.contentWidget.setObjectName("contentWidget")

        self.contentWidget.addWidget(self.chatWidget)
        self.contentWidget.addWidget(self.commandsTable)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setContentWidget(self, index: int):
        self.contentWidget.setCurrentIndex(index)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chatButton.setText(_translate("MainWindow", "Chat"))
        self.commandsButton.setText(_translate("MainWindow", "Commands"))
        self.rulesButton.setText(_translate("MainWindow", "Rules"))
        self.usersButton.setText(_translate("MainWindow", "Users"))
