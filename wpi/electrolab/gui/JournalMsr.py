# -*- coding: UTF-8 -*-
#
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import  QIcon, QColor
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox, QDateEdit, QCheckBox,QLineEdit,QMainWindow
from electrolab.gui.reporting import FRPrintForm
import sys
import datetime
import os
#import qrcode
from electrolab.gui.ReportsMsr import *
from dpframe.base.inits import json_config_init

selectMsr = "SELECT * FROM msr WHERE id_group=:ID ORDER BY name_msr"

#selectJournalChecking = """SELECT t1.id, checking_date, view_date, sertificate, t1.firms_repair_msr, t2.name_firm, t1.fif,
#t2.address, to_char(checking_date, 'dd.mm.yyyy') as checking_date_,
#to_char(checking_date + '8 month'::INTERVAL - '1 day'::INTERVAL, 'dd.mm.yyyy') as checking_date__
#FROM journal_checking t1 LEFT OUTER JOIN firms_repair_msr t2 ON (t1.firms_repair_msr = t2.id)
#WHERE id_zav=:ID
#ORDER BY checking_date"""

selectHistoryLocation = """SELECT t1.id, name_location, date_move, location_msr 
FROM history_location_msr t1 LEFT OUTER JOIN location_msr t2 ON (t1.location_msr = t2.id)
WHERE zav_msr=:ID
ORDER BY date_move DESC"""

id_msr = ''
id_zav = ''
id_journal = ''
id_history_location = ''
tempDate = datetime.date.today()

modelTree = QStandardItemModel()
model = QSqlQueryModel()
model2 = QSqlQueryModel()
model3 = QSqlQueryModel()
model4 = QSqlQueryModel()
model5 = QSqlQueryModel()

withCol1 = 200
withCol2 = 100
withCol3 = 100

withCol4 = 100
withCol41 = 100
withCol5 = 100
withCol6 = 100
withCol61 = 100
withCol62 = 100
withCol63 = 100
withCol7 = 100                       
withCol71 = 100                       

withCol8 = 100                        
withCol81 = 100                        
withCol9 = 100                        
withCol91 = 200                        
withCol92 = 120                        

withCol10 = 100                        
withCol11 = 100                        
withCol12 = 100
                        
withCol13 = 200                        
withCol14 = 100                        

VSB1 = False
VSB2 = False
VSB3 = False
VSB4 = False
VSB5 = False
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
        # try, Чтобы не ругалась при выходе из приложения   
        try:
            QtCore.QEvent.Resize
        except:
            return True    
        global VSB1, VSB2, VSB3, VSB4, VSB5
        
        if id_category == '1':
            withCol3_ = 0
            withCol81_ = 0
        else:    
            withCol3_ = withCol3            
            withCol81_ = withCol81

        if id_category == '1' or id_category == '2':
            withCol92_ = withCol92
            withCol62_ = withCol62
        if id_category == '3':
            withCol92_ = 0
            withCol62_ = 0
                        
        if obj.objectName() == 'tv1' and (e.type() != QtCore.QEvent.Resize or VSB1 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3_))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3_)
            VSB1 = obj.verticalScrollBar().isVisible()
                
        if obj.objectName() == 'tv2' and (e.type() != QtCore.QEvent.Resize or VSB2 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol4 + withCol41 + withCol5 + withCol6 + withCol61 + withCol62_ + withCol63 + withCol7 + withCol71))
            obj.setColumnWidth(2, koef * withCol4)
            obj.setColumnWidth(3, koef * withCol41)
            obj.setColumnWidth(4, koef * withCol5)
            obj.setColumnWidth(5, koef * withCol6)
            
            obj.setColumnWidth(6, koef * withCol61)
#            obj.setColumnWidth(7, koef * withCol62)
            obj.setColumnWidth(7, koef * withCol62_)
            obj.setColumnWidth(8, koef * withCol63)
                        
            obj.setColumnWidth(9, koef * withCol7)
            obj.setColumnWidth(10, koef * withCol71)
            VSB2 = obj.verticalScrollBar().isVisible()    
                
        if obj.objectName() == 'tv3' and (e.type() != QtCore.QEvent.Resize or VSB3 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol8 + withCol81_ + withCol9 + withCol91 + withCol92_))
            obj.setColumnWidth(1, koef * withCol8)
            obj.setColumnWidth(2, koef * withCol81_)
            obj.setColumnWidth(3, koef * withCol9)
            obj.setColumnWidth(5, koef * withCol91)
#            obj.setColumnWidth(6, koef * withCol92)
            obj.setColumnWidth(6, koef * withCol92_)
            VSB3 = obj.verticalScrollBar().isVisible()    
                
        if obj.objectName() == 'tv4' and (e.type() != QtCore.QEvent.Resize or VSB4 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol10 + withCol11 + withCol12))
            obj.setColumnWidth(1, koef * withCol10)
            obj.setColumnWidth(2, koef * withCol11)
            obj.setColumnWidth(3, koef * withCol12)
            VSB4 = obj.verticalScrollBar().isVisible()    
            #print "RESIZE4"    
                
        if obj.objectName() == 'tv5' and (e.type() != QtCore.QEvent.Resize or VSB5 != obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol13 + withCol14))
            obj.setColumnWidth(1, koef * withCol13)
            obj.setColumnWidth(2, koef * withCol14)
            VSB5 = obj.verticalScrollBar().isVisible()    
                
        return False
    
def MyLoadUi(UiDir, UiFile, wnd):
    try:
        uidir = UiDir           
        if not os.path.exists(uidir + UiFile):        
            uidir = ""
            
        uic.loadUi(uidir + UiFile, wnd)
        wnd.tag = 1
        return True
    except:    
        wnd.tag = 0
        QMessageBox.warning(None, u"Предупреждение", u"Проблемы с загрузкой файла: " + UiFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
        return False

class classJournal(QMainWindow):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        self.is_show = True
        if not MyLoadUi(path_ui, "journalmsr.ui", self):
            self.is_show = False
            return

        '''
        import argparse
        parser = argparse.ArgumentParser(description='A tutorial of argparse!')
        args = parser.parse_args()
   
'''
       
       
        self.period = '0'
       

        self.CurDir = os.getcwd()
#        self.CurDir = os.getcwd()
        self.CurDir_ = self.CurDir.replace("\\", "/")

        '''
        print self.CurDir_ + '/qrCode.exe YUIOP'        
        print type(str(self.CurDir_ + '/qrCode.exe YUIOP'))
                
        QMessageBox.warning(self, u"Предупреждение", u"444 " + self.CurDir_, QMessageBox.Ok)
        QMessageBox.warning(self, u"Предупреждение", u"444 " + self.CurDir_ + '/qrCode.exe YUIOP', QMessageBox.Ok)
        
        print 'd:/PROJECTS/C#/QRCode/QRCode/QRCode/bin/Debug/qrCode.exe YUIOP'
        print type('d:/PROJECTS/C#/QRCode/QRCode/QRCode/bin/Debug/qrCode.exe YUIOP')
    
#        os.system('d:/PROJECTS/C#/QRCode/QRCode/QRCode/bin/Debug/qrCode.exe YUIOP')
#        os.system('d:/PROJECTS/qrCode.exe YUIOP')
#        os.system('d:/work4/ElectroLab/trunk/electrolab/gui/qrCode.exe YUIOP')
#        os.system('d:/work4/qrCode.exe YUIOP')
        os.system(self.CurDir_ + '/qrCode.exe YUIOP')
        
        QMessageBox.warning(self, u"Предупреждение", u"555", QMessageBox.Ok)
           '''     
                
                
                
                
                
                
                
                
                
                
                
        self.resize(1000,600)
        self.splitter.setStretchFactor(0,1)

        self.dateEdit.setCalendarPopup(1)
        
        # Временно
        self.checkBox.setChecked(True)
        self.lineEdit.setEnabled(False)
        self.dateEdit.setEnabled(False)        
        self.is_show = True 
        if not self.TestBase():
            self.is_show = False 
            return

        self.dateEdit.setDate(datetime.date.today())        
 
        self.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_3.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_4.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_5.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_6.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_7.setIcon(QIcon(u':/ico/ico/block_64.png'))
        self.pushButton_8.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_9.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_10.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_11.setIcon(QIcon(u':/ico/ico/block_64.png'))
        self.pushButton_12.setIcon(QIcon(u':/ico/ico/print_64.png'))

        self.checkBox.toggled.connect(self.checkBox_Toggle)
        self.checkBox_2.toggled.connect(self.checkBox_2_Toggle)
        self.checkBox_5.toggled.connect(self.checkBox_5_Toggle)
        self.checkBox_3.toggled.connect(self.checkBox_3_Toggle)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)
        self.checkBox_4.toggled.connect(self.checkBox_4_Toggle)
        self.dateEdit.dateChanged.connect(self.dateEdit_textChanged)
        
        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.pushButton_3.clicked.connect(self.pushButton3_Click)
        self.pushButton_4.clicked.connect(self.pushButton4_Click)
        self.pushButton_5.clicked.connect(self.pushButton5_Click)
        self.pushButton_6.clicked.connect(self.pushButton6_Click)
        self.pushButton_7.clicked.connect(self.pushButton7_Click)
        self.pushButton_8.clicked.connect(self.pushButton8_Click)
        self.pushButton_9.clicked.connect(self.pushButton9_Click)
        self.pushButton_10.clicked.connect(self.pushButton10_Click)
        self.pushButton_11.clicked.connect(self.pushButton11_Click)
        self.pushButton_12.clicked.connect(self.pushButton12_Click)

        self.connect(self.action_2, QtCore.SIGNAL('triggered()'), self.StartClsMsr)
        self.connect(self.action_5, QtCore.SIGNAL('triggered()'), self.StartFirmRepair)
        self.connect(self.action_6, QtCore.SIGNAL('triggered()'), self.StartLocation)
        self.connect(self.action_3, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(self.action_4, QtCore.SIGNAL('triggered()'), self.StartRep1)
        self.connect(self.action_7, QtCore.SIGNAL('triggered()'), self.StartRep2)
        self.connect(self.action_8, QtCore.SIGNAL('triggered()'), self.StartRep3)
        self.connect(self.action_9, QtCore.SIGNAL('triggered()'), self.StartRep4)

        self.treeView.setModel(modelTree)        
        self.selModelTree = self.treeView.selectionModel()        
        self.connect(self.selModelTree, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChangedTree)

        self.tableView.setModel(model)
        self.selModel = self.tableView.selectionModel()
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)
        
        self.tableView_2.setModel(model2)
        self.selModel2 = self.tableView_2.selectionModel()
        self.connect(self.selModel2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged2)

        self.tableView_3.setModel(model3)
        self.selModel3 = self.tableView_3.selectionModel()
        self.connect(self.selModel3, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged3)
        
        self.tableView_5.setModel(model5)
        self.selModel5 = self.tableView_5.selectionModel()
        self.connect(self.selModel5, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged5)
        
        self.tableView_4.setModel(model4)

        self.tableView.setObjectName('tv1')
        self.tableView_2.setObjectName('tv2')
        self.tableView_3.setObjectName('tv3')
        self.tableView_5.setObjectName('tv5')
        self.tableView_4.setObjectName('tv4')
                
        # Удаление горизонтальных полос прокрутки
        self.tableView.setHorizontalScrollBarPolicy(1)
        self.tableView_2.setHorizontalScrollBarPolicy(1)
        self.tableView_3.setHorizontalScrollBarPolicy(1)
        self.tableView_5.setHorizontalScrollBarPolicy(1)
        self.tableView_4.setHorizontalScrollBarPolicy(1)

        self.tableView.installEventFilter(MyFilter(self.tableView))
        self.tableView_2.installEventFilter(MyFilter(self.tableView_2))
        self.tableView_3.installEventFilter(MyFilter(self.tableView_3))
        self.tableView_5.installEventFilter(MyFilter(self.tableView_5))
        self.tableView_4.installEventFilter(MyFilter(self.tableView_4))
        
        self.FillTree()
        
        
                
    def StartClsMsr(self):
        from ClsMsr import classMsr
        wind = classMsr(env)
        if wind.tag != 0:
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
            wind.show()
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()
        
        self.FillTree()

    def StartFirmRepair(self):
        from firms_repair_msr import FirmRepair
        wind = FirmRepair(env)
        if wind.tag != 0:
            wind.setWindowTitle(u'Организации, проводящие поверку/калибровку/ремонт СИ');            
            wind.pushButton_4.setEnabled(False)
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
            wind.show()
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()                
            if wind.id != '':
                self.lineEdit.Tag = wind.id
                self.lineEdit.setText(wind.name_firm)

    def StartLocation(self):
        from location_msr import Location
        wind = Location(env)
        if wind.tag != 0:
            wind.setWindowTitle(u'Местонахождения средств измерения')            
            wind.pushButton_4.setEnabled(False)
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
            wind.show()
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()
            if wind.id != '':
              #  print 22222222222222222222222222222222222222
                self.lineEdit.Tag = wind.id
                self.lineEdit.setText(wind.name_location)

    def StartRep1(self):        
        from ReportsMsr import GraphTestMsr
        wind = GraphTestMsr(env)        
        wind.exec_()        
             
    def StartRep2(self):        
        from ReportsMsr import LocationMsr
        wind = LocationMsr(env)        
        wind.setWindowTitle(u'СИ, находящиеся в резерве/консервации')
        wind.label.setVisible(False)        
        wind.comboBox.setVisible(False)        
        wind.exec_()        
             
    def StartRep3(self):
        from ReportsMsr import LocationMsr
        wind = LocationMsr(env)
        wind.setWindowTitle(u'Список СИ по месту нахождения/эксплуатации')        
        wind.exec_()        

    def StartRep4(self):        
        from ReportsMsr import GraphPPR
        wind = GraphPPR(env)        
#        from ReportsMsr import LocationMsr
#        wind = LocationMsr(env)
        wind.setWindowTitle(u'График ППР и аттестации испытательного оборудования')
        wind.label.setVisible(False)        
        wind.comboBox.setVisible(False)        
        wind.exec_()        
                                       
    def FillTree(self):
# Заполнение модели двумя уровнями данных из запросов
        modelTree.clear()        
        modelTree.reset()        
        grandparent = QStandardItem(u"СРЕДСТВА ИЗМЕРЕНИЯ (весь перечень)")
        grandparent.setData(1)
        modelTree.appendRow(grandparent)
        SQL1 = "select id, name_type from type_msr where id_category = 1 order by name_type"
        query1 = QSqlQuery(SQL1, db)
        SQL2 = "select id, name_group from group_msr where id_type=:id_type order by name_group"
        query2 = QSqlQuery(db)
        query2.prepare(SQL2)
        i = 0            
        while query1.next():
            parent = QStandardItem(query1.value(1).toString())
            parent.setData(query1.value(0).toString())
            grandparent.setChild(i, parent)
            query2.bindValue(":id_type", query1.value(0));
            query2.exec_()
            i += 1
            j = 0
            while query2.next():
                item = QStandardItem(query2.value(1).toString())
                item.setData(query2.value(0).toString())
                parent.setChild(j, item)
                j += 1
                        
        grandparent = QStandardItem(u"СРЕДСТВА ЗАЩИТЫ (весь перечень)")
        grandparent.setData(2)
        modelTree.appendRow(grandparent)
        SQL1 = "select id, name_type from type_msr where id_category = 2 order by name_type"
        query1 = QSqlQuery(SQL1, db)
        SQL2 = "select id, name_group from group_msr where id_type=:id_type order by name_group"
        query2 = QSqlQuery(db)
        query2.prepare(SQL2)
        i = 0            
        while query1.next():
            parent = QStandardItem(query1.value(1).toString())
            parent.setData(query1.value(0).toString())
            grandparent.setChild(i, parent)
            query2.bindValue(":id_type", query1.value(0));
            query2.exec_()
            i += 1
            j = 0
            while query2.next():
                item = QStandardItem(query2.value(1).toString())
                item.setData(query2.value(0).toString())
                parent.setChild(j, item)
                j += 1                        
            
        grandparent = QStandardItem(u"ИСПЫТАТЕЛЬНОЕ ОБОРУДОВАНИЕ (весь перечень)")
        grandparent.setData(3)
        modelTree.appendRow(grandparent)
        SQL1 = "select id, name_type from type_msr where id_category = 3 order by name_type"
        query1 = QSqlQuery(SQL1, db)
        SQL2 = "select id, name_group from group_msr where id_type=:id_type order by name_group"
        query2 = QSqlQuery(db)
        query2.prepare(SQL2)
        i = 0            
        while query1.next():
            parent = QStandardItem(query1.value(1).toString())
            parent.setData(query1.value(0).toString())
            grandparent.setChild(i, parent)
            query2.bindValue(":id_type", query1.value(0));
            query2.exec_()
            i += 1
            j = 0
            while query2.next():
                item = QStandardItem(query2.value(1).toString())
                item.setData(query2.value(0).toString())
                parent.setChild(j, item)
                j += 1                        
            
            
            
        self.treeView.expandAll()
        first = modelTree.index(0, 0, QModelIndex());
        self.treeView.setCurrentIndex(first)


    def ViewMsr(self, id_search):
        row = self.selModelTree.currentIndex().row()
        row1 = self.selModelTree.currentIndex().parent().row()
        interId = self.selModelTree.currentIndex().internalId()
        parentitem = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent()
        query = QSqlQuery(db)
        if parentitem == None:
            
            selectMsr = """SELECT msr.id, name_msr, period, period_view, name_group FROM msr, group_msr, type_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = type_msr.id
                           AND type_msr.id_category = :ID_CATEGORY
                           ORDER BY name_msr"""                        
            
            query.prepare(selectMsr)
            global id_category                       
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_category", id_category)          
        elif parentitem.parent() == None:
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent().data().toString()
            selectMsr = """SELECT msr.id, name_msr, period, period_view, name_group FROM msr, group_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = :ID_TYPE
                           ORDER BY name_msr"""
            query.prepare(selectMsr)
            id_type = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_type", id_type)          
#            print 'id_type = ', id_type
        else:
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent().parent().data().toString()
#            selectMsr = """SELECT id, name_msr, period, period_view FROM msr
#                           WHERE id_group = :ID_GROUP
#                           ORDER BY name_msr"""
            # Добовил group_msr, чтобы вытаскивать name_group для отчета
            selectMsr = """SELECT msr.id, name_msr, period, period_view, name_group FROM msr, group_msr
                           WHERE msr.id_group = group_msr.id
                           AND id_group = :ID_GROUP
                           ORDER BY name_msr"""
            query.prepare(selectMsr)
            id_group = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_group", id_group)
#            print 'id_group = ', id_group
        query.exec_()
        
#        print 'id_categoryid_category = ', id_category

        if not self.checkBox_3.isChecked() and not self.checkBox_4.isChecked():   
            model4.clear() ###        
            model4.reset() ###       
            model5.clear()        
            model5.reset()        
            model3.clear()        
            model3.reset()        
            model2.clear()        
            model2.reset()        
            model.clear()                
        
        model.setQuery(query)
        
        if model.query().size() < 1:
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)       
            self.pushButton_8.setEnabled(False)       
            self.pushButton_9.setEnabled(False)       
            self.pushButton_10.setEnabled(False)       
            self.pushButton_11.setEnabled(False)       
            self.pushButton_12.setEnabled(False)       
           
#        print 'id_category = ' + id_category   
                
        if id_category == '1':
#            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование средства измерения")
            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Тип средства\nизмерения")
        if id_category == '2':
#            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование средства защиты")
            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Тип средства защиты")
        if id_category == '1' or id_category == '2':
            model.setHeaderData(2, QtCore.Qt.Horizontal, u"Периодичность\nповерки")
            model.setHeaderData(3, QtCore.Qt.Horizontal, u"Периодичность\nосмотра")
        if id_category == '3':
            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование\nиспытательного\nоборудования")
            model.setHeaderData(2, QtCore.Qt.Horizontal, u"Периодичность\nаттестации")
            model.setHeaderData(3, QtCore.Qt.Horizontal, u"Периодичность\nпроведения ППР")

                     
        self.tableView.setColumnHidden(0, True)        
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        
        self.searchInModel(0, self.tableView, model)
        self.pushButton.setEnabled(self.selModel.currentIndex().row() >= 0)
        self.tableView.repaint()


    def ViewAccuracy(self, id_search):
        query9 = QSqlQuery(db)
        selectAccuracy = """SELECT id, name_vid, range_msr, classaccuracy FROM accuracy_msr
                            WHERE id_msr=:ID
                            ORDER BY name_vid, range_msr"""
        query9.prepare(selectAccuracy)                        
        query9.bindValue(":id", id_msr)            
        query9.exec_()
                
        model4.setQuery(query9)
                
        if id_category == '1' or id_category == '2':
            model4.setHeaderData(1, QtCore.Qt.Horizontal, u"Вид измерения")
            model4.setHeaderData(2, QtCore.Qt.Horizontal, u"Диапазон измерения")
            model4.setHeaderData(3, QtCore.Qt.Horizontal, u"Класс точности")
        if id_category == '3':
            model4.setHeaderData(1, QtCore.Qt.Horizontal, u"Вид измерения")
            model4.setHeaderData(2, QtCore.Qt.Horizontal, u"Ном. значение\nхарактеристики")
            model4.setHeaderData(3, QtCore.Qt.Horizontal, u"Допустимое\nотклонение")
            
        self.tableView_4.setColumnHidden(0, True)        
        self.tableView_4.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        

    def ViewZavMsr(self, id_search, id_msr, zav_num):
        prov_spis = ""
        if self.checkBox.isChecked() and not self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            prov_spis = "AND (finish_date IS NULL AND reserve_date IS NULL)"
        
        if self.checkBox.isChecked() and self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            prov_spis = "AND ((finish_date IS NULL AND reserve_date IS NULL) OR (finish_date IS NOT NULL AND reserve_date IS NULL))"
        
        if self.checkBox.isChecked() and not self.checkBox_2.isChecked() and self.checkBox_5.isChecked():
            prov_spis = "AND ((finish_date IS NULL AND reserve_date IS NULL) OR (finish_date IS NULL AND reserve_date IS NOT NULL))"
        
        if self.checkBox.isChecked() and self.checkBox_2.isChecked() and self.checkBox_5.isChecked():
            prov_spis = "AND ((finish_date IS NULL AND reserve_date IS NULL) OR finish_date IS NOT NULL OR reserve_date IS NOT NULL)"
        
        if not self.checkBox.isChecked() and self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            prov_spis = "AND (finish_date IS NOT NULL AND reserve_date IS NULL)"
        
        if not self.checkBox.isChecked() and not self.checkBox_2.isChecked() and self.checkBox_5.isChecked():
            prov_spis = "AND (finish_date IS NULL AND reserve_date IS NOT NULL)"
        
        if not self.checkBox.isChecked() and self.checkBox_2.isChecked() and self.checkBox_5.isChecked():
            prov_spis = "AND (finish_date IS NOT NULL OR reserve_date IS NOT NULL)"
        
        query9 = QSqlQuery(db)
        
        if id_msr != -1:
            
#COMMENT ON COLUMN zav_msr.type IS 'Назначение прибора: 1 - эталонное СИ, 2 - вспомогательное оборудование';
            
                                          
            query9.prepare(u"""SELECT id, id_msr, zav_num, inv_num, first_checking, start_date,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, finish_date, reserve_date, type            
FROM zav_msr WHERE id_msr=:ID """ + prov_spis + """ ORDER BY zav_num""")
            query9.bindValue(":id", id_msr)            
        else:            
            if self.checkBox_4.isChecked():

                # Новый вариант с средствами защиты
                SQL = """
SELECT id, id_msr, inv_num,  first_checking, start_date, finish_date, reserve_date FROM
(
SELECT t1.id, t1.id_msr, t1.zav_num, t1.inv_num, t1.first_checking, t1.start_date, t1.finish_date, t1.reserve_date t5.id_category,
t2.checking_date,
t3.name_msr, t3.period, t3.period_view,
t4.name_group,
CASE WHEN (t2.checking_date IS NULL) THEN t1.first_checking ELSE t2.checking_date END AS last_checking_date,
CASE WHEN (t2.view_date IS NULL) THEN t1.first_checking ELSE t2.view_date END AS last_view_date,
AGE(timestamp '""" + self.dateEdit.date().toString("yyyy-MM-dd") + """', CASE WHEN (t2.checking_date IS NULL) THEN t1.first_checking ELSE t2.checking_date END) AS period_age,
AGE(timestamp '""" + self.dateEdit.date().toString("yyyy-MM-dd") + """', CASE WHEN (t2.view_date IS NULL) THEN t1.first_checking ELSE t2.view_date END) AS view_period_age
FROM
zav_msr t1 LEFT OUTER JOIN 
(
  select id_zav, MAX(checking_date) AS checking_date, MAX(view_date) AS view_date 
  FROM journal_checking GROUP BY id_zav
) t2
ON (t1.id = t2.id_zav),
msr t3,
group_msr t4,
type_msr t5
WHERE t1.id_msr = t3.id
AND t3.id_group = t4.id
AND t4.id_type = t5.id
AND finish_date IS NULL
) AS t
WHERE
(
  t.id_category = 1 and
  (last_checking_date IS NULL OR 12 * EXTRACT(YEAR FROM period_age) + EXTRACT(MONTH FROM period_age) > period - 1)
) OR
(
  t.id_category = 2 and
  (
    (last_checking_date IS NULL OR 12 * EXTRACT(YEAR FROM period_age) + EXTRACT(MONTH FROM period_age) > period - 1) or
    (last_view_date IS NULL OR 12 * EXTRACT(YEAR FROM view_period_age) + EXTRACT(MONTH FROM view_period_age) > period_view - 1)
  )
)
ORDER BY zav_num
"""
                            
                query9.prepare(SQL)

            else:
                if zav_num == "":
                    query9.prepare("""SELECT id, id_msr, zav_num, first_checking, start_date, finish_date, reserve_date
                                      FROM zav_msr WHERE true """ + prov_spis + """ ORDER BY zav_num""")
                else:
                    query9.prepare("""SELECT id, id_msr, zav_num, first_checking, start_date, finish_date, reserve_date
                                      FROM zav_msr WHERE zav_num LIKE :zav_num """ + prov_spis + """ ORDER BY zav_num""")
                    query9.bindValue(":zav_num", zav_num + "%")
                
        query9.exec_()        
        
        model4.clear()        
        model4.reset()        
        model3.clear()        
        model3.reset()        
        model2.clear()        
        model2.setQuery(query9)

        model2.setHeaderData(2, QtCore.Qt.Horizontal, u"Заводской\nномер")
        model2.setHeaderData(3, QtCore.Qt.Horizontal, u"Инв. №")
           
        if id_category == '1' or id_category == '2':
            model2.setHeaderData(4, QtCore.Qt.Horizontal, u"Дата первич.\nповерки")
        if id_category == '3':
            model2.setHeaderData(4, QtCore.Qt.Horizontal, u"Дата первич.\nаттестации")
        model2.setHeaderData(5, QtCore.Qt.Horizontal, u"Дата ввода\nв эксплуатацию")
        
        model2.setHeaderData(6, QtCore.Qt.Horizontal, u"Назначение")
        model2.setHeaderData(7, QtCore.Qt.Horizontal, u"Номер в\nГосреестре СИ")
        model2.setHeaderData(8, QtCore.Qt.Horizontal, u"Доп. сведения")
                
        model2.setHeaderData(9, QtCore.Qt.Horizontal, u"Дата списания")
        model2.setHeaderData(10, QtCore.Qt.Horizontal, u"Дата вывода\nна резерв/консервацию")

        if id_category == '1' or id_category == '2':
            self.tableView_2.setColumnHidden(7, False)        
        if id_category == '3':
            self.tableView_2.setColumnHidden(7, True)        

            
        self.tableView_2.setColumnHidden(0, True)        
        self.tableView_2.setColumnHidden(1, True)        
        self.tableView_2.setColumnHidden(11, True)        
        self.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
                
        self.searchInModel(id_search, self.tableView_2, model2)
        self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_7, self.pushButton_4, self.selModel2)
        self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_11, self.pushButton_8, self.selModel2) #????????


    def ViewJournalChecking(self, id_search, id_zav):
        
        selectJournalChecking = """SELECT t1.id, checking_date, view_date, sertificate, t1.firms_repair_msr, t2.name_firm, t1.fif,
t2.address, to_char(checking_date, 'dd.mm.yyyy') as checking_date_,
to_char(checking_date + '""" + self.period + """ month'::INTERVAL - '1 day'::INTERVAL, 'dd.mm.yyyy') as checking_date__
FROM journal_checking t1 LEFT OUTER JOIN firms_repair_msr t2 ON (t1.firms_repair_msr = t2.id)
WHERE id_zav=:ID
ORDER BY checking_date"""
        

        
        query9 = QSqlQuery(db)
        query9.prepare(selectJournalChecking)
        query9.bindValue(":id", id_zav)
        query9.exec_()        
        
        model3.clear()        
        model3.setQuery(query9)
        if id_category == '1' or id_category == '2':
            model3.setHeaderData(1, QtCore.Qt.Horizontal, u"Дата\nповерки")
            model3.setHeaderData(2, QtCore.Qt.Horizontal, u"Дата\nосмотра")
        if id_category == '3':
            model3.setHeaderData(1, QtCore.Qt.Horizontal, u"Дата\nпериодической\nаттестации")
            model3.setHeaderData(2, QtCore.Qt.Horizontal, u"Дата\nпоследнего\nпроведения\nППР")
        model3.setHeaderData(3, QtCore.Qt.Horizontal, u"Номер свидетельства\nо поверке")
        model3.setHeaderData(5, QtCore.Qt.Horizontal, u"Организация,\nпроводящая поверку")
        model3.setHeaderData(6, QtCore.Qt.Horizontal, u"Ссылка\nна ФИФ")
        self.tableView_3.setColumnHidden(0, True)
        self.tableView_3.setColumnHidden(4, True)
        
        
        
        
        if id_category == '1' or id_category == '2':
            self.tableView_3.setColumnHidden(6, False)        
        if id_category == '3':
            self.tableView_3.setColumnHidden(6, True)        
        
        
        
        self.tableView_3.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
         
        self.searchInModel(id_search, self.tableView_3, model3)
        self.viewButtons(2, self.pushButton_5, self.pushButton_6, self.pushButton_6, self.pushButton_6, self.selModel3)


    def ViewHistoryLocation(self, id_search, id_zav):
        query9 = QSqlQuery(db)
        query9.prepare(selectHistoryLocation)
        query9.bindValue(":id", id_zav)
        query9.exec_()        
        
        model5.clear()        
        model5.setQuery(query9)
        if id_category == '1' or id_category == '2':
            model5.setHeaderData(1, QtCore.Qt.Horizontal, u"Местонахождение")
        if id_category == '3':
            model5.setHeaderData(1, QtCore.Qt.Horizontal, u"Место установки ИО")
        model5.setHeaderData(2, QtCore.Qt.Horizontal, u"Дата перемещения")
        self.tableView_5.setColumnHidden(0, True) #????
        self.tableView_5.setColumnHidden(4, True) #????
        self.tableView_5.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
         
        self.searchInModel(id_search, self.tableView_5, model5)
        self.viewButtons(2, self.pushButton_9, self.pushButton_10, self.pushButton_10, self.pushButton_10, self.selModel5)


    # Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
    def searchInModel(self, id_search, tableView, model):
        #print 'id_search=', id_search
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


    def selectionChangedTree(self):
        self.ViewMsr(0)        

    def selectionChanged1(self):
        global id_msr
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        

        self.name_group = "'" +  unicode(model.record(row).field('name_group').value().toString()) + "'"
        self.period = model.record(row).field('period').value().toString()
        
        id_msr = model.record(row).field('id').value().toString()
                        
        SQL1 = """select name_group, name_msr, group_msr.id as id_group, msr.id as id_msr
                  from group_msr, msr
                  where group_msr.id = msr.id_group
                  and msr.id = :id_msr"""
        query1 = QSqlQuery(db)
        query1.prepare(SQL1)
        query1.bindValue(":id_msr", id_msr);
        query1.exec_()
        query1.next()
        self.lineEdit_2.setText(query1.value(0).toString())
        
        self.lineEdit_3.setText(model.record(row).field('name_msr').value().toString())
        self.name_msr = "'" + unicode(model.record(row).field('name_msr').value().toString()) + "'"
                        
        if not self.checkBox_3.isChecked() and not self.checkBox_4.isChecked():   
            self.ViewZavMsr(0, id_msr, None)
        self.ViewAccuracy(id_msr)

                 
    def selectionChanged2(self):
        global id_zav, tempDate        
        row = self.selModel2.currentIndex().row()
        if row == -1:
            return
        id_zav = model2.record(row).field('id').value().toString()  
        
        self.zav_num = "'" + unicode(model2.record(row).field('zav_num').value().toString()) + "'"
        self.inv_num = "'" + unicode(model2.record(row).field('inv_num').value().toString()) + "'"
                 
        tempDate = model2.record(row).field('first_checking').value().toDate()
        self.ViewJournalChecking(0, id_zav)
        self.ViewHistoryLocation(0, id_zav) #?
        
        SQL1 = """select name_group, name_msr, group_msr.id as id_group, msr.id as id_msr
                  from group_msr, msr
                  where group_msr.id = msr.id_group
                  and msr.id = :id_msr"""
        query1 = QSqlQuery(db)
        query1.prepare(SQL1)
        query1.bindValue(":id_msr", model2.record(row).field('id_msr').value().toString());
        query1.exec_()
        query1.next()
        self.lineEdit_2.setText(query1.value(0).toString())
        self.lineEdit_2.setCursorPosition(0)
        self.lineEdit_2.setStyleSheet("color: blue; background-color: lightgray")
        self.lineEdit_3.setText(query1.value(1).toString())
        self.lineEdit_3.setCursorPosition(0)
        self.lineEdit_3.setStyleSheet("color: blue; background-color: lightgray")
        self.lineEdit_4.setText(model2.record(row).field('zav_num').value().toString())
        self.lineEdit_4.setCursorPosition(0)
        self.lineEdit_4.setStyleSheet("color: blue; background-color: lightgray")
        self.lineEdit_5.setVisible(False) 

        if self.checkBox_3.isChecked() or self.checkBox_4.isChecked() :
            # поиск в дереве
            for e in range(2):
                for i in range(modelTree.item(e).rowCount()):
                    for j in range(modelTree.item(e).child(i).rowCount()):
                        if query1.value(2).toString() == modelTree.item(e).child(i).child(j).data().toString():
                            self.treeView.setCurrentIndex(modelTree.indexFromItem(modelTree.item(e).child(i).child(j)))

            # поиск в средствах измерения
            self.searchInModel(query1.value(3).toString(), self.tableView, model)
         
    def selectionChanged3(self):
        global id_journal        
        row = self.selModel3.currentIndex().row()
        if row == -1:
            return
        id_journal = model3.record(row).field('id').value().toString()   
#        self.checking_date = "'" +  model3.record(row).field('checking_date').value().toString() + "'"   
        self.checking_date = str( "'" +  model3.record(row).field('checking_date__').value().toString() + "'")   
#        self.checking_date = "'" +  model3.record(row).field('sertificate').value().toString() + "'"   
        self.sertificate = "'" +  unicode(model3.record(row).field('sertificate').value().toString()) + "'"   
#        self.fif = "'" +  unicode(model3.record(row).field('fif').value().toString()) + "'"   
        self.fif = unicode(model3.record(row).field('fif').value().toString())   

#        self.name_group = "'" +  unicode(model.record(row).field('name_group').value().toString()) + "'"


    def selectionChanged5(self):
        #return #
    
        global id_history_location        
        row = self.selModel5.currentIndex().row()
        if row == -1:
            return
        id_history_location = model5.record(row).field('id').value().toString()   


    def checkBox_Toggle(self, check):
        if not check and not self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            self.checkBox_2.setChecked(True)
            
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(0, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(0, id_msr, None)

    def checkBox_2_Toggle(self, check):
        if not check and not self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            self.checkBox.setChecked(True)
            
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(0, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(0, id_msr, None)

    def checkBox_5_Toggle(self, check):
        if not check and not self.checkBox_2.isChecked() and not self.checkBox_5.isChecked():
            self.checkBox.setChecked(True)
            
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(0, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(0, id_msr, None)


    def checkBox_3_Toggle(self, check):
        self.lineEdit.setEnabled(check)        
        self.checkBox_4.setEnabled(not check)
        self.treeView.setEnabled(not check)
        self.tableView.setEnabled(not check)
        self.tableView_4.setEnabled(not check)
        if check:            
            self.ViewZavMsr(0, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(0, id_msr, None)

    def lineEdit_textChanged(self):
        self.ViewZavMsr(0, -1, self.lineEdit.text())

    def checkBox_4_Toggle(self, check):
        self.dateEdit.setEnabled(check)
        self.checkBox.setEnabled(not check)
        self.checkBox_2.setEnabled(not check)
        self.checkBox_3.setEnabled(not check)
        self.treeView.setEnabled(not check)
        self.tableView.setEnabled(not check)
        self.tableView_4.setEnabled(not check)
        if check:
            self.ViewZavMsr(0, -1, None)
        else:
            self.ViewZavMsr(0, id_msr, None)

    def dateEdit_textChanged(self):
        self.ViewZavMsr(0, -1, None)


# Редактирование заводских номеров (начало кода)        
        
    def warn1(self):
        if self.checkBox_4.isChecked():
            QMessageBox.warning(self, u"Предупреждение", u"Отключи фильтр по средствам измерения, которые необходимо поверить!", QMessageBox.Ok)
            return True
        else:
            return False          
                
    def pushButton_Click(self):       
        if not self.checkBox.isChecked():
            QMessageBox.warning(self, u"Предупреждение", u"Установи галочку 'Рабочие средства измерения'!", QMessageBox.Ok)
            return        
        if self.warn1():
            return        
        self.wind1 = self.editZav()
        if self.wind1.tag == 0:
            return
                        
        self.wind1.setWindowTitle(u'Добавление нового заводского номера')
        self.wind1.label_4.setVisible(False)        
        self.wind1.dateEdit_3.setVisible(False)        
        self.wind1.exec_()
        if self.checkBox_3.isChecked() or self.checkBox_4.isChecked():
            self.lineEdit.textChanged.disconnect(self.lineEdit_textChanged)
            self.lineEdit.setText("")
            self.lineEdit.textChanged.connect(self.lineEdit_textChanged)
            self.ViewZavMsr(id_zav, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(id_zav, id_msr, None)

                
    def pushButton2_Click(self):
        
        if self.warn1():
            return
        if model3.rowCount() > 0:
            QMessageBox.warning(self, u"Предупреждение", u"Удаление текущей позиции невозможно,\n\r поскольку она содержит плановые поверки!", QMessageBox.Ok)
            return
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db)
            query.prepare("DELETE FROM zav_msr WHERE id = :ID")
            row = self.selModel2.currentIndex().row()                
            query.bindValue(":id", model2.record(row).field('id').value().toString());
            query.exec_()

            if self.checkBox_3.isChecked() or self.checkBox_4.isChecked():
                self.ViewZavMsr(-1, -1, self.lineEdit.text())
            else:    
                self.ViewZavMsr(-1, id_msr, None)

            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_2.selectRow(row)                                    
            self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_7, self.pushButton_4, self.selModel2)
            
    def pushButton3_Click(self):
        if self.warn1():
            return
        global id_zav, id_msr    #, name_type
        self.wind1 = self.editZav()
        if self.wind1.tag == 0:
            return
        self.wind1.tag = 2
        self.wind1.setWindowTitle(u'Редактирование текущего заводского номера')
        self.wind1.label_4.setVisible(False)        
        self.wind1.dateEdit_3.setVisible(False)        
        row = self.selModel2.currentIndex().row()
        self.wind1.lineEdit.setText(model2.record(row).field('zav_num').value().toString())
        self.wind1.lineEdit_4.setText(model2.record(row).field('inv_num').value().toString())
        self.wind1.dateEdit.setDate(model2.record(row).field('first_checking').value().toDate())
        self.wind1.dateEdit_2.setDate(model2.record(row).field('start_date').value().toDate())
        
        if model2.record(row).field('type').value().toString() == '1':
            self.wind1.checkBox.setChecked(True)
        if model2.record(row).field('type').value().toString() == '2':
            self.wind1.checkBox_2.setChecked(True)
                       
#        if self.wind1.checkBox.isChecked():
#            self.wind1.checkBox.setChecked(True)
#        if self.wind1.checkBox_2.isChecked():
#            self.wind1.checkBox_2.setChecked(True)
                       
#        QtGui.QCheckBox.setChecked()
        
        self.wind1.lineEdit_2.setText(model2.record(row).field('num_gosreestr').value().toString())
        self.wind1.lineEdit_3.setText(model2.record(row).field('comment').value().toString())
        
        self.wind1.exec_()
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(id_zav, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(id_zav, id_msr, None)

                        
    class editZav(QDialog):
        def __init__(self, *args):
            QDialog.__init__(self, *args)

            if not MyLoadUi(path_ui, "editZav.ui", self):
                return

            self.dateEdit.setCalendarPopup(1)
            self.dateEdit_2.setCalendarPopup(1)
            
            self.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))

            self.checkBox.toggled.connect(self.checkBox_Toggle)
            self.checkBox_2.toggled.connect(self.checkBox_Toggle)
                        
            if id_category == '1' or id_category == '2':
                self.label_5.setVisible(True)            
                self.lineEdit_2.setVisible(True)            
            if id_category == '3':
                self.label_5.setVisible(False)            
                self.lineEdit_2.setVisible(False)            
                        
            self.pushButton.clicked.connect(self.pushButton1_Click)
        
        
        def checkBox_Toggle(self, check):            
            if self.sender() == self.checkBox:
                if check and self.checkBox_2.isChecked():
                    self.checkBox_2.setChecked(False)
            if self.sender() == self.checkBox_2:
                if check and self.checkBox.isChecked():
                    self.checkBox.setChecked(False)        
        
        def pushButton1_Click(self):
            if self.lineEdit.text().trimmed() == "":
                QMessageBox.warning(self, u"Предупреждение", u"Введите заводской номер", QMessageBox.Ok)
                self.lineEdit.setFocus(True)
                return
                
            global id_zav            
            query = QSqlQuery(db)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM zav_msr");
                query.exec_()
                query.next()
                id_zav = query.value(0).toString()
                query.prepare("INSERT INTO zav_msr (id_msr, zav_num, inv_num, first_checking, start_date, type, num_gosreestr, comment, id) VALUES (:id_msr, :zav_num, :inv_num, :first_checking, :start_date, :type, :num_gosreestr, :comment, :id)")
            else:
                query.prepare("UPDATE zav_msr SET id_msr = :id_msr, zav_num = :zav_num, inv_num = :inv_num, first_checking = :first_checking, start_date = :start_date, type = :type, num_gosreestr = :num_gosreestr, comment = :comment WHERE id = :id")
            query.bindValue(":id", id_zav);
            query.bindValue(":id_msr", id_msr);
            query.bindValue(":zav_num", self.lineEdit.text())
            query.bindValue(":inv_num", self.lineEdit_4.text())
            if self.dateEdit.date() > datetime.date(2000, 1, 1):
                query.bindValue(":first_checking", self.dateEdit.date())
            if self.dateEdit_2.date() > datetime.date(2000, 1, 1):
                query.bindValue(":start_date", self.dateEdit_2.date())
            if self.dateEdit_3.date() > datetime.date(2000, 1, 1):
                query.bindValue(":finish_date", self.dateEdit_3.date())
 
            query.bindValue(":type", None)
            if self.checkBox.isChecked():
                query.bindValue(":type", 1)
            if self.checkBox_2.isChecked():
                query.bindValue(":type", 2)
 
            query.bindValue(":num_gosreestr", self.lineEdit_2.text())
            query.bindValue(":comment", self.lineEdit_3.text())
 
 
#ALTER TABLE zav_msr ADD column type integer;
#ALTER TABLE zav_msr ADD column num_gosreestr character varying(10);
#ALTER TABLE zav_msr ADD column comment character varying(300);
 
                    
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
                id_zav = 0            
                                    
            self.close()
            
# Редактирование заводских номеров (конец кода)        

# Редактирование списания (начало кода)
        
    def pushButton7_Click(self):
        if self.warn1():
            return
        
        if not self.checkBox_2.isChecked():
            QMessageBox.warning(self, u"Предупреждение", u"Для списания необходимо в условиях фильтра\nвключить: списанные средства измерения", QMessageBox.Ok)
            self.checkBox_2.setFocus(True)
            return
        global id_zav, id_msr    #, name_type
        self.wind1 = self.editDeregist()
        if self.wind1.tag == 0:
            return
                
        row = self.selModel2.currentIndex().row()        

        if model2.record(row).field('reserve_date').value().toDate().toString() != "":
            QMessageBox.warning(self, u"Предупреждение", u"Выведенное на резерв\консервацию средство измерения,\nневозможно списать!", QMessageBox.Ok)
            return
        
        if model2.record(row).field('finish_date').value().toDate().toString() == "":
            self.wind1.dateEdit.setDate(datetime.date.today())
            self.wind1.checkBox.setEnabled(False)
        else:    
            self.wind1.dateEdit.setDate(model2.record(row).field('finish_date').value().toDate())
        self.wind1.exec_()
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(id_zav, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(id_zav, id_msr, None)

    class editDeregist(QDialog):
        def __init__(self, *args):
            QDialog.__init__(self, *args)
                        
            if not MyLoadUi(path_ui, "editDeregist.ui", self):
                return
                        
            self.dateEdit.setCalendarPopup(1)
            
            self.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.checkBox.toggled.connect(self.checkBox_Toggle)

        
        def pushButton1_Click(self):
            if self.dateEdit.date() <= datetime.date(2000, 1, 1) and self.checkBox.checkState() == 0:
                QMessageBox.warning(self, u"Предупреждение", u"Введите правильно дату списания", QMessageBox.Ok)
                self.dateEdit.setFocus(True)
                return
                
            global id_zav            
            query = QSqlQuery(db)
            query.prepare("UPDATE zav_msr SET finish_date = :finish_date WHERE id = :id")
            

            
            if self.checkBox.checkState() == 0:
                query.bindValue(":finish_date", self.dateEdit.date())
            query.bindValue(":id", id_zav);
                    
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
                id_zav = 0            
                                    
            self.close()

        def checkBox_Toggle(self, check):
            self.label.setEnabled(not check)
            self.dateEdit.setEnabled(not check)


# Редактирование списания (конец кода)




# Редактирование резерва/консервации (начало кода)
        
    def pushButton11_Click(self):
        if self.warn1():
            return
        
        if not self.checkBox_5.isChecked():
            QMessageBox.warning(self, u"Предупреждение", u"Для вывода на резерв/консервацию необходимо в условиях фильтра\nвключить: выведены на резерв/консервацию средства измерения", QMessageBox.Ok)
            self.checkBox_5.setFocus(True)
            return
        global id_zav, id_msr    #, name_type
        self.wind1 = self.editReserve()
        if self.wind1.tag == 0:
            return
                
        row = self.selModel2.currentIndex().row()
                
        if model2.record(row).field('finish_date').value().toDate().toString() != "":
            QMessageBox.warning(self, u"Предупреждение", u"Списанное средство измерения,\nневозможно вывести на резерв\консервацию!", QMessageBox.Ok)
            return
        
        if model2.record(row).field('reserve_date').value().toDate().toString() == "":
            self.wind1.dateEdit.setDate(datetime.date.today())
            self.wind1.checkBox.setEnabled(False)
        else:    
            self.wind1.dateEdit.setDate(model2.record(row).field('reserve_date').value().toDate())
        self.wind1.exec_()
        if self.checkBox_3.isChecked():
            self.ViewZavMsr(id_zav, -1, self.lineEdit.text())
        else:    
            self.ViewZavMsr(id_zav, id_msr, None)

    class editReserve(QDialog):
        def __init__(self, *args):
            QDialog.__init__(self, *args)
                        
            if not MyLoadUi(path_ui, "editDeregist.ui", self):
                return
                        
            self.dateEdit.setCalendarPopup(1)
            
            self.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.checkBox.toggled.connect(self.checkBox_Toggle)
        
            self.setWindowTitle(u'Вывод средства измерения на резерв/консервацию')
            self.label.setText(u'Дата вывода на резерв/консервацию')
            self.checkBox.setText(u'Аннулировать вывод на резерв/консервацию')
                
        
        def pushButton1_Click(self):

            if self.dateEdit.date() <= datetime.date(2000, 1, 1) and self.checkBox.checkState() == 0:
                QMessageBox.warning(self, u"Предупреждение", u"Введите правильно дату вывода средства измерения на резерв/консервацию", QMessageBox.Ok)
                self.dateEdit.setFocus(True)
                return
                         
            global id_zav            
            query = QSqlQuery(db)
            query.prepare("UPDATE zav_msr SET reserve_date = :reserve_date WHERE id = :id")
            if self.checkBox.checkState() == 0:
                query.bindValue(":reserve_date", self.dateEdit.date())
            query.bindValue(":id", id_zav)
                    
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
                id_zav = 0            
                                    
            self.close()

        def checkBox_Toggle(self, check):
            self.label.setEnabled(not check)
            self.dateEdit.setEnabled(not check)

# Редактирование резерва/консервации (конец кода)



# Редактирование журнала поверки (начало кода)        
              
    def pushButton4_Click(self):
        global id_journal, id_zav
        self.wind2 = self.editJournal()
        if self.wind2.tag == 0:
            return
        
        self.wind2.setWindowTitle(u'Добавление новой поверки')
        self.wind2.dateEdit.setDate(datetime.date.today())        
        self.wind2.dateEdit_2.setDate(datetime.date.today())        
        self.wind2.exec_()
        self.ViewJournalChecking(id_journal, id_zav)

                
    def pushButton5_Click(self):        
        global id_zav
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db)
            query.prepare("DELETE FROM journal_checking WHERE id = :ID")
            row = self.selModel3.currentIndex().row()                
            query.bindValue(":id", model3.record(row).field('id').value().toString());
            query.exec_()
            self.ViewJournalChecking(-1, id_zav)

            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_3.selectRow(row)                                    
            self.viewButtons(2, self.pushButton_5, self.pushButton_6, self.pushButton_6, self.pushButton_6, self.selModel3)
            
    def pushButton6_Click(self):
        global id_journal, id_zav    #, name_type
        self.wind2 = self.editJournal()
        if self.wind2.tag == 0:
            return
        self.wind2.tag = 2
        self.wind2.setWindowTitle(u'Редактирование текущей поверки')
        row = self.selModel3.currentIndex().row()
        self.wind2.lineEdit.setText(model3.record(row).field('sertificate').value().toString())
        self.wind2.lineEdit_2.Tag = model3.record(row).field('firms_repair_msr').value().toString()
        self.wind2.lineEdit_2.setText(model3.record(row).field('name_firm').value().toString())
        self.wind2.dateEdit.setDate(model3.record(row).field('checking_date').value().toDate())
        self.wind2.dateEdit_2.setDate(model3.record(row).field('view_date').value().toDate())
        self.wind2.lineEdit_3.setText(model3.record(row).field('fif').value().toString())
        self.wind2.exec_()
        self.ViewJournalChecking(id_journal, id_zav)
                        
                        
    def pushButton12_Click(self):
        try:
            
            os.system(self.CurDir_ + '/qrCode.exe ' + '"' + self.fif + '"')
###            os.system(self.CurDir_ + '/qrCode.exe ' + self.fif)


            inputParms = {u'name_group':self.name_group, u'zav_num':self.zav_num, u'name_msr':self.name_msr, u'inv_num':self.inv_num, u'checking_date':self.checking_date, u'sertificate':self.sertificate, u'curdir':"'" + self.CurDir + "'"}
            rpt = FRPrintForm(u'ReportStickersMsr.fr3', inputParms, env)
            rpt.preview()
        except:
            pass
    
                                                    
    class editJournal(QDialog):
        def __init__(self, *args):
            QDialog.__init__(self, *args)
            if not MyLoadUi(path_ui, "editJournal.ui", self):
                return
                        
            self.dateEdit.setCalendarPopup(1)
            self.dateEdit_2.setCalendarPopup(1)
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.pushButton_3.clicked.connect(self.pushButton3_Click)
            
            self.checkBox.toggled.connect(self.checkBox_Toggle)
            
            self.label_3.setVisible(id_category == '2' or id_category == '3')
            self.dateEdit_2.setVisible(id_category == '2' or id_category == '3')
            self.checkBox.setVisible(id_category == '2' or id_category == '3')
            
            
            if id_category == '1' or id_category == '2':
                self.label.setText(u'Дата поверки')
                self.label_3.setText(u'Дата осмотра')
            if id_category == '3':
                self.label.setText(u'Дата периодической аттестации')
                self.label_3.setText(u'Дата последнего проведения ППР')
            
            
            
        
        
        def pushButton1_Click(self):

            if id_category == '1':
                if self.dateEdit.date() <= datetime.date(2000, 1, 1):
                    QMessageBox.warning(self, u"Предупреждение", u"Введите корректную дату поверки", QMessageBox.Ok)
                    self.dateEdit.setFocus(True)
                    return
                        
            if id_category == '2':
                if (self.dateEdit.date() <= datetime.date(2000, 1, 1) and
                    self.dateEdit_2.date() <= datetime.date(2000, 1, 1)):
                    QMessageBox.warning(self, u"Предупреждение", u"Введите корректную дату поверки/осмотра", QMessageBox.Ok)
                    self.dateEdit.setFocus(True)
                    return
                if (self.dateEdit.date() > datetime.date(2000, 1, 1) and
                    self.dateEdit.date() != self.dateEdit_2.date()):
                    QMessageBox.warning(self, u"Предупреждение", u"Даты поверки и осмотра должны совпадать в данной ситуации", QMessageBox.Ok)
                    self.dateEdit.setFocus(True)
                    return
                        
            if self.lineEdit_2.text() == '':
                QMessageBox.warning(self, u"Предупреждение", u"Введите организацию", QMessageBox.Ok)
                self.pushButton_3.setFocus(True)
                return                        
                        
            global id_journal
            query = QSqlQuery(db)
                        
            if self.tag == 1:
                # Проверка на превышение последней даты поверки
                SQL = """SELECT MAX(checking_date) AS max_checking_date, MAX(view_date) AS max_view_date 
                         FROM journal_checking WHERE id_zav = """ + id_zav
                query.prepare(SQL);
                query.exec_()
                query.next()

                if id_category == '1':
                    if self.dateEdit.date() <= max(tempDate, query.value(0).toDate()):
                        QMessageBox.warning(self, u"Предупреждение", u"Дата текущей поверки должна превышать дату предыдущей поверки", QMessageBox.Ok)
                        self.dateEdit.setFocus(True)
                        return            
                            
                if id_category == '2':
                    if self.dateEdit.date() <= datetime.date(2000, 1, 1):
                        if self.dateEdit_2.date() <= max(tempDate, query.value(1).toDate()):
                            QMessageBox.warning(self, u"Предупреждение", u"Дата текущей осмотра должна превышать дату предыдущей осмотра", QMessageBox.Ok)
                            self.dateEdit.setFocus(True)
                            return            
                    if self.dateEdit.date() > datetime.date(2000, 1, 1):
                        if (self.dateEdit.date() <= max(tempDate, query.value(0).toDate()) or
                            self.dateEdit_2.date() <= max(tempDate, query.value(1).toDate())):
                            QMessageBox.warning(self, u"Предупреждение", u"Дата текущей поверки/осмотра должна превышать дату предыдущей поверки/осмотра", QMessageBox.Ok)
                            self.dateEdit.setFocus(True)
                            return            
                            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM journal_checking");
                query.exec_()
                query.next()
                id_journal = query.value(0).toString()
                query.prepare("INSERT INTO journal_checking (id, id_zav, checking_date, view_date, sertificate, firms_repair_msr, fif) VALUES (:id, :id_zav, :checking_date, :view_date, :sertificate, :firms_repair_msr, :fif)")
            else:
                query.prepare("UPDATE journal_checking SET id_zav = :id_zav, checking_date = :checking_date, view_date = :view_date, sertificate = :sertificate, firms_repair_msr = :firms_repair_msr, fif = :fif WHERE id = :id")
            query.bindValue(":id", id_journal);
            query.bindValue(":id_zav", id_zav);
            if self.dateEdit.date() > datetime.date(2000, 1, 1):
                query.bindValue(":checking_date", self.dateEdit.date())
            if self.dateEdit_2.date() > datetime.date(2000, 1, 1):
                query.bindValue(":view_date", self.dateEdit_2.date())
            
            query.bindValue(":sertificate", self.lineEdit.text())
            query.bindValue(":firms_repair_msr", self.lineEdit_2.Tag)            
            query.bindValue(":fif", self.lineEdit_3.text())
            
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
                return            
                                    
            self.close()

        def pushButton3_Click(self):
            pass
            from firms_repair_msr import FirmRepair
            wind = FirmRepair(env)
            if wind.tag != 0:
                wind.setWindowTitle(u'Организации, проводящие поверку/калибровку/ремонт СИ');            
                # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
                # Бред какой-то        
                wind.show()
                wind.resizeEvent(None)
                wind.close()                
                wind.exec_()                
                if wind.id != '':
                    self.lineEdit_2.Tag = wind.id
                    self.lineEdit_2.setText(wind.name_firm)
        
        def checkBox_Toggle(self, check):
            if check:
                self.dateEdit.setDate(datetime.date(2000, 1, 1))        
            else:
                self.dateEdit.setDate(self.dateEdit_2.date())        

            
# Редактирование журнала поверки (конец кода)        



# Редактирование истории перемещения (начало кода)        
              
    def pushButton8_Click(self):
        #return
    
        global id_history_location, id_zav
        self.wind3 = self.editHistoryLocation()
        if self.wind3.tag == 0:
            return
        
        self.wind3.setWindowTitle(u'Добавление нового местонахождения')
        self.wind3.dateEdit.setDate(datetime.date.today())        
        self.wind3.exec_()
        self.ViewHistoryLocation(id_history_location, id_zav)

                
    def pushButton9_Click(self):
        #return
            
        global id_zav
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db)
            query.prepare("DELETE FROM history_location_msr WHERE id = :ID")
            row = self.selModel5.currentIndex().row()                
            query.bindValue(":id", model5.record(row).field('id').value().toString());
            query.exec_()
            self.ViewHistoryLocation(-1, id_zav)

            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_5.selectRow(row)                                    
            self.viewButtons(2, self.pushButton_9, self.pushButton_10, self.pushButton_10, self.pushButton_10, self.selModel5)
            
    def pushButton10_Click(self):
        
        global id_history_location, id_zav    #, name_type
        self.wind3 = self.editHistoryLocation()
        if self.wind3.tag == 0:
            return
        self.wind3.tag = 2
        self.wind3.setWindowTitle(u'Редактирование текущего местонахождения')
        row = self.selModel5.currentIndex().row()
        self.wind3.lineEdit.Tag = model5.record(row).field('location_msr').value().toString()
        self.wind3.lineEdit.setText(model5.record(row).field('name_location').value().toString())
        self.wind3.dateEdit.setDate(model5.record(row).field('date_move').value().toDate())
        self.wind3.exec_()
        self.ViewHistoryLocation(id_history_location, id_zav)
                        
                        
                        
                                                
    class editHistoryLocation(QDialog):
        def __init__(self, *args):
            QDialog.__init__(self, *args)
            if not MyLoadUi(path_ui, "editHistoryLocation.ui", self):
                return
                        
            self.dateEdit.setCalendarPopup(1)
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.pushButton_3.clicked.connect(self.pushButton3_Click)
        
            if id_category == '1' or id_category == '2':
                self.label_4.setText(u'Местонахождения')
            if id_category == '3':
                self.label_4.setText(u'Место установки ИО')



        
        def pushButton1_Click(self):
#            print 'self.lineEdit.Tag111=', self.lineEdit.Tag

            if self.dateEdit.date() <= datetime.date(2000, 1, 1):
                QMessageBox.warning(self, u"Предупреждение", u"Введите корректную дату поверки", QMessageBox.Ok)
                self.dateEdit.setFocus(True)
                return
                                                
            global id_history_location
            query = QSqlQuery(db)
                        
            if self.tag == 1:
                # Проверка на превышение последней даты перемещения
                SQL = """SELECT MAX(date_move) AS max_date_move 
                         FROM history_location_msr WHERE id_zav = """ + id_zav
                query.prepare(SQL);
                query.exec_()
                query.next()

                if self.dateEdit.date() < max(tempDate, query.value(0).toDate()):
                    QMessageBox.warning(self, u"Предупреждение", u"Дата текущего перемещения не должна быть меньше даты предыдущего перемещения", QMessageBox.Ok)
                    self.dateEdit.setFocus(True)
                    return            
                            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM history_location_msr");
                query.exec_()
                query.next()
                id_history_location = query.value(0).toString()
                query.prepare("INSERT INTO history_location_msr (id, zav_msr, location_msr, date_move) VALUES (:id, :id_zav, :location_msr, :date_move)")
            else:
                query.prepare("UPDATE history_location_msr SET zav_msr = :id_zav, location_msr = :location_msr, date_move = :date_move WHERE id = :id")
            query.bindValue(":id", id_history_location);
            query.bindValue(":id_zav", id_zav);
       #     print 'self.lineEdit.Tag=', self.lineEdit.Tag
            query.bindValue(":location_msr", self.lineEdit.Tag)
            if self.dateEdit.date() > datetime.date(2000, 1, 1):
                query.bindValue(":date_move", self.dateEdit.date())
                                    
                        
            if not query.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)            
                                    
            self.close()


        def pushButton3_Click(self):
            from location_msr import Location
            wind = Location(env)
            if wind.tag != 0:
                wind.setWindowTitle(u'Местонахождения средств измерения')            
#                wind.pushButton_4.setEnabled(False)
                 # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
                 # Бред какой-то        
                wind.show()
                wind.resizeEvent(None)
                wind.close()                
                wind.exec_()
                if wind.id != '':
                  #  print 333333333333333333333333333333
                    self.lineEdit.Tag = wind.id
                    self.lineEdit.setText(wind.name_location)

# Редактирование истории перемещения (конец кода)        






    def viewButtons(self, n, button1, button2, button3, button4, selModel):
        enab = selModel.currentIndex().row() >= 0
        button1.setEnabled(enab)
        button2.setEnabled(enab)
        button3.setEnabled(enab)
        button4.setEnabled(enab)
      #  button8.setEnabled(enab) #?????????
        
        if enab == False:
            if n < 2:
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_6.setEnabled(False)
                self.pushButton_8.setEnabled(False) #?
                self.pushButton_9.setEnabled(False) #?
                self.pushButton_10.setEnabled(False) #?

        if self.pushButton.isEnabled():                
            self.pushButton.setToolTip(u'добавить учетную запись')
        else:    
            self.pushButton.setToolTip(u'')
        if self.pushButton_3.isEnabled():                
            self.pushButton_3.setToolTip(u'редактировать учетную запись')
        else:    
            self.pushButton_3.setToolTip(u'')
        if self.pushButton_2.isEnabled():                
            self.pushButton_2.setToolTip(u'удалить учетную запись')
        else:    
            self.pushButton_2.setToolTip(u'')
        if self.pushButton_4.isEnabled():                
            self.pushButton_4.setToolTip(u'добавить поверку')
        else:    
            self.pushButton_4.setToolTip(u'')
        if self.pushButton_6.isEnabled():                
            self.pushButton_6.setToolTip(u'редактировать поверку')
        else:    
            self.pushButton_6.setToolTip(u'')
        if self.pushButton_5.isEnabled():                
            self.pushButton_5.setToolTip(u'удалить поверку')
        else:    
            self.pushButton_5.setToolTip(u'')
            
        if self.pushButton_8.isEnabled():                
            self.pushButton_8.setToolTip(u'добавить местонахождение')
        else:    
            self.pushButton_8.setToolTip(u'')
        if self.pushButton_9.isEnabled():                
            self.pushButton_9.setToolTip(u'редактировать местонахождение')
        else:    
            self.pushButton_9.setToolTip(u'')
        if self.pushButton_10.isEnabled():                
            self.pushButton_10.setToolTip(u'удалить местонахождение')
        else:    
            self.pushButton_10.setToolTip(u'')
            
            
        if self.pushButton_7.isEnabled():                
            self.pushButton_7.setToolTip(u'Списание средства измерения')
        else:    
            self.pushButton_7.setToolTip(u'')
        
        if self.pushButton_11.isEnabled():                
            self.pushButton_11.setToolTip(u'Вывести средство измерения в резерв/консервацию')
        else:
            self.pushButton_11.setToolTip(u'')

        self.pushButton_12.setEnabled(self.pushButton_6.isEnabled())       
        
        if self.pushButton_12.isEnabled():                
            self.pushButton_12.setToolTip(u'Печать этикетки')
        else:
            self.pushButton_12.setToolTip(u'')
        
        
        
        
        
    def widthArea(self, tableView):
        # Возвращает ширину свободной области таблицы tableView
        HSWidth = tableView.verticalHeader().width() + 4
        if tableView.verticalScrollBar().width() < 100 and tableView.verticalScrollBar().isVisible():
            HSWidth += tableView.verticalScrollBar().width()
        return tableView.width() - HSWidth    
    

    def TestBase(self):
        query = QSqlQuery(db)
        err_tbl = ""
        query = QSqlQuery(db)

#        query.prepare("select type, num_gosreestr, comment from zav_msr")
#        if not query.exec_(): err_tbl += "zav_msr\n"

        query.prepare("select inv_num from zav_msr")
        if not query.exec_(): err_tbl += "zav_msr\n"
       
        if err_tbl != "":
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
        query = QSqlQuery(db)


        SQL = u"""
ALTER TABLE zav_msr ADD column inv_num character varying(30);
COMMENT ON COLUMN zav_msr.inv_num IS 'Инвентарный номер';
ALTER TABLE journal_checking ALTER COLUMN sertificate TYPE varchar(30);
ALTER TABLE journal_checking ADD column fif character varying(100);
COMMENT ON COLUMN journal_checking.fif IS 'Ссылка на ФИФ';
ALTER TABLE accuracy_msr ALTER COLUMN range_msr TYPE varchar(60);
"""
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)
        return




        SQL = u"""
ALTER TABLE zav_msr ADD column type integer;
COMMENT ON COLUMN zav_msr.type IS 'Назначение прибора: 1 - эталонное СИ, 2 - вспомогательное оборудование';
ALTER TABLE zav_msr ADD column num_gosreestr character varying(10);
COMMENT ON COLUMN zav_msr.num_gosreestr IS 'Номер в Госреестре СИ';
ALTER TABLE zav_msr ADD column comment character varying(300);
COMMENT ON COLUMN zav_msr.comment IS 'Дополнительные сведения';
"""
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)
        return


        
        SQL = u"""
CREATE TABLE firms_repair_msr
(
  id serial PRIMARY KEY,
  name_firm character varying(30) NOT NULL,
  address character varying(100) NOT NULL
);
COMMENT ON TABLE firms_repair_msr IS 'Справочник организаций, проводящих поверку/калибровку/ремонт СИ';
COMMENT ON COLUMN firms_repair_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN firms_repair_msr.name_firm IS 'Наименование организации';
COMMENT ON COLUMN firms_repair_msr.address IS 'Адрес организации';
"""

        
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            pass
        
        SQL = u"""
CREATE TABLE location_msr
(
  id serial PRIMARY KEY,
  name_location character varying(30) NOT NULL
);
COMMENT ON TABLE location_msr IS 'Справочник местонахождений средств измерения';
COMMENT ON COLUMN location_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN location_msr.name_location IS 'Наименование местонахождения';
"""

        
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            pass

        
        SQL = u"""
CREATE TABLE history_location_msr
(
  id serial PRIMARY KEY,
  zav_msr integer REFERENCES zav_msr (id),
  location_msr integer REFERENCES location_msr (id),
  date_move date NOT NULL
--  date_move timestamp without time zone NOT NULL
);
COMMENT ON TABLE history_location_msr IS 'История перемещений средств измерения';
COMMENT ON COLUMN history_location_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN history_location_msr.zav_msr IS 'Ссылка на средство измерения';
COMMENT ON COLUMN history_location_msr.location_msr IS 'Ссылка на местонахождение средства измерения';
COMMENT ON COLUMN history_location_msr.date_move IS 'Дата перемещения';
"""

        
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            pass

        
        
        
        SQL = u"""
ALTER TABLE journal_checking ADD column firms_repair_msr integer REFERENCES firms_repair_msr (id);
COMMENT ON COLUMN journal_checking.firms_repair_msr IS 'Ссылка на таблицу организаций проводящих ремонт/поверку СИ';
"""
        if not query.exec_(SQL):

            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            pass
            #QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
    
    
        SQL = u"""
ALTER TABLE zav_msr ADD column reserve_date date;
COMMENT ON COLUMN zav_msr.reserve_date IS 'Дата вывода СИ на резерв\консервацию';
"""
        if not query.exec_(SQL):
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        
        
        
        return
        
            
        SQL = """
CREATE TABLE type_msr
(
  id serial PRIMARY KEY,
  name_type character varying(100) NOT NULL
);
COMMENT ON TABLE type_msr IS 'Справочник видов измерения';
COMMENT ON COLUMN type_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN type_msr.name_type IS 'Наименование вида';

CREATE TABLE group_msr
(
  id serial PRIMARY KEY,
  id_type integer REFERENCES type_msr,
  name_group character varying(200) NOT NULL
);
COMMENT ON TABLE group_msr IS 'Справочник групп средств измерения';
COMMENT ON COLUMN group_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN group_msr.id_type IS 'Внешний ключ к type_msr';
COMMENT ON COLUMN group_msr.name_group IS 'Наименование группы';

CREATE TABLE msr
(
  id serial PRIMARY KEY,
  id_group integer REFERENCES group_msr,
  name_msr character varying(200) NOT NULL,
  period integer CHECK (period > 0)
);
COMMENT ON TABLE msr IS 'Классификатор средств измерения';
COMMENT ON COLUMN msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN msr.id_group IS 'Внешний ключ к group_msr';
COMMENT ON COLUMN msr.name_msr IS 'Наименование, тип средства измерения';
COMMENT ON COLUMN msr.period IS 'Периодичность поверки';

CREATE TABLE accuracy_msr
(
  id serial PRIMARY KEY,
  id_msr integer REFERENCES msr,
  name_vid character varying(100),
  range_msr character varying(50),
  classaccuracy character varying(100)
);
COMMENT ON TABLE accuracy_msr IS 'Классы точности средств измерения';
COMMENT ON COLUMN accuracy_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN accuracy_msr.id_msr IS 'Внешний ключ к msr';
COMMENT ON COLUMN accuracy_msr.name_vid IS 'Вид измерения';
COMMENT ON COLUMN accuracy_msr.range_msr IS 'Диапазон измерения';
COMMENT ON COLUMN accuracy_msr.classaccuracy IS 'Класс точности';

CREATE TABLE zav_msr
(
  id serial PRIMARY KEY,
  id_msr integer REFERENCES msr,
  zav_num character varying(20),
  first_checking date,
  start_date date,
  finish_date date
);
COMMENT ON TABLE zav_msr IS 'Заводской справочник средств измерения';
COMMENT ON COLUMN zav_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN zav_msr.id_msr IS 'Внешний ключ к msr';
COMMENT ON COLUMN zav_msr.zav_num IS 'Заводской номер';
COMMENT ON COLUMN zav_msr.first_checking IS 'Дата первичной поверки';
COMMENT ON COLUMN zav_msr.start_date IS 'Дата ввода в эксплуатацию';
COMMENT ON COLUMN zav_msr.finish_date IS 'Дата списания';

CREATE TABLE journal_checking
(
  id serial PRIMARY KEY,
  id_zav integer REFERENCES zav_msr,
  checking_date date NOT NULL,
  sertificate character varying(20)
);
COMMENT ON TABLE journal_checking IS ' Журнал поверки средств измерения';
COMMENT ON COLUMN journal_checking.id IS 'Идентификатор записи';
COMMENT ON COLUMN journal_checking.id_zav IS 'Внешний ключ к zav_msr';
COMMENT ON COLUMN journal_checking.checking_date IS 'Дата поверки';
COMMENT ON COLUMN journal_checking.sertificate IS 'Номер свидетельства о поверке';
"""
        
        if not query.exec_(SQL):
            print("Ошибка инициализации")
        else:
            print("Инициализация выполнена!")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    from dpframe.base.inits import db_connection_init
    @json_config_init
    @db_connection_init
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
    db = env.db
    path_ui = env.config.paths.ui + "/"

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
        # Установка формата даты в БД
#        query = QSqlQuery(db)        
#        SQL = "set datestyle = 'ISO, DMY'"
#        if not query.exec_(SQL):
#            print "Ошибка SQL"
#        else:
#            print "SQL выполнено!"
                        
        wind = classJournal()
        if wind.is_show: 
            wind.show()
        sys.exit(app.exec_())


        

