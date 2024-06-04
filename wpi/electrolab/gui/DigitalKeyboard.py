#-*- coding: UTF-8 -*-
'''
Created on 19.02.2011

@author: knur
'''
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import  QKeyEvent
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QVariant, QObject
from PyQt5.QtWidgets import QWidget
from electrolab.gui.common import UILoader


class DigitalKeyboard(QWidget, UILoader):
    
    enter = pyqtSignal()
    clear = pyqtSignal()
    KeyPress = pyqtSignal(u'QKeyEvent')
    
    def __init__(self, _env):
        super(QWidget, self).__init__()
        self.setUI(_env.config, u"DigitalKeyboard.ui")
        self.ui.btn_0.pressed.connect(self.digital_key_press)
        self.ui.btn_1.pressed.connect(self.digital_key_press)
        self.ui.btn_2.pressed.connect(self.digital_key_press)
        self.ui.btn_3.pressed.connect(self.digital_key_press)
        self.ui.btn_4.pressed.connect(self.digital_key_press)
        self.ui.btn_5.pressed.connect(self.digital_key_press)
        self.ui.btn_6.pressed.connect(self.digital_key_press)
        self.ui.btn_7.pressed.connect(self.digital_key_press)
        self.ui.btn_8.pressed.connect(self.digital_key_press)
        self.ui.btn_9.pressed.connect(self.digital_key_press)
        self.ui.btn_dot.pressed.connect(self.digital_key_press)
        
        self.ui.btn_BackSpace.pressed.connect(self.back_space_press)
        self.ui.btn_Clear.pressed.connect(self.clear.emit)
        self.ui.btn_Ok.pressed.connect(self.enter.emit)
        
        self.reciver = None
        self.setEnabled(False)

    @pyqtSlot()
    def digital_key_press(self):
        keyValue = self.sender().text()
        keyEvent = QKeyEvent(QtCore.QEvent.KeyPress, 0, QtCore.Qt.NoModifier, keyValue)
        self.KeyPress.emit(keyEvent)
        
    @pyqtSlot()
    def back_space_press(self):
        keyEvent = QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace , QtCore.Qt.NoModifier)
        self.KeyPress.emit(keyEvent)
        
    @pyqtSlot()
    def connect_to_widget(self, _reciver = None):
        u"""Подключает/Отлючает цифровую экранную клавиатуру для заданного получателя
            _reciver QObject - получатель
        """
        if(self.reciver == _reciver):
            return
        if(self.reciver):
            #Используется именно старый стиль, иначе начинаются падения TypeError: disconnect() failed between ........ 
            QObject.disconnect(self, QtCore.SIGNAL(u'KeyPress(QKeyEvent)'),  self.reciver.keyPressEvent)
            QObject.disconnect(self, QtCore.SIGNAL(u'clear()'),  self.reciver, QtCore.SLOT(u'clear()'))
        if(_reciver):
            self.reciver = _reciver
            self.KeyPress.connect(self.reciver.keyPressEvent)
            self.clear.connect(self.reciver.clear)
        self.setEnabled(bool(self.reciver))

