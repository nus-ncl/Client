# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScrollUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import os
import PySide6
from PySide6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cwd = os.getcwd()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 1
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 120, 471, 241))
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 60, 60))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 467, 237))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.treeWidget = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 471, 231))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 60, 469, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(PySide6.QtGui.QFont.Weight(75))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # 2
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(280, 382, 208, 64))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(24, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(24, 0))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(24, 0))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        # add
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(280, 450, 208, 210))
        # self.widget.setGeometry(QtCore.QRect(280, 450, 208, 64))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # # empty line
        # self.emptyhorizontalLayout1 = QtWidgets.QHBoxLayout()
        # self.emptyhorizontalLayout1.setObjectName("horizontalLayout5")
        # emptyline1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.emptyhorizontalLayout1.addItem(emptyline1)
        # self.verticalLayout.addLayout(self.emptyhorizontalLayout1)

        # Platform:
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        spacerItemplatformLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                       QtWidgets.QSizePolicy.Minimum)
        self.label_platform = QtWidgets.QLabel(self.widget)
        self.label_platform.setObjectName("label_platform")
        spacerItemplatformRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                        QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItemplatformLeft)
        self.horizontalLayout1.addWidget(self.label_platform)
        self.horizontalLayout1.addItem(spacerItemplatformRight)
        self.verticalLayout.addLayout(self.horizontalLayout1)

        #
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout2.addWidget(self.radioButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem)
        self.radioButton = QtWidgets.QRadioButton(self.widget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout2.addWidget(self.radioButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout2.addWidget(self.radioButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout2)

        # # empty line
        # self.emptyhorizontalLayout2 = QtWidgets.QHBoxLayout()
        # self.emptyhorizontalLayout2.setObjectName("horizontalLayout5")
        # emptyline2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.emptyhorizontalLayout2.addItem(emptyline2)
        # self.verticalLayout.addLayout(self.emptyhorizontalLayout2)

        # Connection
        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        spacerItemVMConnectionLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                           QtWidgets.QSizePolicy.Minimum)
        self.label_Connection = QtWidgets.QLabel(self.widget)
        self.label_Connection.setObjectName("label_Connection")
        spacerItemVMConnectionRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout3.addItem(spacerItemVMConnectionLeft)
        self.horizontalLayout3.addWidget(self.label_Connection)
        self.horizontalLayout3.addItem(spacerItemVMConnectionRight)
        self.verticalLayout.addLayout(self.horizontalLayout3)

        #
        self.horizontalLayout4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout4.setObjectName("horizontalLayout4")
        self.radioButton_4 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_4.setObjectName("radioButton_4")
        self.horizontalLayout4.addWidget(self.radioButton_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout4.addItem(spacerItem2)
        self.radioButton_5 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_5.setObjectName("radioButton_5")
        self.horizontalLayout4.addWidget(self.radioButton_5)
        # spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout4.addItem(spacerItem3)
        # self.radioButton_6 = QtWidgets.QRadioButton(self.widget)
        # self.radioButton_6.setObjectName("radioButton_6")
        # self.horizontalLayout4.addWidget(self.radioButton_6)
        self.verticalLayout.addLayout(self.horizontalLayout4)

        # # empty line
        # self.emptyhorizontalLayout3 = QtWidgets.QHBoxLayout()
        # self.emptyhorizontalLayout3.setObjectName("horizontalLayout5")
        # emptyline3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.emptyhorizontalLayout3.addItem(emptyline3)
        # self.verticalLayout.addLayout(self.emptyhorizontalLayout3)

        # Node Connection
        # self.horizontalLayout5 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout5.setObjectName("horizontalLayout5")
        # spacerItemNodeConnectionLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
        #                                                      QtWidgets.QSizePolicy.Minimum)
        # self.label_Node_Connection = QtWidgets.QLabel(self.widget)
        # self.label_Node_Connection.setObjectName("label_Node_Connection")
        # spacerItemNodeConnectionRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
        #                                                       QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout5.addItem(spacerItemNodeConnectionLeft)
        # self.horizontalLayout5.addWidget(self.label_Node_Connection)
        # self.horizontalLayout5.addItem(spacerItemNodeConnectionRight)
        # self.verticalLayout.addLayout(self.horizontalLayout5)
        #
        # #
        # self.horizontalLayout6 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout6.setObjectName("horizontalLayout6")
        # self.radioButton_6 = QtWidgets.QRadioButton(self.widget)
        # self.radioButton_6.setObjectName("radioButton_2")
        # self.horizontalLayout6.addWidget(self.radioButton_6)
        # spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout6.addItem(spacerItem)
        # spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout6.addItem(spacerItem1)
        # self.radioButton_7 = QtWidgets.QRadioButton(self.widget)
        # self.radioButton_7.setObjectName("radioButton_7")
        # self.horizontalLayout6.addWidget(self.radioButton_7)
        # self.verticalLayout.addLayout(self.horizontalLayout6)

        self.bg1 = QtWidgets.QButtonGroup()
        self.bg1.addButton(self.radioButton, 1)
        self.bg1.addButton(self.radioButton_2, 2)
        self.bg1.addButton(self.radioButton_3, 3)
        self.bg2 = QtWidgets.QButtonGroup()
        self.bg2.addButton(self.radioButton_4, 4)
        self.bg2.addButton(self.radioButton_5, 5)
        # self.bg2.addButton(self.radioButton_6, 6)
        # self.bg3 = QtWidgets.QButtonGroup()
        # self.bg3.addButton(self.radioButton_6, 6)
        # self.bg3.addButton(self.radioButton_7, 7)

        # 3
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"),
                               MainWindow.doubleclick)
        self.pushButton.clicked.connect(lambda: MainWindow.openFile(self.cwd))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.bg1.buttonClicked.connect(MainWindow.platform_Connection_Clicked)
        self.bg2.buttonClicked.connect(MainWindow.platform_Connection_Clicked)
        # self.bg3.buttonClicked.connect(MainWindow.platform_Connection_Clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SSH Tunnel & Rdesktop Tool"))
        self.label_2.setText(_translate("MainWindow", "User"))
        self.label_3.setText(_translate("MainWindow", "XML File"))
        self.label_platform.setText(_translate("MainWindow", "----------Local Platform-------------"))
        self.label_Connection.setText(_translate("MainWindow", "-------Connection Method---------"))
        # self.label_Node_Connection.setText(_translate("MainWindow", "--------Node Connection--------"))
        self.pushButton.setText(_translate("MainWindow", "XML"))
        self.radioButton_2.setText(_translate("MainWindow", "Win"))
        self.radioButton.setText(_translate("MainWindow", "Linux"))
        self.radioButton_3.setText(_translate("MainWindow", "MacOS"))
        self.radioButton_4.setText(_translate("MainWindow", "Console"))
        self.radioButton_5.setText(_translate("MainWindow", "SSH"))
        # self.radioButton_6.setText(_translate("MainWindow", "VNC"))
        # self.radioButton_7.setText(_translate("MainWindow", "SSH"))

