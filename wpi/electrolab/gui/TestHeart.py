﻿#coding=UTF-8
'''
Created on 16.08.2013

@author: atol
'''

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMessageBox, QIcon
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
import os
from dpframe.base.inits import json_config_init
import JournalMsr

from matplotlib import pyplot, rc
from devices import Devices

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from HeartSettings import HeartSettings


import threading
import time
from serial import Serial
from serial.serialutil import SerialException
#from Parabola import *
from numpy import *
import ReportsExcel
import json
import ui.ico_64_rc1

import binhex
import binascii
import struct



isTestHeart = False
model = QtGui.QStandardItemModel()
model2 = QSqlQueryModel()
model3 = QSqlQueryModel()
#query2 = QSqlQuery()
query2 = None


global port
port = Serial()
        
        
# временная переменная для эмуляции компорта
iReadPort = 0


nComError = 0   #колич. сбоев com-порта происходящих подряд        
wasTestRez = False  #была произведена проверка результата тестирования

delay = 0.0

#isReadPort = False                                 


# Перенести со временем в DPFrame
# Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
def searchInModel(id_search, tableView, model):
    if id_search == -1:  # При удалении записи
        return
    if id_search == 0:
        if tableView.size() > 0:   # Грубая защита от ошибки позиционирования
            tableView.selectRow(0)
    else:
        if model.query().size() < 1:  # Грубая защита от зацикливания
            return
        # Навигация на измененную позицию
        model.query().first();
        i = 0
        while model.query().value(0).toString() != id_search:
            if i >= model.rowCount() - 1:
                break            
            model.query().next()
            i += 1
        tableView.selectRow(i)

class MyFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
    def eventFilter(self, obj, e):
       # print 'EVENT'
        return True


class MyThread(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        
        global isTestHeart, wasTestRez, nComError, AV, dalay
        self.nPoint = 0

        while isTestHeart:
            
            global isReadPort
            isReadPort = False                        
            self.emit(QtCore.SIGNAL('treadsignal'))
            while not isReadPort:
                time.sleep(0.001)
                pass    
            if AV == None:
                if not isTestHeart:
                    return
                nComError += 1
                time.sleep(0.1)
                                
                self.emit(QtCore.SIGNAL('mysignal1'))
                time.sleep(0.01)
                                
                if nComError < 10 or wasTestRez:
                    continue
                else:
                    nComError = 0
                    
                    self.emit(QtCore.SIGNAL('mysignal2'))
                    time.sleep(0.01)
                    wind.on_clicked2()
                    time.sleep(0.01)
                    return
                                
            nComError = 0
                        
            #global isReadPort
            isReadPort = False                        
            self.emit(QtCore.SIGNAL('mysignal3'))
            while not isReadPort:
                time.sleep(0.01)
                pass    
             
            time.sleep(delay) # вроде как не нужна но без этой задержки проскакивают ошибочки чтения компорта


# Округление до n значащих цифр
def nRound(x, n):
    x_ = abs(x)
    if x_ == 0:
        return 0
    i = 0
    while x_ >= pow(10, n):
        x_ /= 10.
        i += 1
    while x_ < pow(10, n - 1):
        x_ *= 10.
        i -= 1
    return round(x_, 0) * pow(10, i)
            

class win(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
 
#        QMessageBox.warning(None, u"Предупреждение", u"1", QMessageBox.Ok)

        self.MSamplePoints = []
        self.points = []
        
        self.is_show = True 
        if not self.TestBase():
            self.is_show = False 

        global data
        global path_ui
        global delay
        path_ui = env.config.paths.ui + "/"
        if not os.path.exists(path_ui):        
            path_ui = ""
        if not JournalMsr.MyLoadUi(path_ui, "testHeart.ui", self):
            self.is_show = False
            return
#        QMessageBox.warning(None, u"Предупреждение", u"2", QMessageBox.Ok)


        self.pushButton.setIcon(QIcon(u':/ico/ico/book_green.png'))


        self.pushButton.clicked.connect(self.on_clicked1)
        self.pushButton_2.clicked.connect(self.on_clicked2)
        self.pushButton_3.clicked.connect(self.on_clicked3)
        self.pushButton_4.clicked.connect(self.on_clicked4)
     

        fnt = QtGui.QFont()
        fnt.setPointSize(16)
                
        self.mnu = QtGui.QMenu(u'Удалить образец')
        self.action_7.font().setPointSize(14)
        self.mnu.setFont(fnt)
        self.menu_4.addMenu(self.mnu)
                
        self.connect(self.action_6, QtCore.SIGNAL('triggered()'), self.on_clicked3)
        self.connect(self.action_7, QtCore.SIGNAL('triggered()'), self.on_action7)
        self.connect(self.action_8, QtCore.SIGNAL('triggered()'), self.on_action8)
        self.connect(self.action, QtCore.SIGNAL('triggered()'), self.on_clicked1)
        self.connect(self.action_3, QtCore.SIGNAL('triggered()'), self.on_clicked6)
        self.connect(self.action_4, QtCore.SIGNAL('triggered()'), self.on_clicked7)
        self.connect(self.action_5, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        #self.connect(self.action_9, QtCore.SIGNAL('triggered()'), self.setConfig)

        self.connect(self, QtCore.SIGNAL('mysignal1'), self.on_mysignal1)
        self.connect(self, QtCore.SIGNAL('mysignal2'), self.on_mysignal2)
        self.connect(self, QtCore.SIGNAL('mysignal3'), self.on_mysignal3)
        
        self.errStr = ''

        self.nPoint = 0

        self.tableView.setModel(model)
        self.tableView.verticalHeader().hide()       
        self.tableView.horizontalHeader().hide()       
        
        model.appendRow([None, None, None])
        
        model.removeRow(0)       
                
        self.tableView_2.setModel(model2)
        self.selModel2 = self.tableView_2.selectionModel()        
        self.connect(self.selModel2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged2)

        self.ALess = False # Сила тока меньше минимальной для снятия показаний
        self.ABack = False # Сила тока поползла назад

        self.workAmp = None
        self.workVolt = None
       
       # 15.04
        self.MinAmp = 0.0000001 
       
        #2019
        self.Devices = Devices(env)

        from HeartSettings import HeartSettings
        #04.2019
        #wind = HeartSettings(env, 1, 1)
        wind = HeartSettings(env)
        
        #2019
#        wind.comboBox.addItems(self.Devices.sTypes)
#        self.Types += [QtGui.QComboBox()]
#        self.Types[i].addItems(self.sTypes)
#        self.Types[i].setCurrentIndex(ind_type)
        
        '''
        #04.2019
        # Установка параметров по умолчанию
        self.indAmp = wind.comboBox.currentIndex()
        self.indVolt = wind.comboBox_2.currentIndex()
        #2019
        self.indMeasureA = wind.comboBox_3.currentIndex()
        self.indMeasureV = wind.comboBox_4.currentIndex()
        self.adressA = wind.spinBox_3.value()
        self.adressV = wind.spinBox_4.value()
                
        self.MinAmp = float(wind.lineEdit.text())
        self.Delay = float(wind.lineEdit_2.text())
        delay = self.Delay
        #26.01
        #self.LeftBorder = float(wind.lineEdit_3.text())
        #self.RightBorder = float(wind.lineEdit_4.text())
        self.CoefVoltmeter = float(wind.lineEdit_5.text())
        self.ControlLoops = float(wind.lineEdit_6.text())
        '''
        #10.06
        self.CoefVoltmeter = float(wind.ui.lineEdit_5.text())
        self.ControlLoops = float(wind.ui.lineEdit_6.text())
        #10.06
        
        self.lineEdit.Tag = ""        

#        self.showMaximized()
        self.label_2.setStyleSheet("color : blue")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setStyleSheet("color : red")

        self.label_7.setStyleSheet("color : red")
        self.lineEdit_4.setStyleSheet("color : red")
        self.lineEdit_5.setStyleSheet("color : red")
        self.label_7.setVisible(False)
        self.lineEdit_4.setVisible(False)
        self.lineEdit_5.setVisible(False)

        self.MScene = []
        self.MView = []
        for i in range(10):            
            self.MScene += [QtGui.QGraphicsScene()]        
            self.MScene[i].setSceneRect(0, 0, 10, 10)
            self.MView += [QtGui.QGraphicsView()]
            self.MView[i].setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.MView[i].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.MView[i].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)        
            self.MView[i].setScene(self.MScene[i])

#m11.01
        self.tread = MyThread()     
        self.connect(self.tread, QtCore.SIGNAL("treadsignal"), self.on_treadsignal, QtCore.Qt.QueuedConnection)
        self.connect(self.tread, QtCore.SIGNAL("mysignal"), self.on_mysignal, QtCore.Qt.QueuedConnection)
        self.connect(self.tread, QtCore.SIGNAL("mysignal1"), self.on_mysignal1, QtCore.Qt.QueuedConnection)
        self.connect(self.tread, QtCore.SIGNAL("mysignal2"), self.on_mysignal2, QtCore.Qt.QueuedConnection)
        self.connect(self.tread, QtCore.SIGNAL("mysignal3"), self.on_mysignal3, QtCore.Qt.QueuedConnection)
#        self.points = []
        self.epsilon = 0.0000001
        self.pen = QtGui.QPen()

        # Чтение параметров с heartsettings.json файла, если таковой имеется
        try:
            f = open('heartsettings.json','r')
            data = json.load(f)
            #04.2019
            '''
            print 'q'
            self.indAmp = int(data['indAmp'])
            print 'w'
            self.indVolt = int(data['indVolt'])
            print 'e'
            #2019
            self.indMeasureA = int(data['indMeasureA'])
            self.indMeasureV = int(data['indMeasureV'])
            self.adressA = int(data['adressA'])
            self.adressV = int(data['adressV'])
            
            self.MinAmp = float(data['MinAmp'])
            self.Delay = float(data['Delay'])
            delay = self.Delay
            #26.01
            #self.LeftBorder = float(data['LeftBorder'])
            #self.RightBorder = float(data['RightBorder'])
            self.CoefVoltmeter = float(data['CoefVoltmeter'])
            self.ControlLoops = float(data['ControlLoops'])
            '''
            #10.06
            self.CoefVoltmeter = float(data['CoefVoltmeter'])
            self.ControlLoops = float(data['ControlLoops'])
            #10.06
            
            self.lineEdit.Tag = data['id_heart']
            
        except Exception:
            print u'Ошибка чтения heartsettings.json!'
            return None
            
        if True:            
            query = QSqlQuery(db)
            #selectHeart = "SELECT * FROM heart WHERE id = :id_heart"
            selectHeart = """SELECT t1.id, sizes, apc, vpc, pogr, in_diameter, out_diameter,
            weight_magnetic, mark, dens, left_border, right_border
            FROM heart t1 LEFT OUTER JOIN grade_iron t2 ON (t1.id_grade = t2.id)
            WHERE t1.id = :id_heart"""            
            query.prepare(selectHeart)
            query.bindValue(":id_heart", self.lineEdit.Tag)
            query.exec_()
            query.next()
            if query.size() > 0:
                #self.lineEdit.Tag = ""
                self.lineEdit.setText(query.record().field("sizes").value().toString())
                        
                model.removeRows(0, model.rowCount())       
                self.pushButton_2.setEnabled(True)
            
                self.apc = float(query.record().field("apc").value().toString())
                self.vpc = float(query.record().field("vpc").value().toString())
                self.pogr = float(query.record().field("pogr").value().toString())
                self.in_diameter = float(query.record().field("in_diameter").value().toString())
                self.out_diameter = float(query.record().field("out_diameter").value().toString())
                self.weight_magnetic = float(query.record().field("weight_magnetic").value().toString())
                self.dens = float(query.record().field("dens").value().toString())

                #26.01
                self.LeftBorder = float(query.record().field("left_border").value().toString())
                self.RightBorder = float(query.record().field("right_border").value().toString())
                #wind.lineEdit_3.setText(str(self.LeftBorder))
                #wind.lineEdit_4.setText(str(self.RightBorder))

    def on_treadsignal(self):
        global AV
        AV = self.ReadPort()


    def resizeEvent(self, event):
            if model2.rowCount() == 0:
                self.BieldScene(self.MScene[0], self.MView[0].width(), self.MView[0].height(), [], self.points, 0)
            for i in range(model2.rowCount()):            
                self.BieldScene(self.MScene[i], self.MView[i].width(), self.MView[i].height(), self.MSamplePoints[i], self.points, self.MResult[i][0])

    def signScale(self, x):
        # Генерирует список подписей осей координат
        if abs(x) < self.epsilon:
            return [0]
        n = 0
        x_ = x
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
            sign = round(k * (i+1) * pow(10, n+1), -n+1)
            if sign > x:
                break
            signs += [sign]
        return signs    


    def BieldScene(self, scene, width, height, samplePoints, points, nSample):
        scene.clear()
        upoints = samplePoints + points
        if upoints == []:
            return
        
        maxX = upoints[0][0]
        maxY = upoints[0][1]
        for i in range(len(upoints)):
            if upoints[i][0] > maxX:
                maxX = upoints[i][0]
            if upoints[i][1] > maxY:
                maxY = upoints[i][1]
                
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

        for i in range(len(samplePoints)):
            samplePoints[i][2] = round(samplePoints[i][0] / kX)
            samplePoints[i][3] = grH - round(samplePoints[i][1] / kY)
        for i in range(len(points)):
            points[i][2] = round(points[i][0] / kX)
            points[i][3] = grH - round(points[i][1] / kY)
        
        # Оси координат
        self.pen.setColor(QtCore.Qt.black)
        self.pen.setWidth(2)
        scene.addLine(smXl, smYt, smXl, vH - smYb, self.pen)
        scene.addLine(smXl, vH - smYb, vW - smXr, vH - smYb, self.pen)
        # Подписи осей
        self.pen.setWidth(1)
        ss = self.signScale(maxX)
        for i in range(len(ss)):
            self.pen.setColor(QtCore.Qt.gray)
            scene.addLine(smXl + round(ss[i] / kX), vH - smYb, smXl + round(ss[i] / kX), smYt, self.pen)
            t1 = scene.addText(str(ss[i]))
            #t1 = scene.addText('{:.0f}'.format(ss[i]))
            
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



        if samplePoints <> []:
            # Траектория образца
            preX = samplePoints[0][2]
            preYf = samplePoints[0][1]
            self.pen.setColor(QtCore.Qt.green)
            for i in range(len(samplePoints)):
                self.pen.setWidth(3)
            
                scene.addEllipse(samplePoints[i][2] + smXl - rPoint, samplePoints[i][3] + smYt - rPoint, 2 * rPoint, 2 * rPoint, self.pen)
                if i <> 0:
                    # Границы погрешности
                    self.pen.setWidth(1)                
                    scene.addLine(preX + smXl, grH - round(preYf * ( 1 - float(self.pogr)/100) / kY) + smYt,
                                  samplePoints[i][2] + smXl, grH - round(samplePoints[i][1] * ( 1 - float(self.pogr)/100) / kY) + smYt, self.pen)
                    scene.addLine(preX + smXl, grH - round(preYf * ( 1 + float(self.pogr)/100) / kY) + smYt,
                                  samplePoints[i][2] + smXl, grH - round(samplePoints[i][1] * ( 1 + float(self.pogr)/100) / kY) + smYt, self.pen)
                    preX = samplePoints[i][2]
                    preYf = samplePoints[i][1]



        # Построение границ поверки
        self.pen.setColor(QtCore.Qt.green)
        self.pen.setWidth(2)
        scene.addLine(smXl + round(self.LeftBorder / kX), smYt, smXl + round(self.LeftBorder / kX), vH - smYb, self.pen)
        scene.addLine(smXl + round(self.RightBorder / kX), smYt, smXl + round(self.RightBorder / kX), vH - smYb, self.pen)

        # Построение контрольной точки
        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(4)
        scene.addEllipse(smXl + round(self.apc / kX) - rPoint, smYt + grH - round(self.vpc / kY) - rPoint, 2 * rPoint, 2 * rPoint, self.pen)
        #print u'Построение контрольной', smXl, self.apc, kX, rPoint, smYt, grH, self.vpc, kY, rPoint
        #print u'Построение контрольной точки', smXl + round(self.apc / kX) - rPoint, smYt + grH - round(self.vpc / kY) - rPoint, 2 * rPoint, 2 * rPoint, self.pen

        if len(points) <> 0:        
            # Траектория графика
            preX = points[0][2]
            preY = points[0][3]
            self.pen.setColor(QtCore.Qt.blue)
            for i in range(len(points)):
                self.pen.setWidth(3)
                # Подкраска точек вышедших за пределы погрешности измерения
                if points[i][0] >= self.LeftBorder and points[i][0] <= self.RightBorder:
                    for j in range(len(samplePoints)):
                        if j <> 0:
                            x1 = samplePoints[j-1][0]
                            x2 = samplePoints[j][0]
                            y1 = samplePoints[j-1][1]
                            y2 = samplePoints[j][1]
                            x  = points[i][0]
                            y  = points[i][1]
                          #  print x1, y1, x2, y2, x, y
                          #  print type(x1), type(y1), type(x2), type(y2), type(x), type(y)
                            if x >= x1 and x <= x2:
                                if x1 == x2:
                                    Vmin = min(y1, y2) * ( 1 - float(self.pogr)/100)
                                    Vmax = max(y1, y2) * ( 1 + float(self.pogr)/100)
                                else:
                                    Vmin = ((y1*(x2-x) + y2*(x-x1))/(x2-x1)) * ( 1 - float(self.pogr)/100)         
                                    Vmax = ((y1*(x2-x) + y2*(x-x1))/(x2-x1)) * ( 1 + float(self.pogr)/100)         
                                if y < Vmin or y > Vmax:
                                    self.pen.setColor(QtCore.Qt.red)
                                else:    
                                    self.pen.setColor(QtCore.Qt.blue)

                scene.addEllipse(points[i][2] + smXl - rPoint, points[i][3] + smYt - rPoint, 2 * rPoint, 2 * rPoint, self.pen)
                if i <> 0:
                    self.pen.setColor(QtCore.Qt.blue)
                    self.pen.setWidth(2)
                    scene.addLine(preX + smXl, preY + smYt, points[i][2] + smXl, points[i][3] + smYt, self.pen)
                    preX = points[i][2]
                    preY = points[i][3]
                
        # Заголовок            
        if model2.rowCount() <> 0:
            t1 = scene.addText(u'Образец ' + str(nSample))
            t1.setPos(round(vW / 2 - t1.boundingRect().width() / 2), 0)
            t1.font().setPointSize(10)  
            fnt = QtGui.QFont()
            fnt.setPointSize(12)
            fnt.setBold(True)  
            t1.setFont(fnt)  


    def ViewSample(self):
        global query2
        query2 = QSqlQuery(db)
        selectSample = """SELECT id, num FROM heart_sample
                           WHERE id_heart = :id_heart
                           ORDER BY num"""
        query2.prepare(selectSample)
        query2.bindValue(":id_heart", self.lineEdit.Tag)
        query2.exec_()
        
        model2.setQuery(query2)
            
        self.tableView_2.setColumnHidden(0, True)        
        self.tableView_2.verticalHeader().hide()       
        self.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter) 
        self.tableView_2.selectRow(0)
        self.createMsample()
        self.paintSample()
         
         
    # Заполнение массива образцов из БД
    def createMsample(self):
        for i in range(10):            
            self.verticalLayout_2.removeWidget(self.MView[i])
            self.MView[i].setVisible(False)
        
        query3 = QSqlQuery(db)
        self.MsampleA = []
        self.MsampleV = []
        self.MResult = []
        self.actions = []
        self.mnu.clear()
        self.MSamplePoints = []
        self.points = []
        for i in range(model2.rowCount()):            
            self.verticalLayout_2.addWidget(self.MView[i], 0)
            self.MView[i].setVisible(True)
                        
            SQL = """SELECT num, x, y FROM heart_spoints
                     WHERE id_sample = :id_sample
                     ORDER BY num"""
            query3.prepare(SQL)
            query3.bindValue(":id_sample", model2.query().value(0).toString())
            rez = query3.exec_()
            if not rez:
                print "ОШИБКА"        
            model3.setQuery(query3)
            self.sampleA = []
            self.sampleV = []
            self.MSamplePoints += [[]]
            for j in range(model3.rowCount()):
                model3.query().next()
                self.sampleA += [float(model3.query().value(1).toString())]
                self.sampleV += [float(model3.query().value(2).toString())]            
                self.MSamplePoints[i] += [[float(model3.query().value(1).toString()), float(model3.query().value(2).toString()), 0, 0]]
            
            self.MsampleA.append(self.sampleA)                        
            self.MsampleV.append(self.sampleV)                        
            self.MResult.append([int(model2.query().value(1).toString()), 0])
            
            
            self.act = QtGui.QAction(u'Образец ' + model2.query().value(1).toString() , self)
            
            self.act.font().setPointSize(12)
            self.act.tag = model2.query().value(0).toString()
            self.connect(self.act, QtCore.SIGNAL('triggered()'), self.on_delAction)
            
            self.actions += [self.act]
            
            model2.query().next()
        self.mnu.addActions(self.actions)    
        


    def on_delAction(self):
        row = self.selModel2.currentIndex().row()        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить " + self.sender().text() + "?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db)

            query.prepare('DELETE FROM heart_spoints WHERE id_sample = :id_sample')
            query.bindValue(":id_sample", self.sender().tag);
            rez = query.exec_()
            if not rez:
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка удаления1",
                QMessageBox.Ok)
                return

            query.prepare('DELETE FROM heart_sample WHERE id = :id_sample')
            query.bindValue(":id_sample", self.sender().tag);
            rez = query.exec_()
            if not rez:
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка удаления2",
                QMessageBox.Ok)
                return
                        
            self.ViewSample()

        
    # Прорисовка образцов     
    def paintSample(self):
        
        if model2.rowCount() == 0:
            self.BieldScene(self.MScene[0], self.MView[0].width(), self.MView[0].height(), [], self.points, 0)
        for i in range(model2.rowCount()):            
            #print "PAINT_SAMPLE"
            self.BieldScene(self.MScene[i], self.MView[i].width(), self.MView[i].height(), self.MSamplePoints[i], self.points, self.MResult[i][0])
                            
        if len(self.MsampleA) == 0:
            # Нет образцов, прорисовывается пустой холст
            self.verticalLayout_2.addWidget(self.MView[0], 0)
            self.MView[0].setVisible(True)
            pass
        else:    
            for i in range(len(self.MsampleA)):                
                # Построение границ допустимой погрешности                
                Vp = []
                Vm = []
                for j in range(len(self.MsampleV[i])):
                    Vp.append(self.MsampleV[i][j] * ( 1 + float(self.pogr)/100))
                    Vm.append(self.MsampleV[i][j] * ( 1 - float(self.pogr)/100))


    def selectionChanged2(self):
        row = self.selModel2.currentIndex().row()
        if row == -1:
            return
        global id_sample
        id_sample = model2.record(row).field('id').value().toString()

    def on_action7(self):
        from GroupHeart import GroupHeart
        wind = GroupHeart(env)
        #if wind.tag <> 0:
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
        wind.show()
#            wind.resizeEvent(None)
        wind.close()                
        wind.exec_()

    def on_action8(self):
        from GradeIron import GradeIron
        wind = GradeIron(env)
        wind.show()
        wind.close()                
        wind.exec_()

    def on_clicked1(self):
        
        from Heart import Heart
        wind = Heart(env)
        #if wind.tag <> 0:
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
        wind.show()
#            wind.resizeEvent(None)
        wind.close()                
        wind.exec_()
        if wind.id_h <> '':
            self.label_2.setText("")
            self.label_7.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_5.setVisible(False)
            
            model.removeRows(0, model.rowCount())       
            self.pushButton_2.setEnabled(True)
            self.lineEdit.Tag = wind.id_h
            self.lineEdit.setText(wind.sizes)
            self.apc = wind.apc
            self.vpc = wind.vpc
            self.pogr = wind.pogr
            self.in_diameter = wind.in_diameter
            self.out_diameter = wind.out_diameter
            self.weight_magnetic = wind.weight_magnetic
            self.dens = wind.dens

            #26.01          
            self.LeftBorder = wind.left_border
            self.RightBorder = wind.right_border
#            wind.lineEdit_3.setText(str(self.LeftBorder))
#            wind.lineEdit_4.setText(str(self.RightBorder))
                        
            self.ViewSample()
            self.pushButton_4.setEnabled(query2.size()>0)


    def on_clicked2(self):
        '''
        for i in range(model2.rowCount()):            
            self.verticalLayout_2.removeWidget(self.MView[i])
            self.MView[i].setVisible(False)
        return
        '''
        global isTestHeart
        global wasTestRez
        wasTestRez = False
        self.label_6.setText("")
        if isTestHeart:
            self.pushButton.setEnabled(True)
            self.action.setEnabled(True)
            self.action_7.setEnabled(True)
            self.action_8.setEnabled(True)
           
            self.action_3.setEnabled(True)
            isTestHeart = False
            
            time.sleep(0.1)
            self.pushButton_2.setText(u' Запустить поверку ')
        else:
            # Временно
            global iReadPort
            iReadPort = 0
            
            self.label_2.setText(u"")
            self.RunTestRez = True


            
            self.arrA  = []
            self.arrV  = []            
            model.removeRows(0, model.rowCount())  
            
            w = int((self.tableView.width() - max(self.tableView.verticalHeader().width(), 20) - min(self.tableView.verticalScrollBar().width(), 17) - 4) / 2)        
            self.tableView.setColumnWidth(0, 50)
            self.tableView.setColumnWidth(1, w)
            self.tableView.setColumnWidth(2, w)
            
            # Проверка работоспособности порта и приборов
            global AV
            AV = self.ReadPort()
            if AV == None:
                QMessageBox.warning(None, u"Предупреждение", self.errStr, QMessageBox.Ok)
                return
                               
            self.label_7.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_5.setVisible(False)
            
            self.pushButton.setEnabled(False)
            self.action.setEnabled(False)
            self.action_7.setEnabled(False)
            self.action_8.setEnabled(False)            
            self.action_3.setEnabled(False)
                                
            isTestHeart = True
            self.pushButton_2.setText(u' Остановить поверку ')

            self.workAmp = None
            self.workVolt = None
            
            self.tread.start()


    def on_clicked3(self):
        if len(self.arrA) < 1:
            QMessageBox.warning(None, u"Предупреждение",
            u"Множество точек образца не должно быть пустым!",
            QMessageBox.Ok)
            return
        
        query = QSqlQuery(db)
    
        query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM heart_sample");
        query.bindValue(":id", self.lineEdit.Tag);        
        if not query.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка 1",
            QMessageBox.Ok)
            return
        query.next()
        id_sample = query.value(0).toString()        
        
        query.prepare("SELECT CASE WHEN (MAX(num) IS NULL) THEN 1 ELSE MAX(num) + 1 END FROM heart_sample WHERE id_heart = :id_heart");
        query.bindValue(":id", self.lineEdit.Tag);        
        if not query.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка 2",
            QMessageBox.Ok)
            return
        query.next()
        num = query.value(0).toString()
        
        query.prepare("INSERT INTO heart_sample (id, id_heart, num) VALUES (:id, :id_heart, :num)")                
        query.bindValue(":id", id_sample);
        query.bindValue(":id_heart", self.lineEdit.Tag)
        query.bindValue(":num", num)
        if not query.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка сохранения",
            QMessageBox.Ok)
                        
        for i in range(len(self.arrA)):
            query.prepare("INSERT INTO heart_spoints (id_sample, num, x, y) VALUES (:id_sample, :num, :x, :y)")                
            query.bindValue(":id", id_sample);
            query.bindValue(":num", i + 1)
            query.bindValue(":x", self.arrA[i])
            query.bindValue(":y", self.arrV[i])
            if not query.exec_():
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка сохранения1",
                QMessageBox.Ok)
            
        self.ViewSample()
                

    def polynom(self, x, A):
        s = 0
        for i in range(len(A)):
            s += (x**i)*A[i]
        return s    

    def on_clicked4(self):
        row = self.selModel2.currentIndex().row()
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить образец под номером " + model2.record(row).field('num').value().toString() + "?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db)

            query.prepare('DELETE FROM heart_spoints WHERE id_sample = :id_sample')
            query.bindValue(":id_sample", model2.record(row).field('id').value().toString());
            rez = query.exec_()
            if not rez:
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка удаления1",
                QMessageBox.Ok)
                return

            query.prepare('DELETE FROM heart_sample WHERE id = :id_sample')
            query.bindValue(":id_sample", model2.record(row).field('id').value().toString());
            rez = query.exec_()
            if not rez:
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка удаления2",
                QMessageBox.Ok)
                return
                        
            self.ViewSample()

    def on_clicked6(self):
        global delay
        global data
#        from HeartSettings import HeartSettings
        #04.2019
        #wind = HeartSettings(env, self.indAmp, self.indVolt)
        wind = HeartSettings(env)
        wind.setEnabled(True)
        
        '''        
        #2019
        wind.comboBox.clear()
        wind.comboBox.addItems(self.Devices.sTypes)
        wind.comboBox_2.clear()
        wind.comboBox_2.addItems(self.Devices.sTypes)
        wind.comboBox_3.clear()
        wind.comboBox_3.addItems(self.Devices.sMeasuresA)
        wind.comboBox_3.setCurrentIndex(self.indMeasureA)
        wind.comboBox_4.clear()
        wind.comboBox_4.addItems(self.Devices.sMeasuresV)
        wind.comboBox_4.setCurrentIndex(self.indMeasureV)
        wind.spinBox_3.setValue(self.adressA)                        
        wind.spinBox_4.setValue(self.adressV)                        
                                                                
        wind.comboBox.setCurrentIndex(self.indAmp)
        wind.comboBox_2.setCurrentIndex(self.indVolt)
        
        
        
        wind.lineEdit.setText(str(self.MinAmp))
        wind.lineEdit_2.setText(str(self.Delay))
        ###########################################26.01
        
        #2019
        #wind.lineEdit_3.setText(str(self.LeftBorder))
        #wind.lineEdit_4.setText(str(self.RightBorder))
        wind.lineEdit_5.setText(str(self.CoefVoltmeter))
        wind.lineEdit_6.setText(str(self.ControlLoops))
        '''
        #10.06
        wind.ui.lineEdit_5.setText(str(self.CoefVoltmeter))
        wind.ui.lineEdit_6.setText(str(self.ControlLoops))
        #10.06
        
       # wind.show()
       # wind.close()                
        wind.exec_()
        
#        QMessageBox.warning(None, u"Предупреждение", u"1", QMessageBox.Ok)
        # Чтение параметров с heartsettings.json файла, если таковой имеется
        try:
            f = open('heartsettings.json','r')
            data = json.load(f)
      #      print 'coeff = ', data['devices']['1']['coeff']
        except Exception:
#            QMessageBox.warning(None, u"Предупреждение", u"2", QMessageBox.Ok)
            print u'Ошибка чтения heartsettings.json!'
            return None
        
        
            
        
        '''        
        self.indAmp = wind.comboBox.currentIndex()
        self.indVolt = wind.comboBox_2.currentIndex()
                
        #2019
        self.indMeasureA = wind.comboBox_3.currentIndex()
        self.indMeasureV = wind.comboBox_4.currentIndex()
        self.adressA = wind.spinBox_3.value()
        self.adressV = wind.spinBox_4.value()
                                        
        self.MinAmp = float(wind.lineEdit.text())
        self.Delay = float(wind.lineEdit_2.text())
        delay = self.Delay
        
        #26.01
        #self.LeftBorder = float(wind.lineEdit_3.text())
        #self.RightBorder = float(wind.lineEdit_4.text())
        self.CoefVoltmeter = float(wind.lineEdit_5.text())
        self.ControlLoops = float(wind.lineEdit_6.text())
        '''        
        #10.06
        wind.ui.lineEdit_5.setText(str(self.CoefVoltmeter))
        wind.ui.lineEdit_6.setText(str(self.ControlLoops))
        #10.06

    def on_clicked7(self):
        #10.06
   #     self.arrA = [1,2,3,4,5]
   #     self.arrV = [1,5,6,4,5]
        
        #self.in_diameter = 10
        #self.out_diameter = 20
        #self.weight_magnetic = 7
        #self.dens = 8
   #     self.CoefVoltmeter = 77
   #     self.ControlLoops = 88
        
        #10.06
        
        ReportsExcel.BAX(self.arrA , self.arrV, self.in_diameter, self.out_diameter, self.weight_magnetic, self.dens, self.CoefVoltmeter, self.ControlLoops)

    def on_clicked8(self):
        self.close()

    '''
    def setConfig(self):
        from config import Config
        Config = Config()        
        #sys.exit(app.exec_())
        
        #Config.setEnabled(True)
        #Config.show()
#        Config.close()
        Config.groupBox_2.setVisible(False)        
        Config.groupBox_4.setVisible(False)        
        Config.label_6.setVisible(False)        
        Config.spinBox_6.setVisible(False)        
        Config.spinBox_3.setVisible(False)        
        Config.label_7.setVisible(False)        
        Config.spinBox_7.setVisible(False)        
        Config.spinBox_4.setVisible(False)        
        Config.label_9.setVisible(False)        
        Config.spinBox_5.setVisible(False)        
        Config.exec_()
 #       Config.close()                
        #Config.destroy()
       '''
         

    def closeEvent(self, event):
        global data        
#        print "data=", data
        #return
        # ЗАПИСАТЬ
        f = open('heartsettings.json','w')
        #10.06
        data['CoefVoltmeter'] = str(self.CoefVoltmeter)
        data['ControlLoops'] = str(self.ControlLoops)
        #10.06
        if self.lineEdit.Tag <> "":
            data['id_heart'] = str(self.lineEdit.Tag)
            
  #      print data
#        print 'json.dump(data, f)'
        json.dump(data, f)
        return        
        
        '''       
        data = {}        
        data['indAmp'] = str(self.indAmp)
        data['indVolt'] = str(self.indVolt)
        
        #2019
        data['indMeasureA'] = str(self.indMeasureA)
        data['indMeasureV'] = str(self.indMeasureV)
        data['adressA'] = str(self.adressA)
        data['adressV'] = str(self.adressV)
                        
        data['MinAmp'] = str(self.MinAmp)
        data['Delay'] = str(self.Delay)
        #26.01
        #data['LeftBorder'] = str(self.LeftBorder)
        #data['RightBorder'] = str(self.RightBorder)
        data['CoefVoltmeter'] = str(self.CoefVoltmeter)
        data['ControlLoops'] = str(self.ControlLoops)
        
        if self.lineEdit.Tag <> "":
            data['id_heart'] = str(self.lineEdit.Tag)
            
  #      print data
        print 'json.dump(data, f)'
        json.dump(data, f)
        '''
   

    def on_mysignal(self):
        while isTestHeart:
            time.sleep(0.1)
        return     
        self.startTestHeart1()
        pass

    def on_mysignal1(self):
        self.label_6.setText(self.label_6.text() + "#")
        if len(self.label_6.text()) > 20:
            self.label_6.setText("")
        self.lineEdit_2.setText('____')
        self.lineEdit_3.setText('____')

    def on_mysignal2(self):
        self.label_2.setStyleSheet("color : blue")
        self.label_2.setText(u"Сбой COM-порта!\nЗапустите поверку заново.")

    def on_mysignal3(self):
        #print('Обработан пользовательский сигнал3333333333333')
        self.label_6.setText("")
                                
        #self.lineEdit_2.setText(AV[0])
        #self.lineEdit_3.setText(AV[1])
        
#        print 'AV[0]=', AV[0]
#        print 'AV[1]=', AV[1]
        self.lineEdit_2.setText(str(round(float(AV[0]),3)))    
        self.lineEdit_3.setText(str(round(float(AV[1]),3)))    
        
            
        # Проверка условия на запись точек диаграммы
        if self.ALess and float(AV[0]) >= self.MinAmp:
            wasTestRez = False
            self.RunTestRez = True
            self.arrSIA = []
            self.arrA  = []
            self.arrV  = []            
            model.removeRows(0, model.rowCount())              
            w = int((self.tableView.width() - max(self.tableView.verticalHeader().width(), 40) - min(self.tableView.verticalScrollBar().width(), 17) - 4) / 2)        
            self.tableView.setColumnWidth(0, 40)
            self.tableView.setColumnWidth(1, w)
            self.tableView.setColumnWidth(2, w)
            self.paintSample()
            
            self.nPoint = 0                
            self.pushButton_3.setEnabled(False)
            self.action_6.setEnabled(False)
            
            self.label_2.setText("")
            self.label_7.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_5.setVisible(False)
                        
            self.pushButton_4.setEnabled(False)
            self.action_4.setEnabled(False)
                                
        self.ALess = (float(AV[0]) < self.MinAmp)
           
        # Проверка условия на останов тестирования
        lenA = len(self.arrA)
        if lenA > 0 and float(AV[0]) < self.arrA[lenA - 1]:
             self.ABack = True                      
        self.ALess = (float(AV[0]) < self.MinAmp)
            
        if not self.ALess and not self.ABack:

#15.04.2019            model.insertRow(0, [QtGui.QStandardItem(str(self.nPoint + 1)), QtGui.QStandardItem(AV[0]), QtGui.QStandardItem(AV[1])])    
            model.insertRow(0, [QtGui.QStandardItem(str(self.nPoint + 1)), QtGui.QStandardItem(str(round(float(AV[0]),3))), QtGui.QStandardItem(str(round(float(AV[1]),3)))])    
            self.arrA.append(float(AV[0]))
            self.arrV.append(float(AV[1]))
                              
            self.nPoint += 1
                
            if not self.checkBox.isChecked():                
                
                self.points = []
                for i in range(len(self.arrA)):
                    
                    self.points += [[self.arrA[i], self.arrV[i], 0, 0]]
                if model2.rowCount() == 0:
                    self.BieldScene(self.MScene[0], self.MView[0].width(), self.MView[0].height(), [], self.points, 0)
                for i in range(model2.rowCount()):            
                    self.BieldScene(self.MScene[i], self.MView[i].width(), self.MView[i].height(), self.MSamplePoints[i], self.points, self.MResult[i][0])
                
#15.04.2019        if self.ALess and self.ABack:
        if self.ABack:    # Результат тестирования появятся как только крутанули латер назад 
            if self.RunTestRez:
                wasTestRez = True
                self.TestResult()
                self.RunTestRez = False    
                wasTestRez = True
            self.ABack = False                
            self.pushButton_3.setEnabled(True)
            self.action_6.setEnabled(True)
            self.pushButton_4.setEnabled(query2.size()>0)
            self.action_4.setEnabled(True)
        
        global isReadPort    
        isReadPort = True

            
            
    def TestResult(self):

        # Проверка значений в контрольной точке
        for i in range(len(self.arrA)):
            if i > 0 and self.arrA[i-1] <= self.apc and self.arrA[i] >= self.apc:
                if self.arrA[i-1] == self.arrA[i]:
                    Vpc = max(self.arrV[i-1], self.arrV[i])
                else:
                    Vpc = (self.arrV[i-1] * (self.arrA[i] - self.apc) + self.arrV[i] * (self.apc - self.arrA[i-1])) / (self.arrA[i] - self.arrA[i-1])
                                        
                self.label_7.setVisible(True)
                self.lineEdit_4.setVisible(True)
                self.lineEdit_5.setVisible(True)
                    
                self.lineEdit_4.setText(str(self.apc))    
                self.lineEdit_5.setText(str(nRound(Vpc, 4)))    
                    
                if Vpc < self.vpc:
                    self.label_2.setStyleSheet("color : red")
                    self.label_2.setText(u"Напряжение в\n\rконтрольной точке\n\rниже предельно допустимого")
                    self.pushButton_3.setEnabled(False)
                    self.action_6.setEnabled(False)
                    return

        # Проверка выхода за пределы погрешности измерения
        for i in range(len(self.MResult)):
            self.MResult[i][1] = 0

        for i in range(len(self.MsampleA)):
            Vp = []
            Vm = []
            for j in range(len(self.MsampleV[i])):
                Vp.append(self.MsampleV[i][j] * ( 1 + float(self.pogr)/100))
                Vm.append(self.MsampleV[i][j] * ( 1 - float(self.pogr)/100))
        
            for j in range(len(self.arrA)):
                # Проверка выхода за диапазон
                if self.arrA[j] < self.LeftBorder or self.arrA[j] > self.RightBorder:
                    continue
                for k in range(len(self.MsampleA[i])):
                    if self.arrA[j] < self.MsampleA[i][k] and k > 0:
                        if self.MsampleA[i][k] == self.MsampleA[i][k-1]:
                            Vmin = min(Vm[k], Vp[k-1])
                            Vmax = max(Vp[k], Vp[k-1])
                        else:
                            Vmin = (Vm[k-1] * (self.MsampleA[i][k] - self.arrA[j]) + Vm[k] * (self.arrA[j] - self.MsampleA[i][k-1])) / (self.MsampleA[i][k] - self.MsampleA[i][k-1])         
                            Vmax = (Vp[k-1] * (self.MsampleA[i][k] - self.arrA[j]) + Vp[k] * (self.arrA[j] - self.MsampleA[i][k-1])) / (self.MsampleA[i][k] - self.MsampleA[i][k-1])         
                        # Проверка выхода за пределы погрешности измерения
                        if self.arrV[j] < Vmin or self.arrV[j] > Vmax:
                            self.MResult[i][1] = 1
                        break    
        obr = u'образцу '
        SpisRez = ''
        for i in range(len(self.MResult)):
            if self.MResult[i][1] == 0:
                if SpisRez == '':
                    SpisRez += str(self.MResult[i][0])
                else:        
                    SpisRez += ', ' + str(self.MResult[i][0])
                    obr = u'образцам:\n\r'
        
        if SpisRez == '':
            self.label_2.setStyleSheet("color : blue")
            self.label_2.setText(u"Показания не\n\rсоответствуют\n\rни одному\n\rиз образцов")
            self.pushButton_3.setEnabled(True)
            self.action_6.setEnabled(True)
        else:    
            self.label_2.setStyleSheet("color : blue")
            self.label_2.setText(u"Показания\n\rсоответствуют\n\r" + obr + SpisRez)
            self.pushButton_3.setEnabled(False)
            self.action_6.setEnabled(False)


    '''
    def ReadDevice(self, port, command):
        # Чтение показания прибора типа ЩП02М
        global isTestHeart
        try:
            port.write(command)
            s = port.read(15)
            if len(s) < 13:
                self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                return None                            
            return s[8] + s[7] + s[10] + s[9] + s[12] + s[11]
        except SerialException:
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            ###isTestHeart = False
            self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
            print u'Ошибка чтения показаний прибора!'
            return None

    def ReadDevice1(self, port, command):
        # Чтение показания прибора типа СА3020
        global isTestHeart
        try:
            port.write(command)
            s = port.read(10)
            if len(s) < 10:
                self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
                return None
            
            # Мантисса
            M = ord(s[6]) * 256 + ord(s[5])
            print M
            # Экспонента
            p = ord(s[7]) - 256
            # Результат
            N = M * math.pow(2, p)
            return str(round(N, 3))
        except SerialException:
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
            print u'Ошибка чтения показаний прибора!'
            return None

        

    def ReadDevice2(self, port, command):
        # Чтение показания прибора типа ЩП02П через регистры
        global isTestHeart
        try:
            port.write(command)
            s = port.read(16)
            port.write(command)
            s = port.read(16)
            
            
            lis = [hex(ord(s[4])), hex(ord(s[3])), hex(ord(s[6])), hex(ord(s[5]))]
#            print lis
            a = ''
            for i in range(len(lis)):
                c = str(lis[i])[2:]
                if len(c) == 1:
                    c = '0' + c
                a += c
                
 #           print 'a11111111111111111=', a
            b = struct.unpack('<f', binascii.unhexlify(a))
 #           print 'bbbbbbb=', b
            return str(round(b[0],3))
 
        except SerialException:
            ###isTestHeart = False
            self.errStr = u"Проблема работы прибора с адресом: " + command
            QMessageBox.warning(None, u"Предупреждение", u"Проблема работы прибора с адресом: " + command, QMessageBox.Ok)
            return None                            
        except Exception:
            ###isTestHeart = False
            self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(ord(command[0]))
            print u'Ошибка чтения показаний прибора!'
            return None
'''
        
                
    def ReadPort(self):
        global port        
        global isReadPort
                
#m10.01 закоментировать Эмуляцию чтения порта
        
        # Эмуляция чтения порта
        
        # Чтение показания приборов (амперметр, вольтметр)    
        global isTestHeart
        try:
            A = ''
            V = ''
            port.port = env.config.devices.chp02m.port
            port.baudrate = 9600
            port.bytesize = 8
            port.parity = 'N'
            port.stopbits = 1
            port.timeout = 0.1
            port.close()
            port.open()
            
            
            print 'self.workAmp=self.workAmp=self.workAmp=self.workAmp=self.workAmp', self.workAmp
            #2019            
            # A - показание амперметра
            A = self.ReadDevices_2(port, 0, self.workAmp)        
            #A = self.Devices.ReadDevice_2(port, self.indAmp, self.adressA, 1.0)
            print 'AAA=', A
            if A == None:
                isReadPort = True
                print 'qqq'
                ###self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(self.adressA)
                print 'www'
                return None            
###                Val = self.coefMeasure(self.data['devices'][str(i)]['ind_measure']) * float(Val)
#            A = self.coefMeasure(self.data['devices'][str(i)]['ind_measure']) * float(Val)
#            A = str(self.Devices.coefMeasure(self.indMeasureA ) * float(A))                
                        
            time.sleep(0.01)
            port.close()
            port.open()
            
            # V - показание вольтметра
            V = self.ReadDevices_2(port, 1, self.workVolt)        
#            V = self.Devices.ReadDevice_2(port, self.indVolt, self.adressV, 1.0)
            if V == None:
                isReadPort = True
                ###self.errStr = u"Ошибка чтения показаний прибора с адресом: " + str(self.adressV)
                return None
#            V = str(self.Devices.coefMeasure(self.indMeasureV ) * float(V))                
            time.sleep(0.01)
            port.close()
            port.open()
                        
        except SerialException:
            print u"Порт " + port.port + u' не открывается!'
            self.errStr = u"Порт " + port.port + u' не открывается!'
            isReadPort = True
            return None
        except Exception:
            self.errStr = u"Проблемы с портом " + port.port
            isReadPort = True
            return None
        finally:
            isReadPort = True
            port.close()
        isReadPort = True
        print 'A.strip(), V.strip()', A.strip(), V.strip()
        return A.strip(), V.strip()


    def ReadDevices_2(self, port, ind_name, workDev):        
        # Чтение показаний цепочки приборов (выбирается показание с первого прибора превышающего минимальное значение)         
        # ind_name = 0 - амперметры        
        # ind_name = 1 - вольтметры
        global data
                
        for i in range(len(data['devices'])):
            self.ind_device = i + 1  # self.ind_device - для режима эмуляции
            
            if data['devices'][str(i)]['activ'] == False or data['devices'][str(i)]['ind_name'] <> ind_name:
                continue
            if workDev != None and workDev != i:
                continue
            '''
            if self.Devices.data['devices'][str(i)]['ind_type'] == 0:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(3)+chr(0)+chr(5)+chr(0)+chr(5)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 1:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(22)+chr(0)+chr(2)
            if self.Devices.data['devices'][str(i)]['ind_type'] == 2:
                st = chr(self.Devices.data['devices'][str(i)]['address'])+chr(4)+chr(0)+chr(7)+chr(0)+chr(4)                
            st += chr(crc16(st)[0]) + chr(crc16(st)[1])
'''
           
#            Val = self.Devices.ReadDevice_2(self.port, indType, adr, 1.0)
            Val = self.Devices.ReadDevice_2(port, data['devices'][str(i)]['ind_type'], data['devices'][str(i)]['address'], data['devices'][str(i)]['coeff'])
            #15.04.2019
            Val = str(self.Devices.coefMeasure(data['devices'][str(i)]['ind_measure']) * float(Val))

            
#####            Val = self.Devices.ReadDevice(port, self.Devices.data['devices'][str(i)]['ind_type'], st, self.Devices.data['devices'][str(i)]['coeff'])
            #if ind_name == 0:
            #    self.ui.lineEdit_14.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
            #if ind_name == 1:
            #    self.ui.lineEdit_15.setText(u'М' + str(self.Devices.data['devices'][str(i)]['address']) + '  ' + str(Val))
     #       print 'q'
            time.sleep(data['pause'])
                                            
            # Определение рабочего прибора и присвоение ему индекса
            if workDev == None:
                if Val != None:
                    # С учетом единицы измеренния
#                    print 'e'
                    if float(Val) > data['devices'][str(i)]['min_value']:
 #                       print 'r'
                        workDev = i #??????????????????????????
                        if ind_name == 0:
  #                          print 'ValAmper=', Val
                            self.workAmp = i
                            #25.10.17
                            self.MinAmp = data['devices'][str(i)]['min_value']                            
                            #25.10.17
                            print 'self.workAmp=', self.workAmp
   #                         print self.Devices.Measures[self.workAmp].currentText()
                            #19.01 поменял единицу измерения 
#                            self.ui.label_4.setText(str(self.workAmp + 1) + u'. Амперметр (' + self.Devices.Measures[self.workAmp].currentText() + u')')                            

                        if ind_name == 1:
    #                        print 'ValVoltmetr=', Val
                            self.workVolt = i
                            print 'self.workVolt=', self.workVolt
                            #19.01 поменять единицу измерения 
#                            self.ui.label_5.setText(str(self.workVolt + 1) + u'. Вольтметр (' + self.Devices.Measures[self.workVolt].currentText() + u')')                            
                            
                        return Val
                    else:
                        continue                            
        if workDev == None:
#            return False   # False означает, что показания всех трансов из цепочки нулевые                             
#            return None   # None означает, что показания всех трансов из цепочки нулевые                             
            return '0'   # None означает, что показания всех трансов из цепочки нулевые                             
        return Val



    def TestBase(self):
        #return True        
        query = QSqlQuery(db)
        print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        
        query.prepare("select left_border, right_border from heart")
        if not query.exec_(): err_tbl += "heart\n"        
        """
        query.prepare("select * from grade_iron")
        if not query.exec_(): err_tbl += "grade_iron\n"
        """
        """
        query.prepare("select * from group_heart")
        if not query.exec_(): err_tbl += "group_heart\n"
        """
        """
        query.prepare("select * from heart")
        if not query.exec_(): err_tbl += "heart\n"
        query.prepare("select * from heart_sample")
        if not query.exec_(): err_tbl += "heart_sample\n"
        query.prepare("select * from heart_spoints")
        if not query.exec_(): err_tbl += "heart_spoints\n"
        """  
          
        if err_tbl != "":
         ###   print err_tbl  
            r = QMessageBox.warning(self, u"Предупреждение", u"""Для нормальной работы приложения В БД необходимо произвести изменения в структуры следующих таблиц:
""" + err_tbl + "\n" +
u"Произвести инициализацию БД?", QMessageBox.Yes, QMessageBox.No)                        
#            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД отсутствут следующие таблицы,
#необходимые для работы приложения:\n""" + err_tbl +
#u"Произвести инициализацию БД?", QMessageBox.Yes, QMessageBox.No)                        
                        
            if r == QMessageBox.Yes:
                self.InitBase()
                return True
            else:
                return False
        return True
                       

    def InitBase(self):
        print u"Инициализация БД"        
        query = QSqlQuery(db)

        SQL = u"""
ALTER TABLE heart ADD column left_border numeric(8,4);
ALTER TABLE heart ADD column right_border numeric(8,4);
COMMENT ON COLUMN heart.left_border IS 'Нижняя граница диапазона поверки по показаниям амперметра';
COMMENT ON COLUMN heart.right_border IS 'Верхняя граница диапазона поверки по показаниям амперметра';
UPDATE heart set left_border = 4, right_border = 6;

        """

        query.prepare("select left_border, right_border from heart")

        if not query.exec_(SQL):
            print "Ошибка инициализации"
        else:
            print "Инициализация выполнена!"
            
        return



        SQL = u"""
CREATE TABLE grade_iron
(
  id serial PRIMARY KEY,
  mark character varying(100) NOT NULL,
  dens numeric(10,6)
);
COMMENT ON TABLE grade_iron IS 'Справочник удельных весов железа';
COMMENT ON COLUMN grade_iron.id IS 'Идентификатор записи';
COMMENT ON COLUMN grade_iron.mark IS 'Марка железа';
COMMENT ON COLUMN grade_iron.dens IS 'Удельный вес электротехнического железа';

ALTER TABLE heart DROP column dens_iron;
ALTER TABLE heart ADD column height numeric(8,4);
ALTER TABLE heart ADD column in_length numeric(8,4);
ALTER TABLE heart ADD column in_height numeric(8,4);
ALTER TABLE heart ADD column depth numeric(8,4);
ALTER TABLE heart ADD column width numeric(8,4);
ALTER TABLE heart ADD column id_grade integer REFERENCES grade_iron;    
COMMENT ON COLUMN heart.id_grade IS 'Внешний ключ к grade_iron';
COMMENT ON COLUMN heart.height IS 'Высота сердечника';
COMMENT ON COLUMN heart.in_length IS 'Внутренняя длина';
COMMENT ON COLUMN heart.in_height IS 'Внутренняя высота';
COMMENT ON COLUMN heart.depth IS 'Толщина';
COMMENT ON COLUMN heart.width IS 'Ширина ленты';

ALTER TABLE group_heart ADD column shape numeric(1);
COMMENT ON COLUMN group_heart.shape IS 'Форма сердечника';

COMMENT ON TABLE group_heart IS 'Справочник групп средств измерения';
COMMENT ON COLUMN group_heart.id IS 'Идентификатор записи';
COMMENT ON COLUMN group_heart.name_group IS 'Наименование группы';

COMMENT ON TABLE heart IS 'Справочник сердечников';
COMMENT ON COLUMN heart.id IS 'Идентификатор записи';
COMMENT ON COLUMN heart.sizes IS 'Размеры';
COMMENT ON COLUMN heart.apc IS 'Сила тока в точке контроля';
COMMENT ON COLUMN heart.vpc IS 'Напряжение в точке контроля';
COMMENT ON COLUMN heart.pogr IS 'Максимально допустимая погрешность (в процентах)';
COMMENT ON COLUMN heart.id_group IS 'Внешний ключ к group_heart';
COMMENT ON COLUMN heart.in_diameter IS 'Внутренний диаметр сердечника';
COMMENT ON COLUMN heart.out_diameter IS 'Внешний диаметр сердечника';
COMMENT ON COLUMN heart.weight_magnetic IS 'Вес магнитопровода';


COMMENT ON TABLE heart_sample IS 'Справочник эталонных кривых сердечников';
COMMENT ON COLUMN heart_sample.id IS 'Идентификатор записи';
COMMENT ON COLUMN heart_sample.id_heart IS 'Внешний ключ к heart';
COMMENT ON COLUMN heart_sample.num IS 'Порядковый номер образца';

COMMENT ON TABLE heart_spoints IS 'Справочник точек эталонных кривых сердечников';
COMMENT ON COLUMN heart_spoints.id_sample IS 'Внешний ключ к heart_sample';
COMMENT ON COLUMN heart_spoints.num IS 'Порядковый номер точки';
COMMENT ON COLUMN heart_spoints.x IS 'Координата по X';
COMMENT ON COLUMN heart_spoints.y IS 'Координата по Y';

        """

        if not query.exec_(SQL):
            print "Ошибка инициализации"
        else:
            print "Инициализация выполнена!"
            
            
        return




        SQL = """
CREATE TABLE group_heart
(
  id serial PRIMARY KEY,
  name_group character varying(200) NOT NULL
);
COMMENT ON TABLE group_heart IS 'Справочник групп средств измерения';
COMMENT ON COLUMN group_heart.id IS 'Идентификатор записи';
COMMENT ON COLUMN group_heart.name_group IS 'Наименование группы';

ALTER TABLE heart ADD column id_group integer REFERENCES group_heart;
ALTER TABLE heart ADD column in_diameter numeric(8,4);
ALTER TABLE heart ADD column out_diameter numeric(8,4);
ALTER TABLE heart ADD column weight_magnetic numeric(10,6);
ALTER TABLE heart ADD column dens_iron numeric(10,6);
    
COMMENT ON COLUMN heart.id_group IS 'Внешний ключ к group_heart';
COMMENT ON COLUMN heart.in_diameter IS 'Внутренний диаметр сердечника';
COMMENT ON COLUMN heart.out_diameter IS 'Внешний диаметр сердечника';
COMMENT ON COLUMN heart.weight_magnetic IS 'Вес магнитопровода';
COMMENT ON COLUMN heart.dens_iron IS 'Удельный вес электротехнического железа';

        """

        if not query.exec_(SQL):
            print "Ошибка инициализации"
        else:
            print "Инициализация выполнена!"
        return



        
        SQL = """
drop table heart_spoints;
drop table heart_sample;
drop table heart;        
"""
      #  print SQL
        if not query.exec_(SQL):
            print "Ошибка удаления"
        else:
            print "Удаление выполнено!"
            
        SQL = """
CREATE TABLE heart
(
  id serial PRIMARY KEY,
  sizes character varying(80) NOT NULL,
  apc numeric(8,4),
  vpc numeric(8,4),
  pogr numeric(4,2)
);
COMMENT ON TABLE heart IS 'Справочник сердечников';
COMMENT ON COLUMN heart.id IS 'Идентификатор записи';
COMMENT ON COLUMN heart.sizes IS 'Размеры';
COMMENT ON COLUMN heart.apc IS 'Сила тока в точке контроля';
COMMENT ON COLUMN heart.vpc IS 'Напряжение в точке контроля';
COMMENT ON COLUMN heart.pogr IS 'Максимально допустимая погрешность (в процентах)';


CREATE TABLE heart_sample
(
  id serial PRIMARY KEY,
  id_heart integer REFERENCES heart,
  num integer
);
COMMENT ON TABLE heart_sample IS 'Справочник эталонных кривых сердечников';
COMMENT ON COLUMN heart_sample.id IS 'Идентификатор записи';
COMMENT ON COLUMN heart_sample.id_heart IS 'Внешний ключ к heart';
COMMENT ON COLUMN heart_sample.num IS 'Порядковый номер образца';


CREATE TABLE heart_spoints
(
  id_sample integer REFERENCES heart_sample,
  num integer,
  x numeric(12,6),
  y numeric(12,6)
);
COMMENT ON TABLE heart_spoints IS 'Справочник точек эталонных кривых сердечников';
COMMENT ON COLUMN heart_spoints.id_sample IS 'Внешний ключ к heart_sample';
COMMENT ON COLUMN heart_spoints.num IS 'Порядковый номер точки';
COMMENT ON COLUMN heart_spoints.x IS 'Координата по X';
COMMENT ON COLUMN heart_spoints.y IS 'Координата по Y';
"""


        
        if not query.exec_(SQL):
            print "Ошибка инициализации"
        else:
            print "Инициализация выполнена!"






if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    from dpframe.base.inits import db_connection_init
    @json_config_init
    @db_connection_init
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
        
    db = env.db
    path_ui = env.config.paths.ui + "/"

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

        wind = HeartSettings(env)
        wind.setEnabled(True)
        wind.exec_()
                
    else:                
                        
        wind = win()
        if wind.is_show: 
            wind.show()
            wind.ViewSample()
            wind.showMaximized()
        sys.exit(app.exec_())

