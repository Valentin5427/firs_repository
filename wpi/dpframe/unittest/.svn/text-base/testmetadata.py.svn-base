#-*- coding: UTF-8 -*-
u"""
Created on 16.08.2011
#
@author: knur
"""

import unittest
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4 import QtGui
from dpframe.data import metadata
import sys
from uuid import uuid1

class Test(unittest.TestCase):
    u"""Тест чтения метаданных"""
    app = QtGui.QApplication(sys.argv)

    def setUp(self):
        self.dbname = uuid1().hex
        
        self.db = QSqlDatabase.database() if QSqlDatabase.database().isValid() else QSqlDatabase.addDatabase(u'QPSQL')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("postgres")
        self.db.setUserName("dpframe")
        self.db.setPassword("dpframe")
        self.assertTrue(self.db.open(), u'Не удалось подключится к БД postgress')
        
        q = QSqlQuery(self.db)
        q.exec_(u'CREATE DATABASE "{0}" WITH OWNER = dpframe ENCODING = \'UTF8\';'.format(self.dbname))
        del q
        name = self.db.connectionName()
        self.db.close() 
        del self.db
        QSqlDatabase.removeDatabase(name)
        
        self.db = QSqlDatabase.database() if QSqlDatabase.database().isValid() else QSqlDatabase.addDatabase(u'QPSQL')
        self.db.setHostName("localhost")
        self.db.setDatabaseName(self.dbname)
        self.db.setUserName("dpframe")
        self.db.setPassword("dpframe")
        self.assertTrue(self.db.open(), u'Не удалось подключится к БД {0}'.format(self.dbname))
        
        with open(u'./unittest/fixtures/metadata/create_app_struct.sql') as fp:
            q = QSqlQuery(self.db)
            q.exec_(fp.read())

        with open(u'./unittest/fixtures/metadata/create_metadata_struct.sql') as fp:
            q = QSqlQuery(self.db)
            q.exec_(fp.read())
            
        with open(u'./unittest/fixtures/metadata/fill_metadata.sql') as fp:
            q = QSqlQuery(self.db)
            q.exec_(fp.read())
            

    def tearDown(self):       
        self.db.close() 
        name = self.db.connectionName()
        del self.db
        QSqlDatabase.removeDatabase(name)
        
        self.db = QSqlDatabase.database() if QSqlDatabase.database().isValid() else QSqlDatabase.addDatabase(u'QPSQL')
        self.db.setHostName("localhost")
        self.db.setDatabaseName("postgres")
        self.db.setUserName("dpframe")
        self.db.setPassword("dpframe")
        self.assertTrue(self.db.open(), u'Не удалось подключится к БД postgress')

        QSqlQuery(u'DROP DATABASE "{0}";'.format(self.dbname))

        self.db.close() 
        name = self.db.connectionName()
        del self.db
        QSqlDatabase.removeDatabase(name)

    def test_table(self):
        u"""Получить коллекцию метаданных таблиц"""
        oMetaData = metadata.MetaData(self.db)
        tableName = u'meta_field'
        table = oMetaData.load()[tableName]
        self.assertEqual(table.tableName, tableName, u'Не найдены метаданные таблицы')

    def test_fields(self):
        u"""Чтение коллекции метаданных полей"""
        oMetaData = metadata.MetaData(self.db)
        table = oMetaData.load().meta_field
        self.assertEqual(table.fields.meta_table.name , u'meta_table')
        self.assertEqual(table.fields.meta_table.length , 100)
        self.assertSetEqual(set([fld.cid for fld in table.fields.itervalues()]), set(xrange(0, table.fields.__len__())))

    def test_fkey(self):
        u"""Чтение коллекции метаданных внешних ключей"""
        oMetaData = metadata.MetaData(self.db)
        table = oMetaData.load().meta_field
        self.assertEqual(table.fkeys.meta_table.refTable , u'meta_table')
        self.assertEqual(table.fkeys.meta_table.refField , u'tablename')
        
    def test_table_prop(self):
        u""" """
        oMetaData = metadata.MetaData(self.db)
        table = oMetaData.load().meta_field
        self.assertTrue(not table.createModel)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    