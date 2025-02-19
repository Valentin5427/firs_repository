﻿#coding=UTF-8
u"""
Created on 25.07.2012
#
@author: Knur
desc: 
"""



from PyQt4.QtGui import QApplication, QCursor
from PyQt4.QtCore import  Qt, QTranslator

from dpframe.base.envapp import checkenv
from dpframe.base.inits import json_config_init
from dpframe.base.inits import db_connection_init
from dpframe.base.inits import default_log_init

from electrolab.gui.inits import serial_devices_init
from electrolab.gui.verification import VerificationForm 

#@checkenv(u'log', u'config', u'db', u'devices')
@serial_devices_init
@db_connection_init
@json_config_init
@default_log_init

class MainWnd(VerificationForm):
    pass


def main():
    #from PyQt4.QtGui import QMessageBox
    #QMessageBox.warning(None, u"Предупреждение", u"Ошибка определения серии", QMessageBox.Ok)

    import wmi
    c = wmi.WMI ()
    nekz = 0
    for process in c.Win32_Process ():
        print process.Name.upper()
        if process.Name.upper() == 'WPT.EXE':
            nekz += 1
    if nekz > 1:
        return
    
    from electrolab.gui.msgbox import getTrue, msgBox
    import sys
    app = QApplication(sys.argv)
    app.setStyle(u'Cleanlooks')

    qt_translator = QTranslator()
    if qt_translator.load(u':EL/qt_ru.qm'):
        app.installTranslator( qt_translator )

    MainWindow = MainWnd()
    if MainWindow.env.winparam.fullscreen:
        MainWindow.setWindowState(Qt.WindowFullScreen)
    if MainWindow.env.winparam.nomouse:
        MainWindow.setCursor(QCursor(Qt.BlankCursor))
#    MainWindow.show()
    MainWindow.show()
    sys.exit(app.exec_())


if u'__main__' == __name__:
    main()
