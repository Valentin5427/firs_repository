#-*- coding: UTF-8 -*-
u"""
Created on 13.08.2012
@author: Anton
ticket #
Description: 
"""

from electrolab.data.helper import Gost

class GOST7746(object):
    u""" Здесь забит ГОСТ 7746-2001 используемый при испытании """
    
    def __init__(self, _env, _gostID,  _sClassAccuracy, _iSecondLoad):
        u""" """
        self.oGost = Gost(_env)
        self._curentPointList = self.oGost.GetDetail(_gostID, _sClassAccuracy, _iSecondLoad)
        self._curentPointIndex = 1
        
    def is_complit(self):
        u""" """
        for item, point in self._curentPointList.items():
            if not point.bFound:
                return False
        return True

    def get_point_list(self):
        return self._curentPointList

    # def _fill_quadro(self):
    #     u""" Заполнение таблицы определения четвертных нагрузок ГОСТ 7746-2001"""
    #     self._quadro = {}
    #     self._quadro[1] = 0.8
    #     self._quadro[2] = 1.25
    #     self._quadro[2.5] = 1.5
    #     self._quadro[3] = 1.75
    #     self._quadro[3.75] = 1.75
    #     self._quadro[5] = 3.75
    #     self._quadro[10] = 3.75
    #

    def get_point_by_index(self, _index):
        if not self._curentPointList.has_key(_index):  
            return None
        return self._curentPointList[_index]
    
    def get_left_border(self, _index):
        u"""Левая граница точки"""
        return self._curentPointList[_index].I - self._curentPointList[_index].threshold

    def get_right_border(self, _I, _index):
        u"""Правая граница точки"""
        return self._curentPointList[_index].I + self._curentPointList[_index].threshold
    
    def point_is_found(self, _I, _index):
        u"""Точка найдена"""
        return self.get_left_border(_index) < _I < self.get_right_border(self, _index)

    def on_the_right_of_point(self, _I, _index):
        u"""Cправа от точки"""
        return self.get_right_border(self, _index) <= _I

    def on_the_left_of_point(self, _I, _index):
        u"""Слева от точки"""
        return  _I <= self.get_left_border(_index)

    def is_error_current(self, _I, _index, _value):
        u"""Превышает угловую погрешность"""
        if not _I:
            return False
        if not self.point_is_found(_I, _index):
            return False
        point = self.get_point_by_index(_index)
        if point.ALeftLimit == 0 and point.ARightLimit == 0:
            return 0
        if bool(point.ALeftLimit) and point.ALeftLimit * -1 > _value:
            return abs(_value) - point.ALeftLimit
        elif bool(point.ARightLimit) and point.ARightLimit < _value:
            return abs(_value) - point.ARightLimit
        else:
            return 0
            
    def is_error_angular(self, _I, _index, _value):
        u"""Превышает токовою погрешность"""
        if not _I:
            return False
        if not self.point_is_found(_I, _index):
            return False
        point = self.get_point_by_index(_index)
        if point.PLeftLimit == 0 and point.PRightLimit == 0:
            return 0
        if bool(point.PLeftLimit) and point.PLeftLimit * -1 > _value:
            return abs(_value) - point.PLeftLimit
        elif bool(point.PRightLimit) and point.PRightLimit < _value:
            return abs(_value) - point.PRightLimit
        else:
            return 0
    
    def pint_count(self):
        return len(self._curentPointList)
            

