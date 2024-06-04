#-*- coding: UTF-8 -*-
'''
Created on 11.07.2011
diposoft(c)
@author: knur
Description: 
'''
import os
from dpframe.tech import common

class MigrateScript():
    u"""Атрибуты скрипта миграции <Команда>_<версия>.sql"""
    def __init__(self, _sPath, _sFileName):
        u"""_sPath - Путь к файлу, _sFileName - имя файла скрипта миграции"""
        self.commands = ['UP', 'DOWN']
        self._sVersion = None
        self._sCommand = None
        self.sPath = _sPath
        self.sFileName = _sFileName
        if(None != _sPath and None != _sFileName):
            self._isCorrect = self._parse(_sFileName)
        else:
            self._isCorrect = False
        
    def _parse(self, _sFileName):
        u"""Разбор имени файла, извлекает закодированные в имени аттрибуты скрипта"""
        spliptName = _sFileName.split('_')
        if not (len(spliptName) == 2 and spliptName[0].upper() in  self.commands):
            return False
        self._sCommand = spliptName[0].upper()
        spliptName = spliptName[1].split('.')
        if (not (
                 len(spliptName) 
                 and spliptName[0].isdigit() 
                 and u'sql'.upper() == spliptName[len(spliptName) - 1].upper()
                 )
                 ):
            return False
        self._sVersion = int(spliptName[0])
        return True
        
    @property
    def correct(self):
        u"""Корректное имя файла. Содержит в имени допустимую команду, версию и правильное расширение"""
        return self._isCorrect

    @property
    def version(self):
        u"""Версия"""
        if (self._isCorrect):
            return self._sVersion
        else:
            raise Exception(u'Can`t get version from file name %s' % self.sFileName)

    @property
    def command(self):
        u"""Команда"""
        if (self._isCorrect):
            return self._sCommand
        else:
            raise Exception(u'Can`t get command from file name %s' % self.sFileName)
        
    @property
    def text(self):
        u"""Текст SQL запроса"""
        if (not self._isCorrect):
            raise Exception(u'File %s not migrate script' % self.sFileName)
        oFile = open(os.path.join(self.sPath, self.sFileName), 'r')
        text = oFile.read()
        oFile.close()
        return text

class Scripts():
    u"""Управление скриптами миграции"""
    
    def _get_list(self, _sRootPath, _sPrefix):
        u"""Получить список MigrateScript() _sRootPath - папка со скриптами миграции, _sPrefix - имя команды по которой производится заполнение"""
        if(None in (_sRootPath, _sPrefix)):
            raise Exception(u'Not set param')
        list = []
        for root, dirs, files in os.walk(_sRootPath):
            for file in files:
                item = MigrateScript(root, file)
                if(item.correct and item.command == _sPrefix):
                    list.append(MigrateScript(root, file))
        return list
    
    def get_up_list(self, _sRootPath, _iStartVersion, _iEndVersion):
        u"""Получить список MigrateScript для обновления БД _sRootPath - папка со скриптами миграции, _iStartVersion - начальная версия, _iEndVersion - конечная версия"""
        list = self._get_list(_sRootPath, 'UP'.upper())
        list.sort(key = lambda x: x.version)
        return [item for item in list if item.version >= _iStartVersion and item.version <= _iEndVersion]  
        
    def get_down_list(self, _sRootPath, _iStartVersion, _iEndVersion):
        u"""Получить список MigrateScript для отката БД _sRootPath - папка со скриптами миграции, _iStartVersion - начальная версия, _iEndVersion - конечная версия"""
        list = self._get_list(_sRootPath, 'Down'.upper())
        list.sort(key = lambda x: x.version * -1)
        return [item for item in list if item.version <= int(_iStartVersion) and item.version >= int(_iEndVersion)]  

    def exists_scripts(self, _sRootPath, _sCommand):
        u"""Есть скрипты обновления _sRootPath - Путь к скриптам, _sCommand - Команда Up|Down """
        return len(self._get_list(_sRootPath, _sCommand.upper())) > 0
    
    def get_max_up_version(self, _sRootPath):
        u"""Максимальная версия"""
        list = self._get_list(_sRootPath, 'UP'.upper())
        list.sort(key = lambda x: x.version * -1)
        return list[0].version

    def get_min_up_version(self, _sRootPath):
        u"""Максимальная версия"""
        list = self._get_list(_sRootPath, 'UP'.upper())
        list.sort(key = lambda x: x.version)
        return list[0].version

    def get_max_down_version(self, _sRootPath):
        u"""Максимальная версия"""
        list = self._get_list(_sRootPath, 'DOWN'.upper())
        list.sort(key = lambda x: x.version * -1)
        return list[0].version

    def get_min_down_version(self, _sRootPath):
        u"""Максимальная версия"""
        list = self._get_list(_sRootPath, 'DOWN'.upper())
        list.sort(key = lambda x: x.version)
        return list[0].version


class Migrate():
    u"""Миграция БД"""
    def __init__(self, _oConnect, _sScriptPath, _error_handler = None, _done_handler = None):
        u"""_oConnect - соединение с БД dpframe.tech.pgdb.Connect() , _sScriptPath - папка со скриптами миграции, _errorHandler - обработчик ошибок, _doneHandler - обработчик прогресса"""
        self.conection = _oConnect
        self.oScripts = Scripts()
        self.sScriptPath = _sScriptPath
        # Цепляем CallBakc либо внутренний либо внешний
        self.done_handler = _done_handler or self._build_done_handler 
        self.error_handler = _error_handler or self._build_error_handler
        self._done = True 
        
    def Up(self, _fromVersion, _toVersion):
        u"""Обновить БД _fromVersion - начальная версия, _toVersion - конечная версия"""
        self._done = True 
        scriptList = self.oScripts.get_up_list(self.sScriptPath, _fromVersion, _toVersion)
        for oItem in scriptList: 
            if(not self.conection.run(oItem.text)):
                self.error_handler(oItem.sFileName , self.conection.lastError)
            else:
                self.done_handler(oItem.sFileName)
        return True
    
    def Down(self, _fromVersion, _toVersion):
        u"""Откатить БД _fromVersion - начальная версия, _toVersion - конечная версия"""
        self._done = True 
        scriptList = self.oScripts.get_down_list(self.sScriptPath, _fromVersion, _toVersion)
        for oItem in scriptList: 
            if(not self.conection.run(oItem.text)):
                if(not self.error_handler(oItem.sFileName , self.conection.lastError)):
                    break
            else:
                self.done_handler(oItem.sFileName)
        return True
    
    def _build_error_handler(self, _fileName,  _message):
        u"""Обработчик ошибок по умолчанию"""
        sMessage = u'In file %s ERROR: %s' % (_fileName , _message)
        raise Exception(sMessage)
     
    def _build_done_handler(self, _fileName):
        u"""Обработчик выполнения по умолчанию"""
        return True

class INI(common.INI):
    u""" Чтение секци Migrate из INI файла."""
    #TODO: Отрефакторить в INI Читалки
    def __init__(self, _sFileName, _sProjectName = u'Migrate'):
        common.INI.__init__(self, _sFileName, _sProjectName)
    
    @property
    def path(self):
        u"""Путь к папке скриптов миграции"""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Path')

    @property
    def name(self):
        u"""Имя проекта"""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Name')

    @property
    def parent(self):
        u"""Имя проекта"""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        return self.get_optional_value(self.section, u'Parent')

