#-*- coding: UTF-8 -*-
u'''
Created on 24.07.2011
@author: knur
ticket #4
Интеграция с 1С
1. Разбор INI
2. Отслеживание состояния папки, чтение и удаление файлов.
3. Запись в лог
'''
from dpframe.tech import common
import re
import os
import stat
import logging
from sys import stdout

class INI(common.INI):
    u""" Чтение секци integration из INI файла."""

    def __init__(self, _sFileName):
        common.INI.__init__(self, _sFileName, u'Integration')

    @property
    def path(self):
        u"""Путь к папке """
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Path')

    @property
    def arch(self):
        u""""""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Arch')

    @property
    def log(self):
        u""""""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Log')


class Import1C(common.INI):
    u""" Чтение секци integration из INI файла."""

    def __init__(self, _sFileName):
        common.INI.__init__(self, _sFileName, u'Import')

    @property
    def path(self):
        u"""Путь к папке """
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Path')

    @property
    def arch(self):
        u""""""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Arch')

    @property
    def log(self):
        u""""""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Log')



class Export1C(common.INI):
    u""" Чтение секци integration из INI файла."""

    def __init__(self, _sFileName):
        common.INI.__init__(self, _sFileName, u'Export')

    @property
    def path(self):
        u"""Путь к папке """
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Path')

    @property
    def log(self):
        u""""""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Log')


class LOG():
    u"""Запись в лог"""

    def __init__(self, _sFullFileName = None):
        self.log = logging
        DATE_FORMAT = u'%Y-%m-%d %H:%M:%S'
#        MSG_FORMAT = u'%(asctime)s -%(module)s- *%(levelname)s* %(message)s'
        MSG_FORMAT = u'%(asctime)s: *%(levelname)s* %(message)s'
        MSG_LEVEL = logging.DEBUG

        logging.basicConfig(format=MSG_FORMAT, datefmt=DATE_FORMAT)
        self.log = logging.getLogger(u'electrolab')
#        if _sFullFileName:
        if(_sFullFileName):
            hdlr = logging.FileHandler(_sFullFileName)
        else:
            hdlr = logging.StreamHandler(stdout)
        formatter = logging.Formatter(MSG_FORMAT, DATE_FORMAT)
        hdlr.setFormatter(formatter)
        self.log.addHandler(hdlr)
        self.log.setLevel(MSG_LEVEL)
    
    def error(self, _message):
        u"""Записать в лог ошибку"""
        self.log.error(_message)
#        print _message

    def warning(self, _message):
        u"""Записать в лог предупреждение"""
        self.log.warning(_message)
#        print _message
    
    def info(self, _message):
        u"""Записать в лог информационное сообщение"""
        self.log.info(_message)
#        print _message
     
class ExchangeFile():
    u"""Класс обёртка над файлом"""
    
    def __init__(self, _sPath, _sFileName, _sArchPath = None):
        u"""_sPath - Путь к файлу, _sFileName - имя файла скрипта миграции"""
        self.sPattern = u'data\d+.\d+.\d+ \d+_\d+_\d+\.XML'
        self.sPath = _sPath
        self.sFileName = _sFileName
        self.sArchPath = _sArchPath
#        data01.11.2011 12_56_39.xml
        self._date = self._extract_date(_sFileName)
        
        if(None != _sPath and None != _sFileName):
            self._isCorrect = self._parse(_sPath, _sFileName, self.sPattern)\
                and self._exists(_sPath, _sFileName)\
                and self._not_emty(_sPath, _sFileName)
#                and self._correct_flag(_sPath, _sFileName)
        else:
            self._isCorrect = False
        
    def _parse(self, _sPath, _sFileName, _sPattern):
        u"""Разбор имени файла, проверка корректности имени и флаги"""
        self.pattern = re.compile(_sPattern, re.IGNORECASE)
        if(not re.match(self.pattern, _sFileName)):
            return False
        return True

    def _extract_date(self, _sFileName):
        u"""Разбор имени файла, проверка корректности имени и флаги"""
        self.pattern = re.compile(u'data(\d+.\d+.\d+) ', re.IGNORECASE)
        result = re.match(self.pattern, _sFileName)
        if(result and len(result.groups())):
            return result.groups()[0][-2:]
        else:
            return None

    def _exists(self, _sPath, _sFileName):
        u"""Файл существует"""
        return os.path.exists(os.path.join(_sPath, _sFileName))
        
#    def _correct_flag(self, _sPath, _sFileName):
#        u"""Флаг корректный"""
#        return 0 != os.stat(os.path.join(_sPath, _sFileName)).st_mode & stat.S_IWRITE
        
    def _not_emty(self, _sPath, _sFileName):
        u"""Флаг корректный"""
        return 0 != os.stat(os.path.join(_sPath, _sFileName)).st_size
        
    def delete(self):
        u"""Удалить файл, если есть архивная папка - перенести"""
        if self.sArchPath and not os.path.exists(os.path.join(self.sArchPath, self.sFileName)):
            os.rename(os.path.join(self.sPath, self.sFileName), os.path.join(self.sArchPath, self.sFileName))
        else:
            os.remove(os.path.join(self.sPath, self.sFileName))
        
    def get_yar(self):
        return self._date
        
    @property
    def correct(self):
        u"""Корректное имя файла. Содержит в имени допустимую команду, версию и правильное расширение"""
        return self._isCorrect

    @property
    def file(self):
        u"""Содержимое файла"""
        if not self._isCorrect:
            raise Exception(u'File %s not for excahnge' % self.sFileName)
        return open(os.path.join(self.sPath, self.sFileName))

class FileSystem():
    u"""Управление содержимым папки обмена"""

    def get_filelist(self, _sPath, _sArchPath = None):
        u"""Получить список файлов ExchangeFile() _sPath - папка с файлами обмена, не рекурсивный проход"""
        if None == _sPath:
            raise Exception(u'Not set _sPath')
        lst = []
        for root, dirs, files in os.walk(_sPath):
            if _sPath != root:
                break
            for file in files:
                if ExchangeFile(root, file).correct:
                    lst.append(ExchangeFile(root, file, _sArchPath))
        return lst
    