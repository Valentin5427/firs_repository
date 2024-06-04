# -*- coding: UTF-8 -*-work
#
'''
Created on 16.10.2017

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
from Warming_setup import Warming_setup

import time
import datetime

model = QSqlQueryModel()

PAUSE = u'PAUSE'
WORK = u'WORK'
stateWork = PAUSE

threadBreak = False
###endReadDevice = False        

ENV = None
DEV = None
W_s = None

points = None
points_2 = None
dTime = 60
begin_time = 0

Vals = [0,0,0,0,0,0,0,0]

def time_sec():
    # Время с начала суток в секундах
    t = time.localtime()
    return 3600 * t[3] + 60 * t[4] + t[5] + time.time() % 1

def sec_to_time(sec):
    # Перевод секунд в часы, минуты, секунды (hh:mm:ss)
    pass
    h = sec // 3600
    ost = sec % 3600
    m = ost // 60
    s = ost % 60
    return h, m, s


class MyThread(QtCore.QThread):
        def __init__(self, parent = None):
            QtCore.QThread.__init__(self, parent)
                        
            global ENV, DEV, W_s, Vals
            DEV = Devices(ENV)

        def run(self):
            global points, points_2
            global threadBreak
            global dTime
            global begin_time
                        
            threadBreak = False

            points = []                      
            points_2 = []                      
            Time = 0
                        
            for i in range(1000000):
                try:
                    DEV.port.close()
                    DEV.port.open()
                except SerialException:
                    self.emit(QtCore.SIGNAL('errorport'))
                    return                            
                except Exception:
                    self.emit(QtCore.SIGNAL('errorport'))
                    return
                                                
                try:                    
                    if i == 0:
                        begin_time = time_sec()            
                    if time_sec() >= begin_time + Time:
                        st = '#GOHGROTVLLSJ'+chr(0x0d) #Команда правильная
                        Val = DEV.ReadDevice(DEV.port, 2, st)                    
                        temper = float(Val)
                        points += [[Time, temper]]
                                                
                        DEV.port.close()
                        DEV.port.open()
                        st = '#GPHGROTVMVJT'+chr(0x0d) #Команда правильная
                        Val_2 = DEV.ReadDevice(DEV.port, 2, st)                    
                        temper_2 = float(Val_2)                    
                        points_2 += [[Time, temper_2]]
                                                
                        self.emit(QtCore.SIGNAL('bieldscene'))
                        Time += dTime
                        self.msleep(100)
                        if threadBreak:
                            DEV.port.close()
                            return
                    
                    for j in range(4):
                        # Чтение вольтметров
                        DEV.port.close()
                        DEV.port.open()
                        type = W_s.TypesV[j].currentIndex()
                        if type == 0:
                            st = chr(W_s.AddressV[j].value())+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
                        if type == 1:
                            st = chr(W_s.AddressV[j].value())+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
                        st += chr(crc16(st)[0]) + chr(crc16(st)[1])
                        Vals[j] = DEV.ReadDevice(DEV.port, type, st)
                        self.emit(QtCore.SIGNAL('printVAP'))
                        self.msleep(100)
                        if threadBreak:
                            DEV.port.close()
                            return

                        # Чтение амперметров
                        DEV.port.close()
                        DEV.port.open()
                        type = W_s.TypesA[j].currentIndex()
                        if type == 0:
                            st = chr(W_s.AddressA[j].value())+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
                        if type == 1:
                            st = chr(W_s.AddressA[j].value())+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
                        st += chr(crc16(st)[0]) + chr(crc16(st)[1])
                        Vals[j + 4] = DEV.ReadDevice(DEV.port, type, st)
                        self.emit(QtCore.SIGNAL('printVAP'))
                        self.msleep(100)
                        if threadBreak:
                            DEV.port.close()
                            return
                except SerialException:
                    self.emit(QtCore.SIGNAL('errordevice'))
                    return                            
                except Exception:
                    self.emit(QtCore.SIGNAL('errordevice'))
                    return
                        


class Warming(QWidget, UILoader):    
#    def __init__(self, _env, oMap, tvItem, tvCoil, btnStart, VerificationForm):
    def __init__(self, _env):
        
        global ENV, W_s
        ENV = _env        
        
        super(QWidget, self).__init__()

        self.setUI(_env.config, u"Warming.ui")                
        self.query = QSqlQuery(_env.db)
        self.port = Serial()
        self.Devices = Devices(_env)

        self.pen = QtGui.QPen()        
        self.pen_2 = QtGui.QPen()        
        self.epsilon = 0.0000001
        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.setSceneRect(0, 0, 1, 1)
        self.ui.graphicsView.setScene(self.graphicsScene)        
        self.ui.spinBox.setValue(datetime.datetime.now().year - 2000) 
        self.ui.spinBox_2.setFocus(True)
                
        self.ui.doubleSpinBox.clear()
        self.ui.doubleSpinBox_2.clear()
        self.ui.doubleSpinBox_3.clear()
        self.ui.doubleSpinBox_4.clear()
        self.ui.doubleSpinBox_5.clear()
        self.ui.doubleSpinBox_6.clear()
        self.ui.doubleSpinBox_7.clear()
        self.ui.doubleSpinBox_8.clear()
        self.ui.doubleSpinBox_9.clear()
        self.ui.doubleSpinBox_10.clear()
        self.ui.doubleSpinBox_11.clear()
        self.ui.doubleSpinBox_12.clear()
        self.ui.doubleSpinBox_13.clear()
        self.ui.doubleSpinBox_14.clear()
        self.ui.doubleSpinBox_15.clear()
        self.ui.doubleSpinBox_16.clear()
        self.ui.doubleSpinBox_17.clear()
        self.ui.doubleSpinBox_18.clear()
        self.ui.doubleSpinBox_19.clear()
        self.ui.doubleSpinBox_20.clear()
        self.ui.doubleSpinBox_21.clear()
        self.ui.doubleSpinBox_22.clear()
        self.ui.doubleSpinBox_23.clear()
        self.ui.doubleSpinBox_24.clear()
        self.ui.doubleSpinBox_25.clear()
        self.ui.doubleSpinBox_26.clear()
        self.ui.doubleSpinBox_27.clear()
        self.ui.doubleSpinBox_28.clear()
        self.ui.doubleSpinBox_29.clear()
        self.ui.doubleSpinBox_30.clear()
        self.ui.doubleSpinBox_31.clear()
        self.ui.doubleSpinBox_32.clear()
        self.ui.doubleSpinBox_33.clear()
        self.ui.doubleSpinBox_34.clear()
        self.ui.doubleSpinBox_35.clear()
        self.ui.doubleSpinBox_36.clear()
        
        self.ui.spinBox_2.clear()

        self.ui.lineEdit_2.setStyleSheet("color: red")
        self.ui.lineEdit_3.setStyleSheet("color: red")
        self.ui.lineEdit_4.setStyleSheet("color: green")
        self.ui.lineEdit_5.setStyleSheet("color: green")

        self.ui.pushButton_5.setVisible(False)
        self.ui.pushButton_2.setDisabled(True)

        self.ui.spinBox.valueChanged.connect(self.spinBox_Change)
        self.ui.spinBox_2.valueChanged.connect(self.spinBox_Change)
        self.ui.doubleSpinBox.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.doubleSpinBox_Change)

        self.ui.doubleSpinBox_9.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_10.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_11.valueChanged.connect(self.doubleSpinBox_Change)

        self.ui.doubleSpinBox_5.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_6.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_7.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_8.valueChanged.connect(self.doubleSpinBox_Change)

        self.ui.doubleSpinBox_13.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_14.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_15.valueChanged.connect(self.doubleSpinBox_Change)
        self.ui.doubleSpinBox_16.valueChanged.connect(self.doubleSpinBox_Change)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.tabWidget.currentChanged.connect(self.resizeEvent)
        
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click) #временно

        self.thread = MyThread()     
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.connect(self.thread, QtCore.SIGNAL("started()"), self.on_started, QtCore.Qt.QueuedConnection)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.on_finished, QtCore.Qt.QueuedConnection)
        self.connect(self.thread, QtCore.SIGNAL("errorport"), self.on_errorport, QtCore.Qt.QueuedConnection)
        self.connect(self.thread, QtCore.SIGNAL("errordevice"), self.on_errordevice, QtCore.Qt.QueuedConnection)
        self.connect(self.thread, QtCore.SIGNAL("bieldscene"), self.on_bieldscene, QtCore.Qt.QueuedConnection)
        self.connect(self.thread, QtCore.SIGNAL("printVAP"), self.on_printVAP, QtCore.Qt.QueuedConnection)

        W_s = Warming_setup(_env)
        global dTime
        dTime = W_s.ui.doubleSpinBox.value() * 60

    def on_errorport(self):
        print('Обработан пользовательский сигнал on_errorport')                
        msgBox(self, u"Сбой COM-порта!\nЗапустите поверку заново.!")
        self.pushButton_2_Click()

    def on_errordevice(self):
        print('Обработан пользовательский сигнал on_errordevice')                
        msgBox(self, u"Ошибка чтения прибора!\nЗапустите поверку заново.!")
        self.pushButton_2_Click()

    def on_bieldscene(self):
        global points, points_2
        print('Обработан пользовательский сигнал on_bieldscene')                
        #Расчет приращения температуры
        self.ui.lineEdit_3.setText('')
        self.ui.lineEdit_5.setText('')
        dt = 3600
#        dt = 12
        l = len(points)
        if (l - 1) * dTime >= dt:
            ln = int(dt // dTime)
            self.ui.lineEdit_3.setText(str(round(points[l-1][1] - points[l-ln-1][1], 3)))
            self.ui.lineEdit_5.setText(str(round(points_2[l-1][1] - points_2[l-ln-1][1], 3)))
                
        #Построение графика        
        self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), points, points_2, 1)


    def on_printVAP(self):     
        global Vals
        
        v = [0,0,0,0,0,0,0,0]
        try:
            for i in range(8):            
                if Vals[i] != None:
                    v[i] = float(Vals[i])
                    if i < 4:
                        if W_s.MeasuresV[i].currentIndex() == 1:
                            v[i] /= 1000
                        if W_s.MeasuresV[i].currentIndex() == 2:
                            v[i] *= 1000
                    else:        
                        if W_s.MeasuresA[i-4].currentIndex() == 1:
                            v[i] /= 1000
                        if W_s.MeasuresA[i-4].currentIndex() == 2:
                            v[i] *= 1000
                    
            self.ui.doubleSpinBox_25.setValue(v[0])
            self.ui.doubleSpinBox_29.setValue(v[4])
            self.ui.doubleSpinBox_33.setValue(v[0] * v[4])
                
            self.ui.doubleSpinBox_26.setValue(v[1])
            self.ui.doubleSpinBox_30.setValue(v[5])
            self.ui.doubleSpinBox_34.setValue(v[1] * v[5])
                
            self.ui.doubleSpinBox_27.setValue(v[2])
            self.ui.doubleSpinBox_31.setValue(v[6])
            self.ui.doubleSpinBox_35.setValue(v[2] * v[6])
                
            self.ui.doubleSpinBox_28.setValue(v[3])
            self.ui.doubleSpinBox_32.setValue(v[7])
            self.ui.doubleSpinBox_36.setValue(v[3] * v[7])                
        except Exception:
            pass        

    
    def pushButton_5_Click(self):        
        global DEV, ENV
        DEV = Devices(ENV)
        
        for i in range(4):
            DEV.port.close()
            DEV.port.open()
            type = self.Warming_setup.TypesV[i].currentIndex()
            if type == 0:
                st = chr(self.Warming_setup.AddressV[i].value())+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if type == 1:
                st = chr(self.Warming_setup.AddressV[i].value())+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])
            Val = DEV.ReadDevice(DEV.port, type, st)
                    
        
    def pushButton_7_Click(self):
        self.testExcel()
    
    def calcTempers(self):    
        self.Kcopper = 235.
        self.Tb   = self.ui.doubleSpinBox_4.value()
        self.Te   = self.ui.doubleSpinBox_12.value()
        self.Rb   = self.ui.doubleSpinBox_5.value()
        self.Rb_2 = self.ui.doubleSpinBox_6.value()
        self.Rb_3 = self.ui.doubleSpinBox_7.value()
        self.Rb_4 = self.ui.doubleSpinBox_8.value()
        self.Re   = self.ui.doubleSpinBox_13.value()
        self.Re_2 = self.ui.doubleSpinBox_14.value()
        self.Re_3 = self.ui.doubleSpinBox_15.value()
        self.Re_4 = self.ui.doubleSpinBox_16.value()
        rez = self.calcTemper(self.Tb, self.Te, self.Rb, self.Re, self.Kcopper)
        self.ui.doubleSpinBox_17.setValue(rez[0])
        self.ui.doubleSpinBox_21.setValue(rez[1])
        rez = self.calcTemper(self.Tb, self.Te, self.Rb_2, self.Re_2, self.Kcopper)
        self.ui.doubleSpinBox_18.setValue(rez[0])
        self.ui.doubleSpinBox_22.setValue(rez[1])
        rez = self.calcTemper(self.Tb, self.Te, self.Rb_3, self.Re_3, self.Kcopper)
        self.ui.doubleSpinBox_19.setValue(rez[0])
        self.ui.doubleSpinBox_23.setValue(rez[1])
        rez = self.calcTemper(self.Tb, self.Te, self.Rb_4, self.Re_4, self.Kcopper)
        self.ui.doubleSpinBox_20.setValue(rez[0])
        self.ui.doubleSpinBox_24.setValue(rez[1])
    
    def calcTemper(self, Tb, Te, Rb, Re, K):
        if Rb < self.epsilon:
            return (0, 0)    
        Tr = (K + Tb) * Re / Rb - K
        dT = Tr - Te
        return (Tr, dT)


    def on_started(self):
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_2.setDisabled(False)
        self.ui.pushButton_3.setDisabled(True)
        self.ui.pushButton_4.setDisabled(True)
        self.ui.pushButton_7.setDisabled(True)
       
    def on_finished(self):
        self.ui.pushButton.setDisabled(False)
        self.ui.pushButton_2.setDisabled(True)
        self.ui.pushButton_3.setDisabled(False)
        self.ui.pushButton_4.setDisabled(False)
        self.ui.pushButton_7.setDisabled(False)
        

    def spinBox_Change(self):        
        model.clear()
        
        strSQL = """
select fullname
from serial_number t1, transformer t2
where t1.transformer = t2.id
and makedate = :makedate
and serialnumber = :serialnumber 
"""
        self.query.prepare(strSQL)
        self.query.bindValue("makedate", self.ui.spinBox.value())
        self.query.bindValue("serialnumber", self.ui.spinBox_2.value())
        if not self.query.exec_():
            print 'error'
            raise Exception(self.query.lastError().text())
        else:    
            model.setQuery(self.query)
        if model.rowCount() < 1:
            self.ui.lineEdit.setText('')
        else:
            self.ui.lineEdit.setText(model.record(0).field('fullname').value().toString())
            self.ui.lineEdit.setCursorPosition(0)


    def doubleSpinBox_Change(self):
        self.ui.doubleSpinBox_4.setValue((self.ui.doubleSpinBox.value() + self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox_3.value()) / 3)        
        self.ui.doubleSpinBox_12.setValue((self.ui.doubleSpinBox_9.value() + self.ui.doubleSpinBox_10.value() + self.ui.doubleSpinBox_11.value()) / 3)        
        self.calcTempers()


    def testExcel(self):
        from win32com.client import Dispatch, constants
        global wb, xl
        
        try:
            try:
                xl = Dispatch('Excel.Application')
            except:
                print ("Не запускается Excel")
                return 
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            

            ws.PageSetup.Orientation = 2
            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42

            ws.Cells(1, 1).ColumnWidth = 25            
            ws.Cells(1, 2).ColumnWidth = 10            
            ws.Cells(1, 3).ColumnWidth = 10            
            ws.Cells(1, 4).ColumnWidth = 10            
            ws.Cells(1, 5).ColumnWidth = 10            
            ws.Cells(1, 6).ColumnWidth = 10            
            ws.Cells(1, 7).ColumnWidth = 10            
            ws.Cells(1, 8).ColumnWidth = 10            
            ws.Cells(1, 9).ColumnWidth = 10            
            
            ws.Range('A1:I1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()

            xl.Selection.Font.Size = 16
            xl.Selection.Value = u'Результаты испытания трансформатора на нагрев'

            ws.Range('A3').Select()
            xl.Selection.HorizontalAlignment = 4
            xl.Selection.Merge()            
            xl.Selection.Value = u'Наименование изделия:'
            ws.Range('B3').Select()
            xl.Selection.Font.Size = 12
            xl.Selection.Value = unicode(self.ui.lineEdit.text())
            
            ws.Range('A4').Select()
            xl.Selection.HorizontalAlignment = 4
            xl.Selection.Merge()            
            xl.Selection.Value = u'Заводской номер:'
            ws.Range('B4').Select()
            xl.Selection.Font.Size = 12
            xl.Selection.Value = str(self.ui.spinBox.value()) + '-' + str(self.ui.spinBox_2.value())
                        
            now = datetime.datetime.now()
            ws.Range('A5').Select()
            xl.Selection.HorizontalAlignment = 4
            xl.Selection.Merge()            
            xl.Selection.Value = u'Дата испытания:'
            ws.Range('B5').Select()
            xl.Selection.Font.Size = 12
            xl.Selection.Value = now.strftime('%d.%m.%Y')

            ws.Range("A7:I10").Select()
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.Font.Size = 12
            xl.Selection.WrapText = True
            xl.Selection.VerticalAlignment = 4

            ws.Cells(8,  1).RowHeight = 30            
            ws.Cells(9,  1).RowHeight = 30            
            ws.Cells(10, 1).RowHeight = 30            

            ws.Cells(8, 1).Value = u'В холодном состоянии'            
            ws.Range('A9').Select()
            xl.Selection.Value = u'В конце испытания'
            ws.Range('A10').Select()
            xl.Selection.Value = unicode(u'ΔT,°С при Токр в конце испытания, ') + str(self.ui.doubleSpinBox_12.value()) + unicode(u'°С')

            ws.Range('B7').Select()
            xl.Selection.Value = u'R AX, Ом'
            ws.Range('C7').Select()
            xl.Selection.Value = u'T AX, °C'
            ws.Range('D7').Select()
            xl.Selection.Value = u'R a1x1, Ом'
            ws.Range('E7').Select()
            xl.Selection.Value = u'T a1x1, °C'
            ws.Range('F7').Select()
            xl.Selection.Value = u'R a2x2, Ом'
            ws.Range('G7').Select()
            xl.Selection.Value = u'T a2x2, °C'
            ws.Range('H7').Select()
            xl.Selection.Value = u'R adxd, Ом'
            ws.Range('I7').Select()
            xl.Selection.Value = u'T adxd, °C'

            ws.Range('B8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_5.value())
            ws.Range('C8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_4.value())
            ws.Range('D8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_6.value())
            ws.Range('E8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_4.value())
            ws.Range('F8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_7.value())
            ws.Range('G8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_4.value())
            ws.Range('H8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_8.value())
            ws.Range('I8').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_4.value())
            
            ws.Range('B9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_13.value())
            ws.Range('C9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_17.value())
            ws.Range('D9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_14.value())
            ws.Range('E9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_18.value())
            ws.Range('F9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_15.value())
            ws.Range('G9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_19.value())
            ws.Range('H9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_16.value())
            ws.Range('I9').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_20.value())
            
            ws.Range('C10').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_21.value())
            ws.Range('E10').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_22.value())
            ws.Range('G10').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_23.value())
            ws.Range('I10').Select()
            xl.Selection.Value = str(self.ui.doubleSpinBox_24.value())
#  https://bytes.com/topic/python/answers/523907-creating-charts-excel-pyexcelerator-excelmagic

        except:
            print "Неопознанная ошибка4 ... "  
        

    def BieldScene(self, scene, width, height, points, points_2, mode):
        # mode = 1 - виден график целиком
        # mode = 2 - виден график до правой линии коридора
                        
        global begin_time 
        scene.clear()
        
        self.nomVoltage = None
        all_points = points + points_2
        if len(all_points) < 1:
            return

        maxX = all_points[0][0]
        maxY = all_points[0][1]
        for i in range(len(all_points)):
            if all_points[i][0] > maxX:
                maxX = all_points[i][0]
            if all_points[i][1] > maxY:
                maxY = all_points[i][1]
                                
        smXl = round(0.1 * width)
        smXr = round(0.05 * width)
        smYt = round(0.1 * height)
        smYb = round(0.1 * height)
        
        smXl = round(0.05 * width)
        smXr = round(0.05 * width)
        smYt = round(0.15 * height)
        smYb = round(0.15 * height)
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
        self.pen_2.setColor(QtCore.Qt.black)
                      
        scene.addLine(smXl, smYt, smXl, vH - smYb, self.pen)
        scene.addLine(smXl, vH - smYb, vW - smXr, vH - smYb, self.pen)

        # Подписи осей
        #24.05.2016
        fnt =  QFont()
        fnt.setPixelSize(14)
        t1 = scene.addText(u'время, t, час', fnt)            
        t1.setPos(vW - 100, vH - smYb + 10)
        t1 = scene.addText(u'температура, T, °C', fnt)            
        t1.setPos(10, 2)
        
        self.pen.setWidth(1)
        ss = self.signScale(maxX)
        if len(ss) != 1:
            ss = [0] + ss
        for i in range(len(ss)):
            self.pen.setColor(QtCore.Qt.gray)
            scene.addLine(smXl + round(ss[i] / kX), vH - smYb, smXl + round(ss[i] / kX), smYt, self.pen)
            t = sec_to_time(int(begin_time + ss[i]))
            t1 = scene.addText( str(t[0]) + ':' + str(t[1]) + ':' + str(t[2]) )            
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


        self.pen.setWidth(2)
        self.pen_2.setWidth(1)
        # Кривая текущего испытания
        self.pen.setColor(QtCore.Qt.black)
                
        self.pen.setColor(QtCore.Qt.red)
        for i in range(len(points)):
            x1 = smXl + round(points[i][0]/kX)
            y1 = vH - smYt - round(points[i][1]/kY)
            if i == 0:
                scene.addEllipse(x1-2, y1-2, 4, 4, self.pen)
            if i < len(points) - 1:
                x2 = smXl + round(points[i+1][0]/kX)
                y2 = vH - smYt - round(points[i+1][1]/kY)
                scene.addLine(x1, y1, x2, y2, self.pen)
                scene.addEllipse(x2-2, y2-2, 4, 4, self.pen)

        self.pen.setColor(QtCore.Qt.green)
        for i in range(len(points_2)):
            x1 = smXl + round(points_2[i][0]/kX)
            y1 = vH - smYt - round(points_2[i][1]/kY)
            if i == 0:
                scene.addEllipse(x1-2, y1-2, 4, 4, self.pen)
            if i < len(points_2) - 1:
                x2 = smXl + round(points_2[i+1][0]/kX)
                y2 = vH - smYt - round(points_2[i+1][1]/kY)
                scene.addLine(x1, y1, x2, y2, self.pen)
                scene.addEllipse(x2-2, y2-2, 4, 4, self.pen)


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


    def resizeEvent(self, event):
        global points
        if points != None: 
            self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), points, [], 1)

    def pushButton_Click(self):        
        self.thread.start()
        
    def pushButton_2_Click(self):
        global threadBreak
        threadBreak = True
          
    def pushButton_3_Click(self):
        global W_s, dTime
        W_s = Warming_setup(env)
        W_s.setEnabled(True)
        W_s.exec_()
        dTime = W_s.ui.doubleSpinBox.value() * 60

    def pushButton_4_Click(self):
        try:
            global wb, xl
            wb.Close(False)
            xl.Visible = 0
        except:
            pass    
        self.close()

    def work(self):        
        self.tread.start()
        return
                            
    def pause(self):
        self.isWork = False 
        self.testEnabled(False)
    
        global stateWork        
        self.wasHand = self.isHand
        if True:                
            stateWork = PAUSE
            self.tread.quit()   # А надо ли?
                                
        self.isHand = True   


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
                            
    wind = Warming(env)
    wind.setEnabled(True)
    wind.show()
    sys.exit(app.exec_())
