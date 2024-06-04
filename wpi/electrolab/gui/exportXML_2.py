# -*- coding: UTF-8 -*-

'''
Created on 19.04.2022

@author: atol
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QIcon, QFont, QSystemTrayIcon
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
import PyQt4

import time
import os
from collections import OrderedDict
from string import upper

import datetime
import json
from datetime import date


model   = QSqlQueryModel()
model_2   = QSqlQueryModel()

id_item = -1


withCol1 = 100
withCol2 = 70
withCol3 = 70
withCol4 = 70
withCol5 = 100

withCol_1 = 50
withCol_2 = 70
withCol_3 = 70
withCol_4 = 70
withCol_5 = 70
withCol_6 = 70

global id_transes
global flag_exit

class ProgramTray(QtCore.QThread):
#    def __init__(self, icon):
    def __init__(self):
        QtCore.QThread.__init__(self)
        global flag_exit
        flag_exit = True
#        print 'ProgramTray      flag_exit = True'
        

    def run(self):
#        print 'run'
        """Код работающий в отдельном потоке"""

        global flag_exit
#        print 'flag_exit=flag_exit=flag_exit=flag_exit=flag_exit=flag_exit=',flag_exit
        while flag_exit:
            print "I'm working ..."
            self.emit(QtCore.SIGNAL('treadsignal'))
            time.sleep(30)
            
            
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
        
        global VSB1, VSB2, VSB3, VSB4, width1
        
        if obj.objectName() == 'tv1' and (e.type() <> QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol1 + withCol2 + withCol3 + withCol4 + withCol5))
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            obj.setColumnWidth(5, koef * withCol5)
            VSB1 = obj.verticalScrollBar().isVisible()
        if obj.objectName() == 'tv2' and (e.type() <> QtCore.QEvent.Resize or VSB2 <> obj.verticalScrollBar().isVisible()):
            koef = (1.0 * (self.widthArea(obj)) / (withCol_1 + withCol_2 + withCol_3 + withCol_4 + withCol_5 + withCol_6))
            obj.setColumnWidth(0, koef * withCol_1)
            obj.setColumnWidth(1, koef * withCol_2)
            obj.setColumnWidth(2, koef * withCol_3)
            obj.setColumnWidth(3, koef * withCol_4)
            obj.setColumnWidth(4, koef * withCol_5)
            obj.setColumnWidth(5, koef * withCol_6)
            VSB2 = obj.verticalScrollBar().isVisible()
            
        return False


#class AutoTypeTrans(QtGui.QDialog, UILoader):
class exportXML_2(QtGui.QDialog, UILoader):
    def __init__(self, _env):
        print '12311'

#        QMessageBox.warning(self, u"Ошибка",  '1', QMessageBox.Ok)
        global db1
        db1 = _env.db
                    
        super(QWidget, self).__init__()
        
        if not self.TestBase():
            return
                        
        self.setUI(_env.config, u"exportXML_2.ui")
        print '_env.config = ', _env.config
        
        self.setEnabled(False)
        print '1'
        self.ui.tableView.setModel(model)        
        print '2'
        self.selModel = self.ui.tableView.selectionModel()        
        print '3'
        self.ui.tableView_2.setModel(model_2)        
        print '4'
        self.selModel_2 = self.ui.tableView_2.selectionModel()        

        print '33333'
        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton_4.setVisible(False)
        self.ui.pushButton_5.setVisible(False)
        self.ui.pushButton_6.setVisible(False)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.pushButton_4.clicked.connect(self.pushButton_4_Click)
        self.ui.pushButton_7.clicked.connect(self.pushButton_7_Click)
        self.ui.pushButton_8.clicked.connect(self.pushButton_8_Click)
        print '000'
        
#        msgBox(self, u"Перерасчет потерпел неудачу!")
 #       QMessageBox.warning(self, u"Ошибка",  '2', QMessageBox.Ok)
        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()                
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged)

        # Удаление горизонтальных полос прокрутки
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView.setObjectName('tv1')
        
        self.ui.tableView_2.setHorizontalScrollBarPolicy(1)
        self.ui.tableView_2.installEventFilter(MyFilter(self.ui.tableView))
        self.ui.tableView_2.setObjectName('tv2')
        
        print '111'
        '''          
        self.exportXML = {"pathExport": ""}        
        try:
            f = open('exportXML_2.json','r')
            self.exportXML = json.load(f)
            self.ui.lineEdit.setText(str(self.exportXML['pathExport']))
            self.ui.spinBox.setValue(int(self.exportXML['days']))                       
        except Exception:
            print u'Ошибка чтения exportXML_2.json!'
            self.activate()      
           '''
         
        self.horizontalHeader = self.ui.tableView.horizontalHeader()
        
  #      QMessageBox.warning(self, u"Ошибка",  '3', QMessageBox.Ok)
        global program
        program = ProgramTray()
        self.connect(program, QtCore.SIGNAL("treadsignal"), self.startLogic, QtCore.Qt.QueuedConnection)
        print '123'
#        self.trayIcon = QSystemTrayIcon(QIcon(os.getcwd() + '\\ui\\ico\\fish.png'), self)        
        self.trayIcon = QSystemTrayIcon(QIcon(os.getcwd() + '\\ui\\ico\\fish4.png'), self)        
        print '456'
        
        inputFile = os.getcwd() + u'\\rpt\\Протокол_поверки.xlsx'  # Шаблон
                
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        
        self.trayIcon.activated.connect(self.activate)


   #     QMessageBox.warning(self, u"Ошибка",  '4', QMessageBox.Ok)


        self.exportXML = {"pathExport": ""}        
        try:
            f = open('exportXML_2.json','r')
            self.exportXML = json.load(f)
            self.ui.lineEdit.setText(str(self.exportXML['pathExport']))
            self.ui.spinBox.setValue(int(self.exportXML['days']))                       
#            self.activate()      
            print u'VVVVVVikIKUHBBBBBBBBBBBBBBBBBBBBIKОшибка чтения exportXML_2.json!'
            global flag_exit
            print 'flag_exit=',flag_exit
            
#            QMessageBox.warning(self, u"Ошибка",  '5', QMessageBox.Ok)
#            flag_exit = True
#            stop()
#            QMessageBox.warning(self, u"Ошибка",  'SSSSSSSSSSSSS', QMessageBox.Ok)
#            QMessageBox.warning(self, u"Ошибка",  'xxxxxxxxxxxxx', QMessageBox.Ok)
        except Exception:
            print u'Ошибка чтения exportXML_2.json!'
#            self.activate()      
        
        self.selItem()
        
        
        
        
        
    def startLogic(self):
        print 'startLogic  startLogic  startLogic'
        #return
    
        self.selItem()
   ###     return
        if model.rowCount() < 1:
            return
         
        for i in range(model.rowCount()):
            if model.record(i).field('dateexport').value().toString() == '':
                self.ui.tableView.selectRow(i)
                self.export()
#            if i > 5:
#                break    
                
        self.selItem()            
        
                           

    def activate(self):
        global program
        program.stop()
        self.trayIcon.setVisible(False)
        self.show()
        print 'activate'


    def selItem(self):
#        print 'selTransselTransselTransselTransselTrans'
 #       QMessageBox.warning(self, u"Ошибка",  self.ui.spinBox.text(), QMessageBox.Ok)
        query = QSqlQuery(db1)
        
        global id_transes
        id_transes = []
                                
        SQL = u"""select a.*, b.dateexport from
(
select t5.id as item, trim(to_char(t6.makedate, '9999')) || '-' || trim(to_char(t6.serialnumber, '9999999999')) as serialnumber, 
 t2.temperature, t2.humidity, t2.pressure --, 
from test_map t1, climat t2, stand t3, test_type t4, item t5, serial_number t6 --, checking_2 t6, coil t7, serial_number t8
where t1.climat = t2.id
and t1.stand = t3.id
and t3.test_type = t4.id
and t5.test_map = t1.id
--and t6.item = t5.id
--and t6.coil = t7.id
and t5.serial_number = t6.id
and t4.code = 4
and t5.istested = true
and t1.createdatetime > date(now()) - """ + self.ui.spinBox.text()

        SQL += u""" 
) as a
left outer join itemExportXML_2 as b on (a.item = b.item)
order by a.item
"""

        
        print SQL       
        query.prepare(SQL)
        if not query.exec_():
            QMessageBox.warning(self, u"Ошибка",  query.lastError().text() + SQL, QMessageBox.Ok)
            return
                
        model.setQuery(query)
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Зав. номер")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Температура")            
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Влажность")            
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Давление")            
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Дата экспорта")            
        self.ui.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView.setColumnHidden(0,  True)
        #self.ui.tableView.setColumnHidden(5,  True)
        self.ui.tableView.selectRow(0)


    def selectionChanged(self):
        self.selCoil()
        


    def selCoil(self):
        row = self.selModel.currentIndex().row()
#        print 'row = row = row = ', row
        global id_item
        if row < 0:
            id_item = -1
        else:    
            id_item = int(model.record(row).field('item').value().toString())

        #row = self.selModel.currentIndex().row()
        self.ui.pushButton_7.setEnabled(model.record(row).field('dateexport').value().toString() != '')
            
        query = QSqlQuery(db1)
        query.prepare(u"""select
t7.coilnumber, t7.coilnumber || 'И1-' || t7.coilnumber || 'И' || t7.Tap as fullCoilName,
t6.k, t6.r, t6.un, t6.inom, t7.Tap
from checking_2 t6, coil t7
where t6.coil = t7.id
and t6.item = :item 
order by coilnumber, tap""")
                
        query.bindValue(":item", id_item)
        
        if not query.exec_():
            print unicode(query.lastError().text())
        
        model_2.setQuery(query)

        model_2.setHeaderData(0,  QtCore.Qt.Horizontal, u"Номер\nобмотки")
        model_2.setHeaderData(1,  QtCore.Qt.Horizontal, u"Наименование")
        model_2.setHeaderData(2,  QtCore.Qt.Horizontal, u"Коэффициент")
        model_2.setHeaderData(3,  QtCore.Qt.Horizontal, u"Сопротивление")
        model_2.setHeaderData(4,  QtCore.Qt.Horizontal, u"Напряжение\nнамагничивания")
        model_2.setHeaderData(5,  QtCore.Qt.Horizontal, u"Ток\nнамагничивания")
        
        self.ui.tableView_2.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.ui.tableView_2.setColumnHidden(6,  True)
        self.ui.tableView_2.selectRow(0)
        
        self.ui.tableView_2.setColumnWidth(0,  withCol_1)
        self.ui.tableView_2.setColumnWidth(1,  withCol_2)
        self.ui.tableView_2.setColumnWidth(2,  withCol_3)
        self.ui.tableView_2.setColumnWidth(3,  withCol_4)
        self.ui.tableView_2.setColumnWidth(4,  withCol_5)
        self.ui.tableView_2.setColumnWidth(5,  withCol_6)
        enab = self.selModel_2.currentIndex().row() >= 0        


    def pushButton_Click(self):
        self.trayIcon.show()
        self.hide()
        global program
        global flag_exit
        print 'pushButton_Click           flag_exit = True'
        flag_exit = True
        program.start()        
                
    def pushButton_2_Click(self):
        global program
        program.stop()
        program.exit()
        self.close() 

    def pushButton_3_Click(self):
        for i in range(model.rowCount()):
            if model.record(i).field('dateexport').value().toString() == '':
                self.ui.tableView.selectRow(i)
                self.export()
#                self.insert_itemExportXML()
            if i > 5:
                break    
                
        self.selItem()            
    
        
    def export(self):

        global id_item
        row = self.selModel.currentIndex().row()
        self.dateExport = PyQt4.QtCore.QDateTime.currentDateTime()
        
  
        self.file = u'<item>\n'
        self.file += u'  <number>' +  model.record(row).field('serialnumber').value().toString()  + u'</number>\n'
        self.file += u'  <temperature>' +  model.record(row).field('temperature').value().toString()  + u'</temperature>\n'
        self.file += u'  <humidity>' +  model.record(row).field('humidity').value().toString()  + u'</humidity>\n'
        self.file += u'  <pressure>' +  model.record(row).field('pressure').value().toString()  + u'</pressure>\n'
        self.file += u'  <coils>\n'
        
        coilnumber = ''
        for i in range(model_2.rowCount()):
            coilnumber = model_2.record(i).field('coilnumber').value().toString()
            
            tap = model_2.record(i).field('tap').value().toString()

            self.file += u'    <coil' + coilnumber +  '>\n'            
            self.file +=  '      <name>' + coilnumber + unicode(u'И1').encode('utf-8') + '-' + coilnumber + unicode(u'И').encode('utf-8') + tap + '</name>\n'            
            self.file += u'      <coeff>' +  model_2.record(i).field('k').value().toString()  + u'</coeff>\n'
            self.file += u'      <resist>' +  model_2.record(i).field('r').value().toString()  + u'</resist>\n'
            self.file += u'      <voltage>' +  model_2.record(i).field('un').value().toString()  + u'</voltage>\n'
            self.file += u'      <current>' +  model_2.record(i).field('inom').value().toString()  + u'</current>\n'
            self.file += u'    </coil' + coilnumber +  '>\n'
            
        self.file += u'  </coils>\n'        
        self.file += u'</item>\n'
        
        now = datetime.datetime.now()        
        nameFile = self.ui.lineEdit.text() + '/' + model.record(row).field('serialnumber').value().toString() + '_' + now.strftime("%Y-%m-%d-%H_%M_%S")
        nameFile = str(nameFile).replace('\\', '/')
        nameFile += '.xml'
        f = open(str(nameFile), 'w')
        f.write(self.file)
        f.close()
                
        query = QSqlQuery(db)        
        query.prepare("INSERT INTO itemExportXML_2 (item, dateExport) VALUES (:item, :dateExport)")
        query.bindValue(":item", id_item);
        query.bindValue(":dateExport", self.dateExport);
        if not query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
    

        
    def delete_itemExportXML(self):
        query = QSqlQuery(db)
        
        query.prepare("DELETE FROM itemExportXML_2 WHERE item = :item")
        query.bindValue(":item", id_item);
        if not query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка удаления признака", QMessageBox.Ok)    
    
    
    def pushButton_4_Click(self):
        for i in range(model.rowCount()):
            if model.record(i).field('dateexport').value().toString() != '':
                self.ui.tableView.selectRow(i)    

        
    def pushButton_7_Click(self):
        self.sel_row = self.selModel.currentIndex().row()        
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить признак\nэкспорта в XML-файл по текущей позиции?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.No:
            return
        self.delete_itemExportXML()
        self.selItem()
        self.ui.tableView.selectRow(self.sel_row)        
            
        QMessageBox.warning(self, u"Предупреждение", u"Признак экспорта очищен успешно!", QMessageBox.Ok)

        
    def pushButton_8_Click(self):
         dirlist = QtGui.QFileDialog.getExistingDirectory(self,u"Выбрать папку",".")
         if dirlist != '':
             self.ui.lineEdit.setText(dirlist)
        
        
    def closeEvent(self, event):        
        try:
            f = open('exportXML_2.json','w')
            self.exportXML['pathExport'] = str(self.ui.lineEdit.text())               
            self.exportXML['days'] = str(self.ui.spinBox.text())    
            json.dump(self.exportXML, f)
        except Exception:
            print u'Ошибка записи config.json!'        
        return
        
 

    def TestBase(self):
        print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        query.prepare("select * from itemExportXML_2")
        if not query.exec_(): err_tbl += "itemExportXML_2\n"
       
        if err_tbl != "":
            print err_tbl  
            
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
        print u"Инициализация БД"        
        query = QSqlQuery(db)

        SQL = u"""
CREATE TABLE itemExportXML_2
(
  item integer REFERENCES item (id),
  dateExport timestamp without time zone NOT NULL DEFAULT now()
);
COMMENT ON TABLE itemExportXML IS 'Справочник дат экспорта результатов испытаний по типам испытаний';
COMMENT ON COLUMN itemExportXML.item IS 'Ссылка на item';
COMMENT ON COLUMN itemExportXML.dateExport IS 'Дата/время экспорта';
"""
        if not query.exec_(SQL):
            print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        print SQL
        return


if __name__ == "__main__":
    '''
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    isStart = False
    for line in proc.stdout:
        if upper(line[0:15]) == 'EXPORTXML_2.EXE':
            isStart = True    
    
    if isStart == False:
        import sys
        app = QtGui.QApplication(sys.argv)
     
        msgBox(None, u"Перерасче!")
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
        
        msgBox(None, u"Перерасче!")
        wind = exportXML_2(env)
        wind.setEnabled(True)
        wind.trayIcon.setVisible(True)
        wind.show()


 #####       wind.pushButton_Click()

        sys.exit(app.exec_())
        
'''

    print '1'

    import subprocess
    print '2'
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    print '3'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print '4'
    isStart = False
    print '5'
    '''
    for line in proc.stdout:
        if upper(line[0:15]) ==  'EXPORTXML_2.EXE':
            isStart = True
'''
    print '2'
        
    
    if isStart == False:
        print 'q'
        import sys
        app = QtGui.QApplication(sys.argv)
        print 'w'
     
        from dpframe.base.inits import db_connection_init   
        print 'w1'
        from dpframe.base.envapp import checkenv
        print 'w2'
        from dpframe.base.inits import json_config_init
        print 'w3'
        from dpframe.base.inits import db_connection_init
        print 'w4'
        from dpframe.base.inits import default_log_init
        print 'w5'
#        from electrolab.gui.inits import serial_devices_init
        print 'e'
           
#        @serial_devices_init
        @json_config_init
        @db_connection_init
        @default_log_init    
        class ForEnv(QtGui.QWidget):
            def getEnv(self):
                return self.env
        
        objEnv = ForEnv()
        env = objEnv.getEnv()
        db = env.db
                            
        wind = exportXML_2(env)
        wind.setEnabled(True)
        wind.trayIcon.setVisible(True)
        wind.show()


      #  wind.pushButton_Click()

        sys.exit(app.exec_())

