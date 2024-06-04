#!/usr/bin/env python
#coding=utf-8

from abc import ABCMeta, abstractmethod
import json
from collections import OrderedDict
import validictory
from dpframe.tech.json import schema

class MenuLoader(object):
    u'''
    Абстрактный базовый класс загрузчика меню из разных форматов.

    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self):
        u'''
        Абстрактный метод загрузки меню.
        Возвращает словарь описания меню, соответствующий схеме dpframe.tech.json.schema.MENU

        '''

    def verify(self):
        u'''
        Проверить словарь на соответствие схеме dpframe.tech.json.schema.MENU
        В случае несоответствия выбрасывается исключение

        '''

        validictory.validate(self.menu, schema.MENU)


class JSONMenuLoader(MenuLoader):
    u'''
    Загрузчик меню из JSON-файла.
    Структура файла должна соответствовать схеме dpframe.tech.json.schema.MENU

    '''

    def __init__(self, fname):
        u'''
        Конструктор загрузчика.

        fname - имя JSON-файла со структурой меню.

        '''

        self.fname = fname


    def load(self):
        u'''
        Загрузить меню.
        Возвращает словарь описания меню, соответствующий схеме dpframe.tech.json.schema.MENU
        В случае несоответствия выбрасывается исключение.

        '''

        with open(self.fname) as fp:
            self.menu = json.load(fp, object_pairs_hook=OrderedDict)
        self.verify()
        return self.menu
