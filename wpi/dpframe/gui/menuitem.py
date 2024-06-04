#!/usr/bin/env python
#coding=utf-8

from PyQt5.QtCore import QObject
from dpframe.tech.AttrDict import AttrDict

def menuSlot(slot):
    u'''
    Декоратор для слота пункта меню.
    Добавляет в параметры слота пункт меню (QAction), вызвавший обработчик, ссылку на главное окно и статические параметры.

    '''

    def wrapper(self, checked):
        action =  QObject().sender()
        slot(self, checked, action, self.window, self.params[action], self.window.env)
    return wrapper

def ellipsisSlot(slot):
    u'''
    Декоратор для слота эллипсиса.
    Добавляет в параметры слота целевой виджет, имя поднимаемого справочника.

    '''
    def wrapper(self, refname):
        slot(self, QObject().sender().comboBox, refname)
    return wrapper

class BaseSlotHolder(object):
    u'''
    Базовый класс хранилища слотов.
    Слоты, определяемые в дочерних классах должны иметь вид:

        @menuSlot
        def search(self, checked, action, window, params, env):
            pass

        Параметры:
        checked - признак отмеченного пункта меню;
        action - пункт меню (QAction), испустивший сигнал;
        window - ссылка на главное окно;
        params - словарь статических параметров из словаря описания меню;
        env - объект окружения

    Пример использования класса - dpframe.examples.gui.mainwnd.slots

    Хранилища слотов (и другие динамически загружаемые объекты) не должны
    находиться в одном модуле с классами, декорированными инитами,
    т.к. динамическая загрузка модуля приводит к его перекомпиляции,
    повторному выполнению инитов-декораторов и может привести к нежелательным последствиям.
    '''

    def __init__(self, window):
        self.window = window
        self.params = {}

    def addParams(self, action, params):
        self.params[action] = AttrDict.toAttrDict(params)


