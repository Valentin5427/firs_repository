# -*- coding: UTF-8 -*-work
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont,       QDoubleSpinBox,         QToolButton
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from serial import Serial
from serial.serialutil import SerialException
from electrolab.app.item import Item

from dpframe.tech.SimpleSound import SimpleSound

from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
from electrolab.app.item import Item
from devices import Devices, crc16
from win32com.client import Dispatch
import struct

import json
import math
import time
import datetime


model_2 = QSqlQueryModel()

#QtGui.QTableView.setpa
#QtGui.QPalette.

class TestHighVoltage(QWidget, UILoader):    
    def __init__(self, _env, oMap, tvItem, tvCoil, btnStart, VerificationForm):
#    def __init__(self, _env, oMap, idStand, tvItem, btnStart, VerificationForm):
        
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"TestHighVoltage.ui")
        self.setEnabled(False)
        self.idStand = None
        self.idItem = None
        self.oMap = oMap
        
        #self.idStand = idStand        
        print 'self.idStand = ', self.idStand        
                
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)        
        
        self.ui.pushButton.setVisible(False)        
        self.ui.pushButton_2.setVisible(False)        
        self.ui.pushButton_3.setVisible(False)        
        self.ui.tableView.setVisible(False)        
        
        
        
        self.query_2 = QSqlQuery(_env.db)
        self.query_9 = QSqlQuery(_env.db)
        self.tvItem = tvItem
        
        if self.oMap == None:
            return
        self.oItem = Item(_env, None, self.oMap.iMapID, True)
                
        self.ui.lineEdit.returnPressed.connect(self.returnPress)        
        if not self.TestBase(_env.db):
            return

        
    def get_standId(self, idStand):
        self.idStand = idStand
        
        
    def returnPress(self):
        try:
            if self.ui.lineEdit.text().trimmed() == '':
                self.curr_pdl = 0
            else:    
                self.curr_pdl  = float(self.ui.lineEdit.text())
        except Exception:
            QMessageBox.warning(self, u"Предупреждение",  u'Величина сопротивления: ' + self.ui.lineEdit.text() + u' не корректна', QMessageBox.Ok)
            return        
        self.savePDL()
        
        self.move_item_coil(False)

        
    def savePDL(self):            
        if model_2.rowCount() < 1:
            self.query_9.prepare('INSERT INTO checking_3 (stand, item, pdl) values (:stand, :item, :pdl)')            
            self.query_9.bindValue(":stand", self.idStand)
            self.query_9.bindValue(":item", self.idItem)
        else:
            if self.ui.lineEdit.text() == model_2.record(0).field('pdl').value().toString():
                return  # Если значение не поменялось, не сохранять
                        
            id = int(model_2.record(0).field('id').value().toString())
            self.query_9.prepare('UPDATE checking_3 SET pdl=:pdl WHERE id=:id')            
            self.query_9.bindValue(":id", id)
                
        if self.ui.lineEdit.text().trimmed() == '':
            self.query_9.bindValue(":pdl", None)
        else:                
            self.query_9.bindValue(":pdl", self.curr_pdl)
                                
        if not self.query_9.exec_():
            QMessageBox.warning(None, u"Предупреждение",
            u"Ошибка сохранения значения уровня частичных разрядов в БД",
            QMessageBox.Ok)
        else:
            self.oItem.set_done(self.idItem)
            self.oMap.mapRefresh.emit()
                
        
        
    def pushButton_Click(self):
        print 'self.idItem1=', self.idItem
        self.oItem.set_done(self.idItem)
#        return
        self.oMap.mapRefresh.emit()
        print 11
            
    def pushButton_2_Click(self):
        print 'self.idItem2=', self.idItem
        self.oItem.set_noteste(self.idItem)        
        self.oMap.mapRefresh.emit()
        print 21

    def pushButton_3_Click(self):
        print 'self.oItem.stateItem=', self.oItem.stateItem

    def item_change_row(self, idItem):
#        print 'item_change_row', idItem, self.idStand
        self.idItem = idItem
        #self.defectItem = False

    
        model_2.clear()
        strSQL = """
select id, pdl
from checking_3
where stand = :stand
and item = :item
"""
        self.query_2.prepare(strSQL)
        self.query_2.bindValue(":stand", self.idStand)
        self.query_2.bindValue(":item", self.idItem)
        if not self.query_2.exec_():
            raise Exception(self.query_2.lastError().text())
            return
        else:    
            model_2.setQuery(self.query_2)

        if model_2.rowCount() < 1:
            self.curr_pdl  = None
            self.ui.lineEdit.setText('')            
            self.checking_3 = None
            
            self.oItem.stateItem = self.oItem.NOTESTE
            
        else:            
            self.curr_pdl  = float(model_2.record(0).field('pdl').value().toString())
            self.ui.lineEdit.setText(str(self.curr_pdl))

            self.oItem.stateItem = self.oItem.DONE





#        self.ui.lineEdit.setStyleSheet("background-color: lightgreen")

#        self.ui.lineEdit.setStyleSheet("background-color: lightgreen")
#        print 'type(self.tvItem)=', type(self.tvItem)


    def move_item_coil(self, isTested):
        if self.tvItem.table.currentIndex().row() < self.tvItem.get_row_count() - 1:                
            self.tvItem.table.selectRow(self.tvItem.table.currentIndex().row() + 1)
        else:    
            self.tvItem.table.selectRow(0)
       # self.tvItem.setEnabled(False)
        
        '''
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
'''

    def TestBase(self, db):
        query = QSqlQuery(db)
        print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        query.prepare("select * from checking_3")
        if not query.exec_(): err_tbl += "checking_3\n"
          
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
        print u"Инициализация БД"        
        query = QSqlQuery(db)

        SQL = u"""
CREATE TABLE checking_3
(
  id serial PRIMARY KEY,
  stand integer REFERENCES stand,
  item integer REFERENCES item,
  pdl numeric(10,2)
);

COMMENT ON TABLE checking_3 IS 'Результаты высоковольтных испытаний трансформаторов тока';
COMMENT ON COLUMN checking_3.id IS 'Первичный ключ';
COMMENT ON COLUMN checking_3.stand IS 'Ссылка на тип испытания';
COMMENT ON COLUMN checking_3.item IS 'Ссылка на изделие';
COMMENT ON COLUMN checking_3.pdl IS 'Уровени ЧР (частичных разрядов)';
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
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
    class ForEnv(QtGui.QWidget):
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
                                
        wind = TestHighVoltage(env, None, None, None, None, None)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())

#Калькулятор преобразования чисел
#http://www.binaryconvert.com/convert_float.html#

#представление чисел
#https://server.179.ru/tasks/python/2017b2/22-float.html
#http://dic.academic.ru/dic.nsf/ruwiki/432703
#https://ru.wikipedia.org/wiki/%D0%A7%D0%B8%D1%81%D0%BB%D0%BE_%D0%BE%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%BE%D0%B9_%D1%82%D0%BE%D1%87%D0%BD%D0%BE%D1%81%D1%82%D0%B8
#http://www.softelectro.ru/ieee754.html

# Битовые операции
#http://ru.stackoverflow.com/questions/297129/%D0%91%D0%B8%D1%82%D0%BE%D0%B2%D1%8B%D0%B5-%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8

'''        
>>> import struct
>>> struct.unpack('f', '0000A040'.decode('hex'))[0]
5.0
>>> struct.unpack('f', '\x00\x00\xa0\x40')[0]
5.0
'''        
