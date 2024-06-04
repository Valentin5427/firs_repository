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
from electrolab.gui.reporting import FRPrintForm
from StandMsr import StandMsr

import ui.ico_64_rc

import datetime

import ReportsExcel

from datetime import date

test_map = -1
#id_coil = -1

MAP = None
ID_STAND_MSR = None
ID_ZAV_MSR = None

# self.model.setSortRole(QtCore.Qt.UserRole)

#QtGui.QTableView.horizontalHeader().

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 100
withCol2 = 100
withCol3 = 100
withCol4 = 100
withCol5 = 100                        
withCol6 = 60                       
withCol7 = 50                       
withCol8 = 100                       
withCol9 = 150                       
withCol10 = 25                       

withCol_1 = 40
withCol_2 = 150
withCol_3 = 50
withCol_4 = 100
withCol_5 = 35

withCol_11 = 100
withCol_12 = 40

isSave = False
width1 = 0

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
        global VSB1, VSB2, VSB3, VSB4, width1
        
        '''
        if obj.objectName() == 'win':
            width1 = obj.width()

        print 'width = ', width1, self.wid
        '''
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7 + withCol8 + withCol9 + withCol10))
            obj.setColumnWidth(7, koef * withCol1)
            obj.setColumnWidth(8, koef * withCol2)
            obj.setColumnWidth(9, koef * withCol3)
            obj.setColumnWidth(10, koef * withCol4)
            obj.setColumnWidth(11, koef * withCol5)
            obj.setColumnWidth(12, koef * withCol6)
            obj.setColumnWidth(13, koef * withCol7)
            obj.setColumnWidth(14, koef * withCol8)
            obj.setColumnWidth(15, koef * withCol9)
            obj.setColumnWidth(16, koef * withCol10)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):            
#            QtGui.QTableView.setMinimumWidth(1000)
 #           QtGui.QTableView.set
#            self.ui.tableView_2.setMinimumWidth(1000)
    #        obj.setMinimumWidth(1000)
#            obj.setWidth(1000)
#            print 'self.widthArea(obj)', self.widthArea(obj)
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4 + withCol_5))
            obj.setColumnWidth(3, koef * withCol_1)
            obj.setColumnWidth(4, koef * withCol_2)
            obj.setColumnWidth(5, koef * withCol_3)
            obj.setColumnWidth(6, koef * withCol_4)
            obj.setColumnWidth(7, koef * withCol_5)
            VSB2 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv3' and (e.type() <> QtCore.QEvent.Resize or VSB3 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_11 + withCol_12))
            obj.setColumnWidth(2, koef * withCol_11)
            obj.setColumnWidth(3, koef * withCol_12)
            VSB3 = obj.verticalScrollBar().isVisible()




        return False


class JournalTest(QtGui.QDialog, UILoader):
    def __init__(self, _env, *args):
        QtGui.QDialog.__init__(self, *args)        
                
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"JournalTest.ui")        
        
        
      #  self.resize(1000,600)
        self.ui.splitter.setStretchFactor(0,1)
        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_4.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_5.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_6.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_9.setIcon(QIcon(u':/ico/ico/print_64.png'))
        self.ui.pushButton_7.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_8.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_11.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        
#        self.ui.pushButton_9.setIcon(QIcon(u':/ico/ico/filter.png'))
#        self.ui.pushButton_9.setIcon(QIcon(u':/ico/ico/filt.png'))

#        QtGui.QDialog.resi
#        self.resizeEvent.connect(self.pushButton_2_Click)
#        self.resize.connect(self.pushButton_2_Click)
#        self.ui.Dialog.connect(self.pushButton_2_Click)

#        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
#        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
        self.ui.pushButton_9.clicked.connect(self.pushButton_9_Click)
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_Click)
        
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
        self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)
        self.ui.pushButton_11.clicked.connect(self.pushButton_11_Click)
                
        self.ui.pushButton_12.clicked.connect(self.pushButton_12_Click)


        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        
        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()        
        self.connect(self.selModel_2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_2)


        self.ui.tableView_3.setModel(model_3)        
        self.selModel_3 = self.ui.tableView_3.selectionModel()        
        self.connect(self.selModel_3, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_3)


        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))
        self.ui.tableView_3.installEventFilter(MyFilter(self.ui.tableView_3))

        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setObjectName('tv2')
        self.ui.tableView_3.setObjectName('tv3')
        self.setObjectName('win')
        
        self.IS_SELECT = False    

        self.ui.dateEdit.setDate(datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day))        
        self.ui.dateEdit_2.setDate(datetime.date.today())        
            
        self.selTestMap()        
            
        # Организация меню печати отчетов
        fnt = QtGui.QFont()
        fnt.setPointSize(12)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Отчет поверителя', self))
        self.mnu.addAction(QtGui.QAction(u'Протокол поверки', self))
        self.mnu.addAction(QtGui.QAction(u'Этикетки', self))
        self.mnu.setFont(fnt)        
        self.connect(self.mnu.actions()[0], QtCore.SIGNAL('triggered()'), self.report1)
        self.connect(self.mnu.actions()[1], QtCore.SIGNAL('triggered()'), self.report2)
        self.connect(self.mnu.actions()[2], QtCore.SIGNAL('triggered()'), self.report3)
      

    def report1(self):
        row = self.selModel.currentIndex().row()
        test_mapID = float(model.record(row).field('id').value().toString())
        rpt = FRPrintForm(u'verifier_protocol.fr3', {u'test_map':test_mapID}, self.env)
        rpt.preview()

    def report2(self):
        row = self.selModel.currentIndex().row()
        row_2 = self.selModel_2.currentIndex().row()
        test_mapID = float(model.record(row).field('id').value().toString())
        
        print 'model_2.record(row).field(id).value().toString() = ', model_2.record(row).field('id').value().toString()
        
        itemID = float(model_2.record(row_2).field('id').value().toString())
        
#        ReportsExcel.verification_protocol(self.env.db, _iMapID, None, False)
###        ReportsExcel.verification_protocol(db1, test_mapID, itemID, True)
        ReportsExcel.verification_protocol(db1, test_mapID, None, True)
        return
        
        # Старый отчет
        rpt = FRPrintForm(u'tester_protocol.fr3', {u'test_map':test_mapID}, self.env)
        rpt.preview()

    def report3(self):
        row = self.selModel.currentIndex().row()
        test_mapID = float(model.record(row).field('id').value().toString())
        rpt = FRPrintForm(u'ReportTickets.fr3', {u'test_map':test_mapID}, self.env)
        rpt.preview()

      
    def pushButton_9_Click(self):
        self.mnu.exec_(QPoint(self.ui.pushButton_9.mapToGlobal(QPoint(0,0)).x() + self.ui.pushButton_9.width(), self.ui.pushButton_9.mapToGlobal(QPoint(0,0)).y()))


# Редактирование трансформатора (начало кода)        

    '''              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editTrans(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление новой тележки')
        row = self.selModel.currentIndex().row()
        self.wind.ui.lineEdit.setText(model.record(row).field('type').value().toString())
        isSave = False        
        self.wind.exec_()
        if isSave:
            print 'selTrans1'
            self.selTestMap()
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM transformer");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            
       '''     



                
    def pushButton_2_Click(self):
                    
        global isSave        
        global id_map
        self.wind = self.editMap(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущегй записи')
        row = self.selModel.currentIndex().row()
               
        id_map = int(model.record(row).field('id').value().toString())
                
        id_operator = int(model.record(row).field('operator').value().toString())   
        self.wind.ui.lineEdit.tag = int(model.record(row).field('operator').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('fio_operator').value().toString())
        
        id_supervisor = int(model.record(row).field('supervisor').value().toString())   
        self.wind.ui.lineEdit_2.tag = int(model.record(row).field('supervisor').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('fio_supervisor').value().toString())
        
        id_assistant = int(model.record(row).field('assistant').value().toString())   
        self.wind.ui.lineEdit_3.tag = int(model.record(row).field('assistant').value().toString())        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('fio_assistant').value().toString())
        
        id_climat = int(model.record(row).field('climat').value().toString())   
        self.wind.ui.dateTimeEdit.tag = int(model.record(row).field('climat').value().toString())                     
        self.wind.ui.dateTimeEdit.setDateTime(model.record(row).field('lastupdate').value().toDateTime())                     

        self.wind.ui.checkBox.setChecked(bool(int(model.record(row).field('accept').value().toString())))        
        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selTestMap()
            self.ui.tableView.selectRow(row)                                            


    def pushButton_3_Click(self):
        print 'QSqlQueryModel.rowCount(parent=QModelIndex() = ', model_2.rowCount()
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале обмотки!', QMessageBox.Ok)
                return
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM test_map WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selTestMap()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                                        
    def pushButton_5_Click(self):
        global isSave        
        global id_item
        self.wind = self.editItem(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Трансформатор')
        row = self.selModel_2.currentIndex().row()

        id_item = int(model_2.record(row).field('id').value().toString())

        test_type = int(model.record(row).field('test_type').value().toString())
                
        # Заполнение conboBox списком несоответствий согласно type_test        
        query = QSqlQuery(db1)
                
        SQL = """select t2.defect, t1.fullname 
from defect t1, defect_test_type t2
where t1.id = t2.defect
and t2.test_type = :test_type
order by t1.fullname, t2.defect
"""                
        query.prepare(SQL)                
        query.bindValue(":test_type", test_type)
        if not query.exec_():
            print unicode(query.lastError().text())        
        model_.setQuery(query)
        
        curIndex = -1
        self.wind.ui.comboBox.clear()        
        for i in range(model_.rowCount()):
            self.wind.ui.comboBox.addItem(model_.record(i).field(1).value().toString(), model_.record(i).field(0).value().toString())
            if model_2.record(row).field('defect').value().toString() != '':
                if int(model_.record(i).field('defect').value().toString()) == int(model_2.record(row).field('defect').value().toString()):
                    curIndex = i
                 
        self.wind.ui.comboBox.setCurrentIndex(curIndex)                    
        self.wind.ui.checkBox.setChecked(bool(int(model_2.record(row).field('istest').value().toString())))        

        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selItem()
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
            self.selItem()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_2.selectRow(row)                                    

    def pushButton_10_Click(self):
        #model.record(row).field('isMsr') = 'S'
       # PyQt4.QtSql.QSqlField
        '''
        from PyQt4 import QtSql
        from PyQt4.QtSql import QSqlField
        QSqlField.setValue()
        QSqlField.setva
        self.ui.tableView.setItem(1, 5, 'S')
        return
        self.table_widget.setItem(row, 0, QTableWidgetItem(str(id_)))
#        print type(model.record(1).field('isMsr')).setValue()
        model.record(1).field('isMsr').setValue('S')
        #print model.record(1).field('isMsr').setValue('S')
        
        QtGui.QTableView.
        return
                
        #QSqlQueryModel.
'''
                
        self.selTestMap()        



    def pushButton_7_Click(self):
        global isSave        
        global MAP
        self.wind = self.editMapMsr(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового средства измерения')
        row = self.selModel.currentIndex().row()
        MAP = int(model.record(row).field('id').value().toString())
        #print 'STANDSTANDSTANDSTANDSTAND = ', MAP
        isSave = False        
        self.wind.exec_()
        if isSave:
            
            self.selTestMap()   #?????
            self.ui.tableView.selectRow(row)                                            
                        
         #???????   self.selMapMsr()
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM map_msr");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView_3, model_3)            



        '''
        row = self.selModel.currentIndex().row()                       
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selTestMap()
            self.ui.tableView.selectRow(row)                                            
'''










    def pushButton_8_Click(self):
        global isSave        
        global MAP
        global ID_STAND_MSR
        global ID_ZAV_MSR
        self.wind = self.editMapMsr(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущей записи')
        row = self.selModel.currentIndex().row()
        MAP = int(model.record(row).field('id').value().toString())        
        row = self.selModel_3.currentIndex().row()
               
#        self.ID_STAND_MSR = int(model.record(row).field('id').value().toString())        
        ID_STAND_MSR = int(model_3.record(row).field('id').value().toString())        
        ID_ZAV_MSR = int(model_3.record(row).field('zav_msr').value().toString())   
#        self.wind.ui.lineEdit.tag = int(model.record(row).field('operator').value().toString())        
        self.wind.ui.lineEdit.setText(model_3.record(row).field('name_msr').value().toString())        
        self.wind.ui.lineEdit_2.setText(model_3.record(row).field('zav_num').value().toString())        
                        
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selMapMsr()
            self.ui.tableView_3.selectRow(row)                                            


    def pushButton_11_Click(self):
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM map_msr WHERE id = :ID")
            row = self.selModel_3.currentIndex().row()                
            query.bindValue(":id", model_3.record(row).field('id').value().toString());
            query.exec_()
            
            
            row1 = self.selModel.currentIndex().row()
            self.selTestMap()   #?????
            self.ui.tableView.selectRow(row1)                                            
            
            
            
            
        #?????????    self.selMapMsr()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_3.selectRow(row)                                    





    def pushButton_12_Click(self):
#        QtGui.QRadioButton.isChecked()
#        wind = StandMsr(self.env, self.adStandInfo.ID, self.adStandInfo.FullName)
        row = self.selModel.currentIndex().row()
        if self.ui.radioButton.isChecked():
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете импортировать\nсредства измерения по текущей позиции?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return            
#            row = self.selModel.currentIndex().row()
            stand = int(model.record(row).field('stand').value().toString())
            map = int(model.record(row).field('id').value().toString())
            isMsr = (model.record(row).field('isMsr').value().toString() != '')
            wind = StandMsr(self.env, stand, '')
            wind.generate_map_msr(map, self.ui.checkBox.isChecked(), isMsr)
        else:
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете импортировать\nсредства измерения по тележкам в кол-ве " + str(model.rowCount()) + u" шт. ?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return            
            for i in range(model.rowCount()):
                stand = int(model.record(i).field('stand').value().toString())
                map = int(model.record(i).field('id').value().toString())
                isMsr = (model.record(i).field('isMsr').value().toString() != '')
                wind = StandMsr(self.env, stand, '')
                wind.generate_map_msr(map, self.ui.checkBox.isChecked(), isMsr)

        self.selTestMap()
        self.ui.tableView.selectRow(row)                                            


            
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
            

    def selTestMap(self):
        v = unicode(self.ui.lineEdit.text()).upper()
        
        query = QSqlQuery(db1)
                                
        SQL = """select t1.id, t1.operator, t1.supervisor, t1.climat, t1.assistant, t6.test_type, 
                        case when t1.accepted then 1 else 0 end as accept,
                        t2.fio as fio_operator, t3.fio as fio_supervisor, t4.lastupdate, 
                        t1.createdatetime, t1.acceptdatetime, t1.accepted, 
                        t1.stand, t5.fio as fio_assistant, t7.name,
                        case when t8.test_map is null then null else 'v' end as isMsr
        from test_map as t1 left outer join operator as t2 on (t1.operator = t2.id)
                            left outer join operator as t3 on (t1.supervisor = t3.id)
                            left outer join climat as t4 on (t1.climat = t4.id)
                            left outer join operator as t5 on (t1.assistant = t5.id)
                            left outer join (select distinct test_map from map_msr) as t8 on (t1.id = t8.test_map),
                            stand t6, test_type t7
        where t1.stand = t6.id
        and t6.test_type = t7.id
        and t1.createdatetime between to_date('""" + self.ui.dateEdit.text() + """','dd.mm.yyyy') and to_date('""" + self.ui.dateEdit_2.text() + """','dd.mm.yyyy') + 1
        """
        
        if self.ui.lineEdit.text() != "":
            SQL += """            
        and t1.id in (select test_map from item t1, serial_number t2 where t1.serial_number = t2.id and serialnumber = """ + self.ui.lineEdit.text() + """)
        """
        
        SQL += """order by t1.id desc
        """
        print SQL 
                      
        query.prepare(SQL)
        
        if not query.exec_():
            print unicode(query.lastError().text())
            QMessageBox.warning(self, u"Предупреждение",  unicode(query.lastError().text()), QMessageBox.Ok)
                   
        model.setQuery(query)
        
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Испытатель")
        model.setHeaderData(8, QtCore.Qt.Horizontal, u"Поверитель")
        model.setHeaderData(9, QtCore.Qt.Horizontal, u"Климат(время)")
        model.setHeaderData(10, QtCore.Qt.Horizontal, u"Дата\nсоздания")
        model.setHeaderData(11, QtCore.Qt.Horizontal, u"Дата\nподтверждения")
        model.setHeaderData(12, QtCore.Qt.Horizontal, u"Принято")
        model.setHeaderData(13, QtCore.Qt.Horizontal, u"Стенд")
        model.setHeaderData(14, QtCore.Qt.Horizontal, u"Ассистент")
        model.setHeaderData(15, QtCore.Qt.Horizontal, u"Вид испытания")
        model.setHeaderData(16, QtCore.Qt.Horizontal, u"СИ")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(7,  withCol1)
        self.ui.tableView.setColumnWidth(8,  withCol2)
        self.ui.tableView.setColumnWidth(9,  withCol3)
        self.ui.tableView.setColumnWidth(10,  withCol4)
        self.ui.tableView.setColumnWidth(11,  withCol5)
        self.ui.tableView.setColumnWidth(12,  withCol6)
        self.ui.tableView.setColumnWidth(13,  withCol7)
        self.ui.tableView.setColumnWidth(14,  withCol8)
        self.ui.tableView.setColumnWidth(15,  withCol9)
        self.ui.tableView.setColumnWidth(16,  withCol10)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
        self.ui.tableView.setColumnHidden(2, True)
        self.ui.tableView.setColumnHidden(3, True)
        self.ui.tableView.setColumnHidden(4, True)
        self.ui.tableView.setColumnHidden(5, True)
        self.ui.tableView.setColumnHidden(6, True)
        self.ui.tableView.selectRow(0)
         
        ''' не удалять        
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        self.ui.pushButton_4.setEnabled(enab)
        '''


    def selItem(self):
        row = self.selModel.currentIndex().row()
#        print 'row = row = row = ', row
        global test_map
        if row < 0:
            test_map = -1
            self.CODE_TRANS = -1
            self.NAME_TRANS = ''
        else:    
            test_map = int(model.record(row).field('id').value().toString())
            self.CODE_TRANS = int(model.record(row).field('id').value().toString())
            self.NAME_TRANS = unicode(model.record(row).field('fullname').value().toString())
            
        query = QSqlQuery(db1)
        
        SQL = """select t1.id, t1.defect, case when t1.istested then 1 else 0 end as istest,
serialnumber, t3.fullname as name_trans, createdatetime, t4.fullname as name_defect, t1.istested
from item t1 left outer join defect as t4 on (t1.defect = t4.id), serial_number t2, transformer t3
where t1.serial_number = t2.id
and t2.transformer = t3.id
and t1.test_map = :test_map
"""        
        if self.ui.lineEdit.text() != "":
            SQL += """            
and serialnumber = :serialnumber
"""
            SQL += """            
order by serialnumber
"""

        print test_map, self.ui.lineEdit.text()
        print 'SQL SQL SQL SQL SQL SQL SQL SQL SQL SQL SQL = '
        print SQL

        query.prepare(SQL)
                
        query.bindValue(":test_map", test_map)
        if self.ui.lineEdit.text() != "":
            query.bindValue(":serialnumber", self.ui.lineEdit.text())
                
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_2.setQuery(query)

        model_2.setHeaderData(3,  QtCore.Qt.Horizontal, u"Серийный\nномер")
        model_2.setHeaderData(4,  QtCore.Qt.Horizontal, u"Наименование трансформатора")
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Карта\nиспытаний")
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Несоответствие")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Испы-\nтано")
                    
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(1, True)
        self.ui.tableView_2.setColumnHidden(2, True)
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(3,  withCol_1)
        self.ui.tableView_2.setColumnWidth(4,  withCol_2)
        self.ui.tableView_2.setColumnWidth(5,  withCol_3)
        self.ui.tableView_2.setColumnWidth(6,  withCol_4)
        self.ui.tableView_2.setColumnWidth(7,  withCol_5)
        
        ''' пока не удалять
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)
        '''
        
        
    def selMapMsr(self):
       # QMessageBox.warning(self, u"Ошибка", "FFFFFFFFFFFFFFFFFFFFFF", QMessageBox.Ok)

        row = self.selModel.currentIndex().row()
#        print 'row = row = row = ', row
        global test_map
        if row < 0:
            test_map = -1
#            self.CODE_TRANS = -1
#            self.NAME_TRANS = ''
        else:    
            test_map = int(model.record(row).field('id').value().toString())
#            self.CODE_TRANS = int(model.record(row).field('id').value().toString())
#            self.NAME_TRANS = unicode(model.record(row).field('fullname').value().toString())
        
        query = QSqlQuery(db1)
                                
        SQL = """select t1.id, t1.zav_msr, name_msr, zav_num
from map_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and t1.test_map = :test_map
order by name_msr
        """
                
        query.prepare(SQL)
        query.bindValue(":test_map", test_map);            
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            return
            
        model_3.setQuery(query)
        
        self.ui.pushButton_8.setEnabled(model_3.rowCount() > 0)           #   model_.rowCount()
        self.ui.pushButton_11.setEnabled(model_3.rowCount() > 0)           #   model_.rowCount()
        
#        QtGui.QPushButton.setEnabled()


        model_3.setHeaderData(2, QtCore.Qt.Horizontal, u"Наименование\nсредства измерения")
        model_3.setHeaderData(3, QtCore.Qt.Horizontal, u"Заводской\nномер")
        #model.setHeaderData(4, QtCore.Qt.Horizontal, u"Относительная\nвлажность, %")
        #model.setHeaderData(5, QtCore.Qt.Horizontal, u"Атмосферное\nдавление, кПа")
        #model.setHeaderData(6, QtCore.Qt.Horizontal, u"Время")
    #model.setHeaderData(7, QtCore.Qt.Horizontal, u"Помещение")
            
        self.ui.tableView_3.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.ui.tableView_3.setColumnWidth(2,  withCol_11)
        self.ui.tableView_3.setColumnWidth(3,  withCol_12)
        #self.ui.tableView.setColumnWidth(4,  withCol3)
        #self.ui.tableView.setColumnWidth(5,  withCol4)
        #self.ui.tableView.setColumnWidth(6,  withCol5)
        #self.ui.tableView.setColumnWidth(7,  withCol6)
        
        self.ui.tableView_3.setColumnHidden(0, True)
        self.ui.tableView_3.setColumnHidden(1, True)
        #self.ui.tableView.setColumnHidden(1, True)
        self.ui.tableView_3.selectRow(0)
        
        '''        
        enab = self.selModel_3.currentIndex().row() >= 0        
        self.ui.pushButton_8.setEnabled(enab)
        self.ui.pushButton_11.setEnabled(enab)
        '''
        
        
        
        '''
        
        row = self.selModel.currentIndex().row()
        print 'row = row = row =  row = ', row
        global test_map
        if row < 0:
            test_map = -1
            self.CODE_TRANS = -1
            self.NAME_TRANS = ''
        else:    
            test_map = int(model.record(row).field('id').value().toString())
            self.CODE_TRANS = int(model.record(row).field('id').value().toString())
            self.NAME_TRANS = unicode(model.record(row).field('fullname').value().toString())
            
        query = QSqlQuery(db1)
        
        SQL = """select t1.id, t1.defect, case when t1.istested then 1 else 0 end as istest,
serialnumber, t3.fullname as name_trans, createdatetime, t4.fullname as name_defect, t1.istested
from item t1 left outer join defect as t4 on (t1.defect = t4.id), serial_number t2, transformer t3
where t1.serial_number = t2.id
and t2.transformer = t3.id
and t1.test_map = :test_map
"""        
        if self.ui.lineEdit.text() != "":
            SQL += """            
and serialnumber = :serialnumber
"""
            SQL += """            
order by serialnumber
"""

        query.prepare(SQL)
                
        query.bindValue(":test_map", test_map)
        if self.ui.lineEdit.text() != "":
            query.bindValue(":serialnumber", self.ui.lineEdit.text())
                
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_2.setQuery(query)

        model_2.setHeaderData(3,  QtCore.Qt.Horizontal, u"Серийный №")
        model_2.setHeaderData(4,  QtCore.Qt.Horizontal, u"Наименование трансформатора")
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Карта испытаний")
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Несоответствие")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Испытано")
                    
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(1, True)
        self.ui.tableView_2.setColumnHidden(2, True)
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(3,  withCol_1)
        self.ui.tableView_2.setColumnWidth(4,  withCol_2)
        self.ui.tableView_2.setColumnWidth(5,  withCol_3)
        self.ui.tableView_2.setColumnWidth(6,  withCol_4)
        self.ui.tableView_2.setColumnWidth(7,  withCol_5)
        '''
        ''' пока не удалять
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)
        '''
        
        
        
        
    def selectionChanged(self):
        self.selItem()
        self.selMapMsr()

    def selectionChanged_2(self):
#        global id_coil
        row = self.selModel_2.currentIndex().row()
#        id_coil = model_2.record(row).field('id').value().toString()

    def selectionChanged_3(self):
        pass
#        global id_coil
        #row = self.selModel_2.currentIndex().row()

# Редактирование тележек (начало кода)        
                        
    class editMap(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editMap.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
            self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
            self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
            self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
            self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
            self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)
#            self.ui.pushButton_9.clicked.connect(self.pushButton_9_Click)
        
        
        def pushButton1_Click(self):
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи оператора', QMessageBox.Ok)
                return
                                    
#            global id_coil
            global isSave        
            query = QSqlQuery(db1)

            '''
            SQL = select t1.id, t1.operator, t1.supervisor, t1.climat, t1.assistant, 
                        t2.fio fio_operator, t3.fio fio_supervisor, t4.lastupdate, 
                        t1.createdatetime, t1.acceptdatetime, t1.accepted, t1.stand,
                        t5.fio fio_assistant, t7.name
'''

            SQL ='''UPDATE test_map SET operator = :operator,
                                        supervisor = :supervisor,
                                        assistant = :assistant,
                                        climat = :climat,
                                        accepted = :accepted
                                 WHERE id = :id'''
                
            query.prepare(SQL)
#            print SQL

#            QMessageBox.warning(self, u"Ошибка",  str(self.ui.lineEdit_2.tag), QMessageBox.Ok)
#            return
            
            query.bindValue(":id", id_map);                                
            query.bindValue(":operator", self.ui.lineEdit.tag)
#            query.bindValue(":supervisor", self.ui.lineEdit_2.tag)
#            query.bindValue(":assistant", self.ui.lineEdit_3.tag)
#            query.bindValue(":climat", self.ui.dateTimeEdit.tag)
            if self.ui.lineEdit_2.text().trimmed() == '':
                query.bindValue(":supervisor", None)
            else:    
                query.bindValue(":supervisor", self.ui.lineEdit_2.tag)
                
            if self.ui.lineEdit_3.text().trimmed() == '':
                query.bindValue(":assistant", None)
            else:    
                query.bindValue(":assistant", self.ui.lineEdit_3.tag)
                
            if self.ui.dateTimeEdit.tag < 1:
                query.bindValue(":climat", None)
            else:    
                query.bindValue(":climat", self.ui.dateTimeEdit.tag)
                
#            query.bindValue(":climat", None)
            query.bindValue(":accepted", self.ui.checkBox.isChecked())
            
            '''
            query.bindValue(":temperature", self.ui.doubleSpinBox.value())                                
            query.bindValue(":humidity", self.ui.doubleSpinBox_2.value())                                
            query.bindValue(":pressure", self.ui.doubleSpinBox_3.value())
            query.bindValue(":lastupdate", self.ui.dateTimeEdit.text())
            query.bindValue(":room", self.ui.spinBox.text())
                                
            query.bindValue(":type", noneValue(self.ui.lineEdit.text()))
            query.bindValue(":fullname", noneValue(self.ui.lineEdit_2.text()))
            query.bindValue(":shortname", noneValue(self.ui.lineEdit_3.text()))
            query.bindValue(":standart", noneValue(self.ui.lineEdit_4.text()))
            
            query.bindValue(":voltage", voltage)
            query.bindValue(":maxopervoltage", maxopervoltage)
            query.bindValue(":frequency", frequency)
            query.bindValue(":quantsecondcoil", quantsecondcoil)
            
            query.bindValue(":isolationlevel", noneValue(self.ui.lineEdit_5.text()))            
            query.bindValue(":climat", noneValue(self.ui.lineEdit_6.text()))
            query.bindValue(":weight", weight)
                        '''
            print 777
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
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
            wind.exec_()        
            if wind.IS_SELECT:
                self.ui.lineEdit.setText(wind.FIO)
                self.ui.lineEdit.tag = wind.OPERATOR 
                        
        # Вызов справочника операторов
        def pushButton_4_Click(self):
            from sprTester import sprTester
#            wind = sprTester(self.env, 1)
            wind = sprTester(self.env)
            wind.show()
            
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()        
            if wind.IS_SELECT:
                self.ui.lineEdit_2.setText(wind.FIO)
                self.ui.lineEdit_2.tag = wind.OPERATOR 
                        
        # Вызов справочника операторов
        def pushButton_5_Click(self):
            from sprTester import sprTester
#            wind = sprTester(self.env, 1)
            wind = sprTester(self.env)
            wind.show()
            
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()        
            if wind.IS_SELECT:
                self.ui.lineEdit_3.setText(wind.FIO)
                self.ui.lineEdit_3.tag = wind.OPERATOR 
                        
        # Вызов справочника климатических условий
        def pushButton_6_Click(self):
            print 111
            from sprClimat import sprClimat
#            wind = sprTester(self.env, 1)
            wind = sprClimat(self.env)
            wind.show()
            
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()        
            if wind.IS_SELECT:
                self.ui.dateTimeEdit.setDateTime(wind.LASTUPDATE)                
#                self.wind.ui.dateTimeEdit.setDateTime(model.record(row).field('lastupdate').value().toDateTime())                                     
                self.ui.dateTimeEdit.tag = wind.CLIMAT
                                    
#                self.ui.lineEdit.setText(wind.FIO)
#                self.ui.lineEdit.tag = wind.OPERATOR 




        def pushButton_7_Click(self):
            self.ui.lineEdit_2.setText("")

        def pushButton_8_Click(self):
            self.ui.lineEdit_3.setText("")
        
        '''                    
        def pushButton_9_Click(self):
            return
        
            print 1
            self.ui.dateTimeEdit.tag = -1
            print 2
#            self.ui.dateTimeEdit.text = ""
            self.ui.dateTimeEdit.displayFormat = ""
            print 3
           ''' 

#dd.MM.yyyy H:mm:ss            
#            QtGui.QDateTimeEdit.te
                
# Редактирование тележек (конец кода)        


# Редактирование содержимого тележек (начало кода)        
                        
    class editItem(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editItem.ui")        
                        
 #           self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
 #           self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)
        
        
        def pushButton1_Click(self):            
#            global id_coil
            global isSave
            
            defect = None         
            for i in range(model_.rowCount()):
                if self.ui.comboBox.currentIndex() == i:
                    defect = int(model_.record(i).field(0).value().toString())

            query = QSqlQuery(db1)
            query.prepare('''UPDATE item SET defect = :defect, 
                                             istested = :istested
                                             WHERE id = :id''')

            query.bindValue(":defect", defect)                
            query.bindValue(":istested", self.ui.checkBox.isChecked())
            query.bindValue(":id", id_item);
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

        def pushButton3_Click(self):
            self.ui.comboBox.setCurrentIndex(-1)    
            
# Редактирование трансформаторов (конец кода)        

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




# Редактирование map_msr (начало кода)                                
    class editMapMsr(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editStandMsr.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
            self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)

        
        def pushButton_Click(self):
            global MAP
            global ID_STAND_MSR
#            row = self.selModel_3.currentIndex().row()
#            test_mapID = float(model.record(row).field('id').value().toString())
    #        row = self.selModel.currentIndex().row()
            
#            global id_stand_msr
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи средство измерения', QMessageBox.Ok)
                self.ui.pushButton_3.setFocus()
                return
                
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO map_msr (test_map, zav_msr) values (:test_map, :zav_msr)'''            
                                
                query.prepare(SQL)
            else:
                SQL ='''UPDATE map_msr SET test_map = :test_map,
zav_msr = :zav_msr
WHERE id = :id'''
                                                
                query.prepare(SQL)
#                query.bindValue(":id", id_stand_msr);
                query.bindValue(":id", ID_STAND_MSR);
                                
#            query.bindValue(":stand", self.ui.lineEdit.tag)
#            query.bindValue(":zav_msr", self.ui.doubleSpinBox.value())                                
#            print 'STANDSTAND                  STANDSTANDSTAND = ', MAP
            query.bindValue(":test_map", MAP)
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
        
        wind = JournalTest(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
