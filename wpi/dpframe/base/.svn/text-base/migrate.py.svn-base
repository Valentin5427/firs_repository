#-*- coding: UTF-8 -*-
u''' *********************************************************
Created on 11.07.2011
diposoft(c)
@author: knur
Description: 
********************************************************* '''
import sys
from dpframe.tech.migrate import Scripts 
from dpframe.tech.migrate import Migrate
from dpframe.tech.migrate import INI 
from dpframe.tech import pgdb
from dpframe.base.common import argreader



class MigrateArg(argreader):
    u""" Разбор аргументов и параметров коммандной строки """
    def __init__(self, _argv):
        u"""_argv - список аргументов"""
        self._bCorrect = False
        argreader.__init__(self, _argv)
        
    def Parse(self, _arg):
        """Обработчик входных параметров"""
        argreader.Parse(self, ['INI=', 'Server=', 'Database=', 'User=', 'Password=', 'Path=' ], _arg)
#        argreader.Parse(self, ['INI=', 'Version=', 'Help'], _arg)
        self.sCommandList = ['HELP', 'UP', 'DOWN']
        self.sINIFile = self.GetOptions('--INI') 
        self.sProjectName = self.GetOptions('--Name') 
        self.sServer = self.GetOptions('--Server')
        self.sDatabase = self.GetOptions('--Database')
        self.sUser = self.GetOptions('--User')
        self.sPassword = self.GetOptions('--Password')
        self.sPath = self.GetOptions('--Path')
        self.sCommand = None
        self.iFromVersion = None
        self.iToVersion = None
        self._bCorrect = self.get_command() 
        
    def get_command(self):
        u"""Извлекает из аргументов команду и начальную и конечную версии. Если параметр не корректный вернет False"""
        if(not(0 < len(self.arguments) < 4)):
            return False
        if(self.arguments[0].upper() in self.sCommandList):
            self.sCommand = self.arguments[0]
        else:
            return False
        if(2 == len(self.arguments)):
            self.iToVersion = int(self.arguments[1])
        if(3 == len(self.arguments)):
            self.iFromVersion = int(self.arguments[1])
            self.iToVersion = int(self.arguments[2])
        return True

    @property
    def correct(self):
        u"""Корректность аргументов"""
        return self._bCorrect
    
    def is_command(self, _sCommand):
        u"""Проверка наличия команды _sCommand в аргументах. Не чувствительна к регистру"""
        if(not self._bCorrect):
            return
        return self.sCommand.upper() == _sCommand.upper()

    def Help(self):
        return u"""
Migrate [<Option>] <Command> [<from version>] <to version>
Option
    --INI <ini file>
    --Name <project name>
    --Path <path to scripts>
    --Server <ServerName>
    --Database <DBName>
    --User <UserName>
    --Password <Pass>
Command
    Help|UP|Down
"""

class migrateCLI:
    """ Утилита коммандной строки миграции БД"""
    def __init__(self):
        argv = sys.argv[1:]
        self.oMigrateArg = MigrateArg(argv)
        if(not self.oMigrateArg.IsParsed()):
            self.print_error(u'Не корректные параметры')
            self.print_message(self.oMigrateArg.Help())
            return
        if(not self.oMigrateArg.correct):
            self.print_error(u'Не верная комманда')
            self.print_message(self.oMigrateArg.Help())
            return
        if(self.oMigrateArg.is_command(u'Help')):
            self.print_message(self.oMigrateArg.Help())
            return
        
        #Чтение параметров БД и соединение с ней
        oConectParam = pgdb.DBParam(
                                             self.oMigrateArg.sServer
                                             , self.oMigrateArg.sDatabase  
                                             , self.oMigrateArg.sUser
                                             , self.oMigrateArg.sPassword  
                                             )
        oDBINI = pgdb.INI(self.oMigrateArg.sINIFile)
        if(self.oMigrateArg.sINIFile):
            if(not oDBINI.opened):
                self.print_error(u'Не могу открыть файл %s' % self.oMigrateArg.sINIFile)
                return
            else:
                self.print_message(u'Недостающие параметры будут взяты из %s' % self.oMigrateArg.sINIFile)
            
        #Смотрим путь к папке со скриптами из аргументов или из INI
        oMigrateINI = INI(self.oMigrateArg.sINIFile)
        sPath = self.oMigrateArg.sPath or oMigrateINI.path
        sProjectName = oMigrateINI.name
        if(not sPath):
            self.print_error(u'Не задан путь к скриптам ни в INI ни в аргументах комманды')
            self.print_message(self.oMigrateArg.Help())
            return
        self.print_message(u'Путь к скриптам %s' % sPath)
        
        if(not Scripts().exists_scripts(sPath, self.oMigrateArg.sCommand)):
            self.print_error(u'Нет скриптов "%s" в указанном каталоге "%s"' % (self.oMigrateArg.sCommand, sPath))
            return
        
        oConectParam.merge(oDBINI.get_dbparam())
        if(not oConectParam.isCorrect()):
            self.print_error(u'Не корректные параметры соединения с БД')
            self.print_message(self.oMigrateArg.Help())
            return
        else:
            self.print_message(u'Получены параметры соединения с БД ')
        
        oDBConnect = pgdb.Connect(oConectParam)
        if not(oDBConnect.connected):
            self.print_error(u'Не возможно соединение с БД')
            self.print_error(oDBConnect.lastError)
            return
        else:
            self.print_message(u'Соединение с БД создано')
        
        oDBProperty = pgdb.DBProperty(oDBConnect, sProjectName)
        
        oMigration = Migrate(oDBConnect, sPath, self.error_handler, self.done_handler)
        
        curentVersion = None
        try:
            curentVersion = int(oDBProperty.get_vlaue(u'Version'))
        except:
            pass
            self.print_message(u'Не удалось получить версию БД')
        
        
        if self.oMigrateArg.is_command(u'Up'):
            maxVersion = self.oMigrateArg.iToVersion or Scripts().get_max_up_version(sPath) or 0
            minVersion = self.oMigrateArg.iFromVersion or curentVersion or 0
            if curentVersion and maxVersion <= curentVersion:
                self.print_message(u'БД не требует обновления до версии %d текущая версия %d' % (maxVersion, curentVersion))
                return 
            self.print_message(u'Начало обновления БД с версии %d до %d' % (minVersion, maxVersion))
            oMigration.Up(minVersion + 1, maxVersion)
            oDBProperty.set_vlaue(u'Version', maxVersion)
        
        if self.oMigrateArg.is_command(u'Down'):
            maxVersion = self.oMigrateArg.iToVersion or curentVersion or 0
            minVersion = self.oMigrateArg.iFromVersion or Scripts().get_min_down_version(sPath) or 0
            if 0 == maxVersion or maxVersion < minVersion:
                self.print_message(u'БД не требует откат с версии %d текущая версия %d' % (maxVersion, minVersion))
                return 
            self.print_message(u'Начало отката БД с версии %d до %d' % (maxVersion, minVersion))
            oMigration.Down(maxVersion, minVersion - 1)
            oDBProperty.set_vlaue(u'Version', minVersion)

    def error_handler(self, _sFileName, _sMessage):
        u"""Обработчик ошибок _sFileName - Имя файла в котором обнаружена ошибка , _sMessage - Текст ошибки"""
        self.print_error(u'В файле %s произошла ошибка %s' % (_sFileName, _sMessage))

    def done_handler(self, _sFileName):
        u"""Обработчик процесса выполнения последовательности файлов миграции _sFileName - Имя успешно обработанного файла"""
        self.print_message(u'Файл %s выполнен' % _sFileName)

    def print_error(self, _text):
        u"""Вывод ошибок"""
        #TODO: Сделать вывод через STDError
        print u'Ошибка: ' + _text
        
    def print_message(self, _text):
        u"""Вывод сообщений"""
        print _text
        