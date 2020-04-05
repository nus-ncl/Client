#-*- coding:utf-8 -*-
'''
QFileDialog
'''

# from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFileDialog, QPushButton, QLineEdit, QGridLayout
from PySide2.QtWidgets import QApplication, QDialog,QWidget, QFileDialog, QPushButton, QLineEdit, QGridLayout
from PySide2 import QtCore
import sys
import os


class FileDialog(QDialog):
    def __init__(self):
        super(FileDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QFileDialog")
        self.setGeometry(400,400,300,260)
        self.cwd = os.getcwd()

        self.fileButton = QPushButton("Choose XML File")
        self.fileLineEdit = QLineEdit()
        # self.fileButton.clicked.connect(lambda:self.openFile(self.fileLineEdit.text()))
        self.fileButton.clicked.connect(lambda:self.openFile(self.cwd))
        # QtCore.QObject.connect(self.fileButton, QtCore.SIGNAL("clicked()"), self.openFile(self.cwd))
        # QtCore.QMetaObject.connectSlotsByName(self)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.fileButton,0,0)
        self.mainLayout.addWidget(self.fileLineEdit,0,1)

        self.setLayout(self.mainLayout)

    def openFile(self,filePath):
        if os.path.exists(filePath):
            path = QFileDialog.getOpenFileName(self,"Open File Dialog",filePath,"XML files(*.xml)")
        else:
            path = QFileDialog.getOpenFileName(self,"Open File Dialog","/","XML files(*.xml)")

        self.fileLineEdit.setText(str(path[0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialog()
    ex.show()
    sys.exit(app.exec_())