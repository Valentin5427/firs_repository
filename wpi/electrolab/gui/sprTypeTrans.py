# -*- coding: UTF-8 -*-
#
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt

import socket
import PyQt4
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.ClsTrans import ClsTrans

import ui.ico_64_rc

import datetime

from datetime import date

id_TypeTransformer = -1
id_TypeTransformersp = -1

model_  = QSqlQueryModel()
model   = QSqlQueryModel()
model_2 = QSqlQueryModel()

from PyQt4.QtGui import QTableView

withCol1 = 80
withCol2 = 100
withCol3 = 100
withCol4 = 50
withCol5 = 50
withCol6 = 50
withCol7 = 50

withCol_1 = 50
withCol_2 = 100
withCol_3 = 100

isSave = False

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
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + withCol7))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            obj.setColumnWidth(5, koef * withCol5)
            obj.setColumnWidth(6, koef * withCol6)
            obj.setColumnWidth(7, koef * withCol7)
            VSB1 = obj.verticalScrollBar().isVisible()

        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3))
            obj.setColumnWidth(1, koef * withCol_1)
            obj.setColumnWidth(2, koef * withCol_2)
            obj.setColumnWidth(3, koef * withCol_3)
            VSB2 = obj.verticalScrollBar().isVisible()


        return False


class sprTypeTransformer(QWidget, UILoader):    
    def __init__(self, _env):
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"sprTypeTrans.ui")        
        
        self.setWindowTitle(u"Справочник типов трансформанора")
                
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

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)
        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()                
        self.connect(self.selModel_2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged_2)

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))
        self.ui.tableView_2.setObjectName('tv2')
              
        global currColumnIndex
        currColumnIndex = 1
        global desc
        desc = ''
        self.selTypeTransformer(currColumnIndex, False)

# Настройка сортировки при нажатии колонки      
# пример     https://coderoad.ru/14068823/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D1%8B-%D0%B4%D0%BB%D1%8F-QTableView-%D0%B2-PyQt

        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.sortByColumn)


    def sortByColumn(self, columnIndex):
        print 'sortByColumn sortByColumn sortByColumn sortByColumn sortByColumn  ', columnIndex
        self.selTypeTransformer(columnIndex, False)


      
# Редактирование трансформатора (начало кода)                      
    def pushButton_Click(self):
        global isSave        
        self.wind = self.editTypeTransformer(self.env)
        self.wind.tag = 1
        self.wind.setWindowTitle(u'Добавление нового типа')
        self.wind.ui.dateEdit.setDate(datetime.date.today())   
        row = self.selModel.currentIndex().row()
                
        isSave = False        
        self.wind.exec_()
        if isSave:
            self.selTypeTransformer(currColumnIndex, True)
            
            #Вычисление максимального id и навигация на него
            global id_search
            query = QSqlQuery(db1)
            query.prepare("SELECT MAX(id) FROM type_transformer");
            query.exec_()
            query.next()
            id_search = query.value(0).toString()
            self.searchInModel(id_search, self.ui.tableView, model)            
            
                
    def pushButton_2_Click(self):
        global isSave        
        global id_TypeTransformer
        self.wind = self.editTypeTransformer(self.env)
        self.wind.tag = 2
        self.wind.setWindowTitle(u'Редактирование текущего типа трансформатора')
        row = self.selModel.currentIndex().row()
               
        id_TypeTransformer = int(model.record(row).field('id').value().toString())        
        self.wind.ui.lineEdit.setText(model.record(row).field('type').value().toString())        
        self.wind.ui.lineEdit_2.setText(model.record(row).field('tu').value().toString())        
        self.wind.ui.lineEdit_3.setText(model.record(row).field('method').value().toString())        
        self.wind.ui.lineEdit_4.setText(model.record(row).field('number_reestr').value().toString())        
        self.wind.ui.lineEdit_5.setText(model.record(row).field('declaration').value().toString())        
        self.wind.ui.spinBox.setValue(int(model.record(row).field('interval').value().toString()))
        self.wind.ui.dateEdit.setDate(model.record(row).field('change_date').value().toDate())                     

        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selTypeTransformer(currColumnIndex, True)
            self.ui.tableView.selectRow(row)                                            


    def pushButton_3_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM type_transformer WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            self.selTypeTransformer(currColumnIndex, True)                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView.selectRow(row)                                    


    def pushButton_4_Click(self):
        global isSave        
        self.wind = self.editTypeTransformersp(self.env)
        self.wind.ui.label_5.setVisible(False)
        self.wind.ui.label_2.setVisible(False)
        self.wind.ui.label_3.setVisible(False)
        self.wind.ui.label_7.setVisible(False)
        self.wind.ui.lineEdit_4.setVisible(False)
        self.wind.ui.lineEdit_5.setVisible(False)
        self.wind.ui.spinBox.setVisible(False)
        self.wind.ui.dateEdit.setVisible(False)
        self.wind.ui.lineEdit_3.setMaxLength(40)
        self.wind.ui.label_6.setText(u"Вариант конструктивного исполнения")
        self.wind.ui.label.setText(u"Обозначение ПС")
        self.wind.ui.label_4.setText(u"Руководство РЭ")
                
        self.wind.tag = 1
                
        self.wind.setWindowTitle(u'Добавление новой позиции')
        isSave = False        
        isSave = True        
        self.wind.exec_()
        if isSave:
            self.selTypeTransformersp()
            
                
    def pushButton_5_Click(self):
        global isSave        
        self.wind = self.editTypeTransformersp(self.env)
        self.wind.tag = 2
        self.wind.ui.label_5.setVisible(False)
        self.wind.ui.label_2.setVisible(False)
        self.wind.ui.label_3.setVisible(False)
        self.wind.ui.label_7.setVisible(False)
        self.wind.ui.lineEdit_4.setVisible(False)
        self.wind.ui.lineEdit_5.setVisible(False)
        self.wind.ui.spinBox.setVisible(False)
        self.wind.ui.dateEdit.setVisible(False)
        self.wind.ui.lineEdit_3.setMaxLength(40)
        self.wind.ui.label_6.setText(u"Вариант конструктивного исполнения")
        self.wind.ui.label.setText(u"Обозначение ПС")
        self.wind.ui.label_4.setText(u"Руководство РЭ")
        self.wind.setWindowTitle(u'Редактирование текущей позиции')
        row = self.selModel_2.currentIndex().row()
                
        if model_2.record(row).field('var_constr_isp').value().toString() != '':
            self.wind.ui.lineEdit.setText(model_2.record(row).field('var_constr_isp').value().toString())
        if model_2.record(row).field('designation').value().toString() != '':
            self.wind.ui.lineEdit_2.setText(model_2.record(row).field('designation').value().toString())
        if model_2.record(row).field('manual').value().toString() != '':
            self.wind.ui.lineEdit_3.setText(model_2.record(row).field('manual').value().toString())
                    
        isSave = False        
        self.wind.exec_()        
        if isSave:
            self.selTypeTransformersp()
            # навигация
            self.ui.tableView_2.selectRow(row)                                    

            
    def pushButton_6_Click(self):        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:            
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM type_transformersp WHERE id = :ID")
            row = self.selModel_2.currentIndex().row()                
            query.bindValue(":id", model_2.record(row).field('id').value().toString());
            query.exec_()
            self.selTypeTransformersp()
                                
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.ui.tableView_2.selectRow(row)                                    


            
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
                model.query().next()
                if i + 1 == int(model.query().size()):
                    break
                i += 1
            tableView.selectRow(i)
            
    def selTypeTransformer(self, columnIndex, isEdit):
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
                        
        query = QSqlQuery(db1)
                                
        SQL = """select id,
        type,
        tu,
        method,
        number_reestr,
        declaration,
        interval,
        change_date
        from type_transformer
        """
                
        if columnIndex == 0:            
            SQL += """order by type
                   """
        if columnIndex == 1:            
            SQL += """order by type """ + desc + """
                   """
        if columnIndex == 2:            
            SQL += """order by tu """ + desc + """, type
                   """
        if columnIndex == 3:            
            SQL += """order by method """ + desc + """, type
                   """
        if columnIndex == 4:            
            SQL += """order by number_reestr """ + desc + """, type
                   """
        if columnIndex == 5:            
            SQL += """order by declaration """ + desc + """, type
                   """
        if columnIndex == 6:            
            SQL += """order by interval """ + desc + """, type
                   """
        if columnIndex == 7:            
            SQL += """order by change_date """ + desc + """, type
                   """

        """select id,
        type,
        tu,
        method,
        number_reestr,
        declaration,
        interval,
        change_date
        """
                
        query.prepare(SQL)
            
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model.setQuery(query)

        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Тип\nтрансформатора")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Технические\nусловия")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Методика\nповерки")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Номер в\nГосреестре")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Декларация")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Межповерочный\nинтервал(лет)")
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Дата внесения\nизменения")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        self.ui.tableView.setColumnWidth(3,  withCol3)
        self.ui.tableView.setColumnWidth(4,  withCol4)
        self.ui.tableView.setColumnWidth(5,  withCol5)
        self.ui.tableView.setColumnWidth(6,  withCol6)
        self.ui.tableView.setColumnWidth(6,  withCol7)
        
        self.ui.tableView.setColumnHidden(0, True)
        self.ui.tableView.selectRow(0)
                
        enab = self.selModel.currentIndex().row() >= 0        
        self.ui.pushButton_2.setEnabled(enab)
        self.ui.pushButton_3.setEnabled(enab)


    def selTypeTransformersp(self):           
        row = self.selModel.currentIndex().row()
        global id_TypeTransformer
        if row < 0:
            id_TypeTransformer = -1
        else:    
            id_TypeTransformer = int(model.record(row).field('id').value().toString())
                         
        query = QSqlQuery(db1)
                                
        SQL = """select id,
        var_constr_isp,
        designation,
        manual
        from type_transformersp
        where type_transformer = :id_TypeTransformer
        order by id
        """
        
        query.prepare(SQL)
            
        query.bindValue(":type_transformer", id_TypeTransformer)
                    
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + query.lastError().text(), QMessageBox.Ok)
            
        model_2.setQuery(query)
        model_2.setHeaderData(1, QtCore.Qt.Horizontal, u"Вариант\nконструктивного\nисполнения")
        model_2.setHeaderData(2, QtCore.Qt.Horizontal, u"Обозначение ПС")
        model_2.setHeaderData(3, QtCore.Qt.Horizontal, u"Руководство РЭ")
            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

        self.ui.tableView_2.setColumnWidth(1,  withCol1)
        self.ui.tableView_2.setColumnWidth(2,  withCol2)
        self.ui.tableView_2.setColumnWidth(3,  withCol3)
        
        self.ui.tableView_2.setColumnHidden(0, True)
        self.ui.tableView_2.selectRow(0)
                
        enab = self.selModel_2.currentIndex().row() >= 0        
        self.ui.pushButton_5.setEnabled(enab)
        self.ui.pushButton_6.setEnabled(enab)


    def selectionChanged(self):
        self.selTypeTransformersp()

    def selectionChanged_2(self):
        global id_TypeTransformersp
        row = self.selModel_2.currentIndex().row()
        id_TypeTransformersp = model_2.record(row).field('id').value().toString()


# Редактирование типов трансформатора (начало кода)        
                        
    class editTypeTransformer(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            self.env = _env
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editTypeTransformer.ui")        
                                    
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton_Click)
            
            self.ui.lineEdit.setFocus()

        
        def pushButton_Click(self):
            global id_TypeTransformer
                        
            if self.ui.lineEdit.text().trimmed() == '':
                QMessageBox.warning(self, u"Предупреждение",  u'Введи тип трансформатора', QMessageBox.Ok)
                return
                
            global isSave        
            query = QSqlQuery(db1)
            if self.tag == 1:
                SQL = '''INSERT INTO type_transformer (type, tu, method, number_reestr, declaration, interval, change_date)
                                            values (:type, :tu, :method, :number_reestr, :declaration, :interval, :change_date)'''                                            
                query.prepare(SQL)
            else:
                SQL ='''UPDATE type_transformer SET type = :type,
                                                    tu = :tu,
                                                    method = :method,
                                                    number_reestr = :number_reestr,
                                                    declaration = :declaration,
                                                    interval = :interval,
                                                    change_date = :change_date
                                 WHERE id = :id'''                
                                
                query.prepare(SQL)

                query.bindValue(":id", id_TypeTransformer);
                
                
            query.bindValue(":type", self.ui.lineEdit.text())            
            query.bindValue(":tu", self.ui.lineEdit_2.text())            
            query.bindValue(":method", self.ui.lineEdit_3.text())            
            query.bindValue(":number_reestr", self.ui.lineEdit_4.text())            
            query.bindValue(":declaration", self.ui.lineEdit_5.text())            
            query.bindValue(":interval", self.ui.spinBox.value())            
            query.bindValue(":change_date", self.ui.dateEdit.date())                                    

                        
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка1", SQL +  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close() 
            print SQL                      
            print self.ui.lineEdit_5.text()         
# Редактирование типов трансформатора (конец кода)        
                
                
                
# Редактирование спецификаций к типам трансформаторов (начало кода)        
                        
    class editTypeTransformersp(QtGui.QDialog, UILoader):
        def __init__(self, _env):
            super(QWidget, self).__init__()
            self.setUI(_env.config, u"editTypeTransformer.ui")        
                        
            self.ui.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
            self.ui.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))
            
            self.ui.pushButton.clicked.connect(self.pushButton1_Click)
        
        
        def pushButton1_Click(self):
            
            global id_TypeTransformer
            global id_TypeTransformersp
            global isSave        
            query = QSqlQuery(db1)
            
#            QMessageBox.warning(self, u"Ошибка",  str(id_TypeTransformer), QMessageBox.Ok)
            
            
            if self.tag == 1:
                query.prepare('''INSERT INTO type_transformersp (type_transformer, var_constr_isp, designation, manual) 
                                 values (:type_transformer, :var_constr_isp, :designation, :manual)''')            
                query.bindValue(":type_transformer", id_TypeTransformer);
            else:
                query.prepare('''UPDATE type_transformersp SET var_constr_isp = :var_constr_isp,
                                                 designation = :designation,
                                                 manual = :manual
                                                 WHERE id = :id''')

                query.bindValue(":id", id_TypeTransformersp);
                               
            query.bindValue(":var_constr_isp",   self.ui.lineEdit.text())
            query.bindValue(":designation",   self.ui.lineEdit_2.text())
            query.bindValue(":manual",   self.ui.lineEdit_3.text())

            
            if not query.exec_():
                QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
            else:
                isSave = True        
                self.close()
            
# Редактирование спецификаций к типам трансформаторов (конец кода)        

                
                
                

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
        wind = sprTypeTransformer(env)
        wind.setEnabled(True)
        wind.ui.pushButton_7.setVisible(False)
        wind.ui.pushButton_8.setVisible(False)
        wind.show()
        sys.exit(app.exec_())
        
'''        
CREATE TABLE type_transformer
(
  id serial PRIMARY KEY,
  type character varying(10) NOT NULL,
  tu character varying(30),
  method character varying(30),
  number_reestr character varying(15),
  interval numeric(2),
  change_date date
);

COMMENT ON TABLE type_transformer IS 'Результаты поверки обмоток трансформатора';
COMMENT ON COLUMN type_transformer.id IS 'Первичный ключ';
COMMENT ON COLUMN type_transformer.type IS 'Тип трансформатора';
COMMENT ON COLUMN type_transformer.tu IS 'Технические условия';
COMMENT ON COLUMN type_transformer.method IS 'Методика поверки';
COMMENT ON COLUMN type_transformer.number_reestr IS 'Номер в Госреестре';
COMMENT ON COLUMN type_transformer.interval IS 'Межповерочный интервал';
COMMENT ON COLUMN type_transformer.change_date IS 'Дата внесения изменения';

alter table transformer add column type_transformer integer REFERENCES type_transformer (id)

'''
        
