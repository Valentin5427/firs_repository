#coding=utf-8
'''
ticket: #
Created on 13.07.2011
DipoSoft 2011
Description: 
'''
from getopt import getopt

class argreader():
    u""" Разбор аргументов и параметров коммандной строки """
    def __init__(self, _argv):
        self._bParsed = False
        self.Parse(_argv)
        
    def IsParsed(self):
        u"""Успешность разбора коммандной строки"""
        return self._bParsed
    
    def GetOptions(self, _sName):
        u"""Получить значении опции"""
        for name, value in self.options:
            if(name.upper()  == _sName.upper()):
                return value
                break
            
    def ExistCommand(self, _sName):
        u"""Наличие команды"""
        for name, value in self.options:
            if(name.upper()  == _sName.upper()):
                return True
                break
            return False

    def Parse(self, _command, _argv):
        self.options = []
        self.arguments = []
        try:
            self.options, self.arguments = getopt(_argv, None, _command)
            self._bParsed = True
        except:
            self._bParsed = False
        return self._bParsed
