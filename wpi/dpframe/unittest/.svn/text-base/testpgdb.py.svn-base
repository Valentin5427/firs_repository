#-*- coding: UTF-8 -*-
'''
Created on 15.07.2011

@author: Knurov
'''
import unittest
from  dpframe.tech import pgdb
import os

def get_full_path(_sFileName):
    u"""Получить полный путь к файлу. При запуске через агрегатор подставляет путь к папке с юниттестами"""
    if __name__ == "__main__":
        return os.path.join(u'./', _sFileName)
    else:
        return os.path.join(u'./unittest', _sFileName)

class TestPgdb(unittest.TestCase):
    u"""Тест соединения с БД PostgreSQL"""
            
    def testConnected(self):
        u"""Соедениться удалось"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertTrue(oConnect.connected, oConnect.lastError)

    def testGetConnection(self):
        u"""Получение объекта соединения"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertTrue(oConnect.connected, oConnect.lastError)
        self.assertNotEqual(oConnect.connection, None, oConnect.lastError)
        
    def testBadConnected(self):
        u"""Заведомо не корректные параметры соединения"""
        oDBConectParam = pgdb.DBParam(u'NoHost', u'NoDB', u'User', u'NoPass')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertFalse(oConnect.connected, oConnect.lastError)
        
    def test_merge_dbparam(self):
        u"""Выполнение простого sql запроса"""
        oDBParamDst = pgdb.DBParam(None , u'DB', u'User', u'Pass')
        oDBParamSrc = pgdb.DBParam(u'SecondHost', u'SecondHost', u'SecondHost', u'SecondHost')
        oDBParamDst.merge(oDBParamSrc)
        self.assertEqual(oDBParamDst.sHostName, u'SecondHost')
        self.assertEqual(oDBParamDst.sDBName, u'DB')
        self.assertEqual(oDBParamDst.sUser, u'User')
        self.assertEqual(oDBParamDst.sPass, u'Pass')
        
    def test_run_simpleSQL(self):
        u"""Выполнение простого sql запроса"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertTrue(oConnect.run(u'select (10)'))
        
    def test_run_many_simpleSQL(self):
        u"""Выполнение простого sql запроса"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertTrue(oConnect.run(u'select (10); select (10)'))
        
    def test_run_incorrectSQL(self):
        u"""Выполнение простого sql запроса"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertFalse(oConnect.run(u'select asdf from asdfsdafasdfasdfsda'))
        self.assertTrue(len(oConnect.lastError) > 0)
        
    def test_run_get_value(self):
        u"""Получение скалярного значения"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        self.assertEqual(oConnect.get_value(u'select (10)'), 10)

class TestPgdbINI(unittest.TestCase):
    u"""Тест чтения файла настроек соединения с БД PostgreSQL"""
    
    def test_notexist_file(self):
        u"""Обращение к несуществующему файлу"""
        ini = pgdb.INI(get_full_path(u'NotExistsThosFile.ini'))
        self.assertFalse(ini.opened)

    def test_read_param(self):
        u"""Обращение к несуществующему файлу"""
        ini = pgdb.INI(get_full_path(u'db.ini'))
        self.assertTrue(ini.opened)
        parm = ini.get_dbparam()
        self.assertEqual(parm.sDBName, u'postgres')


class TestDBProperty(unittest.TestCase):
    u"""Тест свойств БД PostgreSQL"""
    
    def test_run_get_value(self):
        u"""Получение скалярного значения"""
        oDBConectParam = pgdb.DBParam('LocalHost', 'dpframe', 'dpframe', 'dpframe')
        oConnect = pgdb.Connect(oDBConectParam)
        oDBProperty = pgdb.DBProperty(oConnect, 'DP')
        self.assertTrue(oDBProperty.set_vlaue(u'migrate', 10) )
        self.assertEqual(oDBProperty.get_vlaue(u'migrate'), u'10')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()