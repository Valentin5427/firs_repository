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

id_climat = -1

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
#model_2 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 100
withCol2 = 50
withCol3 = 50
withCol4 = 50
withCol5 = 100
withCol6 = 50

isSave = False

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
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6))
            obj.setColumnWidth(2, koef * withCol1)
            obj.setColumnWidth(3, koef * withCol2)
            obj.setColumnWidth(4, koef * withCol3)
            obj.setColumnWidth(5, koef * withCol4)
            obj.setColumnWidth(6, koef * withCol5)
            obj.setColumnWidth(7, koef * withCol6)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False


#class sprClimat(QWidget, UILoader):    
class sprClimat(QtGui.QDialog, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprTester.ui")        
        
        self.setWindowTitle(u"Справочник окружающей среды")
                
        self.ui.groupBox.setVisible(False)        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
#        self.ui.pushButton.clicked.connect(self.pushButton_Click)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')
        self.selClimat()
      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()

        self.IS_SELECT = False    
#        self.ui.pushButton_4.setVisible(False)
#        self.ui.pushButton_5.setVisible(False)

        '''      
        if sw == 0:
            self.ui.pushButton_7.setVisible(False)
            self.ui.pushButton_8.setVisible(False)
        if sw == 1:
            self.ui.tableView_2.setVisible(False)
            self.ui.label_3.setVisible(False)
            self.ui.pushButton.setVisible(False)
            self.ui.pushButton_2.setVisible(False)
            self.ui.pushButton_3.setVisible(False)
            self.ui.pushButton_4.setVisible(False)
            self.ui.pushButton_5.setVisible(False)
            self.ui.pushButton_6.setVisible(False)
           ''' 
      
      
      
# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        ''' 
        print datetime.date.today()        
        print datetime.datetime.now()        
        self.wind.ui.dateTimeEdit.setDateTime(model.record(row).field('lastupdate').value().toDateTime())                     
'''
        
        global isSave        
        self.wind = self.editClimat(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового испытательного напряжения')
        row = self.selModel.currentIndex().row()
        #self.wind.ui.spinBox_2.setValue(datetime.datetime.now().year - 2000) 
                
        print datetime.datetime.now()                                     
        self.wind.ui.dateTimeEdit.setDateTime(datetime.datetime.now())
        print datetime.datetime.now()                                     
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selClimat()
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM climat");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            
                
    def pushButton_2_Click(self):
        global isSave        
        global id_climat
        self.wind = self.editClimat(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущегй записи')
        row = self.selModel.currentIndex().row()
               
        id_climat = int(model.record(row).field('id').value().toString())        
        id_operator = int(model.record(row).field('operator').value().toString())   
        self.wind.ui.lineEdit.tag = int(model.record(row).field('operator').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('fio').value().toString())        
        self.wind.ui.doubleSpinBox.setValue(float(model.record(row).field('temperature').value().toString()))
        self.wind.ui.doubleSpinBox_2.setValue(float(model.record(row).field('humidity').value().toString()))
        self.wind.ui.doubleSpinBox_3.setValue(float(model.record(row).field('pressure').value().toString()))
        self.wind.ui.dateTimeEdit.setDateTime(model.record(row).field('lastupdate').value().toDateTime())                     
        self.wind.ui.spinBox.setValue(float(model.record(row).field('room').value().toString()))
                        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selClimat()
            self.ui.tableView.selectRow(row)                                            

    def pushButton_3_Click(self):
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM climat WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selClimat()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    

    def pushButton_4_Click(self):
        row = self.selModel.currentIndex().row()
        self.CLIMAT = int(model.record(row).field('id').value().toString())
#        self.LASTUPDATE = unicode(model.record(row).field('lastupdate').value().toString())           
        self.LASTUPDATE = model.record(row).field('lastupdate').value().toDateTime()                             
        self.IS_SELECT = True
        self.close()        

    def pushButton_5_Click(self):
        self.CLIMAT = -1
        self.LASTUPDATE = ''        
        self.IS_SELECT = False
        self.close()        


            
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

            
    def selClimat(self):        
        query = QSqlQuery(db1)
                                
        SQL = """select t1.id,        
        operator,
        fio,
        temperature,
        humidity,
        pressure,
        lastupdate,
        room                 
        from climat t1, operator t2
        where t1.operator = t2.id
        order by id desc
        """
                
#        from serial_number t1, transformer t2
#        where t1.transformer = t2.id
                        
        query.prepare(SQL)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Оператор")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Температура\nвоздуха, C")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Относительная\nвлажность, %")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Атмосферное\nдавление, кПа")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Время")
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Помещение")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.ui.tableView.setColumnWidth(2,  withCol1)
        self.ui.tableView.setColumnWidth(3,  withCol2)
        self.ui.tableView.setColumnWidth(4,  withCol3)
        self.ui.tableView.setColumnWidth(5,  withCol4)
        self.ui.tableView.setColumnWidth(6,  withCol5)
        self.ui.tableView.setColumnWidth(7,  withCol6)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)


# Редактирование трансов (начало кода)        
                        
    class editClimat(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editClimat.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

        
        def pushButton_Click(self):
            global id_climat
                        
            #QtGui.QLineEdit.setFocus()            
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи оператора', QMessageBox.Ok)
                self.ui.pushButton_3.setFocus()
                return
            '''
            if self.ui.doubleSpinBox.value() == 0:
                QMessageBox.warning(self, u"Предупреждение",  u'Введи температуру', QMessageBox.Ok)
                self.ui.doubleSpinBox.setFocus()
                return
            if self.ui.doubleSpinBox_2.value() == 0:
                QMessageBox.warning(self, u"Предупреждение",  u'Введи влажность', QMessageBox.Ok)
                self.ui.doubleSpinBox_2.setFocus()
                return
            if self.ui.doubleSpinBox_3.value() == 0:
                QMessageBox.warning(self, u"Предупреждение",  u'Введи давление', QMessageBox.Ok)
                self.ui.doubleSpinBox_3.setFocus()
                return
               '''
                
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO climat (operator, temperature, humidity, pressure, lastupdate, room)
                                            values (:operator, :temperature, :humidity, :pressure, :lastupdate, :room)'''            
                                
 #               SQL = '''INSERT INTO climat (operator, temperature, humidity, pressure, room)
 #                                           values (:operator, :temperature, :humidity, :pressure, :room)'''            
                query.prepare(SQL)
                query.bindValue(":lastupdate", self.ui.dateTimeEdit.text())
            else:
                SQL ='''UPDATE climat SET operator = :operator,
                                          temperature = :temperature,
                                          humidity = :humidity,
                                          pressure = :pressure,
                                          room = :room
                                 WHERE id = :id'''

#                                          lastupdate = :lastupdate,

                                                
                query.prepare(SQL)
                query.bindValue(":id", id_climat);
                                
            query.bindValue(":operator", self.ui.lineEdit.tag)
            query.bindValue(":temperature", self.ui.doubleSpinBox.value())                                
            query.bindValue(":humidity", self.ui.doubleSpinBox_2.value())                                
            query.bindValue(":pressure", self.ui.doubleSpinBox_3.value())
#            query.bindValue(":lastupdate", self.ui.dateTimeEdit.text())
            query.bindValue(":room", self.ui.spinBox.text())
            
            
            '''                
            if self.ui.doubleSpinBox.value() == 0:
                query.bindValue(":nominal_voltage", None)
            else:    
                query.bindValue(":nominal_voltage", self.ui.doubleSpinBox.value())
                                
            query.bindValue(":isolation_level", self.ui.lineEdit.text())
            
            if self.ui.doubleSpinBox_2.value() == 0:
                query.bindValue(":prime_test_voltage", None)
            else:    
                query.bindValue(":prime_test_voltage", self.ui.doubleSpinBox_2.value())
            
            if self.ui.doubleSpinBox_3.value() == 0:
                query.bindValue(":second_test_voltage", None)
            else:    
                query.bindValue(":second_test_voltage", self.ui.doubleSpinBox_3.value())
            
            if self.ui.doubleSpinBox_4.value() == 0:
                query.bindValue(":prime_test_voltage2", None)
            else:    
                query.bindValue(":prime_test_voltage2", self.ui.doubleSpinBox_4.value())
            
            if self.ui.doubleSpinBox_5.value() == 0:
                query.bindValue(":pd_level", None)
            else:    
                query.bindValue(":pd_level", self.ui.doubleSpinBox_5.value())
            '''
            
            
                        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

                            
                            
        # Вызов справочника операторов
        def pushButton_3_Click(self):
            from sprTester import sprTester
#            wind = sprTester(self.env, 1)
            wind = sprTester(self.env)
            wind.show()
            
            wind.resizeEvent(None)
            wind.close()                
#            return
            wind.exec_()
        
#            return
            if wind.IS_SELECT:
                self.ui.lineEdit.setText(wind.FIO)
                self.ui.lineEdit.tag = wind.OPERATOR 
                                                        
                            
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
        
        wind = sprClimat(env)        
        wind.ui.pushButton_4.setVisible(False)
        wind.ui.pushButton_5.setVisible(False)                
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
