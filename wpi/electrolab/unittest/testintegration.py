#-*- coding: UTF-8 -*-
u"""
Created on 26.07.2011

@author: Knurov
"""
import unittest
from electrolab.tech.integration import INI
from electrolab.tech.integration import ExchangeFile
from electrolab.tech.integration import FileSystem
from electrolab.tech.integration import LOG
from electrolab.app.integration import Loader

class TestINI(unittest.TestCase):
    u"""Проверка работы с INI"""
    
    def test_path(self):
        u"""Получить путь к папке обмена"""
        self.assertEqual(INI(u'integration.ini').path, u'integration')

class TestExchangeFile(unittest.TestCase):
    u"""Проверка обертки над файлами обмена"""

    def test_correct_file(self):
        u"""Корректное имя, файл существует"""
        oExFile = ExchangeFile(u'integration', u'data01.11.2011 12_56_39.xml')
        self.assertTrue(oExFile.correct)

#    def test_not_correct_filename(self):
#        u"""Не корректное имя"""
#        oExFile = ExchangeFile(u'integration', u'ware_1.txt')
#        self.assertFalse(oExFile.correct)
    
    def test_not_exist_file(self):
        u"""Корректное имя, файл не существует"""
        oExFile = ExchangeFile(u'integration', u'NotExistCorrect.xml')
        self.assertFalse(oExFile.correct)

    def test_read_file(self):
        u"""Чтение файла"""
        oExFile = ExchangeFile(u'integration', u'data01.11.2011 12_56_39.xml')
        self.assertNotEqual(oExFile.file, None)

#    def test_read_emty_file(self):
#        u"""Корректное имя, файл существует, флаг установлен"""
#        oExFile = ExchangeFile(u'integration', u'ware_emty.xml')
#        self.assertTrue(oExFile. )

class TestFileSystem(unittest.TestCase):
    u"""Проверка работы с INI"""
    
    def test_path(self):
        u"""Получить список файлов"""
        self.assertEqual(len(FileSystem().get_filelist(u'integration')), 1)
        
class TestLoader(unittest.TestCase):
    u"""Проверка работы Загрузки"""

    def setUp(self):
        from dpframe.tech import pgdb
        oDBConectParam = pgdb.DBParam('LocalHost', 'electrolab', 'electrolab', 'electrolab')
        self.oConnect = pgdb.Connect(oDBConectParam)
        self.fileCollection = FileSystem().get_filelist(u'integration')
        self.log = LOG(u'c:/integration.log')
    
    def test_process(self):
        u"""Загрузить пробный файл"""
        oLoade = Loader(self.oConnect, self.log)
        self.assertTrue(oLoade.process(self.fileCollection))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()