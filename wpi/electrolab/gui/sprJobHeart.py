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
from electrolab.gui.ReportsExcel import  fill_report_apg

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
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False

'''
class ClsTrans(QtGui.QDialog, UILoader):
    def __init__(self, _env, sw, *args):
        QtGui.QDialog.__init__(self, *args)        

class sprTester(QWidget, UILoader):    
    def __init__(self, _env):
'''
   
class sprJob(QDialog, UILoader):
    def __init__(self, _env, *args):
        QDialog.__init__(self, *args)
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprHeartJob.ui")

        self.ui.dateEdit.setDate(datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day-1))
        self.ui.dateEdit_2.setDate(datetime.date.today())

        modelCB.setQuery("select  NULL, 'Все' UNION ALL SELECT id , name  from machine_heart",db1)
        self.itemsOwens  = {}
        for i  in range(modelCB.rowCount()):
            self.itemsOwens[modelCB.index(i,1).data()] = modelCB.index(i,0).data()
        print(self.itemsOwens)
        self.ui.comboBox.addItems(list(self.itemsOwens.keys()))


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

        self.ui.comboBox.activated.connect(self.change_comboBox)

        # self.ui.comboBox.activated.connect(lambda:  self.selHeart(currColumnIndex, False))
        # self.ui.comboBox_2.activated.connect(lambda: self.selHeart(currColumnIndex, False))
        self.ui.pushButton.clicked.connect(self.fill_report)

        self.horizontalHeader = self.ui.tableView.horizontalHeader()
      
        self.IS_SELECT = False
        self.selected_rows = 0

      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)
      
        self.ui.tableView.clearSelection()

        self.ui.dateEdit.dateChanged.connect(lambda: self.selHeart(currColumnIndex,False))
        self.ui.dateEdit_2.dateChanged.connect(lambda: self.selHeart(currColumnIndex, False))




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

    def change_comboBox(self):
        self.selHeart(currColumnIndex, False)









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


        SQL = """
        select readings_machine_heart.id,
       machine_heart.name,
       readings_machine_heart.date_on ::date,
       to_char(age(readings_machine_heart.date_off , readings_machine_heart.date_on),'HH24:MI:SS' ) as job,
       readings_machine_heart.id,
       readings_machine_heart.date_on ::date ,
       readings_machine_heart.date_on,
       readings_machine_heart.date_off


from readings_machine_heart
        inner join machine_heart  on readings_machine_heart.machine_id = machine_heart.id
         where readings_machine_heart.date_on between to_date('""" + self.ui.dateEdit.text() + """','dd.mm.yyyy') and to_date('""" + self.ui.dateEdit_2.text() + """','dd.mm.yyyy') + 1
        """

        # if self.ui.comboBox.currentIndex() != 0:
        #     print(self.itemsOwens)
        #     SQL += f' and owens_apg.id  = {self.itemsOwens[self.ui.comboBox.currentText()]}'
        #
        #
        # if self.ui.comboBox_2.currentIndex() != 0:
        #     SQL += f' and sensors_apg.id  = {self.itemsSensors[self.ui.comboBox_2.currentText()]}'
        #
        #
        # if columnIndex == 1:
        #     SQL += """order by owens_apg.name """ + desc
        #
        #
        # if columnIndex == 2:
        #     SQL += """order by sensors_apg.name """ + desc
        #
        # if columnIndex == 3:
        #     SQL += """order by readings_apg.set_value """ + desc
        #
        # if columnIndex == 4:
        #     SQL += """order by readings_apg.present_value """ + desc
        #
        # if columnIndex == 5:
        #     SQL += """order by readings_apg.date """ + desc
        #
        #

        query.prepare(SQL)

        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)

        model.setQuery(query)

        print(SQL)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Станок")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Дата")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Время работы")


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
        self.ui.tableView.setColumnHidden(4, True)
        self.ui.tableView.setColumnHidden(5, True)
        self.ui.tableView.setColumnHidden(6, True)
        self.ui.tableView.setColumnHidden(7, True)
        self.ui.tableView.setColumnHidden(8, True)
        self.ui.tableView.setColumnHidden(11, True)
        self.ui.tableView.setColumnHidden(12, True)
        self.ui.tableView.setColumnHidden(13, True)
        self.ui.tableView.selectRow(0)
                


    def checkBox_Toggle(self, check):
        self.selHeart(currColumnIndex, False)



    def fill_report(self):
        fill_report_apg(model)






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

        wind = sprJob(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())

