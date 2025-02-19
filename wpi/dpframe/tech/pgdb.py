#-*- coding: UTF-8 -*-
'''
Created on 11.07.2011
diposoft(c)
@author: knur
Description: Работа с БД PostgreSQL
'''
import psycopg2
from dpframe.tech import common
class DBParam():
    u""" Структуа данных параметров соединения с БД"""
    def __init__(self, _sHostName = None, _sDBName = None, _sUser = None, _sPass = None):
        self.sHostName = _sHostName
        self.sDBName = _sDBName
        self.sUser = _sUser
        self.sPass = _sPass
    
    def merge(self, _oDBParam):
        u"""Объединение двух структур параметров, _oDBParam имеет более низкий приоритет"""
        self.sHostName = self.sHostName or _oDBParam.sHostName
        self.sDBName = self.sDBName or _oDBParam.sDBName
        self.sUser = self.sUser or _oDBParam.sUser
        self.sPass = self.sPass or _oDBParam.sPass
    
    def isCorrect(self):
        u""" Корректность параметров """
        #TODO:Некрасиво, надо придумать как проверять наличие обязательных параметров скорей всего нужны декораторы
        return None != self.sHostName and None != self.sDBName and None != self.sUser and None != self.sPass   

class INI(common.INI):
    u""" Чтение секци DB из ини файла. заполняет  DBParam """
    #TODO: Отрефакторить в INI Читалки
    
    def __init__(self, _sFileName):
        common.INI.__init__(self, _sFileName, u'DB')
    
    def get_dbparam(self):
        u"""Параметры соединения с БД"""
        if(not self.opened):
            raise Exception(u'Not open file %s', self.config.filename)
        oDBParam = DBParam(
                           self.get_optional_value(self.section, u'Host')
                           , self.get_optional_value(self.section, u'DB')
                           , self.get_optional_value(self.section, u'User')
                           , self.get_optional_value(self.section, u'Pass')
                           )
        return oDBParam 
        
class Connect():
    u"""Соединение с БД"""
    def __init__(self, _oDBConectParam):
        u"""_oDBConectParam Структура параметров соединения с БД dpframe.tech.pgdb.DBParam() """
        self.lastError = u''
        self._connected = False
        self._connect(_oDBConectParam)
        
    @property
    def connected(self):
        u"""Соединение установлено"""
        return self._connected
    
    def _connect(self, _oDBConectParam):
        u"""Установить соединение. Возвращает истину при удачном соединении"""
        self.oDBConectParam = _oDBConectParam  
        try:
            self._oConnection = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" % (_oDBConectParam.sHostName, _oDBConectParam.sDBName, _oDBConectParam.sUser, _oDBConectParam.sPass))
            self._connected = True
            self.lastError = u''
        except Exception as e:
            self._connected = False
            self.lastError = e
        return self._connected

    @property
    def connection(self):
        u"""Соединение psycopg2"""
        return self._oConnection
    
    @property
    def last_error(self):
        u"""Ошибка"""
        return self.lastError
    
    def run(self, _sQuery):
        u"""Выполнить SQL запрос с закрытием транзакции. Возвращает True|False """
        if(not self._connected):
            raise Exception('Not connected')
        if(_sQuery in (None, '')):
            self.lastError = u'Empty SQL query'
            return False
        cur = self._oConnection.cursor()
        try:
            cur.execute(_sQuery)
            self._oConnection.commit()
            self.lastError = u''
        except Exception as e:
            self._oConnection.rollback()
            self.lastError = e
            return False
        return True

    def get_result(self, _sQuery):
        u"""Выполнить SQL запрос с закрытием транзакции. Возвращает курсор """
        if(not self._connected):
            raise Exception('Not connected')
        if(_sQuery in (None, '')):
            self.lastError = u'Empty SQL query'
            return None
        cur = self._oConnection.cursor()
        try:
            cur.execute(_sQuery)
            self._oConnection.commit()
            self.lastError = u''
        except Exception as e:
            self._oConnection.rollback()
            self.lastError = e
            return None
        return cur
    
    def get_value(self, _sQuery):
        cur = self.get_result(_sQuery)
        if cur and cur.rowcount:
            return cur.fetchone()[0]
        else:
            return None
        

class DBProperty():
    u"""Аттрибуты БД"""
    def __init__(self, _oConnect, _sProject):
        u"""_oConnect - соединение с БД dpframe.tech.pgdb.Connect() , _sScriptPath - папка со скриптами миграции, _errorHandler - обработчик ошибок, _doneHandler - обработчик прогресса"""
        self.conection = _oConnect
        self.Project = _sProject
        
    def exists(self, _sName):
        sSQL = "select Value from db_property where Project = '%s' and Name = '%s';" % (self.Project, _sName)
        return self.conection.get_value(sSQL) != None

    def set_vlaue(self, _sName, _sValue):
        u"""Установить аттрибут БД"""
        if self.exists(_sName):
            sSQL = "update db_property set Project = '%s', Name = '%s', Value = '%s';" % (self.Project, _sName, _sValue)
        else:
            sSQL = "insert into db_property (Project, Name, Value) values('%s', '%s', '%s');" % (self.Project, _sName, _sValue)
        return self.conection.run(sSQL)

    def get_vlaue(self, _sName):
        u"""Установить аттрибут БД"""
        sSQL = "select Value from db_property where Project = '%s' and Name = '%s';" % (self.Project, _sName)
        return self.conection.get_value(sSQL)
