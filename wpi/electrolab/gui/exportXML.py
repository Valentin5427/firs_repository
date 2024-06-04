# -*- coding: UTF-8 -*-
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont, QSortFilterProxyModel
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt, QPoint

import socket
from fileinput import close
import PyQt4
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.gui.reporting import FRPrintForm
from StandMsr import StandMsr

import ui.ico_64_rc

import datetime
import json

from datetime import date

import xml.etree.ElementTree as ET


test_map = -1

MAP = None
ID_STAND_MSR = None
ID_ZAV_MSR = None

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
model_4 = QSqlQueryModel()

proxyModel = QSortFilterProxyModel(model); # create proxy

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit

withCol1 = 100
withCol2 = 100
withCol3 = 30
withCol4 = 30
withCol5 = 30                        
withCol6 = 60                       
withCol7 = 30                       
withCol8 = 30                       
withCol9 = 150                       
withCol10 = 50                       

withCol_1 = 50
withCol_2 = 140
withCol_3 = 50
withCol_4 = 50
withCol_5 = 30
withCol_6 = 45
withCol_7 = 35
withCol_8 = 50
withCol_9 = 50
withCol_10 = 50

withCol_11 = 100
withCol_12 = 60
withCol_13 = 80
withCol_14 = 80
withCol_15 = 100

isSave = False
width1 = 0

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
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7 + withCol8 + withCol9 + withCol10))
            obj.setColumnWidth(5, koef * withCol1)
            obj.setColumnWidth(6, koef * withCol2)
            obj.setColumnWidth(7, koef * withCol3)
            obj.setColumnWidth(8, koef * withCol4)
            obj.setColumnWidth(9, koef * withCol5)
            obj.setColumnWidth(10, koef * withCol6)
            obj.setColumnWidth(11, koef * withCol7)
            obj.setColumnWidth(12, koef * withCol8)
            obj.setColumnWidth(13, koef * withCol9)
            obj.setColumnWidth(14, koef * withCol10)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):            
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4 + withCol_5 + withCol_6 + withCol_7 + withCol_8 + withCol_9 + withCol_10))
            obj.setColumnWidth(3, koef * withCol_1)
            obj.setColumnWidth(4, koef * withCol_2)
            obj.setColumnWidth(5, koef * withCol_3)
            obj.setColumnWidth(6, koef * withCol_4)
            obj.setColumnWidth(7, koef * withCol_5)
            obj.setColumnWidth(8, koef * withCol_6)
            obj.setColumnWidth(9, koef * withCol_7)
            obj.setColumnWidth(10, koef * withCol_8)
            obj.setColumnWidth(11, koef * withCol_9)
            obj.setColumnWidth(13, koef * withCol_10)
            VSB2 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv3' and (e.type() <> QtCore.QEvent.Resize or VSB3 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_11 + withCol_12 + withCol_13 + withCol_14 + withCol_15))
            obj.setColumnWidth(3, koef * withCol_11)
            obj.setColumnWidth(4, koef * withCol_12)
            obj.setColumnWidth(5, koef * withCol_13)
            obj.setColumnWidth(6, koef * withCol_14)
            obj.setColumnWidth(7, koef * withCol_15)
            VSB3 = obj.verticalScrollBar().isVisible()

        return False


#class sprTypeTransformer(QWidget, UILoader):    
class JournalTest(QWidget, UILoader):
#class JournalTest(QtGui.QDialog, UILoader):
    def __init__(self, _env, *args):
        QtGui.QDialog.__init__(self, *args)        
                
        global db1
        db1 = _env.db
        self.env = _env
                
        super(QWidget, self).__init__()

        if not self.TestBase():
            return

        self.query =   QSqlQuery(db1)
        self.query_2 = QSqlQuery(db1)
        self.query_3 = QSqlQuery(db1)
                
        self.setUI(_env.config, u"exportXML.ui")                
        
        self.setWindowTitle(u'Отчет по экспорту результатов испытаний в XML - файл')
#        self.ui.groupBox_2.setVisible(False)
#        self.ui.groupBox_3.setVisible(False)
                
        self.ui.splitter.setStretchFactor(0,1)
        
        self.ui.pushButton.clicked.connect(self.pushButton_Click)        
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_Click)        
        self.ui.pushButton_12.clicked.connect(self.pushButton_12_Click)        
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)        

#        self.ui.tableView.setModel(model)        
#        self.selModel = self.ui.tableView.selectionModel()        
#        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        
        
        
        proxyModel.setSourceModel(model)   
        self.ui.tableView.setModel(proxyModel)
        self.selModel = self.ui.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        
        #self.connect(proxyModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        
        
        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()        
        self.connect(self.selModel_2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_2)

        self.ui.tableView_3.setModel(model_3)        
        self.selModel_3 = self.ui.tableView_3.selectionModel()
        self.connect(self.selModel_3, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_3)
        
        self.exportXML = {"pathExport": ""}
        
        try:
            f = open('exportXML.json','r')
            self.exportXML = json.load(f)
            self.ui.lineEdit_2.setText(str(self.exportXML['pathExport']))
            self.ui.doubleSpinBox.setValue(float(self.exportXML['maxSizeFile']))           
#            QtGui.QDoubleSpinBox.setValue(double(self.exportXML['MaxSiziFile']))
#            QtGui.QDoubleSpinBox.value()
            
        except Exception:
            print u'Ошибка чтения exportXML.json!'
        
#        QMessageBox.warning(self, u"Предупреждение", str(model_.rowCount()), QMessageBox.Ok)        
#        for i in range(model_.rowCount()):
#            action = self.mnu_2.addAction(model_.record(i).field('type').value().toString())
#            action.setData(model_.record(i).field('id').value().toString())

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

#        self.ui.dateEdit.setDate(datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day))        
        self.ui.dateEdit.setDate(datetime.date.today() - datetime.timedelta(days=30))        
        self.ui.dateEdit_2.setDate(datetime.date.today())
                        
        ''' 
        d2 = datetime.date(2020, 3, 30)
        d1 = d2 -  datetime.timedelta(days=30)
        self.ui.dateEdit_2.setDate(d2)        
        self.ui.dateEdit.setDate(d1)
 '''
        
        self.TestTypeTrans() 
            
        self.selTestMap()        

        '''            
        # Организация меню печати отчетов
        fnt = QtGui.QFont()
        fnt.setPointSize(12)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Отчет поверителя', self))
        self.mnu.addAction(QtGui.QAction(u'Протокол испытаний', self))
        self.mnu.addAction(QtGui.QAction(u'Этикетки', self))
        self.mnu.setFont(fnt)        
'''


    def TestTypeTrans(self):
        pass
    
        query = QSqlQuery(db1)
                                
        SQL = """select * from transformer
where type_transformer is null
        """
        
        query.prepare(SQL)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model_4.setQuery(query)
        if model_4.rowCount() > 0:
            QMessageBox.warning(self, u"Предупреждение", u"В справочнике трансфосматоров имеются трансформаторы с неприсоединенными типами в количестве " + str(model_4.rowCount()) + u" шт.,\n" +
                                u"что может привести к потере информации в выгружаемых XML-файлах.\n"  + u"Для предупреждения этих потерь запустите приложение 'AutoTypeTrans'\n" + 
                                u"(Автоматическое присоединение типов трансформаторов)", QMessageBox.Ok)

    
    
    
    
    
    


    def genItemXML(self, item):
        pass



    def pushButton_Click(self):
         dirlist = QtGui.QFileDialog.getExistingDirectory(self,u"Выбрать папку",".")
         if dirlist != '':
             self.ui.lineEdit_2.setText(dirlist)

    def pushButton_10_Click(self):                
        self.selTestMap()        


    def pushButton_12_Click(self):
        self.order_file = 0
        self.namesFiles = ''  # для сообщения            
        self.file = u'<?xml version="1.0" encoding="UTF-8" ?>\n'
        self.file += u'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-06-19">\n'
        self.items = []
        self.dateExport = PyQt4.QtCore.QDateTime.currentDateTime()

        self.sel_row = self.selModel.currentIndex().row()
        self.sel_row_2 = self.selModel_2.currentIndex().row()
        
        if self.ui.radioButton.isChecked():            
            if self.prExport == 1:
                QMessageBox.warning(self, u"Предупреждение", u"Экспорт по данной тележке был выполнен ранее", QMessageBox.Ok)
                return            
            
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете сформировать XML-файл\nпо текущей тележке?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return
            for j in range(model_2.rowCount()):
                self.ui.tableView_2.selectRow(j)                        
                if model_2.record(self.row_2).field('dateExport').value().toString() != '':
                    continue
                self.formBlock()
        
        if self.ui.radioButton_2.isChecked():
        
            if model_2.record(self.row_2).field('dateExport').value().toString() != '':
                QMessageBox.warning(self, u"Предупреждение", u"Экспорт по данному трансформатору был выполнен ранее", QMessageBox.Ok)
                return            
                        
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете сформировать XML-файл\nпо текущему трансформатору?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return
            self.formBlock()
        
        if self.ui.radioButton_3.isChecked():
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете сформировать XML-файл\nпо " + str(model.rowCount()) + u" тележкам?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return            
                        
            self.ui.tableView.selectRow(0)    
            for i in range(model.rowCount()):
                self.ui.tableView.selectRow(i)
                if self.prExport == 1:
                    continue                    
                for j in range(model_2.rowCount()):
                    self.ui.tableView_2.selectRow(j)
                    print 'model_2.record(self.row_2).field(dateExport).value().toString() = ', model_2.record(self.row_2).field('dateExport').value().toString()
                    if model_2.record(self.row_2).field('dateExport').value().toString() != '':
                        continue
                    self.formBlock()

        self.file += u'</gost:application>'
                
        now = datetime.datetime.now()
        nameFile = self.ui.lineEdit_2.text() + '/' +  now.strftime("%Y-%m-%d-%H_%M_%S")
        nameFile = str(nameFile).replace('\\', '/')
        if self.order_file > 0:
            nameFile += '_' + str(self.order_file)
        nameFile += '.xml'
        f = open(str(nameFile), 'w')
        f.write(self.file)
        f.close()

        
        self.insert_itemExportXML()
        self.selTestMap()
        
        if self.ui.radioButton.isChecked():            
            self.ui.tableView.selectRow(self.sel_row)        
        if self.ui.radioButton_2.isChecked():            
            self.ui.tableView.selectRow(self.sel_row)
            self.ui.tableView_2.selectRow(self.sel_row_2)

        self.namesFiles += nameFile + '\n'
            
#        QMessageBox.warning(self, u"Предупреждение", u"Файл для экспорта:\n" + nameFile + u"\nсформирован успешно!", QMessageBox.Ok)
        QMessageBox.warning(self, u"Предупреждение", u"Файл(ы) для экспорта:\n" + self.namesFiles + u"сформирован(ы) успешно!", QMessageBox.Ok)

                
                    
    def pushButton_2_Click(self):        
        self.items = []
        
        self.sel_row = self.selModel.currentIndex().row()
        self.sel_row_2 = self.selModel_2.currentIndex().row()
        
        if self.ui.radioButton_4.isChecked():            
            if self.prExport == 0:
                QMessageBox.warning(self, u"Предупреждение", u"Экспорт по данной тележке не производился", QMessageBox.Ok)
                return            
            
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить признак\nэкспорта в XML-файл по текущей тележке?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return
            for j in range(model_2.rowCount()):
                self.ui.tableView_2.selectRow(j)    
                self.items += [self.item]
        
        if self.ui.radioButton_5.isChecked():
            if model_2.record(self.row_2).field('dateExport').value().toString() == '':
                QMessageBox.warning(self, u"Предупреждение", u"Экспорт по данному трансформатору не производился", QMessageBox.Ok)
                return            
                        
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить признак\nэкспорта в XML-файл по текущему трансформатору?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return
            self.items += [self.item]
                
        if self.ui.radioButton_6.isChecked():
            r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить признак\nэкспорта в XML-файл по " + str(model.rowCount()) + u" тележкам?", QMessageBox.Yes, QMessageBox.No)            
            if r == QMessageBox.No:
                return
            self.ui.tableView.selectRow(0)    
            for i in range(model.rowCount()):
                self.ui.tableView.selectRow(i)    
                for j in range(model_2.rowCount()):
                    self.ui.tableView_2.selectRow(j)                        
                    self.items += [self.item]
        
#        print 'self.items = ', self.items
        self.delete_itemExportXML()
        self.selTestMap()

        if self.ui.radioButton_4.isChecked():            
            self.ui.tableView.selectRow(self.sel_row)        
        if self.ui.radioButton_5.isChecked():            
            self.ui.tableView.selectRow(self.sel_row)
            self.ui.tableView_2.selectRow(self.sel_row_2)
            
        QMessageBox.warning(self, u"Предупреждение", u"Признаки экспорта очищены успешно!", QMessageBox.Ok)
                

                
    '''
    def openFile(self):
        try:
            file = open(self.fileName, "r")
        except:
            self.createFile()

    def createFile(self):
        rootXML = ET.Element("settings")

        text = ET.Element("text")
        text.text = "Text"
        rootXML.append(text)

        file = open(self.fileName, "w")
        file.write(xml.tostring(rootXML, encoding="utf-8", method="xml").decode(encoding="utf-8"))
        file.close()
'''

    def selTestMap(self):
        v = unicode(self.ui.lineEdit.text()).upper()

        SQL = u"""
select min(id) id1, max(id) id2 from test_map as t1
where t1.createdatetime between to_date('""" + self.ui.dateEdit.text() + u"""','dd.mm.yyyy') and to_date('""" + self.ui.dateEdit_2.text() + u"""','dd.mm.yyyy') + 1
        """
        self.query.prepare(SQL)
        
        if not self.query.exec_():
            QMessageBox.warning(self, u"Предупреждение",  unicode(self.query.lastError().text()) + SQL, QMessageBox.Ok)
            return       
        model_.setQuery(self.query)
        id1 = model_.record(0).field('id1').value().toString()
        id2 = model_.record(0).field('id2').value().toString()

        
        
        SQL = u"""select t1.id, t1.supervisor, t1.climat, t6.test_type, 
                        case when t1.accepted then 1 else 0 end as accept,
                        t2.fio as fio_operator, 
                        t4.lastupdate, t4.temperature, t4.pressure, t4.humidity, 
                        date(t1.createdatetime) as createdatetime,
                        t1.accepted, t1.stand, t7.name,
                        case when count2 is null then null when count1 = count2 then 'выполнен' else 'вып. частично' end as isExport,
                        case when count2 is null then 0 when count1 = count2 then 1 else 2 end as prExport
        from test_map as t1 left outer join operator as t2 on (t1.supervisor = t2.id)
                            left outer join climat as t4 on (t1.climat = t4.id),
                            stand t6, test_type t7,
                            (
                              select * from
                              (select test_map, count(*) as count1 from item group by test_map) as t1 left outer join
                              (select t1.test_map as test_map_2, count(*) as count2 from item as t1, itemExportXML as t2 where t1.id = t2.item group by t1.test_map) as t2
                              on (t1.test_map = t2.test_map_2)
                            ) t9
        where t1.stand = t6.id
        and t6.test_type = t7.id
        and t1.id = t9.test_map
--        and t6.test_type = 1
--        and t6.test_type in (1,5)
--        and t6.test_type in (1,19)
        and t7.code in (1,5)
        and t1.id >=""" + id1 + u""" and t1.id <=""" + id2   
    
        
#        and t1.createdatetime between to_date('""" + self.ui.dateEdit.text() + u"""','dd.mm.yyyy') and to_date('""" + self.ui.dateEdit_2.text() + u"""','dd.mm.yyyy') + 1
                
        
        
        if self.ui.lineEdit.text() != "":
            SQL += u"""            
and t1.id in (select test_map from item t1, serial_number t2 where t1.serial_number = t2.id and serialnumber = """ + self.ui.lineEdit.text() + u""")
        """
        
        SQL += u"""
order by t1.id desc
        """
        
#        QMessageBox.warning(self, u"Предупреждение", SQL, QMessageBox.Ok)        
        """
        self.file = SQL
        
        nameFile = self.ui.lineEdit_2.text() + '/query.txt'
        nameFile = str(nameFile).replace('\\', '/')
#        if self.order_file > 0:
#            nameFile += '_' + str(self.order_file)
#        nameFile += '.xml'
        f = open(str(nameFile), 'w')
        f.write(self.file)
        f.close()
        """
                
        self.query.prepare(SQL)
        
        if not self.query.exec_():
            print unicode(self.query.lastError().text())
            print unicode(SQL)
            QMessageBox.warning(self, u"Предупреждение",  unicode(self.query.lastError().text()), QMessageBox.Ok)
                   
        model.setQuery(self.query)
        
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Поверитель")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Климат(время)")
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Темпера-\nтура")
        model.setHeaderData(8, QtCore.Qt.Horizontal, u"Давле-\nние")
        model.setHeaderData(9, QtCore.Qt.Horizontal, u"Влаж-\nность")
        model.setHeaderData(10, QtCore.Qt.Horizontal, u"Дата\nсоздания")
        model.setHeaderData(11, QtCore.Qt.Horizontal, u"Принято")
        model.setHeaderData(12, QtCore.Qt.Horizontal, u"Стенд")
        model.setHeaderData(13, QtCore.Qt.Horizontal, u"Вид испытания")
        model.setHeaderData(14, QtCore.Qt.Horizontal, u"Экспорт")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(5,  withCol1)
        self.ui.tableView.setColumnWidth(6,  withCol2)
        self.ui.tableView.setColumnWidth(7,  withCol3)
        self.ui.tableView.setColumnWidth(8,  withCol4)
        self.ui.tableView.setColumnWidth(9,  withCol5)
        self.ui.tableView.setColumnWidth(10,  withCol6)
        self.ui.tableView.setColumnWidth(11,  withCol7)
        self.ui.tableView.setColumnWidth(12,  withCol8)
        self.ui.tableView.setColumnWidth(13,  withCol9)
        self.ui.tableView.setColumnWidth(14,  withCol10)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.setColumnHidden(1, True)
        self.ui.tableView.setColumnHidden(2, True)
        self.ui.tableView.setColumnHidden(3, True)
        self.ui.tableView.setColumnHidden(4, True)
        self.ui.tableView.setColumnHidden(15, True)
        self.ui.tableView.selectRow(0)
         

    def selItem(self):
        row = self.selModel.currentIndex().row()
        global test_map
        if row < 0:
            test_map = -1
        else:    
            test_map = int(model.record(row).field('id').value().toString())
            
        query = QSqlQuery(db1)
        
        SQL = """select t1.id, t1.defect, case when t1.istested then 1 else 0 end as istest,
trim(to_char(t2.makedate, '9999')) || '-' || trim(to_char(serialnumber, '9999999999')) as serialnumber, 
--t3.fullname as name_trans, 
t3.shortname as name_trans, 
date(createdatetime),
t4.fullname as name_defect,
t1.istested, 
t5.number_reestr, 
--date(t1.acceptdatetime), 
t5.interval,
--date(t1.acceptdatetime + t5.interval * '1 year'::interval - '1 day'::interval) as validDate,
date(t1.createdatetime + t5.interval * '1 year'::interval - '1 day'::interval) as validDate,
t5.method,
trim(to_char(t2.makedate, '9999')) as makedate,
date(t6.dateExport) as dateExport
from item t1 left outer join defect as t4 on (t1.defect = t4.id)  
             left outer join itemExportXML as t6 on (t1.id = t6.item),
serial_number t2, transformer t3 left outer join type_transformer as t5 on (t3.type_transformer = t5.id)
where t1.serial_number = t2.id
and t2.transformer = t3.id
and t1.test_map = :test_map
and t1.istested
"""        
        if self.ui.lineEdit.text() != "":
            SQL += """            
and serialnumber = :serialnumber
"""
            SQL += """            
order by serialnumber
"""

#        print 'test_map = ', test_map
#        print 'serialnumber = ', self.ui.lineEdit.text()
        print SQL
        print test_map
        print self.ui.lineEdit.text()

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
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Несоот-\nветствие")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Испы-\nтано")
        model_2.setHeaderData(8,  QtCore.Qt.Horizontal, u"Номер по\nреестру")
        model_2.setHeaderData(9,  QtCore.Qt.Horizontal, u"Интер-\nвал")
        model_2.setHeaderData(10,  QtCore.Qt.Horizontal, u"Дата\nповерки")
        model_2.setHeaderData(11,  QtCore.Qt.Horizontal, u"Методика\nповерки")
        model_2.setHeaderData(13,  QtCore.Qt.Horizontal, u"Дата\nэкспорта")
                    
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(1, True)
        self.ui.tableView_2.setColumnHidden(2, True)
        self.ui.tableView_2.setColumnHidden(12, True)
                
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(3,  withCol_1)
        self.ui.tableView_2.setColumnWidth(4,  withCol_2)
        self.ui.tableView_2.setColumnWidth(5,  withCol_3)
        self.ui.tableView_2.setColumnWidth(6,  withCol_4)
        self.ui.tableView_2.setColumnWidth(7,  withCol_5)
        self.ui.tableView_2.setColumnWidth(8,  withCol_6)
        self.ui.tableView_2.setColumnWidth(9,  withCol_7)
        self.ui.tableView_2.setColumnWidth(10,  withCol_8)
        self.ui.tableView_2.setColumnWidth(11,  withCol_9)
        self.ui.tableView_2.setColumnWidth(13,  withCol_10)
        
                
    def selMapMsr(self):
        row = self.selModel.currentIndex().row()
        global test_map
        if row < 0:
            test_map = -1
        else:    
            test_map = int(model.record(row).field('id').value().toString())
        
        query = QSqlQuery(db1)
                                
        SQL = u"""select t1.id, t1.zav_msr, t2.type, name_msr, zav_num,
CASE WHEN t2.type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment        
from map_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and t1.test_map = :test_map
order by type, name_msr
        """
                
        query.prepare(SQL)
        query.bindValue(":test_map", test_map);            
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            return
            
        model_3.setQuery(query)
        
        model_3.setHeaderData(3, QtCore.Qt.Horizontal, u"Наименование\nсредства\nизмерения")
        model_3.setHeaderData(4, QtCore.Qt.Horizontal, u"Завод-\nской\nномер")
        model_3.setHeaderData(5, QtCore.Qt.Horizontal, u"Тип")
        model_3.setHeaderData(6, QtCore.Qt.Horizontal, u"Номер в\nгосреестре")
        model_3.setHeaderData(7, QtCore.Qt.Horizontal, u"Дополни-\nтельные\nсведения")
            
        self.ui.tableView_3.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView_3.setColumnWidth(3,  withCol_11)
        self.ui.tableView_3.setColumnWidth(4,  withCol_12)
        self.ui.tableView_3.setColumnWidth(5,  withCol_13)
        self.ui.tableView_3.setColumnWidth(6,  withCol_14)
        self.ui.tableView_3.setColumnWidth(6,  withCol_15)
        
        self.ui.tableView_3.setColumnHidden(0, True)
        self.ui.tableView_3.setColumnHidden(1, True)
        self.ui.tableView_3.setColumnHidden(2, True)
        self.ui.tableView_3.selectRow(0)
        
                
    def selectionChanged(self):
        print 'selectionChanged'
        self.metrologist = ''
        
        self.mitypeNumber = ''
        self.manufactureNum = ''
        self.manufactureYear = ''
        self.modification = ''
        self.prExport = 0
        self.type = ''
 
        self.number = ''
        self.typeNum = ''
        self.msr_manufactureNum = ''
        
        self.row = self.selModel.currentIndex().row()
        
        self.prExport = int(model.record(self.row).field('prExport').value().toString())
        self.metrologist = model.record(self.row).field('fio_operator').value().toString()
        self.temperature = model.record(self.row).field('temperature').value().toString()
        self.pressure    = model.record(self.row).field('pressure').value().toString()
        self.humidity    = model.record(self.row).field('humidity').value().toString()
        
        self.selItem()
        self.selMapMsr()

    def selectionChanged_2(self):
        print 'selectionChanged_2'
        self.row_2 = self.selModel_2.currentIndex().row()
        if self.row_2 < 0:
            return
        self.item = unicode(model_2.record(self.row_2).field('id').value().toString())
        self.mitypeNumber    = unicode(model_2.record(self.row_2).field('number_reestr').value().toString())
        self.manufactureNum  = unicode(model_2.record(self.row_2).field('serialnumber').value().toString())
        self.manufactureYear = '20' + unicode(model_2.record(self.row_2).field('makedate').value().toString())
        self.modification    = unicode(model_2.record(self.row_2).field('name_trans').value().toString())[:128]
        self.vrfDate  = unicode(model.record(self.row).field('createdatetime').value().toString())
        self.validDate  = unicode(model_2.record(self.row_2).field('validDate').value().toString())
        self.docTitle  = unicode(model_2.record(self.row_2).field('method').value().toString())
  
    def selectionChanged_3(self):
        print 'selectionChanged_3'
        self.row_3 = self.selModel_3.currentIndex().row()
        if self.row_3 < 0:
            return
        self.type = model_3.record(self.row_3).field('type').value().toString()
        self.number = unicode(model_3.record(self.row_3).field('comment').value().toString())
        self.typeNum = unicode(model_3.record(self.row_3).field('num_gosreestr').value().toString())
        self.msr_manufactureNum = unicode(model_3.record(self.row_3).field('zav_num').value().toString()) 
 
        
    def formBlock(self):
#        self.block = ''
        self.block = self.metrologist[0]
#        self.block = self.metrologist
        self.block  += '    <gost:result>\n'

        self.block += '        <gost:miInfo>\n'
        self.block += '            <gost:singleMI>\n'
        self.block += '                <gost:mitypeNumber>' + self.mitypeNumber + '</gost:mitypeNumber>\n'
        self.block += '                <gost:manufactureNum>' + self.manufactureNum + '</gost:manufactureNum>\n'
        self.block += '                <gost:manufactureYear>' + self.manufactureYear + '</gost:manufactureYear>\n'
        self.block += '                <gost:modification>' + unicode(self.modification).encode('utf-8') + '</gost:modification>\n'
        self.block += '            </gost:singleMI>\n'
        self.block += '        </gost:miInfo>\n'
#        self.block += '        <signCipher>' + u'ВЧМ' + '</signCipher>\n'
        self.block += '        <gost:signCipher>' + unicode(u'ВЧМ').encode('utf-8') + '</gost:signCipher>\n'
        self.block += '        <gost:miOwner>' + '-' + '</gost:miOwner>\n'
        self.block += '        <gost:vrfDate>' + self.vrfDate + '</gost:vrfDate>\n'
        self.block += '        <gost:validDate>' + self.validDate + '</gost:validDate>\n'
        self.block += '        <gost:type>' + '1' + '</gost:type>\n'
        self.block += '        <gost:calibration>' + 'false' + '</gost:calibration>\n'
        self.block += '        <gost:applicable>\n'
        self.block += '            <gost:signPass>' + 'true' + '</gost:signPass>\n'
        self.block += '            <gost:signMi>' + 'true' + '</gost:signMi>\n'        
        self.block += '        </gost:applicable>\n'
        self.block += '        <gost:docTitle>' + unicode(self.docTitle).encode('utf-8') + '</gost:docTitle>\n'
        
        self.block += '        <gost:metrologist>' + unicode(self.metrologist).encode('utf-8') + '</gost:metrologist>\n'
        
        self.block += '        <gost:means>\n'
#19.01.2022        self.block += '            <gost:uve>\n'        
        self.block += '            <gost:mieta>\n'        
        for i in range(model_3.rowCount()):
            self.ui.tableView_3.selectRow(i)
            if self.type == '1':                                
                self.block += '                <gost:number>' + unicode(self.number).encode('utf-8') + '</gost:number>\n'            
#19.01.2022        self.block += '            </gost:uve>\n' 
        self.block += '            </gost:mieta>\n' 
               
        self.block += '            <gost:mis>\n'        
        for i in range(model_3.rowCount()):
            self.ui.tableView_3.selectRow(i)                                
            if self.type == '2':                                
                self.block += '                <gost:mi>\n'
                self.block += '                    <gost:typeNum>' + self.typeNum + '</gost:typeNum>\n'
                self.block += '                    <gost:manufactureNum>' + self.msr_manufactureNum + '</gost:manufactureNum>\n'
                self.block += '                </gost:mi>\n'            
        self.block += '            </gost:mis>\n'        
        
        self.block += '        </gost:means>\n'
               
        self.block += '        <gost:conditions>\n'               
        self.block += '            <gost:temperature>' + self.temperature + ' C </gost:temperature>\n'
        self.block += '            <gost:pressure>' + self.pressure + u' кПа'.encode('utf-8') + '</gost:pressure>\n'
        self.block += '            <gost:hymidity>' + self.humidity + ' %</gost:hymidity>\n'               
        self.block += '        </gost:conditions>\n'
               
        self.block += '    </gost:result>\n'
        
        
                
        if len(self.file) + len(self.block) > self.ui.doubleSpinBox.value() * 1000000 - 100:

            self.file += u'</gost:application>'
                
            now = datetime.datetime.now()
            nameFile = self.ui.lineEdit_2.text() + '/' +  now.strftime("%Y-%m-%d-%H_%M_%S")
            nameFile = str(nameFile).replace('\\', '/')
            if self.order_file > 0:
                nameFile += '_' + str(self.order_file)
            nameFile += '.xml'
        #    QMessageBox.warning(self, u"Предупреждение", nameFile, QMessageBox.Ok)
            self.namesFiles += nameFile + '\n'
            f = open(str(nameFile), 'w')
            f.write(self.file)
            f.close()
            
            self.order_file += 1

            self.file = u'<?xml version="1.0" encoding="UTF-8" ?>\n'
            self.file += u'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-06-19">\n'
                
        self.file += self.block[1:]

 #       print 'len(self.file) = ', len(self.file)
 #       QMessageBox.warning(self, u"Предупреждение", str(len(self.file)), QMessageBox.Ok)
        
        
        
        


        
        
        
        
        
        self.items += [self.item]


    def insert_itemExportXML(self):
        query = QSqlQuery(db)
        
        for i in range(len(self.items)):
            query.prepare("INSERT INTO itemExportXML (item, dateExport) VALUES (:item, :dateExport)")
            query.bindValue(":item", self.items[i]);
            query.bindValue(":dateExport", self.dateExport);
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)


    def delete_itemExportXML(self):
        query = QSqlQuery(db)
        
        for i in range(len(self.items)):
            query.prepare("DELETE FROM itemExportXML WHERE item = :item")
            query.bindValue(":item", self.items[i]);
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка удаления признака", QMessageBox.Ok)


    def closeEvent(self, event):        
        try:
            f = open('exportXML.json','w')
            self.exportXML['pathExport'] = str(self.ui.lineEdit_2.text())               
            self.exportXML['maxSizeFile'] = str(self.ui.doubleSpinBox.text())    
            
#            self.ui.doubleSpinBox.setValue(double(self.exportXML['MaxSizeFile']))           
            
                
            json.dump(self.exportXML, f)
        except Exception:
            print u'Ошибка записи config.json!'        
        return

        try:
            print 1        
            f = open('exportXML.json','w')
            print 2        
            #self.config['exportDir'] = self.ui.lineEdit_2.text()        
            print 3, self.ui.lineEdit_2.text()        
            json.dump(self.config, f)
            print 4                    
        except Exception:
            print u'Ошибка записи config.json!'


    def TestBase(self):
        print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        query.prepare("select * from itemExportXML")
        if not query.exec_(): err_tbl += "itemExportXML\n"
       
        if err_tbl != "":
            print err_tbl  
            
            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД требуется произвести изменения,
необходимые для работы приложения\n""" +
u"Произвести изменения БД?", QMessageBox.Yes, QMessageBox.No)                        
                                    
            if r == QMessageBox.Yes:
                self.InitBase()
                return True
            else:
                return False
        return True


    def InitBase(self):
        print u"Инициализация БД"        
        query = QSqlQuery(db)

        SQL = u"""
CREATE TABLE itemExportXML
(
  --id serial PRIMARY KEY,  
  item integer REFERENCES item (id),
  dateExport timestamp without time zone NOT NULL DEFAULT now()
);
COMMENT ON TABLE itemExportXML IS 'Справочник дат экспорта результатов испытаний';
--COMMENT ON COLUMN itemExportXML.id IS 'Идентификатор записи';
COMMENT ON COLUMN itemExportXML.item IS 'Ссылка на item';
COMMENT ON COLUMN itemExportXML.dateExport IS 'Дата/время экспорта';
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        print SQL
        return

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
    print 'type(db) = ', type(db)
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
