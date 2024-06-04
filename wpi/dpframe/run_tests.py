#!/usr/bin/env python
#coding=utf-8

u'''Модуль агрегирования и запуска юниттестов'''

import os
import unittest
import doctest

class TestAggregator(object):
    u'''Агрегатор юниттестов. Поддерживает тесты unittest и doctest.
    
    Использование:
    
    aggr = TestAggregator()
    aggr.aggregate()
    aggr.run()
    
    или
    
    TestAggregator().run()
    
    '''
    
    @staticmethod
    def _visit(self, dirname, names):
        os.sys.path.append(os.path.abspath(dirname))
        for module in [__import__(os.path.splitext(name)[0]) for name in names if name.endswith(u'.py')]:
            test = self._loader.loadTestsFromModule(module)
            if test.countTestCases() > 0:
                self._suite.addTest(test)
            try:
                self._suite.addTest(doctest.DocTestSuite(module))
            except ValueError:
                pass

    def __init__(self):
        self._suite = None
        self._loader = unittest.TestLoader()
        
    def aggregate(self, path=None):
        u'''Собрать все тесты.
        
        Параметры:
        path -- корневой путь для сборки тестов, текущая директория по-умолчанию.
        
        '''
        self._suite = unittest.TestSuite()
        path = os.path.abspath(path or os.curdir)
        os.path.walk(path, self._visit, self)
        
    def run(self, force=False):
        u'''Запустить собранные тесты.
        
        Параметры:
        force -- признак принудительной сборки тестов перед запуском, False по-умолчанию.
        
        '''
        if not self._suite or force:
            self.aggregate()
        unittest.TextTestRunner(verbosity=2).run(self._suite)
        

if __name__ == u'__main__':
    aggr = TestAggregator()
    aggr.aggregate(u'unittest')
    aggr.run()