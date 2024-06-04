# -*- coding: UTF-8 -*-
#

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QWidget, QKeyEvent, QIcon, QFont
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtCore import Qt

#import os
import socket
print socket.gethostname()

hostname = socket.gethostname()

from electrolab.gui.common import UILoader
from electrolab.gui.DigitalKeyboard import DigitalKeyboard

#import ui.ico_64_rc

import datetime

from datetime import date
from devices import Devices


model = QSqlQueryModel()
model_2 = QSqlQueryModel()

#

from PyQt4.QtGui import QTableView

from PyQt4.QtGui import QTextEdit
#QTextEdit.toPlainText()

#QTableView

class Test_OLS(QWidget, UILoader):    
#    def __init__(self, _env, oMap, tvItem, tvCoil, btnStart, VerificationForm):
    def __init__(self, _env):
        
        super(QWidget, self).__init__()
                
        self.setUI(_env.config, u"Test_OLS.ui")        
        
        self.setWindowState(Qt.WindowFullScreen)        
        
  #      self.ui.btnAssistant.setVisible(False)
        self.ui.btnSupervisor.setVisible(False)
        
        self.oDigitalKeyboard = DigitalKeyboard(_env)
        self.oDigitalKeyboard.ui.btn_dot.setText('%')
        self.ui.horizontalLayout_4.addWidget(self.oDigitalKeyboard)
        self.oDigitalKeyboard.setEnabled(True)
        
#        self.ui.textEdit.installEventFilter(self)
        self.ui.lineEdit_2.installEventFilter(self)
        self.ui.lineEdit_3.installEventFilter(self)

        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(False)
        self.ui.frame_5.setVisible(False)

               
        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)        
        self.ui.pushButton_4.clicked.connect(self.pushButton4_Click)        
        self.ui.pushButton_5.clicked.connect(self.pushButton5_Click)        
        self.ui.pushButton_6.clicked.connect(self.pushButton6_Click)        
        self.ui.pushButton_7.clicked.connect(self.pushButton7_Click)        
        

        self.ui.btnTestType.clicked.connect(self.btnTestType_Click)
        self.ui.btnTester.clicked.connect(self.btnTester_Click)
        self.ui.btnTrans.clicked.connect(self.btnTrans_Click)
        self.ui.btnQuit.clicked.connect(self.btnQuit_Click)
        self.ui.btnDevices.clicked.connect(self.btnDevices_Click)

        self.ui.lineEdit_2.setText(str(date.today().year)[2:4])
        self.ui.lineEdit_2.textChanged.connect(self.lineEdit_2_textChanged)
        self.ui.lineEdit_3.textChanged.connect(self.lineEdit_2_textChanged)

        self.sw = 1    # ключ.  1 - выбор теста, 2 - выбор оператора

        self.ui.tableView.setModel(model)        
        self.selModel = self.ui.tableView.selectionModel()
#        self.connect(self.selModel2, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged2)
 
#        self.ui.lineEdit_2.setText(str(datetime.datetime.now().year))

        self.selectTestType()


        return

        QtGui.QPrinter

        print 'FFFFFFFFFFFFF'
        
        
        self.text = QtGui.QTextBrowser()
        self.text.setText(u"Питон печатает!")
        printer = QtGui.QPrinter()
        printer.setpa
        dlg = QtGui.QPrintDialog(printer)
        if dlg.exec_() == QtGui.QDialog.Accepted: self.text.print_(printer)
        
        '''        
        import win32ui
        import win32print
        import win32con

        #win32ui.CreateDC.

        INCH = 1440

        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (win32print.GetDefaultPrinter ())
        hDC.StartDoc ("Test doc")
        hDC.StartPage ()
        hDC.SetMapMode (win32con.MM_TWIPS)
        hDC.DrawText ("TEST", (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
        hDC.EndPage ()
        hDC.EndDoc ()
        '''        
        
        ''' Выводит на принтер 'TEST' по центру
        import win32ui
        import win32print
        import win32con

        INCH = 1440

        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (win32print.GetDefaultPrinter ())
        hDC.StartDoc ("Test doc")
        hDC.StartPage ()
        hDC.SetMapMode (win32con.MM_TWIPS)
        hDC.DrawText ("TEST", (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
        hDC.EndPage ()
        hDC.EndDoc ()
        ''' 
        
        ''' Печатает в буфер
        import os, sys  
        import win32print
        import time
        printer_name = win32print.GetDefaultPrinter()
        if sys.version_info >= (3,):
            raw_data = bytes ("This is a test111", "utf-8")
        else:
            raw_data = "This is a test222"

        hPrinter = win32print.OpenPrinter (printer_name)
        
        hJob = win32print.StartDocPrinter (hPrinter, 1, ("test of raw data", None, "RAW"))
        win32print.StartPagePrinter (hPrinter)
        win32print.WritePrinter (hPrinter, raw_data)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)        
        '''
        
        
        '''
        try:
            hJob = win32print.StartDocPrinter (hPrinter, 1, ("test of raw data", None, "RAW"))
            try:
                win32print.StartPagePrinter (hPrinter)
                win32print.WritePrinter (hPrinter, raw_data)
                win32print.EndPagePrinter (hPrinter)
            finally:
                win32print.EndDocPrinter (hPrinter)
        finally:
            win32print.ClosePrinter (hPrinter)        
        '''
        
        print 'GGGGGGGGGGGGGGGG'
        return
        
        
        import win32print
        printer = win32print.GetDefaultPrinter()
        wp = win32print
        #win32print.dr
        
        printer_name = win32print.GetDefaultPrinter ()
        print'printer_name=', printer_name
        
        hPrinter = win32print.OpenPrinter (printer_name)
        raw_data = "This is a test"
#        hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
#        win32print.WritePrinter(hPrinter, raw_data)
        try:
            hJob = win32print.StartDocPrinter (hPrinter, 1, ("test of raw data", None, "RAW"))
            try:
                win32print.WritePrinter (hPrinter, raw_data)
            finally:
                win32print.EndDocPrinter (hPrinter)
        finally:
            win32print.ClosePrinter (hPrinter)

        
        
        printer_types = [(wp.PRINTER_ENUM_SHARED, 'shared'), (wp.PRINTER_ENUM_LOCAL, 'local'), (wp.PRINTER_ENUM_CONNECTIONS, 'network')]
        
        printer_list = {}
        for printer_type in printer_types:
            print printer_type
            for printer in win32print.EnumPrinters(printer_type[0],None,1):
#                        if name == '*':
#                                printer_list[printer] = win32print.OpenPrinter(printer[2])
#                        elif name.lower() in printer[2].lower():                                
                printer_list[printer] = win32print.OpenPrinter(printer[2])
        print 'printer_list=', printer_list
        '''        
        printer_list= {
                        (8388608, 'Fax,Microsoft Shared Fax Driver,', 'Fax', ''): <PyPrinterHANDLE at 92909056 (4396308)>,
                        (8388608, 'Microsoft XPS Document Writer,Microsoft XPS Document Writer,', 'Microsoft XPS Document Writer', ''): <PyPrinterHANDLE at 92909032 (4396172)>,
                        (8388608, '\xce\xf2\xef\xf0\xe0\xe2\xe8\xf2\xfc \xe2 OneNote 2007,Send To Microsoft OneNote Driver,', '\xce\xf2\xef\xf0\xe0\xe2\xe8\xf2\xfc \xe2 OneNote 2007', ''): <PyPrinterHANDLE at 92909008 (4396036)>,
                        (8388608, 'ZDesigner LP 2824 Plus (ZPL),ZDesigner LP 2824 Plus (ZPL),', 'ZDesigner LP 2824 Plus (ZPL)', None): <PyPrinterHANDLE at 92908984 (4395900)>}
       '''                 
        
        '''
        printer_list= {
                        (8388608, '\\\\wc221\\HP LaserJet P2015 Series PCL 5e,HP LaserJet P2015 Series PCL 5e,',
                         '\\\\wc221\\HP LaserJet P2015 Series PCL 5e', ''):
                          <PyPrinterHANDLE at 190547808 (2544788)>,
                        (8388608, '\\\\Wc15\\Canon LBP2900,Canon LBP2900,', '\\\\Wc15\\Canon LBP2900', ''):
                          <PyPrinterHANDLE at 190547784 (2542684)>,
                        (8388608, '\\\\WS18\\HP LaserJet P2015 Series PCL 6,HP LaserJet P2015 Series PCL 6,',
                         '\\\\WS18\\HP LaserJet P2015 Series PCL 6', ''):
                         <PyPrinterHANDLE at 190547856 (2551700)>,
                        (8388608, '\\\\ws18\\HP DeskJet 1220C,HP DeskJet 1220C,', '\\\\ws18\\HP DeskJet 1220C', ''):
                         <PyPrinterHANDLE at 190547832 (2551276)>}
        '''
        
        print
        
        #import cups
        #conn = cups.Connection()
        #printers = conn.getPrinters()
        
        print 'GGGGGGGGGGGGGGG'
        
       # self.ui.pushButton.setEnabled(False)

    def PrinStickers(self):
        print 'PrinStickers'
        from electrolab.gui.reporting import FRPrintForm
#        inputParms = {u'snID':_iItemID, u'SQL': _SQL, u'accuracyR': _accuracyR, u'accuracyI': _accuracyI}
        inputParms = {}
        inputParms = {u'test_map':52877}
        print 'inputParms=', inputParms
        rpt = FRPrintForm(u'ReportStickers.fr3' ,inputParms , env)
        rpt.preview()
        return
        try:
            rpt = FRPrintForm(u'TestStrickers.fr3' ,inputParms , self.env)
            rpt.preview()
            # rpt.design()
        except:
            pass
        


    def view(self):
        v = False
        if self.sw in (1,2):
            v = True 
            
        self.ui.frame_2.setVisible(self.sw in (1,2))
#        self.ui.tableView.setVisible(self.sw in (1,2))
#        self.ui.pushButton.setVisible(self.sw in (1,2))
#        self.ui.pushButton_3.setVisible(self.sw in (1,2))
        
#        self.ui.label.setVisible(self.sw == 3)
#        self.ui.label_2.setVisible(self.sw == 3)
#        self.ui.textEdit.setVisible(self.sw == 3)
#        self.ui.lineEdit_2.setVisible(self.sw == 3)
#        self.ui.lineEdit_3.setVisible(self.sw == 3)                        
#        self.oDigitalKeyboard.setVisible(self.sw == 3)
        self.ui.label.setVisible(self.sw in (3,4))
        self.ui.label_2.setVisible(self.sw in (3,4))
        self.ui.textEdit.setVisible(self.sw in (3,4))
        self.ui.lineEdit_2.setVisible(self.sw in (3,4))
        self.ui.lineEdit_3.setVisible(self.sw in (3,4))                        
        self.oDigitalKeyboard.setVisible(self.sw == 3)
#        self.oDigitalKeyboard.setVisible(True)

        self.ui.lineEdit_2.setReadOnly(self.sw != 3)
        self.ui.lineEdit_3.setReadOnly(self.sw != 3)

        #QtGui.QLineEdit.setReadOnly()
        if self.sw == 3:
            self.ui.lineEdit_2.installEventFilter(self)
            self.ui.lineEdit_3.installEventFilter(self)
        else:    
            self.ui.lineEdit_2.removeEventFilter(self)
            self.ui.lineEdit_3.removeEventFilter(self)


        self.ui.pushButton_2.setVisible(self.sw != 4)
        
        self.ui.btnStart.setVisible(self.sw == 4)
        #self.ui.frame.setVisible(self.sw == 4)
        self.ui.frame_5.setVisible(self.sw == 4)
        

    def selectTestType(self):
#        self.ui.verticalLayout_3.setVisible(False)
        
        self.sw = 1                
        self.view()        
#        self.ui.frame.setVisible(False)
        
        model.clear()        
        model.reset()        
                
        query = QSqlQuery(db)
        selectStand = """SELECT id, fullname FROM stand
                         WHERE hostname = :hostname
                         ORDER BY fullname"""        
                        
        query.prepare(selectStand)
        query.bindValue(":hostname", hostname)          
        
#        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Заводской номер")
        if not query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
        
        model.setQuery(query)
        
        self.ui.tableView.setColumnHidden(0, True)        
        self.ui.tableView.selectRow(0)


    '''
select stand.id, stand_user.operator, fio from stand, stand_user, operator
where hostname = 'ws241'
and stand.id = stand_user.stand
and stand_user.operator = operator.id
'''


    def selectTester(self):
        self.sw = 2
        
#        self.ui.frame.setVisible(False)
        
        self.view()
        
        model.clear()        
        model.reset()        
                
        query = QSqlQuery(db)
        selectOper = """SELECT operator.id, fio FROM stand_user, operator
                         WHERE stand_user.stand = :stand
                         AND stand_user.operator = operator.id
                         ORDER BY fio"""        
                        
        query.prepare(selectOper)
        query.bindValue(":stand", self.id_stand)          
        
        if not query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
        
        model.setQuery(query)
        self.ui.tableView.setColumnHidden(0, True)        
        self.ui.tableView.selectRow(0)


    def selectTrans(self):
        self.sw = 3
#        self.ui.frame.setVisible(True)
        self.view()
#        self.ui.btnAssistant        
        self.ui.lineEdit_3.setFocus()
        
        pass

    def test(self):
        self.sw = 4
        self.view()
        pass


    def lineEdit_2_textChanged(self):
        
        model_2.clear()        
        model_2.reset()        
                
        #cursor = db.cursor()        

        print 'self.ui.lineEdit_3.text()', self.ui.lineEdit_3.text()
                        
        query = QSqlQuery(db)
        selectTrans = """select t1.id, t1.transformer, t2.fullname 
                         from serial_number as t1, transformer as t2
                         where t1.transformer = t2.id
                         and makedate = :makedate
                         and serialnumber = :serialnumber""" 
#                         and makedate = 16
#                         and serialnumber = 21654"""
                        
        query.prepare(selectTrans)
        query.bindValue(":makedate", self.ui.lineEdit_2.text())          
        query.bindValue(":serialnumber", self.ui.lineEdit_3.text())          
        
#        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Заводской номер")
        if not query.exec_():
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка сохранения", QMessageBox.Ok)
        
        model.setQuery(query)
        #self.ui.lineEdit.setText(model.record(0).field('fullname').value().toString())
        self.ui.textEdit.setText(model.record(0).field('fullname').value().toString())
        
        
        print model.rowCount()
        print model.record(0)
        print model.record(0).fieldName(2)
        print model.record(0).field('fullname').value().toString()
        
        


    def pushButton_Click(self):
        if model.rowCount() < 1:
            return        
        iRow = self.ui.tableView.currentIndex().row()
        if  iRow > 0:
            self.ui.tableView.selectRow(iRow - 1)
        else:
            self.ui.tableView.selectRow(model.rowCount() - 1)        


    def pushButton2_Click(self):
        print 'def pushButton2_Click(self)'
        row = self.selModel.currentIndex().row()
        print 'row', row
        if row == -1 and self.sw != 3:
            return
        if self.sw == 1:
            self.id_stand = model.record(row).field('id').value().toString()   
            self.fullname_test = model.record(row).field('fullname').value().toString()
            print self.id_stand, self.fullname_test
            self.ui.btnTestType.setText(self.fullname_test)
            self.ui.btnTester.setEnabled(True)            
            self.selectTester()
            return
        if self.sw == 2:
            self.id_oper = model.record(row).field('id').value().toString()   
            self.fio_test = model.record(row).field('fio').value().toString()
            print self.id_oper, self.fio_test
            self.ui.btnTester.setText(self.fio_test)
            self.ui.btnTrans.setEnabled(True)            
            self.selectTrans()
            return            
        if self.sw == 3:
            print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
            ###self.ui.btnTrans.setText(self.ui.textEdit.toPlainText())
            self.test()
            #self.ui.btnStart.setVisible(True)

    def pushButton3_Click(self):
        if model.rowCount() < 1:
            return        
        iRow = self.ui.tableView.currentIndex().row()
        if  iRow + 1 < model.rowCount():
            self.ui.tableView.selectRow(iRow + 1)
        else:
            self.ui.tableView.selectRow(0)

    def pushButton4_Click(self):
        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(False)
        pass
        
    def pushButton5_Click(self):
        self.ui.frame_3.setVisible(True)
        self.ui.frame_4.setVisible(False)
        pass
        
    def pushButton6_Click(self):
        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(True)
        pass
        
    def pushButton7_Click(self):
        self.ui.frame_3.setVisible(False)
        self.ui.frame_4.setVisible(False)
        pass
        

    def btnTestType_Click(self):        
        self.PrinStickers()
        return        
        self.selectTestType()

    def btnTester_Click(self):
        self.selectTester()

    def btnTrans_Click(self):
        self.selectTrans()

    def btnQuit_Click(self):
        self.close()


    def eventFilter(self, _object, _event):
        if _event.type() == QtCore.QEvent.FocusOut:
            self.oDigitalKeyboard.setVisible(False)
        if _event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
            self.oDigitalKeyboard.connect_to_widget(_object)
            self.oDigitalKeyboard.setVisible(True)
        return False

    def btnDevices_Click(self):
#    def setDevices(self):
#        self.Devices = Devices(self.env)
        self.Devices = Devices(env)
        self.Devices.setEnabled(True)
        self.Devices.exec_()
#        self.oTestCoil.Devices.data = self.Devices.data
#        self.oTestCoil.setMeasureR(self.Devices.ui.comboBox.currentText())
#        self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None);



'''
select stand.id, stand_user.operator, fio from stand, stand_user, operator
where hostname = 'ws241'
and stand.id = stand_user.stand
and stand_user.operator = operator.id
'''




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
        
        wind = Test_OLS(env)
        wind.setEnabled(True)
        #if wind.is_show: 
        wind.show()
        sys.exit(app.exec_())



'''
--Скрипты для изменения таблиц по трансам типа ОЛС, ЗНОЛ для импорта из 1С

ALTER TABLE transformer ADD column ClassVoltage character varying(10);
COMMENT ON COLUMN transformer.ClassVoltage IS 'Класс напряжения';
ALTER TABLE transformer ADD column Climate character varying(10);
COMMENT ON COLUMN transformer.Climate IS 'Климатическое исполнение';
ALTER TABLE transformer ADD column CategoryAccom character varying(1);
COMMENT ON COLUMN transformer.CategoryAccom IS 'Категория размещения';
ALTER TABLE transformer ADD column QuanSecond integer;
COMMENT ON COLUMN transformer.QuanSecond IS 'Количество вторичных обмоток ЗНОЛ';
ALTER TABLE transformer ADD column SafetyDevice character varying(1);
COMMENT ON COLUMN transformer.SafetyDevice IS 'Защитное предохранительное устройство';

ALTER TABLE coil ADD column NomVoltage numeric(8,2);
COMMENT ON COLUMN coil.NomVoltage IS 'Номинальное напряжение, В';
ALTER TABLE coil ADD column NomPower numeric(8,2);
COMMENT ON COLUMN coil.NomPower IS 'Номинальная мощность, ВА';
ALTER TABLE coil ADD column TypeAX integer;
COMMENT ON COLUMN coil.TypeAX IS 'Тип обмотки а2-х2, ad-xd';
ALTER TABLE coil ADD column ClassAccur character varying(10);
COMMENT ON COLUMN coil.ClassAccur IS 'Класс точности';

-- Пояснения:
1. В колонку TypeAX вставлять 1, если в Названиях параметра:
   "Тип обмотки а2-х2 (основная /?3, дополнительная /3)" либо
   "Тип обмотки ад-хд (основная /?3, дополнительная /3)"
   ЗначениеПараметра="/?3"
   и вставлять 2, если 
   ЗначениеПараметра="/3"

2. Как распределять по катушкам номинальные мощность, напряжения и классы точности, хз.
   Если не придумаешь, придется реализовать ручной вариант.


Для ОЛС
из Паспорта
ALTER TABLE transformer ADD column MaxVoltage numeric(8,4);
COMMENT ON COLUMN transformer.MaxVoltage IS 'Наибольшее рабочее напряжение, В';
ALTER TABLE transformer ADD column NomVoltageXA1 numeric(8,4);
COMMENT ON COLUMN transformer.NomVoltageXA1 IS 'Номинальное напряжение вторичной обмотки x-a1, В';
ALTER TABLE transformer ADD column NomVoltageXA2 numeric(8,4);
COMMENT ON COLUMN transformer.NomVoltageXA2 IS 'Номинальное напряжение вторичной обмотки x-a2, В';
ALTER TABLE transformer ADD column NomVoltageXA3 numeric(8,4);
COMMENT ON COLUMN transformer.NomVoltageXA3 IS 'Номинальное напряжение вторичной обмотки x-a3, В';
ALTER TABLE transformer ADD column NomVoltageXA4 numeric(8,4);
COMMENT ON COLUMN transformer.VoltageXA4 IS 'Номинальное напряжение вторичной обмотки x-a4, В';
ALTER TABLE transformer ADD column OneMinuteVoltage numeric(8,4);
COMMENT ON COLUMN transformer.OneMinuteVoltage IS 'Испытательное одноминутное приложенное напряжение 50 Гц между первичной и вторичной обмотками, В';

Для ОЛС
из таблицы недостающие поля
ALTER TABLE transformer ADD column NomVoltage numeric(8,4);
COMMENT ON COLUMN transformer.NomPower IS 'Номинальное напряжение первичной обмотки, В';
ALTER TABLE transformer ADD column NomCurrent numeric(8,4);
COMMENT ON COLUMN transformer.NomCurrent IS 'Номинальный ток вторичной обмотки, A';
ALTER TABLE transformer ADD column NomCurrentXA1 numeric(8,4);
COMMENT ON COLUMN transformer.NomCurrentXA1 IS 'Номинальный ток вторичной обмотки x-a1, A';
ALTER TABLE transformer ADD column NomCurrentXA2 numeric(8,4);
COMMENT ON COLUMN transformer.NomCurrentXA2 IS 'Номинальный ток вторичной обмотки x-a2, A';
ALTER TABLE transformer ADD column NomCurrentXA3 numeric(8,4);
COMMENT ON COLUMN transformer.NomCurrentXA3 IS 'Номинальный ток вторичной обмотки x-a3, A';
ALTER TABLE transformer ADD column NomCurrentXA4 numeric(8,4);
COMMENT ON COLUMN transformer.NomCurrentXA4 IS 'Номинальный ток вторичной обмотки x-a4, A';
ALTER TABLE transformer ADD column IdleCurrent numeric(8,4);
COMMENT ON COLUMN transformer.IdleCurrent IS 'Ток холостого хода, A, не более';
ALTER TABLE transformer ADD column IdleLosses numeric(8,4);
COMMENT ON COLUMN transformer.IdleLosses IS 'Потери холостого хода, Вт, не более';
ALTER TABLE transformer ADD column ShortCircVoltage numeric(8,4);
COMMENT ON COLUMN transformer.ShortCircVoltage IS 'Напряжение короткого замыкания, %';
ALTER TABLE transformer ADD column ShortCircLosses numeric(8,4);
COMMENT ON COLUMN transformer.ShortCircLosses IS 'Потери короткого замыкания, Вт, не более';

Допуски на основные характеристики:
ALTER TABLE transformer ADD column IdleCurrent numeric(8,4);
COMMENT ON COLUMN transformer.IdleCurrent IS 'Ток холостого хода, A, не более';
ALTER TABLE transformer ADD column IdleLosses numeric(8,4);
COMMENT ON COLUMN transformer.IdleLosses IS 'Потери холостого хода, Вт, не более';
ALTER TABLE transformer ADD column ShortCircVoltage numeric(8,4);
COMMENT ON COLUMN transformer.ShortCircVoltage IS 'Напряжение короткого замыкания, %';
ALTER TABLE transformer ADD column ShortCircLosses numeric(8,4);
COMMENT ON COLUMN transformer.ShortCircLosses IS 'Потери короткого замыкания, Вт, не более';




ALTER TABLE transformer ADD column Un character varying(100);



--Для ОЛС
--из 1С
ALTER TABLE transformer DROP column NomPower;
ALTER TABLE transformer DROP column ClassVoltage;
ALTER TABLE transformer DROP column Climate;
ALTER TABLE transformer DROP column CategoryAccom;
ALTER TABLE transformer DROP column NomVoltage;

--Для ЗНОЛ
--из 1С
ALTER TABLE transformer DROP column QuanSecond;
ALTER TABLE transformer DROP column SafetyDevice;
ALTER TABLE transformer DROP column NomVoltageMainSec;
ALTER TABLE transformer DROP column NomVoltageAddSec;
ALTER TABLE transformer DROP column TypeA2X2;
ALTER TABLE transformer DROP column TypeADXD;
ALTER TABLE transformer DROP column ClassAccurMainSec;
ALTER TABLE transformer DROP column ClassAccurAddSec;
ALTER TABLE transformer DROP column NomPowerMainSec;
ALTER TABLE transformer DROP column NomPowerAddSec;
ALTER TABLE transformer DROP column forAEC;



'''
        
        