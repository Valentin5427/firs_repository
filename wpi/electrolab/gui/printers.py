# -*- coding: UTF-8 -*-work
#
'''
Created on 14.03.2018

@author: atol
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
import ui.ico_64_rc
import win32print        
import json


#import serial.tools.list_ports 
import serial

p = []
ports = []
for i in range(256):
    ports.append('com' + str(i))
    
#for port in ['com1','com2','com3','com4','com5','com6','com7','com8','com9','com10']:
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        p.append(port)
    except (OSError, serial.SerialException):
        pass
print p


#print serial.tools.list_ports 
#print(list(serial.tools.list_ports.comports())) 


class Printers(QtGui.QDialog, UILoader):
    def __init__(self, _env):
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"printers.ui")

        # Считываем локальные принтеры в системе        
        try:
            for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None,1)):
                self.ui.comboBox.addItem(pName)
                self.ui.comboBox_2.addItem(pName)
        except:
            print 'Could not get local printers list.'        
        # Считываем сетевые принтеры в системе        
        try:
            for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS,None,1)):
                self.ui.comboBox.addItem(pName)
                self.ui.comboBox_2.addItem(pName)
        except:
            print 'Could not get network printers list.'        

        self.ui.pushButton.setEnabled(False)

        self.read_config()
                
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))

        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_indexChange)
        self.ui.comboBox_2.currentIndexChanged.connect(self.comboBox_indexChange)
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)


    def read_config(self):
        # Чтение параметров с config.json файла, если таковой имеется
        try:
            f = open('config.json','r')
            self.data = json.load(f)
            
            # Проверяем, присутствуют ли принтеры из файла config.json среди списка принтеров прикрепленных к компьютеру            
            try:
                report = self.data['printers']['report']
            except Exception:
                report = ''
            try:
                sticker = self.data['printers']['sticker']
            except Exception:
                sticker = ''

            for i in range(self.ui.comboBox.count()):
                if self.ui.comboBox.itemText(i) == report:
                   self.ui.comboBox.setCurrentIndex(i)
                   i = -1
                   break
            if i != -1:
                self.ui.pushButton.setEnabled(True)
                if report == '':
                    QMessageBox.warning(None, u"Предупреждение", u"Информация о принтере для печати отчетов отсутствует!'", QMessageBox.Ok)
                else:
                    QMessageBox.warning(None, u"Предупреждение", u"Принтер для печати отчетов: '" + self.data['printers']['report'] + "'\nотсутствует среди прикрепленных к данному компьютеру принтеров!" , QMessageBox.Ok)

            for i in range(self.ui.comboBox_2.count()):
                if self.ui.comboBox_2.itemText(i) == sticker:
                   self.ui.comboBox_2.setCurrentIndex(i)
                   i = -1
                   break
            if i != -1:
                self.ui.pushButton.setEnabled(True)
                if sticker == '':
                    QMessageBox.warning(None, u"Предупреждение", u"Информация о принтере для печати этикеток отсутствует!'", QMessageBox.Ok)
                else:    
                    QMessageBox.warning(None, u"Предупреждение", u"Принтер для печати этикеток: '" + self.data['printers']['sticker'] + "'\nотсутствует среди прикрепленных к данному компьютеру принтеров!" , QMessageBox.Ok)                
        except Exception:
            print u'Ошибка чтения config.json!'
            QMessageBox.warning(None, u"Предупреждение", u"Ошибка чтения config.json!", QMessageBox.Ok)
            self.data = {}


    def write_json(self):
        # ЗАПИСАТЬ
        f = open('config.json','w')                
        try:
            del self.data['printers']
        except Exception:
            pass
        self.data['printers']= {"report": str(self.ui.comboBox.currentText()),"sticker": str(self.ui.comboBox_2.currentText())}
        json.dump(self.data, f, indent=4, sort_keys=False)
        

    def comboBox_indexChange(self):
        self.ui.pushButton.setEnabled(True)

    def pushButton_Click(self):
        self.ui.pushButton.setEnabled(False)
        self.write_json()

    def pushButton_2_Click(self):
        if self.ui.pushButton.isEnabled():
            if getTrue(self, u'Сохранить измененные настройки?'):
                self.pushButton_Click()        
        self.close()    


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
    
    wind = Printers(env)
    wind.setEnabled(True)
    wind.show()
    
    sys.exit(app.exec_())
