# -*- coding: UTF-8 -*-

'''
Created on 22.04.2020
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

import ui.ico_64_rc

import json
import time
import devices

print "jnkjbnibiubibuib"
#QtCore
#QtGui.QSpinBox.setValue()
#QtGui.QLabel.setText()


#~ Table of CRC values for high–order byte
'''
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
'''



class TestDevices(QtGui.QDialog, UILoader):
    def __init__(self, _env):
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"testDevices.ui")
        self.setEnabled(False)

        self.env = _env
        self.port = Serial()
#        self.port.port = _env.config.devices.chp02m.port
#        print "self.port.port1 = " + self.port.port 
#        self.port.port = "COM" + str(self.ui.spinBox_10.value())
#        print "self.port.port2 = " + self.port.port 
#        self.port.baudrate = 9600
        self.port.baudrate = 115200
#        msgBox(self, u'Скорость порта = ' + str(self.port.baudrate))

        self.port.bytesize = 8
        self.port.parity = 'N'
        self.port.stopbits = 1
        self.port.timeout = 0.1
       
        self.ui.spinBox.valueChanged.connect(self.spinBox_valueChanged)
        self.ui.spinBox_4.valueChanged.connect(self.spinBox_valueChanged)
        self.ui.pushButton.clicked.connect(self.pushButton_Click)

        self.ui.spinBox_6.valueChanged.connect(self.spinBox_6_valueChanged)
        
        self.ui.doubleSpinBox.valueChanged.connect(self.doubleSpinBox_valueChanged)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.doubleSpinBox_valueChanged)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.doubleSpinBox_valueChanged)
        self.ui.doubleSpinBox_4.valueChanged.connect(self.doubleSpinBox_valueChanged)
                
        self.ui.spinBox_7.valueChanged.connect(self.spinBox_7_valueChanged)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)



        self.powers = [[0,50],[1,40],[2,30],[3,25],[4,20],[5,15],[6,12.5],[7,10],[8,7.5],[9,6.25],[10,5],[11,3.75],[12,3],[13,2.5],[14,1.75],[15,1.25],[16,1],
                       [17,0],[18,0.8],[19,1],[20,1.25],[21,1.5],[22,2],[23,2.5],[24,3.75],[25,5],[26,7.5],[27,10],[28,15]]

        self.spinBox_valueChanged()
        self.spinBox_7_valueChanged()

        self.ui.radioButton.toggled.connect(self.radioButton_Toggle)
        self.ui.radioButton_2.toggled.connect(self.radioButton_Toggle)
        self.Devices = Devices(self.env)        
#        self.comCA5020 = None
#        self.spinBox_6_valueChanged()
        self.comCA5020 = self.FormComCA5020(1)
        
                
    def spinBox_valueChanged(self):
#        return
        for p in self.powers:
            if p[0] == self.ui.spinBox_4.value():
                self.ui.label_7.setText('(' + str(p[1]) + u' ВА)')
                        
       #Вычисление контрольной суммы         
        check_sum = 0
        check_sum = check_sum ^ self.ui.spinBox.value()
        check_sum = check_sum ^ self.ui.spinBox_2.value()
        check_sum = check_sum ^ self.ui.spinBox_3.value()
        check_sum = check_sum ^ self.ui.spinBox_4.value()                
        self.ui.spinBox_5.setValue(check_sum)
        

    def pushButton_Click(self):
        try:
                        
            st = chr(self.ui.spinBox.value())+chr(self.ui.spinBox_2.value())+chr(self.ui.spinBox_3.value())+chr(self.ui.spinBox_4.value())+chr(self.ui.spinBox_5.value())
            print 'st=', ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4])
 
            self.port.port = "COM" + str(self.ui.spinBox_10.value())
            print "self.port.port2 = " + self.port.port 
           
            print 1
            self.port.close()
            print 2
            self.port.open()
            print 3
                        
            Val = self.ReadDevice(self.port, st)
            if Val == None:
                msgBox(self, u"Данные с прибора не читаются!")
                return None
#            self.ui.spinBox_6.setValue(ord(Val[0]))
#            self.ui.spinBox_7.setValue(ord(Val[2]))
#            self.ui.spinBox_8.setValue(ord(Val[3]))
#            self.ui.spinBox_9.setValue(ord(Val[4]))            
            self.ui.lineEdit.setText(str(ord(Val[0])))
            self.ui.lineEdit_2.setText(str(ord(Val[1])))
            self.ui.lineEdit_3.setText(str(ord(Val[2])))
            self.ui.lineEdit_4.setText(str(ord(Val[3])))

        except SerialException:
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с прибором!')
            return None
        finally:
            self.port.close()

        
    def ReadDevice(self, port,  command):
        # command - команда write
        try:
            print 4
            port.write(command)
            print 5                        
            s = port.read(4)
            print 6
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




    def spinBox_6_valueChanged(self):
        print 'qqqqqqqqqqqqqqqqqqqqq'
        self.ui.label_32.setEnabled(self.ui.spinBox_6.value() == 1)
        self.ui.label_33.setEnabled(self.ui.spinBox_6.value() == 2)
        self.ui.doubleSpinBox.setEnabled(self.ui.spinBox_6.value() == 1)
        self.ui.doubleSpinBox_2.setEnabled(self.ui.spinBox_6.value() == 2)
        self.comCA5020 = self.FormComCA5020(2)
        

    def doubleSpinBox_valueChanged(self):
        print 'wwwwwwwwwwwwwwwwwwww'
        self.comCA5020 = self.FormComCA5020(2)


    def spinBox_7_valueChanged(self):
        return
       #Вычисление контрольной суммы         
        check_sum = 0
        check_sum = check_sum ^ self.ui.spinBox_7.value()
        print 'check_sum=', check_sum
        check_sum = check_sum ^ self.ui.spinBox_11.value()
        print 'check_sum=', check_sum
        check_sum = check_sum ^ self.ui.spinBox_8.value()                
        print 'check_sum=', check_sum
        self.ui.spinBox_9.setValue(check_sum)
        print 'spinBox_7_valueChanged'


    def rs232_checksum(self, the_bytes):
        return bytes('%02X' % (sum(map(ord, the_bytes)) % 256))

    '''
    def crc16(self, data) :
        uchCRCHi = 0xFF   # high byte of CRC initialized
        uchCRCLo = 0xFF   # low byte of CRC initialized
        uIndex   = 0x0000 # will index into CRC lookup table

        for ch in data :
            uIndex   = uchCRCLo ^ ord(ch)
            uchCRCLo = uchCRCHi ^ auchCRCHi[uIndex]
            uchCRCHi = auchCRCLo[uIndex]
        return (uchCRCHi << 8 | uchCRCLo)
    '''

    '''
        public static ushort ComputeChecksum(byte[] bytes)
        {//Расчет CRC16
            ushort crc = 0;
            foreach (var b in bytes)
            {
                var index = (byte)(crc ^ b);
                crc = (ushort)((crc >> 8) ^ Table[index]);
                MessageBox.Show(index.ToString() + "   " + crc.ToString());
            }
            return crc;
        }

    '''
    def ComputeChecksum(self, st):
        crc = 0;
        for i in range(len(st)):
            b = st[i]
            index = (crc ^ b)
            while index >= 256:
                index -= 256 
 
            crc = ((crc >> 8) ^ self.Table[index]);
#            print st[i], index, crc
        return crc    


    def pushButton_2_Click(self):
        
        try:
#            st = chr(self.ui.spinBox_7.value())+chr(self.ui.spinBox_11.value())+chr(self.ui.spinBox_8.value())+chr(self.ui.spinBox_13.value())+chr(self.ui.spinBox_9.value())+chr(self.ui.spinBox_14.value())
#            print 'st=', st, '       ',  ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5])
 
            #a = toBinary(st)
#            print ' '.join(format(ord(x), 'b') for x in st)
 
            self.port.port = "COM" + str(self.ui.spinBox_12.value())
            print "self.port.port2 = " + self.port.port 
            
            self.port.close()
            self.port.open()
                        
#            Val = self.ReadDeviceCA5020(self.port, st)
            print 'self.comCA5020 = ', self.comCA5020
            Val = self.ReadDeviceCA5020(self.port, self.comCA5020)
            if Val == None:
                msgBox(self, u"Данные с прибора не читаются!")
                return None
            if len(Val) > 0:
                self.ui.lineEdit_5.setText(str(ord(Val[0])))
            if len(Val) > 1:
                self.ui.lineEdit_6.setText(str(ord(Val[1])))
            if len(Val) > 2:
                self.ui.lineEdit_7.setText(str(ord(Val[2])))
            if len(Val) > 3:
                self.ui.lineEdit_8.setText(str(ord(Val[3])))
            if len(Val) > 4:
                self.ui.lineEdit_9.setText(str(ord(Val[4])))
            if len(Val) > 5:
                self.ui.lineEdit_10.setText(str(ord(Val[5])))
            if len(Val) > 6:
                self.ui.lineEdit_11.setText(str(ord(Val[6])))
            if len(Val) > 7:
                self.ui.lineEdit_12.setText(str(ord(Val[7])))

        except SerialException:
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с прибором!')
            return None
        finally:
            self.port.close()

        return        
                
#        import devices
#        self.Devices = Devices(self.env)        
        
        nDev = self.ui.spinBox_7.value()
        nCom = self.ui.spinBox_11.value()
        nByte1 = self.ui.spinBox_8.value()
        nByte2 = self.ui.spinBox_13.value()

#        print '-----ComputeChecksumCA5020([]) = ', self.Devices.ComputeChecksumCA5020([5, 255, 6, 0])
#        print '-----ComputeChecksumCA5020([]) = ', self.Devices.ComputeChecksumCA5020([self.ui.spinBox_7.value(), self.ui.spinBox_11.value(), self.ui.spinBox_8.value(), self.ui.spinBox_13.value()])
        check_sum = self.Devices.ComputeChecksumCA5020([nDev, nCom, nByte1, nByte2])
#        check_sum = self.Devices.ComputeChecksumCA5020([self.ui.spinBox_7.value(), self.ui.spinBox_11.value(), self.ui.spinBox_8.value(), self.ui.spinBox_13.value()])
        print check_sum
        print check_sum % 256
        print check_sum // 256
        
        self.ui.spinBox_9.setValue(check_sum % 256)
        self.ui.spinBox_14.setValue(check_sum // 256)
        
        print 12345

        a = 1.2
        import struct
        val = 123.456
        b = struct.pack('f', val)
        #print len(val)
        print len(b)
        print b
        print b[0],b[1]
        print ord('a')
        print ord(b[0])
        #print b[0], int(b[0])
        c = struct.unpack('f', b)
        print c


        
        
        '''
        print 100 // 30
        print 100 // 40
        print 100 // 41
        print 100 // 39
        
        print 100 % 30
        print 100 % 40
        print 100 % 41
        print 100 % 39
'''
#self.ui.spinBox_6.value()
        return



        print '--ComputeChecksumCA5020([5, 255, 6, 0]) = ', self.Devices.WriteToCA5020(None, None)

        return
        print 'ComputeChecksum([5, 255, 6, 0]) = ', ComputeChecksum([5, 255, 6, 0])
        return
        
        self.Table = [
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


        print 'ComputeChecksum([5, 255, 6, 0]) = ', self.ComputeChecksum([5, 255, 6, 0])
        print 'ComputeChecksum([5, 255, 0, 6]) = ', self.ComputeChecksum([5, 255, 0, 6])
              

        return


        try:
                        
 #           st = chr(self.ui.spinBox_7.value())+chr(self.ui.spinBox_11.value())+chr(0)+chr(self.ui.spinBox_8.value())+chr(0)+chr(self.ui.spinBox_9.value())
 #           print 'st=', st, '       ',  ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5])
 
            st = chr(self.ui.spinBox_7.value())+chr(self.ui.spinBox_11.value())+chr(self.ui.spinBox_8.value())+chr(self.ui.spinBox_13.value())+chr(self.ui.spinBox_9.value())+chr(self.ui.spinBox_14.value())
            print 'st=', st, '       ',  ord(st[0]), ord(st[1]), ord(st[2]), ord(st[3]), ord(st[4]), ord(st[5])
 
            #a = toBinary(st)
            print ' '.join(format(ord(x), 'b') for x in st)
 
            self.port.port = "COM" + str(self.ui.spinBox_12.value())
            print "self.port.port2 = " + self.port.port 
           
            print 1
            self.port.close()
            print 2
            self.port.open()
            print 3
                        
            Val = self.ReadDeviceCA5020(self.port, st)
            if Val == None:
                msgBox(self, u"Данные с прибора не читаются!")
                return None
            if len(Val) > 0:
                self.ui.lineEdit_5.setText(str(ord(Val[0])))
            if len(Val) > 1:
                self.ui.lineEdit_6.setText(str(ord(Val[1])))
            if len(Val) > 2:
                self.ui.lineEdit_7.setText(str(ord(Val[2])))
            if len(Val) > 3:
                self.ui.lineEdit_8.setText(str(ord(Val[3])))
            if len(Val) > 4:
                self.ui.lineEdit_9.setText(str(ord(Val[4])))
            if len(Val) > 5:
                self.ui.lineEdit_10.setText(str(ord(Val[5])))
            if len(Val) > 6:
                self.ui.lineEdit_11.setText(str(ord(Val[6])))
            if len(Val) > 7:
                self.ui.lineEdit_12.setText(str(ord(Val[7])))

        except SerialException:
            msgBox(self, u"Порт " + self.port.port + u' не открывается!')
            return None
        except Exception:
            msgBox(self, u'Проблема с портом либо с прибором!')
            return None
        finally:
            self.port.close()


    def FormComCA5020(self, n):
        nDev = self.ui.spinBox_7.value()
        nCom = self.ui.spinBox_11.value()
        nByte1 = self.ui.spinBox_8.value()
        nByte2 = self.ui.spinBox_13.value()
        st = chr(nDev)+chr(nCom)+chr(nByte1)+chr(nByte2)
        if n == 1:
            check_sum = self.Devices.ComputeChecksumCA5020([nDev, nCom, nByte1, nByte2])
        if n == 2:
            sel = self.ui.spinBox_6.value()
                        
            s1 = self.ui.doubleSpinBox.value()
            b = struct.pack('f', s1)
            s1Byte1 = ord(b[0])
            s1Byte2 = ord(b[1])
            s1Byte3 = ord(b[2])
            s1Byte4 = ord(b[3])
                        
            s2 = self.ui.doubleSpinBox_2.value()
            b = struct.pack('f', s2)
            s2Byte1 = ord(b[0])
            s2Byte2 = ord(b[1])
            s2Byte3 = ord(b[2])
            s2Byte4 = ord(b[3])

            pf = self.ui.doubleSpinBox_3.value()
            b = struct.pack('f', pf)
            pfByte1 = ord(b[0])
            pfByte2 = ord(b[1])
            pfByte3 = ord(b[2])
            pfByte4 = ord(b[3])
            
            cur = self.ui.doubleSpinBox_4.value()
            b = struct.pack('f', cur)
            curByte1 = ord(b[0])
            curByte2 = ord(b[1])
            curByte3 = ord(b[2])
            curByte4 = ord(b[3])

            freq = self.ui.doubleSpinBox_5.value()
            b = struct.pack('f', freq)
            freqByte1 = ord(b[0])
            freqByte2 = ord(b[1])
            freqByte3 = ord(b[2])
            freqByte4 = ord(b[3])
            
            st += chr(sel)+chr(s1Byte1)+chr(s1Byte2)+chr(s1Byte3)+chr(s1Byte4)+ \
                           chr(s2Byte1)+chr(s2Byte2)+chr(s2Byte3)+chr(s2Byte4)+ \
                           chr(pfByte1)+chr(pfByte2)+chr(pfByte3)+chr(pfByte4)+ \
                           chr(curByte1)+chr(curByte2)+chr(curByte3)+chr(curByte4)+ \
                           chr(freqByte1)+chr(freqByte2)+chr(freqByte3)+chr(freqByte4)
                           
            check_sum = self.Devices.ComputeChecksumCA5020([nDev, nCom, nByte1, nByte2, sel, s1Byte1, s1Byte2, s1Byte3, s1Byte4,
                                                                                             s2Byte1, s2Byte2, s2Byte3, s2Byte4,
                                                                                             pfByte1, pfByte2, pfByte3, pfByte4,
                                                                                             curByte1, curByte2, curByte3, curByte4,
                                                                                             freqByte1, freqByte2, freqByte3, freqByte4])
        
        chs1 = check_sum % 256
        chs2 = check_sum // 256
        self.ui.spinBox_9.setValue(chs1)
        self.ui.spinBox_14.setValue(chs2)
        
        st += chr(chs1)+chr(chs2)
        return st 




        
    def ReadDeviceCA5020(self, port,  command):
        # command - команда write
        
        print len(command)
        print command
        
        try:
            
            '''
            s = 'ABCDEFGHIJ'           
            val = ''           
            for i in range(len(s)):
                val += s[i]            
            return val
'''
            
            print 'port.baudrate = ', port.baudrate
            
            port.write(command)
            s = port.read(8)
            print 6
            print 'command = ', ' '.join(format(ord(x), 'b') for x in command)
            if len(s) < 4:
                return None
            
            val = ''           
            for i in range(len(s)):
                val += s[i]            
#            val = s[0] + s[1] + s[2] + s[3] + s[4] + s[5] + s[6] + s[7]
                
            return val
                        
        except SerialException:
            QMessageBox.warning(None, u"Предупреждение", u"_Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            print u'Ошибка чтения показаний прибора!'
            QMessageBox.warning(None, u"Предупреждение", u"___Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None


    def radioButton_Toggle(self, check):
        pass
        if self.ui.radioButton.isChecked():
#            self.ui.spinBox_8.setValue(0)
#            self.ui.spinBox_13.setValue(6)

#            self.ui.spinBox_8.setValue(6)
#            self.ui.spinBox_13.setValue(0)
#            self.ui.spinBox_9.setValue(92)
#            self.ui.spinBox_14.setValue(51)
            self.ui.label_31.setEnabled(False)
            self.ui.label_32.setEnabled(False)
            self.ui.label_33.setEnabled(False)
            self.ui.label_34.setEnabled(False)
            self.ui.label_35.setEnabled(False)
            self.ui.label_36.setEnabled(False)
            self.ui.spinBox_6.setEnabled(False)
            self.ui.doubleSpinBox.setEnabled(False)
            self.ui.doubleSpinBox_2.setEnabled(False)
            self.ui.doubleSpinBox_3.setEnabled(False)
            self.ui.doubleSpinBox_4.setEnabled(False)
            self.ui.doubleSpinBox_5.setEnabled(False)
            #self.ui.spinBox_29.setEnabled(False)
            self.ui.spinBox_11.setValue(255)
            self.ui.spinBox_8.setValue(6)
            self.comCA5020 = self.FormComCA5020(1)
            
        else:    
            self.ui.label_31.setEnabled(True)
            self.ui.label_32.setEnabled(True)
            self.ui.label_33.setEnabled(True)
            self.ui.label_34.setEnabled(True)
            self.ui.label_35.setEnabled(True)
            self.ui.label_36.setEnabled(True)
            self.ui.spinBox_6.setEnabled(True)
            self.ui.doubleSpinBox.setEnabled(True)
            self.ui.doubleSpinBox_2.setEnabled(True)
            self.ui.doubleSpinBox_3.setEnabled(True)
            self.ui.doubleSpinBox_4.setEnabled(True)
            self.ui.doubleSpinBox_5.setEnabled(True)
            #self.ui.spinBox_29.setEnabled(True)
            self.spinBox_6_valueChanged()
            self.ui.spinBox_11.setValue(1)
            self.ui.spinBox_8.setValue(27)
            self.comCA5020 = self.FormComCA5020(2)
#            self.ui.spinBox_8.setValue(6)
#            self.ui.spinBox_13.setValue(0)

#            self.ui.spinBox_8.setValue(0)
#            self.ui.spinBox_13.setValue(6)
#            self.ui.spinBox_9.setValue(176)
#            self.ui.spinBox_14.setValue(254)

#            self.ui.spinBox_8.setValue(6)
#            self.ui.spinBox_13.setValue(0)
#            self.ui.spinBox_9.setValue(51)
#            self.ui.spinBox_14.setValue(92)






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
                            
    wind = TestDevices(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())

