#-*- coding: UTF-8 -*-
'''
Created on 12.07.2011

@author: knur
'''
import unittest
from dpframe.base.migrate import MigrateArg
from dpframe.tech.migrate import Scripts
from dpframe.tech.migrate import MigrateScript
from dpframe.base.migrate import Migrate
from dpframe.tech.migrate import INI
import os

def get_full_path(_sFileName):
    u"""Получить полный путь к файлу. При запуске через агрегатор подставляет путь к папке с юниттестами"""
    if __name__ == "__main__":
        return os.path.join(u'./', _sFileName)
    else:
        return os.path.join(u'./unittest', _sFileName)

from os import path
global fixturePath

def get_path(_sFileName):
    u"""Получить актуальный путь"""
    return path.join(fixturePath, _sFileName)

class TestMigrateArg(unittest.TestCase):
    u"""Разборка аргументов MigrateArg"""
    def testExistCommand(self):
        u"""Получить команду из строки аргументов"""
        arg = 'Help'.split()
        oArgv = MigrateArg(arg)
        self.assertEqual(oArgv.sCommand, 'Help')

    def testGetOptions(self):
        u"""Получить опцию"""
        arg = '--INI testmigrate.ini'.split()
        oArgv = MigrateArg(arg)
        self.assertEqual(oArgv.GetOptions('--INI'), 'testmigrate.ini')

    def testINIProp(self):
        u"""Прочитать свойство INI"""
        arg = '--INI testmigrate.ini'.split()
        oArgv = MigrateArg(arg)
        self.assertEqual(oArgv.sINIFile, 'testmigrate.ini')

    def testUnknowParam(self):
        u"""Некорректные параметры"""
        arg = '--UnknowText --UnknowParam  --UnknowParam1 samevalue1 --INI testmigrate.ini --UnknowParam2 samevalue2'.split()
        oArgv = MigrateArg(arg)
        self.assertFalse(oArgv.IsParsed())

    def testToVersion(self):
        u"""Прочитать начальную версию"""
        arg = 'Up 10'.split()
        oArgv = MigrateArg(arg)
        self.assertEqual(oArgv.iToVersion, 10)

    def testFromVersion(self):
        u"""Прочитать начальную версию при наличии конечной"""
        arg = 'Up 10 20'.split()
        oArgv = MigrateArg(arg)
        self.assertEqual(oArgv.iFromVersion, 10)

    def testUnknowCommand(self):
        u"""Неизвестная комманда"""
        arg = 'SUp 10 20'.split()
        oArgv = MigrateArg(arg)
        self.assertFalse(oArgv.correct)

    def testKnowCommand(self):
        u"""Известная комманда"""
        arg = 'Help'.split()
        oArgv = MigrateArg(arg)
        self.assertTrue(oArgv.correct)
        
    def test_correct_parms(self):
        u"""Известная комманда"""
        arg = '--Path dpframe\unittest\migrate --Server localhost --Database dpframe --User dpframe --Password dpframe up 1 1'.split()
        oArgv = MigrateArg(arg)
        self.assertTrue(oArgv.correct)

class TestScripts(unittest.TestCase):

    def test_get_list(self):
        oScripts = Scripts()
        list = oScripts._get_list(get_full_path('migrate'), 'Up'.upper())
        self.assertTrue(len(list) == 3)

    def test_get_up_list(self):
        oScripts = Scripts()
        list = oScripts.get_up_list(get_full_path('migrate'), 1, 2)
        self.assertTrue(list[0].version == 1)
        self.assertTrue(list[1].version == 2)
        
#    def test_get_down_list(self):
#        oScripts = Scripts()
#        list = oScripts.get_down_list('./migrate', 2, 1)
#        self.assertTrue(list[0].version > list[1].version)

    def test_not_exist_script(self):
        self.assertFalse(Scripts().exists_scripts(get_full_path(u'UnknowPath'), u'up') )

class TestMigrateScript(unittest.TestCase):
    
    def test_is_correct(self):
        u"""Корректное имя файла"""
        oScripts = MigrateScript(get_full_path(u'migrate'), u'up_1.sql')
        self.assertTrue(oScripts.correct)
        
    def test_is_incorrect(self):
        u"""Некорректное имя"""
        oScripts = MigrateScript(get_full_path(u'migrate'), u'upd_1.sql')
        self.assertFalse(oScripts.correct)
        oScripts = MigrateScript(get_full_path(u'migrate'), u'up_1a.sql')
        self.assertFalse(oScripts.correct)
        
    def test_command(self):
        oScripts = MigrateScript(get_full_path(u'migrate'), u'up_1.sql')
        self.assertEqual(oScripts.command, u'Up'.upper())
        
    def test_text(self):
        oScripts = MigrateScript(get_full_path(u'migrate'), u'up_1.sql')
        self.assertTrue(oScripts.correct, u'Не удалось получить список')
        self.assertNotEqual(oScripts.text, None)

class TestMigrate(unittest.TestCase):
    
    def setUp(self):
        from dpframe.tech import pgdb
        oDBConectParam = pgdb.DBParam('LocalHost', 'postgres', 'dpframe', 'dpframe')
        self.oConnect = pgdb.Connect(oDBConectParam)
        self.countError = 0
        
    def test_up(self):
        oMigrate = Migrate(self.oConnect, u'migrate')
        self.assertTrue(oMigrate.Up(1,1))

    def test_up_callback(self):
        def done(_message):
            self.assertTrue(None != _message)
            
        def error(_fileName, _message):
            self.assertTrue(None != _message)

        oMigrate = Migrate(self.oConnect, get_full_path(u'migrate'), error, done)
        self.assertTrue(oMigrate.Up(1,3))

    def test_up_callback_with_continue(self):
        self.countError = 0
        def done(_message):
            self.assertTrue(None != _message)
            
        def error(_fileName, _message):
            self.assertTrue(None != _message)
            self.countError += 1
            return True

        oMigrate = Migrate(self.oConnect, get_full_path(u'migrate'), error, done)
        self.assertTrue(oMigrate.Up(1,3))
        self.assertTrue(2 == self.countError)

class TestMigrateINI():
    u"""Чтение конфигурационного файла"""

    def test_notexist_file(self):
        u"""Обращение к несуществующему файлу"""
        oINI = INI(u'NotExistsThosFile.oINI')
        self.assertFalse(oINI.opened)

    def test_read_param(self):
        u"""Обращение к несуществующему файлу"""
        oINI = INI(get_path(u'Migrate.INI'))
        self.assertTrue(oINI.opened)
        parm = oINI.path()
        self.assertEqual(parm.sPath, u'./path/to/migrate/scripts')
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    fixturePath = u'./'
    unittest.main()
else:
    fixturePath = u'./unittest/'
    