#-*- coding: UTF-8 -*-
u"""
Created on 24.07.2011
@author: knur
ticket #4
Интеграция с 1С Разбор XML и вставка полученных данных в БД
"""
#from xml.dom.minidom import parse
from lxml import etree
from dpframe.tech.pgdb import DBParam
from electrolab.tech.integration import LOG
from electrolab.tech.integration import Import1C
from electrolab.tech.integration import FileSystem

from lxml import etree

import re

class Loader():
    u"""Загрузка данных"""

    def __init__(self, _connect, _oLog, _noException = True):
        u"""_connect - Соединение с БД, _oLog - Журнал"""
        self.oConnect = _connect
        self.oLog = _oLog
        self.noException = _noException

    def get_transformer_fields(self):
        u"""Словарь полей для трансформатора"""
        return {
                u'QuantSecondCoil': None
                , u'ShortName': None
                , u'Type': None
                , u'Standart': None
                , u'Voltage': None
                , u'MaxOperVoltage': None
                , u'Frequency': None
                , u'IsolationLevel': None
                , u'Climat': None
                , u'Weight': None
                 }

    def get_coil_fields(self):
        u"""Словарь полей для обмоток"""
        return {
                u'ClassAccuracy': None
                , u'PrimaryCurrent': None
                , u'SecondCurrent': None
                , u'SecondLoad': None
                , u'MagneticVoltage': None
                , u'MagneticCurrent': None
                , u'Resistance': None
                , u'Rating': None
                , u'Tap': None
                , u'AmpereTurn': None
                }

    def _regex_group(self, _pattern, _value):
        u"""Парсилка"""
        result = self._regex_group_list(_pattern, _value)
        if(result and len(result)):
            return result[0]
        else:
            return None

    def _regex_group_list(self, _pattern, _value):
        u"""Парсилка"""
        if None == _value:
            return None
        self.pattern = re.compile(_pattern, re.IGNORECASE)
        result = re.findall(self.pattern, _value)
        if(result and len(result)):
            return result
        else:
            return None

    def _clear(self, _value):
        u"""Ужас!!!!!! вырезаем буквачки"""
        if '' == _value:
            return None
        self.pattern = re.compile(u'\D', re.IGNORECASE)
        value = int(re.sub(self.pattern, '',_value))
        self.pattern = re.compile(u'\d', re.IGNORECASE)
        sufiks = re.sub(self.pattern, '',_value)
        if sufiks == u'кВ':
            return value * 1000
        return value

    def get_transformer_description(self, _sFullName):
        #ТЛО-10_М5ADE-0.5SFS10/10P20/5P20-15/15/15-1500(3000)-3000-3000/5_У3_б_40кА
        #ТШ-ЭК-0,66_М3B285-10P10/0.5FS10-2,5/5-50/5_У3
        #ТВ-ЭК_110М1_УХЛ1
        type = None
        voltage = None
        prefiks = _sFullName[:2]
        if prefiks == u'ТЛ':
            type = _sFullName.split(u'-')[0]
            voltage = self._regex_group(u'^...-(\d+)', _sFullName)
        if prefiks == u'ТШ':
            type = _sFullName.split(u'-')[0]
            voltage = self._regex_group(u'^..-..-(\d+,*\d*)', _sFullName)
            voltage = voltage.replace(',', '.')
        if prefiks == u'ТВ':
            type = _sFullName.split(u' ')[0]
            voltage = self._regex_group(u'^..-.. (\d+)', _sFullName)
        return type, voltage

#    def get_type(self, _sFullName):
#        #ТЛО-10_М5ADE-0.5SFS10/10P20/5P20-15/15/15-1500(3000)-3000-3000/5_У3_б_40кА
#        if u'Л'== _sFullName[2:2]:
#            delemiter = u'-'
#        else:
#            delemiter = u' '
#        description = _sFullName.split(delemiter)
#        return description[0]

    def get_text(self, _node):
        textnode = _node.childNodes[0]
        if textnode.nodeType == textnode.TEXT_NODE:
            return textnode.data

    def get_text_by_name(self, _node, _name):
        nodes = _node.getElementsByTagName(_name)
        if len(nodes) != 1:
            raise Exception(u'Not single node')
        return self.get_text(nodes[0])

    def need_update_coil(self, _data):
        u""""""
        sQuery = u'''
            select
                ID
            from
                coil
            where
                transformer in (select ID from transformer where FullName = %(transformer)s)
                and coalesce(CoilNumber, 0) = coalesce(%(CoilNumber)s, 0)
                /*,CoilType*/
                and coalesce(ClassAccuracy, '') = coalesce(%(ClassAccuracy)s, '')
                and coalesce(PrimaryCurrent, 0) = coalesce(%(PrimaryCurrent)s, 0)
                and coalesce(SecondCurrent, 0) = coalesce(%(SecondCurrent)s, 0)
                and coalesce(SecondLoad, 0) = coalesce(%(SecondLoad)s, 0)
                and coalesce(MagneticVoltage, 0) = coalesce(%(MagneticVoltage)s, 0)
                and coalesce(MagneticCurrent, 0) = coalesce(%(MagneticCurrent)s, 0)
                and coalesce(Resistance, 0) = coalesce(%(Resistance)s, 0)
                and coalesce(Rating, '') = coalesce(%(Rating)s, '')
                and coalesce(Tap, 0) = coalesce(%(Tap)s, 0)
                and coalesce(AmpereTurn, 0) = coalesce(%(AmpereTurn)s, 0)
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery, _data)
        return cursor.rowcount == 1


    def exist_coil(self, _name, _number, _tap):
        u""""""
        sQuery = u'''
            select id from coil
            where transformer in (select ID from transformer where FullName = %s)
            and CoilNumber = %s
            and Tap = %s
            ;
        '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery, (_name, _number, _tap))
        return cursor.rowcount == 1

    def insert_coil(self, _data):
        sQuery = u'''
            insert into
                coil
            (
            transformer
            ,CoilNumber
            /*,CoilType*/
            , ClassAccuracy
            , PrimaryCurrent
            , SecondCurrent
            , SecondLoad
            , MagneticVoltage
            , MagneticCurrent
            , Resistance
            , Rating
            , Tap
            , AmpereTurn
            )
            values
            (
            (select ID from transformer where FullName = %(transformer)s)
            , %(CoilNumber)s
            /*,CoilType*/
            , %(ClassAccuracy)s
            , %(PrimaryCurrent)s
            , %(SecondCurrent)s
            , %(SecondLoad)s
            , %(MagneticVoltage)s
            , %(MagneticCurrent)s
            , %(Resistance)s
            , %(Rating)s
            , %(Tap)s
            , %(AmpereTurn)s
            )
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, _data)
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise


    def update_coil(self,_data):
        u""""""
        sQuery = u'''
            update
                coil
            set
                ClassAccuracy = %(ClassAccuracy)s
                , PrimaryCurrent = %(PrimaryCurrent)s
                , SecondCurrent = %(SecondCurrent)s
                , SecondLoad = %(SecondLoad)s
                , MagneticVoltage = %(MagneticVoltage)s
                , MagneticCurrent = %(MagneticCurrent)s
                , Resistance = %(Resistance)s
                , Rating = %(Rating)s
                , AmpereTurn = %(AmpereTurn)s
            where
                transformer = (select ID from transformer where FullName = %(transformer)s)
                and CoilNumber = %(CoilNumber)s

            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, _data)
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise


    def change_coil(self, _transformerName, _coilNumber, _data):
        u""""""
        if not self.exist_coil(_transformerName, _coilNumber,  _data[u'Tap']):
            self.oLog.info(u'Добавление обмотки %s с отпайкой %s трансформатор %s' % (_coilNumber, _data[u'Tap'], _transformerName))
            return self.insert_coil(_data)
        if not self.need_update_coil(_data):
            self.oLog.info(u'Изменени обмотки %s с отпайкой %s трансформатор %s' % (_coilNumber, _data[u'Tap'], _transformerName))
            return self.update_coil(_data)

    def exist_ware(self, _name):
        u""""""
        cursor = self.oConnect.connection.cursor()
        cursor.execute(u"""select ID from transformer where FullName = %s""", (_name,))
        return cursor.rowcount == 1

    def need_update_ware(self, _name, _data):
        u""""""
        sQuery = u'''
            select
                ID
            from
                transformer
            where
                FullName = %(FullName)s
                and ShortName = %(ShortName)s
                and coalesce(Standart, '') = coalesce(%(Standart)s, '')
                and coalesce(Voltage, 0) = coalesce(%(Voltage)s, 0)
                and coalesce(MaxOperVoltage, 0) = coalesce(%(MaxOperVoltage)s, 0)
                and coalesce(Frequency, 0) = coalesce(%(Frequency)s, 0)
                and coalesce(IsolationLevel, '') = coalesce(%(IsolationLevel)s, '')
                and coalesce(Climat, '') = coalesce(%(Climat)s, '')
                and coalesce(Weight, 0) = coalesce(%(Weight)s, 0)
                and coalesce(Type, '') = coalesce(%(Type)s, '')
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery, _data)
        return cursor.rowcount == 1

    def update_ware(self, _name, _data):
        u""""""
        sQuery = u'''
            update
                transformer
            set
                Standart = %(Standart)s
                , Voltage = %(Voltage)s
                , MaxOperVoltage = %(MaxOperVoltage)s
                , Frequency = %(Frequency)s
                , IsolationLevel = %(IsolationLevel)s
                , Climat = %(Climat)s
                , Weight = %(Weight)s
                , ShortName = %(ShortName)s
                , Type = %(Type)s
            where
                FullName = %(FullName)s
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, _data)
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise

    def insert_ware(self, _name, _data):
        sQuery = u'''
            insert into
                transformer
            (
                FullName
                , ShortName
                , Standart
                , Voltage
                , MaxOperVoltage
                , Frequency
                , IsolationLevel
                , Climat
                , Weight
                , Type
            )
            values
            (
                %(FullName)s
                , %(ShortName)s
                , %(Standart)s
                , %(Voltage)s
                , %(MaxOperVoltage)s
                , %(Frequency)s
                , %(IsolationLevel)s
                , %(Climat)s
                , %(Weight)s
                , %(Type)s
            )
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, _data)
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise

    def change_ware(self, _name, _data):
        u""""""
        if not self.exist_ware(_name):
            self.oLog.info(u'Добавление трансформатора "%s"' % _name)
            return self.insert_ware(_name, _data)
        if not self.need_update_ware(_name, _data):
            self.oLog.info(u'Изменение трансформатора "%s"' % _name)
            return self.update_ware(_name, _data)

    def insert_serial(self, _transformerName, _yar, _serial, _order, _series):
        sQuery = u'''
            insert into
                serial_number
            (
                SerialNumber
                , MakeDate
                , transformer
                , OrderNumber
                , Series
            )
            values
            (
                %s
                , %s
                , (select ID from transformer where FullName = %s)
                , %s
                , %s
            )
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, (_serial, _yar, _transformerName, _order, _series))
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise


    def update_serial(self, _transformerName, _yar, _serial, _order, _series):
        u""""""
        sQuery = u'''
            update
                serial_number
            set
                transformer = (select ID from transformer where FullName = %s)
                , OrderNumber = %s
                , Series = %s
            where
                SerialNumber = %s
                and MakeDate = %s
            ;
            '''
        cursor = self.oConnect.connection.cursor()
        try:
            cursor.execute(sQuery, (_transformerName, _order, _series, _serial, _yar))
            self.oConnect.connection.commit()
        except:
            self.oConnect.connection.rollback()
            raise

    def exist_serial(self, _iSerial, _iYar):
        u""""""
        cursor = self.oConnect.connection.cursor()
        cursor.execute(u"""select ID from serial_number where SerialNumber = %s and MakeDate = %s""", (_iSerial, _iYar))
        return cursor.rowcount == 1

    def need_update_serial(self, _transformerName, _yar, _serial, _order, _series):
        u""""""
        sQuery = u'''
                    select ID from serial_number
                    where
                        SerialNumber = %s
                        and MakeDate = %s
                        and transformer = (select ID from transformer where FullName = %s)
                        and OrderNumber = %s
                        and Series = %s
                    '''
        cursor = self.oConnect.connection.cursor()
        cursor.execute(sQuery, (_serial, _yar, _transformerName, _order, _series))
        return cursor.rowcount == 1

    def change_serial(self, _transformerName, _yar, _serial, _order, _series):
        u""""""
        self.oLog.info(u'Обработка. номер %s год %s Трансформатор %s' % (_serial, _yar, _transformerName))
        if not self.exist_serial(_serial, _yar):
            self.oLog.info(u'Добавление серийного номера "%s %s"' % (_yar, _serial))
            return self.insert_serial(_transformerName, _yar, _serial, _order, _series)
        if not self.need_update_serial(_transformerName, _yar, _serial, _order, _series):
            self.oLog.info(u'Изменение серийного номера "%s %s"' % (_yar, _serial))
            return self.update_serial(_transformerName, _yar, _serial, _order, _series)
        self.oLog.info(u'Серийный номер "%s %s" не измененился' % (_yar, _serial))

    def _get_props_value(self, _rootNode, _name, _containerName = u'ЗначениеПараметра'):
        u"""Специальный метод для извлечения данных из извращентской структуры"""
        for attribNode in _rootNode.childNodes:
            if attribNode.nodeType != attribNode.ELEMENT_NODE:
                continue
            if _name == attribNode.getAttribute(u'НазваниеПараметра'):
                valueAttrin = attribNode.getAttribute(_containerName)
                if not valueAttrin in [u'', u'---']:
                    return valueAttrin
                else:
                    return None

    def parseTLOCoilValue(self, _value, _coilNumber):
        """ ТЛО. обмотки идут через тире """
        aValueList = self._regex_group_list(u'\D*([\d\(]+)\D*', _value)
        # aValueList = self._regex_group_list(u'([\d\(]+)', _value)
        if(None == aValueList or 0 == len(aValueList)):
            return None

        if(len(aValueList) >= _coilNumber):
            return aValueList[_coilNumber - 1]
        else:
            return aValueList[0]

    def parseTLOTapValue(self, _value, _tapNumber):
        """ ТЛО. не более двух """
        firstValue = self._regex_group(u'(\d+)', _value) or 0
        if(2 == _tapNumber):
            return firstValue
        elif(3 == _tapNumber):
            secondValue = self._regex_group(u'\((\d+)', _value) or 0
            return secondValue or firstValue
        else:
            return None


    def get_AmpereTurn(self, _rootNode, _coilNumber, _tap = 2):
		# <ПараметрыСерии_Б-26848 Название="ТЛП-10-2_М1АC-0.5/10P/10P-10/10/15-200/5_У3_б_31.5кА">
		# 	<Обмотка_1И АмперВитки="600"/>
		# 	<Обмотка_2И АмперВитки="600"/>
		# 	<Обмотка_3И АмперВитки="600"/>
		# </ПараметрыСерии_Б-26848>
        if(_rootNode == None):
            return None
        coilName = u'Обмотка_%sИ' % _coilNumber
        try:
            coilNode = _rootNode.getElementsByTagName(coilName).item(0)
            if(coilNode):
                rawValue = coilNode.getAttribute(u'АмперВитки')
                return self.parseTLOTapValue(rawValue, _tap)
            else:
                return None
        except Exception, er:
            self.oLog.warning(u'Неизвестный Ампер-виток. Ошибка "%s"' % er.message)
            return False


    def process_tl_coil(self, _transformerName, _coilNumber, _rootNode, _paramNodeList, _tap = 2):
        data = self.get_coil_fields()
        coilName = u'Сердечник%s' % _coilNumber
        data[u'ClassAccuracy'] = self._get_props_value(_rootNode, u'Класс точности (от кол-ва вторичных обмоток)', coilName)
        try:
            value = int(self._get_props_value(_rootNode, u'Номинальный первичный ток', coilName) or 0) #Похоже отсюда ничего не приезжает, все лежит через "-" 5(6)-1(2)
            rawValue = self._get_props_value(_rootNode, u'Номинальный первичный ток', u'ЗначениеПараметра')
            coilRawValue = self.parseTLOCoilValue(rawValue, _coilNumber)
            tapValue = int(self.parseTLOTapValue(coilRawValue, _tap))
        except Exception, er:
            self.oLog.warning(u'Неизвестный Номинальный первичный ток. Ошибка "%s" трансформатор не будет загружен' % er.message)
            return False
        data[u'PrimaryCurrent'] = tapValue or value
        try:
            value = int(self._get_props_value(_rootNode, u'Номинальный вторичный ток', coilName) or 0) #Похоже отсюда ничего не приезжает, все лежит через "-" 5(6)-1(2)
            rawValue = self._get_props_value(_rootNode, u'Номинальный вторичный ток', u'ЗначениеПараметра')
            coilRawValue = self.parseTLOCoilValue(rawValue, _coilNumber)
            tapValue = int(self.parseTLOTapValue(coilRawValue, _tap))
        except Exception, er:
            self.oLog.warning(u'Неизвестный номинальный вторичный ток. Ошибка "%s" трансформатор не будет загружен' % er.message)
            return False
        data[u'SecondCurrent'] = tapValue or value
        data[u'SecondLoad'] = self.to_float(self._get_props_value(_rootNode, u'Номинальная вторичная нагрузка (от кол-ва вторичных обмоток)', coilName))
        data[u'transformer'] = _transformerName
        data[u'CoilNumber'] = _coilNumber
        data[u'Tap'] = _tap
        data[u'AmpereTurn'] = self.get_AmpereTurn(_paramNodeList, _coilNumber, _tap)
        self.change_coil(_transformerName, _coilNumber, data)
        return True

    def process_tl_coils(self, _transformerName, _rootNode, _paramNodeList):
        nodes = _rootNode.getElementsByTagName(u'ПараметрыТрансформатора').item(0)
        isMoreTap = None != self._get_props_value(nodes, u'E - c переключением по вторичной обмотке (отпайка на вторичной обмотке)')
        quant = int(self._get_props_value(nodes, u'Количество вторичных обмоток') or 0)
        if 0 == quant:
            self.oLog.error(u'У трансформатора "%s" нет обмоток, не будет загружен' % _transformerName)
            return False
        coilNumber = 1
        while quant >= coilNumber:
            if not self.process_tl_coil(_transformerName, coilNumber, nodes, _paramNodeList, 2):
                return False
            if coilNumber == 1 and isMoreTap:
                if not self.process_tl_coil(_transformerName, coilNumber, nodes, _paramNodeList, 3):
                    return False
            coilNumber += 1
        return True

    def process_tv_coil(self, _transformerName, _rootNode):
#        self.oLog.info(u'Обработка обмотки %d тарнсформатора %s' % (_coilNumber, _transformerName))
        data = self.get_coil_fields()
        nodes = _rootNode.getElementsByTagName(u'ДопПараметрыТрансформатора').item(0).childNodes
        for node in nodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            tap = self._clear(node.tagName) + 1
            data[u'Tap'] = tap
            data[u'transformer'] = _transformerName
            data[u'CoilNumber'] = 1
            psCurent = node.getAttribute(u'КоэффициентТрансформации').split(u'/')
            data[u'PrimaryCurrent'] = self.to_float(psCurent[0])
            data[u'SecondCurrent'] = self.to_float(psCurent[1])
            data[u'ClassAccuracy'] = node.getAttribute(u'КлассТочности')
            data[u'Rating']  = node.getAttribute(u'НоминальныйКоэффициентБезопасностиПриборов')
            data[u'SecondLoad']  = self.to_float(node.getAttribute(u'ВА'))
    #        data[u'']  = node.getAttribute(u'ПредельнаяКратность')
            self.change_coil(_transformerName, 1, data)

    def process_tv_coils(self, _transformerName, _rootNode):
        for coilNumber in range(10):
            nodes = _rootNode.getElementsByTagName(u'Отпайка%s' % coilNumber)
            if None == nodes:
                break
            self.process_tv_coil(_transformerName, coilNumber, _rootNode)

    def process_coil(self, _transformerName, _rootNode, _paramNodeList):
        u"""Разбор обмоток для ТЛ и для ТВ отличаются, данные лежат по другому"""
        type = self.get_transformer_description(_transformerName)[0].upper()
        if type in (u'ТЛО', u'ТЛП', u'ТШ'):
            return self.process_tl_coils(_transformerName, _rootNode, _paramNodeList)
        if type == u'ТВ-ЭК':
            self.process_tv_coil(_transformerName, _rootNode)
            return True
        raise Exception(u'Неизвестный тип трансформатора "%s", обмотки не будут добавленны' % type)

    def to_float(self, _value):
        u"""Привести к float. Вместо разделителя может дробной и целой части может быть ','"""
        try:
            if not type(_value) in [unicode, str]:
                return float(_value)
            return float(_value.replace(',', '.'))
        except Exception, er:
            return None

    def process_ware_attrib(self, _transformerName, _shortName, _rootNode):
        u""""""
        type, voltage = self.get_transformer_description(_transformerName)
        if None in [type, voltage]:
            self.oLog.warning(u'Неизвестный тип трансформатора "%s" не будет загружен' % _transformerName)
            return False
        data = self.get_transformer_fields()
        for attribNode in _rootNode.getElementsByTagName(u'ПараметрыТрансформатора').item(0).childNodes:
            if attribNode.nodeType == attribNode.ELEMENT_NODE:
                name = attribNode.getAttribute(u'НазваниеПараметра')
                value = attribNode.getAttribute(u'ЗначениеПараметра')
                if value in [u'', u'---']:
                    continue
                if u'Климатическое исполнение' == name:
                    data[u'Climat'] = value

        #Это изврат. Но так уж данные теперь приходять в XML по этому и идем к родительской ветке
        data[u'MaxOperVoltage'] = self._clear(_rootNode.getAttribute(u'НаибольшееРабочееНапряжение'))
        data[u'Frequency'] = self.to_float(_rootNode.getAttribute(u'НоминальнаяЧастота'))
        data[u'Weight'] = self.to_float(_rootNode.getAttribute(u'ВесТрансформатора'))
        data[u'Standart'] = _rootNode.getAttribute(u'ТУ')

        #Поля разобранные из имени
        data[u'FullName'] = _transformerName
        data[u'ShortName'] = _shortName
        data[u'Type'] = type
        data[u'Voltage'] = self.to_float(voltage)

        self.change_ware(_transformerName, data)
        return True

    def process_ware(self, _rootNode, _paramNodeList):
        u""""""
        transformerName = _rootNode.getElementsByTagName(u'ПараметрыТрансформатора').item(0).getAttribute(u'Название').replace(u'_', ' ')
        shortName = transformerName
        series = _rootNode.getAttribute(u'НомерСерии')
        if u'ТВ' == transformerName[:2].upper():
            u"""Для ТВ-ЭК уникальное имя по другому"""
            transformerName = transformerName + u'(' + series + u')'
        if not self.process_ware_attrib(transformerName, shortName, _rootNode):
            return None
        if self.process_coil(transformerName, _rootNode, _paramNodeList):
            return transformerName
        else:
            return None

    def process_serial(self, _rootNode, _yar):
        u""""""
        serialNodeList = _rootNode.getElementsByTagName(u'ОписаниеТрансформатора')
        for serialNode in serialNodeList:
            serial = serialNode.getAttribute(u'НомерТрансформатора')
            serial = self._clear(serial)
            order = serialNode.getAttribute(u'НомерЗаказаНаПроизводство')
            series = serialNode.getAttribute(u'НомерСерии')
            paramNodeList = _rootNode.getElementsByTagName(u'ПараметрыСерии_%s' % series).item(0)
            transformerName = self.process_ware(serialNode, paramNodeList)
            if None == transformerName:
                continue
            if not self._regex_group(u'^(\D)', order):
                _yar = self._regex_group(u'^(\d\d)-', order)
            self.change_serial(transformerName, _yar, serial, order, series)
#        return _yar, number, transformerName

    def process_file(self, _oExchangeFile):
        u"""Обработать XML ExchangeFile()"""
        if(not _oExchangeFile.correct):
            raise Exception(u'Not correct file')
        dom = parse(_oExchangeFile.file)
        rootNodes = dom.getElementsByTagName(u'ТР')
        if(len(rootNodes) != 1):
            raise Exception(u'Incorrect XML')
        self.process_serial(rootNodes[0], _oExchangeFile.get_yar())

    def process(self, _CollectionXML):
        u"""Обработать коллекцию"""
        self.oLog.info(u'Начало обработки. Найдено %d файлов' % len(_CollectionXML))
        if(not self.oConnect.connected):
            self.oLog.error(u'Not connect to DB')
            return False
        for oItem in _CollectionXML:
            self.oLog.info(u'process %s' % oItem.sFileName)
            try:
                self.process_file(oItem)
            except Exception, er:
                self.oLog.error(u'При обработке файла %s возникла ошибка %s' % (oItem.sFileName, er.message))
                if not self.noException:
                    raise
            self.oLog.info(u'delete %s' % oItem.sFileName)
            try:
                oItem.delete()
            except Exception, er:
                self.oLog.error(u'При удалении %s возникла ошибка %s' % (oItem.sFileName, er))
                if not self.noException:
                    raise
        return True

def integration(env):
    u"""Задача агента загрузки из 1с"""
    from dpframe.tech import pgdb
    log = env.log
    log.info(u'Инициализация задачи. Загрузка данных из %s' % env.params.path)
    try:
        dbparams = DBParam(
                           env.params.db.host,
                           env.params.db.database,
                           env.params.db.user,
                           env.params.db.password,
                           )
        oConnect = pgdb.Connect(dbparams)
    except Exception, er:
        log.error(u'Сбой при подключении к БД. "s%"' % er.message)
    try:
        fileCollection = FileSystem().get_filelist(env.params.path, env.params.arch)
    except Exception, er:
        log.error(u'Сбой при получении списка файлов. "s%"' % er.message)
    if not fileCollection:
        log.info(u'Нет файлов для загрузки')
        return
    try:
        oLoade = Loader(oConnect, log)
        oLoade.process(fileCollection)
    except Exception, er:
        log.error(u'Сбой при загрузке. "s%"' % er.message)
    log.info(u'Загрузка данных из %s выполнена' % env.params.path)



def job(_sINIFile):
    u"""Задача загрузки из 1с"""
    from dpframe.tech import pgdb
    oINI = Import1C(_sINIFile)
    log = LOG(oINI.log)
    log.info(u'Инициализация задачи. Загрузка данных из %s' % oINI.path)
    try:
        oDBConectParam = pgdb.INI(_sINIFile).get_dbparam()
        oConnect = pgdb.Connect(oDBConectParam)
    except Exception, er:
        log.error(u'Сбой при подключении к БД. "s%"' % unicode(er.message))
    try:
        fileCollection = FileSystem().get_filelist(oINI.path, oINI.arch)
    except Exception, er:
        log.error(u'Сбой при получении списка файлов. "s%"' % unicode(er.message))
    if not len(fileCollection):
        log.info(u'Нет файлов для загрузки')
        return
    try:
        oLoade = Loader(oConnect, log)
        oLoade.process(fileCollection)
    except Exception, er:
        log.error(u'Сбой при загрузке. "s%"' % unicode(er.message))
    log.info(u'Загрузка данных из %s выполнена' % oINI.path)

if __name__ == "__main__":
    import sys
    if (len(sys.argv) == 1):
        sINIFile = u'integration.ini'
    elif (len(sys.argv) == 2):
        sINIFile = sys.argv[1]
    else:
        print u'Invalid argument. Example: integration.exe <integration.ini>'
    job(sINIFile)
