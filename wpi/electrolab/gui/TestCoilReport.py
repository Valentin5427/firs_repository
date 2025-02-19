# -*- coding: UTF-8 -*-

'''
Created on 2.08.2015

@author: atol
'''

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import  QIcon, QFont
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox



import json


class TestCoilReport(QDialog, UILoader):
    def __init__(self, _env):
#    def __init__(self):
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"TestCoilReport.ui")
        self.setEnabled(False)

        self.ui.checkBox.setVisible(False)
        self.ui.checkBox_2.setVisible(False)
        #self.ui.groupBox_2.setVisible(False)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.checkBox.toggled.connect(self.checkBox_Toggle)
        self.ui.checkBox_2.toggled.connect(self.checkBox_2_Toggle)

    def pushButton_Click(self):
        self.close() 

    def checkBox_Toggle(self, check):
        self.ui.groupBox.setVisible(check)

    def checkBox_2_Toggle(self, check):
        self.ui.groupBox_2.setVisible(check)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
     
    from dpframe.base.envapp import checkenv
    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import default_log_init
    from electrolab.gui.inits import serial_devices_init
       
    @serial_devices_init
    @json_config_init
    @default_log_init    
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
                            
    wind = TestCoilReport(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())
