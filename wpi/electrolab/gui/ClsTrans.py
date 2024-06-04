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

id_transformer = -1
id_coil = -1
id_trans_copy = -1


# self.model.setSortRole(QtCore.Qt.UserRole)

#QtGui.QTableView.horizontalHeader().

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 100
withCol2 = 25
withCol3 = 25
withCol4 = 25
withCol5 = 25
withCol6 = 25                        
withCol7 = 25                       
withCol8 = 25                       
withCol9 = 25                       
withCol10 = 25                       
withCol11 = 25                       
withCol12 = 25                       

withCol_1 = 50
withCol_2 = 50
withCol_3 = 50
withCol_4 = 50
withCol_5 = 50
withCol_6 = 50                        
withCol_7 = 50                       
withCol_8 = 50                       
withCol_9 = 50                       
withCol_10 = 50                       
withCol_11 = 50                       
withCol_12 = 50                       
#withCol_13 = 50                       

isSave = False
#id_type = None
mnu_2 = None


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
#            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7 + withCol8 + withCol9 + withCol10 + withCol11 + withCol12 + withCol13))
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
            obj.setColumnWidth(13, koef * withCol12)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4 + withCol_5 + withCol_6 + withCol_7 + withCol_8 + withCol_9 + withCol_10 + withCol_11 + withCol_12))
            obj.setColumnWidth(1, koef * withCol_1)
            obj.setColumnWidth(2, koef * withCol_2)
            obj.setColumnWidth(3, koef * withCol_3)
            obj.setColumnWidth(4, koef * withCol_4)
            obj.setColumnWidth(5, koef * withCol_5)
            obj.setColumnWidth(6, koef * withCol_6)
            obj.setColumnWidth(7, koef * withCol_7)
            obj.setColumnWidth(8, koef * withCol_8)
            obj.setColumnWidth(9, koef * withCol_9)
            obj.setColumnWidth(10, koef * withCol_10)
            obj.setColumnWidth(11, koef * withCol_11)
            obj.setColumnWidth(12, koef * withCol_12)
            VSB2 = obj.verticalScrollBar().isVisible()




        return False

        

#        QtGui.QPushButton.pos()

   
#class ClsTrans(QWidget, UILoader):    
#    def __init__(self, _env):
        
class ClsTrans(QtGui.QDialog, UILoader):
    def __init__(self, _env, sw, *args):
        QtGui.QDialog.__init__(self, *args)        
        
        global currColumnIndex
        currColumnIndex = 0
        global desc
        desc = ''
        
        #global id_type
        global mnu_2

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
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
        self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)
        self.ui.pushButton_9.clicked.connect(self.pushButton_9_Click)
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_Click)

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
        
        self.selTypeTrans()

        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_indexChanged)        
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
            #self.ui.groupBox_2.setVisible(False)
            
            
#        self.NAME_TRANS = 'QWERTYU'    
#        self.CODE_TRANS = 0
        self.IS_SELECT = False    

#        QMessageBox.warning(self, u"Предупреждение",  self.NAME_TRANS, QMessageBox.Ok)
            
            
        # Организация контекстного меню на кнопке "Добавить"
        fnt = QtGui.QFont()
        fnt.setPointSize(14)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Добавить с копированием', self))
        self.mnu.setFont(fnt)        
        self.ui.pushButton.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.ui.pushButton.customContextMenuRequested.connect(self.on_context_menu)      
        self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.pushButton_Click_copy)

        # Организация меню типов трансов
        self.mnu_2 = QtGui.QMenu(self)
        mnu_2 = QtGui.QMenu(self)
        query = QSqlQuery(db1)
#        query.prepare("select distinct type from transformer order by type")
        query.prepare("select id, type from type_transformer order by type")
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
        
        
        '''       
        print 'action =', action
        print 'action2 =', action.objectName()
        print 'action3 =', unicode(action.text())
        print 'action4 =', action.data().toInt()
        print 'action5 =', action.data().toString()
        print 'action6 =', str(self.mnu_2.actions())
        for act in self.mnu_2.actions():
            print act.data().toString(), unicode(act.text())
        '''    
        
        self.connect(self.mnu_2, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_2_Click)

   ##############################################     self.mnu_2.actions()


 #       QtGui.QAction.data()
 #       QtGui.QAction.objectName()
 #        QtGui.QActionGroup 

#        QtGui.QMenu.actions()
#        object.

#        QPoint p( 0 , 0 );  // Recall that widget 'lineEdit' is in a layout, which is itself in a layout
#        QPoint point = ui.lineEdit->mapToGlobal( p );
     

#        global currColumnIndex
#        currColumnIndex = 0
#        global desc
#        desc = ''
        self.selTrans(currColumnIndex, False)


# Настройка сортировки при нажатии колонки      
# пример     https://coderoad.ru/14068823/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-QTableView-%D0%B2-PyQt

        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)


    def sortByColumn(self, columnIndex):
        print 'sortByColumn sortByColumn sortByColumn sortByColumn sortByColumn  ', columnIndex
        global currColumnIndex
        self.selTrans(columnIndex, False)

      
    def on_context_menu(self, point):
        self.mnu.exec_(self.ui.pushButton.mapToGlobal(point))

    def mnu_2_Click(self, q):
        #global id_type
        self.id_type = int(q.data().toString())    
        self.ui.lineEdit_2.setText(unicode(q.text()))
            
 #       QtGui.QLineEdit.tag    
#        QtGui.QMenu.add    


# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        global currColumnIndex
        self.wind = self.editTrans(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового трансформатора')
        row = self.selModel.currentIndex().row()
        self.wind.ui.lineEdit.setText(model.record(row).field('type').value().toString())
        isSave = False        
        self.wind.exec_()
        if isSave:
            print 'selTrans1'
            self.selTrans(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM transformer");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            
            


    def pushButton_Click_copy(self):
        
        '''
        model.sort(1)
        model.sort(2)
        return
        '''
        
   
        global isSave        
        global id_trans_copy        
        global currColumnIndex
        self.wind = self.editTrans(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового трансформатора')
        row = self.selModel.currentIndex().row()
        
        id_trans_copy = int(model.record(row).field('id').value().toString())
        print 'id_trans_copy = ', id_trans_copy, type(id_trans_copy)
        
        self.wind.ui.lineEdit.setText(model.record(row).field('fullname').value().toString())
        self.wind.ui.lineEdit_2.setText(model.record(row).field('thermal_current').value().toString())
        self.wind.ui.lineEdit_3.setText(model.record(row).field('dynamic_current').value().toString())
        self.wind.ui.lineEdit_4.setText(model.record(row).field('voltage').value().toString())        
        self.wind.ui.lineEdit_5.setText(model.record(row).field('maxopervoltage').value().toString())
        self.wind.ui.lineEdit_6.setText(model.record(row).field('time_thermal_current').value().toString())
        
        self.wind.ui.lineEdit_7.setText(spaceValue(model.record(row).field('isolationlevel')))        
        self.wind.ui.lineEdit_8.setText(spaceValue(model.record(row).field('climat')))        
        self.wind.ui.lineEdit_9.setText(spaceValue(model.record(row).field('weight')))        
        self.wind.ui.lineEdit_10.setText(spaceValue(model.record(row).field('copper_content')))        
        self.wind.ui.lineEdit_11.setText(spaceValue(model.record(row).field('copper_alloy_content')))        
                
        self.wind.ui.lineEdit_12.setText(spaceValue(model.record(row).field('type2')))
        if model.record(row).field('type_transformer').value().toString() != '': 
            self.wind.type_transformer = int(model.record(row).field('type_transformer').value().toString())        

        isSave = False        
        self.wind.exec_()
        if isSave:
            print 'selTrans1'
            self.selTrans(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM transformer");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            
            
            
            global id_trans_copy
            if id_trans_copy != -1:        
                r = QMessageBox.warning(self, u"Предупреждение", u"Копировать обмотки?", QMessageBox.Yes, QMessageBox.No)            
                if r == QMessageBox.Yes:
                    query = QSqlQuery(db1)
                    query.prepare('''INSERT INTO coil (transformer, coiltype, coilnumber, tap, classaccuracy, primarycurrent,
 secondcurrent, secondload, magneticvoltage, magneticcurrent, resistance, rating, ampereturn)
 SELECT :new_transformer, coiltype, coilnumber, tap, classaccuracy, primarycurrent,
 secondcurrent, secondload, magneticvoltage, magneticcurrent, resistance, rating, ampereturn
 FROM coil WHERE transformer = :transformer''')
                    query.bindValue(":new_transformer", id_search);
                    query.bindValue(":transformer", id_trans_copy);
                    id_trans_copy = -1
                
                    if not query.exec_():
                        QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                      
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            
            self.selCoil()
            
            
                
    def pushButton_2_Click(self):
        global isSave        
        global currColumnIndex
        self.wind = self.editTrans(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего трансформатора')
        row = self.selModel.currentIndex().row()
        self.wind.ui.lineEdit.setText(model.record(row).field('fullname').value().toString())
        self.wind.ui.lineEdit_2.setText(spaceValue(model.record(row).field('thermal_current')))        
        self.wind.ui.lineEdit_3.setText(spaceValue(model.record(row).field('dynamic_current')))        
        self.wind.ui.lineEdit_4.setText(spaceValue(model.record(row).field('voltage')))        
        self.wind.ui.lineEdit_5.setText(spaceValue(model.record(row).field('maxopervoltage')))        
        self.wind.ui.lineEdit_6.setText(spaceValue(model.record(row).field('time_thermal_current')))        
        self.wind.ui.lineEdit_7.setText(model.record(row).field('isolationlevel').value().toString())
        self.wind.ui.lineEdit_8.setText(model.record(row).field('climat').value().toString())
        self.wind.ui.lineEdit_9.setText(spaceValue(model.record(row).field('weight')))
        self.wind.ui.lineEdit_10.setText(spaceValue(model.record(row).field('copper_content')))        
        self.wind.ui.lineEdit_11.setText(spaceValue(model.record(row).field('copper_alloy_content')))        
        
        if model.record(row).field('type_transformer').value().toString() != '0': 
            self.wind.ui.lineEdit_12.setText(spaceValue(model.record(row).field('type2')))
            self.wind.type_transformer = int(model.record(row).field('type_transformer').value().toString())
            print '111' + model.record(row).field('type_transformer').value().toString() + '333'
        else:
            print 222            
            self.wind.ui.lineEdit_12.setText(u'Без типа')
            self.wind.type_transformer = None
                        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selTrans(currColumnIndex, True)
            self.ui.tableView.selectRow(row)                                            



                       
 ###           self.ui.tableView_2.selectRow(row)                                    


    def pushButton_3_Click(self):
        print 'QSqlQueryModel.rowCount(parent=QModelIndex() = ', model_2.rowCount()
        global currColumnIndex
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале обмотки!', QMessageBox.Ok)
                return
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM transformer WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
#            self.selTrans()
            self.selTrans(currColumnIndex, False)
            
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                        
                                
    def pushButton_4_Click(self):
        global isSave        
        self.wind = self.editCoil(self.env)
        self.wind.tag = 1
                
        self.wind.ui.lineEdit_3.setText(model.record(self.selModel.currentIndex().row()).field('fullname').value().toString())        
                
        self.wind.setWindowTitle(u'Добавление новой обмотки (отпайки)')
        # Вычисление следующего порядкового номера обмотки 
        query = QSqlQuery(db1)
        query.prepare("""SELECT CASE WHEN (MAX(coilnumber) IS NULL) THEN 1 ELSE MAX(coilnumber) + 1 END 
                         FROM coil WHERE transformer = :transformer""");
        query.bindValue(":transformer", id_transformer)
        query.exec_()
        query.next()

        self.wind.ui.spinBox_2.setValue(int(query.value(0).toString()))

        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selCoil()
            
                
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
            self.selCoil()
            # навигация
            self.ui.tableView_2.selectRow(row)                                    

            
    def pushButton_6_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM coil WHERE id = :ID")
            row = self.selModel_2.currentIndex().row()                
            query.bindValue(":id", model_2.record(row).field('id').value().toString());
            query.exec_()
            self.selCoil()
                                
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

    def pushButton_10_Click(self):
        global currColumnIndex
        s = u'Вы действительно желаете произвести присоединение '
        SQL = """select id, type from type_transformer
        """
#        if self.ui.lineEdit_2.text() == u'Все типы':
        if self.id_type == -1:           
            s += u' по всем типам?'
#        if self.ui.lineEdit_2.text() == u'Без типа':
        if self.id_type == -2:           
            s += u'только по трансформаторам без типа?'
                        
#        if self.ui.lineEdit_2.text() != u'Все типы' and self.ui.lineEdit_2.text() != u'Без типа':
        if self.id_type != None and self.id_type != -1 and self.id_type != -2:     
            s += u'только\nпо типу: ' + self.ui.lineEdit_2.text() + '?'
            SQL += """where id = :id_type"""            
        
        r = QMessageBox.warning(self, u"Предупреждение", s, QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare(SQL)
            query.bindValue(":id_type", self.id_type)
            query.exec_()        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
                return
            model_3.setQuery(query)
            
            for i in range(model_3.rowCount()):
                type_transformer = int(model_3.record(i).field('id').value().toString())
                type = model_3.record(i).field('type').value().toString()
        
                query = QSqlQuery(db1)
                SQL = """UPDATE transformer SET type_transformer = :type_transformer
                WHERE fullname like '""" + unicode(type) + """%'                
                """
                if self.id_type == -2:           
                    SQL += '''AND type_transformer IS NULL'''
                    
                query.prepare(SQL)
                query.bindValue(":type_transformer", type_transformer)
                print SQL           
                if not query.exec_():
                    QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                    return
        
            self.selTrans(currColumnIndex, True)
            QMessageBox.warning(self, u"Предупреждение",  u"Присоединение типов прошло успешно!", QMessageBox.Ok)
        
                
            
    def lineEdit_textChanged(self):
        global currColumnIndex
        self.selTrans(currColumnIndex, False)
        #self.ViewZavMsr(0, -1, self.lineEdit.text())
            
                        
            
    # Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
    def searchInModel(self, id_search, tableView, model):
        print 'id_search=', id_search
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
            print 'i=', i
            print model.query().value(0).toString(), id_search
            while model.query().value(0).toString() != id_search:
                #print model.query().value(0).toString()
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
                print 'i1=', i
                print model.query().value(0).toString(), id_search
            tableView.selectRow(i)
            
            
            
            
            

    def selTypeTrans(self):
        query = QSqlQuery(db1)
        query.prepare("select distinct type from transformer order by type")
        #query.bindValue(":id_category", id_category)
        query.exec_()        
        
        model_.setQuery(query)
        
        for i in range(model_.rowCount()):
            self.ui.comboBox.addItem(model_.record(i).field(0).value().toString())
        #self.ui.comboBox.addSeparator()
        self.ui.comboBox.addItem(u'Все типы')

        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.count() - 1)
        
        #QtGui.QComboBox.setCurrentIndex()
       # QtGui.QComboBox.count()

    def selTrans(self, columnIndex, isEdit):        
#    def selTrans(self):
        #global id_type
        
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
        
        
        v = unicode(self.ui.lineEdit.text()).upper()
        
        query = QSqlQuery(db1)
                                
        SQL = """select t1.id,
        fullname,
        thermal_current,
        dynamic_current,
        voltage,
        maxopervoltage,        
        time_thermal_current,
        isolationlevel,
        climat,
        weight,
        copper_content,
        copper_alloy_content,
        type_transformer,
        t2.type as type2
        from transformer t1 LEFT OUTER JOIN type_transformer t2 ON (t1.type_transformer = t2.id)
        where 0=0
        """
        
        if self.ui.comboBox.currentText() != u"Все типы":
            SQL += """and t1.type=:type
                   """
        
        if v != "":
            SQL += """and upper(fullname) like :v
                   """
            
        if self.id_type != None and self.id_type != -1:
            if self.id_type == -2:     
                SQL += """and t2.id is null
                       """
            else:           
                SQL += """and t2.id =:id_type
                       """
               
        if columnIndex == 0:            
            SQL += """order by id desc
                   """
        if columnIndex == 1:            
            SQL += """order by fullname """ + desc + """
                   """
        if columnIndex == 2:            
            SQL += """order by thermal_current """ + desc + """, fullname
                   """
        if columnIndex == 3:            
            SQL += """order by dynamic_current """ + desc + """, fullname
                   """
        if columnIndex == 4:            
            SQL += """order by voltage """ + desc + """, fullname
                   """
        if columnIndex == 5:            
            SQL += """order by maxopervoltage """ + desc + """, fullname
                   """
        if columnIndex == 6:            
            SQL += """order by time_thermal_current """ + desc + """, fullname
                   """
        if columnIndex == 7:            
            SQL += """order by isolationlevel """ + desc + """, fullname
                   """
        if columnIndex == 8:            
            SQL += """order by climat """ + desc + """, fullname
                   """
        if columnIndex == 9:            
            SQL += """order by weight """ + desc + """, fullname
                   """
        if columnIndex == 10:            
            SQL += """order by copper_content """ + desc + """, fullname
                   """
        if columnIndex == 11:            
            SQL += """order by copper_alloy_content """ + desc + """, fullname
                   """
        if columnIndex == 12:            
            SQL += """order by type_transformer """ + desc + """, fullname
                   """
        if columnIndex == 13:            
            SQL += """order by type2 """ + desc + """, fullname
                   """

               
               
        print SQL       
        query.prepare(SQL)

        if self.ui.comboBox.currentText() != u"Все типы":
            query.bindValue(":type", self.ui.comboBox.currentText())
        if v != "":
            query.bindValue(":v", '%' + v + '%')
                        
        if self.id_type != None and self.id_type != -1 and self.id_type != -2:     
            query.bindValue(":id_type", self.id_type)
                        
#        if not query.exec_():
#            print unicode(query.lastError().text())        
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
                
        model.setQuery(query)

        model.setHeaderData(1,  QtCore.Qt.Horizontal, u"Наименование")
        model.setHeaderData(2,  QtCore.Qt.Horizontal, u"Ток\nтермической\nстойкости,  кА")
        model.setHeaderData(3,  QtCore.Qt.Horizontal, u"Ток\nэл/дина-\nмической\nстойкости, кА")
        model.setHeaderData(4,  QtCore.Qt.Horizontal, u"Напряжение\n(ном.)")
        model.setHeaderData(5,  QtCore.Qt.Horizontal, u"Напряжение\n(мах.)")
        model.setHeaderData(6,  QtCore.Qt.Horizontal, u"Время\nпротекания\nтока\nтермической\nстойкости, с")
        model.setHeaderData(7,  QtCore.Qt.Horizontal, u"Уровинь\nизоляции")
        model.setHeaderData(8,  QtCore.Qt.Horizontal, u"Выриант\nконструктивного\nисполнения")
        model.setHeaderData(9,  QtCore.Qt.Horizontal, u"Масса")
        model.setHeaderData(10, QtCore.Qt.Horizontal, u"Содержание\nмеди, кг")
        model.setHeaderData(11, QtCore.Qt.Horizontal, u"Содержание\nмедных\nсплавов, кг")
        model.setHeaderData(13, QtCore.Qt.Horizontal, u"Тип")
        
                    
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
        self.ui.tableView.setColumnHidden(12, True)
#        QMessageBox.warning(self, u"Ошибка",  '1', QMessageBox.Ok)
        self.ui.tableView.selectRow(0)
#        QMessageBox.warning(self, u"Ошибка",  '2', QMessageBox.Ok)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        self.ui.pushButton_4.setEnabled(enab)
        


    def selCoil(self):
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
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Первич. ток/\nнапряжение")
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Вторич. ток/\nнапряжение")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Вторич.\nнагрузка")
                
        model_2.setHeaderData(8,  QtCore.Qt.Horizontal, u"Напряжение\n(магн.)")
        model_2.setHeaderData(9,  QtCore.Qt.Horizontal, u"Ток(магн.)")
        model_2.setHeaderData(10,  QtCore.Qt.Horizontal, u"Сопротив-\nление")
        model_2.setHeaderData(11,  QtCore.Qt.Horizontal, u"Коэфф.")
#        model_2.setHeaderData(12,  QtCore.Qt.Horizontal, u"Четвертная\nнагрузка")
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
        

    def selectionChanged(self):
        self.selCoil()

    def selectionChanged_2(self):
        global id_coil
        row = self.selModel_2.currentIndex().row()
        id_coil = model_2.record(row).field('id').value().toString()


    def comboBox_indexChanged(self):
        global currColumnIndex
        model_2.clear()        
        model_2.reset()        
        model.clear()        
        model.reset()
        self.selTrans(currColumnIndex, False)        


# Редактирование трансов (начало кода)        
                        
    class editTrans(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            global mnu_2
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editTrans.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)

            self.connect(mnu_2, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_2_Click)
        
            self.type_transformer = None
             

        def mnu_2_Click(self, q):
#            self.id_type = int(q.data().toString())    
            self.type_transformer = int(q.data().toString())
            if int(q.data().toString()) == -2:
                self.type_transformer = None    
            self.ui.lineEdit_12.setText(unicode(q.text()))

        
        def pushButton1_Click(self):
                                                
#            if self.ui.lineEdit.text().trimmed() == '':
#                QMessageBox.warning(self, u"Предупреждение",  u'Укажи тип трансформатора', QMessageBox.Ok)
#                return
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи наименование трансформатора', QMessageBox.Ok)
                self.ui.lineEdit.setFocus()
                return
#            if self.ui.lineEdit_3.text().trimmed() == '':
#                QMessageBox.warning(self, u"Предупреждение",  u'Укажи краткое наименование трансформатора', QMessageBox.Ok)
#                return
                        
            thermal_current = None
            if self.ui.lineEdit_2.text().trimmed() != '':
                try:
                    thermal_current = float(self.ui.lineEdit_2.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина тока термической стойкости не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_2.setFocus()
                    return

            dynamic_current = None
            if self.ui.lineEdit_3.text().trimmed() != '':
                try:
                    dynamic_current = float(self.ui.lineEdit_3.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина тока динамической эл/стойкости не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_3.setFocus()
                    return
                        
            voltage = None
            if self.ui.lineEdit_4.text().trimmed() != '':
                try:
                    voltage = float(self.ui.lineEdit_4.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина номинального напряжения не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_4.setFocus()
                    return
            maxopervoltage = None
            if self.ui.lineEdit_5.text().trimmed() != '':
                try:
                    maxopervoltage = float(self.ui.lineEdit_5.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина максимального напряжения не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_5.setFocus()
                    return
                                
            time_thermal_current = None
            if self.ui.lineEdit_6.text().trimmed() != '':
                try:
                    time_thermal_current = int(self.ui.lineEdit_6.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Время протекания тока термической стойкости не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_6.setFocus()
                    return
                
            weight = None
            if self.ui.lineEdit_9.text().trimmed() != '':
                try:
                    weight = float(self.ui.lineEdit_9.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина масссы не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_9.setFocus()
                    return

            copper_content = None
            if self.ui.lineEdit_10.text().trimmed() != '':
                try:
                    copper_content = float(self.ui.lineEdit_10.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина содержания меди не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_10.setFocus()
                    return

            copper_alloy_content = None
            if self.ui.lineEdit_11.text().trimmed() != '':
                try:
                    copper_alloy_content = float(self.ui.lineEdit_11.text())
                except Exception:
                    QMessageBox.warning(self, u"Предупреждение",  u'Величина содержания медных сплавов не корректна', QMessageBox.Ok)
                    self.ui.lineEdit_11.setFocus()
                    return

            if self.ui.lineEdit_12.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи тип трансформатора', QMessageBox.Ok)
                self.ui.pushButton_3.setFocus()
                return


            
            global id_coil
#            global id_type
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                query.prepare('''INSERT INTO transformer (fullname, shortname, type, thermal_current, dynamic_current, voltage, maxopervoltage, time_thermal_current,
                                                          isolationlevel, climat, weight, copper_content, copper_alloy_content, type_transformer)
                                 values (:fullname, :shortname, :type, :thermal_current, :dynamic_current, :voltage, :maxopervoltage, :time_thermal_current,
                                         :isolationlevel, :climat, :weight, :copper_content, :copper_alloy_content, :type_transformer)''')            
            else:
                query.prepare('''UPDATE transformer SET fullname = :fullname,
                                                        shortname = :shortname,
                                                        type = :type,
                                                        thermal_current = :thermal_current,
                                                        dynamic_current = :dynamic_current,
                                                        voltage = :voltage,
                                                        maxopervoltage = :maxopervoltage,
                                                        time_thermal_current = :time_thermal_current,
                                                        isolationlevel = :isolationlevel,
                                                        climat = :climat,
                                                        weight = :weight,
                                                        copper_content = :copper_content,
                                                        copper_alloy_content = :copper_alloy_content,                                                        
                                                        type_transformer = :type_transformer                                                        
                                 WHERE id = :id''')

                query.bindValue(":id", id_transformer);
                
                '''
:isolationlevel, :climat, :weight, :copper_content, copper_alloy_content, :type_transformer)            
            '''
                
            query.bindValue(":fullname", noneValue(self.ui.lineEdit.text()))
            query.bindValue(":shortname", noneValue(self.ui.lineEdit.text()))            
            query.bindValue(":type", noneValue(self.ui.lineEdit_12.text()))
            query.bindValue(":thermal_current", thermal_current)
            query.bindValue(":dynamic_current", dynamic_current)
            query.bindValue(":voltage", voltage)
            query.bindValue(":maxopervoltage", maxopervoltage)
            query.bindValue(":time_thermal_current", time_thermal_current)
            query.bindValue(":isolationlevel", noneValue(self.ui.lineEdit_7.text()))            
            query.bindValue(":climat", noneValue(self.ui.lineEdit_8.text()))
            query.bindValue(":weight", weight)            
            query.bindValue(":copper_content", copper_content)
            query.bindValue(":copper_alloy_content", copper_alloy_content)            
            query.bindValue(":type_transformer", self.type_transformer)
            
                        
            
            if not query.exec_():
                id_trans_copy = -1
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True
        
                """       
                global id_trans_copy
                if self.tag == 1 and id_trans_copy != -1:        
                    r = QMessageBox.warning(self, u"Предупреждение", u"Копировать обмотки?", QMessageBox.Yes, QMessageBox.No)            
                    if r == QMessageBox.Yes:
                        query = QSqlQuery(db1)
                        query.prepare('''INSERT INTO coil (transformer, coiltype, coilnumber, tap, classaccuracy, primarycurrent,
 secondcurrent, secondload, magneticvoltage, magneticcurrent, resistance, rating, ampereturn)
 SELECT transformer, coiltype, coilnumber, tap, classaccuracy, primarycurrent,
 secondcurrent, secondload, magneticvoltage, magneticcurrent, resistance, rating, ampereturn
 FROM coil WHERE transformer = :transformer''')
                        query.bindValue(":transformer", id_trans_copy);
                        id_trans_copy = -1
                
                        if not query.exec_():
                            QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                   """    
                       
                       
                self.close()






        def pushButton3_Click(self):
            global mnu_2
            mnu_2.exec_(QPoint(self.ui.lineEdit_12.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_12.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_12.geometry().height())) 

                            
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
                query.bindValue(":transformer", id_transformer);
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
        
        wind = ClsTrans(env, 0)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())


