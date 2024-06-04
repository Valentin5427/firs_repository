#-*- coding: UTF-8 -*-
u"""
Created on 05.08.2012
@author: Anton
"""

from PyQt4.QtCore import QEvent, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget, QPalette, QColor
from PyQt4 import QtCore

from electrolab.gui.common import UILoader
from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.data import helper

class ParamClimat(QWidget, UILoader):
    
    applied = pyqtSignal(int)
    
    def __init__(self, _env, _iRoomID = None):
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"ParamClimat.ui")
        self.env = _env
        self.iRoomID = _iRoomID
        self.iOperID = None

        self.oDigitalKeyboard = DigitalKeyboard(_env)
        self.ui.lblExtended.setVisible(False)
        self.ui.hlOperation.addWidget(self.oDigitalKeyboard)
        self.oDigitalKeyboard.setVisible(True)
        self.oDigitalKeyboard.enter.connect(self.ui.leTemperature.focusNextChild) #TODO: Странно, почему нельзя цеплять к родителю???? 

        self.ui.leTemperature.installEventFilter(self)
        self.ui.leHumidity.installEventFilter(self)
        self.ui.lePressure.installEventFilter(self)

        self.ui.btnOk.pressed.connect(self.apply)
        self.ui.leTemperature.valueChanged.connect(self.terms_change)
        self.ui.leHumidity.valueChanged.connect(self.terms_change)
        self.ui.lePressure.valueChanged.connect(self.terms_change)

        self.normalPalette = QPalette()
        self.normalPalette.setColor(QPalette.Text, QColor(QtCore.Qt.black))
        self.alarmPalette = QPalette()
        self.alarmPalette.setColor(QPalette.Text, QColor(QtCore.Qt.red))
        
        self.oHelperClimat = helper.Climat(self.env)
        self.terms_change()

    def setRoom(self, _iRoomID):
        self.iRoomID = _iRoomID

    def showEvent(self, _event):
        self.ui.leTemperature.setFocus()
        self.ui.leTemperature.selectAll()

    def set_operator(self, _iOperID):
        self.iOperID = _iOperID

    def eventFilter(self, _object, _event):
        u"""Отлавливает переход фокуса, для подключения экранной клавиатуры"""
        if _event.type() == QEvent.FocusOut:
            self.oDigitalKeyboard.connect_to_widget()
        if _event.type() in (QEvent.FocusIn, QEvent.MouseButtonPress):
            self.oDigitalKeyboard.connect_to_widget(_object)
        return False
    
    def temperature_check(self, _value):
        if 15 <= _value <= 35:
            self.ui.leTemperature.setPalette(self.normalPalette)
            return True
        else:
            self.ui.leTemperature.setPalette(self.alarmPalette)
            return False
    
    def humidity_check(self, _value):
        if 30 <= _value <= 80:
            self.ui.leHumidity.setPalette(self.normalPalette)
            return True
        else:
            self.ui.leHumidity.setPalette(self.alarmPalette)
            return False
    
    def pressure_check(self, _value):
        if 85 <= _value <= 105:
            self.ui.lePressure.setPalette(self.normalPalette)
            return True
        else:
            self.ui.lePressure.setPalette(self.alarmPalette)
            return False
    
    @pyqtSlot(int)
    def terms_change(self, _value = None):
        res = self.temperature_check(self.ui.leTemperature.value())
        res = self.humidity_check(self.ui.leHumidity.value()) and res
        res = self.pressure_check(self.ui.lePressure.value()) and res
        if (res):
            self.ui.btnOk.setEnabled(True)
        else:
            self.ui.btnOk.setEnabled(False)
    
    @pyqtSlot()
    def apply(self):
        if not self.iOperID:
            raise Exception(u'Not set iOperID. Need call set_operator(_iOperID)')
        iClimatID = self.oHelperClimat.insert(
                                            self.iRoomID
                                            , self.iOperID
                                            , int(self.ui.leTemperature.text())
                                            , int(self.ui.leHumidity.text())
                                            , int(self.ui.lePressure.text())
                                            )
        self.applied.emit(iClimatID)
        
