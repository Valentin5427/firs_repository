#-*- coding: UTF-8 -*-
u"""
Created on 15.07.2012
@author: knur
ticket #
Логика поведения при работе с картами испытания
"""

from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal, QString, QVariant
from electrolab.data import helper 
from dpframe.tech.AttrDict import AttrDict
from electrolab.gui.msgbox import getTrue

class BarCode(object):
    u"""Анализ штрих-кода используемого для  маркировки трансформатора"""
    
    def __init__(self):
        pass
    
    def varToInt(self, _symbol):
        try:
            res = int(_symbol)
        except:
            res = 0
        return res


    def check_EAN_valid(self, _serNum):
        """
            Расчет контрольной цифры в штрихкоде EAN-13
            
            Шаг 1     Отбросить контрольный разряд (крайний справа)
            Шаг 2     Сложить разряды, стоящие на четных местах
            Шаг 3     Результат ШАГа 2 умножить на 3
            Шаг 4     Сложить разряды, стоящие на нечетных местах
            Шаг 5     Суммировать результаты ШАГов 3 и 4
            Шаг 6     В полученном числе крайнюю справа цифру вычесть из 10. Полученный результат и есть значение контрольной цифры
            Пример расчета контрольного разряда в коде EAN-13: 46 76221 35746 С
            Шаг 1     46 76221 35746
            Шаг 2     6+6+2+3+7+6=30
            Шаг 3     30х3=90
            Шаг 4     4+7+2+1+5+4=23
            Шаг 5     90+23=113
            Шаг 6     10-3=7
            Полный номер EAN-13 будет следующим: 46 76221 35746 7
        """
        arrNum = []
        for item in _serNum:
            arrNum.append(self.varToInt(item))
        res = (arrNum[1] + arrNum[3] + arrNum[5] + arrNum[7] + arrNum[9] + arrNum[11]) * 3 
        res = res + (arrNum[0] + arrNum[2] + arrNum[4] + arrNum[6] + arrNum[8] + arrNum[10])
        res = self.varToInt(str(res)[len(str(res))-1])
        if res > 0:
            res = 10 - res
        return arrNum[12] == self.varToInt(res)

    def parse_barcode(self, _sSerialNumber):
        returnValue = AttrDict({u'error':None, u'year':None, u'serial':None})
        if len(_sSerialNumber) != 13:
            returnValue.error = u'Неверный тип штрих-кода' 
            return returnValue
        if not str(_sSerialNumber).isdigit():
            return
        firstChar = _sSerialNumber[0]
        returnValue.serial = int(_sSerialNumber[1:7])
        returnValue.year = int(_sSerialNumber[9:11])
        lastChar = _sSerialNumber[11]
        if not self.check_EAN_valid(_sSerialNumber):
            returnValue.error = u'Нечитаемый штрих-код' 
        elif firstChar != u'9' or lastChar != u'0':
            returnValue.error = u'Некорректный штрих-код: %s' % _sSerialNumber
        else:
            returnValue.error = None
        return returnValue
    

class TestMap(QObject):
    u""""""
    #StateMap
    NOMAP = u'NOMAP'
    EMPTY = u'EMPTY'
    FULL = u'FULL'
    DONE = u'DONE'
#    TESTING = u'TESTING'
    #Сигналы
#    signalCanChangeOperator = pyqtSignal('QString')
    requestClimat = pyqtSignal() #Поднять диалог климата
    requestSupervisor = pyqtSignal() #Поднять диалог выбора поверителя
    requestTester = pyqtSignal() #Поднять диалог выбора испытателя
    mapRefresh = pyqtSignal() #Обновить грид
    buttonRefresh = pyqtSignal() #Обновить кнопки (enable/disable)
    # testTypeSelected = pyqtSignal(int, str)
    testerSelected = pyqtSignal(int, str)
    assistantSelected = pyqtSignal(int, str)
    supervisorSelected = pyqtSignal(int, str)
    selected = pyqtSignal(u'QVariant')
    dublicated = pyqtSignal()#Такой трансформатор уже есть на тележке
    
    #tam 24.11.2016       
    calc_global = pyqtSignal() #Глобальный расчет для 3 и 4 испатания
    
    
#    scan = pyqtSignal(str)
#    errorScanner = pyqtSignal(str) #Поднять диалог выбора испытателя
     
    def __init__(self, _env, _iStandID = None):
        super(QObject, self).__init__()
        self.oHelperMap = helper.TestMap(_env)
        self.oHelperItem = helper.Item(_env)
        self.oHelperSerial = helper.SerialNumber(_env)
        self.oHelperOperator = helper.Operator(_env)
        self.oHelpClimat =  helper.Climat(_env)
        self.oHelpStand =  helper.Stand(_env)

        self.iStandID = _iStandID 
        self.adStandInfo = self.oHelpStand.get_info(self.iStandID)
        
        self.iTesterID = None #Он же состояние нет испытателя 
        self.iAssistantID = None 
        self.iSupervisorID = None
        print 'self.iSupervisorID=', self.iSupervisorID
        self.iClimatID = None
        self.iMapID = None
        #Состояния
        self.stateMap = self.NOMAP
        
        #Цепляем сканер
#        self.oBarCode = BarCode()
#        self.scanner = _env.devices.scanner
#        self.scanner.SetHandler(self.scanning)
        
    def set_up(self, _adStandInfo):
        u"""Установить готовность. Вызывается при смене типа испытания"""
        if self.stateMap != self.NOMAP:
            Exception(u'TestMap no empty')
        self.iStandID = _adStandInfo.ID
        self.adStandInfo = _adStandInfo
        # self.iTesterID = None #Он же состояние нет испытателя
        # self.iAssistantID = None
        # self.iSupervisorID = None
        self.iClimatID = None
        self.iMapID = None

        if(not _adStandInfo.EnableAssistant or not self.oHelpStand.existsOperator(_adStandInfo.ID, self.iAssistantID)):
            self.iAssistantID = None

        if(not _adStandInfo.EnableSupervisor or not self.oHelpStand.existsOperator(_adStandInfo.ID, self.iSupervisorID)):
            ####self.iSupervisorID = None
            print 'self.iSupervisorID1=', self.iSupervisorID
           #6.04.2018 self.requestSupervisor.emit()

        if(self.iTesterID == None or not self.oHelpStand.existsOperator(_adStandInfo.ID, self.iTesterID)):
            self.iTesterID = None
            self.requestTester.emit()
        else:
            self.supervisor_request()
            self.climat_request()

        # if(self.iAssistantID == None or not self.oHelpStand.existsOperator(_iStandID, self.iAssistantID)):
        #     self.requestTester.emit()

    @pyqtSlot(int)
    def supervisor_select(self, _iOperatorID):
        u""""""
        if QVariant(self.iSupervisorID) == _iOperatorID:
            return
        if not self.stateMap in (self.NOMAP, self.EMPTY):
            if not self.on_change_operator(u'Поверитель ЦСМ'):
                return
        self.iSupervisorID = _iOperatorID.toInt()[0] if _iOperatorID.toInt()[1] else None 
        print 'self.iSupervisorID2=', self.iSupervisorID
        
        self.change_map()
        if _iOperatorID.toInt()[0]:
            self.supervisorSelected.emit(_iOperatorID, QString(self.oHelperOperator.get_fio(_iOperatorID)))
        else:
            self.supervisorSelected.emit(None, QString(u''))
        
    @pyqtSlot(int)
    def asistant_select(self, _iOperatorID):
        u""""""
        if QVariant(self.iAssistantID) == _iOperatorID:
            return
        if not self.stateMap in (self.NOMAP, self.EMPTY):
            if not self.on_change_operator(u'Ассистент'):
                return
        self.iAssistantID = _iOperatorID.toInt()[0] if _iOperatorID.toInt()[1] else None
        self.change_map()
        if _iOperatorID.toInt()[0]:
            self.assistantSelected.emit(_iOperatorID, QString(self.oHelperOperator.get_fio(_iOperatorID)))
        else:
            self.assistantSelected.emit(None, QString(u''))
        
    @pyqtSlot(int)
    def tester_select(self, _iOperatorID):
        u""""""
        if None == _iOperatorID or self.iTesterID == int(_iOperatorID):
            return
        if not self.stateMap in (self.NOMAP, self.EMPTY):
            if not self.on_change_operator(u'Испытатель'):
                return
        self.iTesterID = int(_iOperatorID)
        if self.stateMap == self.NOMAP or self.stateMap == self.EMPTY:
            self.climat_request()
        self.change_map()
        self.testerSelected.emit(_iOperatorID, QString(self.oHelperOperator.get_fio(_iOperatorID)))
        self.supervisor_request()

#    @pyqtSlot()
#    def start(self):
#        if self.stateMap == self.FULL:
#            self.stateMap = self.TESTING
#            self.mapRefresh.emit()
#            self.buttonRefresh.emit()
#
#    @pyqtSlot()
#    def stop(self):
#        if self.stateMap != self.TESTING:
#            return
#        if self.oHelperMap.is_done(self.iMapID):
#            self.stateMap = self.DONE
#        else:
#            self.stateMap = self.FULL
#        self.mapRefresh.emit()
#        self.buttonRefresh.emit()
            
    def map_get_delay_by_serial(self, _iSerialID):
        iMapId = self.oHelperMap.get_incomplit_map_id(self.iStandID, _iSerialID)
        #TODO: Надо избавится от всяких диалогов
        if iMapId and getTrue(None, u'Отложенная тележка, взять целиком?'):
            return iMapId
        else:
            return None

    def map_add(self):
        self.climat_request()
        #24.11.2016
#        return self.oHelperMap.insert(self.iTesterID, self.iAssistantID, self.iSupervisorID, self.iClimatID, self.iStandID)
        a = self.oHelperMap.insert(self.iTesterID, self.iAssistantID, self.iSupervisorID, self.iClimatID, self.iStandID)
        #print '++++++++++++++++++   map_add    self.iMapID=', self.iMapID  
        return a

    def select(self, _iMapID):
        u""""""
        self.iMapID = _iMapID
        if self.oHelperMap.is_empty(self.iMapID):
            self.stateMap = self.EMPTY
        else:
            self.stateMap = self.FULL
        self.selected.emit(self.iMapID)
        self.mapRefresh.emit()
        self.buttonRefresh.emit()

    def map_drag(self, _iTestMapID):
        #TODO: Сейчас если берем отложенную тележку, то пересечиваем все всех операторов
        self.select(_iTestMapID)
        self.change_map()

    @pyqtSlot(int)
    def item_add(self, _iSerialID):
        #print '----------------------------------  item_add   _iSerialID=', _iSerialID, '   self.iMapID=', self.iMapID     #23.11.2016
        #tam 24.11.2016
        self.calc_global.emit()

        iDelayMapID = None
        if self.stateMap == self.NOMAP: #Карты нет 
            #print '+1   item_add    self.iMapID=', self.iMapID  
            iDelayMapID = self.map_get_delay_by_serial(_iSerialID) #Пытаемся получить отложенную карту
            if iDelayMapID: #Выбираем отложенную карту
                self.map_drag(iDelayMapID)
                #tam 24.11.2016
                #print '+2   item_add    self.iMapID=', self.iMapID  
                self.calc_global.emit()
                return
            else: #Создаем новую карту
                self.select(self.map_add())
                #print '+3   item_add    self.iMapID=', self.iMapID  
                 
        if self.oHelperItem.get_id(self.iMapID, _iSerialID): #Такой трансформатор уже есть на тележке
            self.dublicated.emit()
            #print '+4   item_add    self.iMapID=', self.iMapID  
            return
        #print '+5   item_add    self.iMapID=', self.iMapID  
        #TODO: Надо избавится от всяких диалогов
        iDelayMapID = self.oHelperMap.get_incomplit_map_id(self.iStandID, _iSerialID) #Ищем данный трансформатор на отложенной тележке
        if  iDelayMapID and self.iMapID != iDelayMapID and getTrue(None, u'забрать трансформатор с тележки?'):
            itemID = self.oHelperItem.get_id(iDelayMapID, _iSerialID)
            self.oHelperMap.drag_item(itemID, self.iMapID)
            #print '+6   item_add    self.iMapID=', self.iMapID  
        else:
            self.oHelperItem.insert(_iSerialID, self.iMapID)
            #print '+7   item_add    self.iMapID=', self.iMapID  
        self.reset_state()
        #tam 24.11.2016
        self.calc_global.emit()
#        if self.oHelperMap.is_done(self.iMapID):
#            self.stateMap = self.DONE
#        else:
#            self.stateMap = self.FULL
#        self.mapRefresh.emit()
#        self.buttonRefresh.emit()

    @pyqtSlot()
    def reset_state(self):
        u"""ПРоверяем  как поменялось состояние карты, после изсенения итема"""
        if self.oHelperMap.is_empty(self.iMapID):
            self.stateMap = self.EMPTY
        elif self.oHelperMap.is_done(self.iMapID):
            self.stateMap = self.DONE
        else:
            self.stateMap = self.FULL
            self.oHelperMap.set_done(self.iMapID, False)
        self.mapRefresh.emit()
        self.buttonRefresh.emit()
        
    @pyqtSlot(int)
    def clear(self, _iItemID):
        if not self.oHelperMap.is_empty(self.iMapID) and self.oHelperMap.is_done(self.iMapID):
            self.stateMap = self.FULL
        self.mapRefresh.emit()
        self.buttonRefresh.emit()
    
    @pyqtSlot()
    def close(self):
        u""""""
        if self.stateMap == self.EMPTY:
            self.oHelperMap.delete(self.iMapID)
        if self.stateMap == self.DONE:
            self.oHelperMap.set_done(self.iMapID, True)
        self.stateMap = self.NOMAP
        self.iMapID = None
        self.selected.emit(self.iMapID)
        self.mapRefresh.emit()
        self.buttonRefresh.emit()
        self.climat_request()

    @pyqtSlot()
    def climat_request(self):
        u"""Запросить климат"""
        if self.stateMap != self.NOMAP or not self.adStandInfo.NeedClimatLog:
            return
        self.iClimatID = self.oHelpClimat.get_current_id(self.adStandInfo.Room)
#        if not self.iClimatID:
        if not self.iClimatID and self.iTesterID != None and (self.iSupervisorID != None or not self.adStandInfo.EnableSupervisor):
            self.requestClimat.emit()

    @pyqtSlot()
    def supervisor_request(self):
        if(self.iTesterID != None and self.iSupervisorID == None and self.adStandInfo.EnableSupervisor):
            self.requestSupervisor.emit()

    def on_change_operator(self, _sStringNote):
        u"""Изменился оператор в процессе испытания, требуется подтверждение от оператора"""
        #TODO: Надо избавится от всяких диалогов
        return getTrue(None, u'%s будет применен к о всей тележке' % (_sStringNote))

    def change_map(self):
        #print '++++++++++++++++++++++++++   change_map    self.iMapID=', self.iMapID  #23.11.2016
        #tam 24.11.2016
#        self.calc_global.emit()
        
        if self.iMapID:
            self.oHelperMap.change(self.iMapID, self.iTesterID , self.iAssistantID, self.iSupervisorID)

