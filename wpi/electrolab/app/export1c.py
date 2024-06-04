#-*- coding: UTF-8 -*-
u"""
Created on 11.04.2014
@author: knur
ticket #199
Интеграция с 1С Разбор XML и вставка полученных данных в БД
"""

import time

'''
print 111
time.sleep(5)
print 1111111
f = open('C:/text.txt', 'w')
f.write('ASDFDFGqwer1111111111111111111')
#f.close()
'''



from xml.dom.minidom import Document
# import lxml
from dpframe.tech.pgdb import DBParam
from electrolab.tech.integration import LOG
from electrolab.tech.integration import INI
from electrolab.tech.integration import Export1C
from electrolab.tech.integration import FileSystem
from datetime import datetime
import os
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class Exporter():
    u"""Загрузка данных"""

    PREFIX = u'ExportFromElectrolab'

    def __init__(self, _path, _connect, _oLog, _noException = True):
        u"""_connect - Соединение с БД, _oLog - Журнал"""
        self.sPath = _path
        self.oConnect = _connect
        self.oLog = _oLog
        self.noException = _noException


    def calc_last_export(self):
        sQuery = u'''
            select
                max(acceptdatetime)
            from
                item
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery)
        if cursor.rowcount == 1:
            return cursor.fetchone()[0]
        else:
            return datetime.now()

    def get_last_export(self):
        sQuery = u'''
            select
                valuedatetime
            from
                db_property
            where
                name = 'LastExport'
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery)
        if cursor.rowcount == 1:
            # return datetime.strptime(cursor.fetchone()[0]) or datetime.now()
            return cursor.fetchone()[0] or datetime.now()
        else:
            return datetime.now()

    def set_last_export(self, _lastExportDateTime):
        u""""""
        sQuery = u'''
            update
                db_property
            set
                valuedatetime = %s
            where
                name = 'LastExport'
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, (_lastExportDateTime, ))
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise

    def get_export_records(self, _lastDate, _nextDate):
        u""""""
        sQuery = u'''
            select
               it.ID
               , it.createdatetime as start
               , it.acceptdatetime as complete
               , sn.makedate as yar
               , sn.serialnumber as number
               , df.fullname as defect
               , op.number as tabnumber
               , 'tester' as role
               , tt.code as testcode
               , tt.name as testname
            from
               item it
            inner join
               serial_number sn
            on
               it.serial_number = sn.id
            left join
               defect df
            on
               df.id = it.defect
            inner join
               test_map tm
            on
               it.test_map = tm.id
            inner join
               operator op
            on
               op.id = tm.operator
            inner join
               stand st
            on
               st.id = tm.stand
            inner join
               test_type tt
            on
               st.test_type = tt.id
            where
               it.acceptdatetime > %s
               and it.acceptdatetime <= %s
            union all
            select
               it.ID
               , it.createdatetime as start
               , it.acceptdatetime as complete
               , sn.makedate as yar
               , sn.serialnumber as number
               , df.fullname as defect
               , op.number as tabnumber
               , 'assistant' as role
               , tt.code as testcode
               , tt.name as testname
            from
               item it
            inner join
               serial_number sn
            on
               it.serial_number = sn.id
            left join
               defect df
            on
               df.id = it.defect
            inner join
               test_map tm
            on
               it.test_map = tm.id
            inner join
               operator op
            on
               op.id = tm.assistant
            inner join
               stand st
            on
               st.id = tm.stand
            inner join
               test_type tt
            on
               st.test_type = tt.id
            where
               it.acceptdatetime > %s
               and it.acceptdatetime <= %s
                    '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery, (_lastDate, _nextDate, _lastDate, _nextDate))
        if cursor.rowcount > 0:
            return cursor


    def get_export_coils(self, _idItem):
        u""""""
        sQuery = u'''
--select t1.k, t2.rating
--select decode(t2.rating, NULL, t1.k, t2.rating) as coeff
--from checking_2 t1, coil t2
--where t1.coil = t2.id
--and t1.item = %s
select coil, k
from checking_2
where item = ''' + str(_idItem)

        cursor = self.oConnect.connection.cursor()
#        print 12, _idItem, type(_idItem)
#        cursor.execute(sQuery, (_idItem,))
        cursor.execute(sQuery)
        if cursor.rowcount > 0:
            return cursor


    def GetNewFileName(self, _path):
        return os.path.join(_path, '%s_%s.xml' % (Exporter.PREFIX, unicode(datetime.now().strftime("%Y-%m-%d_%H_%M"))))

    def addAttribute(self, _doc, _node, _sName, _value):
        if _value != None:
            _node.setAttribute(_sName, unicode(_value))

    def process_record(self, _aData, _oXML, _rootNode):
        u""""""
        if(_aData == None or  _oXML == None):
            raise Exception(u'new error')
        itemNode = _oXML.createElement(u'item')
        _rootNode.appendChild(itemNode)
        # it.createdatetime as start
        # , it.acceptdatetime as complete
        # , sn.makedate as yar
        # , sn.serialnumber as number
        # , df.fullname as defect
        # , op.number as tabnumber
        # , 'tester' as role
        # , tt.code testcode
        # , tt.name testname

        #if _aData[8] != 3 and _aData[8] != 4:
        #    return
        self.addAttribute(_oXML, itemNode, u'ID', _aData[0])
        self.addAttribute(_oXML, itemNode, u'start', _aData[1].isoformat())
        self.addAttribute(_oXML, itemNode, u'complete', _aData[2].isoformat())
        self.addAttribute(_oXML, itemNode, u'yar', _aData[3])
        self.addAttribute(_oXML, itemNode, u'number', _aData[4])
        # self.addAttribute(_oXML, itemNode, u'defect', _aData[4] or u'Ok')
        self.addAttribute(_oXML, itemNode, u'defect', _aData[5])
        self.addAttribute(_oXML, itemNode, u'tabnumber', _aData[6])
        self.addAttribute(_oXML, itemNode, u'role', _aData[7])
        self.addAttribute(_oXML, itemNode, u'testcode', _aData[8])
        self.addAttribute(_oXML, itemNode, u'testname', _aData[9])

        # Для испытаний типа 3, 4 вставляем в запись подразделы данных по катушкам
        if _aData[8] == 3 or _aData[8] == 4:
            list = self.get_export_coils(_aData[0])
#            print 2, list
            if list != None:
                for oCoil in list:
#                    print 'oCoil', oCoil 
                    subItemNode = _oXML.createElement(u'coil')
                    itemNode.appendChild(subItemNode)
                    self.addAttribute(_oXML, subItemNode, u'ID', oCoil[0])
                    self.addAttribute(_oXML, subItemNode, u'COEFF', oCoil[1])


    def process(self):
        u"""Обработать коллекцию"""
        self.oLog.info(u'Начало обработки')
        if(not self.oConnect.connected):
            self.oLog.error(u'Not connect to DB')
            return False
        lastDate = self.get_last_export()
#        print 'lastDate=', lastDate
        nextDate = self.calc_last_export()

        self.oLog.info(u'Begin exort from %s to %s' % (lastDate, nextDate))
        list = self.get_export_records(lastDate, nextDate)
        if list == None:
            self.oLog.info(u'No data for export')
            return True
        oXML = Document()
        rootNode = oXML.createElement(u'export')
        oXML.appendChild(rootNode)

        fileName = self.GetNewFileName(self.sPath)
        for oRecord in list:
            try:
                self.process_record(oRecord, oXML, rootNode)
            except Exception, er:
                self.oLog.error(u'Ошибка %s' % er.message)
                if not self.noException:
                    raise
        self.oLog.info(u'Complete read export data')
        try:
            oFileHandle = open(fileName, 'w+')
            # oXML.writexml(oFileHandle, indent="  ", addindent="  ", newl='\n')
            sXML = oXML.toxml( encoding="utf-8")
            # oXML.writexml(oFileHandle)
            oFileHandle.write(sXML)
            oFileHandle.close()
            self.oLog.info(u'export file %s complete' % (fileName))
        except Exception, er:
            self.oLog.error(u'save file %s' % (fileName))
            if not self.noException:
                raise
        self.set_last_export(nextDate)
        return True


def job(_sINIFile):
    u"""Задача загрузки из 1с"""
    from dpframe.tech import pgdb
    try:
        print _sINIFile
        oINI = Export1C(_sINIFile)
    except Exception, er:
        print u'Error open INI'
        exit(1)
    try:
        print oINI.log
        log = LOG(oINI.log)
    except Exception, er:
        print u'Error open LOG'
        exit(1)
    log.info(u'Инициализация задачи. Загрузка данных из %s' % oINI.path)
    try:
        oDBConectParam = pgdb.INI(_sINIFile).get_dbparam()
        oConnect = pgdb.Connect(oDBConectParam)
    except Exception, er:
        log.error(u'Сбой при подключении к БД. %s' % er.message)
    try:
        if(not os.path.exists(oINI.path)):
            raise Exception(u'Путь %s не найден' % oINI.path)
    except Exception, er:
        log.error(u'Сбой при определении пути. %s ' % unicode(er.message))
    oExporter = Exporter(oINI.path, oConnect, log)
    oExporter.process()

if __name__ == "__main__":
    import sys
    #print 'len(sys.argv)', len(sys.argv)
    #from PyQt4.QtGui import QMessageBox    
    #QMessageBox.warning(self, u"Предупреждение", u"Ошибка определения серии", QMessageBox.Ok)
    #from dpframe.tech.SimpleSound import SimpleSound
    #name = raw_input("What is your name? ")
    #print name
    
    
       
    if (len(sys.argv) != 2):
        # sINIFile = u'~/work/ElectroLab/trunk/electrolab/unittest/integration.ini'
        sINIFile = u'../unittest/integration.ini'
        job(sINIFile)
#        f.write('q')
    if (len(sys.argv) == 2):
        sINIFile = sys.argv[1]
        job(sINIFile)
#        f.write('w')
    else:
        print u'Invalid argument. Example: integration.exe <integration.ini>'
#        f.write('e')
#    f.close()
    