#!/usr/bin/env python
#coding=utf-8

import sys
import abc

from PyQt4.QtGui import QApplication, QSystemTrayIcon, QMessageBox
from PyQt4.QtCore import QTranslator, SIGNAL, SLOT

from dpframe.gui.wfactory import CWidgetFactory
from dpframe.tech.singleapp import SingleInstance

class BaseApp(QApplication):
    u'''Базовый класс приложения PyQt.
    Инициализирует локализацию приложения.
    '''
    
    def __init__(self, args=sys.argv, trans_file=None):
        u'''Параметры:
        args - список внешних аргументов, как правило, sys.argv
        trans_file - файл локализации
        
        '''
        QApplication.__init__(self, args)
        if trans_file:
            self.translator = QTranslator(self)
            self.translator.load(trans_file)
            self.installTranslator(self.translator)


class CommonApp(BaseApp):
    u'''Обертка над классом приложения Qt. Автоматизирует создание главного окна приложения
    из ресурса *.ui
    
    Пример использования: examples/gui/arithmetic.py
    
    '''

    def __init__(self, ui_file, handles=None, maximize=True, trans_file=None, args=sys.argv):
        u'''Параметры:
        args - список внешних аргументов, как правило, sys.argv
        ui_file - ресурс главного окна
        trans_file - файл локализации
        handles - итератор прикладных базовых классов
        maximize - признак максимизации главного окна при старте приложения.
        
        '''
        BaseApp.__init__(self, args, trans_file)
        self.main_wnd = CWidgetFactory.create(ui_file, handles)()
        self.setActiveWindow(self.main_wnd)
        if maximize:
            self.main_wnd.showMaximized()
        else:
            self.main_wnd.show()            



class SysTrayApp(BaseApp):
    u'''Приложение, отображающее иконку в системном трее.
    Опционально может запускаться только в единственном экземпляре.
    
    Пример использования: dpframe/uiagentsvc.py
    
    '''
    
    class BaseHandler(object):
        u'''Интерфейс прикладного обработчика для приложения SysTrayApp
        '''
        
        @property
        def menu(self):
            u'''Контекстное меню иконки в трее.
            Свойство должно быть переопределено в дочернем прикладном классе.
            
            '''
            return QMenu()
        
        @property
        def ico(self):
            u'''Иконка для отображения в трее.
            Свойство должно быть переопределено в дочернем прикладном классе.
            
            '''
            return QIcon()

        @property
        def tooltip(self):
            u'''Всплывающая подсказка (tooltip).
            Свойство должно быть переопределено в дочернем прикладном классе.
            
            '''
            return u''

        def menu_activated(self, reason):
            u'''Обработчик активации контекстного меню.
            Здесь можно задать видимость и активность пунктов меню и пр.
            Может быть переопределен в дочернем прикладном классе.
            
            '''
            pass


    def __init__(self, hclass, args=sys.argv, app_unique_name=u'', trans_file=None):
        u'''Параметры:
        hclass - класс прикладного обработчика
        args - аргументы командной строки
        app_unique_name - уникальное имя приложения, если задано, то можно запустить только один экземпляр приложения с этим именем
        trans_file - файл локализации
        
        '''
        
        class SysTrayIcon(QSystemTrayIcon, hclass):
            def __init__(self):
                QSystemTrayIcon.__init__(self)
                hclass.__init__(self)
                
        BaseApp.__init__(self, args, trans_file)
        
        if not SysTrayIcon.isSystemTrayAvailable():
            msgBox = QMessageBox()
            msgBox.setText(u'Операционная система не поддерживает системный трей.')
            msgBox.exec_()
            sys.exit(1) #not sure
            #raise SystemError(u'Операционная система не поддерживает системный трей.')
            
        if app_unique_name: 
            self._instance = SingleInstance(app_unique_name)
            if not self._instance.issingle:
                msgBox = QMessageBox()
                msgBox.setText(u"Приложение '{0}' уже запущено.".format(app_unique_name))
                msgBox.exec_()
                sys.exit(1) #not sure
            
        self.tray = SysTrayIcon()

        self.tray.setIcon(self.tray.ico)
        self.tray.setContextMenu(self.tray.menu)
        tooltip = self.tray.tooltip
        if tooltip:
            self.tray.setToolTip(tooltip)
        self.connect(self.tray, SIGNAL(u'activated(QSystemTrayIcon::ActivationReason)'), self.tray.menu_activated)
        self.tray.show()
        
        