#!/usr/bin/env python
#coding=utf-8

from PyQt4.uic import loadUiType

class CWidgetFactory(object):
    u'''
    Абстрактная фабрика классов виджетов PyQt
    
    '''

    @classmethod
    def create(cls, fileName, slotHandleClasses=None):
        u'''
        Создает класс виджета PyQt.
        
        fileName - имя файла ресурса ui
        slotHandleClasses - итератор, возвращающий базовые классы, реализующие прикладную логику виджета.
        
        Порядок разрешения методов (MRO) создаваемого класса - прикладные базовые классы,
        в порядке выдачи итератором slotHandleClasses, базовый класс виджета Qt.
        
        Такой MRO обеспечивает возможность переопределения виртуальных методов объектов Qt.
        
        '''
        uiClass, qtBaseClass = loadUiType(fileName)
        base_classes = (tuple(slotHandleClasses) or ()) + (qtBaseClass,)
        return type(str(fileName), base_classes, {u'uiClass':uiClass,
                                                  u'__init__':cls.__constructor,
                                                  u'slotHandleClasses':slotHandleClasses})

    @staticmethod
    def __constructor(self, parent=None, *args, **kwargs):
        u'''
        Конструктор класса виджета.
        Обеспечивает необходимый порядок вызовов конструкторов базовых классов
        и инициализирует интерфейс.
        
        '''
        self.__class__.__base__.__init__(self, parent)
        self.ui = self.uiClass()
        self.ui.setupUi(self)
        if self.__class__.slotHandleClasses:
            [base_cls.__init__(self, *args, **kwargs) 
             for base_cls 
             in self.__class__.slotHandleClasses]
            