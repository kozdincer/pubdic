#!/usr/bin/env python

#############################################################################
## Copyright 2012
## Authored by Kaan Ozdincer <kaanozdincer@gmail.com>
#############################################################################

import sys
from PyQt4 import QtCore, QtGui
from ui_mainwindow import Ui_MainWindow
import dbus, dbus.service, dbus.glib
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, link):
        QtGui.QMainWindow.__init__(self)

        # main window
        self.setupUi(self)
        self.pb = QtGui.QProgressBar(self.statusBar())
        self.pb.setTextVisible(False)
        self.pb.show()
        self.statusBar().hide()
        self.statusBar().addPermanentWidget(self.pb)
        self.WebBrowser.load(QtCore.QUrl(link))

        # tray menu
        menu = QtGui.QMenu()
        menuActivateAction = QtGui.QAction("Activate", menu)
        menuMinimizeAction = QtGui.QAction("Minimize", menu)
        menuPropertiesAction = QtGui.QAction("Properties", menu)
        menuExitAction = QtGui.QAction("Exit", menu)
        menu.addAction(menuActivateAction)
        menu.addAction(menuMinimizeAction)
        menu.addAction(menuPropertiesAction)
        menu.addAction(menuExitAction)

        # tray icon
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        self.trayIcon.setIcon(QtGui.QIcon("/usr/share/icons/default.kde4/128x128/apps/accessories-dictionary.png"))
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.show()

    def onTrayIconActivated(self):
        print "activate tray"

    def on_WebBrowser_loadStarted(self):
        self.statusBar().show()
        self.pb.setRange(0, 100)
        self.pb.setValue(1)

    def on_WebBrowser_loadFinished(self, flag):
        if flag is True:
            self.statusBar().hide()
        self.WebBrowser.page().mainFrame().evaluateJavaScript("var parent = document.getElementsByTagName('div')[0]; \
                                                               var div1 = document.getElementsByTagName('div')[1];   \
                                                               var div2 = document.getElementsByTagName('div')[2];   \
                                                               var p = document.getElementById('wrcopyright');       \
                                                               parent.removeChild(div1);                             \
                                                               parent.removeChild(div2);                             \
                                                               parent.removeChild(p);                                \
                                                               ")

        #self.WebBrowser.page().mainFrame().setScrollPosition(QtCore.QPoint(0,110))

    def on_WebBrowser_loadProgress(self, status):
        self.statusBar().show()
        self.pb.setRange(0, 100)
        self.pb.setValue(status)

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.ActivationChange:
            if self.isActiveWindow():
                pass
                #self.show()
            elif not self.isActiveWindow():
                self.hide()

class DbusService(dbus.service.Object):
    def __init__(self, mw):
        self.app = mw
        bus_name = dbus.service.BusName('org.kozdincer.dict', bus = dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/kozdincer/dict')

    @dbus.service.method(dbus_interface='org.kozdincer.dict')
    def show_window(self):
        xSelection = app.clipboard().text(QtGui.QClipboard.Selection).trimmed()
        new_link = "http://api.wordreference.com/51923/entr/" + xSelection
        self.app.WebBrowser.load(QtCore.QUrl(new_link))
        self.app.setWindowTitle(xSelection + " | kozdincer's Dict")
        mp = QtGui.QCursor().pos()
        self.app.setGeometry(mp.x()-200, mp.y()+10, 300, 200)
        self.app.show()


if __name__ == "__main__":
    if dbus.SessionBus().request_name("org.kozdincer.dict") != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
        #print "Application is already running..."
        method = dbus.SessionBus().get_object("org.kozdincer.dict", "/org/kozdincer/dict").get_dbus_method("show_window")
        method()
    else:
        #print "Application starting..."
        word_link = "http://api.wordreference.com/51923/entr/"
        app = QtGui.QApplication(sys.argv)
        mainWindow = MainWindow(word_link)
        service = DbusService(mainWindow)
        sys.exit(app.exec_())
