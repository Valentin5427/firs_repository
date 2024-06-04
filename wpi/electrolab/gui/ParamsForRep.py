# -*- coding: UTF-8 -*-
#
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt

import socket
import PyQt4
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.ClsTrans import ClsTrans

import ui.ico_64_rc

import datetime

from datetime import date

from PyQt4.QtGui import QTableView


id_params = -1
model   = QSqlQueryModel()
withCol1 = 100
withCol2 = 30
row = -1


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
        global VSB1     #, VSB2, VSB3, VSB4
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False




class ParamsForRep(QWidget, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"ParamsForRep.ui")        
        
        self.setWindowTitle(u"Параметры для отчетов")
                        
                        
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_4.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_5.setIcon(QIcon(u':/ico/ico/trash_64.png'))
                        
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)

#        QtGui.QPushButton.changeEvent()

#        self.ui.checkBox.toggled.connect(self.checkBox_Toggle)

        self.ui.radioButton.toggled.connect(self.radioButton_Toggle)
        self.ui.radioButton_2.toggled.connect(self.radioButton_Toggle)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')

        self.ui.lineEdit.textChanged.connect(self.textChanged)
        self.ui.dateEdit.dateChanged.connect(self.textChanged)


        # Организация контекстного меню на кнопке "Добавить"
        fnt = QtGui.QFont()
        fnt.setPointSize(14)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Добавить с копированием', self))
        self.mnu.setFont(fnt)        
        self.ui.pushButton_3.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.ui.pushButton_3.customContextMenuRequested.connect(self.on_context_menu)      
        self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.pushButton_3_Click_copy)


#############        self.dateEdit.setCalendarPopup(1)
        self.view(True)

        #QtGui.QDateEdit.datec

#        self.ui.tableView.setModel(model)        
#        self.selModel = self.ui.tableView.selectionModel()                

        self.selParams()
        
        
    def on_context_menu(self, point):
        self.mnu.exec_(self.ui.pushButton_3.mapToGlobal(point))
        
             
    def view(self, enable):
        pass         
        self.ui.groupBox.setEnabled(not enable)
        self.ui.pushButton_3.setEnabled(enable)
        self.ui.pushButton_4.setEnabled(enable)
        self.ui.pushButton_5.setEnabled(enable)
        self.ui.radioButton.setEnabled(enable)
        self.ui.radioButton_2.setEnabled(enable)
        self.ui.tableView.setEnabled(enable)
        if enable:
            self.ui.groupBox.setTitle(u'')
            self.ui.lineEdit.setText("")        
            self.ui.dateEdit.setDate(datetime.date(2000, 1, 1))        
             
             
    def pushButton_3_Click(self):
        self.view(False)
        self.tag = 1
        self.ui.groupBox.setTitle(u'Добавление нового параметра')        
        self.ui.lineEdit.setText("")        
        self.ui.dateEdit.setDate(datetime.date.today())        

            

    def pushButton_3_Click_copy(self):
#        global row        
        self.view(False)
        self.tag = 1
        self.ui.groupBox.setTitle(u'Добавление нового параметра')
        row = self.selModel.currentIndex().row()
        self.ui.lineEdit.setText(model.record(row).field('name').value().toString())  
        self.ui.dateEdit.setDate(datetime.date.today())        

                
    def pushButton_4_Click(self):
        global id_params
        global row
        self.view(False)
        self.tag = 2
        self.ui.groupBox.setTitle(u'Редактирование текущего параметра')
        row = self.selModel.currentIndex().row()
               
        id_params = int(model.record(row).field('id').value().toString())        
        self.ui.lineEdit.setText(model.record(row).field('name').value().toString())  
        self.ui.dateEdit.setDate(model.record(row).field('date_begin').value().toDate())

            
                                                        
    def pushButton_5_Click(self):
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM params WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selParams()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    

                          
                          
                          
                          
             
    def pushButton_Click(self):
#        global id_param
        global row
                        
        if self.ui.lineEdit.text().trimmed() == '':
            QMessageBox.warning(self, u"Предупреждение",  u'Введи наименование параметра', QMessageBox.Ok)
            return

#        global isSave      1)
        query = QSqlQuery(db1)

        if self.tag == 1:
            SQL = '''INSERT INTO params (name, date_begin, clsparams)
                                 values (:name, :date_begin, :clsparams)'''            
                                
            query.prepare(SQL)
        else:
            SQL ='''UPDATE params SET name = :name,
                                      date_begin = :date_begin,
                                      clsparams = :clsparams
                    WHERE id = :id'''                
                                
            query.prepare(SQL)
            query.bindValue(":id", id_params);
                
        query.bindValue(":name", self.ui.lineEdit.text())
        if self.ui.dateEdit.date() > datetime.date(2000, 1, 1):
            query.bindValue(":date_begin", self.ui.dateEdit.date())
        else:
            query.bindValue(":date_begin", None)
        
        if self.ui.radioButton.isChecked():
            query.bindValue(":clsparams", 1)
        else:    
            query.bindValue(":clsparams", 2)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            return
            
        self.selParams()
        
        
        if self.tag == 2:
            self.ui.tableView.selectRow(row)                                            
        
        
        self.view(True)
            
                
    def pushButton_2_Click(self):
        self.view(True)
                        
                        
    def radioButton_Toggle(self, check):
        self.selParams()
                        
            
    def selParams(self):        
        query = QSqlQuery(db1)
                                
        SQL = """select id, name, date_begin from params where clsparams = :clsparams order by date_begin, id"""
                
        query.prepare(SQL)        
        
        if self.ui.radioButton.isChecked():
            query.bindValue(":clsparams", 1)
        else:    
            query.bindValue(":clsparams", 2)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            return
            
        model.setQuery(query)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование параметра")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Дата начала действия")
        
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        
        self.ui.tableView.setColumnHidden(0, True)
                
        self.ui.tableView.setFocus()
        
#        QtGui.QTableView.
  #      QSqlQueryModel
                
    #      self.ui.pushButton_4.setEnabled(enable)
    #      self.ui.pushButton_5.setEnabled(enable)
        self.ui.tableView.selectRow(0)
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_4.setEnabled(enab)
        self.ui.pushButton_5.setEnabled(enab)

                
                
                

    def textChanged(self):
        pass
     #   self.ui.pushButton.setEnabled(True) 
     #   self.ui.pushButton_2.setEnabled(True) 


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
        wind = ParamsForRep(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
