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


STAND = None
ID_STAND_MSR = None
ID_ZAV_MSR = None
#id_stand_msr = -1

#model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 100
withCol2 = 50

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
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2))
            obj.setColumnWidth(2, koef * withCol1)
            obj.setColumnWidth(3, koef * withCol2)
            VSB1 = obj.verticalScrollBar().isVisible()

        return False


#class sprClimat(QWidget, UILoader):    
#class ClsTrans(QtGui.QDialog, UILoader):
#    def __init__(self, _env, sw, *args):
#        QtGui.QDialog.__init__(self, *args)        


class StandMsr(QtGui.QDialog, UILoader):    
    def __init__(self, _env, stand, fullname):
        global db1
        global STAND
        db1 = _env.db
        self.env = _env
        STAND = stand
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprTester.ui")        
        
        self.setWindowTitle(u"Средства измерения")
        self.ui.label.setText(u" Тип испытания: " + fullname)
                
        self.ui.groupBox.setVisible(False)  
        self.ui.pushButton_4.setVisible(False)      
        self.ui.pushButton_5.setVisible(False)      
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
#        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')
        self.selStandMsr()
      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()

        self.IS_SELECT = False    
      
      
# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):        
        global isSave        
        self.wind = self.editStandMsr(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового средства измерения')
        row = self.selModel.currentIndex().row()
        #self.wind.ui.spinBox_2.setValue(datetime.datetime.now().year - 2000) 
                
        #print datetime.datetime.now()                                     
        #self.wind.ui.dateTimeEdit.setDateTime(datetime.datetime.now())
        #print datetime.datetime.now()                                     
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selStandMsr()
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM stand_msr");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            
                
    def pushButton_2_Click(self):
        global isSave        
        global ID_STAND_MSR
        global ID_ZAV_MSR
        self.wind = self.editStandMsr(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущей записи')
        row = self.selModel.currentIndex().row()
               
#        self.ID_STAND_MSR = int(model.record(row).field('id').value().toString())        
        ID_STAND_MSR = int(model.record(row).field('id').value().toString())        
        ID_ZAV_MSR = int(model.record(row).field('zav_msr').value().toString())   
#        self.wind.ui.lineEdit.tag = int(model.record(row).field('operator').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('name_msr').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('zav_num').value().toString())        
                        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selStandMsr()
            self.ui.tableView.selectRow(row)                                            


    def pushButton_3_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM stand_msr WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selStandMsr()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    

    def pushButton_4_Click(self):
        return
        self.generate_map_msr(None)
#        self.generate_map_msr(292022)
        return
        row = self.selModel.currentIndex().row()
        self.STANDMSR = int(model.record(row).field('id').value().toString())
#        self.LASTUPDATE = unicode(model.record(row).field('lastupdate').value().toString())           
        self.LASTUPDATE = model.record(row).field('lastupdate').value().toDateTime()                             
        self.IS_SELECT = True
        self.close()        

    '''
    def pushButton_5_Click(self):
        self.IS_SELECT = False
        self.close()        
'''

            
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

            
    def selStandMsr(self):        
        query = QSqlQuery(db1)
                                
        SQL = """select t1.id, t1.zav_msr, name_msr, zav_num
from stand_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and stand = :stand
order by name_msr
        """
                
        query.prepare(SQL)
        query.bindValue(":stand", STAND);            
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            return
            
        model.setQuery(query)

        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Наименование средства измерения")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Заводской номер")
        #model.setHeaderData(4, QtCore.Qt.Horizontal, u"Относительная\nвлажность, %")
        #model.setHeaderData(5, QtCore.Qt.Horizontal, u"Атмосферное\nдавление, кПа")
        #model.setHeaderData(6, QtCore.Qt.Horizontal, u"Время")
    #model.setHeaderData(7, QtCore.Qt.Horizontal, u"Помещение")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.ui.tableView.setColumnWidth(2,  withCol1)
        self.ui.tableView.setColumnWidth(3,  withCol2)
        #self.ui.tableView.setColumnWidth(4,  withCol3)
        #self.ui.tableView.setColumnWidth(5,  withCol4)
        #self.ui.tableView.setColumnWidth(6,  withCol5)
        #self.ui.tableView.setColumnWidth(7,  withCol6)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
        #self.ui.tableView.setColumnHidden(1, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)


    def generate_map_msr(self, test_map, rewrite, isMsr):
        pass
        sql1 = ''
        sql2 = ''
        if test_map != None:
            sql1 = u" where test_map = :test_map"
            sql2 = u" and t1.id = :test_map_2"
#            sql1 = u" where test_map = 292022"
#            sql2 = u" and t1.id = 292022"

        if rewrite and isMsr:
            query_3 = QSqlQuery(db1)
            SQL = u"delete from map_msr where test_map = :test_map"
            
            query_3.prepare(SQL)
            query_3.bindValue(":test_map", test_map)
            if not query_3.exec_():
                QMessageBox.warning(self, u"Ошибка", SQL + query_3.lastError().text(), QMessageBox.Ok)
                return

        #return ###############################################


        query_2 = QSqlQuery(db1)
        SQL = u"""
select t1.id as test_map, zav_msr, t1.stand, t3.test_map as test_map_2 
from test_map t1 left outer join (select distinct test_map from map_msr""" + sql1 + u""") as t3 on (t1.id = t3.test_map),
     stand_msr t2
where createdatetime > to_date('31.12.2019', 'dd.mm.yyyy')
and t1.stand = t2.stand
""" + sql2 + u"""
and t3.test_map is null
order by createdatetime
"""
        print SQL
        
        print 'test_map = ', test_map
        
        query_2.prepare(SQL)
        if test_map != None:
            query_2.bindValue(":test_map", test_map)
            query_2.bindValue(":test_map_2", test_map)
#        query_2.bindValue(":stand", STAND)
#        query_2.bindValue(":zav_msr", ID_ZAV_MSR)                                            
        if not query_2.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query_2.lastError().text(), QMessageBox.Ok)
            return
        model_2.setQuery(query_2)
        
        print 'model_2.rowCount() = ', model_2.rowCount()
     
     
     
                
        for i in range(model_2.rowCount()):
            print 'test_map, zav_msr = ', model_2.record(i).field('test_map').value().toString(), model_2.record(i).field('zav_msr').value().toString()
            query_3 = QSqlQuery(db1)
            SQL = u"insert into map_msr (test_map, zav_msr) values (:test_map, :zav_msr)"
            
            query_3.prepare(SQL)
            query_3.bindValue(":test_map", int(model_2.record(i).field('test_map').value().toString()))
            query_3.bindValue(":zav_msr", int(model_2.record(i).field('zav_msr').value().toString()))
            if not query_3.exec_():
                QMessageBox.warning(self, u"Ошибка", SQL + query_3.lastError().text(), QMessageBox.Ok)
                return
            

# Редактирование stand_msr (начало кода)                                
    class editStandMsr(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editStandMsr.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

        
        def pushButton_Click(self):
            global STAND
            global ID_STAND_MSR
#            global id_stand_msr
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи средство измерения', QMessageBox.Ok)
                self.ui.pushButton_3.setFocus()
                return
                
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO stand_msr (stand, zav_msr) values (:stand, :zav_msr)'''            
                                
                query.prepare(SQL)
            else:
                SQL ='''UPDATE stand_msr SET stand = :stand,
zav_msr = :zav_msr
WHERE id = :id'''
                                                
                query.prepare(SQL)
#                query.bindValue(":id", id_stand_msr);
                query.bindValue(":id", ID_STAND_MSR);
                                
#            query.bindValue(":stand", self.ui.lineEdit.tag)
#            query.bindValue(":zav_msr", self.ui.doubleSpinBox.value())                                
            query.bindValue(":stand", STAND)
            query.bindValue(":zav_msr", ID_ZAV_MSR)                                
                        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

                            
                            
        # Вызов справочника средств измерений
        def pushButton_3_Click(self):
            global ID_ZAV_MSR
            from sprMsr import classJournal
            wind = classJournal(self.env)
            wind.show()
            
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()
        
            if wind.IS_SELECT:
                ID_ZAV_MSR = wind.ID_ZAV_MSR
                print 'ID_ZAV_MSR', ID_ZAV_MSR
                self.ui.lineEdit.setText(wind.NAME_MSR)
                self.ui.lineEdit_2.setText(wind.ZAV_NUM)
                                                        
                            
                            
# Редактирование stand_msr (конец кода)                        

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
        
        wind = StandMsr(env, 25, "WWWWWWWWWWWWWWWWWWWWWWWW")
#        wind = sprClimat(env)        
 #       wind.ui.pushButton_4.setVisible(False)
 #       wind.ui.pushButton_5.setVisible(False)                
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
