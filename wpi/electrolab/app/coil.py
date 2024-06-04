#-*- coding: UTF-8 -*-
u"""
Created on 21.07.2012
@author: Anton
ticket #
Description: 
"""

from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QString, QVariant
from electrolab.data import helper 
from electrolab.app import gost

class Coil(QObject):
    u""""""
    
#stateCoil
    NOCOIL = u'NOCOIL'
    NOTESTE = u'NOTESTE' 
    TESTE = u'TESTE' 
    DONE = u'DONE'

#Обявляем сигналы
    selected = pyqtSignal('QVariant')
    cleared = pyqtSignal()
    done = pyqtSignal(int)
    lastCoilDone = pyqtSignal(int)
    
    def __init__(self, _env, _adStandInfo, _iTestMapID, _iItemID, _bAvtoIteration):
        super(QObject, self).__init__()
        self.env = _env
        self.oHelperChecking = helper.Checking(_env)
        self.oHelperCoil = helper.Coil(_env)
        self.adStandInfo = _adStandInfo
        self.iTestMapID = _iTestMapID
        self.iItemID = _iItemID
        self.bAvtoIteration = _bAvtoIteration #Автоматический переход на следующий трансформатор по завершению испытания
        
        self.stateCoil = self.NOCOIL
        self.bLastCoil = False
        self.iCoilID = None
        self.bTesting = False

    def is_ready(self):
        u"""Готов к испытанию"""
        return bool(self.iCoilID and self.stateCoil != self.NOCOIL and self.stateCoil != self.DONE)

#Слоты принимаем внешние сообщения
    @pyqtSlot(int)
    def select(self, _iCoilID):
        if not _iCoilID: 
            self.to_nocoil()
        elif self.is_done(_iCoilID): 
            self.to_done(_iCoilID)
        elif self.oHelperChecking.is_clear(self.iItemID, _iCoilID):
            self.to_noteste(_iCoilID)
        else: 
            self.to_teste(_iCoilID)

    @pyqtSlot(int)
    def set_done(self, _iCoilID):
        u"""Вызывать для испытаний!"""
        self.stateCoil = self.DONE
        self.done.emit(self.iItemID)
        if not self.bAvtoIteration:
            return 
#        if not self.bLastCoil:
#            self.lastCoilDone.emit() 
        if self.oHelperCoil.get_next_id(_iCoilID):
            self.select(self.oHelperCoil.get_next_id(_iCoilID))
        else:
            self.lastCoilDone.emit(self.iItemID) 
#        else:
#            self.emit_selected(_iCoilID)

    @pyqtSlot(int)
    def clear(self, _iCoilID):
        if self.stateCoil == self.NOTESTE:
            return
#        self.oHelperChecking.clear_coil(self.iItemID, _iCoilID)
        self.to_noteste(_iCoilID)
        self.cleared.emit()

    def is_done(self, _iCoilID):
        sClassAccuracy = self.oHelperCoil.get_class_accuracy(_iCoilID)
        iSecondLoad = self.oHelperCoil.get_class_secondload(_iCoilID)
        oGost = gost.GOST7746(self.env, self.adStandInfo.GOST_ID, sClassAccuracy, iSecondLoad)
        for oPoint in oGost.get_point_list().itervalues():  #Проитись по всем точкам
            if not self.oHelperChecking.get_point(self.iItemID, _iCoilID, oPoint.I, oPoint.quadroLoad)[0]:
                return False
        return True
        

# Переходы состояния
    def to_nocoil(self):
        self.stateCoil = self.NOCOIL
        self.emit_selected(None)

    def to_noteste(self, _iCoilID):
        self.stateCoil = self.NOTESTE
        self.emit_selected(_iCoilID)

    def to_teste(self, _iCoilID):
        self.stateCoil = self.TESTE
        self.emit_selected(_iCoilID)

    def to_done(self, _iCoilID):
        self.stateCoil = self.DONE
        self.emit_selected(_iCoilID)

# События (Могут генерить сигналы)
    def emit_selected(self, _iCoilID):
        if self.iCoilID == _iCoilID:
            return
        self.iCoilID = _iCoilID
        if (not _iCoilID) or self.oHelperCoil.get_next_id(_iCoilID):
            self.bLastCoil = False
        else:
            self.bLastCoil = True
        self.selected.emit(QVariant(_iCoilID))
