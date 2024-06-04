#-*- coding: UTF-8 -*-
u"""
Created on 20.06.2012
@author: Anton
"""
from electrolab.app.gost import GOST7746
from electrolab.data import helper
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal
from dpframe.tech.AttrDict import AttrDict

#Флаг глобального состояния 
PAUSE = u'PAUSE'
WORK = u'WORK'

#Флаг состояний обработки данных
LEFTPOINT = u'LEFTPOINT'
FOUNDPOINT = u'FOUNDPOINT' 
RIGHTPOINT = u'RIGHTPOINT'
UNKNOWPOINT = u'UNKNOWPOINT'
DONE = u'DONE'

class CoilVerification(QObject):
    u"""Поверка одной обмотки. Специально выделено в отдельный класс, когда надо будет испытовать отдельные обмотки"""
    cleared = pyqtSignal()
    PointFound = pyqtSignal(int, float, float, float, bool)
    PointEmpty = pyqtSignal()
    PointLeft = pyqtSignal(int, bool)
    PointRight = pyqtSignal(int, bool)
    PointError = pyqtSignal(int, float, float, float, bool, float, float)
    PointErrorAngular = pyqtSignal(int, float, float, float, bool, float)
    PointErrorCurrent = pyqtSignal(int, float, float, float, bool, float)
    NeedCurrentOff = pyqtSignal()
    NeedCurrentOn = pyqtSignal()
#    PointNext = pyqtSignal()
    PointOut = pyqtSignal(int)
    PointQuadro = pyqtSignal()
    TermsCurrentOff = pyqtSignal()
    TermsCurrentOn = pyqtSignal()
    TermsSwithVoltage = pyqtSignal(float)
    TermsSwithLoad = pyqtSignal(float)
    worked = pyqtSignal()
    paused = pyqtSignal()
    proggress = pyqtSignal(float, float, float)
    CoilDone = pyqtSignal()
    

    def __init__(self, _env, _adStandInfo, _iItemID, _iCoilID):
        u""""""
        super(QObject, self).__init__()
        self.env = _env
        self.adStandInfo = _adStandInfo
        self.oKNT05 = self.env.devices.knt05
        self.oHelperChecking = helper.Checking(self.env)
        self.oHelperCoil = helper.Coil(self.env)
        self.iItemID = _iItemID
        self.iCoilID = _iCoilID
        self.pointIndex = 1
        self.cache = None
        self.oGOST = GOST7746(self.env, self.adStandInfo.GOST_ID, self.oHelperCoil.get_class_accuracy(_iCoilID), self.oHelperCoil.get_class_secondload(_iCoilID))
        
        #Флаги
        self.stateWork = PAUSE # Может принимать WORK, PAUSE
        self.statePoint = UNKNOWPOINT # Может принимать LEFTOFPOINT, FOUNDPINT, LEFTOFPOINT, UNKNOWPOINT
        self.bStateError = False # Может принимать True False
        self.bNeedCurrentOff =  False # Может принимать True False
        self.bCurrentIsOff = True
        
        self.quadroLoad = None 
        self.silentThreshold = 0.8 #порог "тишины", ток ниже - считается 0
        self.silentQuadriloadThreshold = 3 #порог "тишины", ток ниже - считается 0
         
        self.pause()
        self.set_point_unknow()
        self.info = self.oHelperCoil.get_check_terms(self.iCoilID)

#        self.oKNT05.SetHandler(self.recive_data)
#        self.recived.connect(self.process_data)
        
#        self.fill_existing_points()

#    def recive_data(self, _oData):
#        #TODO: Это сделано чтобы работать через сигналв Qt иначе глюки в интерфейсе, сканер живет в отдельном потоке
#        self.recived.emit(_oData)

    def clear_error(self, _errorPointIndex):
        if _errorPointIndex == 0 or _errorPointIndex == None:
            self.clear()
            return
        point = self.oGOST.get_point_by_index(_errorPointIndex - 1)
        self.oHelperChecking.clear_all_next_points(self.iItemID, self.iCoilID, point.I, point.quadroLoad)
        #self.set_point_unknow()
        self.bStateError = False
        self.cache.clear_all_next_point(point.I)
        self.pointIndex = _errorPointIndex - 1 
        self.cleared.emit()

    def clear(self):
        self.oHelperChecking.clear_coil(self.iItemID, self.iCoilID)
        self.set_point_unknow()
        self.bStateError = False
        self.pointIndex = 1
        self.cache.clear()
        self.cleared.emit()
        
    def fill_existing_points(self):
        u"""Заполнить существующие точки значениями из БД. Это происходит если встали уже на испытанную обмотку"""
        self.cache = self.oHelperChecking.get_all_points(self.iItemID, self.iCoilID)
        lastPointIndex = 0
        for self.pointIndex in self.oGOST.get_point_list():
            self.statePoint = UNKNOWPOINT
            pointDescription = self.oHelperChecking.get_point(
                                                            self.iItemID
                                                            , self.iCoilID
                                                            , self.oGOST.get_point_by_index(self.pointIndex).I
                                                            , self.oGOST.get_point_by_index(self.pointIndex).quadroLoad
                                                            )
            if None == pointDescription: return #нет данных по точке в БД
            #TODO: ПОхоже это лишнее телодвижение self.oGOST.get_point_list()[self.pointIndex].bFound = True
            if None not in pointDescription:
                self.set_point_found(self.pointIndex, pointDescription[0], pointDescription[1], pointDescription[2], bool(self.oGOST.get_point_by_index(self.pointIndex).quadroLoad))
                lastPointIndex = self.pointIndex  
            if pointDescription[0] and self.oGOST.is_error_current(pointDescription[0], self.pointIndex, pointDescription[2]):
                # Ошибка - превышена токовая погрешность
                self.PointErrorCurrent.emit(self.pointIndex, pointDescription[0], pointDescription[1], pointDescription[2], bool(self.oGOST.get_point_by_index(self.pointIndex).quadroLoad), 0)
            if pointDescription[0] and self.oGOST.is_error_angular(pointDescription[0], self.pointIndex, pointDescription[1]):
                # Ошибка - превышена угловая погрешность 
                self.PointErrorAngular.emit(self.pointIndex, pointDescription[0], pointDescription[1], pointDescription[2], bool(self.oGOST.get_point_by_index(self.pointIndex).quadroLoad), 0)
            if self.oGOST.pint_count() == self.pointIndex:
                u"""Больше нечего обрабатывать, все точки найдены, ток выключен"""
                if self.statePoint == FOUNDPOINT:
                    self.set_point_DONE()
                elif  self.statePoint == UNKNOWPOINT:
                    self.PointEmpty.emit()

        self.pointIndex = min(lastPointIndex + 1, self.pointIndex)
        self.terms_need_swith_voltage()
        self.terms_need_swith_load()

    def getThreshold(self):
        u"""Порог тишины, для первой всегда маленький, для последующих не найденных - большой. Сделано для простоты переключения на поиска четвертной нагрузки"""
        if 1 != self.pointIndex and self.statePoint != FOUNDPOINT:
            return self.silentQuadriloadThreshold #Большой
        else:
            return self.silentThreshold #Маленький

    @pyqtSlot(object)
    def process_data(self, _oData):
        u"""Обработка данных с КНТ-05 переключает состояния вызовом методов set_point_left; set_point_right; pause"""
        if not _oData.bParsed: return #битые данные - игнорим
        self.proggress.emit(_oData.I, _oData.A, _oData.P)
        if PAUSE == self.stateWork: return #на паузе - игнорим
        
        if _oData.I <= self.getThreshold():
            #порог тишины, считаем что латр выключен.
            self.terms_current_is_off() 
            self.terms_need_current_on()
            self.set_point_left()
            return
        else:
            self.terms_current_is_on()
        if self.bNeedCurrentOff: return #Надо выключмить ток - игнорим
        if DONE == self.stateWork: 
            return #на паузе - игнорим

        point = None
        bFound = self.oGOST.point_is_found(_oData.I, self.pointIndex)
        quadroLoad = self.oGOST.get_point_by_index(self.pointIndex).quadroLoad

        if bFound:
            point = self.oGOST.get_point_by_index(self.pointIndex).I
        else:
            point = None
        #TODO:Может перенести кеширование в хелпер? 
        if self.cache.exists(_oData.I, quadroLoad): #Запись с таким током уже есть
            return
        
        if point and self.cache.is_best(point, _oData.I, quadroLoad):
            self.oHelperChecking.clear_point(self.iItemID, self.iCoilID, point, quadroLoad)
        else:
            point = None
            
        self.oHelperChecking.insert(
                                     self.iItemID
                                     , self.iCoilID
                                     , _oData
                                     , point
                                     , quadroLoad
                                     )#TODO: А надо ли писать, что ошибка была???? bAngularError, bCurrentError - вот флажки с ошибкой

        
        if bFound:
            # Нашли точку
            iErrorCurrent = self.oGOST.is_error_current(_oData.I, self.pointIndex, _oData.A)
            iErrorAngular = self.oGOST.is_error_angular(_oData.I, self.pointIndex, _oData.P)
            
            if iErrorCurrent or iErrorAngular:
                # Ошибка - превышена погрешность
                self.set_point_error(self.pointIndex, _oData.I, _oData.P, _oData.A, bool(quadroLoad), iErrorAngular, iErrorCurrent)
            else:
                # Нет ошибок
                self.set_point_found(self.pointIndex, _oData.I, _oData.P, _oData.A, bool(quadroLoad))
                
            if iErrorCurrent:
                # Детализирующая ошибка - превышена токовая погрешность
                self.PointErrorCurrent.emit(self.pointIndex, _oData.I, _oData.P, _oData.A, bool(quadroLoad), iErrorCurrent)
                
            if iErrorAngular:
                # Детализирующая ошибка - превышена угловая погрешность 
                self.PointErrorAngular.emit(self.pointIndex, _oData.I, _oData.P, _oData.A, bool(quadroLoad), iErrorAngular)

            self.point_next()
        else:
                
            if self.oGOST.on_the_left_of_point(_oData.I, self.pointIndex):
                # Не нашли точку
                self.set_point_left()
                
            if self.oGOST.on_the_right_of_point(_oData.I, self.pointIndex):
                # Пропустили точку
                self.set_point_right()
            
    
# Состояния работы ########################################################
    @pyqtSlot()
    def work(self):
        if self.stateWork == WORK:
            return
        self.stateWork = WORK
        self.worked.emit()
        if self.oKNT05.__class__.__name__ == u'KNT05_forTest':#Работа с эмулятором и реальным прибором отличается. Прибор включен всегда
            self.oKNT05.SetEnabled(True)
    
    @pyqtSlot()
    def pause(self):
        if self.stateWork == PAUSE:
            return
        self.stateWork = PAUSE
#        self.set_point_unknow()
        self.paused.emit()
        if self.oKNT05.__class__.__name__ == u'KNT05_forTest' :#Работа с эмулятором и реальным прибором отличается. Прибор включен всегда
            self.oKNT05.SetEnabled(False)
        
    def is_work(self):
        return self.stateWork == WORK 

    def is_done(self):
        return self.statePoint == DONE 

# Состояния обработки данных ########################################################
    def set_point_unknow(self):
        u""""""
        if self.statePoint != UNKNOWPOINT:
            self.statePoint = UNKNOWPOINT
#            self.PointEmpty.emit()
        
    def set_point_found(self, _pointIndex , _I, _P, _A, _isQuadroLoad):
        if self.statePoint != FOUNDPOINT:
            self.statePoint = FOUNDPOINT
            self.PointFound.emit(_pointIndex , _I , _P , _A , bool(_isQuadroLoad))
    
    def set_point_left(self):
        if DONE == self.statePoint:              
            return
        if self.statePoint != LEFTPOINT:
            self.statePoint = LEFTPOINT
            self.PointLeft.emit(self.oGOST.get_point_by_index(self.pointIndex).I, bool(self.oGOST.get_point_by_index(self.pointIndex).quadroLoad))
         
    def set_point_right(self):
        if DONE == self.statePoint:              
            return
        if self.statePoint != RIGHTPOINT:
            self.statePoint = RIGHTPOINT
            self.PointRight.emit(self.oGOST.get_point_by_index(self.pointIndex).I, bool(self.oGOST.get_point_by_index(self.pointIndex).quadroLoad))
        
    def set_point_error(self, _pointIndex, _I, _P, _A, _quadroLoad, _iErrorAngular, _iErrorCurrent):
        self.pause()
        if not self.bStateError:
            self.bStateError = True
            self.PointError.emit(_pointIndex, _I, _P, _A, _quadroLoad, _iErrorAngular, _iErrorCurrent)
            
    def set_point_DONE(self):
        u""""""
        if self.statePoint != DONE and not self.bStateError:
            self.statePoint = DONE
            self.CoilDone.emit()
            self.terms_need_current_off()
        
        
# Состояния ожидания переключений латра (и реле?) ########################################
    def terms_current_is_off(self):
        #Если латр отключили
        if not self.bCurrentIsOff:
            self.bCurrentIsOff = True
            self.TermsCurrentOff.emit()
            if self.statePoint == DONE: 
                self.PointOut.emit(self.iCoilID)
    
    def terms_current_is_on(self):
        #Если латр отключили
        if self.bCurrentIsOff:
            self.bCurrentIsOff = False
            self.TermsCurrentOn.emit()
    
    def terms_need_swith_voltage(self):
        self.TermsSwithVoltage.emit(self.info.SecondCurrent)
    
    def terms_need_swith_load(self):
        #тут щелкаем релюхой
        quadroLoad = self.oGOST.get_point_by_index(self.pointIndex).quadroLoad
        #Надо учитывать необходисость четвертной нагрузки
        self.TermsSwithLoad.emit(quadroLoad or self.info.SecondLoad)
    
    def terms_need_current_off(self):
        #Требуется отключить ток (вывести латр на ноль)
        if not self.bNeedCurrentOff:
            self.bNeedCurrentOff = True
            self.NeedCurrentOff.emit()
    
    def terms_need_current_on(self):
        #Требуется подать ток (перевести латр с нуля)
        if self.bNeedCurrentOff:
            self.bNeedCurrentOff = False
            self.NeedCurrentOn.emit()
            self.terms_need_swith_voltage()
            self.terms_need_swith_load()
    
# Состояния перехода по точкам ########################################################
    def point_quadro(self):
        self.terms_need_current_off()
        self.PointQuadro.emit()

    def point_next(self):
        if self.oGOST.pint_count() <= self.pointIndex:
            u"""Больше нечего обрабатывать, все точки найдены, ток выключен"""
            self.set_point_DONE()
        else:
            if self.statePoint != FOUNDPOINT:
                return #Переход делаем, если только данные были найденй
            self.pointIndex += 1
            self.set_point_unknow()
            if self.oGOST.get_point_by_index(self.pointIndex).quadroLoad:
                self.point_quadro()
#            self.PointNext.emit()

