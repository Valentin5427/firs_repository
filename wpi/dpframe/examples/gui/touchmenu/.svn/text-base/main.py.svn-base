#!/usr/bin/env python
#coding=utf-8

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt
from dpframe.gui.touchmenu import BaseTouchMenu
from dpframe.gui.menuloaders import JSONMenuLoader
from dpframe.base.envapp import checkenv
from dpframe.base.inits import json_config_init


@checkenv(u'log', u'config')
@json_config_init
class ExampleTouchMenu(BaseTouchMenu):
    pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    menu = JSONMenuLoader(u'menu.json').load()
    MainWindow = ExampleTouchMenu(menu)
    MainWindow.setWindowState(Qt.WindowFullScreen)
    MainWindow.show()
    sys.exit(app.exec_())
