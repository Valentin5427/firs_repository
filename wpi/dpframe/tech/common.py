#-*- coding: UTF-8 -*-
'''
Created on 26.07.2011
@author: Knurov
'''
from configparser import ConfigParser

class INI():
    u""" Чтение секции из INI файла."""
    def __init__(self, _sFileName, _sSection):
        u"""_sFileName - имя INI файла. _sSection - Имя секции"""
        self.section = _sSection
        self.config = ConfigParser()
        self.config.filename = _sFileName
        self._bOpenFile = 0 < len(self.config.read(self.config.filename))
    
    @property
    def opened(self):
        u"""INI файл открыт"""
        return self._bOpenFile 

    def get_optional_value(self, _sSection, _sName):
        u"""Получить необязательное значение из секции _sSection - Имя секции , _sName - Имя параметра"""
        if(self.config.has_option(_sSection, _sName)):
            return self.config.get(_sSection, _sName)
        else:
            return None

