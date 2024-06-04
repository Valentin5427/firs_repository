# -*- coding: UTF-8 -*-
#
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QModelIndex
#from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtGui import QMessageBox, QWidget, QDateEdit, QIcon, QCheckBox, QColor
from PyQt4.QtGui import QStandardItemModel, QStandardItem, QLineEdit
from electrolab.gui.common import UILoader
import sys
import datetime
import ui.ico_64_rc
import os


from ReportsMsr import *
from dpframe.base.inits import json_config_init

id_msr = ''
id_zav = ''
id_journal = ''
id_history_location = ''
tempDate = datetime.date.today()

modelTree = QStandardItemModel()
model = QSqlQueryModel()
model2 = QSqlQueryModel()

withCol1 = 200

withCol4 = 100
withCol5 = 100
withCol6 = 100
withCol61 = 100
withCol62 = 100
withCol63 = 100
withCol7 = 100                       
withCol71 = 100                       


VSB1 = False
VSB2 = False
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
        global VSB1, VSB2  #, VSB3, VSB4, VSB5
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
  #          koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3_))
            koef = (1.0 * (self.widthArea(obj)) / (withCol1))
            obj.setColumnWidth(1, koef * withCol1)
 #           obj.setColumnWidth(2, koef * withCol2)
 #           obj.setColumnWidth(3, koef * withCol3_)
            VSB1 = obj.verticalScrollBar().isVisible()
            
        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):        
            koef = (1.0 * (self.widthArea(obj)) / (withCol4 + withCol61 + withCol62 + withCol63))
            obj.setColumnWidth(2, koef * withCol4)
            
            obj.setColumnWidth(3, koef * withCol61)
            obj.setColumnWidth(4, koef * withCol62)
            obj.setColumnWidth(5, koef * withCol63)
                        
            VSB2 = obj.verticalScrollBar().isVisible()

        return False
    
'''                            
def MyLoadUi(UiDir, UiFile, wnd):
    try:
        print 1
        uidir = UiDir           
        if not os.path.exists(uidir + UiFile):        
            uidir = ""
        print 2, uidir + UiFile
            
        uic.loadUi(uidir + UiFile, wnd)
        print 3
        wnd.tag = 1
        return True
    except:    
        wnd.tag = 0
        QMessageBox.warning(None, u"Предупреждение", u"Проблемы с загрузкой файла: " + UiFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
        return False
'''
            
#class classJournal(QtGui.QMainWindow):
#    def __init__(self, *args):
#        QtGui.QDialog.__init__(self, *args)
        
class classJournal(QtGui.QDialog, UILoader):
    def __init__(self, _env, *args):
        QtGui.QDialog.__init__(self, *args)
        
        global db
        db = _env.db
                        
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"sprMsr.ui")
                
                
        self.resize(1000,600)
        self.ui.splitter.setStretchFactor(0,1)

        # Временно
        self.ui.lineEdit.setEnabled(False)
        self.is_show = True
         
        self.ui.checkBox_3.toggled.connect(self.checkBox_3_Toggle)
        self.ui.lineEdit.textChanged.connect(self.lineEdit_textChanged)
        
        self.ui.treeView.setModel(modelTree)        
        self.selModelTree = self.ui.treeView.selectionModel()        
        self.connect(self.selModelTree, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChangedTree)

        self.ui.tableView.setModel(model)
        self.selModel = self.ui.tableView.selectionModel()
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)
        
        self.ui.tableView_2.setModel(model2)
        self.selModel2 = self.ui.tableView_2.selectionModel()
        self.connect(self.selModel2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged2)

        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setObjectName('tv2')
                
        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))
        
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_Click)
        
        self.IS_SELECT = False
        self.ID_ZAV_MSR = None
        self.NAME_MSR = None
        self.ZAV_NUM = None
               
        self.FILTR1 = '''
(select t2.id_type 
from group_msr as t2, msr as t3, zav_msr as t4
where t2.id = t3.id_group
and t3.id = t4.id_msr
and t4.type is not null)
'''        
        self.FILTR2 = '''
(select t3.id_group
from msr as t3, zav_msr as t4
where t3.id = t4.id_msr
and t4.type is not null)
'''        
        self.FILTR3 = '''
(select t4.id_msr
from zav_msr as t4
where t4.type is not null)
'''        
        
        
        
        
        self.FillTree()
    
             
    def FillTree(self):
# Заполнение модели двумя уровнями данных из запросов
        modelTree.clear()        
        modelTree.reset()        
        grandparent = QStandardItem(u"СРЕДСТВА ИЗМЕРЕНИЯ (весь перечень)")
        grandparent.setData(1)
        modelTree.appendRow(grandparent)
# 27.06.2022        
        SQL1 = "select id, name_type from type_msr where id_category = 1 order by name_type"
#        SQL1 = "select id, name_type from type_msr where id_category = 1 and id in " + self.FILTR1 + " order by name_type"
        query1 = QSqlQuery(SQL1, db)
        SQL2 = "select id, name_group from group_msr where id_type=:id_type order by name_group"
#        SQL2 = "select id, name_group from group_msr where id_type=:id_type and id in " + self.FILTR2 + " order by name_group"
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
# 27.06.2022        
        SQL1 = "select id, name_type from type_msr where id_category = 2 order by name_type"
#        SQL1 = "select id, name_type from type_msr where id_category = 2 and id in " + self.FILTR1 + " order by name_type"
        print SQL1
        
        query1 = QSqlQuery(SQL1, db)
        SQL2 = "select id, name_group from group_msr where id_type=:id_type order by name_group"
#        SQL2 = "select id, name_group from group_msr where id_type=:id_type and id in " + self.FILTR2 + " order by name_group"
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
            
        self.ui.treeView.expandAll()
        first = modelTree.index(0, 0, QModelIndex());
        self.ui.treeView.setCurrentIndex(first)


    def ViewMsr(self, id_search):
        row = self.selModelTree.currentIndex().row()
        row1 = self.selModelTree.currentIndex().parent().row()
        interId = self.selModelTree.currentIndex().internalId()
        parentitem = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent()
        query = QSqlQuery(db)
        if parentitem == None:
            
            selectMsr = """SELECT msr.id, name_msr, period, period_view FROM msr, group_msr, type_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = type_msr.id
                           AND type_msr.id_category = :ID_CATEGORY
                           AND msr.id IN """ + self.FILTR3 + """
                           ORDER BY name_msr"""
                          
# 27.06.2022        
            selectMsr = """SELECT msr.id, name_msr, period, period_view FROM msr, group_msr, type_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = type_msr.id
                           AND type_msr.id_category = :ID_CATEGORY
                           ORDER BY name_msr"""

            print selectMsr                                       
            
            query.prepare(selectMsr)
            global id_category                       
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_category", id_category)          
        elif parentitem.parent() == None:
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent().data().toString()
            selectMsr = """SELECT msr.id, name_msr FROM msr, group_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = :ID_TYPE
                           AND msr.id IN """ + self.FILTR3 + """
                           ORDER BY name_msr"""
# 27.06.2022        
            selectMsr = """SELECT msr.id, name_msr FROM msr, group_msr
                           WHERE msr.id_group = group_msr.id
                           AND group_msr.id_type = :ID_TYPE
                           ORDER BY name_msr"""
            query.prepare(selectMsr)
            id_type = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_type", id_type)          
        else:
            id_category = modelTree.itemFromIndex(self.selModelTree.currentIndex()).parent().parent().data().toString()
# 27.06.2022        
            selectMsr = """SELECT id, name_msr FROM msr
                           WHERE id_group = :ID_GROUP
                           AND msr.id IN """ + self.FILTR3 + """
                           ORDER BY name_msr"""
            selectMsr = """SELECT id, name_msr FROM msr
                           WHERE id_group = :ID_GROUP
                           ORDER BY name_msr"""
            query.prepare(selectMsr)
            id_group = modelTree.itemFromIndex(self.selModelTree.currentIndex()).data().toString()
            query.bindValue(":id_group", id_group)
        query.exec_()

        if not self.ui.checkBox_3.isChecked(): # and not self.checkBox_4.isChecked():   
            model2.clear()        
            model2.reset()        
            model.clear()                
        
        model.setQuery(query)
        
        if model.query().size() < 1:
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_3.setText("")
           # self.lineEdit_4.setText("")
                
        if id_category == '1':
            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование средства измерения")
        if id_category == '2':
            model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование средства защиты")
                     
        self.ui.tableView.setColumnHidden(0, True)        
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        
        self.searchInModel(0, self.ui.tableView, model)
 #       self.pushButton.setEnabled(self.selModel.currentIndex().row() >= 0)
        self.ui.tableView.repaint()


    def ViewZavMsr(self, id_search, id_msr, zav_num):
        prov_spis = "AND (finish_date IS NULL AND reserve_date IS NULL)"
        #prov_spis = ""
        query9 = QSqlQuery(db)
        
        if id_msr <> -1:
            
            query9.prepare(u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE id_msr=:ID """ + prov_spis + """ AND type IS NOT NULL ORDER BY zav_num""")
            SQL = u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE id_msr=:ID """ + prov_spis + """ ORDER BY zav_num"""
            query9.bindValue(":id", id_msr)            
        else:
            if zav_num == "":
                query9.prepare(u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE true """ + prov_spis + """ AND type IS NOT NULL ORDER BY zav_num""")
                SQL = u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE true """ + prov_spis + """ ORDER BY zav_num"""
            else:
                query9.prepare(u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE zav_num LIKE :zav_num """ + prov_spis + """ AND type IS NOT NULL ORDER BY zav_num""")
                SQL = u"""SELECT id, id_msr, zav_num,
CASE WHEN type = 1 THEN 'Эталонное СИ' WHEN type = 2 THEN 'Вспомогательное оборудование' ELSE NULL END AS name_type,
num_gosreestr, comment, type            
FROM zav_msr WHERE zav_num LIKE :zav_num """ + prov_spis + """ ORDER BY zav_num"""
                query9.bindValue(":zav_num", zav_num + "%")
                
                
        query9.prepare(SQL)        
        query9.bindValue(":id", id_msr)            
        print 'id_msr = ', id_msr        
        print 'zav_num = ', zav_num 
        print SQL       
                
        query9.exec_()        
        
        model2.clear()        
        model2.setQuery(query9)

        model2.setHeaderData(2, QtCore.Qt.Horizontal, u"Заводской\nномер")
        model2.setHeaderData(3, QtCore.Qt.Horizontal, u"Назначение")
        model2.setHeaderData(4, QtCore.Qt.Horizontal, u"Номер в\nГосреестре СИ")
        model2.setHeaderData(5, QtCore.Qt.Horizontal, u"Доп. сведения")
        self.ui.tableView_2.setColumnHidden(0, True)        
        self.ui.tableView_2.setColumnHidden(1, True)        
        self.ui.tableView_2.setColumnHidden(6, True)        
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
                
        self.searchInModel(id_search, self.ui.tableView_2, model2)

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


    def selectionChangedTree(self):
        self.ViewMsr(0)        

    def selectionChanged1(self):
        global id_msr
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        
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
        self.ui.lineEdit_2.setText(query1.value(0).toString())
        
        self.ui.lineEdit_3.setText(model.record(row).field('name_msr').value().toString())
                        
        if not self.ui.checkBox_3.isChecked(): # and not self.checkBox_4.isChecked():   
            self.ViewZavMsr(0, id_msr, None)

                 
    def selectionChanged2(self):
        
        global id_zav, tempDate        
        row = self.selModel2.currentIndex().row()
        if row == -1:
            return
        id_zav = model2.record(row).field('id').value().toString()   
        tempDate = model2.record(row).field('first_checking').value().toDate()
        
        print 'selectionChanged2'
                
        SQL1 = """select name_group, name_msr, group_msr.id as id_group, msr.id as id_msr
                  from group_msr, msr
                  where group_msr.id = msr.id_group
                  and msr.id = :id_msr"""
        query1 = QSqlQuery(db)
        query1.prepare(SQL1)
        query1.bindValue(":id_msr", model2.record(row).field('id_msr').value().toString());
        query1.exec_()
        query1.next()
        self.ui.lineEdit_2.setText(query1.value(0).toString())
        self.ui.lineEdit_2.setCursorPosition(0)
        self.ui.lineEdit_2.setStyleSheet("color: blue; background-color: lightgray")
        self.ui.lineEdit_3.setText(query1.value(1).toString())
        self.ui.lineEdit_3.setCursorPosition(0)
        self.ui.lineEdit_3.setStyleSheet("color: blue; background-color: lightgray")
        
        if self.ui.checkBox_3.isChecked(): # or self.checkBox_4.isChecked() :
            # поиск в дереве
            for e in range(2):
                for i in range(modelTree.item(e).rowCount()):
                    for j in range(modelTree.item(e).child(i).rowCount()):
                        if query1.value(2).toString() == modelTree.item(e).child(i).child(j).data().toString():
                            self.ui.treeView.setCurrentIndex(modelTree.indexFromItem(modelTree.item(e).child(i).child(j)))

            # поиск в средствах измерения
            self.searchInModel(query1.value(3).toString(), self.ui.tableView, model)
       
    def checkBox_3_Toggle(self, check):
        self.ui.lineEdit.setEnabled(check)        
#        self.checkBox_4.setEnabled(not check)
        self.ui.treeView.setEnabled(not check)
        self.ui.tableView.setEnabled(not check)
#        self.tableView_4.setEnabled(not check)
        if check:            
            self.ViewZavMsr(0, -1, self.ui.lineEdit.text())
        else:    
            self.ViewZavMsr(0, id_msr, None)

    def lineEdit_textChanged(self):
        self.ViewZavMsr(0, -1, self.ui.lineEdit.text())
        
        
    def widthArea(self, tableView):
        # Возвращает ширину свободной области таблицы tableView
        HSWidth = tableView.verticalHeader().width() + 4
        if tableView.verticalScrollBar().width() < 100 and tableView.verticalScrollBar().isVisible():
            HSWidth += tableView.verticalScrollBar().width()
        return tableView.width() - HSWidth    
    
    def pushButton_Click(self):
        row = self.selModel.currentIndex().row()
        self.NAME_MSR = unicode(model.record(row).field('name_msr').value().toString())
        print "model.record(row).field('name_msr').value().toString() = ", unicode(model.record(row).field('name_msr').value().toString())
        row = self.selModel2.currentIndex().row()
        self.ID_ZAV_MSR = int(model2.record(row).field('id').value().toString())
        self.ZAV_NUM = model2.record(row).field('zav_num').value().toString()
                
        self.IS_SELECT = True
        self.close()

    def pushButton2_Click(self):
        self.IS_SELECT = False
        self.close()


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
###        wind = classJournal()
        wind = classJournal(env)
        if wind.is_show: 
            wind.show()
        sys.exit(app.exec_())


        

