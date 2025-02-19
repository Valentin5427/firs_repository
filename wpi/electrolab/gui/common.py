#-*- coding: UTF-8 -*-
"""
Created on 20.02.2011
diposoft(c)
@author: knur
Description:
Модуль с базовой логикой
"""
from dpframe.tech.typecheck import *
import electrolab
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtCore import pyqtSlot
import os.path
import sys

class UILoader:

    # @takes('UILoader', dict_of(unicode, anything), unicode)
    def setUI(self, config, sUIFileName):
        sys.path.insert(0, config.paths.ui) # TODO: ???
        UIClass = uic.loadUiType(os.path.join(config.paths.ui, sUIFileName))[0]
        self.ui = UIClass()
        self.ui.setupUi(self)

        
class MessageBox(QMessageBox):
    
    def __init__(self, _parent):
        QMessageBox.__init__(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.SplashScreen)
        self.setModal(True)
        self.parent = _parent
        
    def showEvent(self, _event):
        QMessageBox.showEvent(self, _event)
        rect = self.frameGeometry()
        rect.moveCenter(self.parent.frameGeometry().center() + self.parent.window().pos())
        self.move(rect.topLeft())
        
class QuitDialog(QDialog, UILoader):
    
    def __init__(self, _parent, _sMessage = None):
        QDialog.__init__(self)
        self.setUI(u"QuitDialog.ui")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.SplashScreen)
        self.setModal(True)
        self.parent = _parent
        if _sMessage:
            self.ui.lblMessage.setText(_sMessage)
        
    def showEvent(self, _event):
        QDialog.showEvent(self, _event)
        rect = self.frameGeometry()
        rect.moveCenter(self.parent.frameGeometry().center() + self.parent.window().pos())
        self.move(rect.topLeft())
        self.setMaximumSize(self.size())
        self.setMinimumSize(self.size())

class ELForm(QDialog, UILoader):
    next = QtCore.pyqtSignal()
    prev = QtCore.pyqtSignal()
    reNew = QtCore.pyqtSignal()
    loop = QtCore.pyqtSignal()
    
    def __init__(self, _sFileName):
        QDialog.__init__(self)
        self.setUI(_sFileName)
        self.addKeyboard()
        electrolab.init.devices.scaner.SetHandler(self.scanerHandler)
        electrolab.init.devices.scaner.SetEnabled(True)
        self.aBlockList = {}
        
    def closeEvent(self, event):
        QDialog.closeEvent(self, event)
        electrolab.init.devices.scaner.SetEnabled(False)
        electrolab.init.devices.scaner.SetHandler(None)
        QDialog.__del__(self)

        
    def addKeyboard(self):
        sizePolicy = QtGui.QSizePolicy()
        sizePolicy.setVerticalPolicy(sizePolicy.Preferred)
        sizePolicy.setHorizontalPolicy(sizePolicy.Preferred)
        
        self.keyboard = DigitalKeyboard()

        self.keyboard.setVisible(False)

        self.ui.hlGrid.addWidget(self.keyboard)
        self.keyboard.setSizePolicy(sizePolicy)

    def setEnabledBlock(self, _sAccesibleBlock = None):
        for sBlockName, widgedts in self.aBlockList.iteritems():
            for widget in widgedts:
                widget.setEnabled(_sAccesibleBlock == sBlockName or "All" == _sAccesibleBlock)
        
    def activateKeyboard(self, _bActivate, _reciver, _activator):
        """Включает/выключает цифровую экланную клавиатуру для заданного получателя
            _bActivate Bool - Включить/выключить, _reciver Object - получатель, _activator - Элемент управления включением/выключением клавиатуры  
        """
        self.keyboard.setVisible(_bActivate)
        if _bActivate:
            QtCore.QObject.connect(self.keyboard, QtCore.SIGNAL("KeyPress(QKeyEvent)"), _reciver.keyPressEvent)
            QtCore.QObject.connect(self.keyboard, QtCore.SIGNAL("clear()"), _reciver, QtCore.SLOT("clear()"))
            QtCore.QObject.connect(self.keyboard, QtCore.SIGNAL("okPressed()"), _activator, QtCore.SLOT("toggle()"))
            self.setEnabledBlock()
            _reciver.setEnabled(True)
            _activator.setEnabled(True)
        else: 
            QtCore.QObject.disconnect(self.keyboard, QtCore.SIGNAL("KeyPress(QKeyEvent)"), _reciver.keyPressEvent)
            QtCore.QObject.disconnect(self.keyboard, QtCore.SIGNAL("clear()"), _reciver, QtCore.SLOT("clear()"))
            QtCore.QObject.disconnect(self.keyboard, QtCore.SIGNAL("okPressed()"), _activator, QtCore.SLOT("toggle()"))
            self.setEnabledBlock("All")

    @pyqtSlot()
    def NextForm(self):
        u"""Передача уравления следующей форме"""
        self.emit(QtCore.SIGNAL("next()"))
        
    @pyqtSlot()
    def PrevForm(self):
        self.emit(QtCore.SIGNAL("prev()"))

    @pyqtSlot()
    def LoopForm(self):
        self.emit(QtCore.SIGNAL("loop()"))
        
    @pyqtSlot()
    def ReNewForm(self):
        self.emit(QtCore.SIGNAL("reNew()"))
        
    def scanerHandler(self, _sSerialNumber):
        u"""Обработчик серийных номеров"""
        self.emit(QtCore.SIGNAL("scan(QString)"), _sSerialNumber)
        
    def KNT05Handler(self, _oData):
        '''Обработчик данных измерений'''
        self.emit(QtCore.SIGNAL("dataKNT05(PyQt_PyObject)"), _oData)
        
        
class DigitalKeyboard(QDialog, UILoader):
    def __init__(self):
        QDialog.__init__(self)
        self.setUI(u"DigitalKeyboard.ui")
        QtCore.QObject.connect(self.ui.btn_0, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_1, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_2, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_3, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_4, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_5, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_6, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_7, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_8, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_9, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        QtCore.QObject.connect(self.ui.btn_dot, QtCore.SIGNAL("pressed()"), self.digitalKeyPress)
        
        QtCore.QObject.connect(self.ui.btn_BackSpace, QtCore.SIGNAL("pressed()"), self.backSpacePress)
        QtCore.QObject.connect(self.ui.btn_Clear, QtCore.SIGNAL("pressed()"), self.clearPress)
        QtCore.QObject.connect(self.ui.btn_Ok, QtCore.SIGNAL("pressed()"), self.okPressed)

    def digitalKeyPress(self):
        keyValue = self.sender().text()
        keyEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 0, QtCore.Qt.NoModifier, keyValue)
        self.emit(QtCore.SIGNAL("KeyPress(QKeyEvent)"),keyEvent)
        
    def backSpacePress(self):
        keyEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Backspace , QtCore.Qt.NoModifier)
        self.emit(QtCore.SIGNAL("KeyPress(QKeyEvent)"),keyEvent)
        
    def clearPress(self):
        self.emit(QtCore.SIGNAL("clear()"))
        
    def okPressed(self):
        #keyEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Enter, QtCore.Qt.NoModifier)
        #self.emit(QtCore.SIGNAL("KeyPress(QKeyEvent)"),keyEvent)
        try:
            self.emit(QtCore.SIGNAL("okPressed()"))
        except:
            pass
        