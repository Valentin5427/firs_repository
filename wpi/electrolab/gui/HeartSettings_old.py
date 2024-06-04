# -*- coding: UTF-8 -*-

'''
Created on 16.08.2013

@author: atol
'''

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMessageBox, QIcon
import ui.ico_64_rc
import os
from serial import Serial
from serial.serialutil import SerialException
from devices import Devices
from electrolab.gui.msgbox import getTrue, msgBox


import JournalMsr
import TestHeart
import time
import devices
import json

class HeartSettings(QtGui.QDialog):
    def __init__(self, env, indAmp, indVolt):
        QtGui.QDialog.__init__(self)
        try:
            global path_ui
            path_ui = env.config.paths.ui + "/"
            if not os.path.exists(path_ui):        
                path_ui = ""
            print 'path_ui1=', path_ui    
            if not JournalMsr.MyLoadUi(path_ui, "HeartSettings.ui", self):
                self.is_show = False
                return
            
            self.groupBox.setVisible(False)
            self.groupBox_2.setVisible(False)
            
            self.Devices = Devices(env)
            
            self.read_json()            

            self.pushButton.clicked.connect(self.pushButton_Click)
            self.pushButton_2.clicked.connect(self.pushButton_Click_2)
            self.pushButton_3.clicked.connect(self.pushButton_Click_2)
            self.port = Serial()
            self.port.port = ''
            self.port.port = env.config.devices.chp02m.port
            print self.port.name
            print "port", self.port.port
            self.port.baudrate = 9600
            self.port.bytesize = 8
            self.port.parity = 'N'
            self.port.stopbits = 1
            self.port.timeout = 0.1

            '''             
            print 1    
            self.comboBox.currentIndexChanged.connect(self.comboBox_indexChanged)        
            print 2    
            self.spinBox.valueChanged.connect(self.spinBox_valueChanged)        
            print 3    
            self.spinBox_2.valueChanged.connect(self.spinBox_2_valueChanged)
            print 4    
            '''
            
        except Exception:
            pass
            #msgBox(self, u'Настройки не открываются!')


    def read_json(self):
        # Чтение параметров с heartsettings.json файла, если таковой имеется
        try:
            self.comboBox.clear()
            self.comboBox.addItems(self.Devices.sTypes)
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.Devices.sTypes)
            self.comboBox_3.clear()
            self.comboBox_3.addItems(self.Devices.sMeasuresA)
            self.comboBox_4.clear()
            self.comboBox_4.addItems(self.Devices.sMeasuresA)
            
            f = open('heartsettings.json','r')
            data = json.load(f)
            self.comboBox.setCurrentIndex(int(data['indAmp']))            
            self.comboBox_2.setCurrentIndex(int(data['indVolt']))
            self.comboBox_3.setCurrentIndex(int(data['indMeasureA']))
            self.comboBox_4.setCurrentIndex(int(data['indMeasureV']))
            self.spinBox_3.setValue(int(data['adressA']))                                         
            self.spinBox_4.setValue(int(data['adressV']))                                                     
            self.lineEdit.setText(data['MinAmp'])           
            self.lineEdit_2.setText(data['Delay'])                        
            self.lineEdit_5.setText(data['CoefVoltmeter'])           
            self.lineEdit_6.setText(data['ControlLoops'])            
        except Exception:
            print u'Ошибка чтения heartsettings.json!'
            msgBox(self, u'Ошибка чтения heartsettings.json!')

        
#    def toData(self):
    def write_json(self):
        # ЗАПИСАТЬ
        try:
            f = open('heartsettings.json','w')
            data = {}        
            data['indAmp'] = str(self.comboBox.currentIndex())
            data['indVolt'] = str(self.comboBox_2.currentIndex())
            data['indMeasureA'] = str(self.comboBox_3.currentIndex())
            data['indMeasureV'] = str(self.comboBox_4.currentIndex())
            data['adressA'] = str(self.spinBox_3.value())
            data['adressV'] = str(self.spinBox_4.value())
            data['MinAmp'] = str(self.lineEdit.text())
            data['Delay'] = str(self.lineEdit_2.text())
            data['CoefVoltmeter'] = str(self.lineEdit_5.text())
            data['ControlLoops'] = str(self.lineEdit_6.text())
        
#        if self.lineEdit.Tag <> "":
#            data['id_heart'] = str(self.lineEdit.Tag)
            json.dump(data, f)
        except Exception:
            print u'Ошибка записи heartsettings.json!'
            return None
        
        
    def closeEvent(self, event):
        self.write_json()


    def pushButton_Click(self):
        self.close()


    def pushButton_Click_2(self):
        print "self.sender()=", self.sender().objectName()
        try:
            if self.sender().objectName() == "pushButton_2":
                nameType = self.comboBox.currentText()
                indType = self.comboBox.currentIndex()
                indMeasure = self.comboBox_3.currentIndex()
                adr = self.spinBox_3.value()
            else:
                nameType = self.comboBox_2.currentText()
                indType = self.comboBox_2.currentIndex()
                indMeasure = self.comboBox_4.currentIndex()
                adr = self.spinBox_4.value()
                       
     #       self.port.port = 'COM1'
            
            print 1
            print self.port.name
            print self.port.port
            self.port.close()
            print 2
            self.port.open()
            print 3
            '''
            if indType == 0:
                st = chr(adr)+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if indType == 1:
                st = chr(adr)+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if indType == 2:
                st = chr(adr)+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)
            st += chr(devices.crc16(st)[0]) + chr(devices.crc16(st)[1])
            print 'st=' + str(ord(st[0])) + ' ' + str(ord(st[1])) + ' ' + str(ord(st[2])) + ' ' + str(ord(st[3])) + ' ' + str(ord(st[4])) + ' ' + str(ord(st[5])) + ' ' + str(ord(st[6])) + ' ' + str(ord(st[7]))
            '''
                        
            Val = self.Devices.ReadDevice_2(self.port, indType, adr, 1.0)
            if Val == None:
                msgBox(self, u"Показания прибора " + nameType + u" с адресом: " + str(adr) + u' не читаются!')
            else:                
                #self.comboBox_2.currentText()
                Val = self.Devices.coefMeasure(indMeasure) * float(Val)                
                msgBox(self, u"Показание прибора " + nameType + u" с адресом: " + str(adr) + u': "' + str(Val) + '"')

        except SerialException:
            print u"Порт " + self.port.port + u' не открывается!!!'
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            print u'Проблема с портом либо с приборами_1!'
            msgBox(self, u'Проблема с портом либо с приборами_1!')
            return None
        finally:
            self.port.close()


#    def pushButton_Click_3(self):
#        pass


    '''    
    def comboBox_indexChanged(self):
        self.label_3.setEnabled(self.comboBox.currentIndex() == 0)
        self.spinBox.setEnabled(self.comboBox.currentIndex() == 0)
        print self.comboBox.currentIndex()
 
    def spinBox_valueChanged(self, value):
        #print self.spinBox.value()
        self.WritePort(1, value)

    def spinBox_2_valueChanged(self, value):
        #print self.spinBox.value()
        self.WritePort(2, value)


    def ReadDevice(self, port, command):
        # Чтение показания прибора
        global isTestHeart
        try:
            print "ReadDevice"
            port.write(command)
#            s = port.read(15)
            s = port.read()
        except SerialException:
            isTestHeart = False
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            

        
    def WritePort(self, adrDevice, value):
        # Чтение показания приборов (амперметр, вольтметр)    
        global isTestHeart
        #global port
        try:
            self.port.open()
            #s = '\x01\x03\x00\x05\x00\x05\x95\xC8'
            #V = self.ReadDevice(port, '\x02\x03\x00\x05\x00\x05\x95\xFB')
            if adrDevice == 1:
                if value == 0:
                    V = self.ReadDevice(self.port, '\x01\x10\x0A\x0C\x00\x01\x02\x00\x00\x0C\x9C')
                if value == 1:
                    V = self.ReadDevice(self.port, '\x01\x10\x0A\x0C\x00\x01\x02\x00\x01\xCD\x5C')
                if value == 2:
                    V = self.ReadDevice(self.port, '\x01\x10\x0A\x0C\x00\x01\x02\x00\x02\x8D\x5D')
                if value == 3:
                    V = self.ReadDevice(self.port, '\x01\x10\x0A\x0C\x00\x01\x02\x00\x03\x4C\x9D')
            
            if adrDevice == 2:
                if value == 0:
                    V = self.ReadDevice(self.port, '\x02\x10\x0A\x0C\x00\x01\x02\x00\x00\x18\x6C')
                if value == 1:
                    V = self.ReadDevice(self.port, '\x02\x10\x0A\x0C\x00\x01\x02\x00\x01\xD9\xAC')
                if value == 2:
                    V = self.ReadDevice(self.port, '\x02\x10\x0A\x0C\x00\x01\x02\x00\x02\x99\xAD')
                if value == 3:
                    V = self.ReadDevice(self.port, '\x02\x10\x0A\x0C\x00\x01\x02\x00\x03\x58\x6D')            
            if V == None:
                return None

        except SerialException:
            print u"Порт " + self.port.port + u' не открывается!'
            self.errStr = u"Порт " + self.port.port + u' не открывается!'
            return None
        except Exception:
            self.errStr = u"2Проблемы с портом " + self.port.port
            return None
        finally:
            self.port.close()
        V.strip()
'''


if __name__ == "__main__":    
    import sys
    app = QtGui.QApplication(sys.argv)

    '''
    class Env():
        class config():
            class paths():
                pass    
            class session():
                pass    
    env = Env()
    env.config.paths.ui = "ui"
    '''

    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import db_connection_init
    @json_config_init
    @db_connection_init
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
 
    wind = HeartSettings(env, 0, 0)
    wind.show()
#    if wind.tag <> 0:        
#        wind.show()
    sys.exit(app.exec_())
