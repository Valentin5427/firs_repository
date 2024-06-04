#coding=utf-8
'''
Created on 23.08.2011

@author: kaa
'''

from PyQt4.QtGui import QMessageBox
from dpframe.gui.menuitem import BaseSlotHolder, menuSlot

class FileSlotHolder(BaseSlotHolder):

    @menuSlot
    def save(self, checked, action, window, params, env):
        print action.objectName()
        print params
        print window

    @menuSlot
    def open(self, checked, action, window, params, env):
        window.setWindowTitle(u'New Window Title')

class EditSlotHolder(BaseSlotHolder):

    @menuSlot
    def copy(self, checked, action, window, params, env):
        env.log.error(u'Отработал слот copy')

    @menuSlot
    def paste(self, checked, action, window, params, env):
        env.log.error(u'Отработал слот paste. Настройки: {0}'.format(env.config))

    @menuSlot
    def search(self, checked, action, window, params, env):
        pass

    @menuSlot
    def replace(self, checked, action, window, params, env):
        pass

class RefSlotHolder(BaseSlotHolder):

    @menuSlot
    def openReference(self, checked, action, window, params, env):
        msgbox = QMessageBox(window)
        msgbox.setWindowTitle(u'Справочник {0}'.format(params[u'refname']))
        msgbox.setText(u'Справочник {0}'.format(params[u'refname']))
        msgbox.setInformativeText(u'Идентификатор меню: {0}\nВсе параметры: {1}'.format(action.objectName(), params))
        msgbox.exec_()

