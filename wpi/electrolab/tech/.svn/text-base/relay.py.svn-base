#coding=utf-8
from collections import defaultdict
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtSql import QSqlQuery, QSqlDatabase
from dpframe.tech.typecheck import takes, int_type, returns, dict_of, tuple_of, anything, optional, with_attr, nothing
from pymodbus.client.sync import ModbusSerialClient

__author__ = 'kaa'

class OwenRelay(object):
    u"""
    Высокоуровневая реализация миодулей дискретного вывода компании Овен МУ110-ххР.

    Основной способ доступа к реле - оператор индекса (квадратные скобки).
    Индекс может быть целочисленным, начинаться с нуля (индекс реле) - низкоуровневый доступ,
    и иметь тип tuple(object, object), при работе с БД tuple(int, double) (пара "тип - значение") - высокоуровневый доступ.

    На низком уровне состояние реле просто устанавливаются и сбрасываются по одиночке, не затрагивая остальные.
    Можно также осуществить массовую установку/сброс состояний (см. описание функции set_coils).

    Для обеспечения доступа высокого уровня необходимо в начале задать соответствие пар "тип-значение" реальным индексам реле
    с помощью любой из функций set_map, set_query, set_statement, (см. описание).
    При высокоуровневой работе при установке одного реле сбрасываются все остальные, ассоциированные с тем же типом значения.
    Вызов каждой из функций set_map, set_query, set_statement
    перетирает настройки соответствия реле, сделанные предыдущим вызовом любой из этих функций.

    Типовой пример использования:

    client = OwenRelay(port_name='COM3', baudrate=9600, dev_number=16, relay_count=8)
    map = {
            #(тип, значение): индекс реле
            (1, 10): 0,
            (1, 20): 1,
            (1, 100): 2,
            (1, 200): 3,
            (6, True): 4,
            (6, False): 5,
            (3, 10): 6,
        }
    client.set_map(map)
    #client.set_model(model)
    #client.set_query(model)

    client[1, 10] = True    # установка реле 0, сброс реле 1, 2, 3 (они соотвествуют одному типу значения)
    client[1, 100] = True   # установка реле 2, сброс реле 1, 0, 3
    client[1, 10] = False   # сброс реле 0, при сбросе любого реле остальные не затрагиваются
    print client[1, 10]     # чтение состояние реле 0

    Пример низкоуровневого доступа

    client = OwenRelay(port_name='COM3', baudrate=9600, dev_number=16, relay_count=8)
    client[1] = False # сброс реле 1, состояния других реле не меняются
    client[1] = True  # установка реле 1, состояния других реле не меняются
    print client[1]   # чтение состояние реле 1

    client.set_coils([True, False, None, True]) #установка реле 0 и 3, сброс реле 1, состояние остальных не меняется

    Рекомендации по повышению производительности:
    1. Прикладной код должен избегать чтения состояния реле, т.к. чтение медленнее записи
    2. По возможности, при создании объекта задавать параметр relay_count.
       Это подавляет автоматическое определение количества реле
       и предотвращает многократное чтение при этом (очень долгое первое обращение к устройству)
    3. При настройке карты соответствия пар "тип-значение" и индексов реле настоятельно рекомендуется пары одного типа
       сопоставлять реле, идущим подряд, без дырок. Операции с реле, идущими подряд, производятся одним вызовом
       низкоуровневой функции и происходят одновременно (см. пример в описании функции set_map).

    """

    @takes('OwenRelay', str, int_type, int, optional(int), optional(bool))
    def __init__(self, port_name, baudrate, dev_number, relay_count=0, connect=True):
        self._port_name = port_name
        self._baudrate = baudrate
        self._dev_number = dev_number

        self._client = None
        if connect:
            self.connect()

        self._map = None
        self._types = None
        self._len = relay_count

    @returns(bool)
    def connect(self):
        self._client = self._client or ModbusSerialClient(port=self._port_name, baudrate=self._baudrate)
        return self._client.connect()

    def disconnect(self):
        self._client.close()

    def __del__(self):
        self.disconnect()

    @takes('OwenRelay', dict_of(tuple_of(anything), int))
    def set_map(self, map):
        u"""
        Задает соответствие пар тип-значение с индексами реле, источник - словарь.
        Словарь должен иметь структуру {(object, object): int}
        Рекомендуется пары одного типа сопоставлять непрерывному ряду реле, без дырок (см. пример ниже).

        client = OwenRelay('COM3', 9600, 16)
        map = { # хорошая настройка, нет разрывов между парами одного типа
            #(тип, значение): индекс реле
            (1, 10): 0,
            (1, 20): 1,
            (1, 100): 2,
            (1, 200): 3,
            (6, True): 4,
            (6, False): 5,
            (3, 10): 6,
        }

        #map = { # плохая настройка, есть многочисленные разрывы
        #    #(тип, значение): индекс реле
        #    (1, 10): 0,
        #    (1, 20): 1,
        #    (6, 100): 2,
        #    (1, 200): 3,
        #    (3, True): 4,
        #    (6, False): 5,
        #    (3, 10): 6,
        #}

        client.set_map(map)

        """

        self._map = map
        self._types = defaultdict(list)
        for (type, value), relay_idx in self._map.iteritems():
            self._types[type].append(relay_idx)

    @takes('OwenRelay', QSqlQuery)
    def set_query(self, query):
        u"""
        Задает соответствие пар тип-значение с индексами реле, источник - объект QSqlQuery.
        Результат запроса должен иметь не менее 4 колонок, со значениями,
        преобразующимися к типам int, double, int, int соответственно.
        Используются только первые 4 колонки, их семантическое значение: тип, значение, индекс реле, номер устройства.
        Значения первой пары колонок должны быть уникальными, используются только строки с текущим номером устройства.

        """

        map = {}
        if not query.isActive():
            query.exec_()
        while query.next():
            r = query.record()
            if r.count() < 4:
                query.clear()
                raise ValueError(u'Недостаточно колонок результата запроса (<4)')

            dev, ok = r.value(3).toInt()
            if not ok: raise ValueError(u"Значение номера устройства не целое.")

            if dev == self._dev_number:
                type_, ok = r.value(0).toInt()
                if not ok: raise ValueError(u"Значение типа не целое.")

                value, ok = r.value(1).toDouble()
                if not ok: raise ValueError(u"Значение значения :) не десятичная дробь.")

                relay, ok = r.value(2).toInt()
                if not ok: raise ValueError(u"Значение индекса реле не целое.")

                map[(type_, value)] = relay
        self.set_map(map)

    @takes('OwenRelay', basestring, QSqlDatabase)
    def set_statement(self, statement, db):
        u"""
        Задает соответствие пар тип-значение с индексами реле, источник - SELECT-запрос, заданный строкой.
        Результат запроса должен иметь не менее 4 колонок, со значениями,
        преобразующимися к типам int, double, int, int соответственно.
        Используются только первые 4 колонки, их семантическое значение: тип, значение, индекс реле, номер устройства.
        Значения первой пары колонок должны быть уникальными, используются только строки с текущим номером устройства.

        """

        query = QSqlQuery(statement, db)
        self.set_query(query)

    #@takes('OwenRelay', int)
    #@returns(bool)
    def _get_indexed_coil(self, index):
        #low level
        if index < 0 or index >= len(self):
            raise IndexError(u'Индекс реле за пределами допустимого диапазона (0-{0})'.format(len(self)))
        
        r = self._client.read_holding_registers(index, 1, self._dev_number)
        if r.function_code < 0x80:
            return bool(r.registers[0])
        else:
            raise r

    #@takes('OwenRelay', dict_of(tuple_of(anything), int))
    #@returns(bool)
    def _get_mapped_coil(self, key):
        #high level
        if self._map and key in map:
            return self._get_indexed_coil(self._map[key])
        else:
            raise KeyError(u"Пара (тип, значение) {0} не существует".format(key))

    #@takes('OwenRelay', int, anything)
    def _set_indexed_coil(self, index, value):
        #low level
        if index < 0 or index >= len(self):
            raise IndexError(u'Индекс реле за пределами допустимого диапазона (0-{0})'.format(len(self)))

        r = self._client.write_coil(index, bool(value), self._dev_number)
        if r.function_code >= 0x80:
            raise r

    #@takes('OwenRelay', dict_of(tuple_of(anything), int), anything)
    def _set_mapped_coil(self, key, value):
        #high level
        if self._map and key in self._map:
            coils = [None]*len(self)
            if value:
                for idx in self._types[key[0]]:
                    coils[idx] = False
                self.set_coils(coils)
            self[self._map[key]] = value
        else:
            raise KeyError(u"Пара (тип, значение) {0} не существует".format(key))

    @takes('OwenRelay', with_attr('__getitem__', '__len__'))
    @returns(nothing)
    def set_coils(self, coils):
        u"""
        Массовая установка/сброс состояния реле.
        Принимает список, значения None не оказывают влияния на состояния реле, соответствущие позиции значения в списке,
        значения, эквивалентные True, устанавливают реле, False - сбрасывают его. В списке доскаются значения любого типа,
        все, кроме None, приводятся к bool.
        Длина списка приводится к количеству реле на устройстве усечением либо дополнение соответствущим количеством значений None.

        """

        coils = ([val if val is None else bool(val) for val in coils] + [None]*(len(self)-len(coils)))[:len(self)] #normalizing
        solid = []
        res = {}
        for i, val in enumerate(coils):
            if val is None:
                solid = []
            else:
                if not solid:
                    res[i] = solid
                solid.append(val)
        for idx, coils in res.iteritems():
            self._client.write_coils(idx, coils, self._dev_number)

    def reset_coils(self):
        u""" Сброс всех реле. """

        self.set_coils([0]*len(self))

    @takes('OwenRelay', (int, tuple_of(anything)))
    @returns(bool)
    def __getitem__(self, key):
        # key must be int or (object, object)
        if not len(self):
            raise IndexError(u'Ни одного реле не найдено')

        if isinstance(key, int):
            return self._get_indexed_coil(key)
        elif isinstance(key, tuple) and 2 == len(key):
            return self._get_mapped_coil(key)
        else:
            raise TypeError(u'Недопустимый тип индекса реле')

    @takes('OwenRelay', (int, tuple_of(anything)), anything)
    @returns(nothing)
    def __setitem__(self, key, value):
        # key must be int or (object, object)
        if not len(self):
            raise IndexError(u'The relay is not found')

        if isinstance(key, int):
            self._set_indexed_coil(key, value)
        elif isinstance(key, tuple) and len(key) == 2:
            self._set_mapped_coil(key, value)
        else:
            raise TypeError(u'Недопустимый тип индекса реле')

    @takes('OwenRelay')
    @returns(int)
    def __len__(self):
        if self._len:
            return self._len
        else:
            for n in (2**n for n in xrange(5, 2, -1)):
                r = self._client.read_holding_registers(0, n, self._dev_number)
                if r.function_code < 0x80:
                    self._len = n
                    return self._len
            return 0


if u'__main__' == __name__:
    import sys
    app = QCoreApplication(sys.argv)
    db = QSqlDatabase.addDatabase(u'QPSQL')
    db.setHostName('localhost')
    db.setDatabaseName('electrolab')
    db.setUserName('electrolab')
    db.setPassword('electrolab')
    print db.open()

    client = OwenRelay('COM3', 9600, 16, 8)
    client.set_statement(u'select "type", "value", "relay", "device" from "device_command"', db)
    print client._map

    client.set_coils((1,1,1,1))
    client[1, 100.] = True
    client[1, 10.] = [4]
    client[1, 200.] = 1
    client[1, 11.] = {0: 0}
    client[1, 11.] = 0
