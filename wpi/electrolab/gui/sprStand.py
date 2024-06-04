# -*- coding: UTF-8 -*-
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt, QPoint

#import JournalMsr

import socket
from fileinput import close
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.DigitalKeyboard import DigitalKeyboard

import ui.ico_64_rc

import datetime

from datetime import date

id_stand = -1
id_coil = -1



model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 100
withCol2 = 25
#withCol3 = 20
withCol3 = 70
withCol4 = 25
withCol5 = 50
withCol6 = 50                        
withCol7 = 50                       
withCol8 = 25                       
withCol9 = 25                       
withCol10 = 25                       
withCol11 = 35                       
withCol12 = 100                       

withCol_1 = 100

isSave = False
#mnu_2 = None


def noneValue(v):
    try:
        v.strip()
    except:
        return None

    if v in (None,'') :
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
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7 + withCol8 + withCol9 + withCol10 + withCol11 + withCol12))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            obj.setColumnWidth(5, koef * withCol5)
            obj.setColumnWidth(6, koef * withCol6)
            obj.setColumnWidth(7, koef * withCol7)
            obj.setColumnWidth(8, koef * withCol8)
            obj.setColumnWidth(9, koef * withCol9)
            obj.setColumnWidth(10, koef * withCol10)
            obj.setColumnWidth(11, koef * withCol11)
            obj.setColumnWidth(12, koef * withCol12)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1))
            obj.setColumnWidth(1, koef * withCol_1)
            VSB2 = obj.verticalScrollBar().isVisible()




        return False

        
   
#class ClsTrans(QWidget, UILoader):    
#    def __init__(self, _env):
        
#class ClsTrans(QtGui.QDialog, UILoader):
class sprStand(QtGui.QDialog, UILoader):
    def __init__(self, _env, sw, *args):
        QtGui.QDialog.__init__(self, *args)        
        
        #global id_type
#        global mnu_2

        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"ClsTrans.ui")        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_4.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_5.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_6.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
####        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
#        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
#        self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)
#        self.ui.pushButton_9.clicked.connect(self.pushButton_9_Click)

        self.ui.lineEdit.textChanged.connect(self.lineEdit_textChanged)
        self.ui.lineEdit_2.textChanged.connect(self.lineEdit_textChanged)

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        
        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()        
        self.connect(self.selModel_2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_2)


        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))

        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setObjectName('tv2')
        
        self.selRoom()

#        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_indexChanged)        
        #####self.comboBox_indexChanged()

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
            self.ui.pushButton_10.setVisible(False)
            
            
        self.IS_SELECT = False    

            
        # Организация контекстного меню на кнопке "Добавить"
        fnt = QtGui.QFont()
        fnt.setPointSize(14)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Добавить с копированием', self))
        self.mnu.setFont(fnt)        
        self.ui.pushButton.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.ui.pushButton.customContextMenuRequested.connect(self.on_context_menu)      
        self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.pushButton_Click_copy)



        query = QSqlQuery(db1)
                                

        '''
        # Организация меню помещений
        self.mnu_2 = QtGui.QMenu(self)
        mnu_2 = QtGui.QMenu(self)
        query = QSqlQuery(db1)
        query.prepare("select id, fullname from room order fullname")
        query.exec_()                
                
        
        model_.setQuery(query)        
        for i in range(model_.rowCount()):
            action = self.mnu_2.addAction(model_.record(i).field('type').value().toString())
            action.setData(model_.record(i).field('id').value().toString())
            action = mnu_2.addAction(model_.record(i).field('type').value().toString())
            action.setData(model_.record(i).field('id').value().toString())
        #self.ui.comboBox.addSeparator()
#        self.id_type = None
        self.mnu_2.addSeparator()
        mnu_2.addSeparator()
        
        action = self.mnu_2.addAction(u'Все типы')
        action.setData(-1)
        self.id_type = -1
        self.ui.lineEdit_2.setText(unicode(action.text()))
                
        action = self.mnu_2.addAction(u'Без типа')
        action.setData(-2)
        
        action = mnu_2.addAction(u'Без типа')
        action.setData(-2)
        
        
        self.connect(self.mnu_2, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_2_Click)
        '''
      
        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)
      
        global currColumnIndex
        currColumnIndex = 0
        global desc
        desc = ''
      
        self.selStand(currColumnIndex, False)        
        

    def sortByColumn(self, columnIndex):
        self.selStand(columnIndex, False)
     
      
      
      
    def on_context_menu(self, point):
        self.mnu.exec_(self.ui.pushButton.mapToGlobal(point))

    '''  
    def mnu_2_Click(self, q):
#        self.id_type = int(q.data().toString())    
        self.gost_id = int(q.data().toString())    
        self.ui.lineEdit_2.setText(unicode(q.text()))
'''
        

# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editStand(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового стенда')
        row = self.selModel.currentIndex().row()
        self.wind.ui.lineEdit.setText(model.record(row).field('type').value().toString())
        isSave = False        
        self.wind.exec_()
        if isSave:
            print 'selTrans1'
            self.selStand(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM stand");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            
            


    def pushButton_Click_copy(self):
        global isSave        
        self.wind = self.editStand(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового стенда')
        row = self.selModel.currentIndex().row()
        #self.pushButton_2_Click()

        self.wind.ui.lineEdit.setText(model.record(row).field('name_room').value().toString())
        if model.record(row).field('room').value().toString() != '': 
            self.wind.room_id = int(model.record(row).field('room').value().toString())
                    
        self.wind.ui.lineEdit_2.setText(model.record(row).field('gost').value().toString())
        if model.record(row).field('gost_id').value().toString() != '': 
            self.wind.gost_id = int(model.record(row).field('gost_id').value().toString())        
                
        self.wind.ui.checkBox.setChecked(bool(int(model.record(row).field('needclimatlog_').value().toString())))        
        self.wind.ui.checkBox_2.setChecked(bool(int(model.record(row).field('enablesupervisor_').value().toString())))        
        self.wind.ui.checkBox_3.setChecked(bool(int(model.record(row).field('enableassistant_').value().toString())))        
        self.wind.ui.checkBox_4.setChecked(bool(int(model.record(row).field('singleitem_').value().toString())))        
        self.wind.ui.checkBox_5.setChecked(bool(int(model.record(row).field('useampereturn_').value().toString())))        
        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('name').value().toString())
        if model.record(row).field('test_type').value().toString() != '': 
            self.wind.type_id = int(model.record(row).field('test_type').value().toString())        
                
        self.wind.ui.lineEdit_4.setText(model.record(row).field('fullname').value().toString())
        self.wind.ui.lineEdit_5.setText(model.record(row).field('hostname').value().toString())
        self.wind.ui.spinBox.setValue(int(model.record(row).field('number').value().toString()))
        #self.wind.ui.lineEdit_6.setText(model.record(row).field('description').value().toString())
        self.wind.ui.textEdit.setText(model.record(row).field('description').value().toString())
        
        
        #QtGui.QTextEdit.setText()
        
        
        
                
        self.wind.ui.checkBox_6.setChecked(bool(int(model.record(row).field('supervisorreport_').value().toString())))        
        self.wind.ui.checkBox_7.setChecked(bool(int(model.record(row).field('checkreport_').value().toString())))        
        self.wind.ui.checkBox_8.setChecked(bool(int(model.record(row).field('ticketmatrix_').value().toString())))        

        isSave = False        
        self.wind.exec_()
        if isSave:
            print 'selTrans1'
            id_stand_old = int(model.record(row).field('id').value().toString())

            self.selStand(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM stand");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            


            r = QMessageBox.warning(self, u"Предупреждение", u"Вы желаете скопировать список операторов?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.Yes:
                print id_stand_old, '   ', id_search
#                return
                query = QSqlQuery(db1)

                SQL = """                
insert into stand_user (stand, operator)
select :stand, operator from stand_user where stand = :stand_old
"""
                query.prepare(SQL)                
                
#                row = self.selModel.currentIndex().row()                
                query.bindValue(":stand_old", id_stand_old)
                query.bindValue(":stand", id_search)
            #    query.exec_()
                
                if not query.exec_():
                    QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                    return
                                
                self.selOperator()
                                
   
            
                
    def pushButton_2_Click(self):
        global isSave        
        self.wind = self.editStand(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего стенда')
        row = self.selModel.currentIndex().row()
                
                
                
        self.wind.ui.lineEdit.setText(model.record(row).field('name_room').value().toString())
        if model.record(row).field('room').value().toString() != '': 
            self.wind.room_id = int(model.record(row).field('room').value().toString())
                    
        self.wind.ui.lineEdit_2.setText(model.record(row).field('gost').value().toString())
        if model.record(row).field('gost_id').value().toString() != '': 
            self.wind.gost_id = int(model.record(row).field('gost_id').value().toString())        
                
        self.wind.ui.checkBox.setChecked(bool(int(model.record(row).field('needclimatlog_').value().toString())))        
        self.wind.ui.checkBox_2.setChecked(bool(int(model.record(row).field('enablesupervisor_').value().toString())))        
        self.wind.ui.checkBox_3.setChecked(bool(int(model.record(row).field('enableassistant_').value().toString())))        
        self.wind.ui.checkBox_4.setChecked(bool(int(model.record(row).field('singleitem_').value().toString())))        
        self.wind.ui.checkBox_5.setChecked(bool(int(model.record(row).field('useampereturn_').value().toString())))        
        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('name').value().toString())
        if model.record(row).field('test_type').value().toString() != '': 
            self.wind.type_id = int(model.record(row).field('test_type').value().toString())        
                
        self.wind.ui.lineEdit_4.setText(model.record(row).field('fullname').value().toString())
        self.wind.ui.lineEdit_5.setText(model.record(row).field('hostname').value().toString())
        self.wind.ui.spinBox.setValue(int(model.record(row).field('number').value().toString()))
#        self.wind.ui.lineEdit_6.setText(model.record(row).field('description').value().toString())
        self.wind.ui.textEdit.setText(model.record(row).field('description').value().toString())
                
        self.wind.ui.checkBox_6.setChecked(bool(int(model.record(row).field('supervisorreport_').value().toString())))        
        self.wind.ui.checkBox_7.setChecked(bool(int(model.record(row).field('checkreport_').value().toString())))        
        self.wind.ui.checkBox_8.setChecked(bool(int(model.record(row).field('ticketmatrix_').value().toString())))        



                
                
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selStand(currColumnIndex, True)
            self.ui.tableView.selectRow(row)                                            








    def pushButton_3_Click(self):
        print 'QSqlQueryModel.rowCount(parent=QModelIndex() = ', model_2.rowCount()
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале операторов!', QMessageBox.Ok)
                return
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM stand WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selStand(currColumnIndex, True)
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                        
                                
    def pushButton_4_Click(self):        
        from sprTester import sprTester
#            wind = sprTester(self.env, 1)
        wind = sprTester(self.env)
        wind.show()
            
        wind.resizeEvent(None)
        wind.close()                
        wind.exec_()        
        if wind.IS_SELECT:
            query = QSqlQuery(db1)
            
#            QMessageBox.warning(self, u"IS_SELECT", "lml;kmlkml", QMessageBox.Ok)
#                self.ui.lineEdit.setText(wind.FIO)
#                self.ui.lineEdit.tag = wind.OPERATOR 
                
            query.prepare('''INSERT INTO stand_user (stand, operator) values (:stand, :operator)''')

            query.bindValue(":stand", id_stand)            
            query.bindValue(":operator", wind.OPERATOR)            
                                    
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                return
            '''
            else:
                isSave = True        
                self.close()
                '''

            self.selOperator()




















        
        
        
        return
        
        global isSave        
        self.wind = self.editCoil(self.env)
        self.wind.tag = 1
                
        self.wind.ui.lineEdit_3.setText(model.record(self.selModel.currentIndex().row()).field('fullname').value().toString())        
                
        self.wind.setWindowTitle(u'Добавление пользователя')
        
        
        '''
        # Вычисление следующего порядкового номера обмотки 
        query = QSqlQuery(db1)
        query.prepare("""SELECT CASE WHEN (MAX(coilnumber) IS NULL) THEN 1 ELSE MAX(coilnumber) + 1 END 
                         FROM coil WHERE transformer = :transformer""");
        query.bindValue(":transformer", id_stand)
        query.exec_()
        query.next()

        self.wind.ui.spinBox_2.setValue(int(query.value(0).toString()))
'''
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selOperator()
        
            
    '''            
    def pushButton_5_Click(self):
        global isSave        
        self.wind = self.editCoil(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущей обмотки (отпайки)')
        row = self.selModel_2.currentIndex().row()
        
        self.wind.ui.lineEdit_3.setText(model.record(self.selModel.currentIndex().row()).field('fullname').value().toString())
                
        if model_2.record(row).field('coiltype').value().toString() != '':
            self.wind.ui.spinBox.setValue(int(model_2.record(row).field('coiltype').value().toString()))
        if model_2.record(row).field('coilnumber').value().toString() != '':
            self.wind.ui.spinBox_2.setValue(int(model_2.record(row).field('coilnumber').value().toString()))
        if model_2.record(row).field('tap').value().toString() != '':
            self.wind.ui.spinBox_3.setValue(int(model_2.record(row).field('tap').value().toString()))
        
        self.wind.ui.lineEdit.setText(model_2.record(row).field('classaccuracy').value().toString())
        
        if model_2.record(row).field('primarycurrent').value().toString() != '':
            self.wind.ui.doubleSpinBox.setValue(float(model_2.record(row).field('primarycurrent').value().toString()))
        if model_2.record(row).field('secondcurrent').value().toString() != '':
            self.wind.ui.doubleSpinBox_2.setValue(float(model_2.record(row).field('secondcurrent').value().toString()))
        if model_2.record(row).field('secondload').value().toString() != '':
            self.wind.ui.doubleSpinBox_3.setValue(float(model_2.record(row).field('secondload').value().toString()))
        if model_2.record(row).field('magneticvoltage').value().toString() != '':
            self.wind.ui.doubleSpinBox_4.setValue(float(model_2.record(row).field('magneticvoltage').value().toString()))
        if model_2.record(row).field('magneticcurrent').value().toString() != '':
            self.wind.ui.doubleSpinBox_5.setValue(float(model_2.record(row).field('magneticcurrent').value().toString()))
        if model_2.record(row).field('resistance').value().toString() != '':
            self.wind.ui.doubleSpinBox_6.setValue(float(model_2.record(row).field('resistance').value().toString()))
            
        self.wind.ui.lineEdit_2.setText(model_2.record(row).field('rating').value().toString())
        
        if model_2.record(row).field('ampereturn').value().toString() != '':
            self.wind.ui.spinBox_4.setValue(int(model_2.record(row).field('ampereturn').value().toString()))


        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selOperator()
            # навигация
            self.ui.tableView_2.selectRow(row)                                    
'''
            

            
    def pushButton_6_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM stand_user WHERE id = :ID")
            row = self.selModel_2.currentIndex().row()                
            query.bindValue(":id", model_2.record(row).field('id').value().toString());
            query.exec_()
            self.selOperator()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_2.selectRow(row)                                    

                        
    def pushButton_7_Click(self):
        self.IS_SELECT = True
        self.close()        

    def pushButton_8_Click(self):
        self.IS_SELECT = False
        self.close()        

    def pushButton_9_Click(self):
        self.mnu_2.exec_(QPoint(self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_2.geometry().height()   )) 

                
            
    def lineEdit_textChanged(self):
  #      self.selStand()
        pass
                        
            
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
            
            

#    def selTypeTrans(self):
    def selRoom(self):
        query = QSqlQuery(db1)
        query.prepare("select id, fullname from room order by fullname")
        query.exec_()        
        print 'selRoom'
        model_.setQuery(query)
        
        for i in range(model_.rowCount()):
            self.ui.comboBox.addItem(model_.record(i).field(1).value().toString())
            print 'selRoom1'

#        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.count() - 1)
        

    def selStand(self, columnIndex, isEdit):
#        v = unicode(self.ui.lineEdit.text()).upper()
        global currColumnIndex
        global desc        
        
        query = QSqlQuery(db1)
        
#        print 'currColumnIndex == columnIndex = ', currColumnIndex, columnIndex
        if not isEdit:        
            if currColumnIndex == columnIndex:
                if desc == '':
                    desc = 'desc'
                else:            
                    desc = ''
            else:        
                    desc = ''        

        currColumnIndex = columnIndex        
                                
        SQL = u"""
select t1.id,
       t1.fullname,
       t1.number,
       t1.description,
       t1.needclimatlog,
       t2.fullname as name_room,
       t1.hostname,
       t3.gost,       
       t1.supervisorreport,
       t1.checkreport,
       t1.ticketmatrix,
       t1.useampereturn,       
       t4.name,
       t4.code,
       t1.enablesupervisor,
       t1.enableassistant,
       t1.singleitem,
       t1.room,
       t1.gost_id,
       t1.test_type,       
       case when needclimatlog then 1 else 0 end as needclimatlog_,
       case when enablesupervisor then 1 else 0 end as enablesupervisor_,
       case when enableassistant then 1 else 0 end as enableassistant_,
       case when singleitem then 1 else 0 end as singleitem_,
       case when useampereturn then 1 else 0 end as useampereturn_,
       case when supervisorreport then 1 else 0 end as supervisorreport_,
       case when checkreport then 1 else 0 end as checkreport_,
       case when ticketmatrix then 1 else 0 end as ticketmatrix_
       
       
from stand t1 LEFT OUTER JOIN room t2 ON (t1.room = t2.id)
              LEFT OUTER JOIN gost t3 ON (t1.gost_id = t3.id)
              LEFT OUTER JOIN test_type t4 ON (t1.test_type = t4.id)
--order by t1.id
"""
        '''
       t1.needclimatlog,
       t2.fullname as name_room,
       t1.hostname,
       t3.gost,       
       t1.supervisorreport,
       t1.checkreport,
       t1.ticketmatrix,
       t1.useampereturn,       
       t4.name,
'''

        if columnIndex == 0:            
            SQL += """order by id
                   """
        if columnIndex == 1:            
            SQL += """order by t1.fullname """ + desc + """
                   """
        if columnIndex == 2:            
            SQL += """order by t1.number """ + desc + """, t1.fullname
                   """
        if columnIndex == 3:            
            SQL += """order by t1.description """ + desc + """, t1.fullname
                   """
        if columnIndex == 4:            
            SQL += """order by t1.needclimatlog """ + desc + """, t1.fullname
                   """
        if columnIndex == 5:            
            SQL += """order by t2.fullname """ + desc + """, t1.fullname
                   """
        if columnIndex == 6:            
            SQL += """order by t1.hostname """ + desc + """, t1.fullname
                   """
        if columnIndex == 7:            
            SQL += """order by t3.gost """ + desc + """, t1.fullname
                   """
        if columnIndex == 8:            
            SQL += """order by t1.supervisorreport """ + desc + """, t1.fullname
                   """
        if columnIndex == 9:            
            SQL += """order by t1.checkreport """ + desc + """, t1.fullname
                   """
        if columnIndex == 10:            
            SQL += """order by t1.ticketmatrix """ + desc + """, t1.fullname
                   """
        if columnIndex == 11:            
            SQL += """order by t1.useampereturn """ + desc + """, t1.fullname
                   """
        if columnIndex == 12:            
            SQL += """order by t4.name """ + desc + """, t1.fullname
                   """
   
        print SQL


        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка1",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
        
        
        model.setQuery(query)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Название")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Номер")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Описание")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Вести\nжурнал\nклимата")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Помещение")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Имя\nкомпьютера")
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Гост")
        model.setHeaderData(8, QtCore.Qt.Horizontal, u"ЦСМ")
        model.setHeaderData(9, QtCore.Qt.Horizontal, u"Прото\nкол")
        model.setHeaderData(10, QtCore.Qt.Horizontal, u"Нак\nлейки")
        model.setHeaderData(11, QtCore.Qt.Horizontal, u"Отображать\nампер-\nвиток")
        model.setHeaderData(12, QtCore.Qt.Horizontal, u"Тип испытания")
            
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
        self.ui.tableView.setColumnWidth(10, withCol10)
        self.ui.tableView.setColumnWidth(11, withCol11)
        self.ui.tableView.setColumnWidth(12, withCol12)
        
        self.ui.tableView.setColumnHidden(0,  True)
        '''
        self.ui.tableView.setColumnHidden(13,  True)
        self.ui.tableView.setColumnHidden(14, True)
        self.ui.tableView.setColumnHidden(15, True)
        self.ui.tableView.setColumnHidden(16, True)
        '''
        
        for i in range(15):
            self.ui.tableView.setColumnHidden(i + 13, True)
        
        
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        self.ui.pushButton_4.setEnabled(enab)
        




    def selOperator(self):
                
        row = self.selModel.currentIndex().row()
#        print 'row = row = row = ', row
        global id_stand
        if row < 0:
            id_stand = -1
#            self.CODE_TRANS = -1
#            self.NAME_TRANS = ''
        else:    
            id_stand = int(model.record(row).field('id').value().toString())
#            self.CODE_TRANS = int(model.record(row).field('id').value().toString())
#            self.NAME_TRANS = unicode(model.record(row).field('fullname').value().toString())
                                    
 #       print 'id_stand = ', id_stand   
        #print 'self.NAME_TRANS = ', self.NAME_TRANS        
        query = QSqlQuery(db1)
        SQL = u"""
select
t1.id,
operator,
fio
from stand_user as t1, operator as t2
where stand = :stand
and t1.operator = t2.id 
order by fio
"""
        
        
        query.prepare(SQL)
        query.bindValue(":stand", id_stand)
 
        
        if not query.exec_():
            print unicode(query.lastError().text())
 
        
        model_2.setQuery(query)

        model_2.setHeaderData(2,  QtCore.Qt.Horizontal, u"Оператор")
        
            
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(1, True)
        #self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(2,  withCol_1)
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)
        
        
        
        
        
        
        '''        
        row = self.selModel.currentIndex().row()
        print 'row = row = row = ', row
        global id_transformer
        if row < 0:
            id_transformer = -1
            self.CODE_TRANS = -1
            self.NAME_TRANS = ''
        else:    
            id_transformer = int(model.record(row).field('id').value().toString())
            self.CODE_TRANS = int(model.record(row).field('id').value().toString())
            self.NAME_TRANS = unicode(model.record(row).field('fullname').value().toString())
            
            
            
        print 'id_transformer = ', id_transformer   
        print 'self.NAME_TRANS = ', self.NAME_TRANS        
        query = QSqlQuery(db1)
        query.prepare("""select
id,
coiltype,
coilnumber,
tap,
classaccuracy,
primarycurrent,
secondcurrent,
secondload,
magneticvoltage,
magneticcurrent,
resistance,
rating,
--quadroload,
ampereturn
                                                                      
from coil
where transformer = :transformer 
order by coilnumber, tap""")
        
        
        query.bindValue(":transformer", id_transformer)
        
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_2.setQuery(query)

        model_2.setHeaderData(1,  QtCore.Qt.Horizontal, u"Тип")
        model_2.setHeaderData(2,  QtCore.Qt.Horizontal, u"Номер")
        model_2.setHeaderData(3,  QtCore.Qt.Horizontal, u"Отпайка")
        model_2.setHeaderData(4,  QtCore.Qt.Horizontal, u"Класс\nточности")
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Первич.\nток")
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Вторич.\nток")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Вторич.\nнагрузка")
                
        model_2.setHeaderData(8,  QtCore.Qt.Horizontal, u"Напряжение(магн.)")
        model_2.setHeaderData(9,  QtCore.Qt.Horizontal, u"Ток(магн.)")
        model_2.setHeaderData(10,  QtCore.Qt.Horizontal, u"Сопротивление")
        model_2.setHeaderData(11,  QtCore.Qt.Horizontal, u"Коэфф.")
        model_2.setHeaderData(12,  QtCore.Qt.Horizontal, u"Ампер-витки")
        
            
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(1,  withCol_1)
        self.ui.tableView_2.setColumnWidth(2,  withCol_2)
        self.ui.tableView_2.setColumnWidth(3,  withCol_3)
        self.ui.tableView_2.setColumnWidth(4,  withCol_4)
        self.ui.tableView_2.setColumnWidth(5,  withCol_5)
        self.ui.tableView_2.setColumnWidth(6,  withCol_6)
        self.ui.tableView_2.setColumnWidth(7,  withCol_7)
        self.ui.tableView_2.setColumnWidth(8,  withCol_8)
        self.ui.tableView_2.setColumnWidth(9,  withCol_9)
        self.ui.tableView_2.setColumnWidth(10, withCol_10)
        self.ui.tableView_2.setColumnWidth(11, withCol_11)
        self.ui.tableView_2.setColumnWidth(12, withCol_12)
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)
        '''
        
        
        
        
        

    def selectionChanged(self):
        self.selOperator()

    def selectionChanged_2(self):
        global id_coil
        row = self.selModel_2.currentIndex().row()
        id_coil = model_2.record(row).field('id').value().toString()

    '''
    def comboBox_indexChanged(self):
        model_2.clear()        
        model_2.reset()        
        model.clear()        
        model.reset()
        self.selTrans()        
'''
        

# Редактирование трансов (начало кода)        
                        
    class editStand(QtGui.QDialog, UILoader):
        def __init__(self, _env):
#            global mnu_2
            self.mnu = None
            self.mnu_2 = None
            self.mnu_3 = None
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editStand.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)
            self.ui.pushButton_4.clicked.connect(self.pushButton4_Click)
            self.ui.pushButton_5.clicked.connect(self.pushButton5_Click)

        # Организация меню помещений
            self.mnu = QtGui.QMenu(self)
            query = QSqlQuery(db1)
            query.prepare("select id, fullname from room order by fullname")
            query.exec_()                        
            model_.setQuery(query)   
            for i in range(model_.rowCount()):
                action = self.mnu.addAction(model_.record(i).field('fullname').value().toString())
                action.setData(model_.record(i).field('id').value().toString())
            self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_Click)
        
        # Организация меню гостов
            self.mnu_2 = QtGui.QMenu(self)
            query = QSqlQuery(db1)
            query.prepare("select id, gost from gost order by gost")
            query.exec_()                        
            model_.setQuery(query)   
            for i in range(model_.rowCount()):
                action = self.mnu_2.addAction(model_.record(i).field('gost').value().toString())
                action.setData(model_.record(i).field('id').value().toString())
            self.connect(self.mnu_2, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_2_Click)
        
        # Организация меню типов испытаний
            self.mnu_3 = QtGui.QMenu(self)
            query = QSqlQuery(db1)
            query.prepare("select id, name from test_type order by name")
            query.exec_()                        
            model_.setQuery(query)   
            for i in range(model_.rowCount()):
                action = self.mnu_3.addAction(model_.record(i).field('name').value().toString())
                action.setData(model_.record(i).field('id').value().toString())
            self.connect(self.mnu_3, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_3_Click)
        
        
            self.room_id = None
            self.gost_id = None
            self.type_id = None
        
        
             

        def mnu_Click(self, q):
            print int(q.data().toString())
            self.room_id = int(q.data().toString())
#            self.type_transformer = int(q.data().toString())
#            if int(q.data().toString()) == -2:
#                self.type_transformer = None    
            self.ui.lineEdit.setText(unicode(q.text()))

        def mnu_2_Click(self, q):
            print int(q.data().toString())
            self.gost_id = int(q.data().toString())
#            self.type_transformer = int(q.data().toString())
#            if int(q.data().toString()) == -2:
#                self.type_transformer = None    
            self.ui.lineEdit_2.setText(unicode(q.text()))

        def mnu_3_Click(self, q):
            print int(q.data().toString())
            self.type_id = int(q.data().toString())
            self.ui.lineEdit_3.setText(unicode(q.text()))

        
        def pushButton1_Click(self):
                                                
            if self.ui.lineEdit.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи помещение', QMessageBox.Ok)
                return
            if self.ui.lineEdit_2.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи гост', QMessageBox.Ok)
                return
            if self.ui.lineEdit_3.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи тип испытания', QMessageBox.Ok)
                return
            if self.ui.lineEdit_4.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи название испытания', QMessageBox.Ok)
                return
            if self.ui.lineEdit_5.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи компьютер', QMessageBox.Ok)
                return
            if self.ui.spinBox.text() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи номер испытания', QMessageBox.Ok)
                return
                        
            
#            global id_coil
#            global id_type
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                query.prepare('''INSERT INTO stand (
                                     fullname,  number,  description,  needclimatlog,  room,  hostname,  enablesupervisor,  enableassistant,
                                     singleitem,  gost_id,  supervisorreport,  checkreport,  ticketmatrix,  useampereturn,  test_type)
                                 values (
                                    :fullname, :number, :description, :needclimatlog, :room, :hostname, :enablesupervisor, :enableassistant,
                                    :singleitem, :gost_id, :supervisorreport, :checkreport, :ticketmatrix, :useampereturn, :test_type)''')            
            else:
                query.prepare('''UPDATE stand SET
                                    fullname = :fullname,
                                    number = :number,
                                    description = :description,
                                    needclimatlog = :needclimatlog,
                                    room = :room,
                                    hostname = :hostname,
                                    enablesupervisor = :enablesupervisor,
                                    enableassistant = :enableassistant,
                                    singleitem = :singleitem,       
                                    gost_id = :gost_id,
                                    supervisorreport = :supervisorreport,
                                    checkreport = :checkreport,
                                    ticketmatrix = :ticketmatrix,
                                    useampereturn = :useampereturn,
                                    test_type = :test_type                                                        
                                 WHERE id = :id''')

                query.bindValue(":id", id_stand);


            '''
select t1.id,
       t1.fullname,
       t1.number,
       t1.description,
       t1.needclimatlog,
       t2.fullname as name_room,
       t1.hostname,
       t3.gost,       
       t1.supervisorreport,
       t1.checkreport,
       t1.ticketmatrix,
       t1.useampereturn,       
       t4.name,
       t4.code,
       t1.enablesupervisor,
       t1.enableassistant,
       t1.singleitem,
       t1.room,
       t1.gost_id,
       t1.test_type,       
       case when needclimatlog then 1 else 0 end as needclimatlog_,
       case when enablesupervisor then 1 else 0 end as enablesupervisor_,
       case when enableassistant then 1 else 0 end as enableassistant_,
       case when singleitem then 1 else 0 end as singleitem_,
       case when useampereturn then 1 else 0 end as useampereturn_,
       case when supervisorreport then 1 else 0 end as supervisorreport_,
       case when checkreport then 1 else 0 end as checkreport_,
       case when ticketmatrix then 1 else 0 end as ticketmatrix_
       
       
       
                                    fullname = :fullname,
                                    number = :number,
                                    description = :description,
                                    needclimatlog = :needclimatlog,
                                    room = :room,
                                    hostname = :hostname,
                                    enablesupervisor = :enablesupervisor,
                                    enableassistant = :enableassistant,
                                    singleitem = :singleitem,       
                                    gost_id = :gost_id,
                                    supervisorreport = :supervisorreport,
                                    checkreport = :checkreport,
                                    ticketmatrix = :ticketmatrix,
                                    useampereturn = :useampereturn,
                                    test_type = :test_type                                                               
'''
                
            query.bindValue(":fullname", noneValue(self.ui.lineEdit_4.text()))
            query.bindValue(":number", self.ui.spinBox.value())            
#            query.bindValue(":description", noneValue(self.ui.lineEdit_6.text()))
            query.bindValue(":description", noneValue(self.ui.textEdit.toPlainText()))
                       
            query.bindValue(":needclimatlog", self.ui.checkBox.isChecked())
            query.bindValue(":room", self.room_id)            
            query.bindValue(":hostname", noneValue(self.ui.lineEdit_5.text()))
            query.bindValue(":enablesupervisor", self.ui.checkBox_2.isChecked())
            query.bindValue(":enableassistant", self.ui.checkBox_3.isChecked())
            query.bindValue(":singleitem", self.ui.checkBox_4.isChecked())
            query.bindValue(":gost_id", self.gost_id)            
            query.bindValue(":supervisorreport", self.ui.checkBox_6.isChecked())
            query.bindValue(":checkreport", self.ui.checkBox_7.isChecked())
            query.bindValue(":ticketmatrix", self.ui.checkBox_8.isChecked())
            query.bindValue(":useampereturn", self.ui.checkBox_5.isChecked())
            query.bindValue(":test_type", self.type_id)            
            
                        
                        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()


        def pushButton3_Click(self):
#            global mnu_2
            #mnu_2
            print 'pushButton3_Click'
            self.mnu.exec_(QPoint(self.ui.lineEdit.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit.geometry().height())) 

        def pushButton4_Click(self):
#            global mnu_2
            #mnu_2
            print 'pushButton4_Click'
            self.mnu_2.exec_(QPoint(self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_2.geometry().height())) 

        def pushButton5_Click(self):
#            print 'pushButton3_Click'
            self.mnu_3.exec_(QPoint(self.ui.lineEdit_3.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_3.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_3.geometry().height())) 

                            
# Редактирование трансов (конец кода)        


# Редактирование катушек (начало кода)        
                        
    class editCoil(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editCoil.ui")        
                        
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
        
        
        def pushButton1_Click(self):
            
            global id_coil
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                query.prepare('''INSERT INTO coil (transformer, coiltype, coilnumber, tap, classaccuracy,
                                                   primarycurrent, secondcurrent, secondload, magneticvoltage,
                                                   magneticcurrent, resistance, rating, ampereturn) 
                                  values (:transformer, :coiltype, :coilnumber, :tap, :classaccuracy,
                                          :primarycurrent, :secondcurrent, :secondload, :magneticvoltage,
                                          :magneticcurrent, :resistance, :rating, :ampereturn)''')            
                query.bindValue(":transformer", id_stand);
            else:
                query.prepare('''UPDATE coil SET coiltype = :coiltype, 
                                                 coilnumber = :coilnumber,
                                                 tap = :tap,
                                                 classaccuracy = :classaccuracy,
                                                 primarycurrent = :primarycurrent,
                                                 secondcurrent = :secondcurrent,
                                                 secondload = :secondload,
                                                 magneticvoltage = :magneticvoltage,
                                                 magneticcurrent = :magneticcurrent,
                                                 resistance = :resistance,
                                                 rating = :rating,
                                                 ampereturn = :ampereturn
                                                 WHERE id = :id''')

                query.bindValue(":id", id_coil);
                

            if float(self.ui.spinBox.text()) == 0:            
                query.bindValue(":coiltype",      None)
            else:    
                query.bindValue(":coiltype",      self.ui.spinBox.text())
                
            query.bindValue(":coilnumber",      self.ui.spinBox_2.text())
            query.bindValue(":tap",             self.ui.spinBox_3.text())
            query.bindValue(":classaccuracy",   self.ui.lineEdit.text())
            
            rez = self.none(self.ui.doubleSpinBox.text(), False)
            if rez == 'error':
                return
            query.bindValue(":primarycurrent", rez)
            
            rez = self.none(self.ui.doubleSpinBox_2.text(), False)
            if rez == 'error':
                return
            query.bindValue(":secondcurrent", rez)
            
            rez = self.none(self.ui.doubleSpinBox_3.text(), True)
            if rez == 'error':
                return
            query.bindValue(":secondload", rez)
            
            rez = self.none(self.ui.doubleSpinBox_4.text(), False)
            if rez == 'error':
                return
            query.bindValue(":magneticvoltage", rez)
            
            rez = self.none(self.ui.doubleSpinBox_5.text(), False)
            if rez == 'error':
                return
            query.bindValue(":magneticcurrent", rez)
            
            rez = self.none(self.ui.doubleSpinBox_6.text(), False)
            if rez == 'error':
                return
            query.bindValue(":resistance", rez)
                
            query.bindValue(":rating",          self.ui.lineEdit_2.text())
            
            
            if float(self.ui.spinBox_4.text()) == 0:            
                query.bindValue(":ampereturn",      None)
            else:    
                query.bindValue(":ampereturn",      self.ui.spinBox_4.text())
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()
            
# Редактирование катушек (конец кода)        


        def none(self, text, not_null):
            try:
              text_ = text.replace(',', '.')  
              if float(text_) == 0 and not not_null:            
                  return None
              else:    
                  return text
            except Exception:
                QMessageBox.warning(self, u"Предупреждение",  u'Величина: ' + text + u' не корректна!', QMessageBox.Ok)
                return 'error'


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
        
        wind = sprStand(env, 0)
        wind.setEnabled(True)
        wind.ui.groupBox.setVisible(False)
        wind.ui.pushButton_5.setVisible(False)
        wind.ui.pushButton_10.setVisible(False)
        wind.ui.label_3.setText(u'Пользователи стендов')                                
        wind.setWindowTitle(u'Стенды')
        wind.show()
        sys.exit(app.exec_())


