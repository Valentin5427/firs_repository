#coding=UTF-8
u"""
Created on 17.07.2012
#
@author: Knur
desc:Общий класс для форм операций. 
"""
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import QVariant, QDateTime
from dpframe.tech.AttrDict import AttrDict

class Point(object):
    u""" Часть записи таблицы № 8 ГОСТ 7746-2001 описывающая значения контрольной точки"""
    def __init__(self, _I, _ALeftLimit,  _ARightLimit, _PLeftLimit, _PRightLimit, _threshold, _quadroLoad = None):
        u"""  """
        self.I = _I
        self.ALeftLimit = _ALeftLimit
        self.ARightLimit = _ARightLimit
        self.PLeftLimit = _PLeftLimit
        self.PRightLimit = _PRightLimit
        self.quadroLoad = _quadroLoad
        self.bFound = False
        self.threshold = _threshold

class CheckingCach(object):
    u"""Кешь результатов испытаний, нужен для уменьшения кол-ва запросов к БД"""
    
    def __init__(self):
        self.cache = AttrDict()
        self.cacheQuadro = AttrDict()
        
    def add(self, _I, _ID, _P, _A, _Quadro, _Point):
        if _Quadro:
            self.cacheQuadro[_I] = AttrDict({u'ID':_ID, u'P':_P, u'A':_A, u'Quadro': _Quadro, u'Point': _Point})
        else:
            self.cache[_I] = AttrDict({u'ID':_ID, u'P':_P, u'A':_A, u'Quadro': _Quadro, u'Point': _Point})
        
    def exists(self, _I, _Quadro):
        if _Quadro:
            return self.cacheQuadro.has_key(_I)
        else:
            return self.cache.has_key(_I)
    
    def clear(self):
        self.cache = AttrDict()
        self.cacheQuadro = AttrDict()
        
    def clear_all_next_point(self, _Point):
        minI = None 
        for I in self.cache.keys():
            if(self.cache[I].Point == _Point):
                minI = I
                break 
        for key in self.cache.keys():
            if(key > minI):
                self.cache.pop(key)
        if minI != None:
            self.cacheQuadro = AttrDict()
        
    def is_best(self, _Point, _I, _Quadro):
        if  _Quadro:
            actualCach = self.cacheQuadro
        else:
            actualCach = self.cache
        if not len(actualCach):
            return True
        for data in actualCach.itervalues():
            if _Point == data.Point:
                return abs(_Point - _I) < abs(_Point - data.I)
        return True 

    def get_point(self, _point, _Quadro):
        pass


class Climat(object):
    u"""Колекция методов для работы с журналом окружающей среды."""
    
    def __init__(self, _env):
        self.env = _env

    def get_current_id(self, _iRoomID):
        u"""Получить ID текущей, действительной записи"""
        sQuery = u"""
                    select 
                        cli.id as itemID
                    from 
                        climat cli
                    where
                        (case
                            when time '17:00' < localtime then current_date + time '17:00'
                            when time '13:00' < localtime then current_date + time '13:00'
                            when time '08:00' < localtime then current_date + time '08:00'
                            when time '00:00' < localtime then current_date + time '00:00'
                        end) < cli.lastupdate
                        and cli.room = :iRoomID
                    ;
                    """
        #TODO: Добавить стенд в климат
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iRoomID', QVariant(_iRoomID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'itemID').toInt()[0])
        else:
            return None

    def insert(self, _iRoomID, _iOperatorID, _dTemperature, _dHumidity, _dPressure):
        sQuery = u"""insert into climat
                    (
                    room
                    , operator
                    , temperature
                    , humidity
                    , pressure
                    , lastupdate                    
                    )
                    values
                    (
                        :iRoomID
                        , :iOperatorID
                        , :dTemperature
                        , :dHumidity
                        , :dPressure                    
                        , CURRENT_TIMESTAMP
                    ) 
                    returning ID;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iRoomID', QVariant(_iRoomID))
        oQuery.bindValue(u':iOperatorID', QVariant(_iOperatorID))
        oQuery.bindValue(u':dTemperature', QVariant(_dTemperature))
        oQuery.bindValue(u':dHumidity', QVariant(_dHumidity))
        oQuery.bindValue(u':dPressure', QVariant(_dPressure))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'ID').toInt()[0])
        else:
            return None 


class Operator(object):
    u"""Колекция методов для работы с операторами"""
    
    def __init__(self, _env):
        self.env = _env
        
    def get_fio(self, _iOperId):
        u""""""
        sQuery = u"""select fio 
                    from operator 
                    where id = :iOperId;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iOperId', QVariant(_iOperId))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            #Не более одной записи
            return unicode(oQuery.record().value(u'fio').toString())


class SerialNumber(object):
    u"""Колекция методов для работы с серийными номерами."""
    
    def __init__(self, _env):
        self.env = _env

    def get_id(self, _yar, _number):
        print(645758,_yar,_number)
        u"""Найти ID серийника, ID трансформатора, FullName трансформатора по году и номеру трансформатора"""
        returnValue = AttrDict({u'id':None, u'transformer':None, u'fullname':None, })
        sQuery = u"""select sn.id, sn.transformer, tsf.fullname 
                    from serial_number sn 
                    left join transformer tsf on tsf.id = sn.transformer  
                    where sn.makedate = :yar and sn.serialnumber = :number;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':yar', QVariant(_yar))
        oQuery.bindValue(u':number', QVariant(_number))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            #Не более одной записи
            returnValue.id = int(oQuery.record().value(u'id').toInt()[0])
            returnValue.transformer = int(oQuery.record().value(u'transformer').toInt()[0])
            returnValue.fullname = unicode(oQuery.record().value(u'fullname').toString())
        return returnValue

    def get_info(self, _id):
        u"""Найти ID серийника, ID трансформатора, FullName трансформатора по году и номеру трансформатора"""
        returnValue = AttrDict({u'makedate':None, u'serialnumber':None, u'transformer':None})
        sQuery = u"""select 
                        sn.makedate
                        , sn.serialnumber 
                        , sn.transformer
                    from 
                        serial_number sn 
                    where 
                        sn.id = :id
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':id', QVariant(_id))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            #Не более одной записи
            returnValue.makedate = int(oQuery.record().value(u'makedate').toInt()[0])
            returnValue.serialnumber = int(oQuery.record().value(u'serialnumber').toInt()[0])
            returnValue.transformer = int(oQuery.record().value(u'transformer').toInt()[0])
        return returnValue


class TestMap(object):
    u"""Колекция методов для работы с картой тестирования."""
    
    def __init__(self, _env):
        self.env = _env

    def insert(self, _iOperatorID, _iAssistantID, _iVeriferID, _iClimatID, _iStandID):
        #TODO: Добавить асистента
        sQuery = u"""insert into test_map
                    (
                        operator
                        , assistant
                        , supervisor
                        , climat
                        , stand
                        , accepted
                        , createdatetime
                    )
                    values
                    (
                        :iOperatorID
                        , :iAssistantID
                        , :iVeriferID
                        , :iClimatID
                        , :iStandID
                        , False                        
                        , CURRENT_TIMESTAMP
                    ) 
                    returning ID;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iOperatorID', QVariant(_iOperatorID))
        oQuery.bindValue(u':iAssistantID', QVariant(_iAssistantID))
        oQuery.bindValue(u':iVeriferID', QVariant(_iVeriferID))
        oQuery.bindValue(u':iStandID', QVariant(_iStandID))
        oQuery.bindValue(u':iClimatID', QVariant(_iClimatID))
        
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'ID').toInt()[0])
        else:
            return None 

    def change(self, _iTestMapID, _iOperatorID, _iAssistantID, _iVeriferID):
        sQuery = u"""update test_map
                     set
                         operator = :iOperatorID 
                         , assistant = :iAssistantID
                         , supervisor = :iVeriferID
                     where
                         id = :iTestMapID
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)

        oQuery.bindValue(u':iAssistantID', QVariant(_iAssistantID))
        oQuery.bindValue(u':iVeriferID', QVariant(_iVeriferID))
        oQuery.bindValue(u':iTestMapID', QVariant(_iTestMapID))
        oQuery.bindValue(u':iOperatorID', QVariant(_iOperatorID))
        
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def delete(self, _iItemID):
        sQuery = u'delete from test_map where id = :itemID'
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':itemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def is_empty(self, _testMapID):
        u"""Карта пустая"""
        sQuery = u"""select id from item where test_map = :test_map"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return not oQuery.next() 
    
    def drag_item(self, _item, _testMap):
        u"""Перетащить транс _item на тележку _testMap"""
        sQuery = u"""update item
                    set test_map = :test_map
                    where 
                        id =:item 
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':test_map', QVariant(_testMap))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return True

    def get_incomplit_map_id(self, _standID, _serNumID):
        u"""Получить ID отложенной карты испытания по _serNumID"""
        sQuery = u"""
                    select 
                        tm.id
                    from 
                        item
                    left join
                        test_map tm
                    on
                        tm.id = item.test_map
                    where 
                        item.serial_number = :serial_number
                        and tm.stand = :standID 
                        and tm.accepted = False
                    order by
                        id desc
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':serial_number', QVariant(_serNumID))
        oQuery.bindValue(u':standID', QVariant(_standID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'id').toInt()[0])
        else:
            return None 

    def exists_serial_in_map(self, _serNumID, _testMapID):
        u"""Проверка наличия серийного номера в таблице item"""
        sQuery = u"""select id from item where test_map = :test_map and serial_number = :serial_number"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':serial_number', QVariant(_serNumID))
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.next() 

#TODO: Загадочная хрень, наверно не нужна
    def exists_complit_item(self, _testMapID):
        u"""Проверка наличия протестированных трансформаторов"""
        sQuery = u"""select id from item where test_map = :test_map and istested"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.next() 

    def is_done(self, _testMapID):
        u"""Проверка завершенности испытаний"""
        sQuery = u"""select id from item where not istested and defect is null and test_map = :test_map """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return not oQuery.next() 

    def set_done(self, _testMapID, _isTester = True):
        u"""Пометить карту как испытанную"""
        sQuery = u"""update test_map set accepted = :tested where id = :test_map """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.bindValue(u':tested', QVariant(_isTester))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return not oQuery.next() 

    def set_is_tested(self, _item, _value):
        u"""Пометить трансформатор как протестированный"""
        sQuery = u"""update item
                    set isTested = :value
                    where 
                        id = :item 
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':value', QVariant(_value))
        oQuery.bindValue(u':item', QVariant(_item))
        return oQuery.exec_()

class Item(object):
    u"""Колекция методов для работы с трансформаторами на тележке."""
    
    def __init__(self, _env):
        self.env = _env

    def insert(self, _serialNumberID, _testMapID):
        sQuery = u"""insert into item
                    (
                        serial_number
                        , test_map
                        , istested
                        , createdatetime
                    )
                    values
                    (
                        :serialNumberID
                        , :testMapID
                        , false
                        , CURRENT_TIMESTAMP
                    ) 
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':serialNumberID', QVariant(_serialNumberID))
        oQuery.bindValue(u':testMapID', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def delete(self, _iItemID):
        sQuery = u'delete from item where id = :itemID'
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':itemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        
    def set_defect(self, _iItemID, _iDefectID):
        sQuery = u'update item set defect = :iDefectID, acceptdatetime = CURRENT_TIMESTAMP where id = :itemID'
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':itemID', QVariant(_iItemID))
        oQuery.bindValue(u':iDefectID', QVariant(_iDefectID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
    
    def set_isTested(self, _iItemID, _bIsTested):        
        sQuery = u'update item set isTested = :bIsTested, acceptdatetime = CURRENT_TIMESTAMP where id = :itemID'
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':itemID', QVariant(_iItemID))
        oQuery.bindValue(u':bIsTested', QVariant(_bIsTested))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def get_id(self, _testMapID, _serNumID):
        u"""Получить ID Item-а для трансформатора с _serNumID на тележке _testMapID"""
        sQuery = u"""
                    select 
                        item.id as itemID
                    from 
                        item
                    where 
                        item.serial_number = :serial_number
                        and item.test_map = :test_map
                    order by 
                        item.id desc
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':serial_number', QVariant(_serNumID))
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'itemID').toInt()[0])
        else:
            return None

    def get_next_id(self, _testMapID, _iCurentItemID):
        u"""Получить ID следующего Item-а для трансформатора на тележке _testMapID"""
        sQuery = u"""
                    select 
                        min(item.id) as itemID
                    from 
                        item
                    where 
                        item.id > :iCurentItemID
                        and item.test_map= :test_map
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iCurentItemID', QVariant(_iCurentItemID))
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'itemID').toInt()[0])
        else:
            return None
        
    def get_prev_id(self, _testMapID, _iCurentItemID):
        u"""Получить ID предыдущего Item-а для трансформатора на тележке _testMapID"""
        sQuery = u"""
                    select 
                        max(item.id) as itemID
                    from 
                        item
                    where 
                        item.id < :iCurentItemID
                        and item.test_map = :test_map
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iCurentItemID', QVariant(_iCurentItemID))
        oQuery.bindValue(u':test_map', QVariant(_testMapID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'itemID').toInt()[0])
        else:
            return None
        
    def get_fields(self, _iItemID): 
        u""""""
        returnValue = AttrDict({u'istested':None, u'defect':None, u'serial_number':None, u'test_map':None})
        sQuery = u"""select istested, defect, serial_number, test_map from item where id = :iItemID ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            #Не более одной записи
            returnValue.istested = bool(oQuery.record().value(u'istested').toBool())
            returnValue.defect = int(oQuery.record().value(u'defect').toInt()[0])
            returnValue.serial_number = unicode(oQuery.record().value(u'serial_number').toInt()[0])
            returnValue.test_map = int(oQuery.record().value(u'test_map').toInt()[0])
        return returnValue

    def is_done(self, _iItemID):
        u"""стоит метка 'Испытан'"""
        sQuery = u"""select id from item where istested and defect is null and id = :iItemID ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.next() 

    def is_clear(self, _iItemID):
        u"""Испытание не завершено"""
        sQuery = u"""select id from item where not istested and defect is null and id = :iItemID ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.next() 

    def is_fail(self, _iItemID):
        u"""Проверка завершенности испытаний"""
        sQuery = u"""select id from item where defect is not null and id = :iItemID ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.next() 

    def get_coils(self, _iItemID):
        u"""Получить список обмоток"""
        coilList = []
        sQuery = u"""
                    select 
                        cl.id
                    from 
                        item it
                    inner join 
                        serial_number sn
                    on
                        it.id  = :iItemID
                        and it.serial_number = sn.id
                    inner join 
                        coil cl
                    on
                        cl.transformer = sn.transformer
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        while oQuery.next():
            coilList.append(oQuery.record().value(u'ID').toInt()[0])
        return coilList
        


class Checking(object):
    u"""Колекция методов для работы с обмотками."""
    
    def __init__(self, _env):
        self.env = _env
        self.oItemHelper = Item(_env)
        self.oMapHelper = TestMap(_env)

    def get_point(self, _item, _coil, _point, _QuadroLoad):
        u"""Получить точку"""
        #TODO: переделать на кешь
        sQuery = u"""select 
                        ch.ID
                        , ch.I
                        , ch.P
                        , ch.A
                    from checking as ch 
                    where 
                        ch.item =:item 
                        and ch.coil = :coil 
                        and ch.point = :point
                        and coalesce(ch.quadroload, 0) = %s  
                    ;""" % (_QuadroLoad or 0)
        #Это пиздец, нельзя параметры использовать в нутри функций. coalesce(:point, 0) - неработает. В пизду QSql
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':coil', QVariant(_coil))
        oQuery.bindValue(u':point', QVariant(_point))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            #Не более одной записи
            id = int(oQuery.record().value(u'id').toInt()[0])
            I = oQuery.record().value(u'I').toDouble()[0]
            P = oQuery.record().value(u'P').toDouble()[0]
            A = oQuery.record().value(u'A').toDouble()[0]
            return I , P, A
        else:
            return None, None, None

    def get_all_points(self, _item, _coil):
        u"""Получить точку"""
        cache = CheckingCach()
        sQuery = u"""select 
                        ch.ID
                        , ch.I
                        , ch.P
                        , ch.A
                        , ch.QuadroLoad
                        , ch.Point
                    from checking as ch 
                    where 
                        ch.item =:item 
                        and ch.coil = :coil 
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':coil', QVariant(_coil))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        while oQuery.next():
            ID = oQuery.record().value(u'ID').toInt()[0]
            I = oQuery.record().value(u'I').toDouble()[0]
            P = oQuery.record().value(u'P').toDouble()[0]
            A = oQuery.record().value(u'A').toDouble()[0]
            Quadro = oQuery.record().value(u'Quadro').toDouble()[0]
            Point = oQuery.record().value(u'Point').toInt()[0]
            cache.add(I, ID, P, A, Quadro, Point)
        return cache

    def insert(self, _item, _coil, _data, _point = None, _quadroLoad = None):
        u"""добавить запись в checking"""
        sQuery = u"""insert into checking
                    (
                        item
                        , coil
                        , a
                        , p
                        , i
                        , n
                        , f
                        , k
                        , chektimestamp
                        , point
                        , quadroload
                    )
                    values
                    (
                        :item
                        , :coil
                        , :a
                        , :p
                        , :i
                        , :n
                        , :f
                        , :k
                        , CURRENT_TIMESTAMP
                        , :point
                        , :quadroload
                    ) 
                    ;"""
        #Это пиздец, нельзя параметры использовать в нутри функций. coalesce(:point, 0) - неработает. В пизду QSql
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':coil', QVariant(_coil))
        oQuery.bindValue(u':a', QVariant(_data.A))
        oQuery.bindValue(u':p', QVariant(_data.P))
        oQuery.bindValue(u':i', QVariant(_data.I))
        oQuery.bindValue(u':n', QVariant(_data.N))
        oQuery.bindValue(u':f', QVariant(_data.F))
        oQuery.bindValue(u':k', QVariant(_data.K))
        oQuery.bindValue(u':point', QVariant(_point))
        oQuery.bindValue(u':quadroLoad', QVariant(_quadroLoad))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def clear_point(self, _item, _coil, _point, _QuadroLoad):
        u"""Убрать метку контрольной точки (делается, если нашли лучше)"""
        sQuery = u"""update checking
                    set point = Null
                    where 
                        item =:item 
                        and coil = :coil 
                        and point = :point
                        and coalesce(quadroload, 0) = %s  
                    ;""" % (_QuadroLoad or 0)
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':coil', QVariant(_coil))
        oQuery.bindValue(u':point', QVariant(_point))
        return oQuery.exec_()

    def clear_all_next_points(self, _item, _coil, _point, _QuadroLoad):
        u"""Очистить данные после указанной точки. Используется при очистке ошибок"""
        sQuery = u"""delete from checking
                    where 
                        item = %s 
                        and coil = %s 
                        and id > (
                                select 
                                    goodpoint.id
                                from
                                    checking as goodpoint
                                where
                                    goodpoint.item = %s 
                                    and goodpoint.coil = %s 
                                    and goodpoint.point = %s
                                    and coalesce(goodpoint.quadroload, 0) = %s
                                )
                    """ % (_item, _coil, _item, _coil, _point, _QuadroLoad or 0)
        oQuery = QSqlQuery(self.env.db)
        #oQuery.prepare(sQuery)
        #oQuery.bindValue(u':item', QVariant(_item))
        #oQuery.bindValue(u':coil', QVariant(_coil))
        #oQuery.bindValue(u':item1', QVariant(_item))
        #oQuery.bindValue(u':coil1', QVariant(_coil))
        #oQuery.bindValue(u':point', QVariant(_point))
        oQuery.exec_(sQuery)
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def clear_coil(self, _item, _coil):
        u"""Очистить результаты испытаний для обмотки"""
        sQuery = u"""delete from checking
                    where 
                        item =:item 
                        and coil = :coil 
                    ;"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':item', QVariant(_item))
        oQuery.bindValue(u':coil', QVariant(_coil))
        if oQuery.exec_():
            if oQuery.lastError().isValid():
                raise Exception(oQuery.lastError().text())
            self.oItemHelper.set_isTested(_item, False)
            record = self.oItemHelper.get_fields(_item)
            self.oMapHelper.set_is_tested(record.test_map, False)

    def is_clear(self, _iItemID, _iCoilID):
        u"""Испытания не было"""
        sQuery = u"""select 
                        ch.ID
                    from 
                        checking as ch 
                    where 
                        ch.item =:iItemID 
                        and ch.coil = :iCoilID 
                    ;"""

        
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iItemID', QVariant(_iItemID))
        oQuery.bindValue(u':iCoilID', QVariant(_iCoilID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return not oQuery.next() 



class Coil(object):
    u"""Колекция методов для работы с обмотками."""
    
    def __init__(self, _env):
        self.env = _env
        self.oChecking = Checking(_env)

    def get_check_terms(self, _CoilID):
        u"""Получить условия испытаний"""
        sQuery = u"""
                    select 
                        cl.SecondLoad
                        , cl.PrimaryCurrent
                        , cl.SecondCurrent
                        , cl.ClassAccuracy
                        , cl.CoilNumber
                        , cl.Tap
                        , tr.ShortName
                        , cl.AmpereTurn
                    from 
                        coil cl
                    left join
                        transformer tr
                    on
                        tr.id = cl.transformer
                    where 
                        cl.id = :CoilID
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':CoilID', QVariant(_CoilID))
        oQuery.exec_()
        if oQuery.next():
            return AttrDict(
                        {
                            u'SecondLoad': oQuery.record().value(u'SecondLoad').toDouble()[0]
                            , u'PrimaryCurrent': oQuery.record().value(u'PrimaryCurrent').toInt()[0]
                            , u'SecondCurrent': oQuery.record().value(u'SecondCurrent').toInt()[0]
                            , u'ClassAccuracy': oQuery.record().value(u'ClassAccuracy').toString()
                            , u'CoilNumber': oQuery.record().value(u'CoilNumber').toInt()[0]
                            , u'Tap': oQuery.record().value(u'Tap').toInt()[0]
                            , u'ShortName': oQuery.record().value(u'ShortName').toString()
                            , u'AmpereTurn': oQuery.record().value(u'AmpereTurn').toInt()[0]
                        }
                    )
        else:
            return None

    def get_class_accuracy(self, _coilID):
        u""" Получить класс тосчности"""
        sQuery = u"""select cl.ClassAccuracy from coil as cl where cl.id = :coilID"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':coilID', QVariant(_coilID))
        oQuery.exec_()
        if oQuery.next():
            return unicode(oQuery.record().value(u'ClassAccuracy').toString())
        else:
            return None

    def get_class_secondload(self, _coilID):
        u""" Получить четвертную нагрузку"""
        sQuery = u"""select cl.SecondLoad from coil as cl where cl.id = :coilID"""
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':coilID', QVariant(_coilID))
        oQuery.exec_()
        if oQuery.next():
            return oQuery.record().value(u'SecondLoad').toDouble()[0]
        else:
            return None
 
    def get_next_id(self, _iCoilID):
        sQuery = u"""
                    select
                        ID
                    from
                        coil cl
                    inner join
                        (
                        select
                            min(cl.coilNumber * 100 + cl.tap) as coilandtape
                        from
                            coil cl
                        where
                            cl.transformer = (select prevcl.transformer from coil prevcl where prevcl.id = :iCoilID1)
                            and cl.coilNumber * 100 + cl.tap > (select prevcl.coilNumber * 100 + prevcl.tap from coil prevcl where prevcl.id = :iCoilID2)
                            and cl.id != :iCoilID3
                        ) as prevcl
                    on
                        prevcl.coilandtape = cl.coilNumber * 100 + cl.tap
                        and cl.transformer = (select prevcl.transformer from coil prevcl where prevcl.id = :iCoilID4)
                    ;
                    """

        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iCoilID1', QVariant(_iCoilID))
        oQuery.bindValue(u':iCoilID2', QVariant(_iCoilID))
        oQuery.bindValue(u':iCoilID3', QVariant(_iCoilID))
        oQuery.bindValue(u':iCoilID4', QVariant(_iCoilID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'ID').toInt()[0])
        else:
            return None

class Stand(object):
    u"""Колекция методов для работы с конфигурацией."""
    
    def __init__(self, _env):
        self.env = _env

    def get_id(self, _sHostname):
        u"""Получить ID текущей, действительной записи"""
        sQuery = u"""
                    select 
                        stnd.id as standID
                    from 
                        stand stnd
                    where
                        stnd.hostname = :sHostname
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':sHostname', QVariant(_sHostname))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next(): 
            return int(oQuery.record().value(u'standID').toInt()[0])
        else:
            #raise Exception(u'Not configured stand for host {0}'.format(_sHostname))
            return None

    def get_info(self, _iStandID):
        u"""Найти ID серийника, ID трансформатора, FullName трансформатора по году и номеру трансформатора"""
        returnValue = AttrDict({
                                u'NeedClimatLog':None
                                , u'room':None
                                , u'EnableSupervisor':None
                                , u'EnableAssistant':None
                                , u'SingleItem':None
                                , u'GOST_ID':None
                                , u'ID':None
                                , u'FullName':None
                                , u'useAmpereTurn':None
                                , u'SupervisorReport':None
                                , u'CheckReport':None
                                , u'TicketMatrix':None
                                })
        sQuery = u"""
                    select 
                        stnd.id
                        , stnd.NeedClimatLog
                        , stnd.room
                        , stnd.EnableSupervisor
                        , stnd.EnableAssistant
                        , stnd.SingleItem
                        , stnd.gost_id
                        , stnd.FullName
                        , stnd.useAmpereTurn
                        , stnd.SupervisorReport
                        , stnd.CheckReport
                        , stnd.TicketMatrix
                    from
                        stand stnd
                    where
                        stnd.id = :iStandID
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iStandID', QVariant(_iStandID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if 1 == oQuery.size() and oQuery.next():
            returnValue.NeedClimatLog = bool(oQuery.record().value(u'NeedClimatLog').toBool())
            returnValue.Room = unicode(oQuery.record().value(u'room').toString())
            returnValue.EnableSupervisor = bool(oQuery.record().value(u'EnableSupervisor').toBool())
            returnValue.EnableAssistant = bool(oQuery.record().value(u'EnableAssistant').toBool())
            returnValue.SingleItem = bool(oQuery.record().value(u'SingleItem').toBool())
            returnValue.GOST_ID = int(oQuery.record().value(u'gost_id').toInt()[0])
            returnValue.useAmpereTurn = int(oQuery.record().value(u'useAmpereTurn').toInt()[0])
            returnValue.ID = int(oQuery.record().value(u'id').toInt()[0])
            returnValue.FullName = unicode(oQuery.record().value(u'FullName').toString())
            returnValue.SupervisorReport = bool(oQuery.record().value(u'SupervisorReport').toBool())
            returnValue.CheckReport = bool(oQuery.record().value(u'CheckReport').toBool())
            returnValue.TicketMatrix = bool(oQuery.record().value(u'TicketMatrix').toBool())

        return returnValue

    def is_Single(self, _sHostname):
        u"""Сконфигурирован только один стенд, выбирать не из чего. Кнопка смены стенда не нужна"""
        sQuery = u"""
                    select
                        stnd.id as standID
                    from
                        stand stnd
                    where
                        stnd.hostname = :sHostname
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':sHostname', QVariant(_sHostname))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.size() == 1


    def existsOperator(self, _iStandID, _iOperatorID):
        u"""Сконфигурирован только один стенд, выбирать не из чего. Кнопка смены стенда не нужна"""
        sQuery = u"""
                    select
                        stuser.id
                    from
                        stand_user stuser
                    where
                        stuser.stand = :iStandID
                        and stuser.operator = :iOperatorID
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iStandID', QVariant(_iStandID))
        oQuery.bindValue(u':iOperatorID', QVariant(_iOperatorID))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        return oQuery.size() > 0


#    def is_tested(self, _iItemID, _iCoilID, _pointList):
#        u"""Протестированна ли обмотка. _iItemID - трансформатор  _iCoilID -  _pointList - смотри app.gost.GOST7746.get_point_list"""
#        for oPoint in _pointList:
#            oPoint
#            self.oChecking.get_point(_iItemID, _iCoilID, oPoint, oPoint)

class Gost(object):
    u"""Колекция методов для работы с ГОСТами"""

    def __init__(self, _env):
        self.env = _env

    def GetDetail(self, _iGOSTID, _sClassAccuracy, _iSecondLoad):
        u""""""
        sQuery = u"""
            select
                pnt.ipercent
                , pnt.ALeftLimit
                , pnt.PLeftLimit
                , pnt.ARightLimit
                , pnt.PRightLimit
                , pnt.ALeftLimit
                , pnt.ARightLimit
                , pnt.PLeftLimit
                , pnt.PRightLimit
                , pnt.itreshold
                , ql.Quadro
            from
                gost_detail as pnt
            left join
                GOST_quadroload as ql
            on
                ql.gost_id = pnt.gost_id
                and ql.SecondLoad = (select max(mql.SecondLoad) from GOST_quadroload as mql where mql.SecondLoad <= :iSecondLoad)
                and pnt.UseQuadro = true
            where
                pnt.gost_id = :iGOSTID
                and pnt.classaccuracy = :sClassAccuracy
            order by
                pnt.ipercent
                , pnt.UseQuadro
        """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':iSecondLoad', QVariant(_iSecondLoad))
        oQuery.bindValue(u':iGOSTID', QVariant(_iGOSTID))
        oQuery.bindValue(u':sClassAccuracy', QVariant(_sClassAccuracy))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        res = {}
        index = 0
        while oQuery.next():
            record = oQuery.record()
            index += 1
            iQuadro = None
            if(not record.value(u'Quadro').isNull()):
                iQuadro = self.FiveRound(record.value(u'Quadro').toDouble()[0] if record.value(u'Quadro').toDouble()[0] != 0 else float(_iSecondLoad) / 4)

            res[index] = Point(
                record.value(u'ipercent').toDouble()[0]
                , record.value(u'ALeftLimit').toDouble()[0]
                , record.value(u'ARightLimit').toDouble()[0]
                , record.value(u'PLeftLimit').toDouble()[0]
                , record.value(u'PRightLimit').toDouble()[0]
                , record.value(u'itreshold').toDouble()[0]
                , iQuadro
                )
        return res

    def FiveRound(self, value):
        return round(0.05 * round(float(value)/0.05), 2)


class DBProp(object):
    u"""Колекция методов для работы с prperty."""

    def __init__(self, _env):
        self.env = _env

    def insert(self, _PropName):
        sQuery = u"""
                    insert into
                        db_property
                    (name)
                    values (:PropName)
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)

        oQuery.bindValue(u':PropName', QVariant(_PropName))

        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def set_date(self, _PropName, _PropValue):
        sQuery = u"""
                    update
                        db_property
                    set
                        valuedatetime = :PropValue
                    where
                        name = :PropName
                    ;
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)

        oQuery.bindValue(u':PropValue', QVariant(_PropValue))
        oQuery.bindValue(u':PropName', QVariant(_PropName))

        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())

    def get_date(self, _PropName):
        u"""Получить ID текущей, действительной записи"""
        sQuery = u"""
                    select
                        valuedatetime
                    from
                        db_property
                    where
                       name  = :PropName
                    """
        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':PropName', QVariant(_PropName))
        oQuery.exec_()
        if oQuery.lastError().isValid():
            raise Exception(oQuery.lastError().text())
        if oQuery.next():
            return oQuery.record().value(u'valuedatetime').toDateTime()
        else:
            return None
