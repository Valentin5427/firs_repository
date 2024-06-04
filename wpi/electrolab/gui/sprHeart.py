# -*- coding: UTF-8 -*-
#

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import  QKeyEvent, QIcon, QFont
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  *

import socket

hostname = socket.gethostname()

from electrolab.gui.common import UILoader


import electrolab.gui.ui.ico_64_rc

import datetime

from datetime import date
from electrolab.gui.ReportsExcel import  fill_report_heart

id_operator = -1

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
modelCB = QSqlQueryModel()





withCol1 = 100
withCol2 = 100
withCol3 = 100
withCol4 = 100
withCol5 = 100
withCol6 = 100
withCol7 = 100
withCol8 = 100
withCol9 = 100
withCol10 = 100

isSave = False

def noneValue(v):
    if v == '':
        return None
    else:
        return v

def spaceValue(field):
    if field.isNull():
        return ''
    else:
        return field.value().toString()

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
        global VSB1, VSB2, VSB3, VSB4
        
        if obj.objectName() == 'tv1' and (e.type() != QtCore.QEvent.Resize or VSB1 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7 + withCol9))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            obj.setColumnWidth(5, koef * withCol5)
            obj.setColumnWidth(6, koef * withCol6)
            obj.setColumnWidth(7, koef * withCol7)
            obj.setColumnWidth(9, koef * withCol9)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False

'''
class ClsTrans(QtGui.QDialog, UILoader):
    def __init__(self, _env, sw, *args):
        QtGui.QDialog.__init__(self, *args)        

class sprTester(QWidget, UILoader):    
    def __init__(self, _env):
'''
   
class sprHeart(QDialog, UILoader):
    def __init__(self, _env, *args):
        QDialog.__init__(self, *args)
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprHeart.ui")


        modelCB.setQuery("select  NULL, 'Любая' UNION ALL SELECT id,mark || ' ' || case when grade_iron.feature is Null then '' else grade_iron.feature end feature  from grade_iron",db1)
        self.itemsCB = {}
        for i  in range(modelCB.rowCount()):
            self.itemsCB[modelCB.index(i,1).data()] = modelCB.index(i,0).data()
        print(self.itemsCB)
        self.ui.comboBox.addItems(list(self.itemsCB.keys()))


        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()
        self.ui.tableView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')

        self.ui.tableView.clicked.connect(self.select_rows)

        global currColumnIndex
        currColumnIndex = 0
        global desc
        desc = ''
        self.selHeart(currColumnIndex, False)
        self.ui.comboBox.currentIndexChanged.connect(lambda:  self.selHeart(currColumnIndex, False))
        self.ui.lineEdit.textChanged.connect(lambda:  self.selHeart(currColumnIndex, False))
        self.ui.pushButton.clicked.connect(self.fill_report)

        self.horizontalHeader = self.ui.tableView.horizontalHeader()
      
        self.IS_SELECT = False
        self.selected_rows = 0

      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)
      
        self.ui.tableView.clearSelection()

       # QtGui.QTableView.horizontalHeader()



    def textChanged_lineEdit(self):
        '%" + self.lineEdit.text() + "%'


        text = self.ui.lineEdit.text()

        text = text.replace('x','%') # латинская
        text = text.replace('X', '%')  # ЛАТИНСКАЯ
        text = text.replace('х', '%')  # кириллица
        text = text.replace('Х', '%')  # КИРИЛЛИЦА
        print(f'%{text}%')








    def select_rows(self):
        lst = []
        rows = self.selModel.selectedIndexes()
        for index in rows:
            lst.append(self.ui.tableView.model().index(index.row(),0).data())
        return set(lst)






    def sortByColumn(self, columnIndex):
#        print 'sortByColumn sortByColumn sortByColumn sortByColumn sortByColumn  ', columnIndex , desc
        self.selHeart(columnIndex, False)
     
      
      
              

            
    # Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
    def searchInModel(self, id_search, tableView, model):
        if id_search == -1:  # При удалении записи
            return
        if id_search == 0:
            if int(model.query().size()) > 0:   # Грубая защита от ошибки позиционирования ???????????????
                tableView.selectRow(0)
        else:
            if int(model.query().size()) < 1:  # Грубая защита от зацикливания
                return
            # Навигация на измененную позицию
            model.query().first()
            i = 0
            while model.query().value(0) != id_search:
                #print model.query().value(0).toString()
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
            tableView.selectRow(i)
            
    def selHeart(self, columnIndex, isEdit):
        global currColumnIndex
        global desc
        
        query = QSqlQuery(db1)
                                
        if not isEdit:
            if currColumnIndex == columnIndex:
                if desc == '':
                    desc = 'desc'
                else:            
                    desc = ''
            else:        
                    desc = ''
                                
        currColumnIndex = columnIndex
        print(646464, str(self.ui.comboBox.currentText()))


        SQL = """select heart.id,   cast(grade_iron.mark as varchar) || ' ' || case when grade_iron.feature is Null then '' else grade_iron.feature end feature  ,   out_diameter,  heart.in_diameter, heart.height, heart_sample.num, heart_sample.voltage, heart_accounting.createdatetime, grade_iron.mark, heart_accounting.amount  from heart_accounting
            inner join 
                    heart on heart_accounting.id_heart = heart.id
            inner join
                    grade_iron on heart.id_grade = grade_iron.id
            inner join 
                  heart_sample on heart_accounting.id_sample = heart_sample.id
                  
            
        """

        if self.ui.comboBox.currentIndex() != 0:
            SQL += f'where heart.id_grade = {self.itemsCB[self.ui.comboBox.currentText()]}'

        if self.ui.lineEdit.text() != '':
            text = self.ui.lineEdit.text()
            text = text.replace('x', '%')  # латинская
            text = text.replace('X', '%')  # ЛАТИНСКАЯ
            text = text.replace('х', '%')  # кириллица
            text = text.replace('Х', '%')  # КИРИЛЛИЦА
            if self.ui.comboBox.currentIndex() != 0:
                SQL += f"and heart.sizes LIKE '%{text}%'"
            else:
                SQL += f"where heart.sizes LIKE '%{text}%'"






        print(3234, columnIndex, desc)

        if columnIndex == 2:
            SQL += """order by heart.out_diameter """ + desc

        if columnIndex == 3:
            SQL += """order by heart.heart.in_diameter """ + desc

        if columnIndex == 4:
            SQL += """order by heart.heart.height """ + desc

        if columnIndex == 5:
            SQL += """order by heart_sample.num """ + desc

        if columnIndex == 6:
            SQL += """order by heart_sample.voltage """ + desc

        if columnIndex == 7:
            SQL += """order by heart_accounting.createdatetime """ + desc


        query.prepare(SQL)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        print(SQL)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Тип стали")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Внешний диаметр")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Внутренний диаметр")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Высота")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"№ графика")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Значение \n намагниченности")
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Дата \n проверки")
        model.setHeaderData(9, QtCore.Qt.Horizontal, u"Количество")

            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        self.ui.tableView.setColumnWidth(3,  withCol3)
        self.ui.tableView.setColumnWidth(4,  withCol4)
        self.ui.tableView.setColumnWidth(5,  withCol5)
        self.ui.tableView.setColumnWidth(6,  withCol6)
        self.ui.tableView.setColumnWidth(7,  withCol7)
        self.ui.tableView.setColumnWidth(8,  withCol8)
        self.ui.tableView.setColumnWidth(9,  withCol9)
        self.ui.tableView.setColumnWidth(10,  withCol10)

        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(8, True)
        self.ui.tableView.setColumnHidden(11, True)
        self.ui.tableView.setColumnHidden(12, True)
        self.ui.tableView.setColumnHidden(13, True)
        self.ui.tableView.selectRow(0)
                


    def checkBox_Toggle(self, check):
        self.selHeart(currColumnIndex, False)



    def fill_report(self):
        fill_report_heart(model)






def excepthook(exc_type, exc_value, exc_tb):
    import traceback
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    QMessageBox.warning(None, u"Ошибка!!!!!", tb, QMessageBox.Ok)

import sys
sys.excepthook = excepthook



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
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
        
        wind = sprHeart(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())

