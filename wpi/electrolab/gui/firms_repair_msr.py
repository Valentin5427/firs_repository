# -*- coding: UTF-8 -*-

'''
Created on 16.08.2013

@author: atol
'''

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtGui import QMessageBox, QIcon
from dpframe.base.inits import json_config_init
import ui.ico_64_rc
import os
import JournalMsr
import TestHeart

selFirm = u'''
SELECT id, name_firm, address
FROM firms_repair_msr ORDER BY name_firm
'''

model = QSqlQueryModel()
withCol1 = 200
withCol2 = 100
VSB1 = False

def noneValue(v):
    if v.trimmed() == '':
        return None
    else:
        return v.trimmed()

def nullValue(fild):
    if fild.isNull():
        return ''
    else:
        return fild.value().toString()
    
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
        global VSB1
                
        if obj.objectName() == 'tv1' and (e.type() == QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):        
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            VSB1 = obj.verticalScrollBar().isVisible()            
        return False
'''
               
class FirmRepair(QtGui.QDialog):
    def __init__(self, env):
        QtGui.QDialog.__init__(self)        
        global db1
        db1 = env.db
        global path_ui
        path_ui = env.config.paths.ui + "/"
        if not os.path.exists(path_ui):        
            path_ui = ""
        if not JournalMsr.MyLoadUi(path_ui, "firms_repair_msr.ui", self):
            self.is_show = False
            return

        self.id = ''
        self.name_firm = ''
        self.address = ''

        self.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_3.setIcon(QIcon(u':/ico/ico/pencil_64.png'))

        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.pushButton_3.clicked.connect(self.pushButton3_Click)
        self.pushButton_5.clicked.connect(self.pushButton5_Click)
        self.pushButton_4.clicked.connect(self.pushButton4_Click)
        self.tableView.setModel(model)
        self.selModel = self.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)
        self.tableView.setObjectName('tv1')
        self.tableView.setHorizontalScrollBarPolicy(1)
        ###self.tableView.installEventFilter(MyFilter(self.tableView))        
        self.ViewFirm(0)        
        self.pushButton.setToolTip(u'добавить организацию')

    def ViewFirm(self, id_search):
        if id_search == '':
            return        
        model.setQuery(selFirm, db1)
        self.tableView.setColumnHidden(0, True)        
        TestHeart.searchInModel(id_search, self.tableView, model)
#        enab = self.selModel.currentIndex().row() >= 0
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование организации")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Адрес")
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
#        self.pushButton_2.setEnabled(enab)
#        self.pushButton_3.setEnabled(enab)
        self.viewButtons()

    def selectionChanged1(self):
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        global id_firm
        id_firm = model.record(row).field('id').value().toString()

# Редактирование видов измерения (начало кода)        
    def pushButton_Click(self):
        global id_firm
        self.wind1 = self.editFirm()
        self.wind1.tag = 1                
        self.wind1.setWindowTitle(u'Добавление новой организации')
        self.wind1.exec_()                
        self.ViewFirm(id_firm)

    def pushButton2_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM firms_repair_msr WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            model.setQuery(selFirm, db1)
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView.selectRow(row)                                    
#            enab = self.selModel.currentIndex().row() >= 0
#            self.pushButton_2.setEnabled(enab)
#            self.pushButton_3.setEnabled(enab)
            self.viewButtons()
            
    def viewButtons(self):
        enab = self.selModel.currentIndex().row() >= 0
        self.pushButton_2.setEnabled(enab)
        self.pushButton_3.setEnabled(enab)
        
#        if self.pushButton.isEnabled():                
#            self.pushButton.setToolTip(u'добавить организацию')
#        else:    
#            self.pushButton.setToolTip(u'')
            
        if self.pushButton_2.isEnabled():                
            self.pushButton_2.setToolTip(u'удалить  организацию')
        else:    
            self.pushButton_2.setToolTip(u'')
            
        if self.pushButton_3.isEnabled():                
            self.pushButton_3.setToolTip(u'редактировать  организацию')
        else:    
            self.pushButton_3.setToolTip(u'')

            
            
            
    def pushButton3_Click(self):
        self.wind1 = self.editFirm()
        if self.wind1.tag == 0:
            return
        self.wind1.tag = 2
        self.wind1.setWindowTitle(u'Редактирование текущей организации')
        row = self.selModel.currentIndex().row()                
        self.wind1.lineEdit.setText(model.record(row).field('name_firm').value().toString())
        self.wind1.lineEdit_2.setText(model.record(row).field('address').value().toString())
        
        self.wind1.exec_()                
        self.ViewFirm(id_firm)

    def pushButton5_Click(self):
        self.close()

    def pushButton4_Click(self):
        row = self.selModel.currentIndex().row()
        if row < 0:
            QMessageBox.warning(None, u"Предупреждение", u"Организация не выбрана!", QMessageBox.Ok)
            return    
        self.id = model.record(row).field('id').value().toString()
        self.name_firm = model.record(row).field('name_firm').value().toString()
        self.address = model.record(row).field('address').value().toString()
        print u'ВЫБОР'
        self.close()

    class editFirm(QtGui.QDialog):
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
            if not JournalMsr.MyLoadUi(path_ui, "editGroup.ui", self):
                return
            
            self.lineEdit.setMaxLength(30)         
            self.lineEdit_2.setMaxLength(100)         
            self.label.setText(u'Наименование организации')             
                        
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.pushButton_2.clicked.connect(self.pushButton2_Click)            
        
        def pushButton1_Click(self):            
            if self.lineEdit.text() == '':
                QMessageBox.warning(None, u"Предупреждение",
                u"Введи аименование организации",
                QMessageBox.Ok)
                self.lineEdit.setFocus()
                return
                
            global id_firm
            query = QSqlQuery(db1)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM firms_repair_msr");
                query.exec_()
                query.next()
                id_firm = query.value(0).toString()
                query.prepare("INSERT INTO firms_repair_msr (id, name_firm, address) VALUES (:id, :name_firm, :address)")
            else:
                query.prepare("UPDATE firms_repair_msr SET name_firm = :name_firm, address = :address WHERE id = :id")
                
            query.bindValue(":id", id_firm);
            query.bindValue(":name_firm", noneValue(self.lineEdit.text()))
            query.bindValue(":address", noneValue(self.lineEdit_2.text()))
            #print self.lineEdit.maxLength

            if not query.exec_():
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка сохранения",
                QMessageBox.Ok)
            else:    
                self.close()

        def pushButton2_Click(self):
            global id_firm
            id_firm = ''
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
        wind = FirmRepair(env)
        if wind.tag <> 0:        
            wind.show()
            wind.resizeEvent(None)
        sys.exit(app.exec_())
   