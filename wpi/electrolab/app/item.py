#-*- coding: UTF-8 -*-
u"""
Created on 18.07.2012
@author: Anton
ticket #
Description: Поведение при работе с трансорматороми на таележке, создается для каждой тележке
"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal,  QVariant
from electrolab.data import helper
from electrolab.app import gost

class Item(QObject):
    u""""""
    
#stateItem
    NOITEM = u'NOITEM'
    NOTESTE = u'NOTESTE' 
    DONE = u'DONE'
    FAIL = u'FAIL'

#Обявляем сигналы
    selectedItem = pyqtSignal('QVariant') #Выбран другой трансформатор
    changeItem = pyqtSignal(int) #Сообщить о изменении состояния трансформатора
    noEmptyItem = pyqtSignal(int) #Сообщить о попытки удалить не пустой трансформатор
    deleted = pyqtSignal()
    lastItemDone = pyqtSignal(int)
    
    def __init__(self, _env, _adStandInfo, _iTestMapID, _bAvtoIteration):
        super(QObject, self).__init__()
        self.env = _env
        self.oHelperItem = helper.Item(_env)
        self.oHelperCoil = helper.Coil(_env)
        self.oHelperChecking = helper.Checking(_env)
        
        self.adStandInfo = _adStandInfo
        self.iTestMapID = _iTestMapID
        self.bAvtoIteration = _bAvtoIteration #Автоматический переход на следующий трансформатор по завершению испытания
        
        self.stateItem = self.NOITEM
#        self.bLastItem = False
        self.iItemID = None

#Слоты принимаем внешние сообщения
    @pyqtSlot(int)
    def select(self, _iItemID):
        if not _iItemID: 
            self.to_noitem()
            return 
        elif self.oHelperItem.is_clear(_iItemID): self.to_noteste(_iItemID)
        elif self.oHelperItem.is_done(_iItemID): self.to_done(_iItemID)
        elif self.oHelperItem.is_fail(_iItemID): self.to_fail(_iItemID)

    @pyqtSlot()
    def delete(self):
        if self.stateItem == self.NOITEM:
            return
        elif self.stateItem == self.NOTESTE:
            self.oHelperItem.delete(self.iItemID)
            iNextItemID = self.oHelperItem.get_next_id(self.iTestMapID, self.iItemID) or self.oHelperItem.get_prev_id(self.iTestMapID, self.iItemID) 
            self.deleted.emit()
            self.select(iNextItemID)
        else:
            self.noEmptyItem.emit(self.iItemID)
            
    def is_done(self, _iItemID):
        #TODO: Перетащить в help-ер
        coilList = self.oHelperItem.get_coils(_iItemID)
        for iCoilID in coilList: #Проитись по всем обмоткам
            sClassAccuracy = self.oHelperCoil.get_class_accuracy(iCoilID)
            iSecondLoad = self.oHelperCoil.get_class_secondload(iCoilID)
            oGost = gost.GOST7746(self.env, self.adStandInfo.GOST_ID, sClassAccuracy, iSecondLoad)
            for oPoint in oGost.get_point_list().itervalues():  #Проитись по всем точкам
                if not self.oHelperChecking.get_point(_iItemID, iCoilID, oPoint.I, oPoint.quadroLoad)[0]:
                    return False
        return True

    @pyqtSlot(int)
    def chek_done(self, _iItemID):
        if self.is_done(_iItemID):
            self.set_done(_iItemID)
        else:
            self.set_noteste(_iItemID)


    @pyqtSlot(int)
    def complit(self, _iItemID):
        self.chek_done(_iItemID)
        if not self.bAvtoIteration:
            return 
        if not self.is_last():
            self.select(self.oHelperItem.get_next_id(self.iTestMapID, _iItemID) or _iItemID)
        else:
            self.lastItemDone.emit(self.iItemID) 


    @pyqtSlot(int)
    def set_done(self, _iItemID):
        if self.stateItem == self.DONE:
            return
        self.oHelperItem.set_isTested(_iItemID, True)
        self.to_done(_iItemID)
        self.changeItem.emit(_iItemID)
        
    @pyqtSlot(int)
    def set_noteste(self, _iItemID):
        if self.stateItem == self.NOTESTE:
            return
        self.oHelperItem.set_isTested(_iItemID, False)
        self.to_noteste(_iItemID)
        self.changeItem.emit(_iItemID)
        
    @pyqtSlot(int, int)
    def set_defect(self, _iItemID, _iDefectID):
        self.oHelperItem.set_defect(_iItemID, _iDefectID)
        self.changeItem.emit(_iItemID)
        
    def able_delete(self):
        return self.stateItem == self.NOTESTE 

# Переходы состояния
    def to_noitem(self):
        self.stateItem = self.NOITEM
        self.selected(None)

    def to_noteste(self, _iItemID):
        self.stateItem = self.NOTESTE
        self.selected(_iItemID)

    def to_done(self, _iItemID):
        self.stateItem = self.DONE
        self.selected(_iItemID)

    def to_fail(self, _iItemID):
        self.stateItem = self.FAIL
        self.selected(_iItemID)

# События (Могут генерить сигналы)
    def selected(self, _iItemID):
        if self.iItemID == _iItemID:
            return
        self.iItemID = _iItemID
#        if (not _iItemID) or self.oHelperItem.get_next_id(self.iTestMapID, _iItemID):
#            self.bLastItem = False
#        else:
#            self.bLastItem = True
        self.selectedItem.emit(QVariant(_iItemID))

    def is_last(self):
        return  not bool(self.oHelperItem.get_next_id(self.iTestMapID, self.iItemID))
    