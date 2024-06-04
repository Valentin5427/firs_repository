# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget , QSpinBox, QDialog, QApplication
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
import datetime


from electrolab.gui.DigitalKeyboard import DigitalKeyboard
#from electrolab.gui.findserialnumber import FindSerialNumber
from electrolab.gui.common import UILoader
from electrolab.data import helper
from electrolab.gui.reporting import FRPrintForm
from devices import Devices
from fileinput import close

model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
model_4 = QSqlQueryModel()
model_9 = QSqlQueryModel()
withCol0 = 35
withCol1 = 25
withCol2 = 100
withCol3 = 10
withCol4 = 50
VSB1 = False







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
                
#        if obj.objectName() == 'tv1' and (e.type() == QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):        
        if obj.objectName() == 'tv1':        
            koef = (1.0 * (self.widthArea(obj)) / (withCol0 + withCol1 + withCol2 + withCol3 + withCol4))
            obj.setColumnWidth(0, koef * withCol0)
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            VSB1 = obj.verticalScrollBar().isVisible()
                    
        return False


#class archive(QtGui.QDialog):
class archive(QDialog, UILoader):
#    def __init__(self, _env, *args):
    def __init__(self, _env):
        
        self.env = _env
        
        super(QWidget, self).__init__()

        self.setUI(_env.config, u"Archive.ui")
        
        self.oDigitalKeyboard = DigitalKeyboard(_env)
        
        # Корректировка размеров цифровой клавиатуры
        fnt = self.oDigitalKeyboard.ui.btn_0.font()
        fnt.setPointSize(fnt.pointSize() * 0.7)
        self.oDigitalKeyboard.ui.btn_0.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_1.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_2.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_3.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_4.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_5.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_6.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_7.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_8.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_9.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_dot.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_BackSpace.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_Clear.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_Ok.setFont(fnt)        
        minWidth = self.oDigitalKeyboard.ui.btn_BackSpace.minimumWidth()        
        self.oDigitalKeyboard.ui.btn_1.setMinimumSize(minWidth, 0)
        self.oDigitalKeyboard.ui.btn_2.setMinimumSize(minWidth, 0)
        self.oDigitalKeyboard.ui.btn_3.setMinimumSize(minWidth, 0)
            
        
        self.ui.vlKeyboard.addWidget(self.oDigitalKeyboard)

        self.query_9 = QSqlQuery(_env.db)
         
        self.ui.sbYear.valueChanged.connect(self.change_serial_number)
        self.ui.sbNumber.valueChanged.connect(self.change_serial_number)

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton3_Click)
        
        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
         
        self.iSerialNumberID = None
        self.oHelperSerialNumber = helper.SerialNumber(_env)
        self.ui.sbYear.installEventFilter(self)
        self.ui.sbNumber.installEventFilter(self)
        self.oDigitalKeyboard.enter.connect(self.ui.sbNumber.focusNextChild) #TODO: Странно, почему нельзя цеплять к родителю????
        self.ui.sbYear.setValue(datetime.datetime.now().year - 2000) 
         
        self.Devices = Devices(_env)
        
        self.ui.tableView.setModel(model)
        self.selModel = self.ui.tableView.selectionModel()        
        #self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)
        self.ui.tableView.setObjectName('tv1')
        self.ui.tableView.setHorizontalScrollBarPolicy(1)
        self.ui.tableView.installEventFilter(MyFilter(self.ui.tableView))        
        self.viewTesting(0)        


        self.ui.checkBox_2.setVisible(False)
        self.ui.pushButton_3.setVisible(False)
#        self.ui.comboBox.setCurrentIndex(5)
        
        
        

    def comboBox_currentIndexChanged(self, ind):
        self.ui.checkBox.setEnabled(ind == 3 or ind == 4)
        self.ui.checkBox.setChecked(ind == 3 or ind == 4)
        self.ui.radioButton.setEnabled(ind == 0 or ind == 3 or ind == 4)
        self.ui.radioButton_2.setEnabled(ind == 0 or ind == 3 or ind == 4)
        

    def viewTesting(self, id_search):
        #if id_search == '':
        #    return
        model.clear()        
        # model.reset()
        model_2.clear()        
        # model_2.reset()
        if self.iSerialNumberID == None:
            return        


        SQL = '''select series, ordernumber
from serial_number
where id = ''' + str(self.iSerialNumberID)
        print(SQL)
        model_2.setQuery(SQL, self.env.db)
        self.series = model_2.record(0).field('series').value()
        self.ordernumber = model_2.record(0).field('ordernumber').value()

        SQL = '''select to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item, t1.istested, gost_id
from item as t1, test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = ''' + str(self.iSerialNumberID) + '''
order by t2.createdatetime'''
        
        model.setQuery(SQL, self.env.db)
        model.setHeaderData(0, QtCore.Qt.Horizontal, u"Дата")
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Время")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Тип испытания")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Код")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Оператор")
        
    def showEvent(self, _event):
#        self.ui.sbNumber.clear()
#        self.ui.sbNumber.setValue(33333) 
#        self.ui.sbNumber.setValue(20101) 
#        self.ui.sbNumber.setValue(75844) 
        self.ui.sbNumber.focusNextChild()
        self.ui.sbNumber.setFocus()


    def eventFilter(self, _object, _event):
        u"""Отлавливает переход фокуса, для подключения экранной клавиатуры"""
        if _event.type() == QEvent.FocusOut:
            self.oDigitalKeyboard.connect_to_widget()
        if _event.type() in (QEvent.FocusIn, QEvent.MouseButtonPress):
            self.oDigitalKeyboard.connect_to_widget(_object)
        return False


    def change_serial_number(self):
        print('change_serial_number')
        if not (self.ui.sbNumber.value and self.ui.sbYear.value):
            self.ui.leTransformer.clear()
            self.ui.iSerialNumberID = None
            #return
        print(545, self.ui.sbYear.value(), self.ui.sbNumber.value())
        oSNInfo = self.oHelperSerialNumber.get_id(self.ui.sbYear.value(), self.ui.sbNumber.value())
        if oSNInfo and oSNInfo.id: 
            self.ui.leTransformer.setText(oSNInfo.fullname)
            self.iSerialNumberID = oSNInfo.id
        else:
            self.ui.leTransformer.clear()
            self.iSerialNumberID = None
      
        print('self.iSerialNumberID', self.iSerialNumberID)
        self.viewTesting(0)        


    def pushButton_Click(self):
                
        if self.ui.comboBox.currentIndex() == 0:
                       
            if self.ui.radioButton.isChecked():
                self.calcMapItem((3,))
            if self.ui.radioButton_2.isChecked():
                self.calcMapItem((4,))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return
            inputParms = {u'test_map':self.test_map, u'item':self.item}

            print("self.test_map, self.item", self.test_map, self.item)
            try:
                rpt = FRPrintForm(u'ReportStickers.fr3' , inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']

                rpt.preview()
            except:
                pass

        if self.ui.comboBox.currentIndex() == 1:
            self.calcMapItem((0, 0))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return
            # print 'self.gost_id = ',self.gost_id
            # print 'self.test_map = ', self.test_map
            # print 'self.item = ', self.item
            inputParms = {u'test_map':self.test_map, u'item':self.item, u'gost_id':self.gost_id, u'type_test':1}
            
            try:

                print('self.iSerialNumberID=', self.iSerialNumberID)
                rpt = FRPrintForm(u'ReportStickers_2.fr3' , inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                rpt.preview()
                
                return
                     
#/ Временно
                strSQL = """                
select t1.id as item, t1.serial_number, makedate||'-'||serialnumber as zavnum, ordernumber, series, 
to_char(t3.createdatetime, 'dd.mm.yy') as date, t4.fio as fio, t5.fullname                                                                                                
from item t1, serial_number t2, test_map t3, operator t4, stand t5                          
where t1.serial_number = t2.id
and t1.test_map = t3.id
and t3.operator = t4.id
and t3.stand = t5.id
and test_map = """ + str(self.test_map) + """                   
--and test_map = 52877
order by item        
"""

                print(strSQL)
                
                self.query_9.prepare(strSQL)
                if not self.query_9.exec_():
                    QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
                else:    
                    model_9.setQuery(self.query_9)
                 
                for i in range(model_9.rowCount()):
                    inputParms = {u'test_map':self.test_map, u'item':int(model_9.record(i).field('item').value().toString()), u'gost_id':self.gost_id, u'type_test':1}
                    rpt = FRPrintForm(u'ReportStickers_2.fr3' , inputParms , self.env)
                    rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                    rpt.preview()
                    
                
# Временно/
                
# Вернуть
                """                
                print 'self.iSerialNumberID=', self.iSerialNumberID
                rpt = FRPrintForm(u'ReportStickers_2.fr3' ,inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                rpt.preview()
"""
# Вернуть                
            except:
                pass


        if self.ui.comboBox.currentIndex() == 2:
            self.calcMapItem((2, 2))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return

            inputParms = {u'test_map':self.test_map, u'item':self.item, u'gost_id':self.gost_id, u'type_test':2}
            
            try:
                print('self.iSerialNumberID=', self.iSerialNumberID)
                rpt = FRPrintForm(u'ReportStickers_2.fr3' , inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                rpt.preview()
            # rpt.design()
            except:
                pass


        if self.ui.comboBox.currentIndex() == 3:
            # 7.06.2017
            model_3.clear()        
            # model_3.reset()

            SQL = '''select distinct t1.id 
from serial_number as t1, serial_number as t2, item as t3, checking_2 as t4
where t1.series = t2.series
and t1.ordernumber = t2.ordernumber
and t2.id =  ''' + str(self.iSerialNumberID) + '''
and t1.id = t3.serial_number
and t3.id = t4.item order by t1.id
'''
            model_3.setQuery(SQL, self.env.db)            
            
            if model_3.rowCount() < 1:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных по испытаниям """,
                                    QMessageBox.Ok)
                return
            serial_number = model_3.record(0).field('id').value().toString()
            
            from electrolab.gui.TestCoil import TestCoil
            self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
            if self.ui.radioButton.isChecked():
                self.oTestCoil.codeTypeTest = 3
            if self.ui.radioButton_2.isChecked():
                self.oTestCoil.codeTypeTest = 4
            rez = self.oTestCoil.calcGlobal(None, serial_number, 16, None, None, self.ui.checkBox.isChecked())            
            if rez == False:
                return
            import ReportsExcel
            print('self.oTestCoil.globalReport = ', self.oTestCoil.globalReport)
            ReportsExcel.report(self.ui.leTransformer.text(), self.series, self.ordernumber, self.oTestCoil.globalReport, self.Devices.data['accuracy']['r'], self.Devices.data['accuracy']['a'], self.ui.checkBox.isChecked())                

            
        if self.ui.comboBox.currentIndex() == 4:
            from electrolab.gui.TestCoil import TestCoil
            self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
            import ReportsExcel

            if self.ui.radioButton.isChecked():
                code = 3
            if self.ui.radioButton_2.isChecked():
                code = 4

            coilsInfa = self.oTestCoil.buildCoilsInfa(self.iSerialNumberID, self.ui.checkBox.isChecked(), code)
            print(self.iSerialNumberID, self.ui.checkBox.isChecked(), code)
            print('coilsInfa = ', coilsInfa)
            ReportsExcel.BAX_coil1(self.ui.leTransformer.text(),
                                   str(self.ui.sbYear.value()) + '-' + str(self.ui.sbNumber.value()),
                                   self.ordernumber, coilsInfa, code)
#            ReportsExcel.BAX_coil1(fullname, serialnumbel, zakaz, coilsInfa)


        if self.ui.comboBox.currentIndex() == 5:
            self.calcMapItem((0, 1, 2, 5, 6))
                        
            import ReportsExcel
           

            ReportsExcel.verification_protocol(self.env.db, self.test_map, self.item, True)
            
            
            return
            
            # Старый выриант отчета
            inputParms = {u'test_map':self.test_map, u'itemid':self.item}
                        
            print('inputParmsinputParmsinputParmsinputParmsinputParms=', inputParms)
            rpt = FRPrintForm(u'tester_protocol.fr3', inputParms, self.env)
            rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
            rpt.preview()
            return


        if self.ui.comboBox.currentIndex() == 6:
#            self.calcMapItem((2, 2))
            self.calcMapItem((4, 4))
#            self.calcMapItem((3, 3))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return
            
            from electrolab.gui.TestCoil import TestCoil
            self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
            # Расчет коридоров для цеха
            
            self.oTestCoil.codeTypeTest = 3
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors = [[-1, -1, -1, 0, 0, 0, 0]]
            globalCorridors = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors += [self.oTestCoil.globalCorridors[i]]
               
                
            # Расчет коридоров для лаборатории
            self.oTestCoil.codeTypeTest = 4
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors_2 = [[-1, -1, -1, 0, 0, 0, 0]]                
                #return
            globalCorridors_2 = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors_2 += [self.oTestCoil.globalCorridors[i]]
            

            accurR = u"'Коридор " + str(self.Devices.data['accuracy']['r']) + "%'"
            accurI = u"'Коридор " + str(self.Devices.data['accuracy']['a']) + "%'"

 #           globalCorridors = globalCorridors_2

            import ReportsExcel      
            ReportsExcel.CommonReport(self.env, self.iSerialNumberID, accurR, accurI, self.gost_id, globalCorridors, globalCorridors_2, True)




        if self.ui.comboBox.currentIndex() == 7:
            import ReportsExcel
            SQL = """select id, serialnumber
from serial_number
where ordernumber = '""" + self.ordernumber +"""'
and series = '""" + self.series + """'
order by serialnumber
"""            
                                                
            model_2.clear()        
            # model_2.reset()
            model_2.setQuery(SQL, self.env.db)

            spisok = []
        
            codes = ['0', '3', '2', '7', '4', '1']
        
            for i in range(model_2.rowCount()):
                spisok += [[int(model_2.record(i).field('serialnumber').value().toString()),[],[],[],[],[],[]]]
                for j in range(len(codes)):
                    spisok[i][j+1] += []
                    
                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item,
--cast(t1.istested as integer) istested,
--cast(t1_.iscritical as integer) iscritical,
case when t1.istested then 1 else 0 end as istested,
case when t1_.iscritical then 1 else 0 end as iscritical,
t1.defect, t1_.fullname as name_defect, gost_id
from item as t1 left outer join defect as t1_ on (t1.defect = t1_.id),
test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = """ + model_2.record(i).field('id').value().toString() + """
and t5.code = """ + codes[j] + """
order by t2.createdatetime
"""                

                    model_3.clear()        
                    # model_3.reset()
                    model_3.setQuery(SQL, self.env.db)
                
                    for k in range(model_3.rowCount()):
                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value().toString()), unicode(model_3.record(k).field('fio').value().toString()),
                                            int(model_3.record(k).field('istested').value().toString()), int(model_3.record(k).field('iscritical').value().toString()),
                                            unicode(model_3.record(k).field('name_defect').value().toString())]]
                                    
            # for i in range(len(spisok)):

            ReportsExcel.repMoveTask(self.ordernumber, self.series, spisok)
        

        if self.ui.comboBox.currentIndex() == 8:
            from repDefect import repDefect
            wind = repDefect(env)
            wind.exec_()

        if self.ui.comboBox.currentIndex() == 9:
            # print 'self.print_report(int(serial_number))', self.iSerialNumberID
            self.calcMapItem((2, 2))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return

            from electrolab.gui.TestCoil import TestCoil
            self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
            # Расчет коридоров для цеха
            self.oTestCoil.codeTypeTest = 3
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors = [[-1, -1, -1, 0, 0, 0, 0]]
            globalCorridors = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors += [self.oTestCoil.globalCorridors[i]]
                
                                
            # Расчет коридоров для лаборатории
            self.oTestCoil.codeTypeTest = 4
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors_2 = [[-1, -1, -1, 0, 0, 0, 0]]                
                #return
            globalCorridors_2 = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors_2 += [self.oTestCoil.globalCorridors[i]]
                        
            # SQL запрос формирую в виде одной стоки, поскольку не знаю как передать 
            # из питона в FastReport переменную типа TStrings 
            SQL = u"'select t3.coilnumber "
            SQL += u", cast(t3.coilnumber as varchar ) || ''И1-'' || cast(t3.coilnumber as varchar ) || ''И'' || cast(t3.tap as varchar )  as coil "
            SQL += u", t1.r "
            
            SQL += u", case when u2 is null then round(un,2) else round(u2,2) end as un "              
            SQL += u", case when i2 is null then round(inom,2) else round(i2,2) end as inom " 
            
            SQL += u", round(t1.k, 1) as k "
            SQL += u", t1.rating "
            SQL += u", t5.fio "
            SQL += u", t2.createdatetime::date as sdate "
            SQL += u", round(minR, 4) as minR, round(maxR, 4) as maxR, round(minI, 4) as minI, round(maxI, 4) as maxI "            
            SQL += u", round(predel, 2) as predel "            
            SQL += u"from checking_2 t1,"
            
            SQL += u"(select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7 "
            SQL += u"where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id " 
            SQL += u"and t7.code = :code and serial_number = " + str(self.iSerialNumberID) + " "
            SQL += u"group by serial_number, coil) t1_, "
            
                    
            SQL += u"item t2, coil t3, "



            SQL_2 = SQL
                                
            # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors"
            SQL_ = ""
            if globalCorridors == []:
                SQL_ += u"( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,"
            else:  
                SQL_ += u"( "
                for i in range(len(globalCorridors)):
                    idCoil = str(globalCorridors[i][2])
                    minR = str(globalCorridors[i][3])
                    maxR = str(globalCorridors[i][4])
                    
                    minI = str(globalCorridors[i][5])
                    maxI = str(globalCorridors[i][6])
                    
                    if minI == 'None':
                        minI = 'null'    
                    if maxI == 'None':
                        maxI = 'null'   
                    

                    #19.05.2017
                    if globalCorridors[i][7] != None:
                        minI = str(globalCorridors[i][7])
                    if globalCorridors[i][8] != None:
                        maxI = str(globalCorridors[i][8])                    
                    
                    SQL_ += u"select " + idCoil + " as idCoil, " + minR + u" as minR, " + maxR + u" as maxR, " + minI + u" as minI, " + maxI + u" as maxI " 
                    if i < len(globalCorridors) - 1:
                        SQL_ += u" union "
                SQL_ += u") as corridor, "
            SQL += SQL_    
            
            # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors_2"
            SQL_ = ""
            if globalCorridors_2 == []:
                SQL_ += u"( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,"
            else:  
                SQL_ += u"( "
                for i in range(len(globalCorridors_2)):
                    idCoil = str(globalCorridors_2[i][2])
                    minR = str(globalCorridors_2[i][3])
                    maxR = str(globalCorridors_2[i][4])
                    
                    minI = str(globalCorridors_2[i][5])
                    maxI = str(globalCorridors_2[i][6])

                    #19.05.2017
                    if globalCorridors_2[i][7] != None:
                        minI = str(globalCorridors_2[i][7])
                    if globalCorridors_2[i][8] != None:
                        maxI = str(globalCorridors_2[i][8]) 
                        
                    if minI == 'None':
                        minI = 'null'    
                    if maxI == 'None':
                        maxI = 'null'   
                                                               
                    SQL_ += u"select " + idCoil + " as idCoil, " + minR + u" as minR, " + maxR + u" as maxR, " + minI + u" as minI, " + maxI + u" as maxI " 
                    if i < len(globalCorridors_2) - 1:
                        SQL_ += u" union "
                SQL_ += u") as corridor, "
            SQL_2 += SQL_    

                                                                        
            SQL_ = ""
            SQL_ += u"test_map t4 LEFT OUTER JOIN operator t5 ON (t4.operator = t5.id), "            
            SQL_ += u"stand t6, test_type t7 "            
            
            SQL_ += u"where t1.id = t1_.id  "            
            SQL_ += u"and t1.item = t2.id "            
            SQL_ += u"and t1.coil = t3.id "
            SQL_ += u"and t2.test_map = t4.id "
            SQL_ += u"and t2.serial_number = " + str(self.iSerialNumberID) + " "                                                                  
            SQL_ += u"and t3.id = corridor.idCoil "
            SQL_ += u"and t1.stand = t6.id "
            SQL_ += u"and t6.test_type = t7.id "
            SQL_ += u"and code = :code "
            SQL_ += u"order by t3.coilnumber, t3.tap'"                            
            
            SQL += SQL_    
            SQL_2 += SQL_    

            accurR = u"'Коридор " + str(self.Devices.data['accuracy']['r']) + "%'"
            accurI = u"'Коридор " + str(self.Devices.data['accuracy']['a']) + "%'"

            inputParms = {u'snID':self.iSerialNumberID, u'SQL': SQL, u'SQL_2': SQL_2, u'accuracyR': accurR, u'accuracyI': accurI, u'gost_id':self.gost_id}
            try:
                rpt = FRPrintForm(u'error_estimation.fr3' , inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
                rpt.preview()
            # rpt.design()
            except:
                pass
                        
            return


    def calcMapItem(self, p):
        self.test_map = None
        self.item = None
        for i in range(model.rowCount()):
            if int(model.record(i).field('code').value()) in p:
                self.test_map = int(model.record(i).field('test_map').value())
                self.item = int(model.record(i).field('item').value())
                self.gost_id = int(model.record(i).field('gost_id').value())


    def pushButton2_Click(self):
            self.close()
            return
        
        
        
            self.calcMapItem((2, 2))
            if self.test_map == None:
                QMessageBox.warning(None, u"Предупреждение",
                                      u"""Нет данных:host: """,
                                    QMessageBox.Ok)
                return
            
            from electrolab.gui.TestCoil import TestCoil
            self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
            # Расчет коридоров для цеха
            self.oTestCoil.codeTypeTest = 3
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors = [[-1, -1, -1, 0, 0, 0, 0]]
            globalCorridors = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors += [self.oTestCoil.globalCorridors[i]]
                
            # Расчет коридоров для лаборатории
            self.oTestCoil.codeTypeTest = 4
            rez = self.oTestCoil.calcGlobal(None, self.iSerialNumberID, 16, None, None, False)            
            if rez == False:
                self.oTestCoil.globalCorridors_2 = [[-1, -1, -1, 0, 0, 0, 0]]                
                #return
            globalCorridors_2 = []            
            for i in range(len(self.oTestCoil.globalCorridors)):
                if str(self.oTestCoil.globalCorridors[i][1]) == unicode(self.ordernumber):
                    globalCorridors_2 += [self.oTestCoil.globalCorridors[i]]
            

            accurR = u"'Коридор " + str(self.Devices.data['accuracy']['r']) + "%'"
            accurI = u"'Коридор " + str(self.Devices.data['accuracy']['a']) + "%'"

            import ReportsExcel      
            ReportsExcel.CommonReport(self.env, self.iSerialNumberID, accurR, accurI, self.gost_id, globalCorridors, globalCorridors_2, True)

            return
            


            SQL_2 = SQL
                                
            # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors"
            SQL_ = ""
            if globalCorridors == []:
                SQL_ += u"( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,"
            else:  
                SQL_ += u"( "
                for i in range(len(globalCorridors)):
                    idCoil = str(globalCorridors[i][2])
                    minR = str(globalCorridors[i][3])
                    maxR = str(globalCorridors[i][4])
                    
                    minI = str(globalCorridors[i][5])
                    maxI = str(globalCorridors[i][6])
                    
                    if minI == 'None':
                        minI = 'null'    
                    if maxI == 'None':
                        maxI = 'null'   
                    

                    #19.05.2017
                    if globalCorridors[i][7] != None:
                        minI = str(globalCorridors[i][7])
                    if globalCorridors[i][8] != None:
                        maxI = str(globalCorridors[i][8])                    
                    
                    SQL_ += u"select " + idCoil + " as idCoil, " + minR + u" as minR, " + maxR + u" as maxR, " + minI + u" as minI, " + maxI + u" as maxI " 
                    if i < len(globalCorridors) - 1:
                        SQL_ += u" union "
                SQL_ += u") as corridor, "
            SQL += SQL_    
            
            # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors_2"
            SQL_ = ""
            if globalCorridors_2 == []:
                SQL_ += u"( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,"
            else:  
                SQL_ += u"( "
                for i in range(len(globalCorridors_2)):
                    idCoil = str(globalCorridors_2[i][2])
                    minR = str(globalCorridors_2[i][3])
                    maxR = str(globalCorridors_2[i][4])
                    
                    minI = str(globalCorridors_2[i][5])
                    maxI = str(globalCorridors_2[i][6])

                    #19.05.2017
                    if globalCorridors_2[i][7] != None:
                        minI = str(globalCorridors_2[i][7])
                    if globalCorridors_2[i][8] != None:
                        maxI = str(globalCorridors_2[i][8]) 
                        
                    if minI == 'None':
                        minI = 'null'    
                    if maxI == 'None':
                        maxI = 'null'   
                                                               
                    SQL_ += u"select " + idCoil + " as idCoil, " + minR + u" as minR, " + maxR + u" as maxR, " + minI + u" as minI, " + maxI + u" as maxI " 
                    if i < len(globalCorridors_2) - 1:
                        SQL_ += u" union "
                SQL_ += u") as corridor, "
            SQL_2 += SQL_    

                                                                        
            SQL_ = ""
            SQL_ += u"test_map t4 LEFT OUTER JOIN operator t5 ON (t4.operator = t5.id), "            
            SQL_ += u"stand t6, test_type t7 "            
            
            SQL_ += u"where t1.id = t1_.id  "            
            SQL_ += u"and t1.item = t2.id "            
            SQL_ += u"and t1.coil = t3.id "
            SQL_ += u"and t2.test_map = t4.id "
            SQL_ += u"and t2.serial_number = " + str(self.iSerialNumberID) + " "                                                                  
            SQL_ += u"and t3.id = corridor.idCoil "
            SQL_ += u"and t1.stand = t6.id "
            SQL_ += u"and t6.test_type = t7.id "
            SQL_ += u"and code = :code "
            SQL_ += u"order by t3.coilnumber, t3.tap'"                            
            
            SQL += SQL_    
            SQL_2 += SQL_    

            accurR = u"'Коридор " + str(self.Devices.data['accuracy']['r']) + "%'"
            accurI = u"'Коридор " + str(self.Devices.data['accuracy']['a']) + "%'"
            
            inputParms = {u'snID':self.iSerialNumberID, u'SQL': SQL, u'SQL_2': SQL_2, u'accuracyR': accurR, u'accuracyI': accurI, u'gost_id':self.gost_id}
            '''
            try:
                rpt = FRPrintForm(u'error_estimation.fr3' , inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
                rpt.preview()
            # rpt.design()
            except:
                pass
'''
        
            import ReportsExcel      

#            ReportsExcel.CommonReport(self.env.db, self.test_map, self.item, True)
#            ReportsExcel.CommonReport(self.env.db, None, None, True)
#            ReportsExcel.CommonReport(self.env.db, self.iSerialNumberID, accurR, accurI, self.gost_id, True)
            ReportsExcel.CommonReport(self.env, self.iSerialNumberID, accurR, accurI, self.gost_id, True, self)
        
        
        
        
        
        
        
        
        

    def pushButton3_Click(self):
                
        import ReportsExcel
        try:
            self.query_9 = QSqlQuery(self.env.db)
            
            test_map = 378136
                     
            strSQL = """                
select id as item
from item
where test_map = """ + str(test_map) + """
and istested
order by id
"""

                
            self.query_9.prepare(strSQL)
            if not self.query_9.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
                return
            else:    
                model_9.setQuery(self.query_9)
                 
            for i in range(model_9.rowCount()):
                item = int(model_9.record(i).field('item').value().toString())

                QMessageBox.warning(self, u"Предупреждение", u"1", QMessageBox.Ok)
                if self.ui.checkBox_2.isChecked():
                    ReportsExcel.verification_protocol(self.env.db, test_map, item, True)
                else:    
                    ReportsExcel.verification_protocol(self.env.db, test_map, item, False)
                QMessageBox.warning(self, u"Предупреждение", u"2", QMessageBox.Ok)
                
                if i == 2:
                    break
        except:
            pass
                
        return        
                
                
                
                
                
#        self.calcMapItem((0, 1, 2, 5, 6))
#        '''                
        import ReportsExcel
           
        ReportsExcel.verification_protocol(self.env.db, 378136, 1293640, True)
#        ReportsExcel.verification_protocol(self.env.db, 378136, 1293640, False)
        return
#        '''
        
        
        
        
        
        from win32com.client import Dispatch, constants
        try:
            xl = Dispatch('Excel.Application')
        except:
            QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel", QMessageBox.Ok)
            return             

        inputFile = os.getcwd() + u'\\rpt\\Протокол_поверки.xlsx'  # Шаблон

        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(None, u"Предупреждение", u"Не открывается файл: " + inputFile, QMessageBox.Ok)
            return

        ws = wb.Worksheets(1)   
        
#        print xl.ActiveWindow
#        print xl.ActiveWindow.SelectedSheets.PrintOut()
        
        
#      MsExcel.ActiveWindow.SelectedSheets.PrintOut(From := 1, To := PageCount, Copies:=1, Collate:=True);
        
#      ActiveWindow.SelectedSheets.PrintOut Copies:=1, Collate:=True, _
#        IgnorePrintAreas:=False
#End Sub



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
        #points = [[1,2],[3,4],[5,6]]                
        #points1 = [[0.1,0.2],[0.3,0.4],[0.5,0.6]]
                
#        self.oItem = Item(self.env, None, self.oMap.iMapID, True)
                        
        wind = archive(env)
        wind.setEnabled(True)
        #if wind.is_show: 
        wind.show()
        sys.exit(app.exec_())
