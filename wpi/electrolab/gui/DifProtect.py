#coding=utf-8
u"""
Created on 7.06.2017
@author: TAM
"""
import sys

print 111111111111

'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont,       QDoubleSpinBox,         QToolButton
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from serial import Serial
from serial.serialutil import SerialException

from dpframe.tech.SimpleSound import SimpleSound

from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
from electrolab.app.item import Item
from devices import Devices
from TestCoilReport import TestCoilReport
from electrolab.gui.reporting import FRPrintForm
from win32com.client import Dispatch
import stat




'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
import ReportsExcel


from electrolab.gui.common import UILoader

import ui.ico_64_rc


model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()


class DifProtect(QtGui.QDialog, UILoader):
    def __init__(self, _env, trans):
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"DifProtect.ui")
#        self.setEnabled(False)
        self.fnt =  QFont()
        self.fnt.setPixelSize(20)
        
        self.env = _env

        self.pen = QtGui.QPen()        
        self.epsilon = 0.0000001

        self.query   = QSqlQuery(self.env.db)
        self.query_2 = QSqlQuery(self.env.db)
        self.query_3 = QSqlQuery(self.env.db)

        self.charts = None
        
#        for i in range(len(self.Numbering)):
#        self.QuanCoil = 4
        self.Numbering = []   # нумерация приборов
        self.Coil      = []   # обмотки
        self.MinLim    = []   # мин предел диапазона
        self.MaxLim    = []   # мах предел диапазона
        
        self.ui.lineEdit.setText(trans)



        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.setSceneRect(0, 0, 1, 1)
        self.ui.graphicsView.setScene(self.graphicsScene)        


                
        self.ui.pushButton.clicked.connect(self.pushButton_Click)        
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)        

        self.add_coils(5.0)            
        self.refresh_coils()
        


    def pushButton_Click(self):
        import ReportsExcel
        #self.read_charts(208941, True)
        #self.charts = [[105827, [[0.2, 32.94427191], [1.0, 44.0], [1.2, 45.9089023002], [1.4, 47.6643191324], [1.6, 49.2982212813], [1.8, 50.83281573], [2.0, 52.2842712475], [2.2, 53.6647939484], [2.4, 54.9838667697], [2.6, 56.2490309932], [2.8, 57.4664010614], [3.0, 58.6410161514], [3.2, 59.77708764], [3.4, 60.8781778292], [3.6, 61.947331922], [3.8, 62.9871773792], [4.0, 64.0], [4.2, 64.9878030638], [4.4, 65.9523539268], [4.6, 66.8952211791], [4.8, 67.8178046004], [5.0, 68.72135955], [5.2, 69.607017004], [5.4, 70.4758001545]]], [105831, [[0.2, 64.94427191], [1.0, 76.0], [1.4, 79.6643191324], [1.6, 81.2982212813], [1.8, 82.83281573], [2.2, 85.6647939484], [2.6, 88.2490309932], [2.8, 89.4664010614], [3.0, 90.6410161514], [3.2, 91.77708764], [3.4, 92.8781778292], [3.6, 93.947331922], [4.0, 96.0], [4.4, 97.9523539268], [4.6, 98.8952211791], [4.8, 99.8178046004], [5.2, 101.607017004], [5.6, 103.328638265], [5.8, 104.166378315], [6.0, 104.989794856], [6.2, 105.799598392]]], [105829, [[0.2, 48.94427191], [1.0, 60.0], [1.2, 61.9089023002], [1.4, 63.6643191324], [1.6, 65.2982212813], [1.8, 66.83281573], [2.0, 68.2842712475], [2.2, 69.6647939484], [2.4, 70.9838667697], [2.6, 72.2490309932], [2.8, 73.4664010614], [3.2, 75.77708764], [3.4, 76.8781778292], [3.6, 77.947331922], [3.8, 78.9871773792], [4.0, 80.0], [4.2, 80.9878030638], [4.8, 83.8178046004], [5.0, 84.72135955], [5.2, 85.607017004], [5.4, 86.4758001545], [5.6, 87.3286382648], [5.8, 88.1663783152], [6.0, 88.9897948557]]], [105833, [[0.2, 80.94427191], [0.4, 84.6491106407], [1.4, 95.6643191324], [1.6, 97.2982212813], [1.8, 98.83281573], [2.2, 101.664793948], [2.6, 104.249030993], [3.0, 106.641016151], [3.2, 107.77708764], [3.4, 108.878177829], [3.6, 109.947331922], [3.8, 110.987177379], [4.0, 112.0], [4.2, 112.987803064], [4.4, 113.952353927], [4.6, 114.895221179], [4.8, 115.8178046], [5.0, 116.72135955], [5.2, 117.607017004], [5.4, 118.475800154]]], [105825, [[0.2, 16.94427191], [0.4, 20.6491106407], [1.4, 31.6643191324], [1.8, 34.83281573], [2.0, 36.2842712475], [2.2, 37.6647939484], [2.4, 38.9838667697], [2.6, 40.2490309932], [2.8, 41.4664010614], [3.0, 42.6410161514], [3.2, 43.77708764], [3.4, 44.8781778292], [3.6, 45.947331922], [3.8, 46.9871773792], [4.0, 48.0], [4.2, 48.9878030638], [4.4, 49.9523539268], [4.6, 50.8952211791], [4.8, 51.8178046004], [5.0, 52.72135955], [5.2, 53.607017004], [5.4, 54.4758001545], [5.6, 55.3286382648], [5.8, 56.1663783152]]], [105834, [[0.4, 92.6491106407], [0.8, 97.88854382], [1.6, 105.298221281], [1.8, 106.83281573], [2.2, 109.664793948], [2.6, 112.249030993], [2.8, 113.466401061], [3.2, 115.77708764], [3.6, 117.947331922], [4.0, 120.0], [4.4, 121.952353927], [4.6, 122.895221179], [4.8, 123.8178046], [5.0, 124.72135955], [5.2, 125.607017004], [5.4, 126.475800154]]], [105826, [[0.2, 24.94427191], [1.0, 36.0], [1.2, 37.9089023002], [1.4, 39.6643191324], [1.6, 41.2982212813], [1.8, 42.83281573], [2.0, 44.2842712475], [2.2, 45.6647939484], [2.4, 46.9838667697], [2.6, 48.2490309932], [2.8, 49.4664010614], [3.0, 50.6410161514], [3.2, 51.77708764], [3.4, 52.8781778292], [3.6, 53.947331922], [3.8, 54.9871773792], [4.0, 56.0], [4.2, 56.9878030638], [4.4, 57.9523539268], [4.6, 58.8952211791], [4.8, 59.8178046004], [5.0, 60.72135955], [5.2, 61.607017004], [5.4, 62.4758001545]]], [105828, [[0.2, 40.94427191], [0.4, 44.6491106407], [1.2, 53.9089023002], [1.4, 55.6643191324], [1.6, 57.2982212813], [1.8, 58.83281573], [2.2, 61.6647939484], [2.4, 62.9838667697], [2.8, 65.4664010614], [3.0, 66.6410161514], [3.2, 67.77708764], [3.4, 68.8781778292], [3.6, 69.947331922], [3.8, 70.9871773792], [4.0, 72.0], [4.2, 72.9878030638], [4.6, 74.8952211791], [5.0, 76.72135955], [5.2, 77.607017004], [5.4, 78.4758001545], [5.6, 79.3286382648]]], [105830, [[0.2, 56.94427191], [1.0, 68.0], [2.4, 78.9838667697], [2.6, 80.2490309932], [2.8, 81.4664010614], [3.0, 82.6410161514], [3.2, 83.77708764], [3.6, 85.947331922], [3.8, 86.9871773792], [4.0, 88.0], [4.2, 88.9878030638], [4.4, 89.9523539268], [4.6, 90.8952211791], [4.8, 91.8178046004], [5.0, 92.72135955], [5.2, 93.607017004], [5.4, 94.4758001545]]], [105832, [[0.4, 76.6491106407], [0.6, 79.4919333848], [1.4, 87.6643191324], [1.6, 89.2982212813], [1.8, 90.83281573], [2.0, 92.2842712475], [2.2, 93.6647939484], [2.6, 96.2490309932], [2.8, 97.4664010614], [3.0, 98.6410161514], [3.2, 99.77708764], [3.4, 100.878177829], [3.6, 101.947331922], [4.0, 104.0], [4.2, 104.987803064], [4.4, 105.952353927], [4.8, 107.8178046], [5.0, 108.72135955], [5.2, 109.607017004], [5.4, 110.475800154], [5.8, 112.166378315], [6.0, 112.989794856], [6.2, 113.799598392]]]]
        self.read_charts(208499, True)
        return
        
        self.points = self.charts[0][1]
        
        print 'self.ui.graphicsView.width(), self.ui.graphicsView.height()', self.ui.graphicsView.width(), self.ui.graphicsView.height()
        self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.charts, 2)
                
#        ReportsExcel.BAX_coil2(self.charts)
        
#--and t1.id = 110006
#and t1.id = 208499


    def pushButton_2_Click(self):
        pass
        self.close()        



    def resizeEvent(self, event):
        if self.charts != None: 
            self.BieldScene(self.graphicsScene, self.ui.graphicsView.width(), self.ui.graphicsView.height(), self.charts, 2)
        pass


#    def add_device(self, i, activ, ind_name, ind_type, ind_measure, address, min_value):
#    def add_coils(self, i, activ, coil, accuracy):
    def add_coils(self, accuracy):
        
        strSQL = """
select t2.coilnumber, t2.tap
, cast(t2.coilnumber as varchar ) || 'И1-' || cast(t2.coilnumber as varchar ) || 'И' || cast(t2.tap as varchar )  as coil
from serial_number t1, coil t2
where t1.transformer = t2.transformer             
--and t1.id = 110006
and t1.id = 208499
--and t1.series = '43876'
--and t1.ordernumber = '17-02-339'                                                                  
order by t2.coilnumber                            
"""
        
        self.query.prepare(strSQL)
        if not self.query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки из БД", QMessageBox.Ok)
            return
        else:    
            model.setQuery(self.query)

        self.QuanCoil = model.rowCount()

        if self.QuanCoil < 1:
            return False
        
        for i in range(self.QuanCoil):
            activ = (i == 0)

            coilnumber     = int(model.record(i).field('coilnumber').value().toString())
            tap            = int(model.record(i).field('tap').value().toString())
            coilname       = str(coilnumber) + u'И1-' + str(coilnumber) + u'И' + str(tap)

#            QMessageBox.warning(self, u"Предупреждение", coilname, QMessageBox.Ok)

            self.Numbering += [QtGui.QRadioButton('  ' + str(coilnumber))]
            self.Numbering[i].setObjectName(str(i))
            self.Numbering[i].setChecked(activ)
            self.Numbering[i].setMaximumWidth(70)
#            self.Numbering[i].setMaximumWidth(30)
#            self.Numbering[i].setMaximumWidth(10)
            self.Numbering[i].setFont(self.fnt)
            self.Numbering[i].clicked.connect(self.checkBox_Click)
            self.Numbering[i].setVisible(False)

            self.Coil += [QtGui.QLineEdit()]
            self.Coil[i].setMaximumHeight(30)
            self.Coil[i].setText(coilname)
            self.Coil[i].setFont(self.fnt)
            self.Coil[i].setEnabled(activ)
            self.Coil[i].setReadOnly(True)
        
        #self.Names[i].changeEvent.connect(self.comboBox_changeEvent)
       # self.Coil[i].currentIndexChanged['int'].connect(self.comboBox_currentIndexChanged)
            self.Coil[i].setVisible(False)

                    
       # self.MinValues += [QtGui.QSpinBox()]
            self.MinLim += [QtGui.QDoubleSpinBox()]
            self.MinLim[i].setSingleStep(1)
            self.MinLim[i].setMaximum(100000)
            self.MinLim[i].setMinimum(0.00000)
            self.MinLim[i].setDecimals(5)
            self.MinLim[i].setValue(5.0)
            self.MinLim[i].setDecimals(2)                
            self.MinLim[i].setAlignment(QtCore.Qt.AlignCenter)
            self.MinLim[i].setMinimumWidth(100)
            self.MinLim[i].setFont(self.fnt)
            self.MinLim[i].setEnabled(activ)
            self.MinLim[i].setVisible(False)
            
            self.MaxLim += [QtGui.QDoubleSpinBox()]
            self.MaxLim[i].setSingleStep(1)
            self.MaxLim[i].setMaximum(100000)
            self.MaxLim[i].setMinimum(0.00000)
            self.MaxLim[i].setDecimals(5)
            self.MaxLim[i].setValue(5.0)
            self.MaxLim[i].setDecimals(2)                
            self.MaxLim[i].setAlignment(QtCore.Qt.AlignCenter)
            self.MaxLim[i].setMinimumWidth(100)
            self.MaxLim[i].setFont(self.fnt)
            self.MaxLim[i].setEnabled(activ)
            self.MaxLim[i].setVisible(False)
            
            #return
        



    '''
    def clear_coils(self):
#        for i in range(len(self.Numbering)):
        for i in range(self.QuanCoil):
            self.ui.gridLayout.removeWidget(self.Numbering[i])
            self.ui.gridLayout.removeWidget(self.Names[i])
            self.ui.gridLayout.removeWidget(self.Types[i])
            self.ui.gridLayout.removeWidget(self.Measures[i])
            self.ui.gridLayout.removeWidget(self.Address[i])
            #14.01
            self.ui.gridLayout.removeWidget(self.MinValues[i])
            self.ui.gridLayout.removeWidget(self.TestButtons[i])            
            
            self.Numbering[i].setVisible(False)
            self.Names[i].setVisible(False)
            self.Types[i].setVisible(False)
            self.Measures[i].setVisible(False)
            self.Address[i].setVisible(False)
            #14.01
            self.MinValues[i].setVisible(False)
            self.TestButtons[i].setVisible(False)
'''            
            

    def refresh_coils(self):
        for i in range(len(self.Numbering)):
            
            #QtGui.QLayoutItem.setAlignment(QtCore.Qt.AlignCenter)
            #QtGui.QGridLayout.itemAtPosition(int, int).
            
            self.ui.gridLayout.addWidget(self.Numbering[i], i + 2, 0)
            #continue
            self.ui.gridLayout.addWidget(self.Coil[i],   i + 2, 1)
            self.ui.gridLayout.addWidget(self.MinLim[i], i + 2, 2)
            self.ui.gridLayout.addWidget(self.MaxLim[i], i + 2, 3)
            #continue
            
            self.Numbering[i].setVisible(True)
            self.Coil[i].setVisible(True)
            self.MinLim[i].setVisible(True)
            self.MaxLim[i].setVisible(True)
            
            
#            for j in range(6):
#                self.ui.gridLayout.itemAtPosition(i+1, j+1).setAlignment(QtCore.Qt.AlignCenter)



    def read_charts(self, serial_number, LastTest):
#        from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
#        from PyQt4.QtGui import QMessageBox
#        import ReportsExcel
        #return
        '''
        self.query   = QSqlQuery(self.env.db)
        self.query_2 = QSqlQuery(self.env.db)
        self.query_3 = QSqlQuery(self.env.db)
        model   = QSqlQueryModel()
        model_2 = QSqlQueryModel()
        model_3 = QSqlQueryModel()
        '''

        self.charts = []

        strSQL = """
select series, ordernumber 
from serial_number
--where serialnumber = """ +  str(serial_number) + """                                                                  
--where id = 208941                                                                  
where id = """ +  str(serial_number) + """                                                                  
"""

        print strSQL

        self.query.prepare(strSQL)
        if not self.query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки из БД", QMessageBox.Ok)
            return
        else:    
            model.setQuery(self.query)

        if model.rowCount() < 1:
            return False
        series      = model.record(0).field('series').value().toString()
        ordernumber = model.record(0).field('ordernumber').value().toString()
        

        strSQL = """
select t1.id as checking_2, t1.item as itemID, t1.coil as coilID
, t3.coilnumber
, t3.tap
, cast(t3.coilnumber as varchar ) || 'И1-' || cast(t3.coilnumber as varchar ) || 'И' || cast(t3.tap as varchar )  as coil
, 1000 * t1.r as r            
, round(t1.un, 4) as un              
, round(t1.inom, 4) as inom                  
, t1.k
, t5.fio
, t2.createdatetime::date as sdate
from """ 

        if LastTest:
            strSQL += """
checking_2 t1 RIGHT OUTER JOIN (select max(t2.id) as id from item t1, checking_2 t2 where t1.id=t2.item group by serial_number, coil) t1_
ON (t1.id = t1_.id),"""
        else:
            strSQL += """checking_2 t1,"""

        strSQL += """
item t2, coil t3,
test_map t4 LEFT OUTER JOIN operator t5 ON (t4.operator = t5.id),
serial_number t6
where t1.item = t2.id             
and t1.coil = t3.id
and t2.test_map = t4.id
and t2.serial_number = t6.id
--and t6.series = '43876'
--and t6.ordernumber = '17-02-339'                                                                                                                                    
--and t6.series =  :series
--and t6.ordernumber = :ordernumber                                                                  
                                                                  
and t6.series = """ + "'" + series + "'" + """
and t6.ordernumber = """ + "'" + ordernumber + "'" + """                                                                  
                                                                  
order by t3.coilnumber                            
"""

        print 'series, ordernumber', series, ordernumber  
        print strSQL

        self.query_2.prepare(strSQL)
        #self.query_2.bindValue("series", series)
        #self.query_2.bindValue("ordernumber", ordernumber)
        if not self.query_2.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки из БД", QMessageBox.Ok)
            return
        else:    
            model_2.setQuery(self.query_2)

        #return
        
        self.charts = []
        for i in range(model_2.rowCount()):
            checking_2 = model_2.record(i).field('checking_2').value().toString()
            strSQL = """
select a, v
from checking_2sp
where checking_2 = :checking_2
order by id"""        
            self.query_3.prepare(strSQL)
            self.query_3.bindValue(":checking_2", checking_2)
            
            if not self.query_3.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки из БД", QMessageBox.Ok)
                return
            else:    
                model_3.setQuery(self.query_3)

#            self.charts += [[float(model_3.record(i).field('a').value().toString()), float(model_3.record(i).field('v').value().toString())]]
            
            points = []
            for j in range(model_3.rowCount()):
                points += [[float(model_3.record(j).field('a').value().toString()), float(model_3.record(j).field('v').value().toString())]]
                #checking_2 = model_2.record(i).field('checking_2').value().toString()

            self.charts += [[int(checking_2),points]]
#            self.charts += [[int(checking_2)]]
#            self.charts += [points]

            
            print 'model_3.rowCount()', model_3.rowCount()
#            self.charts += [int(checking_2)]
#            self.charts += [[float(model_3.record(i).field('a').value().toString()), float(model_3.record(i).field('v').value().toString())]]

            continue
    
        print 'self.charts', self.charts
        for i in range(len(self.charts)):
            print len(self.charts[i])
            print len(self.charts[i][1])
            print self.charts[i]
            print
            pass
            
        return    
                 
        coils = []
        points = []
        coilsInfa = []
        for i in range(model.rowCount()):
            checking_2 = int(model.record(i).field('checking_2').value().toString()) 
            coilID = int(model.record(i).field('coilID').value().toString())
            coilnumber = str(model.record(i).field('coilnumber').value().toString())
            tap = str(model.record(i).field('tap').value().toString())
                
            coils +=  [[coilID,
                        float(model.record(i).field('r').value().toString()), 
                        float(model.record(i).field('un').value().toString()), 
                        float(model.record(i).field('inom').value().toString()), 
                        float(model.record(i).field('k').value().toString())]]

            coilsInfa += [{}]
            coilsInfa[i]['coilnumber'] = int(model.record(i).field('coilnumber').value().toString())
            coilsInfa[i]['coil'] = coilnumber + u'И1' + '-' + coilnumber + u'И' + tap 
            coilsInfa[i]['points'] = []
                                                
            strSQL = """
select a, v
from checking_2sp
where checking_2 = :checking_2
order by id"""

            self.query_2.prepare(strSQL)
            self.query_2.bindValue(":checking_2", checking_2)
            if not self.query_2.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
                break
            else:    
                model_2.setQuery(self.query_2)

            for j in range(model_2.rowCount()):
                points += [[coilID, 
                            float(model_2.record(j).field('a').value().toString()), 
                            float(model_2.record(j).field('v').value().toString())]]
   
                coilsInfa[i]['points'] += [[float(model_2.record(j).field('a').value().toString()), 
                                            float(model_2.record(j).field('v').value().toString())]]
   
        for i in range(len(coilsInfa)): 
            print coilsInfa[i]

        return coilsInfa

        
        


    def checkBox_Click(self):
        for i in range(self.QuanCoil):
            self.Coil[i].setEnabled(False)
            self.MinLim[i].setEnabled(False)
            self.MaxLim[i].setEnabled(False)
            '''
            i = int(self.sender().objectName())
            check = self.sender().isChecked()
            self.Coil[i].setEnabled(check)
            self.Accuracy[i].setEnabled(check)            
        '''
            
        i = int(self.sender().objectName())
        check = self.sender().isChecked()
        self.Coil[i].setEnabled(check)
        self.MinLim[i].setEnabled(check)
        self.MaxLim[i].setEnabled(check)




    def BieldScene(self, scene, width, height, charts, mode):
        # mode = 1 - виден график целиком
        # mode = 2 - виден график до правой линии коридора 
        scene.clear()
        '''
        self.nomVoltage = None
        all_points = points + pre_points
        if len(all_points) < 1:
            return
        '''
                
        '''        
        maxX = all_points[0][0]
        maxY = all_points[0][1]
        for i in range(len(all_points)):
            if all_points[i][0] > maxX:
                maxX = all_points[i][0]
            if all_points[i][1] > maxY:
                maxY = all_points[i][1]
        '''        
        
        maxX = 0
        maxY = 0
        for i in range(len(charts)):
            for j in range(len(charts[i][1])):
                if charts[i][1][j][0] > maxX:
                    maxX = charts[i][1][j][0]
                if charts[i][1][j][1] > maxY:
                    maxY = charts[i][1][j][1]
                
                                
                
                
#        print '1maxX=', maxX
        '''        
        if mode == 1:                        
            if self.corridors != None and maxX < self.corridors['max_in']: 
                maxX = self.corridors['max_in']        
            if self.curr_inom != None and maxX < self.curr_inom:
                maxX = self.curr_inom
        else:            
            maxX_ = self.info.SecondCurrent    
            if self.corridors != None and maxX_ < self.corridors['max_in']: 
                maxX_ = self.corridors['max_in']        
            if self.curr_inom != None and maxX_ < self.curr_inom:
                maxX_ = self.curr_inom
            maxX = maxX_           
        '''
                     
        maxX *= 1.02 # Чтобы были видны линии коридоров  
        
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
                        
        print 'smXl, smYt, smXl, vH - smYb', smXl, smYt, smXl, vH - smYb                
        scene.addLine(smXl, smYt, smXl, vH - smYb, self.pen)
        scene.addLine(smXl, vH - smYb, vW - smXr, vH - smYb, self.pen)

        # Подписи осей
        #24.05.2016
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
                
        '''        
        # Линия номинального вторичного тока
        self.pen.setColor(QtCore.Qt.red)
        scene.addLine(smXl + round(self.info.SecondCurrent/kX), smYt,
                      smXl + round(self.info.SecondCurrent/kX), vH - smYb, self.pen)
                
        # Расчет номинального напряжения
        self.nomVoltage = self.calcNomVoltage(points, self.info.SecondCurrent)
                                                                                                 
        # Линия номинального напряжения образца
        if self.sample != None:
            self.pen.setColor(QtCore.Qt.green)
            scene.addLine(smXl, vH - smYt - round(self.sample['un']/kY), vW - smXr, vH - smYt - round(self.sample['un']/kY), self.pen)

        if self.curr_inom != None:
            scene.addLine(smXl + round(self.curr_inom/kX), smYt,
                          smXl + round(self.curr_inom/kX), vH - smYb, self.pen)
        '''
        
        self.pen.setWidth(1)
        self.pen.setColor(QtCore.Qt.black)
        # Кривая текущего испытания
        '''
        self.pen.setColor(QtCore.Qt.black)
        for i in range(len(points) - 1):
            scene.addLine(smXl + round(points[i][0]/kX), vH - smYt - round(points[i][1]/kY),
                          smXl + round(points[i+1][0]/kX), vH - smYt - round(points[i+1][1]/kY), self.pen)
        '''
        
        for i in range(len(charts)):
            for j in range(len(charts[i][1]) - 1):
                scene.addLine(smXl + round(charts[i][1][j][0]/kX), vH - smYt - round(charts[i][1][j][1]/kY),
                              smXl + round(charts[i][1][j+1][0]/kX), vH - smYt - round(charts[i][1][j+1][1]/kY), self.pen)
                


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
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
    
    db = env.db

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
        wind = DifProtect(env, 'TRANSFORM')
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
