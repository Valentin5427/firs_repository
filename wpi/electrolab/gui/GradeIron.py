# -*- coding: UTF-8 -*-
'''
Created on 29.10.2013

@author: Atol
'''
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtGui import QMessageBox, QIcon
#import ico_64_rc
import ui.ico_64_rc
import os
import JournalMsr
import TestHeart

selGradeIron = "SELECT * FROM grade_iron ORDER BY mark"

model = QSqlQueryModel()
withCol1 = 200
withCol2 = 100
VSB1 = False

id_grade = ''

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
    
    
class GradeIron(QtGui.QDialog):
    def __init__(self, env):
        QtGui.QDialog.__init__(self)        
        global db1
        db1 = env.db
        global path_ui
        path_ui = env.config.paths.ui + "/"
        if not os.path.exists(path_ui):        
            path_ui = ""
        if not JournalMsr.MyLoadUi(path_ui, "gradeIron.ui", self):
            self.is_show = False
            return

        self.id_h = ''

        self.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_3.setIcon(QIcon(u':/ico/ico/pencil_64.png'))

        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.pushButton_3.clicked.connect(self.pushButton3_Click)
        self.pushButton_5.clicked.connect(self.pushButton5_Click)
        self.tableView.setModel(model)
        self.selModel = self.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)
        self.tableView.setObjectName('tv1')
        self.tableView.setHorizontalScrollBarPolicy(1)
        self.tableView.installEventFilter(MyFilter(self.tableView))        
        self.ViewGradeIron(0)        

    def ViewGradeIron(self, id_search):
        if id_search == '':
            return
        
        model.setQuery(selGradeIron, db1)
        self.tableView.setColumnHidden(0, True)        
        TestHeart.searchInModel(id_search, self.tableView, model)
        enab = self.selModel.currentIndex().row() >= 0
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Марка железа")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Удельный вес")
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.pushButton_2.setEnabled(enab)
        self.pushButton_3.setEnabled(enab)

    def selectionChanged1(self):
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        global id_grade
        id_grade = model.record(row).field('id').value().toString()

# Редактирование видов измерения (начало кода)        
    def pushButton_Click(self):
        global id_grade
        self.wind1 = self.editGradeIron()
        self.wind1.tag = 1
                
        self.wind1.setWindowTitle(u'Добавление новой марки железа')
        self.wind1.exec_()        
        
        self.ViewGradeIron(id_grade)

    def pushButton2_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM grade_iron WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            model.setQuery(selGradeIron, db1)
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView.selectRow(row)                                    
            enab = self.selModel.currentIndex().row() >= 0
            self.pushButton_2.setEnabled(enab)
            self.pushButton_3.setEnabled(enab)
            
    def pushButton3_Click(self):
        global id_grade
        self.wind1 = self.editGradeIron()
        if self.wind1.tag == 0:
            return
        self.wind1.tag = 2
        self.wind1.setWindowTitle(u'Редактирование текущей позиции')
        row = self.selModel.currentIndex().row()                
        self.wind1.lineEdit.setText(model.record(row).field('mark').value().toString())
        self.wind1.lineEdit_2.setText(model.record(row).field('dens').value().toString())
        self.wind1.exec_()                
        self.ViewGradeIron(id_grade)

    def pushButton5_Click(self):
        self.close()

    class editGradeIron(QtGui.QDialog):
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
            if not JournalMsr.MyLoadUi(path_ui, "editGradeIron.ui", self):
                return
                        
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.pushButton_2.clicked.connect(self.pushButton2_Click)
            
        
        def pushButton1_Click(self):
            if self.lineEdit.text() == '':
                QMessageBox.warning(None, u"Предупреждение",
                u"Введи марку железа",
                QMessageBox.Ok)
                self.lineEdit.setFocus()
                return
                
            global id_grade
            query = QSqlQuery(db1)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM grade_iron");
                query.exec_()
                query.next()
                id_grade = query.value(0).toString()
                query.prepare("INSERT INTO grade_iron (id, mark, dens) VALUES (:id, :mark, :dens)")
            else:
                query.prepare("UPDATE grade_iron SET mark = :mark, dens = :dens WHERE id = :id")
                
            query.bindValue(":id", id_grade);
            query.bindValue(":mark", noneValue(self.lineEdit.text()))
            query.bindValue(":dens", noneValue(self.lineEdit_2.text()))

            if not query.exec_():
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка сохранения",
                QMessageBox.Ok)
            else:    
                self.close()

        def pushButton2_Click(self):
            global id_grade
            id_grade = ''
            self.close()            


if __name__ == "__main__":    
    import sys
    app = QtGui.QApplication(sys.argv)
    db = QSqlDatabase("QPSQL")
    db.setHostName("localhost")
    db.setDatabaseName("electrolab")
    db.setUserName("electrolab")
    db.setPassword("electrolab")
    rez = db.open();
    class Env():
        class config():
            class paths():
                pass    
    env = Env()
    env.db = db    
    env.config.paths.ui = "ui"

    wind = GradeIron(env)
    if wind.tag <> 0:        
        wind.show()
        wind.resizeEvent(None)
    sys.exit(app.exec_())
