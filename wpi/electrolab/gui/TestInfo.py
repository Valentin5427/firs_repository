#coding=utf-8
u"""
Created on 19.08.2011
#14
@author: Anton
"""
import sys

from PyQt5.QtWidgets import QDialog, QAbstractItemView, QHeaderView, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant,   QVariant, QEvent
from dpframe.tech import pgdb
from electrolab.gui.common import UILoader
from electrolab.gui.reporting import FRPrintForm


import datetime
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
from dpframe.tech.pgdb import DBParam
from electrolab.gui.devices   import Devices

from electrolab.report_otk import  reportTT, reportTN, reportOLS, reportTP
# from electrolab.gui.Config_base import   db

# from tech.integration import INI, LOG, FileSystem
import json
import os
from electrolab.gui import ReportsExcel
from electrolab.gui.msgbox import msgBox



# oINI = INI('integration.ini')
# log = LOG(oINI.log)




# 7.06.2017
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()


lstOLS = ['Этикетки (КТ)',"Этикетки (КТ И Сопротивление)","Протокол ПСИ","Общий отчет","Отчет о браке","Отчет о прохождении заказа","Шильдик","Паспорт"]
lstTN = ['Этикетки (Сопротивления)', "Этикетки (Погрешности)", "Этикетки (Погрешности И Сопротивление)","Протокол ПСИ","Протокол поверки", "Общий протокол","Паспорт", 'Шильдик',"Отчет о браке", "Отчет о прохождении заказа"]
lstTT = ["Общий отчет", "Вольт-амперная харастеристика намагничивания обмоток", "Результаты поверки тока намагничивения вторичных обмоток", "Протокол поверки", "Отчет о прохождении заказа", "Отчет о браке", "Протокол ПСИ", "Паспорт", 'Шильдик','Этикетка дополнительные испытания']
lstTP = ["Протокол ПСИ","Вольт-амперная харастеристика намагничивания обмоток",  'Шильдик', "Отчет о прохождении заказа", "Отчет о браке","Паспорт"]
basedir = os.path.abspath(os.getcwd())
path = '\\'.join(basedir.split('\\')[:3]) + '\\report_otk\\'

tt = 1
tn = 2
tp = 3
ol = 4

            
# dpframe.tech.pgdb.DBParam()
#         oDBConectParam = pgdb.INI(_sINIFile).get_dbparam()
#         oConnect = pgdb.Connect(oDBConectParam)


class DPField(object):

    def __init__(self, table, field, alias=None, visible=True, size=None, subquery=None):
        self.table = table
        self.field = field
        self.alias = alias or field
        self.visible = visible
        self.size = size
        self.subquery = subquery

    def field_name(self):
        if(self.subquery == None):
            return u"%s.%s" % (self.table, self.field)
        else:
            return u"(%s) as %s" % (self.subquery, self.field)

class DPQuery(psycopg2.extensions.cursor):

    def prepare(self, _query=None, _fields=None, _condition=None, _args=None):
        self.statment = _query
        print(5454, self.statment)
        self.fields = _fields
        self.params = _args
        self.condition = _condition

    def build(self, _condidion=None):
        print(8787878)
        #todo: make as lambda
        sFieldList = []
        self.condition = _condidion
        for index in self.fields:
            sFieldList.append(self.fields[index].field_name())
        fieldlist = u', '.join(sFieldList)
        statment = self.statment % (fieldlist,)
        if self.condition:
            return statment + u' where ' + self.condition + 'order by  sn.makedate DESC, sn.serialnumber DESC LIMIT 10000'
        else:
            return statment + 'order by  sn.makedate DESC, sn.serialnumber DESC LIMIT 10000'

    def execute(self, _condidion=None, args=None):
        psycopg2.extensions.cursor.execute(self, self.build(_condidion), args)


class DPModel(QAbstractTableModel):
    def __init__(self, _connect, _query, _fields):
        super(QAbstractTableModel, self).__init__()
        self.connect = _connect.connection

        self.metadata = _fields

        self.cursor = self.connect.cursor(cursor_factory=DPQuery)
        self.cursor.prepare(_query, self.metadata)
        print(43435, _query, self.metadata)
        self.select()

    def select(self, _condition=None, _args=None):
        print(8780980,  _condition, _args )
        self.layoutAboutToBeChanged.emit()
        self.cursor.execute(_condition, _args)
        self.layoutChanged.emit()
        # self.dataChanged.emit(self.createIndex(0, 0), oldIndex)


    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.cursor.rowcount

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.metadata)

    def data(self, QModelIndex, int_role=None):
        print('dataaaaa')
        if QModelIndex.row() == -1:
            return

        if(int_role == Qt.DisplayRole):
            print(45345, QModelIndex.row() , self.cursor.rownumber )

            self.cursor.scroll(QModelIndex.row() - self.cursor.rownumber)
            return QVariant(self.cursor.fetchone()[QModelIndex.column()])
        else:
            return QVariant()

    def setDatat(self, _index, _vlue, _role=None):
        print(54444444)
        # if self.cursor.rownumber != QModelIndex.row():
        if(_role == Qt.DisplayRole):
            self.cursor.scroll(_index.row() - self.cursor.rownumber)
            self.cursor.fetchone()[_index.column()]
            return True
        else:
            return False

    # def index(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
    #     return QAbstractTableModel.index(self, p_int, p_int_1, None)#QModelIndex_parent)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if(int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal):
            return QVariant(self.metadata[p_int].alias)
        # if(int_role == Qt.DisplayRole and Qt_Orientation == Qt.Vertical):
        #     return QVariant()
        return QAbstractTableModel.headerData(self, p_int, Qt_Orientation, int_role)

    # def index(self, _iRow, _iColumn, QModelIndex_parent=None, *args, **kwargs):
    #     index = self.createIndex(_iRow, _iColumn, QModelIndex_parent)
    #     index.


class TestInfo(QDialog, UILoader):
    def __init__(self, _window, _env):
        super(QDialog, self).__init__()
        self.env = _env
        self.setUI(self.env.config, u"TestInfo.ui")
        param = DBParam(
            self.env.config.db.host
            , self.env.config.db.database
            , self.env.config.db.user
            , self.env.config.db.password
        )
        self.connect = pgdb.Connect(param)
        self.type_transformer = None



        self.ui.leYar.setText(str(datetime.date.today().year)[2:4])

        self.Devices = Devices(_env)


        self.metadata = {
            0: DPField(u'sn', u'id', None, False)
            , 1: DPField(u'sn', u'makedate', u'Год')
            , 2: DPField(u'sn', u'serialnumber', u'Номер')
            , 3: DPField(u'sn', u'transformer', None, False)
            , 4: DPField(u'sn', u'series', u'Серия')
            , 5: DPField(u'sn', u'ordernumber', u'Заказ')
            , 6: DPField(u'sc', u'sc', u'Испытания')
            , 7: DPField(u'tf', u'fullname', u'Трансформатор')
            , 8: DPField(u'tf', u'type_transformer', u'Тип Трансформатора',None,False)
            # , 7: DPField(None, u'sc', u'Втор. обм', subquery=u'exists(select id from item where sn.id = item.serial_number)')
            # , 8: DPField(None, u'ap', u'Акт. час.')
            # , 9: DPField(None, u'lt', u'Окон. пов.')
        }

        sQuery = f'''
            select
                %s
            from
              serial_number sn
            inner join
              transformer tf
            on
              tf.id = sn.transformer
            left join
                (select distinct item.serial_number, 'Есть' as sc  from item) sc
            on
              sc.serial_number = sn.id
              --where sn.makedate = {str(datetime.datetime.today().year)[2:]}
              --limit 1000
        '''
        print(sQuery)
        self.serialNumberModel = DPModel(self.connect, sQuery, self.metadata)
        self.ui.tableView.setModel(self.serialNumberModel)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.selectionModel().selectionChanged.connect(self.change_comboBox)

        #TODO: в будущем перенести в конструктор собственного виджета грида
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.tableView.installEventFilter(self)

        for idx in self.metadata:
            fld = self.metadata[idx]
            self.ui.tableView.setColumnHidden(idx, not fld.visible)
            if(fld.size):
                header.resizeSection(idx, fld.size)
            # if fld_md.visiblePosition >= 0:
            #     header.moveSection(header.visualIndex(fld_md.cid), fld_md.visiblePosition)

        header.setStretchLastSection(True)
        # header.setResizeMode(QHeaderView.ResizeToContents)
        #END TODO

        self.ui.pushButton.clicked.connect(self.pushButton_Click)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.ui.pushButton_3.clicked.connect(self.pushButton_3_Click)
        self.ui.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
        self.ui.tableView.clicked.connect(self.change_transformator)
        
        
        self.ui.pushButton_2.setVisible(False)
        self.ui.pushButton_3.setVisible(False)

        self.data = {}
        self.read_json()
        
        # self.setFilter()
        print(54654364575487)

    def change_transformator(self):
        print(3343)


    def comboBox_currentIndexChanged(self, ind):
        self.ui.checkBox.setEnabled(ind == 1 or ind == 2)
        self.ui.checkBox.setChecked(ind == 1 or ind == 2)
        self.ui.radioButton.setEnabled(ind == 1 or ind == 2)
        self.ui.radioButton_2.setEnabled(ind == 1 or ind == 2)



    def to_int(self, _value):
        print(656757,_value)
        val = str(_value)
        val = ' '.join(val.split())

        try:
            return int(val)
        except:
            return  None



    def to_string(self, _value):
        if _value in (None,''):
            return None
        try:
            return str(_value)
        except:
            return None


    def equalCondition(self, _fieldMetaData, _value):
        if _value != None:
            if issubclass(type(_value), int):
                return f'{_fieldMetaData.field_name()} = {_value}'
            else:
                return f"{_fieldMetaData.field_name()} = '{_value}'"



    def likeCondition(self, _fieldMetaData, _value):
        if _value != None:
            return str(_fieldMetaData.field_name()) + u" like '%" + str(_value) + u"%'"


    def setFilter(self):
        self.ui.tableView.selectRow(0)
        row = self.get_row()
        print(16,row)
        print('setFilter')

        condition = []
        c1 = self.equalCondition(DPField(u'sn', u'makedate'), self.to_int(self.ui.leYar.text()))
        if c1: condition.append(c1)

        c1 = self.equalCondition(DPField(u'sn', u'serialnumber'), self.to_int(self.ui.leNumber.text()))
        if c1: condition.append(c1)

        c1 = self.equalCondition(DPField(u'sn', u'series'), self.to_string(self.ui.leSeries.text()))
        if c1: condition.append(c1)

#tam         c1 = self.equalCondition(DPField(u'sn', u'ordernumber'), self.to_string(self.ui.leOrder.text()))
        c1 = self.likeCondition(DPField(u'sn', u'ordernumber'), self.to_string(self.ui.leOrder.text()))
        if c1: condition.append(c1)

        c1 = self.likeCondition(DPField(u'tf', u'fullname'), self.to_string(self.ui.leTrans.text()))
        if c1: condition.append(c1)
        print(3543545, condition)

        if len(condition):
            print(2222)
            self.ui.tableView.model().select(u" and ".join(condition))
        else:
            print(4444)
            self.ui.tableView.model().select()

        if self.ui.tableView.model().rowCount() > 0:
            self.change_comboBox()


    def get_row(self):
        if self.ui.tableView.model().rowCount()>0:
            row = self.ui.tableView.selectionModel().currentIndex().row()
            if row == -1:
                row = 0
            return row
        return 0

    def change_comboBox(self):
        print(23556575868)
        row = self.get_row()
        current_transformator = self.get_type_transformator(row) # тип текущего выбранного трансофрматора
        print('тип текущего выбранного трансофрматора', current_transformator)
        print('тип ghtlsle выбранного трансофрматора', self.type_transformer)
        if self.type_transformer !=  current_transformator:
            self.ui.comboBox.clear()
            self.type_transformer = current_transformator
            if self.type_transformer == 1:
                self.ui.comboBox.insertItems(0, lstTT)
            elif self.type_transformer == 2 :
                self.ui.comboBox.insertItems(0, lstTN)
            elif self.type_transformer == 3:
                self.ui.comboBox.insertItems(0,lstTP)
            else:
                self.ui.comboBox.insertItems(0, lstOLS)


        #         self.ui.comboBox.insertItems(0, lstTN)
        #     elif self.type_transformer in (16,13,12):
        #         self.ui.comboBox.insertItems(0,lstOLS)
        #     elif self.type_transformer in (23,):
        #         self.ui.comboBox.insertItems(0,lstTP)
        #     else:
        #         self.ui.comboBox.insertItems(0, lstTT)
        #
        # tt = 1
        # tn = 2
        # tp = 3
        # ol = 4

    def get_type_transformator(self,row):
        print(2356723, row)
        if int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 8), Qt.DisplayRole).value()) in (11,10,9,8):
            return tn
        if int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 8), Qt.DisplayRole).value()) in (16,13,12):
            return ol
        if int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 8), Qt.DisplayRole).value()) in (23,):
            return tp
        return tt




    def printReport(self,dd):
        return

    def eventFilter(self, _object, _event):
        u""""""
        if _event.type() == QEvent.KeyPress and _event.key() == Qt.Key_Return:
            selection = self.ui.tableView.selectionModel().selection().indexes()
            if len(selection):
                self.printReport(selection[0])
        return QDialog.eventFilter(self, _object, _event)
        # return True
    
    def print_report(self, _iItemID, _SQL, _accuracyR, _accuracyI):
        u"""Печать"""
        if not _iItemID:
            return
        #10.02
        #inputParms = {u'snID':_iItemID}
        inputParms = {u'snID':_iItemID, u'SQL': _SQL, u'accuracyR': _accuracyR, u'accuracyI': _accuracyI}
        # print 'inputParms=', inputParms
#        QMessageBox.warning(self, u"Предупреждение", u"1111111111111", QMessageBox.Ok)
        try:
            rpt = FRPrintForm(u'error_estimation.fr3' ,inputParms , self.env)
            rpt.preview()
            # rpt.design()
        except:
            pass


    def pushButton_2_Click(self):
        ReportsExcel.BAX_test()
        pass

    def pushButton_3_Click(self):
        ReportsExcel.BAX_test_2()

    def searсh_item(self,serianumber, test):
       SQL =  f"""select item.id FROM item
                inner join test_map  on item.test_map = test_map.id
                inner join stand on test_map.stand = stand.id
            where item.serial_number = {serianumber} and stand.test_type = {test} and item.istested
            order by item.id DESC
            LIMIT 1"""
       print(SQL)
       query = QSqlQuery(SQL,self.env.db)
       if query.first():
           return query.value(0)
       else:
           return False









    def pushButton_Click(self):
        self.write_json() # Вставил здесь поскольку событие CloseEvent почему-то не срабатывает
        row = self.get_row()
        print("тип трансформатора" ,self.type_transformer )
        if self.type_transformer == 1:
            self.report_generationTT(row)
        elif self.type_transformer == 2:
            self.report_generationTN(row)
        elif   self.type_transformer == 3:
            self.report_generationTP(row)
        else:
            self.report_generationOLS(row)


    def  report_generationTN(self, row):
        zakaz = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).value())
        series = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).value())
        print('Формирование отчетов для трасформаторовт ЗНОЛ')
        print(self.ui.comboBox.currentIndex())
        sn = int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0), Qt.DisplayRole).value())
        print(134, sn)
        if self.ui.comboBox.currentIndex() == 0:
            item = self.searсh_item(sn,20)
            reportTN.open_excel(path + 'stickerTTP.xlsx', None)
            reportTN.select_Stikert(item)
            reportTN.stickerTTP('R')
        elif self.ui.comboBox.currentIndex() == 1:
            item = self.searсh_item(sn,21)
            reportTN.open_excel(path + 'stickerTTP.xlsx', None)
            reportTN.select_Stikert(item)
            reportTN.stickerTTP('P')
        elif self.ui.comboBox.currentIndex() == 2:
            item = self.searсh_item(sn,22)
            reportTN.open_excel(path + 'stickerTTP.xlsx', None)
            reportTN.select_Stikert(item)
            reportTN.stickerTTP('RP')
        elif self.ui.comboBox.currentIndex() == 3:
            item = self.searсh_item(sn,19)
            if item:
                reportTN.open_excel(path +'protocolTN.xlsx', None)
                reportTN.select_result(item)
                reportTN.data_TN(reportTN.fill_TNprotocol_full)
        elif self.ui.comboBox.currentIndex() == 4:
            item = self.searсh_item(sn, 19)
            if item:
                reportTN.open_excel(path + 'poverkaTN.xlsx', None)
                reportTN.select_result(item)
                reportTN.data_TN(reportTN.fill_TNpoverka_full)

        elif self.ui.comboBox.currentIndex() == 5:
            reportTN.open_excel(path + 'full_repTN.xlsx', None)
            reportTN.select_repTN(sn)

        elif self.ui.comboBox.currentIndex() == 6:
            item = self.searсh_item(sn, 19)
            if item:
                reportTN.open_excel(path + 'passportTN.xlsx', None)
                reportTN.select_passportTN(item, reportTN.fill_passportTN_full)
        elif self.ui.comboBox.currentIndex() == 7:
            for i in (19,20,21,22):
                item = self.searсh_item(sn,i)
                if item:
                    reportTN.open_excel(path +'ticket_tn.xlsx', None)
                    reportTN.select_passportTN(item, reportTN.fill_ticket_tn)
                    break

        elif self.ui.comboBox.currentIndex() == 8:
            self.print_repdefect()

        elif self.ui.comboBox.currentIndex() == 9:
            SQL = """select id, serialnumber
            from serial_number
            where ordernumber = '""" + zakaz + """'
            and series = '""" + series + """'
            order by serialnumber
            """
            print(111, SQL)
            model_2.clear()
            # model_2.reset()
            model_2.setQuery(SQL, self.env.db)

            spisok = []

            codes = ['16', '17', '18', '7', '5']

            for i in range(model_2.rowCount()):
                spisok += [[int(model_2.record(i).field('serialnumber').value()), [], [], [], [], [], []]]
                for j in range(len(codes)):
                    spisok[i][j + 1] += []

                    '''
                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item, t1.istested, gost_id
from item as t1, test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = """ + model_2.record(i).field('id').value().toString() + """
and t5.code = """ + codes[j] + """
order by t2.createdatetime
"""
'''

                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
            to_char(t2.createdatetime, 'hh:mi') as createtime,
            t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item,
            --cast(t1.istested as integer) istested, cast(t1_.iscritical as integer) iscritical,
            case when t1.istested then 1 else 0 end as istested,
            case when t1_.iscritical then 1 else 0 end as iscritical,
            t1.defect, t1_.fullname as name_defect, gost_id
            from item as t1 left outer join defect as t1_ on (t1.defect = t1_.id),
            test_map as t2, stand as t3, operator as t4, test_type as t5
            where t1.test_map = t2.id
            and t2.stand = t3.id
            and t2.operator = t4.id
            and t3.test_type = t5.id
            and t1.serial_number = """ + str(model_2.record(i).field('id').value()) + """
            and t5.code = """ + codes[j] + """
            order by t2.createdatetime
            """
                    print(222, SQL)
                    model_3.clear()
                    # model_3.reset()
                    model_3.setQuery(SQL, self.env.db)

                    for k in range(model_3.rowCount()):
                        #                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value().toString()), unicode(model_3.record(k).field('fio').value().toString()), model_3.record(k).field('istested').value().toString()]]
                        spisok[i][j + 1] += [
                            [str(model_3.record(k).field('createdate').value()), model_3.record(k).field('fio').value(),
                             int(model_3.record(k).field('istested').value()),
                             int(model_3.record(k).field('iscritical').value()),
                             model_3.record(k).field('name_defect').value()]]


            print(spisok)
            reportTN.repMoveTask(zakaz, series, spisok)





    def report_generationOLS(self,row):
        selection = self.ui.tableView.selectionModel().selection().indexes()
        row = selection[0].row()
        index = self.ui.tableView.model().index(row, 0)
        sn = int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0), Qt.DisplayRole).value())
        if self.ui.comboBox.currentIndex() == 0:
            item = self.searсh_item(sn, 17)
            if item:
                reportOLS.open_excel(path +'stickerKT.xlsx', None)
                reportOLS.select_Stikert(item)
                reportOLS.stickerKT()
                return

        if self.ui.comboBox.currentIndex() == 1:
            item = self.searсh_item(sn, 16)
            if item:
                reportOLS.open_excel(path +'stickerOLS.xlsx', None)

                reportOLS.select_Stikert(item)
                reportOLS.stickerRKT()
                return

        if self.ui.comboBox.currentIndex() == 2:
            item = self.searсh_item(sn, 18)
            if item:
                reportOLS.open_excel(path +'protocolOLS.xlsx', None)
                reportOLS.select_result(item)
                reportOLS.data_OLSprotocol()
                return



        if self.ui.comboBox.currentIndex() == 3:
            reportOLS.open_excel(path +'full_repOLS.xlsx', None)
            reportOLS.select_repOLS(sn)
            return


        if self.ui.comboBox.currentIndex() == 4:
            self.print_repdefect()
            return

        if self.ui.comboBox.currentIndex() == 5:
            zakaz = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).value())
            series = str(
                self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).value())
            SQL = """select id, serialnumber
                        from serial_number
                        where ordernumber = '""" + zakaz + """'
                        and series = '""" + series + """'
                        order by serialnumber
                        """
            print(111, SQL)
            model_2.clear()
            # model_2.reset()
            model_2.setQuery(SQL, self.env.db)

            spisok = []

            codes = ['14', '13',  '7', '15']

            for i in range(model_2.rowCount()):
                spisok += [[int(model_2.record(i).field('serialnumber').value()), [], [], [], [], [], []]]
                for j in range(len(codes)):
                    spisok[i][j + 1] += []

                    '''
                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item, t1.istested, gost_id
from item as t1, test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = """ + model_2.record(i).field('id').value().toString() + """
and t5.code = """ + codes[j] + """
order by t2.createdatetime
"""
'''

                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
                        to_char(t2.createdatetime, 'hh:mi') as createtime,
                        t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item,
                        --cast(t1.istested as integer) istested, cast(t1_.iscritical as integer) iscritical,
                        case when t1.istested then 1 else 0 end as istested,
                        case when t1_.iscritical then 1 else 0 end as iscritical,
                        t1.defect, t1_.fullname as name_defect, gost_id
                        from item as t1 left outer join defect as t1_ on (t1.defect = t1_.id),
                        test_map as t2, stand as t3, operator as t4, test_type as t5
                        where t1.test_map = t2.id
                        and t2.stand = t3.id
                        and t2.operator = t4.id
                        and t3.test_type = t5.id
                        and t1.serial_number = """ + str(model_2.record(i).field('id').value()) + """
                        and t5.code = """ + codes[j] + """
                        order by t2.createdatetime
                        """
                    print(222, SQL)
                    model_3.clear()
                    # model_3.reset()
                    model_3.setQuery(SQL, self.env.db)

                    for k in range(model_3.rowCount()):
                        #                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value().toString()), unicode(model_3.record(k).field('fio').value().toString()), model_3.record(k).field('istested').value().toString()]]
                        spisok[i][j + 1] += [
                            [str(model_3.record(k).field('createdate').value()), model_3.record(k).field('fio').value(),
                             int(model_3.record(k).field('istested').value()),
                             int(model_3.record(k).field('iscritical').value()),
                             model_3.record(k).field('name_defect').value()]]

            print(spisok)
            reportOLS.repMoveTask(zakaz, series, spisok)
            return

        if self.ui.comboBox.currentIndex() == 6:
            for i in (16,17,18):
                item = self.searсh_item(sn,i)
                if item:
                    if reportOLS.open_excel(path +'ticket_ols.xlsx', None):
                        reportOLS.select_resultOLS(item, reportOLS.fill_ticket_ols)
                        return

        if self.ui.comboBox.currentIndex() == 7:
            print(6544)
            item = self.searсh_item(sn,18)
            if item:
                if reportOLS.open_excel(path +'passportOLS.xlsx', None):
                    reportOLS.select_passportOLS(item, reportOLS.fill_passportOLS_full)
                    return


        QMessageBox.warning(None, u"Ошибка!!!!!", 'Не удалось найти результаты испытания', QMessageBox.Ok)


    def report_generationTP(self,row):
        zakaz = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).value())
        series = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).value())
        print('Формирование отчетов для трасформаторовт ЗНОЛ')
        print(self.ui.comboBox.currentIndex())
        sn = int(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0), Qt.DisplayRole).value())
        print(134, sn)

        selection = self.ui.tableView.selectionModel().selection().indexes()
        if len(selection):
            #            QMessageBox.warning(self, u"Предупреждение", u"4", QMessageBox.Ok)
            row = selection[0].row()
            index = self.ui.tableView.model().index(row, 0)
            serial_number = str(self.ui.tableView.model().data(index, Qt.DisplayRole).value())

            print('id=', serial_number)
            '''
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 1), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 2), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 3), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 6), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 7), Qt.DisplayRole).toString()
            '''
            fullname = str(
                self.ui.tableView.model().data(self.ui.tableView.model().index(row, 7), Qt.DisplayRole).value())
            serialnumbel = str(
                self.ui.tableView.model().data(self.ui.tableView.model().index(row, 2), Qt.DisplayRole).value())
            year = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 1), Qt.DisplayRole).value())
            zakaz = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).value())
            series = str(
                self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).value())
            print(54345, fullname, serialnumbel, zakaz, series)
        else:
            return





        if self.ui.comboBox.currentIndex() == 0:
            items = self.searсh_item(sn, 5)
            if items != []:
                if reportTP.open_excel(path + 'protocolTP.xlsx', 'hp LaserJet 1320 series (10.5.0.20)'):
                    reportTP.select_result(items)
                    reportTP.data_TP(reportTP.fill_TPprotocol_full)

        if self.ui.comboBox.currentIndex() == 5:
            items = self.searсh_item(sn, 5)
            if items != []:
                if reportTP.open_excel(path + 'passportTP.xlsx', 'hp LaserJet 1320 series (10.5.0.20)'):
                    reportTP.select_passportTP(items, reportTP.fill_passportTP_full)

        if self.ui.comboBox.currentIndex() == 2:
            items = self.searсh_item(sn, 23)
            if items != []:
                if reportTP.open_excel(path + 'ticket_tp.xlsx', 'hp LaserJet 1320 series (10.5.0.20)'):
                    reportTP.select_passportTP(items, reportTP.fill_ticket_tp)

        if self.ui.comboBox.currentIndex() == 3:

                    '''
                    #global serialNumberModel
                    print 'zakaz = ', zakaz
                    print 'series = ', series            
                    print 'serialNumberModel.rowCount()= ', self.serialNumberModel.rowCount()            
                    return
                    '''

                    SQL = """select id, serialnumber
        from serial_number
        where ordernumber = '""" + zakaz + """'
        and series = '""" + series + """'
        order by serialnumber
        """
                    print(111, SQL)
                    model_2.clear()
                    # model_2.reset()
                    model_2.setQuery(SQL, self.env.db)

                    spisok = []

                    codes = ['0', '3', '2', '7', '4', '1']

                    for i in range(model_2.rowCount()):
                        spisok += [[int(model_2.record(i).field('serialnumber').value()), [], [], [], [], [], []]]
                        for j in range(len(codes)):
                            spisok[i][j + 1] += []

                            '''
                            SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
        to_char(t2.createdatetime, 'hh:mi') as createtime,
        t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item, t1.istested, gost_id
        from item as t1, test_map as t2, stand as t3, operator as t4, test_type as t5
        where t1.test_map = t2.id
        and t2.stand = t3.id
        and t2.operator = t4.id
        and t3.test_type = t5.id
        and t1.serial_number = """ + model_2.record(i).field('id').value().toString() + """
        and t5.code = """ + codes[j] + """
        order by t2.createdatetime
        """
        '''

                            SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
        to_char(t2.createdatetime, 'hh:mi') as createtime,
        t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item,
        --cast(t1.istested as integer) istested, cast(t1_.iscritical as integer) iscritical,
        case when t1.istested then 1 else 0 end as istested,
        case when t1_.iscritical then 1 else 0 end as iscritical,
        t1.defect, t1_.fullname as name_defect, gost_id
        from item as t1 left outer join defect as t1_ on (t1.defect = t1_.id),
        test_map as t2, stand as t3, operator as t4, test_type as t5
        where t1.test_map = t2.id
        and t2.stand = t3.id
        and t2.operator = t4.id
        and t3.test_type = t5.id
        and t1.serial_number = """ + str(model_2.record(i).field('id').value()) + """
        and t5.code = """ + codes[j] + """
        order by t2.createdatetime
        """
                            print(222, SQL)
                            model_3.clear()
                            # model_3.reset()
                            model_3.setQuery(SQL, self.env.db)

                            for k in range(model_3.rowCount()):
                                #                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value().toString()), unicode(model_3.record(k).field('fio').value().toString()), model_3.record(k).field('istested').value().toString()]]
                                spisok[i][j + 1] += [[str(model_3.record(k).field('createdate').value()),
                                                      model_3.record(k).field('fio').value(),
                                                      int(model_3.record(k).field('istested').value()),
                                                      int(model_3.record(k).field('iscritical').value()),
                                                      model_3.record(k).field('name_defect').value()]]
                    print(234, spisok)
                    ReportsExcel.repMoveTask(zakaz, series, spisok)
                    return

        if self.ui.comboBox.currentIndex() == 4:
            self.print_repdefect()
            return

        if self.ui.comboBox.currentIndex() == 1:
            try:
                from electrolab.gui.TestCoil import TestCoil
                self.oTestCoil = TestCoil(self.env, None, None, None, None, self)

                if self.ui.radioButton.isChecked():
                    code = 3
                if self.ui.radioButton_2.isChecked():
                    code = 4
                sn = f"{year}-{serialnumbel}"
                coilsInfa = self.oTestCoil.buildCoilsInfa(serial_number, self.ui.checkBox.isChecked(), code)
                ReportsExcel.BAX_coil1(fullname, sn, zakaz, coilsInfa, code)
                return
            except Exception as ex:
                QMessageBox.warning(None, u"Предупреждение",
                                    f""" {ex}""",
                                    QMessageBox.Ok)
        pass

    def print_repdefect(self):
        from electrolab.gui.repDefect import repDefect
        wind = repDefect(self.env)
        wind.exec_()
        return

    def report_generationTT(self,row):
        print('Формирование отчетов для трасформаторовт тока')
        if self.ui.comboBox.currentIndex() == 5:
            self.print_repdefect()
            return



        selection = self.ui.tableView.selectionModel().selection().indexes()
        if len(selection):
#            QMessageBox.warning(self, u"Предупреждение", u"4", QMessageBox.Ok)
            row = selection[0].row()
            index = self.ui.tableView.model().index(row, 0)
            serial_number = str(self.ui.tableView.model().data(index, Qt.DisplayRole).value())

            print ('id=', serial_number)
            '''
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 1), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 2), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 3), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 6), Qt.DisplayRole).toString()
            print self.ui.tableView.model().data(self.ui.tableView.model().index(row, 7), Qt.DisplayRole).toString()
            '''
            fullname = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 7), Qt.DisplayRole).value())
            serialnumbel = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 2), Qt.DisplayRole).value())
            year = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 1), Qt.DisplayRole).value())
            zakaz = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 5), Qt.DisplayRole).value())
            series = str(self.ui.tableView.model().data(self.ui.tableView.model().index(row, 4), Qt.DisplayRole).value())
            print(54345, fullname,serialnumbel,zakaz,series)
        else:
            return    



                    
        if self.ui.comboBox.currentIndex() == 0:
            try:
                # print 'q1'
                from electrolab.gui.Archive import archive
                # print 'q2'
                self.oArchive = archive(self.env)
                # print 'q3'
                self.oArchive.iSerialNumberID = serial_number
                print(765757,self.oArchive.iSerialNumberID)
                self.oArchive.viewTesting(0)
                self.oArchive.calcMapItem((2, 2))
                self.oArchive.calcMapItem((0,1,2,5,6))
    #            self.oArchive.calcMapItem((0,1,2,5,6))
                if self.oArchive.test_map == None:
                    QMessageBox.warning(None, u"Предупреждение",
                                          u"""Нет данных:host: """,
                                        QMessageBox.Ok)
                    return
                # print 'q5'
                from electrolab.gui.TestCoil import TestCoil

                # print 'q'
                self.oTestCoil = TestCoil(self.env, None, None, None, None, self)
                # print 'w'
                # Расчет коридоров для цеха
                self.oTestCoil.codeTypeTest = 3
                rez = self.oTestCoil.calcGlobal(None, serial_number, 16, None, None, False)
                print(7567, rez)
                # print 'e'
                if rez in (None,False):
                    self.oTestCoil.globalCorridors = [[-1, -1, -1, 0, 0, 0, 0]]
                globalCorridors = []
                for i in range(len(self.oTestCoil.globalCorridors)):
                    if str(self.oTestCoil.globalCorridors[i][1]) == self.oArchive.ordernumber:
                        globalCorridors += [self.oTestCoil.globalCorridors[i]]
                # print 'r'
                #
                # Расчет коридоров для лаборатории
                self.oTestCoil.codeTypeTest = 4
                rez = self.oTestCoil.calcGlobal(None, serial_number, 16, None, None, False)
                if rez in (None,False):
                    self.oTestCoil.globalCorridors_2 = [[-1, -1, -1, 0, 0, 0, 0]]
                    #return
                globalCorridors_2 = []
                for i in range(len(self.oTestCoil.globalCorridors)):
                    if str(self.oTestCoil.globalCorridors[i][1]) == self.oArchive.ordernumber:
                        globalCorridors_2 += [self.oTestCoil.globalCorridors[i]]

                # print 't'

                accurR = u"'Коридор " + str(self.Devices.data['accuracy']['r']) + "%'"
                accurI = u"'Коридор " + str(self.Devices.data['accuracy']['a']) + "%'"

                ReportsExcel.CommonReport(self.env, serial_number, accurR, accurI, self.oArchive.gost_id, globalCorridors, globalCorridors_2, True)
                return
                # print 'y'
            except Exception as ex:
                QMessageBox.warning(None, u"Предупреждение",
                                    f""" {ex}""",
                                    QMessageBox.Ok)

        
        if self.ui.comboBox.currentIndex() == 1:
            try:
                from electrolab.gui.TestCoil import TestCoil
                self.oTestCoil = TestCoil(self.env, None, None, None, None, self)

                if self.ui.radioButton.isChecked():
                    code = 3
                if self.ui.radioButton_2.isChecked():
                    code = 4
                sn = f"{year}-{serialnumbel}"
                coilsInfa = self.oTestCoil.buildCoilsInfa(serial_number, self.ui.checkBox.isChecked(), code)
                ReportsExcel.BAX_coil1(fullname, sn, zakaz, coilsInfa, code)
                return
            except Exception as ex:
                QMessageBox.warning(None, u"Предупреждение",
                                    f""" {ex}""",
                                    QMessageBox.Ok)


        if self.ui.comboBox.currentIndex() == 2:
            try:
                # 7.06.2017
                model_3.clear()
                # model_3.reset()

                SQL = '''select distinct t1.id 
    from serial_number as t1, serial_number as t2, item as t3, checking_2 as t4
    where t1.series = t2.series
    and t1.ordernumber = t2.ordernumber
    and t2.id =  ''' + serial_number + '''
    and t1.id = t3.serial_number
    and t3.id = t4.item order by t1.id
    '''
                model_3.setQuery(SQL, self.env.db)

                if model_3.rowCount() < 1:
                    QMessageBox.warning(None, u"Предупреждение",
                                          u"""Нет данных по испытаниям """,
                                        QMessageBox.Ok)
                    return
                serial_number_2 = model_3.record(0).field('id').value()

                from electrolab.gui.TestCoil import TestCoil
                self.oTestCoil = TestCoil(self.env, None, None, None, None, self)

                if self.ui.radioButton.isChecked():
                    self.oTestCoil.codeTypeTest = 3
                if self.ui.radioButton_2.isChecked():
                    self.oTestCoil.codeTypeTest = 4



    #            rez = self.oTestCoil.calcGlobal(None, serial_number_2, 16, None, None, self.ui.checkBox.isChecked())
                rez = self.oTestCoil.calcGlobal(None, serial_number_2, 16, self.ui.doubleSpinBox.value(), self.ui.doubleSpinBox_2.value(), self.ui.checkBox.isChecked())
                if rez == False:
                    return

                ReportsExcel.report(fullname, series, zakaz, self.oTestCoil.globalReport, self.ui.doubleSpinBox.value(), self.ui.doubleSpinBox_2.value(), self.ui.checkBox.isChecked())
                return
            except Exception as ex:
                QMessageBox.warning(None, u"Предупреждение",
                                    f""" {ex}""",
                                    QMessageBox.Ok)
            
                                                
                
        if self.ui.comboBox.currentIndex() == 3:
            item = self.searсh_item(serial_number, 1)
            if item:
                reportTT.open_excel(path + 'poverkaTT.xlsx', None)
                reportTT.select_result(item)
                reportTT.TTpoverka(reportTT.fill_poverkaTT_full)
                return

#
                
                
        if self.ui.comboBox.currentIndex() == 4:

            '''
            #global serialNumberModel
            print 'zakaz = ', zakaz
            print 'series = ', series            
            print 'serialNumberModel.rowCount()= ', self.serialNumberModel.rowCount()            
            return
            '''
            
            
            
            SQL = """select id, serialnumber
from serial_number
where ordernumber = '""" + zakaz +"""'
and series = '""" + series + """'
order by serialnumber
"""            
            print(111, SQL)
            model_2.clear()        
            # model_2.reset()
            model_2.setQuery(SQL, self.env.db)

            spisok = []
        
            codes = ['0', '3', '2', '7', '4', '1']
        
            for i in range(model_2.rowCount()):
                spisok += [[int(model_2.record(i).field('serialnumber').value()),[],[],[],[],[],[]]]
                for j in range(len(codes)):
                    spisok[i][j+1] += []
                    
                    '''
                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item, t1.istested, gost_id
from item as t1, test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = """ + model_2.record(i).field('id').value().toString() + """
and t5.code = """ + codes[j] + """
order by t2.createdatetime
"""
'''            

                    SQL = """select t1.serial_number, to_char(t2.createdatetime, 'dd.mm.yyyy') as createdate,
to_char(t2.createdatetime, 'hh:mi') as createtime,
t3.fullname, t5.code, t4.fio, t1.test_map, t1.id as item,
--cast(t1.istested as integer) istested, cast(t1_.iscritical as integer) iscritical,
case when t1.istested then 1 else 0 end as istested,
case when t1_.iscritical then 1 else 0 end as iscritical,
t1.defect, t1_.fullname as name_defect, gost_id
from item as t1 left outer join defect as t1_ on (t1.defect = t1_.id),
test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t1.serial_number = """ + str(model_2.record(i).field('id').value()) + """
and t5.code = """ + codes[j] + """
order by t2.createdatetime
"""            
                    print(222,SQL)
                    model_3.clear()        
                    # model_3.reset()
                    model_3.setQuery(SQL, self.env.db)
                
                    for k in range(model_3.rowCount()):
#                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value().toString()), unicode(model_3.record(k).field('fio').value().toString()), model_3.record(k).field('istested').value().toString()]]
                        spisok[i][j+1] += [[str(model_3.record(k).field('createdate').value()), model_3.record(k).field('fio').value(),
                                            int(model_3.record(k).field('istested').value()), int(model_3.record(k).field('iscritical').value()),
                                            model_3.record(k).field('name_defect').value()]]
            print(234, spisok)
            ReportsExcel.repMoveTask(zakaz, series, spisok)
            return

        if self.ui.comboBox.currentIndex() == 6:
            item = self.searсh_item(serial_number, 5)
            if item:
                reportTT.open_excel(path + 'protocolTT.xlsx', None)
                reportTT.select_result(item)
                reportTT.data_TT(reportTT.fill_TTprotocol_full)
                return


        if self.ui.comboBox.currentIndex() == 7:
            item = self.searсh_item(serial_number, 5)
            if item:
                reportTT.open_excel(path + 'passportTT.xlsx', None)
                reportTT.select_passportTT(item, reportTT.fill_passportTT_full)
                return

        if self.ui.comboBox.currentIndex() == 8:
            for i in (5,4):
                item = self.searсh_item(serial_number, i)
                if item:
                    reportTT.open_excel(path +'ticket_tt.xlsx', None)
                    reportTT.select_passportTT(item, reportTT.fill_ticket_tt)
                    return

        if self.ui.comboBox.currentIndex() == 9:
            item = self.searсh_item(serial_number, 24)
            if item:
                reportTT.open_excel(path +'ticket_tc.xlsx', None)
                reportTT.select_passportTT(item, reportTT.fill_ticket_tc)
                return

        QMessageBox.warning(None, f"Предупреждение",
                            f"Не удалось получить результаты испытания, отчет не будет распечатан",
                            QMessageBox.Ok)

                        
    
    def read_json(self):
        # Чтение параметров с TestInfo.json файла, если таковой имеется
        try:
            f = open('TestInfo.json','r')
            self.data = json.load(f)
            self.ui.doubleSpinBox.setValue(self.data['accuracy']['r'])                                         
            self.ui.doubleSpinBox_2.setValue(self.data['accuracy']['a'])  

        except Exception:
            # print u'Ошибка чтения TestInfo.json!'
            self.data = {}

    def write_json(self):
        # ЗАПИСАТЬ
        f = open('TestInfo.json','w')        
        self.toData()    
        json.dump(self.data, f)

        
    def toData(self):
        self.data = {}        
        self.data['accuracy'] = {}
        self.data['accuracy']['r'] = self.ui.doubleSpinBox.value()
        self.data['accuracy']['a'] = self.ui.doubleSpinBox_2.value()
    
    def closeEvent(self, event):
        # print 'close'
        self.write_json()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import *
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

        wind =TestInfo(app,env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())