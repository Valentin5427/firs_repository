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

id_test_type = -1

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()

from PyQt4.QtGui import QTableView
#from PyQt4.QtGui import QTextEdit

withCol1 = 20
withCol2 = 100
withCol3 = 200

isSave = False

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
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False


class sprTypeTest(QWidget, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprTester.ui")        
        
        self.setWindowTitle(u"Справочник помещений")
                
        self.ui.groupBox.setVisible(False)        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')
        self.selRoom()
      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()
      
# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editTypeTest(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового помещения')
        row = self.selModel.currentIndex().row()
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selRoom()
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM test_type");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            
                
    def pushButton_2_Click(self):
        global isSave        
        global id_test_type
        self.wind = self.editTypeTest(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего помещения')
        row = self.selModel.currentIndex().row()
               
        id_test_type = int(model.record(row).field('id').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('name').value().toString())        
        self.wind.ui.spinBox.setValue(int(model.record(row).field('code').value().toString()))
        self.wind.ui.lineEdit_2.setText(model.record(row).field('description').value().toString())        
                        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selRoom()
            self.ui.tableView.selectRow(row)                                            


    def pushButton_3_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM test_type WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selRoom()                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
            
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
            model.query().first();
            i = 0
            while model.query().value(0).toString() != id_search:
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
            tableView.selectRow(i)
            
    def selRoom(self):        
        query = QSqlQuery(db1)
                                
        SQL = """select id,
        code,
        name,
        description
        from test_type
        order by id
        """
        query.prepare(SQL)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Код")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Наименование")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Описание")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        self.ui.tableView.setColumnWidth(3,  withCol3)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)


# Редактирование помещений (начало кода)        
                        
    class editTypeTest(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editTypeTest.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)

        
        def pushButton_Click(self):
            global id_test_type
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи наименование', QMessageBox.Ok)
                return
            if self.ui.spinBox.value() < 0:
                QMessageBox.warning(self, u"Предупреждение",  u'Введи номер', QMessageBox.Ok)
                return
                
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO test_type (name, code, description)
                                            values (:name, :code, :description)'''                                            
                query.prepare(SQL)
            else:
                SQL ='''UPDATE test_type SET name = :name,
                                                   code = :code,
                                                   description = :description
                                 WHERE id = :id'''                
                                
                query.prepare(SQL)

                query.bindValue(":id", id_test_type);
                
                
            query.bindValue(":name", self.ui.lineEdit.text())            
            query.bindValue(":code", self.ui.spinBox.value())            
            query.bindValue(":description", self.ui.lineEdit_2.text())                                    
                        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()                            
# Редактирование помещений (конец кода)        
                

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
        wind = sprTypeTest(env)
        wind.setEnabled(True)
        wind.ui.pushButton_4.setVisible(False)
        wind.ui.pushButton_5.setVisible(False)
        wind.setWindowTitle(u'Типы испытаний')
        wind.show()
        sys.exit(app.exec_())
