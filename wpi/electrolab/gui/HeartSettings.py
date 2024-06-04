# -*- coding: UTF-8 -*-

'''
Created on 2.08.2015

@author: atol
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from serial import Serial
from serial.serialutil import SerialException
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
from devices import Devices

import binhex
import binascii
import struct
import devices
import ui.ico_64_rc

import json
import time
#import datetime


#class HeartSettings(QtGui.QDialog):
#class Devices(QWidget, UILoader):
class HeartSettings(QtGui.QDialog, UILoader):
    def __init__(self, _env):
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"HeartSettings.ui")
        self.setEnabled(False)

        self.fnt =  QFont()
        self.fnt.setPixelSize(20)

        self.ui.label_14.setEnabled(False)
        self.ui.label_15.setEnabled(False)
        self.ui.spinBox.setEnabled(False)
        self.ui.spinBox_2.setEnabled(False)

        #04.2019 
        self.Devices = Devices(_env)
 
        # Списки к массиву приборов        
        self.Numbering = []   # нумерация приборов
        self.Names = []       # наименования
        self.Types = []       # типы
        self.Measures = []    # единицы измерения
        self.Address = []     # адреса
        self.Coeff = []       # коэффициенты
        #14.01
        self.MinValues = []    # минимальное рабочее значение
        self.TestButtons = []  # кнопка тестирования
        
        # Стандартные наименования приборов     
        
        '''   
        self.sNames = QtCore.QStringList()
        self.sNames.append(u'Амперметр')
        self.sNames.append(u'Вольтметр')
        
        self.sTypes = QtCore.QStringList()
        self.sTypes.append(u'ЩП02М')
        self.sTypes.append(u'ЩП02П')
        self.sTypes.append(u'Щ02П')
        
        self.sMeasuresA = QtCore.QStringList()
        self.sMeasuresA.append(u'A')
        self.sMeasuresA.append(u'mA')
        self.sMeasuresA.append(u'kA')
        
        self.sMeasuresV = QtCore.QStringList()
        self.sMeasuresV.append(u'V')
        self.sMeasuresV.append(u'mV')
        self.sMeasuresV.append(u'kV')
        '''
        
        # Словарь для хранения данных по приборам
        self.data = {}
        self.read_json()
        self.refresh_devices()


        self.port = Serial()
        self.port.port = _env.config.devices.chp02m.port
        self.port.baudrate = 9600
        self.port.bytesize = 8
        self.port.parity = 'N'
        self.port.stopbits = 1
        self.port.timeout = 0.1
       
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/64_Exit.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

    def testButton_Click(self):
#        print self.data        
        self.toData()
#        print self.data        
        for i in range(len(self.TestButtons)):
            if self.TestButtons[i] == self.sender():
                break
        try:
#            print 1
            self.port.close()
#            print 2
            self.port.open()
#            print 3


            #04.2019
            '''
            if self.data['devices'][str(i)]['ind_type'] == 0:
                st = chr(self.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if self.data['devices'][str(i)]['ind_type'] == 1:
                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if self.data['devices'][str(i)]['ind_type'] == 2:
                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)            
            
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])

            Val = self.ReadDevice(self.port, self.data['devices'][str(i)]['ind_type'], st, self.data['devices'][str(i)]['coeff'])
            if Val == None:
                msgBox(self, u"Данные с прибора № " + str(i+1) + u' не читаются!')
            else:
                msgBox(self, u"Показание прибора № " + str(i+1) + u': "' + str(Val) + '"')
            '''
            #self.data['devices'][str(i)]['ind_type']
            
            Val = self.Devices.ReadDevice_2(self.port, self.data['devices'][str(i)]['ind_type'], self.data['devices'][str(i)]['address'], 1.0)
#            Val = self.Devices.ReadDevice_2(self.port, indType, adr, 1.0)
            if Val == None:
#15.04.2019                msgBox(self, u"Показания прибора: " + self.sNames[self.data['devices'][str(i)]['ind_name']] + u" с адресом: " + str(self.data['devices'][str(i)]['address']) + u' не читаются!')
                msgBox(self, u"Показания прибора: " + self.Devices.sNames[self.data['devices'][str(i)]['ind_name']] + u" с адресом: " + str(self.data['devices'][str(i)]['address']) + u' не читаются!')
            else:
#                Val = self.coefMeasure(self.data['devices'][str(i)]['ind_measure']) * float(Val)
                Val = self.coefMeasure(self.data['devices'][str(i)]['ind_measure']) * float(Val) * self.data['devices'][str(i)]['coeff']
#15.04.2019                msgBox(self, u"Показание прибора: " + self.sNames[self.data['devices'][str(i)]['ind_name']] + u" с адресом: " + str(self.data['devices'][str(i)]['address']) + u' "' + str(Val) + '"')
                msgBox(self, u"Показание прибора: " + self.Devices.sNames[self.data['devices'][str(i)]['ind_name']] + u" с адресом: " + str(self.data['devices'][str(i)]['address']) + u' "' + str(Val) + '"')
            

        except SerialException:
            print u"Порт " + self.port.port + u' не открывается!'
            self.errStr = u"Порт " + self.port.port + u' не открывается!'
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами_11!')
            return None
        finally:
            self.port.close()


    def pushButton_Click(self):
        self.clear_devices()
        i = len(self.Numbering)
        self.add_device(i, True, 0, 0, 0, i+1, 1, 0.01)
        self.refresh_devices()

    def pushButton_2_Click(self):
        if getTrue(self, u'Вы действительно хотите удалить\nвсе неактивные приборы?'):        
            self.clear_devices()
            self.remove_devices()
            self.refresh_devices()

    def pushButton_3_Click(self):
        self.close() 
             
            
    def coefMeasure(self, ind_measure):
        # Вычисление коэффициента в зависимости от единицы измерения
        coef = 1.0
        if ind_measure == 1:
            coef = 0.001
        if ind_measure == 2:
            coef = 1000.0
        return coef    
                        
            
    def checkBox_Click(self):
        i = int(self.sender().objectName())
        check = self.sender().isChecked()
        self.Names[i].setEnabled(check)
        self.Types[i].setEnabled(check)
        self.Measures[i].setEnabled(check)
        self.Address[i].setEnabled(check)
        self.Coeff[i].setEnabled(check)
        #14.01
        self.MinValues[i].setEnabled(check)
        self.TestButtons[i].setEnabled(check)


    def read_json(self):
        # Чтение параметров с heartsettings.json файла, если таковой имеется
        try:
            f = open('heartsettings.json','r')
            self.data = json.load(f)
            for i in range(len(self.data['devices'])):
                try:
                    min_value = self.data['devices'][str(i)]['min_value']
                except Exception:
                    min_value = 0.01
                    
                self.add_device(i, 
                                self.data['devices'][str(i)]['activ'],
                                self.data['devices'][str(i)]['ind_name'],
                                self.data['devices'][str(i)]['ind_type'],
                                self.data['devices'][str(i)]['ind_measure'],
                                self.data['devices'][str(i)]['address'],
                                self.data['devices'][str(i)]['coeff'],
                                min_value)
            #04.2019
            '''    
            self.ui.doubleSpinBox.setValue(self.data['accuracy']['r'])                                         
            self.ui.doubleSpinBox_2.setValue(self.data['accuracy']['a'])
            self.ui.checkBox.setChecked(self.data['min_alg'])                              
            self.ui.comboBox.setCurrentIndex(self.data['ind_measureR'])
            self.ui.radioButton.setChecked(self.data['forward'])              
            self.ui.radioButton_2.setChecked(self.data['back'])
            '''
            self.ui.doubleSpinBox_3.setValue(self.data['pause'])  
            
        except Exception:
            print u'Ошибка чтения heartsettings.json!'
            self.data = {}


        # Чтение параметров с config.json файла, если таковой имеется
        try:
            f = open('config.json','r')
            self.data_config = json.load(f)
            
            
            # Проверяем, присутствуют ли данные по соединению с БД в файле config.json  
            try:
                self.ui.lineEdit.setText(self.data_config['db']['host'])
            except Exception:
                self.ui.lineEdit.setText('')
            try:
                self.ui.lineEdit_2.setText(self.data_config['db']['database'])
            except Exception:
                 self.ui.lineEdit_2.setText('')
            try:
                self.ui.lineEdit_3.setText(self.data_config['db']['user'])
            except Exception:
                self.ui.lineEdit_3.setText('')
            try:
                self.ui.spinBox_6.setValue(int(self.data_config['devices']['chp02m']['port'][3:]))
            except Exception:
                self.ui.spinBox_6.setValue(0)

            try:
                self.ui.spinBox.setValue(int(self.data_config['devices']['knt05']['port'][3:]))
            except Exception:
                self.ui.spinBox.setValue(0)

            try:
                self.ui.spinBox_2.setValue(int(self.data_config['devices']['scanner'][3:]))
            except Exception:
                self.ui.spinBox_2.setValue(0)


#        self.data_config['devices']['chp02m']['port'] = "COM" + str(self.spinBox_6.value())

            
            '''          
            try:
                host = self.data_config['db']['host']
            except Exception:
                host = ''
            try:
                database = self.data_config['db']['database']
            except Exception:
                database = ''
            try:
                user = self.data_config['db']['user']
            except Exception:
                user = ''
                
            self.ui.lineEdit.setText(host)
            self.ui.lineEdit_2.setText(database)
            self.ui.lineEdit_3.setText(user)
            '''
            
        except Exception:
            print u'Ошибка чтения config.json!'
            self.data = {}



    def write_json(self):
        # ЗАПИСАТЬ
        f = open('heartsettings.json','w')        
        self.toData()    
        json.dump(self.data, f)

            
        
        f = open('config.json','w')
        
#        print 'self.ui.lineEdit.text()=', self.ui.lineEdit.text()
        
#        self.data_config['db']['host'] = self.ui.lineEdit.text()
#        self.data_config['db']['database'] = self.ui.lineEdit_2.text()
#        self.data_config['db']['user'] = self.ui.lineEdit_3.text()
               
        self.data_config['db']= {"host": str(self.ui.lineEdit.text()),
                                 "database": str(self.ui.lineEdit_2.text()), 
                                 "user": str(self.ui.lineEdit_3.text()), 
                                 "password": self.data_config['db']['password']}
                
#        print 'self.data_config=', self.data_config
        
#        chp02m = {"port":self.port3, "ammeter":{"address":str(self.spinBox.value())}, "voltmeter":{"address":str(self.spinBox_2.value())}}
#        self.data['devices']= {"knt05": knt05, "scanner": scanner, "chp02m": chp02m}
        
        self.data_config['devices']['chp02m']['port'] = "COM" + str(self.ui.spinBox_6.value())
        
        #return
#        json.dump(self.data_config, f)
        json.dump(self.data_config, f, indent=4, sort_keys=False)
        

#        json.dump(self.data, f, indent=4, sort_keys=False)
        
        
        
        
        
        
    def toData(self):
        #04.2019
        #self.data = {}        
        self.data['devices'] = {}
        for i in range(len(self.Numbering)):            
            self.data['devices'][str(self.Numbering[i].objectName())] = {}
            self.data['devices'][str(self.Numbering[i].objectName())]['activ'] = self.Numbering[i].isChecked()
            self.data['devices'][str(self.Numbering[i].objectName())]['ind_name'] = self.Names[i].currentIndex()
            self.data['devices'][str(self.Numbering[i].objectName())]['ind_type'] = self.Types[i].currentIndex()
            self.data['devices'][str(self.Numbering[i].objectName())]['ind_measure'] = self.Measures[i].currentIndex()
            self.data['devices'][str(self.Numbering[i].objectName())]['address'] = self.Address[i].value()
            self.data['devices'][str(self.Numbering[i].objectName())]['coeff'] = self.Coeff[i].value()
            #14.01
            self.data['devices'][str(self.Numbering[i].objectName())]['min_value'] = self.MinValues[i].value()
            
            '''
            self.data['devices'][int(self.Numbering[i].objectName())] = {}
            self.data['devices'][int(self.Numbering[i].objectName())]['activ'] = self.Numbering[i].isChecked()
            self.data['devices'][int(self.Numbering[i].objectName())]['ind_name'] = self.Names[i].currentIndex()
            self.data['devices'][int(self.Numbering[i].objectName())]['ind_type'] = self.Types[i].currentIndex()
            self.data['devices'][int(self.Numbering[i].objectName())]['ind_measure'] = self.Measures[i].currentIndex()
            self.data['devices'][int(self.Numbering[i].objectName())]['address'] = self.Address[i].value()
            #14.01
            self.data['devices'][int(self.Numbering[i].objectName())]['min_value'] = self.MinValues[i].value()
            '''
                        
        #04.2019
        '''
        self.data['accuracy'] = {}
        self.data['accuracy']['r'] = self.ui.doubleSpinBox.value()
        self.data['accuracy']['a'] = self.ui.doubleSpinBox_2.value()
        self.data['min_alg'] = self.ui.checkBox.isChecked()
        self.data['ind_measureR'] = self.ui.comboBox.currentIndex()        
        self.data['forward'] = self.ui.radioButton.isChecked()
        self.data['back'] = self.ui.radioButton_2.isChecked()
        '''
        self.data['pause'] = self.ui.doubleSpinBox_3.value()
                    

    def comboBox_currentIndexChanged(self, ind):
        i = int(self.sender().objectName())
        self.Measures[i].clear()
        if ind == 0:
#15.04.2019            self.Measures[i].addItems(self.sMeasuresA)
            self.Measures[i].addItems(self.Devices.sMeasuresA)
        else:    
#15.04.2019            self.Measures[i].addItems(self.sMeasuresV)
            self.Measures[i].addItems(self.Devices.sMeasuresV)
        self.Measures[i].setCurrentIndex(0)


    def add_device(self, i, activ, ind_name, ind_type, ind_measure, address, coeff, min_value):
        #QtGui.QCheckBox.clicked()
        self.Numbering += [QtGui.QCheckBox('   ' +str(i+1))]
        self.Numbering[i].setObjectName(str(i))
        self.Numbering[i].setChecked(activ)
        self.Numbering[i].setMaximumWidth(70)
        self.Numbering[i].setFont(self.fnt)
        self.Numbering[i].clicked.connect(self.checkBox_Click)
        self.Numbering[i].setVisible(False)

        #QtGui.QComboBox.clear()
        self.Names += [QtGui.QComboBox()]
        self.Names[i].setObjectName(str(i))
#15.04.2019        self.Names[i].addItems(self.Devices.sNames)
        self.Names[i].addItems(self.Devices.sNames)
        self.Names[i].setCurrentIndex(ind_name)
        self.Names[i].setFont(self.fnt)
        self.Names[i].setEnabled(activ)
        #self.Names[i].changeEvent.connect(self.comboBox_changeEvent)
        self.Names[i].currentIndexChanged['int'].connect(self.comboBox_currentIndexChanged)
        self.Names[i].setVisible(False)
            
        self.Types += [QtGui.QComboBox()]
#15.04.2019        self.Types[i].addItems(self.sTypes)
        self.Types[i].addItems(self.Devices.sTypes)
        self.Types[i].setCurrentIndex(ind_type)
        self.Types[i].setFont(self.fnt)
        self.Types[i].setEnabled(activ)
        self.Types[i].setVisible(False)
        
        self.Measures += [QtGui.QComboBox()]
        if ind_name == 0:
#15.04.2019            self.Measures[i].addItems(self.sMeasuresA)
            self.Measures[i].addItems(self.Devices.sMeasuresA)
        else:            
#15.04.2019            self.Measures[i].addItems(self.sMeasuresV)
            self.Measures[i].addItems(self.Devices.sMeasuresV)
        self.Measures[i].setCurrentIndex(ind_measure)
        self.Measures[i].setMaximumWidth(100)
        self.Measures[i].setFont(self.fnt)
        self.Measures[i].setEnabled(activ)
        self.Measures[i].setVisible(False)
                        
        self.Address += [QtGui.QSpinBox()]
        self.Address[i].setValue(address)
        self.Address[i].setAlignment(QtCore.Qt.AlignCenter)
        #self.Address[i].setMaximumWidth(70)
        self.Address[i].setMinimumWidth(70)
        self.Address[i].setFont(self.fnt)
        self.Address[i].setEnabled(activ)
        self.Address[i].setVisible(False)
                        
        
        #14.01
        
       # self.MinValues += [QtGui.QSpinBox()]
        self.MinValues += [QtGui.QDoubleSpinBox()]
        self.MinValues[i].setSingleStep(1)

        #20.01        
        self.MinValues[i].setMaximum(100000)
        self.MinValues[i].setMinimum(0.00000)
        self.MinValues[i].setDecimals(5)
        #print 'min_value=', min_value
        self.MinValues[i].setValue(min_value)
                
        self.MinValues[i].setAlignment(QtCore.Qt.AlignCenter)
        #self.MinValues[i].setMaximumWidth(100)
        self.MinValues[i].setMinimumWidth(100)
        self.MinValues[i].setFont(self.fnt)
        self.MinValues[i].setEnabled(activ)
        self.MinValues[i].setVisible(False)
        
        
        
        self.Coeff += [QtGui.QDoubleSpinBox()]
        #QtGui.QDoubleSpinBox.ButtonSymbols = None
        #QtGui.QAbstractSpinBox.NoButtons
        #QtGui.QDoubleSpinBox.setButtonSymbols()
        self.Coeff[i].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.Coeff[i].setValue(coeff)
#        print 1
        self.Coeff[i].setDecimals(4)
#        print 2
        self.Coeff[i].setAlignment(QtCore.Qt.AlignCenter)
        #self.Coeff[i].setMinimumWidth(70)
        self.Coeff[i].setMaximumWidth(80)
        self.Coeff[i].setFont(self.fnt)
        self.Coeff[i].setEnabled(activ)
        self.Coeff[i].setVisible(False)
        
                
        
        self.TestButtons += [QtGui.QPushButton()]
        #QtGui.QPushButton.setT
        self.TestButtons[i].setText(u'Проверить')
        #self.TestButtons[i].setAlignment(QtCore.Qt.AlignCenter)
        #self.TestButtons[i].setMaximumWidth(50)
        self.TestButtons[i].setFont(self.fnt)
        self.TestButtons[i].setEnabled(activ)
        self.TestButtons[i].setVisible(False)
        self.TestButtons[i].clicked.connect(self.testButton_Click)
        self.TestButtons[i].setFocusPolicy(QtCore.Qt.NoFocus)
        #QtGui.QPushButton.setFocusPolicy()
                
        
    def clear_devices(self):
        for i in range(len(self.Numbering)):
            self.ui.gridLayout.removeWidget(self.Numbering[i])
            self.ui.gridLayout.removeWidget(self.Names[i])
            self.ui.gridLayout.removeWidget(self.Types[i])
            self.ui.gridLayout.removeWidget(self.Measures[i])
            self.ui.gridLayout.removeWidget(self.Address[i])
            self.ui.gridLayout.removeWidget(self.Coeff[i])
            #14.01
            self.ui.gridLayout.removeWidget(self.MinValues[i])
            self.ui.gridLayout.removeWidget(self.TestButtons[i])            
            
            self.Numbering[i].setVisible(False)
            self.Names[i].setVisible(False)
            self.Types[i].setVisible(False)
            self.Measures[i].setVisible(False)
            self.Address[i].setVisible(False)
            self.Coeff[i].setVisible(False)
            #14.01
            self.MinValues[i].setVisible(False)
            self.TestButtons[i].setVisible(False)
            
            

    def refresh_devices(self):
        for i in range(len(self.Numbering)):
            
            #QtGui.QLayoutItem.setAlignment(QtCore.Qt.AlignCenter)
            #QtGui.QGridLayout.itemAtPosition(int, int).
            
            self.ui.gridLayout.addWidget(self.Numbering[i], i + 1, 1)
            self.ui.gridLayout.addWidget(self.Names[i], i + 1, 2)
            self.ui.gridLayout.addWidget(self.Types[i], i + 1, 3)
            self.ui.gridLayout.addWidget(self.Measures[i], i + 1, 4)
            self.ui.gridLayout.addWidget(self.Address[i], i + 1, 5)
            self.ui.gridLayout.addWidget(self.MinValues[i], i + 1, 6)
            self.ui.gridLayout.addWidget(self.Coeff[i], i + 1, 7)
            self.ui.gridLayout.addWidget(self.TestButtons[i], i + 1, 8)
            
            self.Numbering[i].setVisible(True)
            self.Names[i].setVisible(True)
            self.Types[i].setVisible(True)
            self.Measures[i].setVisible(True)
            self.Address[i].setVisible(True)
            self.Coeff[i].setVisible(True)
            #14.01
            self.MinValues[i].setVisible(True)
            self.TestButtons[i].setVisible(True)
                        
            for j in range(7):
                self.ui.gridLayout.itemAtPosition(i+1, j+1).setAlignment(QtCore.Qt.AlignCenter)
            
            #self.ui.gridLayout.activate()
            #QtGui.QGridLayout.activate()
        #self.refresh_devices()
            
            


    def remove_devices(self):
        # Удаление всех неактивных устройств из списка с перенумерацией
        for i in reversed(range(len(self.Numbering))):
            if not self.Numbering[i].isChecked():
                self.Numbering.pop(i)
                self.Names.pop(i)
                self.Types.pop(i)
                self.Measures.pop(i)
                self.Address.pop(i)
                self.Coeff.pop(i)
                #14.01
                self.MinValues.pop(i)
                self.TestButtons.pop(i)
        for i in range(len(self.Numbering)):
            self.Numbering[i].setText('   ' + str(i + 1))
            self.Numbering[i].setObjectName(str(i))
        

    def closeEvent(self, event):
        self.write_json()
        

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
                            
    wind = HeartSettings(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())
