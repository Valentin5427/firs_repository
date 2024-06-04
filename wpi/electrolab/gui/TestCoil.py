# -*- coding: UTF-8 -*-work
#

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QGraphicsScene
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent, QIcon, QFont
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from serial import Serial
from serial.serialutil import SerialException

from dpframe.tech.SimpleSound import SimpleSound

from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
from electrolab.app.item import Item
from  electrolab.gui.devices import Devices
from electrolab.gui.TestCoilReport import TestCoilReport
from electrolab.gui.reporting import FRPrintForm
from win32com.client import Dispatch
import stat

import json
import math
import time
import datetime

import binhex
import binascii
import struct
import socket

global port
port = Serial()

model = QSqlQueryModel()
model_ = QSqlQueryModel()
model__ = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
model_4 = QSqlQueryModel()
model_5 = QSqlQueryModel()

#Флаг глобального состояния 
PAUSE = u'PAUSE'
WORK = u'WORK'
stateWork = PAUSE
isReadPort = False                                 
isBreak = False
stop = True       # для создания пауз в потоке

yyy = 0  #Для эмуляции      

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

# Расчет контрольной суммы по протоколу modbus
def crc16(data):
    uchCRCHi = 0xFF   # high byte of CRC initialized
    uchCRCLo = 0xFF   # low byte of CRC initialized
    uIndex   = 0x0000 # will index into CRC lookup table

    for ch in data :
        uIndex   = uchCRCLo ^ ord(ch)
        uchCRCLo = uchCRCHi ^ auchCRCHi[uIndex]
        uchCRCHi = auchCRCLo[uIndex]
    return uchCRCLo, uchCRCHi

withCol1 = 100


class MyFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
    def widthArea(self, tableView):
        # Возвращает ширину свободной области таблицы tableView
        HSWidth = tableView.verticalHeader().width() + 4
        if tableView.verticalScrollBar().width() < 100 and tableView.verticalScrollBar().isVisible():
            HSWidth += tableView.verticalScrollBar().width()
        return tableView.width() - HSWidth    
    def eventFilter(self, obj, e):
        try:
            QtCore.QEvent.Resize
        except:
            return True
        
        global VSB1
        
        if obj.objectName() == 'tv1' and (e.type() != QtCore.QEvent.Resize or VSB1 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / withCol1)
            obj.setColumnWidth(1, koef * withCol1)
            VSB1 = obj.verticalScrollBar().isVisible()
            
        return False


                                 
class MyThread(QtCore.QThread):
        signal1 = pyqtSignal()
        signal2 = pyqtSignal()


        def __init__(self, parent = None):
            QtCore.QThread.__init__(self, parent)
        def run(self):
            nComError = 0        
            
            global AV, points, points_back, stateWork, yyy, oldPoints_, getSecondCurrent 

            self.nPoint = 0
            points = []
            points_back = []
            oldPoints_ = []
            #29.10.2018
            getSecondCurrent = False        # Признак достижения графиком номинального тока                
            
            yyy = 0
            
            stateWork = WORK
            AV = None
            while stateWork == WORK:
               # print 'isBreakisBreakisBreakisBreakisBreakisBreakisBreakisBreakisBreakisBreakisBreakisBreak=', isBreak
                global isReadPort
                isReadPort = False
                self.emit(QtCore.SIGNAL('treadsignal'))
                self.msleep(10)
                #Задержка, чтобы цикл не проскакивал                
                while not isReadPort:
                    self.emit(QtCore.SIGNAL('signal1'))
                   # print '_____________11111111111111111111111111111111111111'
                    time.sleep(0.001)
                    pass                                        
                self.emit(QtCore.SIGNAL('signal3'))
                
                if AV == None:
                    if stateWork == PAUSE:
                        return
                    nComError += 1
                
                    self.emit(QtCore.SIGNAL('mysignal'))
                    time.sleep(0.001)   #Задержка, чтобы цикл не проскакивал
                                
                    if nComError < 10:
                        continue
                    else:
                        nComError = 0
                    
                        self.emit(QtCore.SIGNAL('mysignal2'))
                        return
                                
                nComError = 0

                global isBreak, stop
                isBreak = False
                stop = True        
                self.emit(QtCore.SIGNAL('mysignal3'))
                while stop: 
                    self.emit(QtCore.SIGNAL('signal2'))
                    time.sleep(0.001)
                    pass
                self.emit(QtCore.SIGNAL('signal3'))
             #   time.sleep(0.001)   #Задержка, чтобы цикл не проскакивал
             #  time.sleep(0.1)   #Задержка, чтобы цикл не проскакивал
                if isBreak == True:
                    return
                time.sleep(0.001)   #Задержка, чтобы цикл не проскакивал
            return


class TestCoil(QWidget, UILoader):    
    def __init__(self, _env, oMap, tvItem, tvCoil, btnStart, VerificationForm):

#19.01.2023
#        self.f = open('WPT.log', 'w')
#        self.f.write(u'Begin ' + str(datetime.datetime.now()) + '\n')
#        self.f.close()
        
                
        super(QWidget, self).__init__()
#*****        self.setUI(_env.config, u"TestCoil.ui")
        self.setUI(_env.config, u"TestCoil_.ui")
        self.setEnabled(False)
        # временно для эмуляции
        self.yyy = 0.4
        self.ui.radioButton.setVisible(False)
        self.ui.radioButton_2.setVisible(False)

        self.sound = SimpleSound()

        self.query = QSqlQuery(_env.db)
        self.query_2 = QSqlQuery(_env.db)
        self.query_3 = QSqlQuery(_env.db)
        self.query_4 = QSqlQuery(_env.db)
        self.query_5 = QSqlQuery(_env.db)
        self.query_9 = QSqlQuery(_env.db)
                
        self.oMap = oMap    
        
        self.tvItem = tvItem
        self.tvCoil = tvCoil
        self.btnStart = btnStart
               
        self.VerificationForm = VerificationForm
        try:
            self.VerificationForm.ui.lbShortName.setWordWrap(True)
        except Exception:
            pass
            
        self.idStand = None
        self.idItem = None
        self.idCoil = None
        self.idItemLast = None
        self.idCoilLast = None
        self.K = None              # Коэффициент
        self.nomVoltage = None     # Номинальное напряжение

        self.curr_r  = None    # Текущее сопротивление
        self.curr_inom = None  # Текущий ток
        self.curr_un = None    # Текущее напряжение
        self.curr_k  = None    # Текущий коэффициент
        self.curr_rating  = None   #Текущая номинальная или расчетная предельная кратность
        self.rating = None
        self.fRating = None
        self.u2 = None         # Напряжение для защитных обмоток
        self.i2 = None         # Ток для защитных обмоток

        self.coefR = 1   # Преобразователь ед. измер. сопротивления

        self.MinAmp = 0.5   # В перспективе взять из настроек
        self.isHand = True # Кнопка 'Start' нажимается ручками
        self.wasHand = True # Кнопка 'Start' была нажата ручками
        
        self.isWork = False 

        self.workAmp = None
        self.workVolt = None
        
        self.series = None   # Номер текущей серии
        self.ordernumber = None   # Номер текущего заказа
        self.serialnumber = None # Текущий заводской номер

        self.graphicsScene =  QGraphicsScene()
        self.graphicsScene.setSceneRect(0, 0, 1, 1)
        self.ui.graphicsView.setScene(self.graphicsScene)        
         
        self.pen = QtGui.QPen()        
        self.pen_2 = QtGui.QPen()        
        self.epsilon = 0.0000001
         
        self.points = None           
        self.oldPoints = None 
        oldPoints_ = None 

        self.sample = None
        self.corridors = None
        self.globalCorridors = None
        self.defectItem = False   # Наличие отклонения какого-либо параметра транса во время испытания

        self.oItem = None
        self.swDone = True    # Транс без дефектов, ставим галочку. False - наоборот 

        self.ui.checkBox_6.setVisible(False)
        self.ui.pushButton_4.setVisible(False)
        self.ui.lineEdit_2.setVisible(False)
#*****        self.ui.label_10.setVisible(False)
           
        self.ui.lineEdit.returnPressed.connect(self.returnPress)

        self.idPreStand = self.preStand()

        self.tread = MyThread()
        
        #ВРЕМЕННО
        self.tread.signal1.connect(self.on_signal1)

        # self.connect(self.tread, QtCore.SIGNAL("signal1"), self.on_signal1, QtCore.Qt.QueuedConnection)
        # self.connect(self.tread, QtCore.SIGNAL("signal2"), self.on_signal2, QtCore.Qt.QueuedConnection)
        # self.connect(self.tread, QtCore.SIGNAL("signal3"), self.on_signal3, QtCore.Qt.QueuedConnection)
        #
        #
        # self.connect(self.tread, QtCore.SIGNAL("treadsignal"), self.on_treadsignal, QtCore.Qt.QueuedConnection)
        # self.connect(self.tread, QtCore.SIGNAL("mysignal"), self.on_mysignal, QtCore.Qt.QueuedConnection)
        # self.connect(self.tread, QtCore.SIGNAL("mysignal2"), self.on_mysignal2, QtCore.Qt.QueuedConnection)
        # self.connect(self.tread, QtCore.SIGNAL("mysignal3"), self.on_mysignal3_, QtCore.Qt.QueuedConnection)

        self.ui.pushButton.setVisible(False)
        self.ui.pushButton_6.setVisible(False)
        self.ui.pushButton_6.setVisible(True)
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)        
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)        
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)  
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)  
        self.ui.lineEdit_3.textChanged.connect(self.change_lineEdit_3)
        
              
### 05.2019        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)        
        self.ui.checkBox.clicked.connect(self.checkBox_Click)
        self.ui.checkBox_2.clicked.connect(self.checkBox_2_Click)
        self.ui.checkBox_6.clicked.connect(self.checkBox_6_Click)
        self.ui.checkBox.setChecked(False)
        self.checkBox_Click()

        self.env = _env
        self.Devices = Devices(_env)
        self.setMeasureR(self.Devices.ui.comboBox.currentText())
        self.Devices_comboBox_currentText = self.Devices.ui.comboBox.currentText()        
        self.TestCoilReport = TestCoilReport(self.env)

# Списки виджетов
        self.nK = 3
        self.sK = [5, 10, 15]
        self.scheckBox = [self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5]
        self.slineEdit_K = [self.ui.lineEdit_K5, self.ui.lineEdit_K10, self.ui.lineEdit_K15]
        self.slineEdit_U = [self.ui.lineEdit_U5, self.ui.lineEdit_U10, self.ui.lineEdit_U15]
        self.slineEdit_I = [self.ui.lineEdit_I5, self.ui.lineEdit_I10, self.ui.lineEdit_I15]
        self.slineEdit_Pred = [self.ui.lineEdit_Pred5, self.ui.lineEdit_Pred10, self.ui.lineEdit_Pred15]
        self.slineEdit_Kor = [self.ui.lineEdit_Kor5, self.ui.lineEdit_Kor10, self.ui.lineEdit_Kor15]

#Центрирование виджетов
        for i in range(self.nK):
            self.ui.gridLayout_3.setAlignment(self.scheckBox[i],      QtCore.Qt.AlignCenter)
            self.ui.gridLayout_3.setAlignment(self.slineEdit_K[i],    QtCore.Qt.AlignCenter)
            self.ui.gridLayout_3.setAlignment(self.slineEdit_U[i],    QtCore.Qt.AlignCenter)
            self.ui.gridLayout_3.setAlignment(self.slineEdit_I[i],    QtCore.Qt.AlignCenter)
            self.ui.gridLayout_3.setAlignment(self.slineEdit_Pred[i], QtCore.Qt.AlignCenter)
            self.ui.gridLayout_3.setAlignment(self.slineEdit_Kor[i],  QtCore.Qt.AlignCenter)

        self.ui.checkBox.setVisible(socket.gethostname() == 'ws241' or socket.gethostname() == 'TAM' or socket.gethostname() == 'nc0001' or socket.gethostname() == 'DESKTOP-B6JA0B4')

        if _env.db.isOpen() == False:
            return
        
                
        
        if not self.TestBase(_env.db):
            return
        
        # print 'self.oMap789 = ', self.oMap
        if self.oMap == None:  #ВРЕМЕННО
            return
# #        msgBox(self, u"Проблемы считывания данных с приборов111  " + str(self.oMap.iMapID))
#         print 'self.oMap.iMapID = ', self.oMap.iMapID

        self.oItem = Item(self.env, None, self.oMap.iMapID, True)
        self.temperature = self.CalcTemperature(self.oMap.iMapID)
        # print 'temperature = ', self.temperature

        self.globalInfa = None



    def CalcTemperature(self, test_map):
        model.clear()
        strSQL = """
select temperature
from test_map t1, climat t2
where t1.climat = t2.id
and t1.id = :test_map
and t2.temperature is not null
"""
        self.query.prepare(strSQL)
        self.query.bindValue("test_map", test_map)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
        else:    
            model.setQuery(self.query)
        if model.rowCount() < 1:
            return None
        else:            
            return float(model.record(0).field('temperature').value())


    def on_treadsignal(self):
        global AV, yyy
        AV = self.ReadPort()
        # print 'AVAVAVAV=', AV
        #26.10.2018
        # ДЛЯ ЭМУЛЯЦИИ
        if self.ui.checkBox.isChecked():
            yyy += 0.005
            hs = self.ui.horizontalSlider.value()
            AV = [str(0.2 * hs * float(self.ui.lineEdit_18.text())),
                  str((math.sqrt(0.2 * hs) + yyy) * 0.9 * float(self.ui.lineEdit_19.text()))]
            time.sleep(0.01)
        #
        # print 'AVAVAVAVAVAVAVAV_____=', AV
        #

    def TransR(self, sw, R1, T1, T2):
        # Преобразование сопротиаления
        # sw = 1 - из температуры T1 в T2
        # sw = 2 - из температуры T2 в T1
        if T1 == None or T2 == None:
            return R1
        if sw == 1:
            return R1 * 255. / (255. - T2 + T1) 
        else:
            return R1 * (255. - T2 + T1) / 255. 


    def calcK(self, I, R, U, S):
        try:
            B1 = I
            B2 = R
            B3 = U
            B4 = S
                        
            B1 *= 1.        
            B2 *= 1.        
            B3 *= 1.        
            B4 *= 1.
                            
            B15 = B1 * B1
            B18 = abs(B4/B15)
            B11 = abs(B2 + B18 * 0.8)
            B16 = B11 * B11
              
            B12 = abs(B18 * 0.6)
            B17 = B12 * B12

            B13 = B16 + B17
            B14 = math.sqrt(B13)
            K = B3 / (B1 * B14)
        except Exception:
            K = None        
        return K

    def calcU(self, I, R, K, S):
        try:
            B1 = I
            B2 = R
            B3 = K
            B4 = S
                        
            B1 *= 1.        
            B2 *= 1.        
            B3 *= 1.        
            B4 *= 1.
                            
            B15 = B1 * B1
            B18 = abs(B4/B15)
            B11 = abs(B2 + B18 * 0.8)
            B16 = B11 * B11
              
            B12 = abs(B18 * 0.6)
            B17 = B12 * B12

            B13 = B16 + B17
            B14 = math.sqrt(B13)
            U = B3 * (B1 * B14)
        except Exception:
            U = None        
        return U


    def pushButton_6_Click(self):
        # print self.calcU(1, 44.451, 10, 30)
        # print self.calcU(1, 0.044451, 10, 30)
        # print self.calcU(1, 44.451, 10, 0)
        # print self.calcU(1, 44.451, 10, 1)
        # print self.calcU(1, 44.451, 10, 5)
        # print self.calcU(1, 44.451, 10, 10)
        # print self.calcU(1, 44.451, 10, 15)
        # print self.calcU(1, 44.451, 10, 20)
        #
        return
        # print round(0.216, 3)
        # print round(0.2160001, 3)
        #
        return
        
        # print self.calcU(5, 0.253, 15, 15)
        # print self.calcU(5, 0.253, 15, 10)
        # print self.calcU(5, 0.253, 15, 9.5)
        #
        #
        # print self.calcU(10, 0.553, 15, 15)
        # print self.calcU(15, 0.553, 15, 15)
        # print self.calcU(5, 0.166, 15, 10)
        #
        # print self.calcU(5, 0.253, 5, 15)
        # print self.calcU(5, 0.253, 10, 15)
        #
        # print self.calcU(5, 0.252, 15, 15)
        
        return


    def calcI(self, U, points):
        # Расчет тока путем пересечения напряжения в графике "points"
        try:
            if len(points) < 2:
                # print 'I0=None'
                return None
            for i in range(len(points) - 1):
                if abs(points[i][1] - points[i+1][1]) < self.epsilon:
                    continue
                if U >= points[i][1] and U <= points[i+1][1]:
                    I = (U - points[i][1]) * (points[i+1][0] - points[i][0]) / (points[i+1][1] - points[i][1]) + points[i][0]
                    # print 'I=',I
                    if I < 0:
                        I = 0
                    return I


            # 05.2019
            # Вычисление тока на линии продолжения графика
            for i in range(len(points) - 1):
                j = len(points) - 2 - i
                if abs(points[j][0] - points[j+1][0]) < self.epsilon or points[j+1][1] - points[j][1] < self.epsilon:
                    continue                
                I = (points[j+1][0] - points[j][0]) * (U - points[j][1]) / (points[j+1][1] - points[j][1]) + points[j][0]
                # print 'I=I=I=',I
                # print U, points[j][0], points[j+1][0], points[j][1], points[j+1][1]
                if I < 0:
                    I = 0
                return I                


            # Вычисление тока на отрезке между началом координат и первой точкой
            if U >= 0 and U <= points[0][1]:
                I = U * points[0][0] / points[0][1]
                # print 'I1=',I
                if I < 0:
                    I = 0
                return I
            else:
                # print 'I=None'
                return None    
        except Exception:
            # print 'I1=None'
            return None        

    def calcU_(self, I, points):
        # Расчет напряжения путем пересечения тока в графике "points"
        try:
            if len(points) < 2:
                return None
            for i in range(len(points) - 1):
                if abs(points[i][0] - points[i+1][0]) < self.epsilon:
                    continue                
                if I >= points[i][0] and I <= points[i+1][0]:
                    U = (I - points[i][0]) * (points[i+1][1] - points[i][1]) / (points[i+1][0] - points[i][0]) + points[i][1]
                    return U
            
            # 05.2019
            # Вычисление тока на линии продолжения графика
            for i in range(len(points) - 1):
                j = len(points) - 2 - i
                if abs(points[j][0] - points[j+1][0]) < self.epsilon or points[j+1][1] - points[j][1] < self.epsilon:
                    continue                
                U = (points[j+1][1] - points[j][1]) * (I - points[j][0]) / (points[j+1][0] - points[j][0]) + points[j][1]
                return U                
                
            # Вычисление тока на отрезке между началом координат и первой точкой
            if I >= 0 and I <= points[0][0]:
                U = I * points[0][1] / points[0][0]
                return U
            else:
                return None    
        except Exception:
            # print 'U1=None'
            return None        



    def roundKz(self, K):
        # Округление до кратности 5 в меньшую сторону
        # Пока с ошибкой roundKz(11) = 5, а должно быть 10
        if K < 5:
            return None
        k1 = round(5. * math.floor(K / 5))
        if k1 > 5 and K - k1 < 2:
            k1 -= 5
        return k1    


    def clear(self):
        self.ui.checkBox_3.setChecked(False) 
        self.ui.checkBox_4.setChecked(False) 
        self.ui.checkBox_5.setChecked(False) 
        self.ui.lineEdit.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_U5.clear()
        self.ui.lineEdit_U10.clear()
        self.ui.lineEdit_U15.clear()
        self.ui.lineEdit_I5.clear()
        self.ui.lineEdit_I10.clear()
        self.ui.lineEdit_I15.clear()
        self.ui.lineEdit_Pred5.clear()
        self.ui.lineEdit_Pred10.clear()
        self.ui.lineEdit_Pred15.clear()
        self.ui.lineEdit_Kor5.clear()
        self.ui.lineEdit_Kor10.clear()
        self.ui.lineEdit_Kor15.clear()
        self.ui.lineEdit_11.clear()
        self.ui.pushButton_3.setEnabled(False)        
        
        self.graphicsScene.clear()
        self.points = None        



    def code_type_test(self, idStand):
        self.idStand = idStand
        
        model.clear()
        
        strSQL = """
select test_type.code
from stand, test_type
where stand.test_type = test_type.id
and stand.id = :id
"""
        self.query.prepare(strSQL)
        self.query.bindValue("id", idStand)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
        else:    
            model.setQuery(self.query)
        if model.rowCount() < 1:
            self.codeTypeTest = None
        else:
            self.codeTypeTest = int(model.record(0).field('code').value())
        return self.codeTypeTest 


    def preStand(self):
        try:
            model.clear()
        
            strSQL = """
select stand.id
from stand, test_type
where stand.test_type = test_type.id
and test_type.code = 3
"""
            self.query.prepare(strSQL)
            if not self.query.exec_():
                raise Exception(self.query.lastError().text())
            else:    
                model.setQuery(self.query)
            if model.rowCount() < 1:
                return None
            else:
                return int(model.record(0).field('id').value())
        except Exception:
            return None
                        

    def item_change_row(self, idItem):
        self.defectItem = False


    def calcSeries(self, idItem):
        #Вычисляем номер серии
        strSQL = """
select t2.series, t2.serialnumber, t2.ordernumber
from item t1, serial_number t2
where t1.serial_number = t2.id
and t1.id = :item
--order by chektimestamp"""
        self.query_4.prepare(strSQL)
        self.query_4.bindValue(":item", self.idItemLast)
        if not self.query_4.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка определения серии", QMessageBox.Ok)
        else:    
            model_4.setQuery(self.query_4)
                
        if model_4.rowCount() > 0:
            self.series = model_4.record(0).field('series').value()
            self.ordernumber = model_4.record(0).field('ordernumber').value()
            self.serialnumber = int(model_4.record(0).field('serialnumber').value())
         

    def coil_change_row(self, idCoil, idItem):
        if idCoil == None:  # Чтобы не повторялось построение графика
            return
        self.idCoil = idCoil
        self.idItem = idItem

                
    def coil_after_change_row(self, idCoil, idItem, info):
        
        global oldPoints_    
        oldPoints_ = []
        
        #16.06.2019
        self.setMeasureR(self.Devices_comboBox_currentText)        
        self.info = info       
        # print "self.idCoilLast == None or idCoil == None=", self.idCoilLast, idCoil
        if self.idCoilLast == None or idCoil == None:  # Чтобы не повторялось построение графика
            self.idCoilLast = idCoil
            self.idItemLast = idItem
            return
        
        if self.VerificationForm.oTestCoil.isVisible() == False:  # Чтобы не повторялось построение графика
            return
          
        self.graphicsScene.clear()
        
        self.idCoilLast = idCoil
        self.idItemLast = idItem

        # Выясняем, есть ли заданный коэффициент
        self.rating2 = None
        model_2.clear()
        strSQL = """select rating from coil where id = :coil"""
        self.query_2.prepare(strSQL)
        self.query_2.bindValue(":coil", self.idCoilLast)
        if not self.query_2.exec_():
            raise Exception(self.query_2.lastError().text())
            return
        else:    
            model_2.setQuery(self.query_2)

        if model_2.rowCount() > 0:
            self.rating2 = model_2.record(0).field('rating').value()
        if self.rating2 == '':
            self.rating2 = None
            
        # Выясняем, есть ли номилальная кратность в таблице 'coil'            
        try:
            self.fRating2 = float(self.rating2)
            self.ui.lineEdit_3.setText(str(self.fRating2))
        except Exception:
            self.fRating2 = None                                           
            self.ui.lineEdit_3.clear()

        self.ui.pushButton_5.setEnabled(False)        

        
        if self.codeTypeTest == 3:
            pass
#            self.ui.label.setText(u'Сопротивление, Ом / коридор')
#            self.ui.label.setText(u'Сопротивление, ' + self.Devices.ui.comboBox.currentText() + u' / коридор')
            
            #self.Devices.ui.comboBox.currentText()
            
        if self.codeTypeTest == 4:
            self.ui.lineEdit_7.clear()
            model_2.clear()
            strSQL = """
select r from checking_2 where item in
(
select max(t1.id) 
from item as t1, test_map as t2, stand as t3, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t3.test_type = t5.id
--and t1.serial_number = 254304
--and t1.serial_number in (select serial_number from item where id = 801000)
and t1.serial_number in (select serial_number from item where id = :item)
and t5.code = 3
--and t1.istested = true
)
--and coil = 36555
and coil = :coil"""
            self.query_2.prepare(strSQL)
            self.query_2.bindValue(":item", self.idItemLast)
            self.query_2.bindValue(":coil", self.idCoilLast)
            if not self.query_2.exec_():
                raise Exception(self.query_2.lastError().text())
                return
            else:    
                model_2.setQuery(self.query_2)

            if model_2.rowCount() > 0:
                self.ui.lineEdit_7.setText(str(round(self.coefR * float(model_2.record(0).field('r').value()),3)))

        model_2.clear()
        strSQL = """
select t1.id, t1.r, t1.un, t1.inom, t1.u2, t1.i2, t1.k, t1.rating, t2.rating as rating2
from checking_2 t1, coil t2
where t1.stand = :stand
and t1.item = :item
and t1.coil = t2.id
and t1.coil = :coil
"""

        self.query_2.prepare(strSQL)
        self.query_2.bindValue(":stand", self.idStand)
        self.query_2.bindValue(":item", self.idItemLast)
        self.query_2.bindValue(":coil", self.idCoilLast)
        if not self.query_2.exec_():
            raise Exception(self.query_2.lastError().text())
            return
        else:    
            model_2.setQuery(self.query_2)

        if model_2.rowCount() < 1:
            self.ui.checkBox_6.setEnabled(False)
            self.curr_r  = None
            self.curr_un = None
            self.curr_inom  = None
            self.curr_k  = None
            self.curr_rating  = None
            
            self.ui.lineEdit.setText('')
            self.ui.lineEdit_6.setText('')
            
            self.checking_2 = None
        else:            
            self.ui.checkBox_6.setEnabled(True)
            self.curr_r  = self.coefR * float(model_2.record(0).field('r').value())
#            self.ui.lineEdit_6.setText(str(self.curr_r))            
#            self.ui.lineEdit.setText(str(self.TransR(2, self.curr_r, self.temperature, 20)))
            self.ui.lineEdit_6.setText(str(round(self.curr_r, 4)))            
            self.ui.lineEdit.setText(str(round(self.TransR(2, self.curr_r, self.temperature, 20), 4)))
            
            
            self.curr_un = float(model_2.record(0).field('un').value())
            self.curr_inom = float(model_2.record(0).field('inom').value())
            #5.05.2017
            self.u2 = float(model_2.record(0).field('u2').value())
            self.i2 = float(model_2.record(0).field('i2').value())
            
            self.curr_k  = float(model_2.record(0).field('k').value())
            self.curr_rating = model_2.record(0).field('rating').value()
          
            '''                         
            # Выясняем, есть ли номилальная кратность в таблице 'coil'            
            try:
                self.fRating2 = float(self.rating2)
            except Exception:
                self.fRating2 = None                                           
            '''
                                            
            self.checking_2 = int(model_2.record(0).field('id').value())
            
        vsbl = self.fRating2 == None        
        self.slineEdit_K[0].setText('5')
        self.sK[0] = 5
        self.nK = 3
        if not vsbl:
            self.slineEdit_K[0].setText(self.rating2)
            self.sK[0] = self.fRating2
            self.nK = 1                
        for i in range(len(self.sK) - 1):
            self.scheckBox[i + 1].setVisible(vsbl)
            self.slineEdit_K[i + 1].setVisible(vsbl)
            self.slineEdit_U[i + 1].setVisible(vsbl)
            self.slineEdit_I[i + 1].setVisible(vsbl)
            self.slineEdit_Pred[i + 1].setVisible(vsbl)
            self.slineEdit_Kor[i + 1].setVisible(vsbl)
            
        self.ui.checkBox_6.setChecked(False)
        self.checkBox_6_Click()
                                                        
        self.selectPoints(self.checking_2)
        self.selectOldPoints()
        
        self.VerificationForm.btnCoilClear.setEnabled(self.checking_2 != None or len(self.points) > 0)

        self.graphEmpty = (len(self.points) < 1) 
        
        self.calcSeries(idItem)
        self.sample = self.calcSample(self.series, self.ordernumber, self.idCoilLast)
        # print 'self.sample self.sample self.sample = ', self.sample
        
        self.ui.lineEdit_11.setText(str(self.sampleSerialnumber))
        
        
        for i in range(self.nK):
            self.scheckBox[i].setChecked(False)
        # print 'self.sample=', self.sample
        if self.sample != None: 
            for i in range(self.nK):
                # print 'self.sample[rating] , self.sK[i]=', self.sample['rating'], self.sK[i]
                self.scheckBox[i].setChecked(self.sample['rating'] == self.sK[i]) 
                        
        if self.serialnumber == self.sampleSerialnumber:
            self.ui.pushButton_3.setText(u'Удалить')
        else:    
            self.ui.pushButton_3.setText(u'Назначить')


        self.U5  = None
        self.U10 = None
        self.U15 = None

        for i in range(self.nK):
            self.slineEdit_K[i].setStyleSheet("background-color: white")
            self.slineEdit_U[i].setText("")
            self.slineEdit_I[i].setText("")
            self.slineEdit_Pred[i].setText("")
            self.slineEdit_Kor[i].setText("")

        
        classAccuracy = None    
        if str(self.info.ClassAccuracy).find('P') == -1:
            typeCoil = 1
        else:    
            typeCoil = 2
            if str(self.info.ClassAccuracy).find('10P') != -1:
                classAccuracy = 1
            else:    
                classAccuracy = 2
        
        # print 'self.curr_r, self.info.SecondCurrent, self.info.SecondLoad, self.points, typeCoil, classAccuracy=', self.curr_r, self.info.SecondCurrent, self.info.SecondLoad, self.points, typeCoil, classAccuracy
        self.solut = self.calcCoil(None, self.curr_r, self.info.SecondCurrent, self.info.SecondLoad, self.points, typeCoil, classAccuracy, self.sample)
        # print self.solut[0]
        # print self.solut[1]
        # print self.solut[2]
        # print self.solut[3]
        
        if str(self.info.ClassAccuracy).find('P') == -1:
            # Измерительная обмотка
            # print u'Измерительная обмотка'
            self.ui.label_7.setText(u'Ток намагн, A')
            self.ui.label_9.setText(u'Напряж намагн, V')
            self.ui.label_10.setText(u'Предел, V')
                        
            for i in range(self.nK):
                if self.solut[2][i] != None:
                    self.slineEdit_I[i].setText(str(round(self.solut[2][i], 2)))
                if self.solut[1][i] != None:
                    self.slineEdit_U[i].setText(str(round(self.solut[1][i], 2)))
                if self.solut[3][i] != None:
                    self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                if self.solut[2][i] != None and self.solut[3][i] != None:
                    self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                    if self.solut[2][i] > self.solut[3][i]:
                        self.slineEdit_K[i].setStyleSheet("background-color: red")
                
        else:        
            # Защитная обмотка
            # print u'Защитная обмотка'
            self.ui.label_7.setText(u'Напряж намагн, V')
            self.ui.label_9.setText(u'Ток намагн, A')
            self.ui.label_10.setText(u'Предел, A')


            for i in range(self.nK):
                if self.solut[1][i] != None:
                    self.slineEdit_I[i].setText(str(round(self.solut[1][i], 2)))
                if self.solut[2][i] != None:
                    self.slineEdit_U[i].setText(str(round(self.solut[2][i], 2)))
                if self.solut[3][i] != None:
                    self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                if self.solut[1][i] != None and self.solut[3][i] != None:
                    self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                    if self.solut[1][i] > self.solut[3][i]:
                        self.slineEdit_K[i].setStyleSheet("background-color: red")


        self.setColors(idItem, idCoil)
        self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.points, self.oldPoints, 1, self.solut)

        
    def selectPoints(self, checking_2):
        self.points = []
        strSQL = """
select a, v
from checking_2sp
where checking_2 = :checking_2
order by id"""
        self.query_4.prepare(strSQL)
        self.query_4.bindValue(":checking_2", checking_2)
        if not self.query_4.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        else:    
            model_4.setQuery(self.query_4)
                 
        for i in range(model_4.rowCount()):                                
            self.points += [[float(model_4.record(i).field('a').value()), float(model_4.record(i).field('v').value())]]

            
    def selectOldPoints(self):        
        self.oldPoints = []
            
            
    def resizeEvent(self, event):
        if self.points != None: 
            self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.points, self.oldPoints, 1, self.solut) 
        pass
            
                        
    def returnPress(self):
        try:
            if self.ui.lineEdit.text().trimmed() == '':
                self.curr_r = 0
            else:                    
#                self.curr_r  = float(self.ui.lineEdit.text())
#                 print 996856856
                if self.temperature == None:
                    self.temperature = self.CalcTemperature(self.oMap.iMapID)        
                self.curr_r  = self.TransR(1, float(self.ui.lineEdit.text()), self.temperature, 20)
#                self.ui.lineEdit_6.setText(str(self.curr_r))
                self.ui.lineEdit_6.setText(str(round(self.curr_r, 4)))




            accuracyR = self.Devices.data['accuracy']['r']

            if self.codeTypeTest == 4:
                swWarning = False
                try:
                    predR = float(self.ui.lineEdit_7.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина сопротивления предыдущего испытания не корректна', QMessageBox.Ok)
                    #16.06.2019
                    predR = 0
                    swWarning = True
                
                #16.06.2019
                if predR > self.epsilon:
                    if self.curr_r < predR * (1 - accuracyR / 100) or self.curr_r > predR * (1 + accuracyR / 100): 
                        QMessageBox.warning(self, u"Предупреждение",  u'Расхождение между величинами сопротивлений текущего\nи предыдущего испытаний превышает ' + str(accuracyR) + '%', QMessageBox.Ok)
                        swWarning = True
                if swWarning:
                    self.saveR()
                    self.btnStart.click()
                    return
                                    
        except Exception:
            QMessageBox.warning(self, u"Предупреждение",  u'Величина сопротивления: ' + self.ui.lineEdit.text() + u' не корректна', QMessageBox.Ok)
            return
               
        self.saveR()
        
        self.calcGlobal(self.oMap.iMapID, None, self.idStand, None, None, True)
        # print 'calcGlobal                     666666666666666666666666666666'
        rez = self.setColors(self.idItem, self.idCoil)
                
        if rez != '':
            self.btnStart.click()
            self.sound.play(self.env.config.snd_notify.point_error)
            QMessageBox.warning(self, u"Предупреждение",  rez, QMessageBox.Ok)
        else:    
            self.move_item_coil(False)
       
                        
                         
    def move_item_coil(self, isTested):
        if self.tvCoil.table.currentIndex().row() < self.tvCoil.get_row_count() - 1:
            self.tvCoil.table.selectRow(self.tvCoil.table.currentIndex().row() + 1)
        else:            
            if self.tvItem.table.currentIndex().row() < self.tvItem.get_row_count() - 1:                
                self.tvItem.table.selectRow(self.tvItem.table.currentIndex().row() + 1)
            else:    
                self.tvItem.table.selectRow(0)
                self.tvCoil.table.selectRow(0)
        self.tvItem.setEnabled(False)
        self.tvCoil.setEnabled(False)
                                         
                    
    def saveR(self):            
        if model_2.rowCount() < 1:
            self.query_9.prepare('INSERT INTO checking_2 (stand, item, coil, r) values (:stand, :item, :coil, :r)')            
            self.query_9.bindValue(":stand", self.idStand)
            self.query_9.bindValue(":item", self.idItemLast)
            self.query_9.bindValue(":coil", self.idCoilLast)
        else:
            if self.ui.lineEdit.text() == model_2.record(0).field('r').value():
                return  # Если значение не поменялось, не сохранять
                        
            id = int(model_2.record(0).field('id').value())
            self.query_9.prepare('UPDATE checking_2 SET r=:r WHERE id=:id')            
            self.query_9.bindValue(":id", id)
                
        if self.ui.lineEdit.text().trimmed() == '':
            self.query_9.bindValue(":r", None)
        else:                
            self.query_9.bindValue(":r", self.curr_r / self.coefR)
                                
                                
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка сохранения значения сопротивления в БД",
            QMessageBox.Ok)


    def save_calcData(self, checking_2):
#        QMessageBox.warning(None, u"r / self.coefR = ", "update 111 " + str(self.predel), QMessageBox.Ok)  ###TAM
        # Сохранение Un, In, K в таблице
        self.query_9.prepare('UPDATE checking_2 SET un=:un, un_=:un_, inom=:inom, k=:k, rating=:rating, su2=:su2, u2=:u2, i2=:i2, predel=:predel WHERE id=:id')            
        self.query_9.bindValue(":id", checking_2)        
        self.query_9.bindValue(":un", self.U)            
        self.query_9.bindValue(":un_", self.U)        
        self.query_9.bindValue(":inom", self.I)        
        self.query_9.bindValue(":k", self.K)        
        self.query_9.bindValue(":rating", self.K)  # Расчетная номинальная кратность
        self.query_9.bindValue(":u2", self.U)
        self.query_9.bindValue(":i2", self.I)
        self.query_9.bindValue(":su2", self.U)
        self.query_9.bindValue(":predel", self.predel)
                
        self.query_9.exec_()
        if self.query_9.lastError().isValid():
            stateWork = PAUSE
            self.tread.quit()
            return


    def save_points(self, points):
        self.coil_clear_()
                            
        for i in range(len(points)):
            self.query_9.prepare('INSERT INTO checking_2sp (checking_2, chektimestamp, a, v) values (:checking_2, CURRENT_TIMESTAMP, :a, :v)')
            self.query_9.bindValue(":checking_2", self.checking_2)
            self.query_9.bindValue(":a", points[i][0])
            self.query_9.bindValue(":v", points[i][1])
                                    
            self.query_9.exec_()
            if self.query_9.lastError().isValid():
                # print self.query_9.lastError().text()
                return

        model.clear()
        
        strSQL = """
select distinct coil from checking_2 t1, checking_2sp t2
where t1.id = t2.checking_2 and t1.item=:item
"""
        self.query.prepare(strSQL)
        self.query.bindValue("item", self.idItem)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
        else:    
            model.setQuery(self.query)
        if model.rowCount() < self.tvCoil.get_row_count():
            pass
            # print u'МЕНЬШЕ'
        else:
            self.oItem = Item(self.env, None, self.oMap.iMapID, True)
            
            if not self.defectItem: 
                self.oItem.set_done(self.idItem)
                self.oMap.mapRefresh.emit()


    ''' 27.04.2021
    def calcSample(self, series, ordernumber, coil):
        # Определение образца (первого испытанного транса) из указанной серии
        print 'series, ordernumber, coil = ', series, ordernumber, coil
        self.sampleSerialnumber = None
        self.ui.pushButton_3.setEnabled(False)                        

        model.clear()
        strSQL = """
select min(t1.id) as id
from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and series = :series
--19.04
and ordernumber = :ordernumber
and coil = :coil
"""

        self.query.prepare(strSQL)
        self.query.bindValue(":series", series)
        self.query.bindValue(":ordernumber", ordernumber)
        self.query.bindValue(":coil", coil)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            id = -1
        else:
            id =  int(model.record(0).field('id').value().toString())

        model.clear()
        strSQL = """
select max(t1.id) as id
from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and series = :series
and ordernumber = :ordernumber

and coil = :coil
--and t1.id <= :checking_2
and sample
"""

        self.query.prepare(strSQL)
        self.query.bindValue(":series", series)
        self.query.bindValue(":ordernumber", ordernumber)
        self.query.bindValue(":coil", coil)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            id1 = -1
        else:
            id1 =  int(model.record(0).field('id').value().toString())

        id = max(id, id1)
        if id == -1:
            return None

        model.clear()
        strSQL = """
select serialnumber from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and t1.id = :id
"""
        self.query.prepare(strSQL)
        self.query.bindValue(":id", id)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            return None
        else:
            self.sampleSerialnumber =  int(model.record(0).field('serialnumber').value().toString())
            
            if self.sampleSerialnumber == 0:
                return None

            
            model.clear()
            strSQL = "select * from checking_2 where id = :id"
            self.query.prepare(strSQL)
            self.query.bindValue(":id", id)
            if not self.query.exec_():
                raise Exception(self.query.lastError().text())
                return None
            else:
                model.setQuery(self.query)            
            
            if model.rowCount() < 1:
                return None
            else:
                r      = self.coefR * float(model.record(0).field('r').value().toString())
                k      =  float(model.record(0).field('k').value().toString())
                rating =  float(model.record(0).field('rating').value().toString())
                un     = float(model.record(0).field('un').value().toString())
                inom   = float(model.record(0).field('inom').value().toString())
                un2     = float(model.record(0).field('u2').value().toString())
                inom2   = float(model.record(0).field('i2').value().toString())
                self.ui.pushButton_3.setEnabled(True)                        
                return {'id':  id, 'r':  r,  'k':  k, 'rating': rating, 'un': un, 'in': inom, 'un2': un2, 'in2': inom2}
        pass
'''

    def calcSample(self, series, ordernumber, coil):
        # Определение образца (первого испытанного транса) из указанной серии
        # print 'series, ordernumber, coil = ', series, ordernumber, coil
        self.sampleSerialnumber = None
        self.ui.pushButton_3.setEnabled(False)                        

        '''
        model.clear()
        strSQL = """
select min(t1.id) as id
from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and series = :series
--19.04
and ordernumber = :ordernumber
and coil = :coil
"""

        self.query.prepare(strSQL)
        self.query.bindValue(":series", series)
        self.query.bindValue(":ordernumber", ordernumber)
        self.query.bindValue(":coil", coil)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            id = -1
        else:
            id =  int(model.record(0).field('id').value().toString())

        model.clear()
        strSQL = """
select max(t1.id) as id
from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and series = :series
and ordernumber = :ordernumber

and coil = :coil
--and t1.id <= :checking_2
and sample
"""

        self.query.prepare(strSQL)
        self.query.bindValue(":series", series)
        self.query.bindValue(":ordernumber", ordernumber)
        self.query.bindValue(":coil", coil)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            id1 = -1
        else:
            id1 =  int(model.record(0).field('id').value().toString())

        id = max(id, id1)
        if id == -1:
            return None

        model.clear()
        strSQL = """
select serialnumber from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and t1.id = :id
"""
        self.query.prepare(strSQL)
        self.query.bindValue(":id", id)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return None
        else:
            model.setQuery(self.query)
'''
        
        if len(self.globalReport) < 1:
            return None
        
        
#    def calcSample(self, series, ordernumber, coil):
        
        
        
        
        
#        if model.rowCount() < 1:
#            return None
        
        
        else:
#            self.sampleSerialnumber =  int(model.record(0).field('serialnumber').value().toString())
            
#            if self.sampleSerialnumber == 0:
#                return None
            self.sampleSerialnumber = 0

            for i in range(len(self.globalReport)):
                if self.globalReport[i][1] == series and self.globalReport[i][2] == ordernumber and self.globalReport[i][19] == coil:
                    id = self.globalReport[i][0]
#                    msgBox(self, str(id))
                    self.sampleSerialnumber = self.globalReport[i][3]
                    break

            if self.sampleSerialnumber == 0:
                return None
            
            model.clear()
            strSQL = "select * from checking_2 where id = :id"
            self.query.prepare(strSQL)
            self.query.bindValue(":id", id)
            if not self.query.exec_():
                raise Exception(self.query.lastError().text())
                return None
            else:
                model.setQuery(self.query)            
            
            if model.rowCount() < 1:
                return None
            else:
                r      = self.coefR * float(model.record(0).field('r').value())
                k      =  float(model.record(0).field('k').value())
                rating =  float(model.record(0).field('rating').value())
                un     = float(model.record(0).field('un').value())
                inom   = float(model.record(0).field('inom').value())
                un2     = float(model.record(0).field('u2').value())
                inom2   = float(model.record(0).field('i2').value())
                self.ui.pushButton_3.setEnabled(True)                        
                return {'id':  id, 'r':  r,  'k':  k, 'rating': rating, 'un': un, 'in': inom, 'un2': un2, 'in2': inom2}
        pass



#        self.globalReport += [[checking_2, series, ordernumber, serialnumber, coilname, round(r, 3), min_r, max_r, round(un, 2), min_un, max_un, round(inom, 2), pred, round(k, 2), createdatetime, idMap, idClass, id4, round(inom2, 2)]]


    def calcGlobal(self, iMapID_, serial_number_, idStand, _accuracyR, _accuracyI, LastTest):

#        msgBox(self, u"Проблемы считывания данных с приборов222  " + str(iMapID_))
        
        
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t1 = datetime.datetime.now()
#        self.f.write('CG_01_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '\n')
#        self.f.close()

        # Если точности по сопротивлению и току равны None,
        # то их берем из словаря "self.Devices.data" иначе из параметров
        accuracyR = _accuracyR
        accuracyI = _accuracyI
        print(48908796757546,self.Devices.data)
        try:
            if accuracyR == None:
                accuracyR = self.Devices.data['accuracy']['r']
            if accuracyI == None:
                accuracyI = self.Devices.data['accuracy']['a']
        except Exception:
            QMessageBox.warning(self, u"Предупреждение",  u'Файл "devices.json" не корректен либо отсутствует. Войдите в настройку приборов!', QMessageBox.Ok)
            return
                
        iMapID = iMapID_
        serial_number = serial_number_
        if iMapID == None and serial_number == None:
            return False

        self.temperature = None
        if self.temperature == None:
            self.temperature = self.CalcTemperature(iMapID)        
        if self.temperature == None:
            self.ui.label.setText(u't = 20°')
            self.ui.label.setStyleSheet("color: red")            
        else:
            self.ui.label.setText(u't = ' + str(self.temperature) + u'°')
            self.ui.label.setStyleSheet("color: blue")            

            
            
            
        
        # print 'serial_number serial_number serial_number === ', serial_number

        model.clear()
        
#26.04.2021        
        if serial_number != None:
            strSQL = """
select t1.id as id_item, t3.id as id_coil, series, ordernumber,        t4.fullname
from item t1, serial_number t2, coil t3          , transformer t4
where t1.serial_number = t2.id
and t2.transformer = t3.transformer
and t2.id = :serial_number
and t3.transformer = t4.id
order by t1.id, t3.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":serial_number", serial_number)
        else:    
            strSQL = """
select t1.id as id_item, t3.id as id_coil, series, ordernumber,        t4.fullname
from item t1, serial_number t2, coil t3          , transformer t4
where t1.serial_number = t2.id
and t2.transformer = t3.transformer
and test_map = :test_map
and t3.transformer = t4.id
order by t1.id, t3.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":test_map", iMapID)
        
        
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return False
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            return False

        self.globalInfa = []
        self.globalItem = []
        item = -1
        for i in range(model.rowCount()):
            idItem = int(model.record(i).field('id_item').value())
            idCoil = int(model.record(i).field('id_coil').value())
                        
            series = model.record(i).field('series').value()
            ordernumber = model.record(i).field('ordernumber')
            #5.05.2017
            self.globalInfa += [[idItem, idCoil, series, ordernumber, None, None, None, None, None, None, None]]
            if item != idItem:
                self.globalItem += [[idItem, True]]
                item = idItem
        
        series = '('
        model.clear()
        
        
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t2 = datetime.datetime.now()
#        self.f.write('CG_02_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t2 - t1) +  '\n')        
#        self.f.close()
        
        
#26.04.2021        
        if serial_number != None:
            strSQL = """
select distinct series from item t1, serial_number t2
where t2.id = :serial_number
and t1.serial_number = t2.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":serial_number", serial_number)
        else:    
            strSQL = """
select distinct series from item t1, serial_number t2
where t1.test_map = :test_map
and t1.serial_number = t2.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":test_map", iMapID)
                
        
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return False
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            return False

        for i in range(model.rowCount()):
            s = ','
            if i == model.rowCount() - 1:
                s = ')'                                
            series += "'" + model.record(i).field('series').value() + "'" + s




        ordernumber = '('
        model.clear()
        
        
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t2_1 = datetime.datetime.now()
#        self.f.write('CG_02_01 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t2_1 - t1) +  '\n')        
#        self.f.close()
        
        
#30.01.2023        
        if serial_number != None:
            strSQL = """
select distinct ordernumber from item t1, serial_number t2
where t2.id = :serial_number
and t1.serial_number = t2.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":serial_number", serial_number)
        else:    
            strSQL = """
select distinct ordernumber from item t1, serial_number t2
where t1.test_map = :test_map
and t1.serial_number = t2.id
"""
            self.query.prepare(strSQL)
            self.query.bindValue(":test_map", iMapID)
                
        
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return False
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
            return False

        for i in range(model.rowCount()):
            s = ','
            if i == model.rowCount() - 1:
                s = ')'                                
            ordernumber += "'" + model.record(i).field('ordernumber').value() + "'" + s

        #
        # print 'series series series=', series, 'ordernumber ordernumber ordernumber=', ordernumber, 'iMapID = ', iMapID
        # print 'self.globalInfa=', self.globalInfa
        # print 'self.idItemLast=', self.idItemLast
        
        # Строку coils_ формируем для ускорения последущего запроса
        coils_ = '('
        for i in range(len(self.globalInfa)):
            if self.globalInfa[i][0] == self.idItemLast:
                coils_ += str(self.globalInfa[i][1]) + ','
        coils_ = coils_[0 : len(coils_) - 1] + ')'
        # print 'coils_=', coils_, len(coils_)
        
        
        model.clear()
        
        
        
        
        
        
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t3 = datetime.datetime.now()
#        self.f.write('CG_03_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t3 - t2_1) +  '\n')        
#        self.f.close()
        
        
        
# Старый запрос        
        strSQL = u"""
select t1.id, t1.test_map, series, ordernumber, serialnumber, item, coil, coilnumber, tap, 
r, un, un_, inom, i2, su2, u2, t4.k, t4.rating, t3.rating as rating2, predel,
t5.createdatetime, t4.id as checking_2, t1.test_map, t1.defect, 
t3.classaccuracy, t3.secondcurrent, t3.secondload,"""
        if LastTest:
            strSQL += """t4_.id as id4"""
        else:
            strSQL += """0 as id4"""

        strSQL += """
from item t1, serial_number t2, coil t3,"""

        if LastTest:
            if coils_ == ')':
                strSQL += """
checking_2 t4 LEFT OUTER JOIN
(select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + """
group by serial_number, coil) t4_
ON (t4.id = t4_.id),"""
            else:
                strSQL += """
checking_2 t4 LEFT OUTER JOIN 
(select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where coil in """ + coils_ + """ and t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + """
group by serial_number, coil) t4_
ON (t4.id = t4_.id),"""
        else:
            strSQL += """checking_2 t4,"""

        strSQL += """
test_map t5, stand t6, test_type t7
where  t2.series in """ + series + """
and t1.serial_number = t2.id
and t2.transformer = t3.transformer
and t1.id = t4.item
and t3.id = t4.coil 
and t1.test_map = t5.id
and t4.stand = t6.id
and t6.test_type = t7.id
and t7.code = """ + str(self.codeTypeTest) + """
order by series, ordernumber, coil, sample, t4.id
"""

# Старый запрос        

# Новый запрос        
        strSQL = u"""
select t1.id, t1.test_map, series, ordernumber, serialnumber, item, coil, coilnumber, tap, 
r, un, un_, inom, i2, su2, u2, t4.k, t4.rating, t3.rating as rating2, predel,
t5.createdatetime, t4.id as checking_2, t1.test_map, t1.defect, 
t3.classaccuracy, t3.secondcurrent, t3.secondload,"""
        if LastTest:
            strSQL += u"""t4.id as id4
"""
        else:
            strSQL += u"""0 as id4
"""
        strSQL += u"""from item t1, serial_number t2, coil t3, checking_2 t4,
"""
        strSQL += u"""
test_map t5, stand t6, test_type t7
where  t2.series in """ + series + u"""
and t2.ordernumber in """ + ordernumber + u"""
and t1.serial_number = t2.id
and t2.transformer = t3.transformer
and t1.id = t4.item
and t3.id = t4.coil 
and t1.test_map = t5.id
and t4.stand = t6.id
and t6.test_type = t7.id
and t7.code = """ + str(self.codeTypeTest) + u"""
order by series, ordernumber, coil, sample, t4.id
"""
# Новый запрос        

#        QMessageBox.warning(None, u"Предупреждение", u"1", QMessageBox.Ok)
        
        self.globalCorridors = []
        self.globalReport = []
        
        # print 'strSQL=',strSQL
        self.query.prepare(strSQL)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
            return False
        else:
            model.setQuery(self.query)

        if model.rowCount() < 1:
#            self.oMap.mapRefresh.emit()
            return False
#        QMessageBox.warning(None, u"Предупреждение", u"2", QMessageBox.Ok)



#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t4 = datetime.datetime.now()
#        self.f.write('CG_04_01 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t4 - t3) +  '\n')        
#        self.f.close()
        
        
        
###################################################
#   Вычисление минимального id
        MaxId = 999999999999
        for i in range(model.rowCount()):
            if MaxId > int(model.record(i).field('id4').value()):
                MaxId = int(model.record(i).field('id4').value())

#   Вспоиогательный запрос
        if LastTest:
            model_.clear()
            model__.clear()
            if serial_number == None:
# сТАРЫЙ ВАРИАНТ                
                strSQL = u"""
select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u""" and t2.id >= """ + str(MaxId) + u"""
and serial_number in
(
select id from serial_number
where (ordernumber, series) in
(
select ordernumber, series from item t1, serial_number t2
where test_map = """ + str(iMapID) + u"""
and t1.serial_number = t2.id
)    
)    
group by t1.id, coil
having max(t2.id) >= """ + str(MaxId)
            else:
                strSQL = u"""
select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where coil in
(
select t1.id from coil t1, serial_number t2
where t1.transformer = t2.transformer
and t2.id = """ + str(serial_number) + u"""
)
and t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u"""
group by serial_number, coil
having max(t2.id) >= """ + str(MaxId)
# сТАРЫЙ ВАРИАНТ                




            if serial_number == None:
                strSQL = u"""
select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u""" and t2.id >= """ + str(MaxId) + u"""
and serial_number in
(
select id from serial_number
where (ordernumber, series) in
(
select ordernumber, series from item t1, serial_number t2
where test_map = """ + str(iMapID) + u"""
and t1.serial_number = t2.id
)    
)    
group by t1.id, coil
having max(t2.id) >= """ + str(MaxId) + u"""
order by max(t2.id)
"""

                strSQL1 = u"""
select t2.id from item t1, checking_2 t2, stand t6, test_type t7
where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u""" and t2.id >= """ + str(MaxId) + u"""
and serial_number in
(
select id from serial_number
where (ordernumber, series) in
(
select ordernumber, series from item t1, serial_number t2
where test_map = """ + str(iMapID) + u"""
and t1.serial_number = t2.id
)    
)    
and t2.id >= """ + str(MaxId) + u"""
order by t2.id
"""
            else:
                strSQL = u"""
select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where coil in
(
select t1.id from coil t1, serial_number t2
where t1.transformer = t2.transformer
and t2.id = """ + str(serial_number) + u"""
)
and t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u"""
group by serial_number, coil
having max(t2.id) >= """ + str(MaxId) + u"""
order by max(t2.id)
"""
                strSQL1 = u"""
select t2.id from item t1, checking_2 t2, stand t6, test_type t7
where coil in
(
select t1.id from coil t1, serial_number t2
where t1.transformer = t2.transformer
and t2.id = """ + str(serial_number) + u"""
)
and t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id and t7.code = """ + str(self.codeTypeTest) + u"""
and t2.id >= """ + str(MaxId) + u"""
order by t2.id
"""


#   Вспоиогательный запрос


            #
            # print 'strSQL=',strSQL
            self.query.prepare(strSQL)
            if not self.query.exec_():
                raise Exception(self.query.lastError().text())
                return False
            else:
                model_.setQuery(self.query)

            # print 'strSQL1=',strSQL1
            self.query.prepare(strSQL1)
            if not self.query.exec_():
                raise Exception(self.query.lastError().text())
                return False
            else:
                model__.setQuery(self.query)

#        QMessageBox.warning(None, u"Предупреждение", u"3  model_.rowCount() = " + str(model_.rowCount()), QMessageBox.Ok)
#        QMessageBox.warning(None, u"Предупреждение", u"4  model_.rowCount() = " + str(model__.rowCount()), QMessageBox.Ok)



#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t5 = datetime.datetime.now()
#        self.f.write('CG_05_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t5 - t4) +  '\n')        
#        self.f.close()




        
#        self.globalCorridors = []
#        self.globalReport = []
        series_ = ''
        ordernumber_ = ''
        coil_ = -1

        self.lastes = []

        j = 0
        for i in range(model__.rowCount()):
#            QMessageBox.warning(None, u"Предупреждение", u"i, j = " + str(i) + '  ' +  str(j) + '  ' +  model__.record(i).field('id').value().toString() + '   ' + model_.record(j).field('id').value().toString(), QMessageBox.Ok)
            model__.record(i).field('id').value()
            if int(model__.record(i).field('id').value()) < int(model_.record(j).field('id').value()):
                self.lastes += [int(model__.record(i).field('id').value())]
                continue
            else:
                j += 1
                continue

        # print 'self.lastes = ', self.lastes

#        QMessageBox.warning(None, u"Предупреждение", u"4444444444  model.rowCount() = " + str(model.rowCount()), QMessageBox.Ok)
                        
        for i in range(model.rowCount()):
            idMap          = int(model.record(i).field('test_map').value())
            checking_2     = int(model.record(i).field('checking_2').value())
            serialnumber   = int(model.record(i).field('serialnumber').value())
            series         = model.record(i).field('series').value()
            ordernumber   = model.record(i).field('ordernumber').value()
            item           = int(model.record(i).field('item').value())
            coil           = int(model.record(i).field('coil').value())
            coilnumber     = int(model.record(i).field('coilnumber').value())
            tap            = int(model.record(i).field('tap').value())
            coilname       = str(coilnumber) + u'И1-' + str(coilnumber) + u'И' + str(tap)


            createdatetime = str(model.record(i).field('createdatetime').value().toString("dd.MM.yy"))
            r              = float(model.record(i).field('r').value())
            inom           = float(model.record(i).field('inom').value())
            un             = float(model.record(i).field('un').value())
            un_            = float(model.record(i).field('un_').value())
            inom2          = float(model.record(i).field('i2').value())
            sun2           = float(model.record(i).field('su2').value())
            un2            = float(model.record(i).field('u2').value())
            
            k              = float(model.record(i).field('k').value())
            rating         = float(model.record(i).field('rating').value())
            rating_2       = model.record(i).field('rating2').value()
            
            # 22.07.2019
            pred           = float(model.record(i).field('predel').value())
            pred = round(pred, 2)
                      
            defect         = int(model.record(i).field('defect').value())
            id4            = int(model.record(i).field('id4').value())
            
            
            
            
            
#26.04.2021 ????????????????        
#            if LastTest and id4 == 0:
#                    continue
            '''
            sw = False
            if LastTest:
                for j in range(model_.rowCount()):
                    if int(model_.record(j).field('id').value().toString()) == id4:
                        sw = True
            if LastTest and sw == False:
                continue    
'''


            sw = False
            for j in range(len(self.lastes)):
                if self.lastes[j] == id4:
                    sw = True
            if LastTest and sw:
                continue    
                       
            
            # Выясняем, есть ли номилальная кратность в таблице 'coil'            
            try:
                fRating2 = float(rating2)
            except Exception:
                fRating2 = None                                           

            if fRating2 != None and fRating2 > self.epsilon:
                rating = fRating2
                
            classaccuracy  = str(model.record(i).field('classaccuracy').value())
            if str(classaccuracy).find('P') == -1:
                idClass = 1  # измерительная
            else:    
                idClass = 2  # защитная

            secondcurrent  = float(model.record(i).field('secondcurrent').value())
            secondload  = float(model.record(i).field('secondload').value())
                        
            if idMap == iMapID:
                for j in range(len(self.globalInfa)):
                    if self.globalInfa[j][0] == item and self.globalInfa[j][1] == coil:            
                        self.globalInfa[j][4] = r #19.04
                        self.globalInfa[j][5] = inom #19.04
                        self.globalInfa[j][6] = k #19.04
                        self.globalInfa[j][7] = rating #19.04
                        self.globalInfa[j][8] = idClass #19.04
                        self.globalInfa[j][9] = inom2  #5.05.2017
                        self.globalInfa[j][10] = un  #01.19
                        
            if series_ != series or ordernumber_ != ordernumber or coil_ != coil:
#########################################                if series_ != '':
                print(3454375689678543645768)
                if coil_ != -1:                    
                    self.globalCorridors += [[series_, ordernumber_, coil_, min_r, max_r, min_in, max_in, min_in2, max_in2, min_un, max_un]]
                # Образцовая катушка
                series_ = series
                ordernumber_ = ordernumber
                coil_  = coil
                
                if r > self.epsilon and defect == 0:
                    accur_r = r * accuracyR / 100
                    min_r  = r - accur_r
                    max_r  = r + accur_r
                    #print '111 r, accur_r, min_r, max_r = ', r, accur_r, min_r, max_r
                else:
                    min_r  = None
                    max_r  = None
                
                if inom > self.epsilon and defect == 0:
                    accur_in = inom * accuracyI / 100
                    min_in  = inom - accur_in
                    max_in  = inom + accur_in
                else:
                    min_in = None
                    max_in = None
                    
                if inom2 > self.epsilon and defect == 0:
                    accur_in2 = inom2 * accuracyI / 100
                    min_in2  = inom2 - accur_in2
                    max_in2  = inom2 + accur_in2
                else:
                    min_in2 = None
                    max_in2 = None
                    
                #01.2019
                if un > self.epsilon and defect == 0:
                    accur_un = un * accuracyI / 100
                    min_un  = un - accur_un
                    max_un  = un + accur_un
                else:
                    min_un = None
                    max_un = None
            else:
                if r > self.epsilon and defect == 0:
                    if min_r == None:
                        accur_r = r * accuracyR / 100
                        min_r  = r - accur_r
                        max_r  = r + accur_r
                        #print '222 r, accur_r, min_r, max_r = ', r, accur_r, min_r, max_r
                    else:    
                        if r >= min_r - self.epsilon and r <= max_r + self.epsilon:
                           # accur_r = r * accuracyR / 100  #???????????????????????????????
                            min_r = max(min_r, r - accur_r)  
                            max_r = min(max_r, r + accur_r)                    
                            #print '333 r, accur_r, min_r, max_r = ', r, accur_r, min_r, max_r
                    
                if inom > self.epsilon and defect == 0:
                    if min_in == None:
                        accur_in = inom * accuracyI / 100
                        min_in  = inom - accur_in
                        max_in  = inom + accur_in
                    else:    
                        if inom >= min_in - self.epsilon and inom <= max_in + self.epsilon:
                            min_in = max(min_in, inom - accur_in)  
                            max_in = min(max_in, inom + accur_in)                    

                if inom2 > self.epsilon and defect == 0:
                    if min_in2 == None:
                        accur_in2 = inom2 * accuracyI / 100
                        min_in2  = inom2 - accur_in2
                        max_in2  = inom2 + accur_in2
                    else:    
                        if inom2 >= min_in2 - self.epsilon and inom2 <= max_in2 + self.epsilon:
                            min_in2 = max(min_in2, inom2 - accur_in2)  
                            max_in2 = min(max_in2, inom2 + accur_in2)                    
#01.2019
                if un > self.epsilon and defect == 0:
                    if min_un == None:
                        accur_un = un * accuracyI / 100
                        min_un  = un - accur_in2
                        max_un  = un + accur_in2
                    else:    
                        if un >= min_un - self.epsilon and un <= max_un + self.epsilon:
                            min_un = max(min_un, un - accur_un)  
                            max_un = min(max_un, un + accur_un)                    

            
            if min_r != None:
                min_r = round(min_r, 3)
            if max_r != None:
                max_r = round(max_r, 3)
                
            if min_in != None:
                min_in = round(min_in, 2)
            if max_in != None:
                max_in = round(max_in, 2)

            #5.05.2017
            if min_in2 != None:
                min_in2 = round(min_in2, 2)
            if max_in2 != None:
                max_in2 = round(max_in2, 2)
#01.2019
            if min_un != None:
                min_un = round(min_un, 2)
            if max_un != None:
                max_un = round(max_un, 2)
                
            self.globalReport += [[checking_2, series, ordernumber, serialnumber, coilname, round(r, 3), min_r, max_r, round(un, 2), min_un, max_un, round(inom, 2), pred, round(k, 2), createdatetime, idMap, idClass, id4, round(inom2, 2), coil]]
            
        self.globalCorridors += [[series, ordernumber, coil, min_r, max_r, min_in, max_in, min_in2, max_in2, min_un, max_un]]
        
#        QMessageBox.warning(None, u"Предупреждение", u"5  len(self.globalReport) = " + str(len(self.globalReport)), QMessageBox.Ok)
        
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t6 = datetime.datetime.now()
#        self.f.write('CG_06_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t6 - t5) +  '\n')        
#        self.f.close()

        
        '''
        print 'self.globalCorridors = ', len(self.globalCorridors), self.globalCorridors
        for i in range(len(self.globalCorridors)):
            print self.globalCorridors[i]
        print    
        print 'self.globalReport = ', len(self.globalReport), self.globalReport
        for i in range(len(self.globalReport)):
            print self.globalReport[i]
        '''    
            
        if serial_number != None:  # Эта ситуация имеет место при печати отчета
            return True
                        
        for i in range(len(self.globalItem)):
            for j in range(len(self.globalInfa)):
                if self.globalInfa[j][0] == self.globalItem[i][0]:
                    if self.globalInfa[j][4] == None: #19.04
                        self.globalItem[i][1] = False
                    else:
                        for k in range(len(self.globalCorridors)):
                            if self.globalInfa[j][2] == self.globalCorridors[k][0] and \
                               self.globalInfa[j][3] == self.globalCorridors[k][1] and \
                               self.globalInfa[j][1] == self.globalCorridors[k][2]:
                                if self.globalInfa[j][4] < self.epsilon or \
                                   self.globalInfa[j][5] < self.epsilon or \
                                   self.globalInfa[j][4] < self.globalCorridors[k][3] or \
                                   self.globalInfa[j][4] > self.globalCorridors[k][4] or \
                                   self.globalInfa[j][5] < self.globalCorridors[k][5] or \
                                   self.globalInfa[j][5] > self.globalCorridors[k][6]:
                                    self.globalItem[i][1] = False

            self.oItem.changeItem.emit(self.globalItem[i][0])
        self.oMap.mapRefresh.emit()
#19.01.2023        
#        self.f = open('WPT.log', 'a')
#        t7 = datetime.datetime.now()
#        self.f.write('CG_07_00 ' + str(iMapID_) + ' ' + str(self.idItemLast) + ' ' + str(datetime.datetime.now()) + '   ' + str(t7 - t6) +  '\n')        
#        self.f.close()


    def setColors(self, idItem, idCoil):
        if self.globalInfa == None:
            return
  # 23.11.2016  закоментировал чтобы коридоры появились при работе со сканером штрихкодов
      #  if self.isVisible() == False:
      #      return None
        self.ui.lineEdit.setStyleSheet("background-color: white")
        for i in range(self.nK):
            self.slineEdit_Kor[i].setStyleSheet("background-color: white")

        r    = None
        minR = None
        maxR = None
        inom = None
        minI = None
        maxI = None
        minI2 = None
        maxI2 = None
        minU = None
        maxU = None        
        series = None
        ordernumber = None #19.04
        self.corridors = None
        
        for i in range(len(self.globalInfa)):
            if self.globalInfa[i][0] == idItem and self.globalInfa[i][1] == idCoil:
                series = self.globalInfa[i][2]
                ordernumber = self.globalInfa[i][3] #19.04
                r      = self.globalInfa[i][4] #19.04
                inom   = self.globalInfa[i][5] #19.04
                k      = self.globalInfa[i][6] #19.04
                rating = self.globalInfa[i][7] #19.04
                p      = self.globalInfa[i][8] #19.04
                inom2  = self.globalInfa[i][9] #5.05.2017
                un     = self.globalInfa[i][10] #01.19
                break
        
        rez = ''
        
#5.12.2018
        if series != None and self.globalCorridors != None:   
            for i in range(len(self.globalCorridors)):
                if self.globalCorridors[i][0] == series and self.globalCorridors[i][1] == ordernumber and self.globalCorridors[i][2] == idCoil:
                    minR = self.globalCorridors[i][3]
                    maxR = self.globalCorridors[i][4]
                    minI = self.globalCorridors[i][5]
                    maxI = self.globalCorridors[i][6]
                    minI2 = self.globalCorridors[i][7]
                    maxI2 = self.globalCorridors[i][8]                    
                    minU = self.globalCorridors[i][9]
                    maxU = self.globalCorridors[i][10]                    
                    break

            if self.codeTypeTest == 3:  #05.2019
                                
                if minR != None and maxR != None:
                    self.ui.lineEdit_7.setText(str(round(self.coefR * minR,3)) + ' - ' + str(self.coefR * round(maxR,3))) 

                if r != None and minR != None and maxR != None:
                    if r < minR or r > maxR:
                        self.ui.lineEdit.setStyleSheet("background-color: red")
                        rez += u'Cопротивление ' + self.ui.lineEdit.text() + u' не входит в рассчитанный коридор.'
                        self.defectItem = True                
#01.2019        
            if minU != None and maxU != None:
                for i in range(self.nK):
                    if self.curr_k == self.sK[i] :
                        self.slineEdit_Kor[i].setText(str(round(minU,2)) + ' - ' + str(round(maxU,2)))
                        if un != None:
                            if un < minU or un > maxU:
                                self.slineEdit_Kor[i].setStyleSheet("background-color: red")
                                rez += u'Напряжение ' + str(un) + u' не входит в рассчитанный коридор.'
                                self.defectItem = True                        
        return rez    
        
        
    def coefMeasure(self, id_dev):
        coef = 1.0
        if self.Devices.data['devices'][str(id_dev)]['ind_measure'] == 1:
            coef = 0.001
        if self.Devices.data['devices'][str(id_dev)]['ind_measure'] == 2:
            coef = 1000.0
        return coef    


    def work(self):        
        self.workAmp = None
        self.workVolt = None
        self.ui.label_4.setText(u'Амперметр')
        self.ui.label_5.setText(u'Вольтметр')
        if str(self.info.ClassAccuracy).find('P') == -1:
            self.U5 = None
            self.U10 = None
            self.U15 = None
        else:    
            self.I5 = None
            self.I10 = None
            self.I15 = None
        self.ui.lineEdit_I5.setText("")
        self.ui.lineEdit_I10.setText("")
        self.ui.lineEdit_I15.setText("")
        self.ui.lineEdit_K5.setStyleSheet("background-color: white")
        self.ui.lineEdit_K10.setStyleSheet("background-color: white")
        self.ui.lineEdit_K15.setStyleSheet("background-color: white")
        
        self.isWork = True 
        
        self.Devices = Devices(self.env)
        
#        self.MinAmp = 999999
        self.MinAmp = 0.01
        for i in range(len(self.Devices.data['devices'])):
            if self.Devices.data['devices'][str(i)]['activ'] == True and self.Devices.data['devices'][str(i)]['ind_name'] == 0:
                if self.MinAmp > self.Devices.data['devices'][str(i)]['min_value']:
                    self.MinAmp = self.Devices.data['devices'][str(i)]['min_value']
                                    
        self.testEnabled(True)
        
        global stateWork
        
        self.wasHand = self.isHand
        if True:                
            # Проверка работоспособности порта и приборов
            global AV, yyy                 
            global isBreak
            AV = self.ReadPort()
            #26.10.2018
            # ДЛЯ ЭМУЛЯЦИИ
            if self.ui.checkBox.isChecked():
                yyy += 0.005
                hs = self.ui.horizontalSlider.value()
                AV = [str(0.2 * hs * float(self.ui.lineEdit_18.text())),
                      str((math.sqrt(0.2 * hs) + yyy) * float(self.ui.lineEdit_19.text()))]
            # ВРЕМЕННО ДЛЯ ЭРМАНА
           # self.ui.label_14.setText(u'Предел')
                        
            if AV == None:
                isBreak = True                                
                msgBox(self, u"Проблемы считывания данных с приборов!")
                self.isHand = False   
                self.btnStart.click()
                return False

            # 20.01 подумать как пересчитать единицу измерения
            if float(AV[0]) >= self.MinAmp:
                isBreak = True                                
                msgBox(self, u"Выставьте реостат в ноль и\nзапустите поверку заново.!!!")
                
                self.ui.horizontalSlider.setValue(0)
                
                self.isHand = False   
                self.btnStart.click()
                return False
                        
            stateWork = WORK
            self.tread.start()
        self.isHand = True
        self.ui.lineEdit.setFocus()
        return True
        
                    
    def pause(self):
        self.isWork = False 
        self.testEnabled(False)
    
        global stateWork        
        self.wasHand = self.isHand
        if True:                
            stateWork = PAUSE
            self.tread.quit()   # А надо ли?                                
        self.isHand = True   


#ВРЕМЕННО
    def on_signal1(self):
        self.ui.lineEdit_2.setText('1')

    def on_signal2(self):
        self.ui.lineEdit_2.setText('2')

    def on_signal3(self):
        self.ui.lineEdit_2.setText('')


    def on_mysignal(self):
        self.ui.label_6.setText(self.ui.label_6.text() + "#")
        if len(self.ui.label_6.text()) > 20:
            self.ui.label_6.setText("")
        self.ui.lineEdit_4.setText('____')
        self.ui.lineEdit_5.setText('____')

    def on_mysignal2(self):
        print('Обработан пользовательский сигнал2')
                
        msgBox(self, u"Сбой COM-порта!\nЗапустите поверку заново.!")
        self.isHand = True   
        self.btnStart.click()
                    
                
    def on_mysignal3_(self):
        global AV
        global points
        global points_back
        global isBreak
        global stateWork
        global oldPoints_
        global getSecondCurrent
        global stop
        
        self.ui.label_6.setText("")
        if AV[0] == False:
            self.ui.lineEdit_4.setText('____')
        else:    
            self.ui.lineEdit_4.setText(str(round(float(AV[0]),3)))
        
        if AV[1] == False:
            self.ui.lineEdit_5.setText('____')
        else:    
            self.ui.lineEdit_5.setText(str(round(float(AV[1]),3)))        
        
        if AV[0] == False or AV[1] == False:
            # хотя бы в одной цепочке приборов нет реального значения
            stop = False
            return
        
        self.u2 = None       
        self.i2 = None       
        

        
        if float(AV[0]) < self.MinAmp or float(AV[1]) < self.MinAmp:

            self.yyy += 0.4 # для эмуляции        
            self.workAmp = None
            self.workVolt = None
            if len(points) >= 1:
                # НОВЫЙ АЛГОРИТМ РАСЧЕТА!
                # Меняем порядок точек в points_back
                points_back_ = []
                for i in range(len(points_back)):
                    points_back_ += [[points_back[len(points_back) - i - 1][0], points_back[len(points_back) - i - 1][1]]]                
                
                if self.Devices.data['back'] == True:    
                    points = points_back_
                 
 
                for i in range(self.nK):
                    self.slineEdit_K[i].setStyleSheet("background-color: white")
                    self.slineEdit_U[i].setText("")
                    self.slineEdit_I[i].setText("")
                    self.slineEdit_Pred[i].setText("")
                    self.slineEdit_Kor[i].setText("")

        
                classAccuracy = None    
                if str(self.info.ClassAccuracy).find('P') == -1:
                    typeCoil = 1
                else:    
                    typeCoil = 2
                    if str(self.info.ClassAccuracy).find('10P') != -1:
                        classAccuracy = 1
                    else:    
                        classAccuracy = 2
                self.solut = self.calcCoil(None, self.curr_r, self.info.SecondCurrent, self.info.SecondLoad, points, typeCoil, classAccuracy, self.sample)
                # print self.solut[0]
                # print self.solut[1]
                # print self.solut[2]
                # print self.solut[3]
                #
                swRed = False        
                if str(self.info.ClassAccuracy).find('P') == -1:
                    # Измерительная обмотка
                    # print u'Измерительная обмотка'
                    for i in range(self.nK):
                        if self.solut[2][i] != None:
                            self.slineEdit_I[i].setText(str(round(self.solut[2][i], 2)))
                        if self.solut[1][i] != None:
                            self.slineEdit_U[i].setText(str(round(self.solut[1][i], 2)))
                        if self.solut[3][i] != None:
                            self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                        if self.solut[2][i] != None and self.solut[3][i] != None:
                            self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                            if self.solut[2][i] > self.solut[3][i]:
                                self.slineEdit_K[i].setStyleSheet("background-color: red")
                                if self.solut[0] == i:
                                    swRed = True
                                    self.defectItem = True                                                    
                else:        
                    # Защитная обмотка
                    # print u'Защитная обмотка'
                    for i in range(self.nK):
                        if self.solut[1][i] != None:
                            self.slineEdit_I[i].setText(str(round(self.solut[1][i], 2)))
                        if self.solut[2][i] != None:
                            self.slineEdit_U[i].setText(str(round(self.solut[2][i], 2)))
                        if self.solut[3][i] != None:
                            self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                        if self.solut[1][i] != None and self.solut[3][i] != None:
                            self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                            if self.solut[1][i] > self.solut[3][i]:
                                self.slineEdit_K[i].setStyleSheet("background-color: red")
                                if self.solut[0] == i:
                                    swRed = True
                                    self.defectItem = True                                    

                # print 999999999999999999999999999
                self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), points, points_back, 1, self.solut)

                n = self.solut[0]
                # print 'n=', n
                # print self.sK
                # print self.solut[1]
                # print self.solut[2]
                if n == None or (n != None and (self.solut[1][n] == None or self.solut[2][n] == None)):
                    self.defectItem = True                                    
                    self.oItem.set_noteste(self.idItem) 
                    self.oMap.mapRefresh.emit()
                    
                    self.btnStart.click()
                    msgBox(self, u"Нет решения для данной катушки, т.к. нет пересечения \n графика с линиями напряжений намагничивания по всем коэффициентам")
                    stop = False
                    return
                self.K = self.sK[n]
                self.I = self.solut[1][n]
                self.U = self.solut[2][n]
                self.predel = self.solut[3][n]
                
                # print 'SAVE SAVE SAVE SAVE SAVE '
                self.save_calcData(self.checking_2)
                self.save_points(points)                

                self.calcGlobal(self.oMap.iMapID, None, self.idStand, None, None, True)                
                # print 'calcGlobal                     777777777777777777777777777777'
                
                # Выдача предупреждения в случае отсутствия решения либо неправильного решения
                if swRed:
                    self.btnStart.click()
                    msgBox(self, u"Коэффициент не соответствует заданному!")
                    stop = False
                    return
                                                            
                rez = self.setColors(self.idItem, self.idCoil)
                
                                
                self.ui.label_4.setText(u'Амперметр')                            
                self.ui.label_5.setText(u'Вольтметр')                            
                                
                points = []
                points_back = []
                
                # останавливаем чтение с приборов, если протестированы все трансы
                if (self.tvCoil.table.currentIndex().row() == self.tvCoil.get_row_count() - 1 and
                    self.tvItem.table.currentIndex().row() == self.tvItem.get_row_count() - 1):                
                    self.isHand = True   
                    self.btnStart.click()
                    stop = False
                    return

                '''
                self.isHand = True      # ВРЕМЕННО
                self.btnStart.click()   # ВРЕМЕННО
                return                  # ВРЕМЕННО
                '''
                                
                self.isHand = False
                self.move_item_coil(True)
        else:            
            if self.checking_2 == None:
                isBreak = True        
                msgBox(self, u"Продолжение невозможно, поскольку\n не сохранено сопротивление!")
                self.isHand = True   
                self.btnStart.click()
                stop = False
                return
            
            if not self.graphEmpty:            
                isBreak = True        
                msgBox(self, u"Продолжение невозможно, поскольку\nтестирование данной катушки\nбыло проведено ранее!")
                self.isHand = True   
                self.btnStart.click()
                stop = False
                return            
            
            if not self.ui.checkBox.isChecked():
                if self.workAmp == None or self.workVolt == None:
                    stop = False
                    return
            
            if len(points) < 1:
                if not self.wasHand:
                    self.isHand = False   
                    self.btnStart.click()
                points += [[float(AV[0]), float(AV[1])]]
                stop = False
                return
            else:
                if float(AV[0]) < points[len(points)-1][0]:
                    # Обратный график
                    # 06.03.2020 Новый алгоритм
                    if getSecondCurrent:        
                        if len(points_back) < 1:
                            points_back += [[float(AV[0]), float(AV[1])]]
                            stop = False
                            return
                        if float(AV[0]) >= points_back[0][0]:
#                            print 'points_back = []points_back = []points_back = []points_back = []points_back = []points_back = []points_back = []points_back = []points_back = []points_back = []'
                            points_back = []
                            stop = False
                            return
                        if float(AV[0]) >= points_back[len(points_back)-1][0]:
                            stop = False
                            return
                        points_back += [[float(AV[0]), float(AV[1])]]
                        
                    oldPoints_ += [[float(AV[0]), float(AV[1])]]  #  ?????????
                else:
                    # Прямой график
                    if float(AV[0]) == points[len(points)-1][0]:                        
                        stop = False
                        return    # игнорирование повторяющихся точек
                    points += [[float(AV[0]), float(AV[1])]]
                      
                    if (str(self.info.ClassAccuracy).find('P') == -1 and points[len(points)-1][0] > self.solut[1][self.nK - 1]  ) or \
                       (str(self.info.ClassAccuracy).find('P') != -1 and points[len(points)-1][0] > self.solut[3][self.nK - 1]):
                        
                        # ВРЕМЕННО ДЛЯ ЭРМАНА
                        '''
                        if (getSecondCurrent == False):
                            if (str(self.info.ClassAccuracy).find('P') == -1):
                                self.ui.label_14.setText(str(self.solut[1][self.nK - 1]))
                            if (str(self.info.ClassAccuracy).find('P') != -1):
                                self.ui.label_14.setText(str(self.solut[3][self.nK - 1]))
                        '''
                        getSecondCurrent = True           # Признак достижения графиком номинального тока             
                        self.sound.play(self.env.config.snd_notify.coil_done)
 
                # Меняем порядок точек в points_back
                points_back_ = []
                for i in range(len(points_back)):
                    points_back_ += [[points_back[len(points_back) - i - 1][0], points_back[len(points_back) - i - 1][1]]]                
                
                if self.Devices.data['back'] == True:    
                    points_ = points_back_
                else:    
                    points_ = points
  
 
                for i in range(self.nK):
                    self.slineEdit_K[i].setStyleSheet("background-color: white")
                    self.slineEdit_U[i].setText("")
                    self.slineEdit_I[i].setText("")
                    self.slineEdit_Pred[i].setText("")
                    self.slineEdit_Kor[i].setText("")

        
                classAccuracy = None    
                if str(self.info.ClassAccuracy).find('P') == -1:
                    typeCoil = 1
                else:    
                    typeCoil = 2
                    if str(self.info.ClassAccuracy).find('10P') != -1:
                        classAccuracy = 1
                    else:    
                        classAccuracy = 2
                self.solut = self.calcCoil(None, self.curr_r, self.info.SecondCurrent, self.info.SecondLoad, points_, typeCoil, classAccuracy, self.sample)
                # print self.solut[0]
                # print self.solut[1]
                # print self.solut[2]
                # print self.solut[3]
        
                if str(self.info.ClassAccuracy).find('P') == -1:
                    # Измерительная обмотка
                    # print u'Измерительная обмотка'
                        
                    for i in range(self.nK):
                        if self.solut[2][i] != None:
                            self.slineEdit_I[i].setText(str(round(self.solut[2][i], 2)))
                        if self.solut[1][i] != None:
                            self.slineEdit_U[i].setText(str(round(self.solut[1][i], 2)))
                        if self.solut[3][i] != None:
                            self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                        if self.solut[2][i] != None and self.solut[3][i] != None:
                            self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                            if self.solut[2][i] > self.solut[3][i]:
                                self.slineEdit_K[i].setStyleSheet("background-color: red")
                
                else:        
                    # Защитная обмотка
                    # print u'Защитная обмотка'

                    for i in range(self.nK):
                        if self.solut[1][i] != None:
                            self.slineEdit_I[i].setText(str(round(self.solut[1][i], 2)))
                        if self.solut[2][i] != None:
                            self.slineEdit_U[i].setText(str(round(self.solut[2][i], 2)))
                        if self.solut[3][i] != None:
                            self.slineEdit_Pred[i].setText(str(round(self.solut[3][i], 2)))
                        if self.solut[1][i] != None and self.solut[3][i] != None:
                            self.slineEdit_K[i].setStyleSheet("background-color: lightgreen")
                            if self.solut[1][i] > self.solut[3][i]:
                                self.slineEdit_K[i].setStyleSheet("background-color: red")

                self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), points, points_back, 1, self.solut)
        stop = False


    def calcNomAmperage(self, points, checking_2, sample, SecondCurrent):
        # Расчет обратного номинального тока
        if sample == None or checking_2 == sample['id']:
            self.nomAmperage = SecondCurrent
            return self.nomAmperage             
        self.nomAmperage = None
        for i in range(len(points)):
            if (i > 0 and sample['un'] >= points[i - 1][1]
                      and sample['un'] <= points[i][1]):
                # График пересекся с линией y = self.sample['un']
                x1 = points[i - 1][0]
                x2 = points[i][0]
                y1 = points[i - 1][1]
                y2 = points[i][1]
                                
                if abs(y2 - y1) > self.epsilon:
                    self.nomAmperage = (sample['un'] - y1) * (x2 - x1) / (y2 - y1) + x1
                else:
                    self.nomAmperage = y1
                return self.nomAmperage             
                    
        # График не пересекся с линией y = self.sample['un']
        # Продлеваем последний отрезок и пытаемся найти пересечение
           
        i = len(points) - 1                
        x2 = points[i][0]
        y2 = points[i][1]        
        while i > 0 and y2 <= points[i - 1][1]:
            i -= 1        
        if i > 0:  
            x1 = points[i - 1][0]
            y1 = points[i - 1][1]                
            y  = sample['un']
            if abs(x2 - x1) > self.epsilon and abs(y2 - y1) > self.epsilon:
                self.nomAmperage = (y - y1) * (x2 - x1) / (y2 - y1) + x1                                        
        return self.nomAmperage             
    
        
    def showTestCoilReport(self):
        self.TestCoilReport.ui.groupBox.setTitle(u'Данные по катушке № ' + str(self.info.CoilNumber) + u' (серия: ' + self.series + ')')
        
        self.TestCoilReport.ui.label.setText(u'Образец\nЗав.№ ' + str(self.sampleSerialnumber))
        self.TestCoilReport.ui.label_2.setText(u'Изделие\nЗав.№ ' + str(self.serialnumber))
        
        self.TestCoilReport.ui.lineEdit.setText(str(self.sample['r']))
        self.TestCoilReport.ui.lineEdit_2.setText(str(self.sample['un']))
        self.TestCoilReport.ui.lineEdit_3.setText(str(self.sample['in']))
        self.TestCoilReport.ui.lineEdit_4.setText(str(self.sample['k']))
        self.TestCoilReport.ui.lineEdit_5.setText(self.ui.lineEdit.text())
        self.TestCoilReport.ui.lineEdit_6.setText(self.ui.lineEdit_2.text())
        self.TestCoilReport.ui.lineEdit_7.setText(self.ui.lineEdit_10.text())
        self.TestCoilReport.ui.lineEdit_8.setText(self.ui.lineEdit_3.text())
        self.TestCoilReport.ui.lineEdit_9.setText(str(self.Devices.data['accuracy']['r']))
        self.TestCoilReport.ui.lineEdit_10.setText(str(self.Devices.data['accuracy']['a']))
        self.TestCoilReport.ui.lineEdit_13.setText(str(self.fact_accur_r))        
        if self.fact_accur_r  > self.Devices.data['accuracy']['r']:                        
            self.TestCoilReport.ui.lineEdit_13.setStyleSheet("background-color: red")
        else:    
            self.TestCoilReport.ui.lineEdit_13.setStyleSheet("background-color: white")
        
        self.TestCoilReport.ui.lineEdit_14.setText(str(self.fact_accur_un))
        if self.fact_accur_un  > self.Devices.data['accuracy']['a']:                        
            self.TestCoilReport.ui.lineEdit_14.setStyleSheet("background-color: red")
        else:    
            self.TestCoilReport.ui.lineEdit_14.setStyleSheet("background-color: white")
                                                
        self.TestCoilReport.setEnabled(True)
        self.TestCoilReport.exec_()
        
                
    def signScale(self, x):
        # Генерирует список подписей осей координат
        if abs(x) < self.epsilon:
            return [0]
        sgn = 1
        if x < 0:
            sgn = -1            
        n = 0
        x_ = abs(x)
        if x_ >= 100:
            while x_ >= 100:
                x_ /= 10;  n += 1
        if x_ < 10:
            while x_ < 10:
                x_ *= 10;  n -= 1
        x_ = round(x_)
        signs = []
        k = 1.    
        if x_ > 25 and x_ <= 50:
            k = 0.5
        if x_ <= 25:
            k = 0.25
        for i in range(10):    
            sign = sgn * round(k * (i+1) * pow(10, n+1), -n+1)
            if abs(sign) > abs(x):
                break
            signs += [sign]
        return signs    


    def BieldScene(self, scene, width, height, points, pre_points, mode, solut):
        # mode = 1 - виден график целиком
        # mode = 2 - виден график до правой линии коридора 
        scene.clear()
        
        self.nomVoltage = None
        all_points = points + pre_points
        if len(all_points) < 1:
            return

        maxX = all_points[0][0]
        maxY = all_points[0][1]
        for i in range(len(all_points)):
            if all_points[i][0] > maxX:
                maxX = all_points[i][0]
            if all_points[i][1] > maxY:
                maxY = all_points[i][1]
                
        if mode == 1:                        
            if self.corridors != None and maxX < self.corridors['max_in']: 
                maxX = self.corridors['max_in']        
            if self.curr_inom != None and maxX < self.curr_inom:
                maxX = self.curr_inom
        else:
            if self.fRating2 == None:
                if str(self.info.ClassAccuracy).find('P') == -1:
                    # Измерительная обмотка
                    maxX = self.I15
                else:
                    maxX = self.PredI15
            else:
                if str(self.info.ClassAccuracy).find('P') == -1:
                    maxX = self.I5
                else:
                    maxX = self.PredI5
                    if self.U5 != None and self.U5 > maxY:
                        maxY = self.U5
                                                        
            if maxX < self.info.SecondCurrent:
                maxX = self.info.SecondCurrent
                            
        maxX *= 1.02 # Чтобы были видны линии коридоров  
        maxY *= 1.02 # Чтобы были видны линии коридоров  
        
        smXl = round(0.1 * width)
        smXr = round(0.05 * width)
        smYt = round(0.1 * height)
        smYb = round(0.1 * height)
        vW = width
        vH = height
        grW = width - smXl - smXr
        grH = height - smYt - smYb
        rPoint = 2
        
        kX = kY = 1
        
        if abs(maxX) > self.epsilon:
            kX = maxX / grW        
        if abs(maxY) > self.epsilon:
            kY = maxY / grH        
        
        # Оси координат
        self.pen.setColor(QtCore.Qt.black)
        self.pen.setWidth(2)
                        
        scene.addLine(smXl, smYt, smXl, vH - smYb, self.pen)
        scene.addLine(smXl, vH - smYb, vW - smXr, vH - smYb, self.pen)

        # Подписи осей
        fnt =  QFont()
        fnt.setPixelSize(20)
        t1 = scene.addText('A', fnt)            
        t1.setPos(vW - smXr + 2, vH - 2 * smYb)
        t1 = scene.addText('V', fnt)            
        t1.setPos(smXl, 2)
        
        self.pen.setWidth(1)
        ss = self.signScale(maxX)
        for i in range(len(ss)):
            self.pen.setColor(QtCore.Qt.gray)
            scene.addLine(smXl + round(ss[i] / kX), vH - smYb, smXl + round(ss[i] / kX), smYt, self.pen)
            t1 = scene.addText(str(ss[i]))
            
            t1.setPos(smXl + round(ss[i] / kX - t1.boundingRect().width() / 2), vH - smYb - 4)
        ss = self.signScale(maxY)
        for i in range(len(ss)):
            scene.addLine(smXl, vH - smYb - round(ss[i] / kY), vW - smXr, vH - smYb - round(ss[i] / kY), self.pen)
            t1 = scene.addText(str(ss[i]))
            #t1 = scene.addText('{:.0f}'.format(ss[i]))
            smT = smXl - t1.boundingRect().width()
            if smT < 0:
                smT = 0
            t1.setPos(smT , vH - smYb - round(ss[i] / kY + t1.boundingRect().height() / 2))
                
        # Линия номинального вторичного тока
        self.pen.setColor(QtCore.Qt.red)
      
        if str(self.info.ClassAccuracy).find('P') == -1:
            # Линии напряжения намагничивания
            scene.addLine(smXl, vH - smYt - round(solut[3][0]/kY),  vW - smXr, vH - smYt - round(solut[3][0]/kY), self.pen)
            if self.rating2 == None:
                scene.addLine(smXl, vH - smYt - round(solut[3][1]/kY),  vW - smXr, vH - smYt - round(solut[3][1]/kY), self.pen)
                scene.addLine(smXl, vH - smYt - round(solut[3][2]/kY),  vW - smXr, vH - smYt - round(solut[3][2]/kY), self.pen)
        else:
            # Линии тока намагничивания
            scene.addLine(smXl + round(solut[3][0]/kX), smYt,  smXl + round(solut[3][0]/kX), vH - smYb, self.pen)
            if self.rating2 == None:
                scene.addLine(smXl + round(solut[3][1]/kX), smYt,  smXl + round(solut[3][1]/kX), vH - smYb, self.pen)
                scene.addLine(smXl + round(solut[3][2]/kX), smYt,  smXl + round(solut[3][2]/kX), vH - smYb, self.pen)
                
                                
                
        self.pen.setColor(QtCore.Qt.blue)
        if self.info.SecondCurrent != None or self.info.SecondCurrent > self.epsilon:
            scene.addLine(smXl + round(self.info.SecondCurrent/kX)+10, smYt, smXl + round(self.info.SecondCurrent/kX)+10, vH - smYb, self.pen)
                
        self.pen.setColor(QtCore.Qt.green)
        if self.curr_un == None or self.curr_un < self.epsilon:
            if solut[2][0] != None:
                scene.addLine(smXl, vH - smYt - round(solut[2][0]/kY), vW - smXr, vH - smYt - round(solut[2][0]/kY), self.pen)
            if solut[1][0] != None:
                scene.addLine(smXl + round(solut[1][0]/kX), smYt, smXl + round(solut[1][0]/kX), vH - smYb, self.pen)
            if self.rating2 == None:
                if solut[2][1] != None:
                    scene.addLine(smXl, vH - smYt - round(solut[2][1]/kY), vW - smXr, vH - smYt - round(solut[2][1]/kY), self.pen)
                if solut[1][1] != None:
                    scene.addLine(smXl + round(solut[1][1]/kX), smYt, smXl + round(solut[1][1]/kX), vH - smYb, self.pen)
                if solut[2][2] != None:
                    scene.addLine(smXl, vH - smYt - round(solut[2][2]/kY), vW - smXr, vH - smYt - round(solut[2][2]/kY), self.pen)
                if solut[1][2] != None:
                    scene.addLine(smXl + round(solut[1][2]/kX), smYt, smXl + round(solut[1][2]/kX), vH - smYb, self.pen)
                    
        self.pen.setWidth(1)
                
        self.pen.setWidth(2)        
        if self.curr_un != None and self.curr_un > self.epsilon:
            scene.addLine(smXl, vH - smYt - round(self.curr_un/kY), vW - smXr, vH - smYt - round(self.curr_un/kY), self.pen)
        if self.curr_inom != None and self.curr_inom > self.epsilon:
            scene.addLine(smXl + round(self.curr_inom/kX), smYt, smXl + round(self.curr_inom/kX), vH - smYb, self.pen)
                                                               
        # Расчет номинального напряжения
        self.nomVoltage = self.calcNomVoltage(points, self.info.SecondCurrent)
                
        # Коридор номинального тока по всей серии/заказу
        self.pen_2.setWidth(2)
        self.pen_2.setColor(QtCore.Qt.green)
        #self.pen_2.setColor(QtCore.Qt.black)
        self.pen_2.setDashPattern([5,5])
        self.pen_2.setDashOffset(5)
        
        
        if self.corridors != None:
            if self.corridors['min_in'] != None:
                scene.addLine(smXl + round(self.corridors['min_in']/kX), smYt,
                              smXl + round(self.corridors['min_in']/kX), vH - smYb, self.pen_2)
                scene.addLine(smXl + round(self.corridors['max_in']/kX), smYt,
                              smXl + round(self.corridors['max_in']/kX), vH - smYb, self.pen_2)

        # Кривая текущего испытания
        self.pen.setWidth(2)
        self.pen.setColor(QtCore.Qt.black)
        for i in range(len(points) - 1):
            scene.addLine(smXl + round(points[i][0]/kX), vH - smYt - round(points[i][1]/kY),
                          smXl + round(points[i+1][0]/kX), vH - smYt - round(points[i+1][1]/kY), self.pen)

        # Кривая предыдущего испытания
        if pre_points != [] and self.Devices.data['back'] == True:        
            self.pen.setColor(QtCore.Qt.blue)
            self.pen.setWidth(2)
            for i in range(len(pre_points) - 1):
                scene.addLine(smXl + round(pre_points[i][0]/kX), vH - smYt - round(pre_points[i][1]/kY),
                              smXl + round(pre_points[i+1][0]/kX), vH - smYt - round(pre_points[i+1][1]/kY), self.pen)



    def calcNomVoltage(self, points, SecondCurrent):
        # Расчет номинального напряжения
        for i in range(len(points)):
            if (i > 0 and SecondCurrent >= points[i - 1][0]
                      and SecondCurrent <= points[i][0]):
                x1 = points[i - 1][0]
                x2 = points[i][0]
                y1 = points[i - 1][1]
                y2 = points[i][1]
                if abs(x2 - x1) > self.epsilon:
                    return (SecondCurrent - x1) * (y2 - y1) / (x2 - x1) + y1
                else:
                    return y1
        return None



    def pushButton_2_Click(self):
        # print self.TransR(1, 41, 24, 20)
        # print self.TransR(2, 41, 24, 20)
        # print 'temperature1 = ', self.temperature
        # print 'self.oMap.iMapID1 = ', self.oMap.iMapID
        #
        return
        
        import wmi
        c = wmi.WMI ()

        for process in c.Win32_Process ():
            print(process.ProcessId, process.Name)
        return        

                
    def pushButton_Click(self):
        import ReportsExcel
        if self.ui.checkBox.isChecked():
            ReportsExcel.report(self.VerificationForm.ui.lbShortName.text(), self.series, None, self.globalReport, self.Devices.data['accuracy']['r'], self.Devices.data['accuracy']['a'], False)
        else:            
            ReportsExcel.report(self.VerificationForm.ui.lbShortName.text(), self.series, self.ordernumber, self.globalReport, self.Devices.data['accuracy']['r'], self.Devices.data['accuracy']['a'], False)                
        return
        

    def ReadPort(self):
        global port
        global isReadPort

        time.sleep(0.01)
        
        # Чтение показания приборов (амперметр, вольтметр)    
        global isTest
        
        try:
            A = ''
            V = ''
            port.port = self.env.config.devices.chp02m.port
            port.baudrate = 9600
            port.bytesize = 8
            port.parity = 'N'
            port.stopbits = 1
            port.timeout = 0.1
            if not self.ui.checkBox.isChecked() or self.ui.checkBox_2.isChecked():
                port.close()
                port.open()
                                                
            if self.ui.checkBox.isChecked():
                a = self.workAmp
                if a != None: a += 1
                v = self.workVolt
                if v != None: v += 1
                
                self.ui.checkBox_2.setText(u'Читать приборы (' + str(a) + ') (' + str(v) + ')')                     
                                                
            # A - показание амперметра
            if self.Devices.data['min_alg'] == False:    
                A = self.ReadDevices(port, 0)
            else:    
                A = self.ReadDevices_2(port, 0, self.workAmp)                
                  
            if A == None:
                isReadPort = True
                return None
           
            if self.workAmp != None:
                A = str(self.coefMeasure(self.workAmp) * float(A))
            
            time.sleep(0.01)
            # V - показание вольтметра
            if self.Devices.data['min_alg'] == False:    
                V = self.ReadDevices(port, 1)
            else:    
                V = self.ReadDevices_2(port, 1, self.workVolt)
                            
            if V == None:
                isReadPort = True
                return None
            if self.workVolt != None:
                V = str(self.coefMeasure(self.workVolt) * float(V))
            
        except SerialException:
            # print u"Порт " + port.port + u' не открывается!'
            self.errStr = u"Порт " + port.port + u' не открывается!'
            isReadPort = True
            return None
        except Exception:
            isReadPort = True
            return None
        finally:
            port.close()
        isReadPort = True
        if A != False:
            A = A.strip()
        if V != False:
            V = V.strip()
        return [A, V]                    


    def ReadDevices(self, port, ind_name):
        # Чтение показаний цепочки приборов (выбирается показание с первого работающего прибора)        
        # ind_name = 0 - амперметры        
        # ind_name = 1 - вольтметры
        
        self.ind_name = ind_name # self.ind_name - для режима эмуляции 
                
        for i in range(len(self.Devices.data['devices'])):
            self.ind_device = i + 1  # self.ind_device - для режима эмуляции
            
            if self.Devices.data['devices'][str(i)]['activ'] == False or self.Devices.data['devices'][str(i)]['ind_name'] != ind_name:
                continue
            
            
            if self.Devices.data['devices'][str(i)]['ind_type'] == 0:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 1:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 2:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)                
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])

            Val = self.Devices.ReadDevice(port, self.Devices.data['devices'][str(i)]['ind_type'], st, self.Devices.data['devices'][str(i)]['coeff'])
            if ind_name == 0:
                self.ui.lineEdit_14.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
            if ind_name == 1:
                self.ui.lineEdit_15.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
            time.sleep(self.Devices.data['pause'])
                                
            if Val == None:
                continue
            else:
                return Val                             
        return Val


    def ReadDevices_2(self, port, ind_name, workDev):        
        # Чтение показаний цепочки приборов (выбирается показание с первого прибора превышающего минимальное значение)         
        # ind_name = 0 - амперметры        
        # ind_name = 1 - вольтметры
        
        #20.01
        self.ind_name = ind_name # self.ind_name - для режима эмуляции 
                
        for i in range(len(self.Devices.data['devices'])):
            self.ind_device = i + 1  # self.ind_device - для режима эмуляции
            
            if self.Devices.data['devices'][str(i)]['activ'] == False or self.Devices.data['devices'][str(i)]['ind_name'] != ind_name:
                continue
            if workDev != None and workDev != i:
                continue
            if self.Devices.data['devices'][str(i)]['ind_type'] == 0:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 1:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 2:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)                
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])

            Val = self.Devices.ReadDevice(port, self.Devices.data['devices'][str(i)]['ind_type'], st, self.Devices.data['devices'][str(i)]['coeff'])
            if ind_name == 0:
                self.ui.lineEdit_14.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
            if ind_name == 1:
                self.ui.lineEdit_15.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
            time.sleep(self.Devices.data['pause'])
                            
                            
            # Определение рабочего прибора и присвоение ему индекса
            if workDev == None:
                if Val != None:
                    # С учетом единицы измеренния
                    if float(Val) > self.Devices.data['devices'][str(i)]['min_value']:
                        workDev = i #??????????????????????????
                        if ind_name == 0:
                            # print 'ValAmper=', Val
                            self.workAmp = i
                            #25.10.17
                            self.MinAmp = self.Devices.data['devices'][str(i)]['min_value']                            
                            #25.10.17
                            # print 'self.workAmp=', self.workAmp
                            #19.01 поменял единицу измерения 
                            self.ui.label_4.setText(str(self.workAmp + 1) + u'. Амперметр (' + self.Devices.Measures[self.workAmp].currentText() + u')')                            

                        if ind_name == 1:
                            # print 'ValVoltmetr=', Val
                            self.workVolt = i
                            # print 'self.workVolt=', self.workVolt
                            #19.01 поменять единицу измерения 
                            self.ui.label_5.setText(str(self.workVolt + 1) + u'. Вольтметр (' + self.Devices.Measures[self.workVolt].currentText() + u')')                            
                            
                        return Val
                    else:
                        continue                            
        if workDev == None:
            return False   # False означает, что показания всех трансов из цепочки нулевые                             
        return Val
                    

    def coil_clear(self, mode):
#        mode = 1 - Очищается график вместе с сопротивлением
#        mode = 2 - Очищается только график

        self.yyy = 0.4 # для эмуляции        
        
        self.coil_clear_()
        self.points = []
            
        self.query_9.prepare('UPDATE checking_2 SET un=:un, un_=:un_, inom=:inom, k=:k, rating=:rating, su2=:su2, u2=:u2, i2=:i2, predel=:predel WHERE id=:id')            
        self.query_9.bindValue(":id", self.checking_2)                
        self.query_9.bindValue(":un", None)
        self.query_9.bindValue(":un_", None)
        self.query_9.bindValue(":inom", None)
        self.query_9.bindValue(":k", None)
        self.query_9.bindValue(":rating", None)
        self.query_9.bindValue(":su2", None)
        self.query_9.bindValue(":u2", None)
        self.query_9.bindValue(":i2", None)
        self.query_9.bindValue(":predel", None)

        self.query_9.exec_()
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка обнуления данных2",
            QMessageBox.Ok)        
        
        self.oItem.stateItem = self.oItem.NOITEM  # Для того чтобы set_noteste гарантированно срабатывала  
        self.oItem.set_noteste(self.idItem) 
        defectItem_ = self.defectItem       
        self.oMap.mapRefresh.emit()
        self.defectItem = defectItem_       
                
        self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.points, self.oldPoints, 1, self.solut)
                
        
    def coil_clear_(self):
        self.query_9.prepare('DELETE FROM checking_2sp WHERE checking_2 in (SELECT id FROM checking_2 WHERE item = :item AND coil = :coil AND stand = :stand)')
        self.query_9.bindValue(":stand", self.idStand)
        self.query_9.bindValue(":item", self.idItemLast)
        self.query_9.bindValue(":coil", self.idCoilLast)
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка обнуления данных1",
            QMessageBox.Ok)
            return        

    def testEnabled(self,enab):
#        self.ui.label.setEnabled(enab)
        self.ui.label_3.setEnabled(enab)
        self.ui.label_4.setEnabled(enab)
        self.ui.label_5.setEnabled(enab)
        self.ui.label_7.setEnabled(enab)
        self.ui.label_9.setEnabled(enab)
        self.ui.label_10.setEnabled(enab)
        self.ui.lineEdit.setEnabled(enab)
        self.ui.lineEdit_7.setEnabled(enab)
                
        for i in range(len(self.sK)):
            self.scheckBox[i].setEnabled(enab)
            self.slineEdit_K[i].setEnabled(enab)
            self.slineEdit_U[i].setEnabled(enab)
            self.slineEdit_I[i].setEnabled(enab)
            self.slineEdit_Pred[i].setEnabled(enab)
            self.slineEdit_Kor[i].setEnabled(enab)
            
        self.ui.checkBox_6.setChecked(False)
        self.VerificationForm.ui.btnDevices.setEnabled(not enab)
        self.ui.pushButton.setEnabled(not enab)
        self.ui.pushButton_3.setEnabled(not enab)
        global isBreak
        if isBreak:        
            self.VerificationForm.btnCoilClear.setEnabled(False)
            if enab == False:
                self.VerificationForm.btnCoilClear.setEnabled(self.checking_2 != None or len(self.points) > 0)
        else:    
            self.VerificationForm.btnCoilClear.setEnabled(not enab)


    def done_test(self):
        # Проверяем протестирован ли трансформатор (тележка??????) полностью
        model.clear()
        
        strSQL = """
select * from item
where test_map = :test_map
and istested <> true
"""
        self.query.prepare(strSQL)
        self.query.bindValue("test_map", self.oMap.iMapID)
        if not self.query.exec_():
            raise Exception(self.query.lastError().text())
        else:    
            model.setQuery(self.query)
        if model.rowCount() > 0:
            return False
        else:
            return True


    def closeEvent(self, event):
        return    

    def setMeasureR(self, nameMeasure):
        try:
            # print 'self.Devices.data[ind_measureR]=', self.Devices.data['ind_measureR']

            self.coefR = 1
            if self.Devices.data['ind_measureR'] == 1:
                self.coefR = 1000           
           
            '''       
            if self.codeTypeTest == 3:
                self.ui.label.setText(u'Сопротивление, ' + nameMeasure + u' / коридор')            
            if self.codeTypeTest == 4:
                self.ui.label.setText(u'Сопротивление, ' + nameMeasure + u' / пред. исп.')
               ''' 
                            
            self.ui.label_14.setText(u'Сопротивление, ' + nameMeasure)
            if self.temperature == None:
                self.ui.label.setText(u't = 20°')
#                self.ui.label.setStyleSheet("background-color: red")            
                self.ui.label.setStyleSheet("color: red")            
            else:
                self.ui.label.setText(u't = ' + str(self.temperature) + u'°')
                self.ui.label.setStyleSheet("color: blue")            
                                                        
            if self.codeTypeTest == 3:
                self.ui.label_8.setText(u'Коридор')
                
            if self.codeTypeTest == 4:
                self.ui.label_8.setText(u'Пред. исп.')
                                            
        except Exception:
            pass


    def pushButton_3_Click(self):
        
        
        # print 111
        err = u"Ошибка удаления образца"
                
        if self.ui.pushButton_3.text() == u'Назначить':
            # print 222
            strSQL = """
select * 
from
(
select t1.id as idItem, t3.id as idCoil 
from item t1, serial_number t2, coil t3
where series = :series
and t1.id = :item
and t1.serial_number = t2.id
and t2.transformer = t3.transformer
) t1 LEFT OUTER JOIN (select item, coil, un, inom from checking_2 where stand = :stand) t2
ON (idItem =item and idCoil = coil)
where t2.inom is NULL
--where t2.un is NULL
"""
            # print 'strSQL = ', strSQL
            self.query_5.prepare(strSQL)
            self.query_5.bindValue(":series", self.series)
            self.query_5.bindValue(":item", self.idItem)
            self.query_5.bindValue(":stand", self.idStand)
            
            # print 'self.series, self.idItem, self.idStand = ', self.series, self.idItem, self.idStand
        
            if not self.query_5.exec_():
                QMessageBox.warning(None, u"Предупреждение", u"Ошибка работы с БД", QMessageBox.Ok)
                return None
            else:
                model_5.setQuery(self.query_5)
        
            if  model_5.rowCount() > 0:
                msgBox(self, u"Назначение данного трансформатора в качестве образца невозможно,\n поскольку он полностью не протестирован!")
                return
            
            err = u"Ошибка назначения образца"

#            print 'self.series, self.idItem, self.idStand = ', self.series, self.idItem, self.idStand
#            return





        '''
        st =  u"""Изменение статуса образца приведет к перерасчету
характеристик трансформаторов по всей серии.
Тем не менее, продолжить?"""
        if getTrue(self, st) == False:
            return            
           '''
                

        global id_defect
        self.codeTypeTest = 3    # УБРАТЬ
        
        # print 'self.codeTypeTest = ', self.codeTypeTest
        self.oDefects = Defects(self.env, self.codeTypeTest)
        self.oDefects.exec_()
        
        # print 'id_defect = ', id_defect
        #
        if id_defect == None:
            return
        
        




        '''
                
# ДИАЛОГ
                
                
        strSQL = """
SELECT * FROM checking_2
WHERE stand = :stand
AND item in
(
  SELECT t1.id FROM item t1, serial_number t2
  WHERE t1.serial_number = t2.id
  AND series = :series
  AND ordernumber = :ordernumber 
)
AND sample IS NOT NULL   
"""

        self.query_5.prepare(strSQL)            
        self.query_5.bindValue(":stand", self.idStand)
        self.query_5.bindValue(":series", self.series)
        self.query_5.bindValue(":ordernumber", self.ordernumber)        
        
        if not self.query_5.exec_():
            QMessageBox.warning(None, u"Предупреждение", err, QMessageBox.Ok)
            return
        else:
            model_5.setQuery(self.query_5)

        if model_5.rowCount() > 0:

            for i in range(model_5.rowCount()):
                print "model_5.record(i).field('un').value().toString() = " + model_5.record(i).field('un').value().toString()
                checking_2 = int(model_5.record(i).field('checking_2').value().toString())




# ДИАЛОГ   '''             
                
                
                
        '''                
        print 444
        strSQL = """
UPDATE checking_2 SET sample = NULL
WHERE stand = :stand
AND item in
(
  SELECT t1.id FROM item t1, serial_number t2
  WHERE t1.serial_number = t2.id
  AND series = :series
)   
"""            
        self.query_9.prepare(strSQL)            
        self.query_9.bindValue(":stand", self.idStand)
        self.query_9.bindValue(":series", self.series)
        '''
        
        
        strSQL = """
select distinct t1.item 
from checking_2 t1, item t2, serial_number t3
where t1.item = t2.id
and t2.serial_number = t3.id
and stand = :stand and series = :series and ordernumber = :ordernumber
and sample = true
"""        

        # print 'strSQL = ', strSQL
        self.query_5.prepare(strSQL)
        self.query_5.bindValue(":stand", self.idStand)
        self.query_5.bindValue(":series", self.series)
        self.query_5.bindValue(":ordernumber", self.ordernumber)
        
        if not self.query_5.exec_():
            QMessageBox.warning(None, u"Предупреждение", u"Ошибка работы с БД", QMessageBox.Ok)
            return None
        else:
            model_5.setQuery(self.query_5)
        
        if  model_5.rowCount() > 0:
            item = int(model_5.record(0).field('item').value())
            strSQL = """
UPDATE item SET defect = :defect
WHERE id = :item
"""            
            self.query_9.prepare(strSQL)            
            self.query_9.bindValue(":defect", id_defect)
            self.query_9.bindValue(":item", item)
                
            # print 'strSQL = ', strSQL
            if not self.query_9.exec_():
                QMessageBox.warning(None, u"Предупреждение", u"Ошибка работы с БД", QMessageBox.Ok)
                return None
                        
                
                
        # print 444
        strSQL = """
UPDATE checking_2 SET sample = NULL
WHERE stand = :stand
AND item in
(
  SELECT t1.id FROM item t1, serial_number t2
  WHERE t1.serial_number = t2.id
  AND series = :series
  AND ordernumber = :ordernumber 
)   
"""            
        self.query_9.prepare(strSQL)            
        self.query_9.bindValue(":stand", self.idStand)
        self.query_9.bindValue(":series", self.series)
        self.query_9.bindValue(":ordernumber", self.ordernumber)        
                
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение", err, QMessageBox.Ok)
            return
            
        if self.ui.pushButton_3.text() == u'Назначить':
            strSQL = """
UPDATE checking_2 SET sample = TRUE
WHERE stand = :stand
AND item = :item
"""            
            self.query_9.prepare(strSQL)            
            self.query_9.bindValue(":stand", self.idStand)
            self.query_9.bindValue(":item", self.idItemLast)
            if not self.query_9.exec_():
                QMessageBox.warning(None, u"Предупреждение", err, QMessageBox.Ok)
                return
        if self.recalcTesting():
            self.calcGlobal(self.oMap.iMapID, None, self.idStand, None, None, True)
            # print 'calcGlobal                     888888888888888888888888888888'
            msgBox(self, u"Перерасчет прошел успешно!")
        else:    
            msgBox(self, u"Перерасчет потерпел неудачу!")
                


    #20.06.2019
    def pushButton_5_Click(self):        
        if self.fRating2 == None and self.ui.lineEdit_3.text().trimmed() != '':
            st =  u"""Вы действительно намерены задать
коэффициент по всей серии
и произвести перерасчет?"""
        if self.fRating2 != None and self.ui.lineEdit_3.text().trimmed() != '':
            st =  u"""Вы действительно намерены изменить
заданный коэффициент по всей серии
и произвести перерасчет?"""
        if self.fRating2 != None and self.ui.lineEdit_3.text().trimmed() == '':
            st =  u"""Вы действительно намерены удалить
заданный коэффициент по всей серии
и произвести перерасчет?"""
        if getTrue(self, st) == False:
            return            

        try:
            rating2 = None
            if self.ui.lineEdit_3.text().trimmed() != '':
                rating2 = float(self.ui.lineEdit_3.text())
        except Exception:
            QMessageBox.warning(self, u"Предупреждение",  u'Величина заданного коэффициента не корректна', QMessageBox.Ok)
            return


        strSQL = """
UPDATE coil SET rating = :rating
WHERE id = :coil
"""            

        self.query_9.prepare(strSQL)            
        if rating2 == None:
            self.query_9.bindValue(":rating", None)
        else:                
            self.query_9.bindValue(":rating", str(rating2))
        self.query_9.bindValue(":item", self.idCoilLast)
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение", err, QMessageBox.Ok)
            return

        self.fRating2 = rating2
        self.ui.pushButton_5.setEnabled(False)        


        if self.recalcTesting():
            self.calcGlobal(self.oMap.iMapID, None, self.idStand, None, None, True)
            # print 'calcGlobal                     999999999999999999999999999999'
            msgBox(self, u"Перерасчет прошел успешно!")
        else:    
            msgBox(self, u"Перерасчет потерпел неудачу!")

        self.coil_after_change_row(self.idCoilLast, self.idItemLast, self.info)

    def change_lineEdit_3(self):
        self.ui.pushButton_5.setEnabled(True)        
        pass


    def calcCoil(self, coil, r, SecondCurrent, SecondLoad, points, typeCoil, ClassAccuracy, sample):
        # coil - код обмотки
        # r - сопротивление
        # SecondCurrent - вторичный ток
        # SecondLoad - вторичная нагрузка        
        # points - точки графика
        # typeCoil = 1  -  измерительная обмотка           
        # typeCoil = 2  -  защитная обмотка           
        #self.NSolut = None
        #sample - Образец

#        QMessageBox.warning(None, u"Точки", str(len(points)), QMessageBox.Ok)

#        QMessageBox.warning(None, u"r / self.coefR = ", str(r / self.coefR), QMessageBox.Ok) ###TAM

        nSolut = None
        #sK = [5, 10, 15]
        sI = [None, None, None]
        sU = [None, None, None]
        sPred = [None, None, None]
        if r == None:        
            return [nSolut, sI, sU, sPred]
                            
        if typeCoil == 1:                    
            kk = 0.1 * SecondCurrent            
            for i in range(self.nK):
                sI[i] = kk * self.sK[i]
                sPred[i] = self.calcU(SecondCurrent, r / self.coefR, self.sK[i], SecondLoad)
                sU[i] = self.calcU_(sI[i], points)              
            for i in range(self.nK):
                if sU[self.nK - 1 - i] != None and sU[self.nK - 1 - i] < sPred[self.nK - 1 - i]:
                    nSolut = self.nK - 1 - i
            # print 'nSolut1 = ', nSolut
            if nSolut == None:   # Нет правильного решения, пытаемся найти неправильное с минимальным коэффициентом
                for i in range(self.nK):
                    if sU[self.nK - 1 - i] != None:
                        nSolut = self.nK - 1 - i
                # print 'nSolut2 = ', nSolut
        else:
            #05.2019
            if self.codeTypeTest == 3:
                if ClassAccuracy == 1:
                    kk = 0.08 * SecondCurrent
                else:
                    kk = 0.04 * SecondCurrent
            if self.codeTypeTest == 4:
                if ClassAccuracy == 1:
                    kk = 0.1 * SecondCurrent
                else:
                    kk = 0.05 * SecondCurrent

            for i in range(self.nK):
                sU[i]  = self.calcU(SecondCurrent, r / self.coefR, self.sK[i], SecondLoad)
                sPred[i]  = kk * self.sK[i]
                sI[i]  = self.calcI(sU[i],  points)
                if sI[i] != None and sI[i] < sPred[i]:
                    nSolut = i
                # print 'nSolut3, sI[i] = ', nSolut, sI[i], sPred[i]
            if nSolut == None:   # Нет правильного решения, пытаемся найти неправильное с максмальным коэффициентом
                for i in range(self.nK):
                    if sI[i] != None:
                        nSolut = i
                # print 'nSolut4 = ', nSolut

        if sample != None:
            for i in range(self.nK):
                if sample['rating'] == self.sK[i]:
                    nSolut = i
        #     print 'nSolut5 = ', nSolut
        # print 'nSolut = ', nSolut
        # print 'sPred = ', sPred

        return [nSolut, sI, sU, sPred]


    def recalcTesting(self):
        # print 'recalcTesting'
        #Перерасчет по всей серии
        
        model_5.clear()
        
        strSQL = """
select t4.id as checking_2, item, coil, r, un, inom, k, t3.secondcurrent, t3.secondload,
       t3.rating as rating2, t3.classaccuracy
from item t1, serial_number t2, coil t3, checking_2 t4
where  t2.series = :series
and t2.ordernumber = :ordernumber 
and t1.serial_number = t2.id
and t2.transformer = t3.transformer
and t4.stand = :stand 
and t1.id = t4.item
and t3.id = t4.coil
order by coil, sample, t4.id
"""

#--and t2.ordernumber = :ordernumber 
        #
        # print 'qqq ' + strSQL
        # print self.series, self.idStand, self.ordernumber

        self.query_5.prepare(strSQL)
        self.query_5.bindValue(":series", self.series)
        self.query_5.bindValue(":ordernumber", self.ordernumber)
        self.query_5.bindValue(":stand", self.idStand)
        if not self.query_5.exec_():
            # print u'ошивка1'
#            raise Exception(self.query.lastError().text())
#            raise Exception(self.query_5.lastError().text())
#             print u'ошивка2'
            return None
        else:
            model_5.setQuery(self.query_5)

        # print 'www'



        coil = -1
        for i in range(model_5.rowCount()):
            # print "model_5.record(i).field('un').value().toString() = " + model_5.record(i).field('un').value().toString()
            checking_2 = int(model_5.record(i).field('checking_2').value())
            self.selectPoints(checking_2)
            if self.points == []:
                continue
            coil1 = int(model_5.record(i).field('coil').value())

            r    = float(model_5.record(i).field('r').value())
            secondcurrent = float(model_5.record(i).field('secondcurrent').value())
            secondload = float(model_5.record(i).field('secondload').value())
            classaccuracy = model_5.record(i).field('classaccuracy').value()
            rating2 = model_5.record(i).field('rating2').value()
            
            if coil != coil1:
                coil = coil1
                                
                classAccuracy = None    
                if str(classaccuracy).find('P') == -1:
                    typeCoil = 1
                else:    
                    typeCoil = 2
                    if str(classaccuracy).find('10P') != -1:
                        classAccuracy = 1
                    else:    
                        classAccuracy = 2                                
                                
                # Выясняем, есть ли номилальная кратность в таблице 'coil'            
                try:
                    fRating2 = float(rating2)
                except Exception:
                    fRating2 = None                                           
                                         
                self.sK[0] = 5
                self.nK = 3
                if fRating2 != None:
                    self.sK[0] = fRating2
                    self.nK = 1
        
                # print 'eee ', r, secondcurrent, secondload, self.points, typeCoil, classAccuracy
                                
                self.solut = self.calcCoil(None, r, secondcurrent, secondload, self.points, typeCoil, classAccuracy, None)
                if self.solut[0] == None:                
                    # print 'rrr '
                    return False
                # print 'ttt '
                n = self.solut[0]
                sample = {'id':  checking_2, 'r':  r, 'k': self.sK[n], 'rating':  self.sK[n], 'un': self.solut[2][n], 'in': self.solut[1][n], 'un2': self.solut[2][n], 'in2': self.solut[1][n]}
            else:
                    
                # print 'eee1 ', r, secondcurrent, secondload, self.points, typeCoil, classAccuracy
                
                self.solut = self.calcCoil(None, r, secondcurrent, secondload, self.points, typeCoil, classAccuracy, sample)
                if self.solut[0] == None:
                    # print 'rrr1 '
                    return False
                # print 'ttt1 '
                n = self.solut[0]
            # Сохранение Un, In, K в таблице
#            QMessageBox.warning(None, u"r / self.coefR = ", "update 111 " + str(self.solut[3][n]), QMessageBox.Ok)  ###TAM
            self.query_9.prepare('UPDATE checking_2 SET un=:un, un_=:un_, inom=:inom, k=:k, rating=:rating, su2=:su2, u2=:u2, i2=:i2, predel=:predel WHERE id=:id')            
            self.query_9.bindValue(":id", checking_2)
            self.query_9.bindValue(":un", self.solut[2][n])                
            self.query_9.bindValue(":un_", self.solut[2][n])                
            self.query_9.bindValue(":inom", self.solut[1][n])
            self.query_9.bindValue(":k", self.sK[n])
            self.query_9.bindValue(":rating", sample['rating'])                
            self.query_9.bindValue(":su2", self.solut[2][n])                
            self.query_9.bindValue(":u2", self.solut[2][n])                
            self.query_9.bindValue(":i2", self.solut[1][n])                
            self.query_9.bindValue(":predel", self.solut[3][n])                
            
            self.query_9.exec_()
            if self.query_9.lastError().isValid():
                QMessageBox.warning(None, u"Предупреждение", u"Ошибка сохранения в БД", QMessageBox.Ok)
                return None
                                    
        return True


    def checkBox_6_Click(self):        
        self.ui.pushButton_4.setEnabled(self.ui.checkBox_6.checkState())
        
        if self.isWork == False:
            self.ui.lineEdit.setEnabled(self.ui.checkBox_6.checkState())
                
        if self.ui.checkBox_6.isChecked():
            self.ui.lineEdit.setFocus()


# Вспомогательная функция к отчету: BAX_coil1
    def buildCoilsInfa(self, serial_number, LastTest, code):
        from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
        from PyQt5.QtWidgets import QMessageBox

        self.query = QSqlQuery(self.env.db)
        self.query_2 = QSqlQuery(self.env.db)
        model = QSqlQueryModel()
        model_2 = QSqlQueryModel()
        
        
        strSQL = """
select t1.id as checking_2, t1.item as itemID, t1.coil as coilID
, t3.coilnumber
, t3.tap
, 'И' || cast(t3.coilnumber as varchar ) || 'И' || cast(t3.tap as varchar )  as coil
, 1000 * t1.r as r            
, round(t1.un, 4) as un              
, round(t1.inom, 4) as inom                  
, t1.k
, t5.fio
, t2.createdatetime::date as sdate
from """ 

        if LastTest:
            print(86586954678)
            strSQL += """
checking_2 t1 RIGHT OUTER JOIN (select max(t2.id) as id from item t1, checking_2 t2, stand t3, test_type t4
where t1.id=t2.item and t2.stand = t3.id and t3.test_type = t4.id group by serial_number, coil, code) t1_
ON (t1.id = t1_.id),"""
        else:
            strSQL += """checking_2 t1,"""

        strSQL += """
item t2, coil t3,
test_map t4 LEFT OUTER JOIN operator t5 ON (t4.operator = t5.id),
stand t6, test_type t7
where t1.item = t2.id       
and t1.coil = t3.id
--and t1.stand = :stand
and t2.test_map = t4.id
and t1.stand = t6.id 
and t6.test_type = t7.id
--and t7.code = :code
and t7.code = """ + str(code) + """

--and t2.serial_number = :snID                                                                  
--and t2.serial_number = 110006                                                                  
and t2.serial_number = """ +  str(serial_number) + """                                                                  
order by t3.coilnumber                            
"""
                
        self.query.prepare(strSQL)
        print(331, strSQL)
        if not self.query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"ОООшибка выборки общих результатов испытания", QMessageBox.Ok)
        else:    
            model.setQuery(self.query)

        coils = []
        points = []
        coilsInfa = []
        for i in range(model.rowCount()):
            checking_2 = int(model.record(i).field('checking_2').value())
            coilID = int(model.record(i).field('coilID').value())
            coilnumber = str(model.record(i).field('coilnumber').value())
            tap = str(model.record(i).field('tap').value())
                
            coils +=  [[coilID,
                        float(model.record(i).field('r').value()),
                        float(model.record(i).field('un').value()),
                        float(model.record(i).field('inom').value()),
                        float(model.record(i).field('k').value())]]

            coilsInfa += [{}]
            coilsInfa[i]['coilnumber'] = int(model.record(i).field('coilnumber').value())
            coilsInfa[i]['coil'] = coilnumber + u'И1' + '-' + coilnumber + u'И' + tap 
            coilsInfa[i]['points'] = []
                                                
            strSQL = """
select a, v
from checking_2sp
where checking_2 = :checking_2
order by id"""

            self.query_2.prepare(strSQL)
            self.query_2.bindValue(":checking_2", checking_2)
            print(332, checking_2, 35,  strSQL)
            if not self.query_2.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
                break
            else:    
                model_2.setQuery(self.query_2)

            for j in range(model_2.rowCount()):
                points += [[coilID, 
                            float(model_2.record(j).field('a').value()),
                            float(model_2.record(j).field('v').value())]]
   
                coilsInfa[i]['points'] += [[float(model_2.record(j).field('a').value()),
                                            float(model_2.record(j).field('v').value())]]
   
        for i in range(len(coilsInfa)): 
            print(coilsInfa[i])
        print(666, coilsInfa)
        return coilsInfa


    def TestBase(self, db):
        query = QSqlQuery(db)
        # print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        query.prepare("select predel from checking_2")
        if not query.exec_(): err_tbl += "checking_2\n"
          
        if err_tbl != "":
            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД требуется произвести изменения,
необходимые для работы приложения\n""" +
u"Произвести изменения БД?", QMessageBox.Yes, QMessageBox.No)                        
                        
            if r == QMessageBox.Yes:
                self.InitBase(db)
                return True
            else:
                return False
        return True
                                 

    def InitBase(self, db):
        # print u"Инициализация БД"
        query = QSqlQuery(db)


        SQL = u"""
ALTER TABLE checking_2 ADD column predel numeric(16,10);
COMMENT ON COLUMN checking_2.predel IS 'Предельное значение напряжения для измерительных и тока для защитных обмоток';
"""

        if not query.exec_(SQL):
            # print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            # print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        return


        SQL = u"""
ALTER TABLE checking_2 ADD column Sample bool;
COMMENT ON COLUMN checking_2.Sample IS 'Является образцом или нет';
ALTER TABLE checking_2sp ALTER column a TYPE numeric(16,10);
ALTER TABLE checking_2sp ALTER column v TYPE numeric(16,10);
ALTER TABLE checking_2 ALTER column r TYPE numeric(16,10);
ALTER TABLE checking_2 ALTER column un TYPE numeric(16,10);
ALTER TABLE checking_2 ALTER column inom TYPE numeric(16,10);
ALTER TABLE checking_2 ALTER column k TYPE numeric(16,10);
"""
        if not query.exec_(SQL):
            # print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            # print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        return


        SQL = u"""
ALTER TABLE checking_2 ADD column Un numeric(8,4);
ALTER TABLE checking_2 ADD column Inom numeric(8,4);
ALTER TABLE checking_2 ADD column K numeric(8,4);
COMMENT ON COLUMN checking_2.Un IS 'Номинальное напряжение';
COMMENT ON COLUMN checking_2.Inom IS 'Номинальная сила тока';
COMMENT ON COLUMN checking_2.K IS 'Коэффициент';
"""
        if not query.exec_(SQL):
            # print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            # print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        return

        SQL = u"""
CREATE TABLE checking_2
(
  id serial PRIMARY KEY,
  stand integer REFERENCES stand,
  item integer REFERENCES item,
  coil integer REFERENCES coil,
  r numeric(8,4)
);

COMMENT ON TABLE checking_2 IS 'Результаты поверки обмоток трансформатора';
COMMENT ON COLUMN checking_2.id IS 'Первичный ключ';
COMMENT ON COLUMN checking_2.stand IS 'Ссылка на тип испытания';
COMMENT ON COLUMN checking_2.item IS 'Ссылка на изделие';
COMMENT ON COLUMN checking_2.coil IS 'Ссылка на испытываемую обмотку';
COMMENT ON COLUMN checking_2.r IS 'Сопротивление';

CREATE TABLE checking_2sp
(
  id serial NOT NULL,
  checking_2 integer REFERENCES checking_2,
  chektimestamp timestamp without time zone NOT NULL,
  a numeric(8,4),
  v numeric(8,4)
);

COMMENT ON TABLE checking_2sp IS 'Результаты поверки обмоток трансформатора';
COMMENT ON COLUMN checking_2sp.id IS 'Первичный ключ';
COMMENT ON COLUMN checking_2sp.checking_2 IS 'Ссылка на checking_2';
COMMENT ON COLUMN checking_2sp.chektimestamp IS 'Временная метка измерения';
COMMENT ON COLUMN checking_2sp.a IS 'Сила тока';
COMMENT ON COLUMN checking_2sp.v IS 'Напряжение';
"""

        if not query.exec_(SQL):
            # print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            # print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        return


    def checkBox_Click(self):
        self.ui.horizontalSlider.setVisible(self.ui.checkBox.checkState())
        self.ui.pushButton_2.setVisible(self.ui.checkBox.checkState())
        self.ui.checkBox_2.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_12.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_13.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_14.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_15.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_16.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_17.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_18.setVisible(self.ui.checkBox.checkState())
        self.ui.lineEdit_19.setVisible(self.ui.checkBox.checkState())
        self.ui.label_12.setVisible(self.ui.checkBox.checkState())
        self.ui.label_13.setVisible(self.ui.checkBox.checkState())
        self.checkBox_2_Click()
        
        
    def checkBox_2_Click(self):
        return
        self.ui.label_12.setVisible(self.ui.checkBox_2.checkState())
        self.ui.label_13.setVisible(self.ui.checkBox_2.checkState())
        self.ui.lineEdit_12.setVisible(self.ui.checkBox_2.checkState())
        self.ui.lineEdit_13.setVisible(self.ui.checkBox_2.checkState())


class Defects(QDialog, UILoader):

    def __init__(self, env, codeTypeTest):
        import JournalMsr
        super(QWidget, self).__init__()
        global id_defect
        id_defect = None
        global db1
        db1 = env.db        
        global path_ui

        super(QWidget, self).__init__()
                
        self.setUI(env.config, u"DEfects.ui")        
        
        self.ui.tableView.setModel(model)
        self.selModel = self.ui.tableView.selectionModel()                

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')

        SQL = '''
select id, fullname from defect    
where id in 
(
    select defect from defect_test_type where test_type in 
    (
        select id from test_type where code = ''' + str(codeTypeTest) + '''
    )
)        
'''

        query = QSqlQuery(db1)
        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
        model.setQuery(query)
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Несоответствие")
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_Click)

    def pushButton_Click(self):
#            self.wind.ui.lineEdit.setText(model.record(row).field('family').value().toString())        
        global id_defect
        row = self.selModel.currentIndex().row()
        self.ui.label.setText(model.record(row).field('fullname').value())
        id_defect = model.record(row).field('id').value()
        self.close()
        return

    def pushButton2_Click(self):
        self.close()
        return


                
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    from dpframe.base.inits import db_connection_init   
    from dpframe.base.envapp import checkenv
    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import db_connection_init
    from dpframe.base.inits import default_log_init
    from electrolab.gui.inits import serial_devices_init
   
    
    @serial_devices_init
    @json_config_init
    @db_connection_init
    @default_log_init    
    class ForEnv(QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
    db = env.db
    path_ui = env.config.paths.ui + "/"

    import os
    if not os.path.exists(path_ui):        
        path_ui = ""

    rez = db.open();
    if not rez:
        QMessageBox.warning(None, u"Предупреждение",
u"""Не установлено соединение с БД со следующими параметрами:
host: """ + db.hostName() + """
database: """ + db.databaseName() + """
user: """ + db.userName() + """
password: """ + db.password(),
QMessageBox.Ok)
                
    else:
        points = [[1,2],[3,4],[5,6]]                
        points1 = [[0.1,0.2],[0.3,0.4],[0.5,0.6]]
                                
        wind = TestCoil(env, None, None, None, None, None)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())


