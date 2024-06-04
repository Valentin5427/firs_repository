# -*- coding: UTF-8 -*-

'''
Created on 14.10.2021

@author: atol
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont, QSystemTrayIcon
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox

import time
import os
from collections import OrderedDict
from string import upper

model   = QSqlQueryModel()
model_2   = QSqlQueryModel()
model_3   = QSqlQueryModel()

withCol1 = 100
withCol2 = 30

global id_transes
global flag_exit

class ProgramTray(QtCore.QThread):
#    def __init__(self, icon):
    def __init__(self):
        QtCore.QThread.__init__(self)
        global flag_exit
        flag_exit = True
        print 'ProgramTray'
        

    def run(self):
        print 'run'
        """Код работающий в отдельном потоке"""

        global flag_exit
#        while self.flag_exit:
        while flag_exit:
#            time.sleep(4)
            print "I'm working ..."
            self.emit(QtCore.SIGNAL('treadsignal'))
            print "I'm working222222222222 ..."
            time.sleep(15)
            
            

    def stop(self):
        global flag_exit
        flag_exit = False


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
        koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2))
        obj.setColumnWidth(1, koef * withCol1)
        obj.setColumnWidth(2, koef * withCol2)
        return False


class AutoTypeTrans(QtGui.QDialog, UILoader):
    def __init__(self, _env):

        global db1
        db1 = _env.db
                
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"AutoTypeTrans.ui")
        print '_env.config = ', _env.config
        
        self.setEnabled(False)
        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()        
        self.ui.tableView_2.setModel(model_2)        
        self.selModel_2 = self.ui.tableView_2.selectionModel()        

        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton_4.setVisible(False)
        self.ui.pushButton_5.setVisible(False)
        self.ui.pushButton_6.setVisible(False)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        
        '''
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_5.clicked.connect(self.pushButton_5_Click)
        self.ui.pushButton_6.clicked.connect(self.pushButton_6_Click)
'''
        
        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView_2))

        global program
        program = ProgramTray()
        self.connect(program, QtCore.SIGNAL("treadsignal"), self.startLogic, QtCore.Qt.QueuedConnection)

#        self.trayIcon = QSystemTrayIcon(QIcon("d:/work4/ElectroLab/trunk/electrolab/gui/ui/ico/mushroom.png"), self)
#        self.trayIcon = QSystemTrayIcon(QIcon(":/ui/ico/mushroom.png"), self)
        self.trayIcon = QSystemTrayIcon(QIcon(os.getcwd() + '\\ui\\ico\\mushroom.png'), self)
        
        
        inputFile = os.getcwd() + u'\\rpt\\Протокол_поверки.xlsx'  # Шаблон
        
        
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        
        self.trayIcon.activated.connect(self.activate)






        '''
        self.trayIcon.setVisible(True)
        self.hide()

        global flag_exit
        flag_exit = True
        global program
        program.start()        
        program.exec_()
'''
        '''
        global flag_exit
        flag_exit = True
        program.start()
        '''        
#        program.exec_()





        
    def startLogic(self):
        print 'startLogic  startLogic  startLogic'
#        return
        self.selTrans()
        if model.rowCount() > 0:
            self.auto_type_trans()
        if model.rowCount() > 0 or model_2.rowCount() > 0:
            self.activate()
                           

    def activate(self):
        global program
        program.stop()
        self.trayIcon.setVisible(False)
        self.show()
        
#        self.exec_()
#        self.done()
        #self.focusWidget()
       # self.setFocus()
        print 'activate'

        #self.setEnabled(True)
        
        
        
        
################################




################################################
    '''
    def closeEvent(self, event):
        if self.okayToClose(): 
            #user asked for exit
            self.trayIcon.hide()
            event.accept()
        else:
            #"minimize"
            self.hide()
            self.trayIcon.show() #thanks @mojo
            event.ignore()

    def __icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show()
            '''
###################################################


    def selTrans(self):
        query = QSqlQuery(db1)
        
        global id_transes
        id_transes = []
                                
        SQL = """select t1.id,
fullname,
t2.type
from transformer t1 LEFT OUTER JOIN type_transformer t2 ON (t1.type_transformer = t2.id)
where t2.id is null
order by fullname
"""        
#        print SQL       
        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
                
        model.setQuery(query)
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Тип")            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        self.ui.tableView.setColumnHidden(0,  True)
        self.ui.tableView.selectRow(0)

        for i in range(model.rowCount()):
            id_transes += [model.record(i).field('id').value().toString()]


        SQL = """select t1.id, fullname, t2.type
from transformer t1 LEFT OUTER JOIN type_transformer t2 ON (t1.type_transformer = t2.id)
where fullname not like '%'||t2.type||'%'               
order by fullname
"""        
#        print SQL       
        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
        
        
        model_2.setQuery(query)
        model_2.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование")
        model_2.setHeaderData(2, QtCore.Qt.Horizontal, u"Тип")            
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.setColumnWidth(1,  withCol1)
        self.ui.tableView_2.setColumnWidth(2,  withCol2)
        self.ui.tableView_2.setColumnHidden(0,  True)
        self.ui.tableView_2.selectRow(0)



    def auto_type_trans(self):
        
        query = QSqlQuery(db1)
        
        SQL = "select id, type from type_transformer order by type"
        query.prepare(SQL)
        query.exec_()       
        
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка", SQL + '  ' + query.lastError().text(), QMessageBox.Ok)
            return
                
        model_3.setQuery(query)        
        Types = []         
        id_types = []         
        for i in range(model_3.rowCount()):
            id_types += [int(model_3.record(i).field('id').value().toString())]
            Types += [unicode(model_3.record(i).field('type').value().toString())]
        for i in range(len(Types)):
            print Types[i]
  
        for i in range(model.rowCount()):
            FullName = unicode(model.record(i).field('fullname').value().toString())
            id_trans = int(model.record(i).field('id').value().toString())
            for j in range(len(Types)):
             #   print i, j,  FullName, Types[i]
#                print i, j,  str(FullName).find(Types[i])
                print i, j, FullName, Types[j], FullName.find(Types[j])
           
                if FullName.find(Types[j]) > -1:
                    SQL = """UPDATE transformer SET type_transformer = :type_transformer
                    WHERE id = :id_transfomer"""                 
                    query.prepare(SQL)
                    query.bindValue(":type_transformer", id_types[j])
                    query.bindValue(":id_transformer", id_trans)
                    print SQL           
                    if not query.exec_():
                        QMessageBox.warning(self, u"Ошибка",  query.lastError().text(), QMessageBox.Ok)
                        return
           
        global id_transes
        if len(id_transes) == 0:
            return
        '''          
        st = '('
        for i in range(len(id_transes)):
            st += id_transes[i] + ','
        st = st[:len(st)-1] + ')'  
'''
        SQL = """select t1.id, fullname,
case when t2.type is null then '""" + unicode(u'НЕ ПРИСОЕДИНЕН') + """' else t2.type end as type
--t2.type
from transformer t1 LEFT OUTER JOIN type_transformer t2 ON (t1.type_transformer = t2.id)
where t2.id is null
order by fullname
"""

#--where t1.id in """ + unicode(st) + """
        
#        print SQL       
        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
                
        model.setQuery(query)
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Наименование")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Тип")            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView.setColumnWidth(1,  withCol1)
        self.ui.tableView.setColumnWidth(2,  withCol2)
        self.ui.tableView.setColumnHidden(0,  True)
        self.ui.tableView.selectRow(0)

    def pushButton_Click(self):
        self.trayIcon.show()
        self.hide()
        global program
        global flag_exit
        flag_exit = True
        program.start()        
     ###   program.exec_()   #???????????????????????
                
    def pushButton_2_Click(self):
        global program
        program.stop()
        program.exit()
        self.close() 

    '''
    def pushButton_3_Click(self):
        self.auto_type_trans()


    def pushButton_4_Click(self):
        print self.trayIcon.isVisible()
        global program
        QMessageBox.warning(self, u"Ошибка",  "2", QMessageBox.Ok)
        program = ProgramTray()
        program.start()        
        program.exec_()
        
    def pushButton_5_Click(self):
        global program
        program.stop()
        return
        self.trayIcon.setVisible(True)
        self.hide()

    def pushButton_6_Click(self):
        self.trayIcon.setVisible(False)
        self.show()
'''


if __name__ == "__main__":

    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    isStart = False
    for line in proc.stdout:
        if upper(line[0:17]) == 'AUTOTYPETRANS.EXE':
            isStart = True
#            print  "AUTOTYPETRANS.EXE"
#        else:    
#            print "No No No"

    
    '''
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    spis = []
    for line in proc.stdout:
        #print(line)
        spis += [line]
    print spis
    spis.sort()    
    for line in spis:
        print line
    '''
    
    '''
    import psutil
    for proc in psutil.process_iter():
        name = proc.name()
        print(name)
        if name == "program.exe":
            pass
    '''
    '''
    import subprocess

    def process_exists(process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call)
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())    
    
    print 111111111111
    print process_exists('AutoTypeTrans.exe')
#    print process_exists('AptanaStudio3.exe')
    
    print 222222222222
    '''
    
    
    
    if isStart == False:
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
                            
        wind = AutoTypeTrans(env)
        wind.setEnabled(True)
        wind.trayIcon.setVisible(True)
#    wind.hide()
        wind.show()

        '''
    global flag_exit
    flag_exit = True
    global program
    program.start()        
###    program.exec_()
'''

        wind.pushButton_Click()

        sys.exit(app.exec_())
        
