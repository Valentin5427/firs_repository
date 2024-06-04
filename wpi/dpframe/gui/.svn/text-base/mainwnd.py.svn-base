#!/usr/bin/env python
#coding=utf-8

import os.path
from PyQt4.QtGui import QMainWindow, QMdiArea, QMenuBar, QWidget, QMenu,  QAction, QIcon, QKeySequence, QToolBar
from PyQt4.QtCore import Qt
from dpframe.base.envapp import checkenv
from dpframe.base.inits import default_log_init

@checkenv(u'log')
@default_log_init
class BaseMainWnd(QMainWindow):
    u'''
    Базовый класс главного окна приложения с динамической загрузкой меню и панелей инструментов.
    Пример использования класса - dpframe.examples.gui.mainwnd.main

    '''

    class Ui(object):
        u'''
        Служебный класс, инкапсулирующий все интерфейсные элементы главного окна.

        '''

        def __init__(self, window, menu, cwidgetclass):
            u'''
            Конструктор интерфейса главного окна, загружает меню и панели инструментов.

            window - ссылка на главное окно;
            menu - словарь, содержащий описание структуры меню;
            cwidgetclass - класс центрального виджета главного окна.

            Структура словаря меню определяется схемой dpframe.tech.json.schema.MENU

            '''

            self.window = window
            self.holders = []
            self.centralwidget = cwidgetclass(window)
            self.centralwidget.setObjectName(u'centralwidget')
            window.setCentralWidget(self.centralwidget)
            self.menubar = QMenuBar(window)
            self.menubar.setObjectName(u'menubar')
            window.setMenuBar(self.menubar)
            resources = menu.get(u'res', [])
            for res in resources:
                __import__(res, globals(), locals(), [], -1)
            self.items = {}
            self.load_menu(self.menubar, u'', menu[u'main'])
            self.toolbars = []
            self.create_toolbars(menu[u'toolbars'])


        def load_menu(self, parent, pname, subs):
            u'''
            Загрузить главное меню. Вызывается рекурсивно.

            parent - родительское меню;
            pname - имя родительского меню (ключ в словаре элементов self.items);
            subs - словарь, содержащий описание структуры дочернего меню.

            Структура словаря дочернего меню определяется схемой dpframe.tech.json.schema.MENU

            '''
            
            for menu in subs:
                name = u'.'.join([pname, menu]) if pname else menu
                menudict = subs[menu]
                if u'subs' in menudict:
                    #submenu
                    qmenu = self.items[name] = QMenu(parent)
                    qmenu.setObjectName(name)
                    qmenu.setIcon(QIcon(menudict.get(u'icon', u'')))
                    qmenu.setTitle(menudict[u'title'])
                    self.load_menu(qmenu, name, menudict[u'subs'])
                    parent.addAction(qmenu.menuAction())
                else:
                    #menu item
                    qaction = self.items[name] = QAction(parent)
                    qaction.setObjectName(name)
                    if u'separator' in menudict:
                        qaction.setSeparator(True)
                    else:
                        qaction.setText(menudict[u'title'])
                        qaction.setIcon(QIcon(menudict.get(u'icon', u'')))
                        qaction.setToolTip(menudict.get(u'tooltip', u''))
                        qaction.setStatusTip(menudict.get(u'statustip', u''))
                        qaction.setCheckable(menudict.get(u'checkable', False))
                        qaction.setIconVisibleInMenu(menudict.get(u'menuicon', False))
                        shortcutlst = menudict.get(u'shortcut', [])
                        for shortcut in [shortcutlst] if isinstance(shortcutlst, basestring) else shortcutlst:
                            qaction.setShortcut(QKeySequence(shortcut))
                        slotname = menudict[u'slot']
                        if slotname.split(u'.')[0] == u'self':
                            slot = self.window.__getattribute__(slotname.split(u'.')[-1])
                        else:
                            cls, func = os.path.splitext(slotname)
                            func = func[1:]
                            module, cls = os.path.splitext(cls)
                            cls = cls[1:]
                            #TODO: не загружать модуль целиком, только слот
                            module = __import__(module, globals(), locals(), [cls], -1)
                            holder = module.__getattribute__(cls)(self.window)
                            self.holders.append(holder)
                            holder.addParams(qaction, menudict.get(u'params', {}))
                            slot = holder.__getattribute__(func)

                        if qaction.isCheckable():
                            qaction.toggled.connect(slot)
                        else:
                            qaction.triggered.connect(slot)
                    parent.addAction(qaction)

        def create_toolbars(self, toolbars):
            u'''
            Создать панели инструментов.

            toolbars - словарь с описаниями панелей инструментов.

            Структура словаря панелей инструментов определяется частью схемы dpframe.tech.json.schema.MENU (свойство toolbars)

            '''

            for barname, buttons in toolbars.items():
                toolbar = QToolBar(self.window)
                self.toolbars.append(toolbar)
                toolbar.setObjectName(barname)
                self.window.addToolBar(Qt.TopToolBarArea, toolbar)
                for button in buttons:
                    if u'sep' == button:
                        toolbar.addSeparator()
                    else:
                        toolbar.addAction(self.items[button])


    def __init__(self, caption, menu, cwidgetclass=QWidget):
        u'''
        Конструктор главного окна приложения.

        caption - заголовок главного окна;
        menu - словарь, содержащий описание структуры меню;
        cwidgetclass - класс центрального виджета главного окна (QWidget по умолчанию).

        Структура словаря меню определяется схемой dpframe.tech.json.schema.MENU

        '''

        QMainWindow.__init__(self)
        self.setObjectName(u'MainWindow')
        self.setWindowTitle(caption)
        self.ui = self.Ui(self, menu, cwidgetclass)


@checkenv(u'log')
@default_log_init
class BaseMDIMainWnd(BaseMainWnd):
    u'''
    Базовый класс многодокументного (MDI) главного окна приложения с динамической загрузкой меню и панелей инструментов.
    Пример использования класса - dpframe.examples.gui.mainwnd.main

    '''

    def __init__(self, caption, menu):
        u'''
        Конструктор главного окна приложения.

        caption - заголовок главного окна;
        menu - словарь, содержащий описание структуры меню;

        Структура словаря меню определяется схемой dpframe.tech.json.schema.MENU
        Центральным виджетом является QMdiArea.

        '''
        BaseMainWnd.__init__(self, caption, menu, QMdiArea)
        
