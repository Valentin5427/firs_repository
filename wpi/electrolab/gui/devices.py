# -*- coding: UTF-8 -*-

'''
Created on 2.08.2015

@author: atol
'''

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from serial import Serial
from serial.serialutil import SerialException
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox

import binhex
import binascii
import struct


import math
import json
import time
#import datetime

#~ Table of CRC values for high–order byte
auchCRCHi = [
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81,
0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01,
0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01,
0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81,
0x40]

#~ Table of CRC values for low–order byte
auchCRCLo = [
0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4,
0x04, 0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD,
0x1D, 0x1C, 0xDC, 0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7,
0x37, 0xF5, 0x35, 0x34, 0xF4, 0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE,
0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2,
0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68, 0x78, 0xB8, 0xB9, 0x79, 0xBB,
0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0, 0x50, 0x90, 0x91,
0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98, 0x88,
0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80,
0x40]
##########################################################################

# Таблица нагрузок для прибора CA5018
powers = [[0,50],[1,40],[2,30],[3,25],[4,20],[5,15],[6,12.5],[7,10],[8,7.5],[9,6.25],[10,5],[11,3.75],[12,3],[13,2.5],[14,1.75],[15,1.25],[16,1],
          [17,0],[18,0.8],[19,1],[20,1.25],[21,1.5],[22,2],[23,2.5],[24,3.75],[25,5],[26,7.5],[27,10],[28,15]]


def crc16(data):
    uchCRCHi = 0xFF   # high byte of CRC initialized
    uchCRCLo = 0xFF   # low byte of CRC initialized
    uIndex   = 0x0000 # will index into CRC lookup table

    for ch in data :
        uIndex   = uchCRCLo ^ ord(ch)
        uchCRCLo = uchCRCHi ^ auchCRCHi[uIndex]
        uchCRCHi = auchCRCLo[uIndex]
    return uchCRCLo, uchCRCHi, hex(uchCRCLo), hex(uchCRCHi), hex((uchCRCHi << 8 | uchCRCLo))
    #return (uchCRCHi << 8 | uchCRCLo)

# Список используется для расчета контрольной суммы к прибору CA5020
Table = [
0, 49345, 49537, 320, 49921, 960, 640, 49729, 50689, 1728, 1920, 51009, 1280, 50625, 50305, 1088,
52225, 3264, 3456, 52545, 3840, 53185, 52865, 3648, 2560, 51905, 52097, 2880, 51457, 2496, 2176, 51265,
55297, 6336, 6528, 55617, 6912, 56257, 55937, 6720, 7680, 57025, 57217, 8000, 56577, 7616, 7296, 56385,
5120, 54465, 54657, 5440, 55041, 6080, 5760, 54849, 53761, 4800, 4992, 54081, 4352, 53697, 53377, 4160,
61441, 12480, 12672, 61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 13760, 13440, 62529,
15360, 64705, 64897, 15680, 65281, 16320, 16000, 65089, 64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400,
10240, 59585, 59777, 10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 60545, 11328,
58369, 9408, 9600, 58689, 9984, 59329, 59009, 9792, 8704, 58049, 58241, 9024, 57601, 8640, 8320, 57409,
40961, 24768, 24960, 41281, 25344, 41921, 41601, 25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 42049,
27648, 44225, 44417, 27968, 44801, 28608, 28288, 44609, 43521, 27328, 27520, 43841, 26880, 43457, 43137, 26688,
30720, 47297, 47489, 31040, 47873, 31680, 31360, 47681, 48641, 32448, 32640, 48961, 32000, 48577, 48257, 31808,
46081, 29888, 30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 29504, 45313, 29120, 28800, 45121,
20480, 37057, 37249, 20800, 37633, 21440, 21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568,
39937, 23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617, 39809, 23360, 39169, 22976, 22656, 38977,
34817, 18624, 18816, 35137, 19200, 35777, 35457, 19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905,
17408, 33985, 34177, 17728, 34561, 18368, 18048, 34369, 33281, 17088, 17280, 33601, 16640, 33217, 32897, 16448             
]

def ComputeChecksumCA5020(data):
        crc = 0;
        for i in range(len(data)):
            b = data[i]
            index = (crc ^ b)
            while index >= 256:
                index -= 256  
            crc = ((crc >> 8) ^ Table[index]);
        return crc    



#class HeartSettings(QtGui.QDialog):
#class Devices(QWidget, UILoader):
class Devices(QDialog, UILoader):
    def __init__(self, _env):
#    def __init__(self):

        '''
        s = '' �� 
        print str(ord(s[0]))
        '''
        
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"devices.ui")
        self.setEnabled(False)

        self.env = _env
        self.fnt =  QFont()
        self.fnt.setPixelSize(20)
 
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
        self.sNames = []
        self.sNames.append(u'Амперметр')
        self.sNames.append(u'Вольтметр')
        
        self.sTypes = []
        self.sTypes.append(u'ЩП02М')
        self.sTypes.append(u'ЩП02П')
        self.sTypes.append(u'Щ02П')
        self.sTypes.append(u'Щ00П')
        
        self.sMeasuresA = []
        self.sMeasuresA.append(u'A')
        self.sMeasuresA.append(u'mA')
        self.sMeasuresA.append(u'kA')
        
        self.sMeasuresV = []
        self.sMeasuresV.append(u'V')
        self.sMeasuresV.append(u'mV')
        self.sMeasuresV.append(u'kV')
        
        # Словарь для хранения данных по приборам
        self.data = {}
        self.read_json()
        self.refresh_devices()


        self.port = Serial()
#        print type(self.port.port)
#        self.port.port = self.env.config.devices.chp02m.port
#        print _env.config.devices.chp02m.port
        self.port.port = _env.config.devices.chp02m.port
#        self.port.port = 'COM1'
#        print type(_env.config.devices.chp02m.port)
#        print type(self.port.port)
        self.port.baudrate = 9600
        self.port.bytesize = 8
        self.port.parity = 'N'
        self.port.stopbits = 1
        self.port.timeout = 0.1


        # Определяем порты для устройств CA5018
        self.port1 = Serial()
        self.port1.port = _env.config.devices.ca5018_1.port
        self.ca5018_1_active = _env.config.devices.ca5018_1.active
        self.port1.baudrate = 9600
        self.port1.bytesize = 8
        self.port1.parity = 'N'
        self.port1.stopbits = 1
        self.port1.timeout = 0.1

        self.port2 = Serial()
        self.port2.port = _env.config.devices.ca5018_2.port
        self.ca5018_2_active = _env.config.devices.ca5018_2.active
        self.port2.baudrate = 9600
        self.port2.bytesize = 8
        self.port2.parity = 'N'
        self.port2.stopbits = 1
        self.port2.timeout = 0.1

        self.port4 = Serial()
        self.port4.port = _env.config.devices.ca5020.port
        self.ca5020_active = _env.config.devices.ca5020.active
        self.port4.baudrate = 115200
        self.port4.bytesize = 8
        self.port4.parity = 'N'
        self.port4.stopbits = 1
        self.port4.timeout = 0.1

        # Определяем порт для реле ПР200
        self.port3 = Serial()
        self.port3.port = _env.config.devices.pr200.port
        self.port3.baudrate = 9600
        self.port3.bytesize = 8
        self.port3.parity = 'N'
        self.port3.stopbits = 1
        self.port3.timeout = 0.1

       
#        self.port.close()
#        self.port.open()
                
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/64_Exit.png'))
#        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/close_32.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.setVisible(False)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.setVisible(False)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        #self.connect(self.ui.pushButton_3, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        
#        QtGui.QComboBox.setFocus()
#        QtGui.QPushButton.focusPolicy()
#        QtGui.QPushButton.fo        
#        self.ui.comboBox.setFocus()


    def ComputeChecksumCA5020(self, data):
        return ComputeChecksumCA5020(data)


    def testButton_Click(self):
#        print self.data        
        self.toData()
#        print self.data        
        for i in range(len(self.TestButtons)):
            if self.TestButtons[i] == self.sender():
                break
        try:
#            print self.data['devices'][str(i)]['ind_type']
           # print self.data['devices'][i]['ind_type']
            self.port.close()
            self.port.open()

            if self.data['devices'][str(i)]['ind_type'] == 0:
                st = chr(self.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if self.data['devices'][str(i)]['ind_type'] == 1:
                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
#***            
            if self.data['devices'][str(i)]['ind_type'] == 2:
#                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)
#***                
            if self.data['devices'][str(i)]['ind_type'] == 3:
                st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)
            
            
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])

      #      print 'st=' + str(ord(st[0])) + ' ' + str(ord(st[1])) + ' ' + str(ord(st[2])) + ' ' + str(ord(st[3])) + ' ' + str(ord(st[4])) + ' ' + str(ord(st[5])) + ' ' + str(ord(st[6])) + ' ' + str(ord(st[7]))
            
            Val = self.ReadDevice(self.port, self.data['devices'][str(i)]['ind_type'], st, self.data['devices'][str(i)]['coeff'])
            if Val == None:
                msgBox(self, u"Данные с прибора № " + str(i+1) + u' не читаются!')
            else:
                #Val = 3.3333    
                msgBox(self, u"Показание прибора № " + str(i+1) + u': "' + str(Val) + '"')

        except SerialException:
            # print u"Порт " + self.port.port + u' не открывается!'
            self.errStr = u"Порт " + self.port.port + u' не открывается!'
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами_1!')
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
 
    def pushButton_4_Click(self):
#                    byte[] bs = { 5, 255, 6, 0 };

        self.WriteToCA5020(self, power, SecondCurrent)

      
        command = self.commandCA5020(5, 1, 27, 0, 0, 0, 0, 0, 50)
        # print 'command = ', ' '.join(format(ord(x), 'b') for x in command)

        return
        #
        # print 'ComputeChecksumCA5020([5, 255, 6, 0]) = ', ComputeChecksumCA5020([5, 255, 6, 0])
        # print 'ComputeChecksumCA5020([5, 255, 0, 6]) = ', ComputeChecksumCA5020([5, 255, 0, 6])
        # print 'ComputeChecksumCA5020([5, 255, 0, 6]) = ', ComputeChecksumCA5020([5, 255, 6, 6])


        return

        st = chr(5)+chr(255)+chr(6)+chr(0)
        # print crc16(st)
        return

        st += chr(crc16(st)[0]) + chr(crc16(st)[1])
        
        return
        
        self.WriteToPR200(516, 3)
        return 
        
 #   def WriteToPR200(self, adr_dev, adr_reg, val):
        
#        print 512/256
#math.floor(X) - округление вниз.
#math.fmod(X, Y) - остаток от деления X на Y.
        # print int(math.floor(516/256))
        # print int(math.fmod(516, 256))
        # print chr(int(math.floor(516/256)))
        #
        #
        return
#        print 77777777777
#        self.WriteToCA5018(10)
#        print 8
#        return
        '''  
        try:
            
            self.port1 = Serial()
            print '_env.config.devices = ', env.config.devices
            print 'env.config.devices.sa5018_1.port = ', env.config.devices.ca5018_1.port
            self.port1.port = env.config.devices.ca5018_1.port
            self.port1.baudrate = 9600
            self.port1.bytesize = 8
            self.port1.parity = 'N'
            self.port1.stopbits = 1
            self.port1.timeout = 0.1
                                
            print self.port1.port
        
            self.port1.close()
            self.port1.open()
  
            
#            comand = self.comandCA5018(env.config.devices.ca5018_1.address, 3.75)
            command = self.commandCA5018(1, 5)
            
            print 'command=', ord(command[0]), ord(command[1]), ord(command[2]), ord(command[3]), ord(command[4])
            
            self.WriteToCA5018(self.port1, command)
            
        except SerialException:
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с прибором!')
            return None
        finally:
            self.port.close()

        return
    
    
    
    
        time.sleep(1)
#        self.msleep(1000)
        time.sleep(1)
#        self.msleep(1000)
        time.sleep(1)
#        self.msleep(1000)
        time.sleep(1)
#        self.msleep(1000)
        time.sleep(1)
#        self.msleep(1000)
        return
        
        '''        
        
 
        #self.port.port = 'COM3'
        
        
#    def commandPR200(self, address, power):
        
        
#        self.WriteToPR200(self.commandPR200(1, 2))
        self.WriteToPR200()
        return 
        
        
        # print self.port.port
        self.port.port = 'COM3'
        try:
            self.port.close()
            self.port.open()

#            st = chr(4)+chr(3)+chr(0)+chr(5)+chr(0)+chr(5) # амперметр
#            st = chr(1)+chr(16)+chr(0) # ПР200
            st = chr(1)+chr(3)+chr(4)+chr(3)+chr(0)+chr(3) # ПР200 день
#            st = chr(1)+chr(6)+chr(4)+chr(3)+chr(0)+chr(28) # ПР200 день запись
#            st = chr(1)+chr(3)+chr(4)+chr(4)+chr(0)+chr(2) # ПР200 месяц
#            st = chr(1)+chr(3)+chr(4)+chr(5)+chr(0)+chr(1) # ПР200 чтение года
#            st = chr(1)+chr(6)+chr(4)+chr(5)+chr(0)+chr(18) # ПР200 запись года

#            st = chr(1)+chr(4)+chr(1)+chr(0)+chr(0)+chr(1) # ПР200 запись дискрет вход
#            st = chr(1)+chr(3)+chr(1)+chr(0)+chr(0)+chr(1) # ПР200 чтение дискрет вход

#            st = chr(1)+chr(3)+chr(2)+chr(0)+chr(0)+chr(3) # ПР200 чтение сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(1)+chr(0)+chr(3) # ПР200 чтение сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(2)+chr(0)+chr(3) # ПР200 чтение сет. перем.
            
#            st = chr(1)+chr(6)+chr(2)+chr(0)+chr(3)+chr(5) # ПР200 запись в сет. перем.
#            st = chr(1)+chr(6)+chr(2)+chr(1)+chr(0)+chr(57) # ПР200 запись в сет. перем.

#            st = chr(1)+chr(6)+chr(2)+chr(0)+chr(0)+chr(3) # ПР200 запись в сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(0)+chr(0)+chr(1) # ПР200 чтение сет. перем.
            

            # Контрольная сумма
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])

#            print ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5]), ord(st[6]), ord(st[7])
#             print ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5]), ord(st[6]), ord(st[7])
            
            try:
                self.port.write(st)
                        
                s = self.port.read(20)
                #s = self.port.read(15)
                # print 44
                # print 's', s
                # print 'len(s)', len(s)
                ss = ''
                for i in range(len(s)):
                    ss += str(ord(s[i])) + '  '
                    
                # print 's=', ss

                if len(s) < 1:
                    # print 8
                    msgBox(self, u"Данныееееееееееее с прибора №? не читаются!")
                else:
                    #Val = 3.3333    
                    # print 9
#                    msgBox(self, u"Показание прибора № " + str(i+1) + u': "' + str(Val) + '"')
                    msgBox(self, u"Показание прибора № ")
                
                
        
            except SerialException:
                ###isTestHeart = False
                self.errStr = u"Проблема работы прибора с адресом: " + command
                QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
           #     return None                            
            except Exception:
                ###isTestHeart = False
                self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                # print u'Ошибка чтения показаний прибора!'
            #    return None

           
        # except SerialException:
        #     print u"Порт " + self.port.port + u' не открывается!'
            self.errStr = u"Порт " + self.port.port + u' не открывается!'
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами!')
            return None
        finally:
            # print 'self.port.close()'
            self.port.close()

                 
    def decG_0(self, ch):
        if ch == 'G': return 0
        if ch == 'H': return 1
        if ch == 'I': return 2
        if ch == 'J': return 3
        if ch == 'K': return 4
        if ch == 'L': return 5
        if ch == 'M': return 6
        if ch == 'N': return 7
        if ch == 'O': return 8
        if ch == 'P': return 9
        if ch == 'Q': return 10
        if ch == 'R': return 11
        if ch == 'S': return 12
        if ch == 'T': return 13
        if ch == 'U': return 14
        if ch == 'V': return 15
        pass        
            
    def dec0_G(self, ch):
        if ch == 0: return 'G'
        if ch == 1: return 'H'
        if ch == 2: return 'I'
        if ch == 3: return 'J'
        if ch == 4: return 'K'
        if ch == 5: return 'L'
        if ch == 6: return 'M'
        if ch == 7: return 'N'
        if ch == 8: return 'O'
        if ch == 9: return 'P'
        if ch == A: return 'Q'
        if ch == B: return 'R'
        if ch == C: return 'S'
        if ch == D: return 'T'
        if ch == E: return 'U'
        if ch == F: return 'V'
        pass        

            

    def pushButton_5_Click(self):

        st = chr(0x23)+chr(0x47)+chr(0x4f)+chr(0x48)+chr(0x47)+chr(0x52)+chr(0x4f)+chr(0x54)+chr(0x56)+chr(0x4c)+chr(0x4c)+chr(0x53)+chr(0x4a)+chr(0x0d)
        #st = '#GKHGROTVUMPS'+chr(0x0d)
        # 23 47 4f 48 47 52 4f 54 56 4c 4c 53 4a 0d  #GOHGROTVLLSJ. 14 14 COM2  



#        st = chr(self.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
#        st += chr(crc16(st)[0]) + chr(crc16(st)[1])
       # 010400160002
#        s = chr(1)+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
        s = chr(1)+chr(4)+chr(0)+chr(22)
#        print 'crc0=', crc16(s)[0]
#        print 'crc1=', crc16(s)[1]
        s += chr(crc16(s)[0]) + chr(crc16(s)[1])

        # пример из интернета 
#       0410b8df e69c
#         print u'пример из интернета'
        s = chr(4)+chr(16)+chr(184)+chr(223)
        s = chr(184)+chr(223)
 #       print 'crc0=', crc16(s)[0]
 #       print 'crc1=', crc16(s)[1]
        s += chr(crc16(s)[0]) + chr(crc16(s)[1])


        #return
        st = '#GOHGROTVLLSJ'+chr(0x0d) #Команда правильная
      # 0810b8df 55c3
        s = chr(8) + chr(16) + chr(184) + chr(223)
        
        #print 'crc2=', crc16(s)[2]
        #return
        #st = '#GOHGROTVJGHP'+chr(0x0d) #Команда правильная


        try:            
            self.port.port = 'COM2'
            self.port.close()
            self.port.open()
            
            Val = self.ReadDevice(self.port, 2, st)
            # print 'Val=', Val
            #
            
            '''
            self.port.write(st)
            s = self.port.read(20)
            print 's', s
            print 'len(s)', len(s)
            ss = ''
            for i in range(len(s)):
                ss += str(ord(s[i])) + '  '                    
            print 'ss=', ss
            '''          
        except SerialException:
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
      #     return None                            
        except Exception:
            ###isTestHeart = False
           # self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
           print(u'oОшибка чтения показаний прибора!')
           #
#        return None
       
        # print self.decG_0('I')
        # print self.dec0_G(3)
        #
        # Пример температуры 22.5
        st = ''
        s = chr(0x41) + chr(0xb4) + chr(0x49) + chr(0x00)      #22.5356445312
        s = chr(0x41) + chr(0xb4) + chr(0x38) + chr(0x00)     #22.52734375
# 23 47 4f 47 4a 52 4f 54 56 4b 48 52 4b 4a 4f 4b  #GOGJROTVKHRKJOK 16  COM2  
        #// Пример температуры 22.5

        # Пример температуры 20.4
        st = ''
        #4 1 a 3 4 a
        #s = chr(0x41) + chr(0xa3) + chr(0x4a) + chr(0x00)      #20.4111328125
        #4 1 a 2 d 8
        s = chr(0x41) + chr(0xa2) + chr(0xd8) + chr(0x00)      #20.35546875
      #  s = chr(4) + chr(1) + chr(10) + chr(2) + chr(12) + chr(8) + chr(0) + chr(0)      #20.35546875
      #   print 'sss=', s
      #   print 'ord=', ord(s[0])
      #   print 'ord=', ord(s[1])
      #   print 'ord=', ord(s[2])
      #   print 'ord=', ord(s[3])

        # Верный расчет
        st = '#GOGJROTVKHQITOU'
        st1 = ''
        for i in range(3):
            st1 += chr(self.decG_0(st[2*i + 9]) * 16 + self.decG_0(st[2*i + 10]))
        st1 += chr(0)
        #
        # print 'st1=', st1
        s = st1

#                st = chr(self.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
        
        

        
        # Пример температуры 19.8
        st = ''
        #s = chr(0x54) + chr(0x56) + chr(0x4b) + chr(0x00)
        #// Пример температуры 19.8
        
#a= 54564b00
        
        #
        # print 'ABC', 's=', s
        a1 = str(hex(ord(s[3])))[2:]
        # print 36
        if len(a1) == 1:
            a1 = '0' + a1
        # print 37
        a2 = str(hex(ord(s[2])))[2:]
        if len(a2) == 1:
            a2 = '0' + a2
        # print 38
        a3 = str(hex(ord(s[1])))[2:]
        if len(a3) == 1:
            a3 = '0' + a3
            pass
        # print 39
        a4 = str(hex(ord(s[0])))[2:]
        if len(a4) == 1:
            a4 = '0' + a4
        # print 35
        #
        a = a1 + a2 + a3 + a4
        # print 41
        #
        b = struct.unpack('<f', binascii.unhexlify(a))            
        # print 421
        # print 'str(b[0])=', str(b[0])
        # print 431
        return
        
        
        
        #Val = self.ReadDevice(self.port, 2, st)
        
        
        #return
        
        
        # print self.port.port
        self.port.port = 'COM2'
        try:
            self.port.close()
            self.port.open()



            st = chr(1)+chr(3)+chr(2)+chr(0)+chr(0)+chr(3) # ПР200 чтение сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(1)+chr(0)+chr(3) # ПР200 чтение сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(2)+chr(0)+chr(3) # ПР200 чтение сет. перем.
            
#            st = chr(1)+chr(6)+chr(2)+chr(0)+chr(3)+chr(5) # ПР200 запись в сет. перем.
#            st = chr(1)+chr(6)+chr(2)+chr(1)+chr(0)+chr(57) # ПР200 запись в сет. перем.

#            st = chr(1)+chr(6)+chr(2)+chr(0)+chr(0)+chr(3) # ПР200 запись в сет. перем.
#            st = chr(1)+chr(3)+chr(2)+chr(0)+chr(0)+chr(1) # ПР200 чтение сет. перем.
            


            st = chr(8)+chr(16)+chr(184)+chr(223)+chr(230)+chr(156) # ПР200 чтение сет. перем.
            st = chr(8)+chr(16)+chr(184)+chr(223) # ПР200 чтение сет. перем.
# 0 4 1 0 B 8 D F E 6 9 C)
            # Контрольная сумма
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])
            
            #st = 0x23474f 4849 4a50 564a 4747 4747 5652 504b 0d  
            #http://www.owen.ru/forum/archive/index.php/f-16.html
            #http://www.owen.ru/forum/archive/index.php/t-5397.html
            #http://www.owen.ru/forum/archive/index.php/t-5397.html
            st = chr(0x23)+chr(0x47)+chr(0x4f)+chr(0x48)+chr(0x49)+chr(0x4a)+chr(0x50)+chr(0x56)+chr(0x4a)+chr(0x47)+chr(0x47)+chr(0x47)+chr(0x47)+chr(0x56)+chr(0x52)+chr(0x50)+chr(0x4b)+chr(0x0d) 
            
            st = chr(0x23)+chr(0x47)+chr(0x4f)+chr(0x48)+chr(0x47)+chr(0x52)+chr(0x4f)+chr(0x54)+chr(0x56)+chr(0x4c)+chr(0x4c)+chr(0x53)+chr(0x4a)+chr(0x0d)
            st = '#GKHGROTVUMPS'+chr(0x0d)

   #GOHGROTVLLSJ. 14  COM2  
            st = '#GOHGROTVLLSJ'+chr(0x0d)
# 23 47 4f 48 47 52 4f 54 56 4c 4c 53 4a 0d  #GOHGROTVLLSJ. 14  COM2  
            
            #st = '#GKHGROTVUMPS'
            #st = '#GOHGROTVLLSJ'  

            # print 'st=', st
            # print 6
#            print ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5]), ord(st[6]), ord(st[7])
          #  print ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5]), ord(st[6]), ord(st[7])
            
            try:
                # print 11
                self.port.write(st)

                s = self.port.read(20)
                #s = self.port.read(15)
                ss = ''
                for i in range(len(s)):
                    ss += str(ord(s[i])) + '  '                    

                
                ss1 = ''
                for i in range(len(s)):
                    ss1 += chr(ord(s[i]))
                    

                #return

##############            if type_dev == 1:





                # Пример температуры 22.5
                s = chr(0x41) + chr(0xb4) + chr(0x49) + chr(0x00)    #22.5356445312
                s = chr(0x41) + chr(0xb4) + chr(0x38) + chr(0x00)   #20.35546875
                
                #// Пример температуры 22.5
                #s = chr(8)+chr(16)+chr(184)+chr(223)
                # print 'ABC', 's=', s
                a1 = str(hex(ord(s[3])))[2:]
                # print 36
                if len(a1) == 1:
                    a1 = '0' + a1
                # print 37
                a2 = str(hex(ord(s[2])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                # print 38
                a3 = str(hex(ord(s[1])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                # print 39
                a4 = str(hex(ord(s[0])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4
                # print 35
                
                a = a1 + a2 + a3 + a4
                # print 41
                
                b = struct.unpack('<f', binascii.unhexlify(a))            
                # print 420
                # print 'str(b[0])=', str(b[0])
                # print 430
                return
                
                
                
                a1 = str(hex(ord(s[4])))[2:]
                # print 36
                if len(a1) == 1:
                    a1 = '0' + a1
                # print 37
                a2 = str(hex(ord(s[3])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                # print 38
                a3 = str(hex(ord(s[6])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                # print 39
                a4 = str(hex(ord(s[5])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4
                # print 40
                a = a1 + a2 + a3 + a4
                # print 41
                b = struct.unpack('<f', binascii.unhexlify(a))            
                # print 42
                # print 'str(b[0])=', str(b[0])
                #
                # print 'str(hex(ord(s[4])))[2:]', str(hex(ord(s[4])))[2:]
                # print 'str(hex(ord(s[5])))[2:]', str(hex(ord(s[5])))[2:]
                # print 'str(hex(ord(s[6])))[2:]', str(hex(ord(s[6])))[2:]
                #
                # print 'q'
                a1 = str(hex(ord(s[4])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                # print 'a1=', a1
                a2 = str(hex(ord(s[5])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                # print 'a2=', a2
                a3 = str(hex(ord(s[6])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                # print 'a3=', a3
                a = '00' + a3 + a2 + a1
                a = a2 + a1 + a3 + '00'
                a = a3 + '00' +  a2 + a1
                # a = a1 + a2 + '00' + a3
                # print 'r'
                b = struct.unpack('<f', binascii.unhexlify(a))            
                # print 42
                # print '////////str(b[0])=', str(b[0])


###################################

                if len(s) < 1:
                    # print 8
                    msgBox(self, u"Данныееееееееееее с прибора №? не читаются!")
                else:
                    #Val = 3.3333    
                    # print 9
#                    msgBox(self, u"Показание прибора № " + str(i+1) + u': "' + str(Val) + '"')
                    msgBox(self, u"Показание прибора № ")
                
                
        
            except SerialException:
                ###isTestHeart = False
                self.errStr = u"Проблема работы прибора с адресом: " + command
                QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
           #     return None                            
            except Exception:
                ###isTestHeart = False
                self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                # print u'Ошибка чтения показаний прибора!'
            #    return None

           
        except SerialException:
            # print u"Порт " + self.port.port + u' не открывается!'
            self.errStr = u"Порт " + self.port.port + u' не открывается!'
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами!')
            return None
        finally:
            # print 'self.port.close()'
            self.port.close()




 
    def ReadDevice(self, port, type_dev, command, coeff):
        # type_dev = 0 Чтение показания прибора типа ЩП02М
        # type_dev = 1 Чтение показания прибора типа ЩП02П через регистры
        # type_dev = 2 Чтение показания прибора типа Щ02П
        # type_dev = 3 Чтение показания прибора типа Щ00П
        # type_dev = 101 Чтение показания прибора типа ТРМ202
        # command - команда write
        # coeff - поправочный коэффициент
        
        try:
            '''
            print port, type_dev, command, coeff
            print 'q'
            print 'command=', ord(command[0]),ord(command[1]),ord(command[2]),ord(command[3]),ord(command[4]),ord(command[5]),ord(command[6]),ord(command[7])
            print 'w'
            '''
#            time.sleep(1)
#            self.msleep(1000)
            
            port.baudrate = 9600
            if type_dev == 3:
                port.baudrate = 19200

            port.write(command)
            #print 'command=', command
                        
            if type_dev == 0:
                s = port.read(15)
                if len(s) < 13:
                    #self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                    return None            
#                print s[8] + s[7] + s[10] + s[9] + s[12] + s[11]            
                #return s[8] + s[7] + s[10] + s[9] + s[12] + s[11]
                val = s[8] + s[7] + s[10] + s[9] + s[12] + s[11]
                
                
            if type_dev == 1:
 #               print 11111111111111111
                s = port.read(16)
                a1 = str(hex(ord(s[4])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                a2 = str(hex(ord(s[3])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                a3 = str(hex(ord(s[6])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                a4 = str(hex(ord(s[5])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4
                a = a1 + a2 + a3 + a4
                b = struct.unpack('<f', binascii.unhexlify(a))            
#                print 444444444442, str(b[0])
#                return str(b[0])
                val = str(b[0])
 
            if type_dev == 2:
 #               print 22222222222222222
                s = port.read(15)
  #              print 44
  #              print 's=', s
                if len(s) < 13:
                    #self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                    return None            
   #             print s[6] + s[5] + s[8] + s[7] + s[10] + s[9]
#                return s[6] + s[5] + s[8] + s[7] + s[10] + s[9]
                val = s[6] + s[5] + s[8] + s[7] + s[10] + s[9]
    #            print 'val=', val
                

            if type_dev == 3:
                s = port.read(16)
                a1 = str(hex(ord(s[4])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                a2 = str(hex(ord(s[3])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                a3 = str(hex(ord(s[6])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                a4 = str(hex(ord(s[5])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4
                a = a1 + a2 + a3 + a4
                b = struct.unpack('<f', binascii.unhexlify(a))            
                val = str(b[0])



               
            if type_dev == 101:
     #           print 101
                s = port.read(16)
                #print 's=', s
                #print 355
                
                #s = '#GOGJROTVKHQITOU'
                st = ''
                for i in range(3):
                    st += chr(self.decG_0(s[2*i + 9]) * 16 + self.decG_0(s[2*i + 10]))
                st += chr(0)
                #print 'st=', st
                s = st
                #print 36
                #print 's1=', s
                  
                a1 = str(hex(ord(s[3])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                a2 = str(hex(ord(s[2])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                a3 = str(hex(ord(s[1])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                a4 = str(hex(ord(s[0])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4

                a = a1 + a2 + a3 + a4
                b = struct.unpack('<f', binascii.unhexlify(a))            
#                return str(b[0])
                val = str(b[0])
                #return str(b[1])
            val1 = float(val) * coeff
            return str(val1)
                        
        except SerialException:
            ###isTestHeart = False
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            ###isTestHeart = False
            self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
            # print u'Ошибка чтения показаний прибора!'
            return None

            
    def ReadDevice_2(self, port, type_dev, address, coeff):
        # В отличие от ReadDevice параметр command заменен параметром address
        # а command формируется внутри функции  
        # type_dev = 0 Чтение показания прибора типа ЩП02М
        # type_dev = 1 Чтение показания прибора типа ЩП02П через регистры
        # type_dev = 2 Чтение показания прибора типа Щ02П
        # type_dev = 101 Чтение показания прибора типа ТРМ202
        # address - алрес прибора
        # coeff - поправочный коэффициент
        
        try:
      #      print port, type_dev, address, coeff
#            print 'q'
#            print 'command=', ord(command[0]),ord(command[1]),ord(command[2]),ord(command[3]),ord(command[4]),ord(command[5]),ord(command[6]),ord(command[7])
#            print 'w'
            
            if type_dev == 0:
                command = chr(address)+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if type_dev == 1:
                command = chr(address)+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if type_dev == 2:
       #         print 'q'
                command = chr(address)+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)
        #    print 'w'
            command += chr(crc16(command)[0]) + chr(crc16(command)[1])           
        #    print 'e'
         #   print 'command=', ord(command[0]),ord(command[1]),ord(command[2]),ord(command[3]),ord(command[4]),ord(command[5]),ord(command[6]),ord(command[7])
            port.write(command)
         #   print 'command=', command
                        
            if type_dev == 0:
                s = port.read(15)
                if len(s) < 13:
                    return None            
                val = s[8] + s[7] + s[10] + s[9] + s[12] + s[11]
                
            if type_dev == 1:
                s = port.read(16)
                a1 = str(hex(ord(s[4])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                a2 = str(hex(ord(s[3])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                a3 = str(hex(ord(s[6])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                a4 = str(hex(ord(s[5])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4
                a = a1 + a2 + a3 + a4
                b = struct.unpack('<f', binascii.unhexlify(a))            
                val = str(b[0])
 
            if type_dev == 2:
          #      print 'e'
                s = port.read(15)
          #      print 's=', s, 'len(s)=', len(s)
                if len(s) < 13:
                    return None            
                val = s[6] + s[5] + s[8] + s[7] + s[10] + s[9]
          #      print 'val=', val
                
               
            if type_dev == 101:
#                print 101
                s = port.read(16)
                #print 's=', s
                #print 355
                
                #s = '#GOGJROTVKHQITOU'
                st = ''
                for i in range(3):
                    st += chr(self.decG_0(s[2*i + 9]) * 16 + self.decG_0(s[2*i + 10]))
                st += chr(0)
                #print 'st=', st
                s = st
                #print 36
                #print 's1=', s
                  
                a1 = str(hex(ord(s[3])))[2:]
                if len(a1) == 1:
                    a1 = '0' + a1
                a2 = str(hex(ord(s[2])))[2:]
                if len(a2) == 1:
                    a2 = '0' + a2
                a3 = str(hex(ord(s[1])))[2:]
                if len(a3) == 1:
                    a3 = '0' + a3
                a4 = str(hex(ord(s[0])))[2:]
                if len(a4) == 1:
                    a4 = '0' + a4

                a = a1 + a2 + a3 + a4
                b = struct.unpack('<f', binascii.unhexlify(a))            
#                return str(b[0])
                val = str(b[0])
                #return str(b[1])
 #           print 'val=', val
            val1 = float(val) * coeff
 #           print 'val1=', val1
            return str(val1)
                        
        except SerialException:
            ###isTestHeart = False
            self.errStr = u"Проблема работы прибора с адресом: " + str(address)
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + str(address), QMessageBox.Ok)
            return None                            
        except Exception:
            ###isTestHeart = False
            self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(address)
            # print u'Ошибка чтения показаний прибора!'
            return None

            
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
        print('Чтение параметров с devices.json файла, если таковой имеется')
        try:
            f = open('devices.json','r')
            self.data = json.load(f)
            print(self.data)
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
            self.ui.doubleSpinBox.setValue(self.data['accuracy']['r'])                                         
            self.ui.doubleSpinBox_2.setValue(self.data['accuracy']['a'])
            #3.06
            self.ui.checkBox.setChecked(self.data['min_alg'])              
            
            #19.02  
            self.ui.doubleSpinBox_3.setValue(self.data['pause'])  
            self.ui.comboBox.setCurrentIndex(self.data['ind_measureR'])

            self.ui.radioButton.setChecked(self.data['forward'])              
            self.ui.radioButton_2.setChecked(self.data['back'])              
        except Exception:
            # print u'Ошибка чтения devices.json!'
            self.data = {}


    def write_json(self):
        # ЗАПИСАТЬ
        f = open('devices.json','w')        
        self.toData()    
        json.dump(self.data, f)

        
    def toData(self):
        self.data = {}        
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
                        
        self.data['accuracy'] = {}
        self.data['accuracy']['r'] = self.ui.doubleSpinBox.value()
        #19.02
        self.data['accuracy']['a'] = self.ui.doubleSpinBox_2.value()
        #3.06
        self.data['min_alg'] = self.ui.checkBox.isChecked()
        self.data['pause'] = self.ui.doubleSpinBox_3.value()
        self.data['ind_measureR'] = self.ui.comboBox.currentIndex()
        
        self.data['forward'] = self.ui.radioButton.isChecked()
        self.data['back'] = self.ui.radioButton_2.isChecked()
                    

    def comboBox_currentIndexChanged(self, ind):
        i = int(self.sender().objectName())
        self.Measures[i].clear()
        if ind == 0:
            self.Measures[i].addItems(self.sMeasuresA)
        else:    
            self.Measures[i].addItems(self.sMeasuresV)
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
        self.Names[i].addItems(self.sNames)
        self.Names[i].setCurrentIndex(ind_name)
        self.Names[i].setFont(self.fnt)
        self.Names[i].setEnabled(activ)
        #self.Names[i].changeEvent.connect(self.comboBox_changeEvent)
        self.Names[i].currentIndexChanged['int'].connect(self.comboBox_currentIndexChanged)
        self.Names[i].setVisible(False)
            
        self.Types += [QtGui.QComboBox()]
        self.Types[i].addItems(self.sTypes)
        self.Types[i].setCurrentIndex(ind_type)
        self.Types[i].setFont(self.fnt)
        self.Types[i].setEnabled(activ)
        self.Types[i].setVisible(False)
        
        self.Measures += [QtGui.QComboBox()]
        if ind_name == 0:
            self.Measures[i].addItems(self.sMeasuresA)
        else:            
            self.Measures[i].addItems(self.sMeasuresV)
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
        self.Coeff[i].setDecimals(4)
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


    def PowerToKey(self, power):
        for i in range(len(powers)):
            if powers[i][1] == power:
                return powers[i][0]
        return None

    def commandCA5018(self, address, power):
        #Формирование команды для прибора CA5018
        pass
        key = self.PowerToKey(power)
        if key == None:
            return None
                        
       #Вычисление контрольной суммы         
        check_sum = 0
        check_sum = check_sum ^ address
        check_sum = check_sum ^ 5
        check_sum = check_sum ^ 1
        check_sum = check_sum ^ key  
        
        comand = chr(address) + chr(5) + chr(1) + chr(key) + chr(check_sum)
        return comand               
    

    def WriteToCA5018_(self, port, command):
        try:
            port.write(command)
            s = port.read(4)
            if len(s) < 4:
                return None            
            val = s[0] + s[1] + s[2] + s[3]                
            return val                        
        except SerialException:
            QMessageBox.warning(None, u"Предупреждение", u"_Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            # print u'Ошибка чтения показаний прибора!'
            QMessageBox.warning(None, u"Предупреждение", u"___Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None

    
    def WriteToCA5018(self, power, SecondCurrent):
        # command - команда write
        # print self.port1.port, self.port2.port
        
        if self.port1.port != 'COM0' and self.ca5018_1_active and SecondCurrent == 1:
            try:            
                self.port1.close()
                self.port1.open()
              
                command = self.commandCA5018(self.env.config.devices.ca5018_1.address, power)            
                # print 'command=', ord(command[0]), ord(command[1]), ord(command[2]), ord(command[3]), ord(command[4])
                self.WriteToCA5018_(self.port1, command)
                #
                # print 'finish'
            except SerialException:
                msgBox(self, u"Порт " + self.port1.port + u' не открывается!')
#                return None
            except Exception:
                msgBox(self, u'Проблема с портом ' + self.port1.port + u' либо с прибором!')
#                return None
            finally:
                self.port1.close()

        if self.port2.port != 'COM0' and self.ca5018_2_active and SecondCurrent == 5:
            try:            
                self.port2.close()
                self.port2.open()
            
                command = self.commandCA5018(self.env.config.devices.ca5018_2.address, power)            
                # print 'command=', ord(command[0]), ord(command[1]), ord(command[2]), ord(command[3]), ord(command[4])
                self.WriteToCA5018_(self.port2, command)
                # print 'finish'
            except SerialException:
                msgBox(self, u"Порт " + self.port2.port + u' не открывается!')
#                return None
            except Exception:
                msgBox(self, u'Проблема с портом ' + self.port2.port + u' либо с прибором!')
#                return None
            finally:
                self.port2.close()



    def commandCA5020(self, nDev, nCom, size, sel, s1, s2, pf, cur, freq):
        nByte1 = size % 256
        nByte2 = size // 256
        
        command = chr(nDev)+chr(nCom)+chr(nByte1)+chr(nByte2)
        b = struct.pack('f', s1)
        s1Byte1 = ord(b[0])
        s1Byte2 = ord(b[1])
        s1Byte3 = ord(b[2])
        s1Byte4 = ord(b[3])
                        
        b = struct.pack('f', s2)
        s2Byte1 = ord(b[0])
        s2Byte2 = ord(b[1])
        s2Byte3 = ord(b[2])
        s2Byte4 = ord(b[3])

        b = struct.pack('f', pf)
        pfByte1 = ord(b[0])
        pfByte2 = ord(b[1])
        pfByte3 = ord(b[2])
        pfByte4 = ord(b[3])
            
        b = struct.pack('f', cur)
        curByte1 = ord(b[0])
        curByte2 = ord(b[1])
        curByte3 = ord(b[2])
        curByte4 = ord(b[3])

        b = struct.pack('f', freq)
        freqByte1 = ord(b[0])
        freqByte2 = ord(b[1])
        freqByte3 = ord(b[2])
        freqByte4 = ord(b[3])
            
        command += chr(sel)+chr(s1Byte1)+chr(s1Byte2)+chr(s1Byte3)+chr(s1Byte4)+ \
                            chr(s2Byte1)+chr(s2Byte2)+chr(s2Byte3)+chr(s2Byte4)+ \
                            chr(pfByte1)+chr(pfByte2)+chr(pfByte3)+chr(pfByte4)+ \
                            chr(curByte1)+chr(curByte2)+chr(curByte3)+chr(curByte4)+ \
                            chr(freqByte1)+chr(freqByte2)+chr(freqByte3)+chr(freqByte4)
                           
        check_sum = self.ComputeChecksumCA5020([nDev, nCom, nByte1, nByte2, sel, s1Byte1, s1Byte2, s1Byte3, s1Byte4,
                                                                                 s2Byte1, s2Byte2, s2Byte3, s2Byte4,
                                                                                 pfByte1, pfByte2, pfByte3, pfByte4,
                                                                                 curByte1, curByte2, curByte3, curByte4,
                                                                                 freqByte1, freqByte2, freqByte3, freqByte4])
        chs1 = check_sum % 256
        chs2 = check_sum // 256
        command += chr(chs1)+chr(chs2)
        return command 
        

    def WriteToCA5020_(self, port, command):
        try:
            port.write(command)
            s = port.read(8)
            # print '___command = ', ' '.join(format(ord(x), 'b') for x in command)
            if len(s) < 4:
                return None
            
            val = ''           
            for i in range(len(s)):
                val += s[i]            
                
            return val
                        
        except SerialException:
            QMessageBox.warning(None, u"Предупреждение", u"_Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            # print u'Ошибка чтения показаний прибора!'
            QMessageBox.warning(None, u"Предупреждение", u"___Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None


    def WriteToCA5020(self, power, SecondCurrent):
        # command - команда write
#        print self.port4.port, self.port4.baudrate
        
#        msgBox(self, u"port/baudrate = " + self.port4.port + '/' + str(self.port4.baudrate)) #27.09.2021
#        msgBox(self, u"Отправляем данные на прибор: Порт - " + self.port4.port + u', нагрузка - ' + str(power) + u', ток - ' + str(SecondCurrent))
####        time.sleep(0.1)
#        time.sleep(0.5)
#        time.sleep(3)
        
        if self.port4.port != 'COM0':
            try:            
                self.port4.close()
                self.port4.open()
                # print 'power = ', power, '  SecondCurrent = ', SecondCurrent
                command = self.commandCA5020(5, 1, 27, 1, power, 0, 0.8, SecondCurrent, 50)            
                Val = self.WriteToCA5020_(self.port4, command)
                if Val == None:
                    msgBox(self, u"Данные с прибора CA5020 не читаются!")
            
                # print 'finish'
            except SerialException:
                msgBox(self, u"Порт " + self.port4.port + u' не открывается!')
#                return None
            except Exception:
                msgBox(self, u'Проблема с портом ' + self.port4.port + u' либо с прибором!')
#                return None
            finally:
                self.port1.close()

        
        

    '''
    def commandCA5020(self, address, power):
        #Формирование команды для прибора CA5020
        print 'qqq'  
        pass
        key = self.PowerToKey(power)
        if key == None:
            return None
                        
       #Вычисление контрольной суммы         
        check_sum = 0
        check_sum = check_sum ^ address
        check_sum = check_sum ^ 5
        check_sum = check_sum ^ 1
        check_sum = check_sum ^ key  
        
        comand = chr(address) + chr(5) + chr(1) + chr(key) + chr(check_sum)
        return comand               
    '''
                
    '''
    def WriteToCA5020(self, port, command):
        print 'ComputeChecksumCA5020([5, 255, 6, 0]) = ', ComputeChecksumCA5020([5, 255, 6, 0])
        print 'ComputeChecksumCA5020([5, 255, 0, 6]) = ', ComputeChecksumCA5020([5, 255, 0, 6])
        print 'ComputeChecksumCA5020([5, 255, 6, 6]) = ', ComputeChecksumCA5020([5, 255, 6, 6])
        print 'ComputeChecksumCA5020([5, 255, 0, 0]) = ', ComputeChecksumCA5020([5, 255, 0, 0])
        
        return
       
        
        
        try:
            port.write(command)
            s = port.read(4)
            if len(s) < 4:
                return None            
            val = s[0] + s[1] + s[2] + s[3]                
            return val                        
        except SerialException:
            QMessageBox.warning(None, u"Предупреждение", u"_Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            print u'Ошибка чтения показаний прибора!'
            QMessageBox.warning(None, u"Предупреждение", u"___Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None
'''




#    def WriteToPR200(self, adr_dev, adr_reg, val):
    def WriteToPR200(self, adr_reg, val):
        
#        command = self.commandCA5018(self.env.config.devices.ca5018_1.address, power)
        '''
        print 'val=', val            
        command1 = chr(self.env.config.devices.pr200.address)
        command2 = chr(int(math.floor(adr_reg/256)))
        command3 = chr(int(math.fmod(adr_reg, 256)))
        command4 = chr(val)
           '''     
#        command = chr(self.env.config.devices.pr200.address)+chr(6)+chr(int(math.floor(adr_reg/256)))+chr(int(math.fmod(adr_reg, 256)))+chr(0)+chr(val) # ПР200 запись в сет. перем.
        command = chr(self.env.config.devices.pr200.address)+chr(6)+chr(int(math.floor(adr_reg/256)))+chr(int(math.fmod(adr_reg, 256)))+chr(int(math.floor(val/256)))+chr(int(math.fmod(val, 256))) # ПР200 запись в сет. перем.
        # print 'self.env.config.devices.pr200.address = ', self.env.config.devices.pr200.address
#        command = chr(adr_dev)+chr(6)+chr(int(math.floor(adr_reg/256)))+chr(int(math.fmod(adr_reg, 256)))+chr(0)+chr(val) # ПР200 запись в сет. перем.
        # Контрольная сумма
        command += chr(crc16(command)[0]) + chr(crc16(command)[1])
        
        s = ''
        for i in range(len(command)):
            s += str(ord(command[i])) + '  '
                    
        # print 's = ', s
        
        
        
        try:
            self.port3.close()
            self.port3.open()

#            print 'command = ', ord(command[0]), ord(command[1]), ord(command[2]), ord(command[3]), ord(command[4]), ord(command[5]), ord(command[6]), ord(command[7])
            
            try:
                self.port3.write(command)
                        
                s = self.port3.read(20)
                #s = self.port.read(15)
                # print 's', s
                # print 'len(s)', len(s)
                ss = ''
                for i in range(len(s)):
                    ss += str(ord(s[i])) + '  '
                #
                # print 'ss=', ss

                if len(s) < 1:
                    return None
                return
            
                '''
                    print 8
                    msgBox(self, u"Данныееееееееееее с прибора №? не читаются!")
                else:
                    #Val = 3.3333    
                    print 9
#                    msgBox(self, u"Показание прибора № " + str(i+1) + u': "' + str(Val) + '"')
                    msgBox(self, u"Показание прибора № ")
                '''
                
        
            except SerialException:
                ###isTestHeart = False
                self.errStr = u"Проблема работы прибора с адресом: " + command
                QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
                return None                            
            except Exception:
                ###isTestHeart = False
                self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                # print u'Ошибка чтения показаний прибора!'
                return None
        
        except SerialException:
            # print u"Порт " + self.port3.port + u' не открывается!'
            self.errStr = u"Порт " + self.port3.port + u' не открывается!'
            msgBox(self, u"Порт " + self.port3.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с приборами!')
            return None
        finally:
            # print 'self.port.close()'
            self.port3.close()
        
        
        
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

     
    from dpframe.base.envapp import checkenv
    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import default_log_init
    from electrolab.gui.inits import serial_devices_init
           
    # @serial_devices_init
    @json_config_init
    @default_log_init
    class ForEnv(QWidget):
        def getEnv(self):
            return self.env
    
    
    objEnv = ForEnv()
    env = objEnv.getEnv()
                            
    wind = Devices(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())
