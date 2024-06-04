#!/usr/bin/env python
#coding=utf-8

from PyQt4.QtGui import QApplication 
from dpframe.gui.mainwnd import BaseMDIMainWnd
from dpframe.gui.menuloaders import JSONMenuLoader
from dpframe.base.envapp import checkenv
from dpframe.base.inits import json_config_init


@checkenv(u'log', u'config')
@json_config_init
class ExampleMainWnd(BaseMDIMainWnd):
    
    def __init__(self, caption, menu):
        BaseMDIMainWnd.__init__(self, caption, menu)
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    menu = JSONMenuLoader(u'menu.json').load()
    MainWindow = ExampleMainWnd(u'Example Main Window', menu)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
