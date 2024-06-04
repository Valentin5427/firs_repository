#!/usr/bin/env python
#coding=utf-8

import sys, re

class ISingleInstance(object):
    u"""Кроссплатформенный интерфейс для класса обеспечения единственного экземпляра приложения"""
    
    def __init__(self):
        self.issingle = True

if u'win32' == sys.platform:
    from win32event import CreateMutex
    from win32api import GetLastError, CloseHandle
    from winerror import ERROR_ALREADY_EXISTS
    
    class SingleInstance(ISingleInstance):
        u"""Класс обеспечения единственного экземпляра приложения (Windows).
        Экземпляр класса должен создаваться при запуске приложения и
        разрушаться при его закрытии.

        """
    
        def __init__(self, unique_name):
            u"""Создать глобальный именованный мьютекс, если не существует."""
            ISingleInstance.__init__(self)
            unique_name = re.sub(ur'[^\w]+', u'_', unique_name)
            self._mutexname = u'appmutex_{0}'.format(unique_name)
            self._mutex = CreateMutex(None, False, self._mutexname)
            self.issingle = GetLastError() != ERROR_ALREADY_EXISTS
        
           
        def __del__(self):
            u"""Удалить глобальный именованный мьютекс, если создан."""
            if self._mutex:
                CloseHandle(self._mutex)
else:
    class SingleInstance(ISingleInstance):
        u"""Класс обеспечения единственного экземпляра приложения (Linux).
        Экземпляр класса должен создаваться при запуске приложения и
        разрушаться при его закрытии.
        Не реализован.

        """
