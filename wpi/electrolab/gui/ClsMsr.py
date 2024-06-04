# -*- coding: UTF-8 -*-

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtGui import QMessageBox, QIcon
import ui.ico_64_rc
#import electrolab.gui.ui.ico_64_rc
import os
import JournalMsr

selectTypeMsr = "SELECT id, name_type FROM type_msr WHERE id_category=:id_category ORDER BY name_type"
#selectTypeMsr = "SELECT * FROM type_msr WHERE id_category=:id_category ORDER BY name_type"
selectGroupMsr = "SELECT * FROM group_msr WHERE id_type=:ID ORDER BY name_group"
selectMsr = "SELECT * FROM msr WHERE id_group=:ID ORDER BY name_msr"
selectAccuracy = "SELECT * FROM accuracy_msr WHERE id_msr=:ID ORDER BY classaccuracy"
id_type = ''
id_group = ''
id_msr = ''
id_accuracy = ''
model = QSqlQueryModel()
model2 = QSqlQueryModel()
model3 = QSqlQueryModel()
model4 = QSqlQueryModel()


# Позволяет выбирать значки из контекстного меню и вставлять их в строку редактирования
# значки задаются в параметре signs
class MLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None, signs=""):
        QtGui.QLineEdit.__init__(self, parent)
        self.signs=signs

    def contextMenuEvent(self, event):
        submenu = QtGui.QMenu(u"Значки")
        for sign in self.signs:
            submenu.addAction(sign)
        self.connect(submenu, QtCore.SIGNAL('triggered(QAction *)'), self.actions)
        menu = self.createStandardContextMenu()
        menu.addSeparator()
        menu.addMenu(submenu)        
        menu.exec_(event.globalPos())
            
    def actions(self, action):        
        curspos = self.cursorPosition()
        self.setText(self.text()[:curspos] + action.text() + self.text()[curspos:])
        self.setCursorPosition(curspos + 1)


class classMsr(QtGui.QDialog):
    def __init__(self, env, *args):
        QtGui.QDialog.__init__(self, *args)        
        global db1
        global id_category
        db1 = env.db        
        global path_ui
        path_ui = env.config.paths.ui + "/"
        if not os.path.exists(path_ui):        
            path_ui = ""
#        uic.loadUi(path_ui + "clsmsr.ui", self)                
        if not JournalMsr.MyLoadUi(path_ui, "clsmsr.ui", self):
            self.is_show = False
            return



        '''
        QMessageBox.warning(self, u"Предупреждение", u"444", QMessageBox.Ok)
        os.system('d:/PROJECTS/C#/QRCode/QRCode/QRCode/bin/Debug/qrCode.exe YUIOP')
        QMessageBox.warning(self, u"Предупреждение", u"555", QMessageBox.Ok)
'''



        self.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_3.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_4.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_5.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_6.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_7.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_8.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_9.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_10.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_11.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_12.setIcon(QIcon(u':/ico/ico/pencil_64.png'))

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

        self.connect(self.splitter, QtCore.SIGNAL('splitterMoved(int,int)'), self.splitMoved)

        self.tableView.setModel(model)
        self.selModel = self.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)

        self.tableView_2.setModel(model2)
        self.selModel2 = self.tableView_2.selectionModel()
        self.connect(self.selModel2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged2)
        
        self.tableView_3.setModel(model3)
        self.selModel3 = self.tableView_3.selectionModel()
        self.connect(self.selModel3, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged3)
        
        self.tableView_4.setModel(model4)
        self.selModel4 = self.tableView_4.selectionModel()
        self.connect(self.selModel4, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged4)

        self.comboBox.currentIndexChanged.connect(self.comboBox_indexChanged)        
        self.withCol1 = 200
        self.withCol2 = 100
        self.withCol3 = 100                        
        self.withCol4 = 50                        
        self.withCol5 = 50                        
        self.withCol6 = 50                        

        self.label_2.setText("")
        self.label_6.setText("")
        self.label_7.setText("")
        self.comboBox_indexChanged()
#        self.ViewTypeMsr(0, id_category)




    def splitMoved(self, x, y):
        self.resizeEvent(None)


    def ViewTypeMsr(self, id_search, id_category):
        query9 = QSqlQuery(db1)
        query9.prepare(selectTypeMsr)
        query9.bindValue(":id_category", id_category)
        query9.exec_()        
        
        model.setQuery(query9)
                
        self.tableView.setColumnHidden(0, True)        
        self.searchInModel(id_search, self.tableView, model)
        self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.selModel)
                
        '''
        model.setQuery(selectTypeMsr, db1)
        self.tableView.setColumnHidden(0, True)        
        self.searchInModel(id_search, self.tableView, model)
        self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.selModel)
        '''
               

    def ViewGroupMsr(self, id_search, id_type):
        query9 = QSqlQuery(db1)
        query9.prepare(selectGroupMsr)
        query9.bindValue(":id", id_type)
        query9.exec_()        
        
        model4.clear()        
        model4.reset()        
        model3.clear()        
        model3.reset()        
        model2.clear()        
        model2.setQuery(query9)
        self.tableView_2.setColumnHidden(0, True)        
        self.tableView_2.setColumnHidden(1, True)
                
        self.searchInModel(id_search, self.tableView_2, model2)
        self.viewButtons(2, self.pushButton_5, self.pushButton_6, self.pushButton_7, self.selModel2)
        
    def ViewMsr(self, id_search, id_group):
        query9 = QSqlQuery(db1)
        query9.prepare(selectMsr)
        query9.bindValue(":id", id_group)
        query9.exec_()        
        
        model4.clear()        
        model4.reset()        
        model3.clear()        
        model3.setQuery(query9)
        
        model3.setHeaderData(2, QtCore.Qt.Horizontal, u"Наименование")
        if id_category == 1 or id_category == 2:          
            model3.setHeaderData(3, QtCore.Qt.Horizontal, u"Периодичность\nповерки")
            model3.setHeaderData(4, QtCore.Qt.Horizontal, u"Периодичность\nосмотра")
        if id_category == 3:          
            model3.setHeaderData(3, QtCore.Qt.Horizontal, u"Периодичность\nаттестации")
            model3.setHeaderData(4, QtCore.Qt.Horizontal, u"Периодичность\nпроведения ППР")
            
        self.tableView_3.setColumnHidden(0, True)        
        self.tableView_3.setColumnHidden(1, True)





                        
        '''                
        if id_category == 1:
            self.tableView_3.setColumnHidden(4, True)
            self.label_5.setText(u'Виды измерения')
        else:            
            self.tableView_3.setColumnHidden(4, False)        
            self.label_5.setText(u'Виды защиты')
        '''    

        self.resizeEvent(True)
        self.tableView_3.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.searchInModel(id_search, self.tableView_3, model3)
#        self.searchInModel(0, self.tableView_3, model3)
#        QMessageBox.warning(self, u"Предупреждение", u"444", QMessageBox.Ok)
        self.viewButtons(3, self.pushButton_8, self.pushButton_9, self.pushButton_10, self.selModel3)              

    def ViewAccuracy(self, id_search, id_msr):
        query9 = QSqlQuery(db1)
        query9.prepare(selectAccuracy)
        query9.bindValue(":id", id_msr)
        query9.exec_()        
        
        model4.clear()        
        model4.setQuery(query9)

        global id_category
        model4.setHeaderData(2, QtCore.Qt.Horizontal, u"Вид измерения")
        if id_category == 1 or id_category == 2:          
            model4.setHeaderData(3, QtCore.Qt.Horizontal, u"Диапазон измерения")
            model4.setHeaderData(4, QtCore.Qt.Horizontal, u"Класс точности")
        if id_category == 3:          
            model4.setHeaderData(3, QtCore.Qt.Horizontal, u"Номинальное знач.\nхарактеристики")
            model4.setHeaderData(4, QtCore.Qt.Horizontal, u"Допустимое\nотклонение")
        
        self.tableView_4.setColumnHidden(0, True)        
        self.tableView_4.setColumnHidden(1, True)        
        self.resizeEvent(True)

        self.searchInModel(id_search, self.tableView_4, model4)
        self.viewButtons(4, self.pushButton_11, self.pushButton_12, self.pushButton_12, self.selModel4)

    # Поиск в модели по идентификатору: id_search и позиционирование на соответствующую позицию в гриде 
    def searchInModel(self, id_search, tableView, model):
        if id_search == -1:  # При удалении записи
            return
        if id_search == 0:
            if tableView.size() > 0:   # Грубая защита от ошибки позиционирования
                tableView.selectRow(0)
        else:
            if model.query().size() < 1:  # Грубая защита от зацикливания
                return
            # Навигация на измененную позицию
            model.query().first();
            i = 0
            while model.query().value(0).toString() != id_search:
                model.query().next()
                i += 1
            tableView.selectRow(i)
                      

    def selectionChanged1(self):
        global id_type
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        id_type = model.record(row).field('id').value().toString() 
        self.label_7.setText("")
        self.label_6.setText("")
        self.label_2.setText(model.record(row).field('name_type').value().toString()) 
        self.ViewGroupMsr(0, id_type)  
       
    def selectionChanged2(self):
        global id_group
        row = self.selModel2.currentIndex().row()
        if row == -1:
            return
        id_group = model2.record(row).field('id').value().toString()   
        self.label_7.setText("")
        self.label_6.setText(model2.record(row).field('name_group').value().toString()) 
        self.ViewMsr(0, id_group)
                 
    def selectionChanged3(self):
        global id_msr        
        row = self.selModel3.currentIndex().row()
        if row == -1:
            return
        id_msr = model3.record(row).field('id').value().toString()   
        self.label_7.setText(model3.record(row).field('name_msr').value().toString()) 
        self.ViewAccuracy(0, id_msr)
                                  
    def selectionChanged4(self):
        global id_accuracy        
        row = self.selModel4.currentIndex().row()
        if row == -1:
            return
        id_accuracy = model4.record(row).field('id').value().toString()   
                 
# Редактирование видов измерения (начало кода)        
              
    def pushButton_Click(self):
        self.wind1 = self.editType()
        #self.wind1.tag = 1
        if self.wind1.tag == 0:
            return
                
#        self.wind1.setWindowTitle(u'Добавление нового вида измерения')
        self.wind1.setWindowTitle(u'Добавление новой позиции')
        self.wind1.exec_()
        self.ViewTypeMsr(id_type, id_category)
                
    def pushButton2_Click(self):        
        if model2.rowCount() > 0:
            QMessageBox.warning(self, u"Предупреждение", u"Удаление текущей позиции невозможно,\n\r поскольку она содержит группы средств измерения!", QMessageBox.Ok)
            return
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM type_msr WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.ViewTypeMsr(0, id_category)
            
            #model.setQuery(selectTypeMsr, db1)
            
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView.selectRow(row)                                    
            self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.selModel)
                        
            
    def pushButton3_Click(self):
        global id_type, name_type
        self.wind1 = self.editType()
        if self.wind1.tag == 0:
            return
        self.wind1.tag = 2
#        self.wind1.setWindowTitle(u'Редактирование текущего вида измерения')
        self.wind1.setWindowTitle(u'Редактирование текущей позиции')
        row = self.selModel.currentIndex().row()
        self.wind1.lineEdit.setText(model.record(row).field('name_type').value().toString())
        self.wind1.exec_()
        self.ViewTypeMsr(id_type, id_category)
                        
                        
    class editType(QtGui.QDialog):
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
#            uic.loadUi(path_ui + "editType.ui", self)
            if not JournalMsr.MyLoadUi(path_ui, "editType.ui", self):
                return
                      
            global id_category
            if id_category == 1:          
                self.label.setText(u'Вид измерения')            
            if id_category == 2:          
                self.label.setText(u'Вид защиты')            
            if id_category == 3:          
                self.label.setText(u'Вид испытательного оборуд.')            
            self.pushButton.clicked.connect(self.pushButton1_Click)
        
        def pushButton1_Click(self):
            global id_type
            query = QSqlQuery(db1)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM type_msr");
                query.exec_()
                query.next()
                id_type = query.value(0).toString()
#                query.prepare("INSERT INTO type_msr (id, name_type) VALUES (:id, :name_type)")
                query.prepare("INSERT INTO type_msr (id, name_type, id_category) VALUES (:id, :name_type, :id_category)")
                query.bindValue(":id_category", id_category);
            else:
#                query.prepare("UPDATE type_msr SET name_type = :name_type WHERE id = :id")
                query.prepare("UPDATE type_msr SET name_type = :name_type WHERE id = :id")
            query.bindValue(":id", id_type);
            query.bindValue(":name_type", self.lineEdit.text())
                    
            query.exec_()                        
            self.close()
# Редактирование видов измерения (конец кода)        


# Редактирование групп средств измерения (начало кода)        
    def pushButton4_Click(self):
        self.wind2 = self.editGroup()
#        self.wind2.tag = 1
        if self.wind2.tag == 0:
            return
        
        self.wind2.setWindowTitle(u'Добавление новой группы средств измерения')
        self.wind2.exec_()
        self.ViewGroupMsr(id_group, id_type)

    def pushButton5_Click(self):       
        if model3.rowCount() > 0:
            QMessageBox.warning(self, u"Предупреждение", u"Удаление текущей позиции невозможно,\n\r поскольку она содержит средства измерения!", QMessageBox.Ok)
            return
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM group_msr WHERE id = :ID")
            row = self.selModel2.currentIndex().row()                
            query.bindValue(":id", model2.record(row).field('id').value().toString());
            query.exec_()
            self.ViewGroupMsr(-1, id_type)
            
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_2.selectRow(row)                                    
            self.viewButtons(2, self.pushButton_5, self.pushButton_6, self.pushButton_7, self.selModel2)


    def pushButton6_Click(self):
        self.wind2 = self.editGroup()
        if self.wind2.tag == 0:
            return        
        self.wind2.tag = 2
        self.wind2.setWindowTitle(u'Редактирование текущей группы измерения')
        row = self.selModel2.currentIndex().row()
        self.wind2.lineEdit.setText(model2.record(row).field('name_group').value().toString())
        self.wind2.exec_()                
        self.ViewGroupMsr(id_group, id_type)


    class editGroup(QtGui.QDialog):    
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
#            uic.loadUi(path_ui + "editGroup.ui", self)
            if not JournalMsr.MyLoadUi(path_ui, "editGroup.ui", self):
                return
            
            self.label_2.setVisible(False)            
            self.lineEdit_2.setVisible(False)            
            
            
            
            
            self.pushButton.clicked.connect(self.pushButton1_Click)
        
        def pushButton1_Click(self):
            global id_type
            global id_group
            query = QSqlQuery(db1)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM group_msr");
                query.exec_()
                query.next()
                id_group = query.value(0).toString()
                query.prepare("INSERT INTO group_msr (id, id_type, name_group) VALUES (:id, :id_type, :name_group)")
            else:
                query.prepare("UPDATE group_msr SET id_type = :id_type, name_group = :name_group WHERE id = :id")
            query.bindValue(":id", id_group);
            query.bindValue(":id_type", id_type);                
            query.bindValue(":name_group", self.lineEdit.text())                    
            query.exec_()
            self.close()
# Редактирование групп средств измерения (конец кода)        


# Редактирование средств измерения (начало кода)        
    def pushButton7_Click(self):
        #print 'pushButton7_Click'
        #QMessageBox.warning(self, u"Предупреждение", u"pushButton7_Click", QMessageBox.Yes, QMessageBox.No)            
        self.wind3 = self.editMsr()
#        self.wind3.tag = 1
        if self.wind3.tag == 0:
            return
        
#        self.wind3.setWindowTitle(u'Добавление нового средств измерения')
        self.wind3.setWindowTitle(u'Добавление нового позиции')
        self.wind3.spinBox.setValue(12)
        self.wind3.spinBox_2.setValue(6)
        self.wind3.exec_()
        self.ViewMsr(id_msr, id_group)

    def pushButton8_Click(self):       
        if model4.rowCount() > 0:
            QMessageBox.warning(self, u"Предупреждение", u"Удаление текущей позиции невозможно,\n\r поскольку она содержит классы точности!", QMessageBox.Ok)
            return
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM msr WHERE id = :ID")
            row = self.selModel3.currentIndex().row()                
            query.bindValue(":id", model3.record(row).field('id').value().toString())
            query.exec_()

            self.ViewMsr(-1, id_group)
            
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_3.selectRow(row)                                    
            self.viewButtons(3, self.pushButton_8, self.pushButton_9, self.pushButton_10, self.selModel3)

    def pushButton9_Click(self):
        self.wind3 = self.editMsr()
        if self.wind3.tag == 0:
            return        
        self.wind3.tag = 2
#        self.wind3.setWindowTitle(u'Редактирование текущей средства измерения')
        self.wind3.setWindowTitle(u'Редактирование текущей позиции')
        row = self.selModel3.currentIndex().row()
        self.wind3.lineEdit.setText(model3.record(row).field('name_msr').value().toString())
        self.wind3.spinBox.setValue(int(model3.record(row).field('period').value().toString()))
        self.wind3.spinBox_2.setValue(int(model3.record(row).field('period_view').value().toString()))
        self.wind3.exec_()                
        self.ViewMsr(id_msr, id_group)


    class editMsr(QtGui.QDialog):    
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
#            uic.loadUi(path_ui + "editMsr.ui", self)
            if not JournalMsr.MyLoadUi(path_ui, "editMsr.ui", self):
                return            
            #l = QtGui.QLabel
            #l.isVisible()
            if id_category == 1 or id_category == 2:
                self.label_4.setText(u'Периодичность поверки (мес)')
                self.label_2.setText(u'Периодичность осмотра (мес)')
            if id_category == 3:
                self.label_4.setText(u'Периодичность аттестации (мес)')
                self.label_2.setText(u'Периодичность проведения ППР (мес)')
                
            self.label_2.setVisible(id_category == 2 or id_category == 3)
            self.spinBox_2.setVisible(id_category == 2 or id_category == 3)
#            print self.pushButton.text()
            self.pushButton.clicked.connect(self.pushButton1_Click)
        
        def pushButton1_Click(self):
            global id_group
            global id_msr
            query = QSqlQuery(db1)
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM msr");
                query.exec_()
                query.next()
                id_msr = query.value(0).toString()
                if id_category == 1:                    
                    query.prepare("INSERT INTO msr (id, id_group, name_msr, period) VALUES (:id, :id_group, :name_msr, :period)")
                if id_category == 2 or id_category == 3:                    
                    query.prepare("INSERT INTO msr (id, id_group, name_msr, period, period_view) VALUES (:id, :id_group, :name_msr, :period, :period_view)")
            else:
                if id_category == 1:                    
                    query.prepare("UPDATE msr SET id_group = :id_group, name_msr = :name_msr, period = :period WHERE id = :id")
                if id_category == 2 or id_category == 3:                    
                    query.prepare("UPDATE msr SET id_group = :id_group, name_msr = :name_msr, period = :period, period_view =:period_view WHERE id = :id")
            query.bindValue(":id", id_msr);
            query.bindValue(":id_group", id_group);                
            query.bindValue(":name_msr", self.lineEdit.text())            
            query.bindValue(":period", self.spinBox.text())
#            if id_category == 1:                    
#                query.bindValue(":period_view", null)
            if id_category == 2 or id_category == 3:                    
                query.bindValue(":period_view", self.spinBox_2.text())
#            query.                        
            query.exec_()
            self.close()            
# Редактирование средств измерения (конец кода)        


# Редактирование классов точности (начало кода)        
    def pushButton10_Click(self):
        self.wind4 = self.editAccuracy()
        #self.wind4.tag = 1
        if self.wind4.tag == 0:
            return        
        self.wind4.setWindowTitle(u'Добавление нового класса точности')
        self.wind4.exec_()        
        self.ViewAccuracy(id_accuracy, id_msr)

    def pushButton11_Click(self):       
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM accuracy_msr WHERE id = :ID")
            row = self.selModel4.currentIndex().row()                
            query.bindValue(":id", model4.record(row).field('id').value().toString())
            query.exec_()

            self.ViewAccuracy(-1, id_msr)
            
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView_4.selectRow(row)                                    
            self.viewButtons(4, self.pushButton_11, self.pushButton_12, self.pushButton_12, self.selModel4)

    def pushButton12_Click(self):
        self.wind4 = self.editAccuracy()
        if self.wind4.tag == 0:
            return        
        self.wind4.tag = 2
        self.wind4.setWindowTitle(u'Редактирование текущего класса точности')
        row = self.selModel4.currentIndex().row()
        self.wind4.lineEdit.setText(model4.record(row).field('name_vid').value().toString())
        self.wind4.lineEdit_2.setText(model4.record(row).field('range_msr').value().toString())
        self.wind4.lineEdit_3.setText(model4.record(row).field('classaccuracy').value().toString())
        self.wind4.exec_()                
        self.ViewAccuracy(id_accuracy, id_msr)

    class editAccuracy(QtGui.QDialog):    
        def __init__(self, *args):
            QtGui.QDialog.__init__(self, *args)
#            uic.loadUi(path_ui + "editAccuracy.ui", self)
            if not JournalMsr.MyLoadUi(path_ui, "editAccuracy.ui", self):
                return
            
            self.pushButton.clicked.connect(self.pushButton1_Click)
                
            self.lineEdit = MLineEdit(self, u"±≤≥≠º√¶^²³")
            self.lineEdit.setMaxLength(100)
            self.horizontalLayout.addWidget(self.lineEdit)
            self.lineEdit_2 = MLineEdit(self, u"±≤≥≠º√¶^²³")
            self.lineEdit_2.setMaxLength(60)
####            self.horizontalLayout_3.addWidget(self.lineEdit_2)
            self.verticalLayout_2.addWidget(self.lineEdit_2)
            self.lineEdit_3 = MLineEdit(self, u"±≤≥≠º√¶^²³")
            self.lineEdit_3.setMaxLength(100)
            self.horizontalLayout_4.addWidget(self.lineEdit_3)
                         
            
            if id_category == 1 or id_category == 2:
                self.label_2.setText(u'Диапазон измерения')
                self.label_3.setText(u'Класс точности')
            if id_category == 3:
                self.label_2.setText(u'Номинальное значение характеристики')
                self.label_3.setText(u'Допустимое отклонение')
            
            
            
            
            
            
            
        def pushButton1_Click(self):
            global id_msr
            global id_accuracy
            query = QSqlQuery(db1)
            if self.tag == 1: 
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM accuracy_msr");
                query.exec_()
                query.next()
                id_accuracy = query.value(0).toString()
                query.prepare("INSERT INTO accuracy_msr (id, id_msr, name_vid, range_msr, classaccuracy) VALUES (:id, :id_msr, :name_vid, :range_msr, :classaccuracy)")
            else:
                query.prepare("UPDATE accuracy_msr SET id_msr = :id_msr, name_vid = :name_vid, range_msr = :range_msr, classaccuracy = :classaccuracy WHERE id = :id")
            query.bindValue(":id", id_accuracy);
            query.bindValue(":id_msr", id_msr);                
            query.bindValue(":name_vid", self.lineEdit.text())
            query.bindValue(":range_msr", self.lineEdit_2.text())
            query.bindValue(":classaccuracy", self.lineEdit_3.text())
            query.exec_()
            self.close()            
# Редактирование классов точности (конец кода)        
                        
                                
# Определяет состояние кнопок редактирования
    def viewButtons(self, n, button1, button2, button3, selModel):
        enab = selModel.currentIndex().row() >= 0
        button1.setEnabled(enab)
        button2.setEnabled(enab)
        button3.setEnabled(enab)
        
        if enab == False:
            if n < 4:
                self.pushButton_10.setEnabled(False)
                self.pushButton_11.setEnabled(False)
                self.pushButton_12.setEnabled(False)
            if n < 3:
                self.pushButton_7.setEnabled(False)
                self.pushButton_8.setEnabled(False)
                self.pushButton_9.setEnabled(False)
            if n < 2:
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_6.setEnabled(False)
                
                
        if self.pushButton.isEnabled():                
            self.pushButton.setToolTip(u'добавить вид измерения')
        else:    
            self.pushButton.setToolTip(u'')
        if self.pushButton_2.isEnabled():                
            self.pushButton_2.setToolTip(u'удалить вид измерения')
        else:    
            self.pushButton_2.setToolTip(u'')
        if self.pushButton_3.isEnabled():                
            self.pushButton_3.setToolTip(u'редактировать вид измерения')
        else:    
            self.pushButton_3.setToolTip(u'')
        if self.pushButton_4.isEnabled():                
            self.pushButton_4.setToolTip(u'добавить группу средств измерения')
        else:    
            self.pushButton_4.setToolTip(u'')
        if self.pushButton_5.isEnabled():                
            self.pushButton_5.setToolTip(u'удалить группу средств измерения')
        else:    
            self.pushButton_5.setToolTip(u'')
        if self.pushButton_6.isEnabled():                
            self.pushButton_6.setToolTip(u'редактировать группу средств измерения')
        else:    
            self.pushButton_6.setToolTip(u'')
        if self.pushButton_7.isEnabled():                
            self.pushButton_7.setToolTip(u'добавить средство измерения')
        else:    
            self.pushButton_7.setToolTip(u'')
        if self.pushButton_8.isEnabled():                
            self.pushButton_8.setToolTip(u'удалить средство измерения')
        else:    
            self.pushButton_8.setToolTip(u'')
        if self.pushButton_9.isEnabled():                
            self.pushButton_9.setToolTip(u'редактировать средство измерения')
        else:    
            self.pushButton_9.setToolTip(u'')
        if self.pushButton_10.isEnabled():                
            self.pushButton_10.setToolTip(u'добавить класс точности измерения')
        else:    
            self.pushButton_10.setToolTip(u'')
        if self.pushButton_11.isEnabled():                
            self.pushButton_11.setToolTip(u'удалить класс точности измерения')
        else:    
            self.pushButton_11.setToolTip(u'')
        if self.pushButton_12.isEnabled():                
            self.pushButton_12.setToolTip(u'редактировать класс точности измерения')
        else:    
            self.pushButton_12.setToolTip(u'')
                
                
                    
    def resizeEvent( self, event ):
        #print "resizeEvent"
#        koef = (1.0 * (self.tableView_3.width() - 20) / (self.withCol1 + self.withCol2))
        if id_category == 1:
            withCol3 = 0
        else:    
            withCol3 = self.withCol3            

        koef = (1.0 * (self.tableView_3.width() - 20) / (self.withCol1 + self.withCol2 + withCol3))
        self.tableView_3.setColumnWidth(2, koef * self.withCol1)
        self.tableView_3.setColumnWidth(3, koef * self.withCol2)
        self.tableView_3.setColumnWidth(4, koef * withCol3)
        koef = (1.0 * (self.tableView_4.width() - 20) / (self.withCol4 + self.withCol5 + self.withCol6))
        self.tableView_4.setColumnWidth(2, koef * self.withCol4)
        self.tableView_4.setColumnWidth(3, koef * self.withCol5)
        self.tableView_4.setColumnWidth(4, koef * self.withCol6)                    

    def comboBox_indexChanged(self):
        #self.label_3.setEnabled(self.comboBox.currentIndex() == 0)
        #self.spinBox.setEnabled(self.comboBox.currentIndex() == 0)
        print 'self.comboBox.currentIndex()=', self.comboBox.currentIndex()
        model4.clear()        
        model4.reset()        
        model3.clear()        
        model3.reset()        
        model2.clear()        
        model2.reset()        
        global id_category
        id_category = self.comboBox.currentIndex() + 1
        
        print 'id_category id_category id_category id_category id_category id_category = ', id_category
        
        if id_category == 1:
            self.tableView_3.setColumnHidden(4, True)
            self.label_5.setText(u'Виды измерения')
            self.label.setText(u'Тип, заводское обозначение средства измерения')
        if id_category == 2:
            self.tableView_3.setColumnHidden(4, False)        
            self.label_5.setText(u'Виды защиты')
            self.label.setText(u'Тип, заводское обозначение средства защиты')
        if id_category == 3:
            self.tableView_3.setColumnHidden(4, False)        
            self.label_5.setText(u'Виды испытательного оборудования')
            self.label.setText(u'Наименование, заводское обозначение испытательного оборудования')
                
        self.ViewTypeMsr(0, id_category)
        
                    
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
        
        wind = classMsr(env)
    #    wind = ClsTrans(env, 0)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
    
    
    '''
    import sys
    app = QtGui.QApplication(sys.argv)
    db = QSqlDatabase("QPSQL")
    db.setHostName("localhost")
    db.setDatabaseName("electrolab1")
    db.setUserName("postgres")
    db.setPassword("electrolab")
    rez = db.open();
    
    class Env():
        class config():
            class paths():
                pass    
    env = Env()
    env.db = db    
    env.config.paths.ui = "ui"

    wind = classMsr(env)
    if wind.tag <> 0:        
        wind.show()
        wind.resizeEvent(None)
    sys.exit(app.exec_())
'''
    