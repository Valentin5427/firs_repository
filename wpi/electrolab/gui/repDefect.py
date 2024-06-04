# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QMenu, QApplication
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
import datetime

from electrolab.gui.common import UILoader
from PyQt5.QtCore import Qt, QPoint
from electrolab.gui import ReportsExcel

model  = QSqlQueryModel()
model_2  = QSqlQueryModel()
model_3  = QSqlQueryModel()
model_4  = QSqlQueryModel()


class repDefect(QDialog, UILoader):
    def __init__(self, _env):
        
        global db1
        db1 = _env.db
        self.env = _env
        
        super(QWidget, self).__init__()

        self.setUI(_env.config, u"repDefect.ui")
        
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton4_Click)

        self.ui.checkBox.toggled.connect(self.checkBox_Toggle)
        self.ui.checkBox_2.toggled.connect(self.checkBox_2_Toggle)
        self.ui.checkBox_3.toggled.connect(self.checkBox_3_Toggle)
        self.ui.checkBox_4.toggled.connect(self.checkBox_4_Toggle)
        
        self.ui.lineEdit_3.textChanged.connect(self.change_order_number)
        self.ui.sbYear.valueChanged.connect(self.change_serial_number)
        self.ui.sbNumber.valueChanged.connect(self.change_serial_number)
        

        # Организация меню типов трансов
        self.mnu = QMenu(self)
        query = QSqlQuery(db1)
        SQL = '''
select distinct fullname from stand
where id in
(
select distinct stand
from item t1, test_map t4
where t1.createdatetime between to_date('01.05.2021','dd.mm.yyyy') and to_date('01.06.2021','dd.mm.yyyy')
and defect is not null
and t1.test_map = t4.id
)
order by fullname
'''

        query.prepare(SQL)
        query.exec_()                
        model.setQuery(query)        
        for i in range(model.rowCount()):
            action = self.mnu.addAction(model.record(i).field('fullname').value())

        self.mnu.triggered.connect(self.mnu_Click)

        # Организация меню брака
        self.mnu_2 = QMenu(self)
        query = QSqlQuery(db1)
        query.prepare("select id, fullname from defect order by fullname")
        query.exec_()                
        model_2.setQuery(query)        
        for i in range(model_2.rowCount()):
            action = self.mnu_2.addAction(model_2.record(i).field('fullname').value())
            action.setData(model_2.record(i).field('id').value())

        # self.connect(self.mnu_2, QtCore.SIGNAL('triggered(QAction *)'), self.mnu_2_Click)
        self.mnu.triggered.connect(self.mnu_2_Click)

        self.ui.dateEdit.setDate(datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day))        
        self.ui.dateEdit_2.setDate(datetime.date.today())        

        self.ui.sbYear.setValue(datetime.datetime.now().year - 2001)
        
        self.ui.radioButton.setChecked(True)

        self.name_stand = None
        self.id_defect = None
        self.ordernumber = None
        self.id_serial_number = None


    def mnu_Click(self, q):
        self.ui.lineEdit.setText(q.text())

    def mnu_2_Click(self, q):
        #global id_type
        self.id_defect = int(q.data())
        self.ui.lineEdit_2.setText(q.text())

    def pushButton_Click(self):
        self.mnu.exec_(QPoint(self.ui.lineEdit.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit.geometry().height())) 
        

    def pushButton2_Click(self):
#        self.mnu.exec_(QPoint(self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_2.geometry().height())) 
        self.mnu_2.exec_(QPoint(self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).x(), self.ui.lineEdit_2.mapToGlobal(QPoint(0, 0)).y() + self.ui.lineEdit_2.geometry().height())) 

    def pushButton3_Click(self):
        name_stand = None
        id_defect = None
        ordernumber = None
        id_serial_number = None
        
        if self.ui.checkBox.isChecked() and self.ui.lineEdit.text() != "":
            name_stand = self.ui.lineEdit.text()
        if self.ui.checkBox_2.isChecked() and self.ui.lineEdit_2.text() != "":
            id_defect = self.id_defect
        if self.ui.checkBox_3.isChecked() and self.ui.lineEdit_4.text() != "":
            ordernumber = self.ui.lineEdit_3.text()
        if self.ui.checkBox_4.isChecked() and self.ui.leTransformer.text() != "":
            id_serial_number = self.id_serial_number

        if self.ui.radioButton.isChecked():
            sort = 1
        if self.ui.radioButton_2.isChecked():
            sort = 2
        if self.ui.radioButton_3.isChecked():
            sort = 3
        if self.ui.radioButton_4.isChecked():
            sort = 4
        if self.ui.radioButton_5.isChecked():
            sort = 5
            
        ReportsExcel.repDefect(self.env.db, self.ui.dateEdit.date(), self.ui.dateEdit_2.date(), name_stand, id_defect, ordernumber, id_serial_number, sort)


    def pushButton4_Click(self):
        self.close()


    def checkBox_Toggle(self, check):
        self.ui.lineEdit.setEnabled(check)        
        self.ui.pushButton.setEnabled(check)        

    def checkBox_2_Toggle(self, check):
        self.ui.lineEdit_2.setEnabled(check)        
        self.ui.pushButton_2.setEnabled(check)        

    def checkBox_3_Toggle(self, check):
        self.ui.lineEdit_3.setEnabled(check)        

    def checkBox_4_Toggle(self, check):
        self.ui.sbYear.setEnabled(check)        
        self.ui.sbNumber.setEnabled(check)        
                
    def change_order_number(self):
        
        query = QSqlQuery(db1)
        SQL = '''
select t1.id, fullname from serial_number t1, transformer t2
where t1.transformer = t2.id
and ordernumber = :ORDERNUMBER 
order by fullname
'''        
        query.prepare(SQL)
        query.bindValue(":ORDERNUMBER", self.ui.lineEdit_3.text())
        query.exec_()                
        model_3.setQuery(query)
        self.ui.lineEdit_4.setText(str(model_3.rowCount()) + u' трансформ.')        


    def change_serial_number(self):
        self.ui.leTransformer.setText('')
        self.id_serial_number = None        
        query = QSqlQuery(db1)
        SQL = '''
select t1.id, t1.ordernumber, fullname from serial_number t1, transformer t2
where t1.transformer = t2.id
and makedate = :MAKEDATE 
and serialnumber = :SERIALNUMBER 
order by fullname
'''        
        query.prepare(SQL)
        query.bindValue(":MAKEDATE", self.ui.sbYear.value())
        query.bindValue(":SERIALNUMBER", self.ui.sbNumber.value())
        query.exec_()                
        model_4.setQuery(query)

        if model_4.rowCount() > 0:
            self.ui.leTransformer.setText(model_4.record(0).field('fullname').value())
            self.ui.lineEdit_3.setText(model_4.record(0).field('ordernumber').value())
            self.id_serial_number = int(model_4.record(0).field('id').value())
        
        return
        if not (self.ui.sbNumber.value and self.ui.sbYear.value):
            self.ui.leTransformer.clear()
            self.ui.iSerialNumberID = None
            #return
        oSNInfo = self.oHelperSerialNumber.get_id(self.ui.sbYear.value(), self.ui.sbNumber.value())
        if oSNInfo and oSNInfo.id: 
            self.ui.leTransformer.setText(oSNInfo.fullname)
            self.ui.lineEdit_3.setText(oSNInfo.ordernumber)
            self.iSerialNumberID = oSNInfo.id
        else:
            self.ui.leTransformer.clear()
            self.iSerialNumberID = None

                    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
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
    class ForEnv(QWidget):
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
        wind = repDefect(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
