# -*- coding: UTF-8 -*-work
#
'''
Created on 20.10.2017

@author: atol
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from serial import Serial
from serial.serialutil import SerialException
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
from devices import Devices, crc16

import time
import datetime
import json


class Warming_setup(QtGui.QDialog, UILoader):    
    def __init__(self, _env):
        
        super(QWidget, self).__init__()

        self.setUI(_env.config, u"Warming_setup.ui")
        
        self.port = Serial()
        
        self.Devices = Devices(_env)
        global DEV
        DEV = Devices(_env)
        
        data = [{'type':'self.ui.comboBox'}]

   #     self.msleep(100)
        
        # Списки к массиву приборов
        # типы        
        self.TypesV = [QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox()]
        self.TypesV[0] = self.ui.comboBox_2
        self.TypesV[1] = self.ui.comboBox_3
        self.TypesV[2] = self.ui.comboBox_4
        self.TypesV[3] = self.ui.comboBox_5
        self.TypesA = [QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox()]
        self.TypesA[0] = self.ui.comboBox_6
        self.TypesA[1] = self.ui.comboBox_7
        self.TypesA[2] = self.ui.comboBox_8
        self.TypesA[3] = self.ui.comboBox_9
        
        # адреса
        self.AddressV = [QtGui.QSpinBox, QtGui.QSpinBox, QtGui.QSpinBox, QtGui.QSpinBox]
        self.AddressV[0] = self.ui.spinBox_2
        self.AddressV[1] = self.ui.spinBox_3
        self.AddressV[2] = self.ui.spinBox_4
        self.AddressV[3] = self.ui.spinBox_5
        self.AddressA = [QtGui.QSpinBox, QtGui.QSpinBox, QtGui.QSpinBox, QtGui.QSpinBox]
        self.AddressA[0] = self.ui.spinBox_6
        self.AddressA[1] = self.ui.spinBox_7
        self.AddressA[2] = self.ui.spinBox_8
        self.AddressA[3] = self.ui.spinBox_9
        
        # единицы измерения
        self.MeasuresV = [QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox()]
        self.MeasuresV[0] = self.ui.comboBox_10
        self.MeasuresV[1] = self.ui.comboBox_11
        self.MeasuresV[2] = self.ui.comboBox_12
        self.MeasuresV[3] = self.ui.comboBox_13        
        self.MeasuresA = [QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox(), QtGui.QComboBox()]
        self.MeasuresA[0] = self.ui.comboBox_14
        self.MeasuresA[1] = self.ui.comboBox_15
        self.MeasuresA[2] = self.ui.comboBox_16
        self.MeasuresA[3] = self.ui.comboBox_17
        
        # кнопки
        self.TestButtonsV = [QtGui.QPushButton(), QtGui.QPushButton(), QtGui.QPushButton(), QtGui.QPushButton()]
        self.TestButtonsV[0] = self.ui.pushButton_2
        self.TestButtonsV[1] = self.ui.pushButton_3
        self.TestButtonsV[2] = self.ui.pushButton_4
        self.TestButtonsV[3] = self.ui.pushButton_5
        self.TestButtonsA = [QtGui.QPushButton(), QtGui.QPushButton(), QtGui.QPushButton(), QtGui.QPushButton()]
        self.TestButtonsA[0] = self.ui.pushButton_6
        self.TestButtonsA[1] = self.ui.pushButton_7
        self.TestButtonsA[2] = self.ui.pushButton_8
        self.TestButtonsA[3] = self.ui.pushButton_9
        
        self.toData()
                
        # Словарь для хранения данных по приборам
        self.read_json()
        
        for i in range(4):
            self.TestButtonsV[i].clicked.connect(self.pushButton_Click)
            self.TestButtonsA[i].clicked.connect(self.pushButton_Click)
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_Click)
        

    def pushButton_Click(self):
        global DEV
        self.toData()
        sw = 'T'
        data_ = self.data['T']
        for i in range(len(self.TestButtonsV)):
            if self.TestButtonsV[i] == self.sender():
                sw = 'V'
                data_ = self.data['V']                
                name_type = self.TypesV[i].currentText()                
                break
            if self.TestButtonsA[i] == self.sender():
                sw = 'A'
                data_ = self.data['A']
                name_type = self.TypesA[i].currentText()                
                break
        try:
            DEV.port.close()
            print 11
            print DEV.port.baudrate
            print DEV.port.name
            print DEV.port
            DEV.port.open()
            print 12

            rez = None
            if sw == 'T':
                if data_['type'] == 0:
                    type = 2
                name_type = self.ui.comboBox.currentText()
                address = self.ui.spinBox.value()                    
                st = '#GOHGROTVLLSJ'+chr(0x0d) #Команда правильная
                print 1
                Val = DEV.ReadDevice(DEV.port, type, st)                            
                print 2
                DEV.port.close()
                DEV.port.open()
                st = '#GPHGROTVMVJT'+chr(0x0d) #Команда правильная
                print 3
                Val_2 = DEV.ReadDevice(DEV.port, type, st)            
                print 4
                if Val != None and Val_2 != None:
                    rez = str(round(float(Val),3)) + ' / ' +  str(round(float(Val_2),3))
                else:
                    if Val != None:
                        rez = str(round(float(Val),3)) + ' /'
                    if Val_2 != None:
                        rez = '/ ' +  str(round(float(Val_2),3))
                        
                print 5
            else:
                type = data_[i]['type']
                if type == 0:
                    st = chr(data_[i]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
                if type == 1:
                    st = chr(data_[i]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
                st += chr(crc16(st)[0]) + chr(crc16(st)[1])
                address = data_[i]['address']                
                Val = DEV.ReadDevice(DEV.port, type, st)            
                if Val != None:
                    rez = str(round(float(Val),3))

            DEV.port.close()
            print 6
            
            if rez == None:
                msgBox(self, u"Данные с прибора '" + name_type + u"' с адресом '" + str(address) + u"' не читаются!")
            else:
                msgBox(self, u"Показание прибора '" + name_type + u"' с адресом '" + str(address) + u"': " + rez)
                       
        except SerialException:
            print u"Порт " + DEV.port.port + u' не открывается!'
            self.errStr = u"Порт " + DEV.port.port + u' не открывается!'
            msgBox(self, u"Порт " + DEV.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами!')
            return None
        finally:
            self.port.close()
                

    def pushButton_10_Click(self):
        self.close()    


    def read_json(self):
        # Чтение параметров с Warming_setup.json файла, если таковой имеется
        try:
            f = open('Warming_setup.json','r')
            self.data = json.load(f)
            
            data_ = self.data['T']
            self.ui.comboBox.setCurrentIndex(data_['type'])
            self.ui.spinBox.setValue(data_['address'])
            
            data_ = self.data['P']
            self.ui.doubleSpinBox.setValue(data_['period'])
            
            data_ = self.data['V']
            for i in range(len(data_)):
                self.TypesV[i].setCurrentIndex(data_[i]['type'])
                self.AddressV[i].setValue(data_[i]['address'])
                self.MeasuresV[i].setCurrentIndex(data_[i]['measure'])

            data_ = self.data['A']
            for i in range(len(data_)):
                self.TypesA[i].setCurrentIndex(data_[i]['type'])
                self.AddressA[i].setValue(data_[i]['address'])
                self.MeasuresA[i].setCurrentIndex(data_[i]['measure'])            

        except Exception:
            print u'Ошибка чтения Warming_setup.json!'


    def write_json(self):
        # ЗАПИСАТЬ
        f = open('Warming_setup.json','w')        
        self.toData()    
        json.dump(self.data, f)

        
    def toData(self):
        self.data = {}        
        self.data['V'] = []
        self.data['A'] = []
        self.data['T'] = {}
        self.data['P'] = {}
        
        for i in range(4):            
            self.data['V'].append({})
            self.data['V'][i]['type'] = self.TypesV[i].currentIndex()
            self.data['V'][i]['address'] = self.AddressV[i].value()
            self.data['V'][i]['measure'] = self.MeasuresV[i].currentIndex()
            self.data['A'].append({})
            self.data['A'][i]['type'] = self.TypesA[i].currentIndex()
            self.data['A'][i]['address'] = self.AddressA[i].value()
            self.data['A'][i]['measure'] = self.MeasuresA[i].currentIndex()
        self.data['T']['type'] = self.ui.comboBox.currentIndex()
        self.data['T']['address'] = self.ui.spinBox.value()
        self.data['P']['period'] = self.ui.doubleSpinBox.value()
            

    def closeEvent(self, event):
        self.write_json()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
     
    from dpframe.base.envapp import checkenv
    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import db_connection_init
    from dpframe.base.inits import default_log_init
    from electrolab.gui.inits import serial_devices_init
              
    @serial_devices_init
    @json_config_init
    @db_connection_init
    @default_log_init    
            
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
                            
    wind = Warming_setup(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())
