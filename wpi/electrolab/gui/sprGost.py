# -*- coding: UTF-8 -*-
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt, QPoint

import socket
from fileinput import close
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.DigitalKeyboard import DigitalKeyboard

import ui.ico_64_rc

import datetime

from datetime import date

gost_id = -1
detail_id = -1
quadro_id = -1


model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit


withCol1 = 200
withCol2 = 500

withCol_1 = 50
withCol_2 = 50
withCol_3 = 50
withCol_4 = 50
withCol_5 = 50
withCol_6 = 50
withCol_7 = 50
withCol_8 = 50

withCol__1 = 200
withCol__2 = 200

isSave = False
mnu_2 = None


sw_ = 0

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
        
        global sw_
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            obj.setColumnWidth(1, withCol1)
            obj.setColumnWidth(2, withCol2)
            VSB1 = obj.verticalScrollBar().isVisible()


        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4 + withCol_5 + withCol_6 + withCol_7 + withCol_8))
            obj.setColumnWidth(1, koef * withCol_1)
            obj.setColumnWidth(2, koef * withCol_2)
            obj.setColumnWidth(3, koef * withCol_3)
            obj.setColumnWidth(4, koef * withCol_4)
            obj.setColumnWidth(5, koef * withCol_5)
            obj.setColumnWidth(6, koef * withCol_6)
            obj.setColumnWidth(7, koef * withCol_7)
            obj.setColumnWidth(8, koef * withCol_8)
            VSB2 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv3' and (e.type() <> QtCore.QEvent.Resize or VSB3 <> obj.verticalScrollBar().isVisible()):
            obj.setColumnWidth(1, withCol__1)
            obj.setColumnWidth(2, withCol__2)
            VSB3 = obj.verticalScrollBar().isVisible()


        return False

        
        
class sprGost(QtGui.QDialog, UILoader):
    def __init__(self, _env, sw, *args):
        QtGui.QDialog.__init__(self, *args)        
       
        global sw_
        sw_ = sw
        
        self.sw = sw
        global mnu_2

        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"sprGost.ui")        
        
        self.ui.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_3.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_4.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_5.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_6.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.ui.pushButton_9.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.ui.pushButton_10.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.ui.pushButton_11.setIcon(QIcon(u':/ico/ico/trash_64.png'))

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)      
        
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
        self.ui.pushButton_9.clicked.connect(self.pushButton_9_Click)
        self.ui.pushButton_10.clicked.connect(self.pushButton_10_Click)
        self.ui.pushButton_11.clicked.connect(self.pushButton_11_Click)
        
        
        
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
        self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)

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
        self.ui.tableView_3.setHorizontalScrollBarPolicy(1)

        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))
        self.ui.tableView_3.installEventFilter(MyFilter(self.ui.tableView_3))

        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setObjectName('tv2')
        self.ui.tableView_3.setObjectName('tv3')
        

        self.ui.pushButton_7.setVisible(False)
        self.ui.pushButton_8.setVisible(False)
        
        
        if sw == 1:
            self.ui.tableView_3.setVisible(False)
            self.ui.label_4.setVisible(False)
            self.ui.pushButton_9.setVisible(False)
            self.ui.pushButton_10.setVisible(False)
            self.ui.pushButton_11.setVisible(False)
                
        if sw == 2:
            self.ui.tableView_2.setVisible(False)
            self.ui.label_3.setVisible(False)
            self.ui.pushButton_4.setVisible(False)
            self.ui.pushButton_5.setVisible(False)
            self.ui.pushButton_6.setVisible(False)
        self.IS_SELECT = False    

            
        # Организация контекстного меню на кнопке "Добавить"
        '''
        fnt = QtGui.QFont()
        fnt.setPointSize(14)                
        self.mnu = QtGui.QMenu(self)
        self.mnu.addAction(QtGui.QAction(u'Добавить с копированием', self))
        self.mnu.setFont(fnt)        
        self.ui.pushButton.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.ui.pushButton.customContextMenuRequested.connect(self.on_context_menu)      
        self.connect(self.mnu, QtCore.SIGNAL('triggered(QAction *)'), self.pushButton_Click_copy)
'''
                
        self.selGost()

      
    def on_context_menu(self, point):
        self.mnu.exec_(self.ui.pushButton.mapToGlobal(point))

    def mnu_2_Click(self, q):
        self.id_type = int(q.data().toString())    
        self.ui.lineEdit_2.setText(unicode(q.text()))
            

# Редактирование трансформатора (начало кода)        
              
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editGost(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового госта')
        row = self.selModel.currentIndex().row()
  #      self.wind.ui.lineEdit.setText(model.record(row).field('type').value().toString())
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selGost()
            
            #Вычисление максимального id и навигация на него

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM gost");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView, model)            
            
            
                
    def pushButton_2_Click(self):
        global isSave        
        
        self.wind = self.editGost(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего госта')
        row = self.selModel.currentIndex().row()
        self.wind.ui.lineEdit.setText(model.record(row).field('gost').value().toString())
        self.wind.ui.textEdit.setText(model.record(row).field('description').value().toString())
        
        id_search = model.record(row).field('id').value().toString()

        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selGost()
            self.searchInModel(id_search, self.ui.tableView, model)            
                       



    def pushButton_3_Click(self):
        print 'QSqlQueryModel.rowCount(parent=QModelIndex() = ', model_2.rowCount()
        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            if model_2.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале точки!', QMessageBox.Ok)
                return
            if model_3.rowCount() > 0:            
                QMessageBox.warning(self, u"Предупреждение",  u'Удалите вначале нагрузки!', QMessageBox.Ok)
                return
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM gost WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selGost()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    
                        
                                
    def pushButton_4_Click(self):
        print 'swswswswswsw=', self.sw
        
        global isSave        
        self.wind = self.editPoint(self.env)
        self.wind.tag = 1
                                
        self.wind.setWindowTitle(u'Добавление новой точки')
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selPoint()

            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM gost_detail");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView_2, model_2)            
            
                
                
    def pushButton_9_Click(self):
        global isSave        
        self.wind = self.editQuadroLoad(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление новой нагрузки')
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selQuadroLoad()
            
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM gost_quadroload");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            
            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView_3, model_3)            
                
                
                
                
                
    def pushButton_5_Click(self):
        global isSave        
        self.wind = self.editPoint(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущей точки')
        row = self.selModel_2.currentIndex().row()


        self.wind.ui.lineEdit.setText(model_2.record(row).field('classaccuracy').value().toString())
        self.wind.ui.doubleSpinBox.setValue(float(model_2.record(row).field('ipercent').value().toString()))
        self.wind.ui.doubleSpinBox_3.setValue(float(model_2.record(row).field('aleftlimit').value().toString()))
        self.wind.ui.doubleSpinBox_4.setValue(float(model_2.record(row).field('arightlimit').value().toString()))
        self.wind.ui.doubleSpinBox_5.setValue(float(model_2.record(row).field('pleftlimit').value().toString()))
        self.wind.ui.doubleSpinBox_6.setValue(float(model_2.record(row).field('prightlimit').value().toString()))        
        self.wind.ui.checkBox.setChecked(bool(model_2.record(row).field('usequadro').value().toString()))              
        self.wind.ui.checkBox.setChecked(bool(int(model_2.record(row).field('usequad').value().toString())))                  
        self.wind.ui.doubleSpinBox_2.setValue(float(model_2.record(row).field('itreshold').value().toString()))

        id_search = model_2.record(row).field('id').value().toString()

        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selPoint()
            # навигация
###            self.ui.tableView_2.selectRow(row)                                    
            self.searchInModel(id_search, self.ui.tableView_2, model_2)            


    def pushButton_10_Click(self):
        global isSave        
        self.wind = self.editQuadroLoad(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущей нагрузки')
        row = self.selModel_3.currentIndex().row()

        self.wind.ui.doubleSpinBox.setValue(float(model_3.record(row).field('secondload').value().toString()))
        self.wind.ui.doubleSpinBox_2.setValue(float(model_3.record(row).field('quadro').value().toString()))

        id_search = model_3.record(row).field('id').value().toString()


        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selQuadroLoad()
            # навигация
            ###self.ui.tableView_3.selectRow(row)                                    

            print 'id_search    =', id_search
            self.searchInModel(id_search, self.ui.tableView_3, model_3)            


            
    def pushButton_6_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM gost_detail WHERE id = :ID")
            row = self.selModel_2.currentIndex().row()                
            query.bindValue(":id", model_2.record(row).field('id').value().toString());
            query.exec_()
            self.selPoint()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_2.selectRow(row)                                    


    def pushButton_11_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM gost_quadroload WHERE id = :ID")
            row = self.selModel_3.currentIndex().row()                
            query.bindValue(":id", model_3.record(row).field('id').value().toString());
            query.exec_()
            self.selQuadroLoad()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_3.selectRow(row)                                    




                        
    def pushButton_7_Click(self):
        self.IS_SELECT = True
        self.close()        

    def pushButton_8_Click(self):
        self.IS_SELECT = False
        self.close()        

                        
            
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
            
            
    def selGost(self):
        
        query = QSqlQuery(db1)
                                
        SQL = """select id, gost, description from gost order by id"""
        
        print SQL       
        query.prepare(SQL)

        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
        
        
        model.setQuery(query)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"ГОСТ")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Описание")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        
        self.ui.tableView.setColumnHidden(0,  True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)
        self.ui.pushButton_4.setEnabled(enab)
        


    def selPoint(self):
        
        row = self.selModel.currentIndex().row()
        print 'row = row = row = ', row
        global gost_id
        if row < 0:
            gost_id = -1
        else:    
            gost_id = int(model.record(row).field('id').value().toString())
            
        query = QSqlQuery(db1)
        query.prepare("""select
id,
classaccuracy,
ipercent,
aleftlimit,
arightlimit,
pleftlimit,
prightlimit,
usequadro,
itreshold,
case when usequadro then 1 else 0 end as usequad
from gost_detail
where gost_id = :gost_id 
order by classaccuracy, ipercent
""")
        
        
        query.bindValue(":gost_id", gost_id)
        
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_2.setQuery(query)

        model_2.setHeaderData(1,  QtCore.Qt.Horizontal, u"Класс\nточности")
        model_2.setHeaderData(2,  QtCore.Qt.Horizontal, u"Процент")
        model_2.setHeaderData(3,  QtCore.Qt.Horizontal, u"Токовая\nпогрешность-")
        model_2.setHeaderData(4,  QtCore.Qt.Horizontal, u"Токовая\nпогрешность+")
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Угловая\nпогрешность-")
        model_2.setHeaderData(6,  QtCore.Qt.Horizontal, u"Угловая\nпогрешность+")
        model_2.setHeaderData(7,  QtCore.Qt.Horizontal, u"Четвертная\nнагрузка")                
        model_2.setHeaderData(8,  QtCore.Qt.Horizontal, u"Погрешность\nточки")
        
        
            
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.setColumnHidden(9, True)
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
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)
        


    def selQuadroLoad(self):
        row = self.selModel.currentIndex().row()
        print 'row = row = row = ', row
        global gost_id
        if row < 0:
            gost_id = -1
        else:    
            gost_id = int(model.record(row).field('id').value().toString())
        query = QSqlQuery(db1)
        query.prepare("""select
id,
secondload,
quadro
from gost_quadroload
where gost_id = :gost_id 
order by secondload, quadro
""")
        
        
        query.bindValue(":gost_id", gost_id)
        
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_3.setQuery(query)

        model_3.setHeaderData(1,  QtCore.Qt.Horizontal, u"Вторичная нагрузка")
        model_3.setHeaderData(2,  QtCore.Qt.Horizontal, u"Четвертная нагрузка")
            
        self.ui.tableView_3.setColumnHidden(0, True)
        self.ui.tableView_3.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_3.selectRow(0)
        
        self.ui.tableView_3.setColumnWidth(1,  withCol__1)
        self.ui.tableView_3.setColumnWidth(2,  withCol__2)
        enab = self.selModel_3.currentIndex().row() >= 0        
        self.ui.pushButton_10.setEnabled(enab)
        self.ui.pushButton_11.setEnabled(enab)
        


    def selectionChanged(self):
        global sw_
        self.selPoint()
        self.selQuadroLoad()
        
        

    def selectionChanged_2(self):
        global detail_id
        global sw_
        row = self.selModel_2.currentIndex().row()
        detail_id = model_2.record(row).field('id').value().toString()
            

    def selectionChanged_3(self):
###        global detail_id
        global quadro_id
        global sw_
        row = self.selModel_3.currentIndex().row()
        quadro_id = model_3.record(row).field('id').value().toString()
            

# Редактирование гостов (начало кода)        
                        
    class editGost(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            global mnu_2
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editGost.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
        
        def pushButton1_Click(self):
                                                
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Укажи ГОСТ', QMessageBox.Ok)
                return
                                    
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                query.prepare('''INSERT INTO gost (gost, description)
                                 values (:gost, :description)''')            
            else:
                query.prepare('''UPDATE gost SET gost = :gost,
                                                        description = :description                                                        
                                 WHERE id = :id''')

                query.bindValue(":id", gost_id);
                                
            query.bindValue(":gost", noneValue(self.ui.lineEdit.text()))
            query.bindValue(":description", noneValue(self.ui.textEdit.toPlainText()))
            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

                           
# Редактирование гостов (конец кода)        


# Редактирование точек (начало кода)        
                        
    class editPoint(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editPoint.ui")        
                        
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
        
        
        def pushButton1_Click(self):
            global gost_id
            global detail_id
            global isSave        
            query = QSqlQuery(db1)

            
            if self.tag == 1:
                query.prepare('''INSERT INTO gost_detail (gost_id, classaccuracy, ipercent, aleftlimit, arightlimit,
                                                          pleftlimit, prightlimit, usequadro, itreshold) 
                                  values (:gost_id, :classaccuracy, :ipercent, :aleftlimit, :arightlimit,
                                          :pleftlimit, :prightlimit, :usequadro, :itreshold)''')            
                query.bindValue(":gost_id", gost_id);
            else:
                query.prepare('''UPDATE gost_detail SET classaccuracy = :classaccuracy,
                                                        ipercent = :ipercent,
                                                        aleftlimit = :aleftlimit,
                                                        arightlimit = :arightlimit,
                                                        pleftlimit = :pleftlimit,
                                                        prightlimit = :prightlimit,
                                                        usequadro = :usequadro,
                                                        itreshold = :itreshold                
                                                 WHERE id = :detail_id''')
                query.bindValue(":detail_id", detail_id);
                


            query.bindValue(":classaccuracy", self.ui.lineEdit.text())
            query.bindValue(":ipercent",      self.ui.doubleSpinBox.text())
            query.bindValue(":aleftlimit",    self.ui.doubleSpinBox_3.text())
            query.bindValue(":arightlimit",   self.ui.doubleSpinBox_4.text())
            query.bindValue(":pleftlimit",    self.ui.doubleSpinBox_5.text())
            query.bindValue(":prightlimit",   self.ui.doubleSpinBox_6.text())            
            query.bindValue(":usequadro",     self.ui.checkBox.isChecked())            
            query.bindValue(":itreshold",     self.ui.doubleSpinBox_2.text())


            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()
            
# Редактирование точек (конец кода)        



# Редактирование нагрузок (начало кода)        


    class editQuadroLoad(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editQuadroLoad.ui")        
                        
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
        
        
        def pushButton1_Click(self):
            global gost_id            
            global quadro_id
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                query.prepare('''INSERT INTO gost_quadroload (gost_id, secondload, quadro) 
                                  values (:gost_id, :secondload, :quadro)''')            
                query.bindValue(":gost_id", gost_id);
            else:
                query.prepare('''UPDATE gost_quadroload SET secondload = :secondload,
                                                            quadro = :quadro
                                                 WHERE id = :quadro_id''')
                query.bindValue(":quadro_id", quadro_id);
                

            query.bindValue(":secondload",      self.ui.doubleSpinBox.text())
            query.bindValue(":quadro",     self.ui.doubleSpinBox_2.text())

            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()

            
# Редактирование нагрузок (конец кода)        


                

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
        
        wind = sprGost(env, 0)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())


