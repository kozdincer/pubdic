#!/usr/bin/env python

#############################################################################
## Copyright 2012
## Authored by Kaan Ozdincer <kaanozdincer@gmail.com>
#############################################################################

import sys
from PyQt4 import QtCore, QtGui, QtWebKit

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,300,200).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "kozdincer 's Dict", None, QtGui.QApplication.UnicodeUTF8))
        #MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #MainWindow.setWindowFlags(QtCore.Qt.Popup)
        #MainWindow.setWindowFlags(QtCore.Qt.SplashScreen)

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.WebBrowser = QtWebKit.QWebView(self.centralWidget)
        self.WebBrowser.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        self.WebBrowser.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOn)
        self.WebBrowser.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.WebBrowser.setObjectName("WebBrowser")
        self.WebBrowser.resize(QtCore.QSize(QtCore.QRect(0,0,300,200).size()))
        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
