# -*- coding: UTF-8 -*-
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt

#import JournalMsr

import socket
import PyQt4
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
#from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.gui.ClsTrans import ClsTrans

import ui.ico_64_rc

import datetime

from datetime import date

id_serial_number = -1
#id_transformer = -1
# id_coil = -1

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 30
withCol2 = 20
withCol3 = 20
withCol4 = 10
withCol5 = 100

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
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5))
            obj.setColumnWidth(2, koef * withCol1)
            obj.setColumnWidth(3, koef * withCol2)
            obj.setColumnWidth(4, koef * withCol3)
            obj.setColumnWidth(5, koef * withCol4)
            obj.setColumnWidth(6, koef * withCol5)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False


class sprSerialNumber(QWidget, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprSerialNumber.ui")        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

        self.ui.lineEdit.textChanged.connect(self.lineEdit_textChanged)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))

        self.ui.tableView.setObjectName('tv1')
        
        self.selMakeDate()
        global currColumnIndex
        currColumnIndex = 0
        global desc
        desc = ''
        self.selSerialNumber(currColumnIndex, False)
        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_indexChanged)        
        self.comboBox_indexChanged()
      
      
        # Организация контекстного меню на кнопке "Добавить"
        fnt = QtGui.QFont()
        fnt.setPointSize(14)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Добавить с копированием', self))
        self.mnu.setFont(fnt)        
        self.ui.pushButton.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.ui.pushButton.customContextMenuRequested.connect(self.on_context_menu)      
        self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.pushButton_Click_copy)
      
      
      
# Настройка сортировки при нажатии колонки      
# пример     https://coderoad.ru/14068823/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-QTableView-%D0%B2-PyQt

        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)
      
      
      
      
      
      
    def on_context_menu(self, point):
        self.mnu.exec_(self.ui.pushButton.mapToGlobal(point))

    
#    def actions(self, action):        
#    def actions(self):        
#        print 'DFGHJ'    
    
      
    def sortByColumn(self, columnIndex):
        print 'sortByColumn sortByColumn sortByColumn sortByColumn sortByColumn  ', columnIndex
        self.selSerialNumber(columnIndex, False)
      
      

# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editSerialNumber(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового серийного номера')
        row = self.selModel.currentIndex().row()
        self.wind.ui.spinBox_2.setValue(datetime.datetime.now().year - 2000) 
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selSerialNumber(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM serial_number");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            

    def pushButton_Click_copy(self):
        global isSave        
        self.wind = self.editSerialNumber(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового серийного номера')
        row = self.selModel.currentIndex().row()
 
        self.wind.ui.lineEdit.tag = int(model.record(row).field('transformer').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('fullname').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('ordernumber').value().toString())        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('series').value().toString())        
        self.wind.ui.spinBox.setValue(int(model.record(row).field('serialnumber').value().toString()))
        self.wind.ui.spinBox_2.setValue(int(model.record(row).field('makedate').value().toString()))
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selSerialNumber(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM serial_number");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            

                
    def pushButton_2_Click(self):
        global isSave        
        global id_serial_number
        self.wind = self.editSerialNumber(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего серийного номера')
        row = self.selModel.currentIndex().row()
               
        id_serial_number = int(model.record(row).field('id').value().toString())        
        self.wind.ui.lineEdit.tag = int(model.record(row).field('transformer').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('fullname').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('ordernumber').value().toString())        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('series').value().toString())        
        self.wind.ui.spinBox.setValue(int(model.record(row).field('serialnumber').value().toString()))
        self.wind.ui.spinBox_2.setValue(int(model.record(row).field('makedate').value().toString()))
                
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selSerialNumber(currColumnIndex, True)
            self.ui.tableView.selectRow(row)                                            



    def pushButton_3_Click(self):
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале обмотки!', QMessageBox.Ok)
                return
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM serial_number WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selSerialNumber(currColumnIndex, True)
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                        
                                                
            
    def lineEdit_textChanged(self):
        self.selSerialNumber(currColumnIndex, False)
        pass
    #    self.selSerialNumber()
        #self.ViewZavMsr(0, -1, self.lineEdit.text())
            
                        
            
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
            
                        

    def selMakeDate(self):
        query = QSqlQuery(db1)
        query.prepare("select distinct makedate from serial_number order by makedate desc")
        query.exec_()        
        
        model_.setQuery(query)
        
        for i in range(model_.rowCount()):
            self.ui.comboBox.addItem(model_.record(i).field(0).value().toString())


    def selSerialNumber(self, columnIndex, isEdit):
        global currColumnIndex
        global desc

        if self.ui.lineEdit.text().trimmed() != '':
            try:
                n = int(self.ui.lineEdit.text())
            except Exception:
                QMessageBox.warning(self, u"Предупреждение",  u'Номер для поиска (' + self.ui.lineEdit.text() + u') не корректный', QMessageBox.Ok)
                self.ui.lineEdit.setFocus()
                return



        
        if not isEdit:
            if currColumnIndex == columnIndex:
                if desc == '':
                    desc = 'desc'
                else:            
                    desc = ''
            else:        
                    desc = ''
        
        
        currColumnIndex = columnIndex        
#        v = unicode(self.ui.lineEdit.text()).upper()
        print 'columnIndex = ', columnIndex
        
        
        
                
        
        query = QSqlQuery(db1)
                        
        
        SQL = """select t1.id,
        transformer,
        ordernumber,
        series,
        serialnumber,
        makedate,
        fullname
        from serial_number t1, transformer t2
        where t1.transformer = t2.id
        and makedate=:makedate
        """

        if self.ui.lineEdit.text().trimmed() != '':
            SQL += """and t1.serialnumber = :serialnumber
               """
                
        if columnIndex == 0:            
            SQL += """order by id desc
                   """
        if columnIndex == 2:            
            SQL += """order by ordernumber """ + desc + """, series, serialnumber
                   """
        if columnIndex == 3:            
            SQL += """order by series """ + desc + """, serialnumber
                   """
        if columnIndex == 4:            
            SQL += """order by serialnumber """ + desc + """
                   """
        if columnIndex == 6:            
            SQL += """order by fullname """ + desc + """, serialnumber
                   """
#        SQL += """order by makedate, fullname
#               """

        print SQL       
        query.prepare(SQL)

        query.bindValue(":makedate", self.ui.comboBox.currentText())

        if self.ui.lineEdit.text().trimmed() != '':
            query.bindValue(":serialnumber", self.ui.lineEdit.text().trimmed())

        '''
        query.bindValue(":type", self.ui.comboBox.currentText())
        if v != "":
            query.bindValue(":", '%' + v + '%')
           ''' 
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Заказ")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Серия")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Номер")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Дата")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Трансформатор")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(2,  withCol1)
        self.ui.tableView.setColumnWidth(3,  withCol2)
        self.ui.tableView.setColumnWidth(4,  withCol3)
        self.ui.tableView.setColumnWidth(5,  withCol4)
        self.ui.tableView.setColumnWidth(6,  withCol5)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
#        self.ui.tableView.setColumnHidden(3, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)


    def comboBox_indexChanged(self):
        columnIndex = 0
        model.clear()        
        model.reset()
        self.selSerialNumber(columnIndex, False)        


# Редактирование трансов (начало кода)        
                        
    class editSerialNumber(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editSerialNumber.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        
        
        def pushButton_Click(self):
            global id_serial_number
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи трансформатор', QMessageBox.Ok)
                return
            if self.ui.lineEdit_2.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи номер заказа', QMessageBox.Ok)
                return
            if self.ui.lineEdit_3.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи номер серии', QMessageBox.Ok)
                return
        
        
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                if not self.test_serialnumber(-1, self.ui.spinBox.text(), self.ui.spinBox_2.text()):
                    return
                SQL = '''INSERT INTO serial_number (ordernumber, series, serialnumber, makedate, transformer)
                                            values (:ordernumber, :series, :serialnumber, :makedate, :transformer)'''            
                                
                query.prepare(SQL)
            else:
                SQL ='''UPDATE serial_number SET ordernumber = :ordernumber,
                                                 series = :series,
                                                 serialnumber = :serialnumber,
                                                 makedate = :makedate,
                                                 transformer = :transformer
                                 WHERE id = :id'''
                if not self.test_serialnumber(id_serial_number, self.ui.spinBox.text(), self.ui.spinBox_2.text()):
                    return
                query.prepare(SQL)

                query.bindValue(":id", id_serial_number);
                
            query.bindValue(":ordernumber", self.ui.lineEdit_2.text())
            query.bindValue(":series", self.ui.lineEdit_3.text())
            query.bindValue(":serialnumber", self.ui.spinBox.text())
            query.bindValue(":makedate", self.ui.spinBox_2.text())            
            query.bindValue(":transformer", self.ui.lineEdit.tag)
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()


        def test_serialnumber(self, id, serialnumber, makedate):
#            global id_search
            query = QSqlQuery(db1)
            SQL = '''SELECT *
                     FROM serial_number 
                     WHERE serialnumber = :serialnumber
                     AND makedate = :makedate
                  '''
            if id > -1:
                SQL += '''AND id != :id'''
                
            query.prepare(SQL);
            if id > -1:
                query.bindValue(":id", id);                
            query.bindValue(":serialnumber", serialnumber)
            query.bindValue(":makedate", makedate)            
            
            query.exec_()
            
            if query.size() > 0:
                QMessageBox.warning(self, u"Предупреждение", u"Серийный номер: " + serialnumber + u' не может повторяться втечении одного года!', QMessageBox.Ok)                                
                return False
            return True
        


        # Вызов справочника трансов
        def pushButton_3_Click(self):
            from ClsTrans import ClsTrans
            wind = ClsTrans(self.env, 1)
          #  if wind.tag <> 0:
                # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
                # Бред какой-то        
            wind.show()
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()
        
            if wind.IS_SELECT:
                self.ui.lineEdit.setText(wind.NAME_TRANS)
                self.ui.lineEdit.tag = wind.CODE_TRANS 
            
            
                            
# Редактирование трансов (конец кода)        


        '''
        def none(self, text, not_null):
            try:
              if float(text) == 0 and not not_null:            
                  return None
              else:    
                  return text
            except Exception:
                QMessageBox.warning(self, u"Предупреждение",  u'Величина: ' + text + u' не корректна!', QMessageBox.Ok)
                return 'error'
'''
                

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
        
        wind = sprSerialNumber(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())

