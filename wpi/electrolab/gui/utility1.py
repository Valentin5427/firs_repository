# -*- coding: UTF-8 -*-
#

#from PyQt4.QtGui import QMessageBox, QDateEdit, QIcon, QCheckBox, QColor

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont,       QDoubleSpinBox,         QToolButton
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery


from electrolab.gui.common import UILoader


model = QSqlQueryModel()
model_2 = QSqlQueryModel()


class utility1(QWidget, UILoader):    
    def __init__(self, _env):
        
        super(QWidget, self).__init__()

       # QMessageBox.warning(self, u"Предупреждение", u"В БД", QMessageBox.Yes, QMessageBox.No)                        



                
        self.setUI(_env.config, u"utility1.ui")


        if not self.TestBase(_env.db):
            return

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)        




    def pushButton_Click(self):
        
        I = [0.014,0.026,0.029,0.03,0.032,0.033,0.036,0.038,0.04,0.045,0.048,0.052,0.056,0.063,0.066,0.071,0.098,0.169,0.421,1.233,2.141,2.956,3.84,4.597,5.288,5.932,6.581,7.287,7.837,8.47,8.978,9.423,9.798,10.105]
        U = [0.144,0.688,1.909,2.731,3.508,4.229,4.962,5.694,6.438,7.182,8.303,9.058,9.823,10.589,11.093,11.344,12.121,12.876,13.908,14.441,14.763,14.918,14.985,15.04,15.085,15.14,15.185,15.218,15.262,15.296,15.34,15.373,15.429,15.462]        
        
        for i in range(len(I) - 1):
            print I[i+1] - I[i],  U[i+1] - U[i], 100 * ((U[i+1] - U[i]) / (I[i+1] - I[i]))  #  1000 * ((I[i+1] - I[i]) / (U[i+1] - U[i]))
        
        
     #   print len(I) 
     #   print len(U) 
        return
        
        

        query = QSqlQuery(db)

        SQL = u"""
        
update serial_number set
ordernumber = case when substring(ordernumber,1,1)='Б' then substring(ordernumber,2) else ordernumber end,
series = case when substring(series,1,2)='Б-' then substring(series,3) else series end,
replace = case when substring(ordernumber,1,1)='Б' or replace = true then true end
--replace = case when substring(ordernumber,1,1)='Б' then true else null end
where id > 150000
        
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка при выполнении операции", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Преобразование выполнено!", QMessageBox.Ok)            
        return




    def pushButton_2_Click(self):

        query = QSqlQuery(db)

        SQL = u"""
update serial_number set
ordernumber = 'Б'||ordernumber,
series = 'Б-'||series,
replace = null
where id > 150000 and replace = true
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка при выполнении операции!", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Обратное преобразование выполнено!", QMessageBox.Ok)            
        return



    def TestBase(self, db):
        #return True        
        query = QSqlQuery(db)
        print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        query.prepare("select replace from serial_number")
#        query.prepare("select sample from checking_2")
#        query.prepare("select un, inom, k from checking_2")
        if not query.exec_(): err_tbl += "error"
          
        if err_tbl != "":
            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД требуется произвести изменения,
необходимые для работы приложения\n""" +
u"Произвести изменения БД?", QMessageBox.Yes, QMessageBox.No)                        
                        
            if r == QMessageBox.Yes:
                self.InitBase(db)
                return True
            else:
                return False
        return True
                                 

    def InitBase(self, db):
        print u"Инициализация БД"        
        query = QSqlQuery(db)

        SQL = u"""
ALTER TABLE serial_number ADD column replace boolean;
COMMENT ON COLUMN serial_number.replace IS 'Трансформатор изготавливается взамен бракованому';
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
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
        
        wind = utility1(env)
        wind.setEnabled(True)
        #if wind.is_show: 
        wind.show()
        sys.exit(app.exec_())

