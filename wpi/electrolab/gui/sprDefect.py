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

id_defect = -1

#model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()


#QtGui.QTableView.text
#QSqlQueryModel.co

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 10
withCol2 = 25
withCol3 = 100
withCol4 = 100

withCol_1 = 30
withCol_2 = 20
withCol_3 = 100
withCol_4 = 100

isSave = False

'''
def noneValue(v):
    if v.trimmed() == '':
        return None
    else:
        return v.trimmed()

def spaceValue(field):
    if field.isNull():
        return ''
    else:
        return field.value().toString()
'''

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
        global VSB1, VSB2
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4))
            obj.setColumnWidth(2, koef * withCol1)
            obj.setColumnWidth(3, koef * withCol2)
            obj.setColumnWidth(4, koef * withCol3)
            obj.setColumnWidth(5, koef * withCol4)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4))
            obj.setColumnWidth(2, koef * withCol_1)
            obj.setColumnWidth(3, koef * withCol_2)
            obj.setColumnWidth(4, koef * withCol_3)
            obj.setColumnWidth(5, koef * withCol_4)
            VSB2 = obj.verticalScrollBar().isVisible()

        return False


class sprDefect(QWidget, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprDefect.ui")        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)

        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()                
        self.connect(self.selModel_2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_2)


        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))

        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setObjectName('tv2')
        
        global currColumnIndex
        currColumnIndex = 0
        global desc
        desc = ''
        self.selDefect(currColumnIndex, False)
            

# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editDefect(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового несоответствие')
        row = self.selModel.currentIndex().row()
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selDefect(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM defect");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            

                
    def pushButton_2_Click(self):
        global isSave        
        global id_defect
        self.wind = self.editDefect(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего несоответствия')
        row = self.selModel.currentIndex().row()
               
        id_defect = int(model.record(row).field('id').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('defecttype').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('fullname').value().toString())        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('description').value().toString())        
        self.wind.ui.checkBox.setChecked(bool(int(model.record(row).field('iscrit').value().toString())))        
                
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selDefect(currColumnIndex, True)
            self.ui.tableView.selectRow(row)                                            


    def pushButton_3_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            '''
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале обмотки!', QMessageBox.Ok)
                return
                '''
            SQL = "DELETE FROM defect WHERE id = :ID"
            query = QSqlQuery(db1)
            query.prepare(SQL)
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
#            query.exec_()
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
                return
            
            
            
            self.selDefect(currColumnIndex, True)
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                        

    def pushButton_4_Click(self):
#        row_type = self.selModel_2.currentIndex().row()
        query = QSqlQuery(db1)
        row = self.selModel_2.currentIndex().row()
        id_type_test = model_2.record(row).field('id').value().toString()                
        if self.bind:
            SQL = "DELETE FROM defect_test_type  WHERE id = :ID"            
            query.prepare(SQL)
            query.bindValue(":id", model_2.record(row).field('id_').value().toString());                                
        else:
            SQL = "INSERT INTO defect_test_type (defect, test_type) values (:defect, :test_type)"
            query.prepare(SQL)
            query.bindValue(":defect", model.record(self.selModel.currentIndex().row()).field('id').value().toString())
            query.bindValue(":test_type", model_2.record(row).field('id').value().toString())
                        
#        print SQL
                        
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            return

        self.selTestType()
        
        
        model_2.query().first();
        i = 0
        while model_2.query().value(0).toString() != id_type_test:
            model_2.query().next()
            if i + 1 == int(model_2.query().size()):
                break
            i += 1
        self.ui.tableView_2.selectRow(i)
    

                                                            
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
                #print model.query().value(0).toString()
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
            tableView.selectRow(i)
                       
                                    
    # Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
    def searchInModel_2(self, id_search, tableView, model):
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
                #print model.query().value(0).toString()
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
            tableView.selectRow(i)
                                    

    def selDefect(self, columnIndex, isEdit):
        global currColumnIndex
        global desc
        
        currColumnIndex = columnIndex        
        print 'columnIndex = ', columnIndex
        
        query = QSqlQuery(db1)
                                
        SQL = """select id,
        case when iscritical then 1 else 0 end as iscrit,
        defecttype,
        iscritical,
        fullname,
        description
        from defect
        order by defecttype, fullname
        """

        print SQL       
        query.prepare(SQL)

        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Тип")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Критичность")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Полное наименование")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Описание")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(2,  withCol1)
        self.ui.tableView.setColumnWidth(3,  withCol2)
        self.ui.tableView.setColumnWidth(4,  withCol3)
        self.ui.tableView.setColumnWidth(5,  withCol4)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
#        self.ui.tableView.setColumnHidden(3, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        print 7



    def selTestType(self):
        '''
        global currColumnIndex
        global desc
        
        currColumnIndex = columnIndex        
        print 'columnIndex = ', columnIndex
        '''
        global id_defect

        query = QSqlQuery(db1)                                
        SQL = u"""select t1.id, t2.id as id_, case when t2.id is null then '' else 'ПРИВЯЗАНО' end as bind, t1.code, t1.name, t1.description
                from test_type as t1 left outer join (select * from defect_test_type where defect = :defect) as t2 on (t1.id = t2.test_type)
                order by t1.code
        """

        print SQL       
        query.prepare(SQL)
        query.bindValue(":defect", id_defect);                                

        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model_2.setQuery(query)

        model_2.setHeaderData(2, QtCore.Qt.Horizontal, u"Привязка")
        model_2.setHeaderData(3, QtCore.Qt.Horizontal, u"Код")
        model_2.setHeaderData(4, QtCore.Qt.Horizontal, u"Наименование")
        model_2.setHeaderData(5, QtCore.Qt.Horizontal, u"Описание")
            
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView_2.setColumnWidth(2,  withCol_1)
        self.ui.tableView_2.setColumnWidth(3,  withCol_2)
        self.ui.tableView_2.setColumnWidth(4,  withCol_3)
        self.ui.tableView_2.setColumnWidth(5,  withCol_4)
        
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(1, True)
#        self.ui.tableView.setColumnHidden(3, True)
        self.ui.tableView_2.selectRow(0)
        '''        
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        '''
        print 8


    def selectionChanged(self):
        global id_defect
        id_defect = int(model.record(self.selModel.currentIndex().row()).field('id').value().toString())        
        
        
        
        self.selTestType()


    def selectionChanged_2(self):
#        global row_type
        row = self.selModel_2.currentIndex().row()
        if model_2.record(row).field('bind').value().toString() == u'ПРИВЯЗАНО':
            self.bind = True
            self.ui.pushButton_4.setText(u'Отвязать')
        else:    
            self.bind = False
            self.ui.pushButton_4.setText(u'Привязать')


#        QtGui.QPushButton.setText()

# Редактирование трансов (начало кода)        
                        
    class editDefect(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editDefect.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
                
        def pushButton_Click(self):
            global id_defect
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи тип', QMessageBox.Ok)
                return
            if self.ui.lineEdit_2.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи полное наименование', QMessageBox.Ok)
                return
        
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO defect (defecttype, iscritical, fullname, description)
                                            values (:defecttype, :iscritical, :fullname, :description)'''            
                                
                query.prepare(SQL)
            else:
                SQL ='''UPDATE defect SET defecttype = :defecttype,
                                          iscritical = :iscritical,
                                          fullname = :fullname,
                                          description = :description
                        WHERE id = :id'''
                query.prepare(SQL)

                query.bindValue(":id", id_defect);
                
            query.bindValue(":defecttype", self.ui.lineEdit.text())
            query.bindValue(":iscritical", self.ui.checkBox.isChecked())
            query.bindValue(":fullname", self.ui.lineEdit_2.text())
            query.bindValue(":description", self.ui.lineEdit_3.text())            
            
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

# Редактирование трансов (конец кода)        

                

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
        
        wind = sprDefect(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())

