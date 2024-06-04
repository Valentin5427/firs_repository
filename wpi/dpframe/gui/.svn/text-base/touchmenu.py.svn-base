#!/usr/bin/env python
#coding=utf-8

import math
import os.path
from PyQt4.QtCore import Qt, QSize, QObject
from PyQt4.QtGui import QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QLabel, QFont, QPushButton, QIcon, QGridLayout, QApplication
import dpframe.ui.res.touchheader
from dpframe.base.envapp import checkenv
from dpframe.base.inits import default_log_init


@checkenv(u'log')
@default_log_init
class BaseTouchMenu(QWidget):
    u'''
    Класс главного окна-меню для touchscreen с динамической загрузкой меню.
    Пример использования класса - dpframe.examples.gui.touchmenu.main

    '''

    class Ui(object):
        u'''
        Служебный класс, инкапсулирующий все интерфейсные элементы главного окна.

        '''

        SPACING = 20
        HEADFONTSIZE = 20
        BTNFONTSIZE = 20
        STATUSFONTSIZE = 16

        MINBTNWIDTH = 100
        ICONSIZE = 32

        HEADSTRETCH = 2
        MAINSTRETCH = 17
        STATUSSTRETCH = 1

        def __init__(self, window):
            u'''
            Конструктор интерфейса главного окна, загружает меню верхнего уровня.

            window - ссылка на главное окно;

            '''

            self.window = window
            self.buttons = []
            window.setObjectName(u'window')
            self.verticalLayout = QVBoxLayout(window)
            self.verticalLayout.setMargin(self.SPACING)
            self.verticalLayout.setSpacing(self.SPACING)
            self.verticalLayout.setObjectName(u'verticalLayout')
            self.wHeader = QWidget(window)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setVerticalStretch(self.HEADSTRETCH)
            self.wHeader.setSizePolicy(sizePolicy)
            self.wHeader.setObjectName(u'wHeader')
            self.horizontalLayout = QHBoxLayout(self.wHeader)
            self.horizontalLayout.setSpacing(self.SPACING)
            self.horizontalLayout.setMargin(0)
            self.horizontalLayout.setObjectName(u'horizontalLayout')
            self.lblTitle = QLabel(self.wHeader)
            self.lblTitle.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
            self.lblTitle.setFont(QFont(QApplication.font().family(), self.HEADFONTSIZE))
            self.lblTitle.setAlignment(Qt.AlignCenter)
            self.lblTitle.setObjectName(u'lblTitle')
            self.horizontalLayout.addWidget(self.lblTitle)
            self.btnHome = QPushButton(self.wHeader)
            self.btnHome.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
            self.btnHome.setMinimumSize(QSize(self.MINBTNWIDTH, 0))
            self.btnHome.setText(u'')
            self.btnHome.setIcon(QIcon(u':/home'))
            self.btnHome.setIconSize(QSize(self.ICONSIZE, self.ICONSIZE))
            self.btnHome.setObjectName(u'btnHome')
            self.btnHome.clicked.connect(window.home)
            self.horizontalLayout.addWidget(self.btnHome)
            self.btnUp = QPushButton(self.wHeader)
            self.btnUp.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
            self.btnUp.setMinimumSize(QSize(self.MINBTNWIDTH, 0))
            self.btnUp.setText(u'')
            self.btnUp.setIcon(QIcon(u':/up'))
            self.btnUp.setIconSize(QSize(self.ICONSIZE, self.ICONSIZE))
            self.btnUp.setObjectName(u'btnUp')
            self.btnUp.clicked.connect(window.up)
            self.horizontalLayout.addWidget(self.btnUp)
            self.btnClose = QPushButton(self.wHeader)
            self.btnClose.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
            self.btnClose.setMinimumSize(QSize(self.MINBTNWIDTH, 0))
            self.btnClose.setText(u'')
            self.btnClose.setIcon(QIcon(u':/close'))
            self.btnClose.setIconSize(QSize(self.ICONSIZE, self.ICONSIZE))
            self.btnClose.setObjectName(u'btnClose')
            self.btnClose.clicked.connect(window.close)
            self.horizontalLayout.addWidget(self.btnClose)
            self.verticalLayout.addWidget(self.wHeader)
            self.wMain = QWidget(window)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setVerticalStretch(self.MAINSTRETCH)
            self.wMain.setSizePolicy(sizePolicy)
            self.wMain.setObjectName(u'wMain')
            self.gridLayout = QGridLayout(self.wMain)
            self.gridLayout.setMargin(0)
            self.gridLayout.setObjectName(u'gridLayout')
            self.gridLayout.setSpacing(self.SPACING)

            self.verticalLayout.addWidget(self.wMain)
            self.lblStatus = QLabel(window)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setVerticalStretch(self.STATUSSTRETCH)
            self.lblStatus.setSizePolicy(sizePolicy)
            self.lblStatus.setFont(QFont(QApplication.font().family(), self.STATUSFONTSIZE))
            self.lblStatus.setObjectName(u'lblStatus')
            self.verticalLayout.addWidget(self.lblStatus)

            resources = window.menu.get(u'res', [])
            for res in resources:
                __import__(res, globals(), locals(), [], -1)

            self.loadMenu(window, [u'main'])

        def menuinfo(self):
            u'''
            Вернуть полную информацию о текущем уровне меню.

            '''

            if u'main' != self.names[0]:
                raise RuntimeError(u'Incorrect menu name: "{0}". First part must be "main".'.format(u'.'.join(self.names)))
            menu = self.window.menu
            subs = menu[u'main']
            ismain = len(self.names) == 1
            if ismain:
                title = u'Главное меню'
                desc = u''
                cols = menu.get(u'cols', 1)
            else:
                for i, name in enumerate(self.names[1:]):
                    if i == (len(self.names) - 2):
                        title = subs[name][u'title']
                        desc = subs[name].get(u'statustip', u'')
                        cols = subs[name].get(u'cols', 1)
                    subs = subs[name][u'subs']
            return ismain, subs, title, desc, cols

        def loadMenu(self, window, names):
            u'''
            Загрузить и отобразить кнопки текущего уровня меню.

            window - ссылка на главное окно;
            names - имя текущего уровня меню (список).

            '''

            self.names = names
            for btn in self.buttons:
                btn.setVisible(False)
                self.gridLayout.removeWidget(btn)
            self.buttons = []
            self.holders= []
            ismain, subs, title, desc, cols = self.menuinfo()

            self.btnHome.setEnabled(not ismain)
            self.btnUp.setEnabled(not ismain)
            self.lblTitle.setText(title)
            self.lblStatus.setVisible(not ismain)
            self.lblStatus.setText(desc)

            rows = int(math.ceil(len(subs)*1./cols))
            col = row = 0
            for name, item in subs.items():
                if item.get(u'separator', False):
                    continue
                btn = QPushButton(self.wMain)
                self.buttons.append(btn)
                btn.setObjectName(name)
                btn.setFont(QFont(QApplication.font().family(), self.BTNFONTSIZE, QFont.Bold if u'subs' in item else QFont.Normal))
                btn.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
                btn.setText(item[u'title'])
                btn.setIconSize(QSize(self.ICONSIZE, self.ICONSIZE))
                btn.setIcon(QIcon(item.get(u'icon', u'')))
                self.gridLayout.addWidget(btn, row, col)
                slot = None
                if u'subs' in item:
                    slot = window.showMenu
                else:
                    slotname = item[u'slot']
                    if slotname.split(u'.')[0] == u'self':
                        slot = window.__getattribute__(slotname.split(u'.')[-1])
                    else:
                        cls, func = os.path.splitext(slotname)
                        func = func[1:]
                        module, cls = os.path.splitext(cls)
                        cls = cls[1:]
                        module = __import__(module, globals(), locals(), [cls], -1)
                        holder = module.__getattribute__(cls)(window)
                        self.holders.append(holder)
                        holder.addParams(btn, item.get(u'params', {}))
                        slot = holder.__getattribute__(func)
                btn.clicked.connect(slot)

                col += 1
                if col == cols:
                    col = 0
                    row += 1


    def __init__(self, menu):
        u'''
        Конструктор главного окна меню.

        menu - словарь, содержащий описание структуры меню;

        Структура словаря меню определяется схемой dpframe.tech.json.schema.MENU
        '''

        QWidget.__init__(self)
        self.setObjectName(u'TouchMenu')
        self.menu = menu
        self.ui = self.Ui(self)

    def home(self):
        u'''
        Слот обработки перехода на верхний уровень меню.
        '''

        self.ui.loadMenu(self, [u'main'])

    def up(self):
        u'''
        Слот обработки перехода на уровень выше.
        '''

        self.ui.loadMenu(self, self.ui.names[:-1])

    def showMenu(self):
        u'''
        Слот обработки перехода на подменю.
        '''

        self.ui.names.append(unicode(QObject().sender().objectName()))
        self.ui.loadMenu(self, self.ui.names)
