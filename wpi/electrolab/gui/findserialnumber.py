#-*- coding: UTF-8 -*-
u"""
Created on 07.08.2012
@author: knur
ticket #
"""
from PyQt4.QtCore import QEvent, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget, QPalette, QColor
from PyQt4 import QtCore
import datetime

from electrolab.gui.common import UILoader
#from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.data import helper


class FindSerialNumber(QWidget, UILoader):
    adding = pyqtSignal(int)
    hideDialog = pyqtSignal()
    
    def __init__(self, _env, _oKeyboard):
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"FindSerialNumber.ui")
        self.env = _env
        self.oKeyboard = _oKeyboard
        self.iSerialNumberID = None
        self.oHelperSerialNumber = helper.SerialNumber(self.env)
        self.ui.sbYar.installEventFilter(self)
        self.ui.sbNumber.installEventFilter(self)
        self.oKeyboard.enter.connect(self.ui.sbNumber.focusNextChild) #TODO: Странно, почему нельзя цеплять к родителю????
        self.ui.sbYar.setValue(datetime.datetime.now().year - 2000) 
        #self.ui.btnArchive.clicked.connect(self.StartArchive)


    def showEvent(self, _event):
        self.ui.sbNumber.clear()
        self.ui.btnAdd.setEnabled(False)
        #self.ui.btnArchive.setEnabled(False)
        self.ui.sbNumber.focusNextChild()
        self.ui.sbNumber.setFocus()
        
    def eventFilter(self, _object, _event):
        u"""Отлавливает переход фокуса, для подключения экранной клавиатуры"""
        if _event.type() == QEvent.FocusOut:
            self.oKeyboard.connect_to_widget()
        if _event.type() in (QEvent.FocusIn, QEvent.MouseButtonPress):
            self.oKeyboard.connect_to_widget(_object)
        return False

    def change_serial_number(self):
        if not (self.ui.sbNumber.value and self.ui.sbYar.value):
            self.ui.leTransformer.clear()
            self.iSerialNumberID = None
            return
        oSNInfo = self.oHelperSerialNumber.get_id(self.ui.sbYar.value(), self.ui.sbNumber.value())
        if oSNInfo and oSNInfo.id: 
            self.ui.leTransformer.setText(oSNInfo.fullname)
            self.iSerialNumberID = oSNInfo.id
            self.ui.btnAdd.setEnabled(True)
            #self.ui.btnArchive.setEnabled(True)
        else:
            self.ui.leTransformer.clear()
            self.iSerialNumberID = None
            self.ui.btnAdd.setEnabled(False)
            #self.ui.btnArchive.setEnabled(False)

    def add(self):
        if self.iSerialNumberID:
            self.adding.emit(self.iSerialNumberID)
            self.ui.leTransformer.clear()
            self.ui.sbNumber.clear()
            self.iSerialNumberID = None
            self.ui.btnAdd.setEnabled(False)
            #self.ui.btnArchive.setEnabled(False)
            self.ui.sbNumber.setFocus()
            self.oKeyboard.connect_to_widget(self.ui.sbNumber)
            self.ui.sbNumber.focusNextChild()
            self.ui.sbNumber.setFocus()

    '''
    def StartArchive(self):
        from Archive import archive
        wind = archive(self.env, (self.ui.leTransformer.text(), self.ui.sbYar.text(), self.ui.sbNumber.text()))
        wind.show()
        wind.close()                
        wind.exec_()
        return
        if wind.tag <> 0:
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
            #wind.show()
            #wind.resizeEvent(None)
            #wind.close()                
            wind.exec_()


        from ClsMsr import classMsr
        wind = classMsr(env)
        if wind.tag <> 0:
             # Команды: show(),close() необходимы лишь для того, что бы сработала "resizeEvent"
             # Бред какой-то        
            wind.show()
            wind.resizeEvent(None)
            wind.close()                
            wind.exec_()
        '''