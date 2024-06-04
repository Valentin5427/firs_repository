#-*- coding: UTF-8 -*-
u"""
Created on 29.07.2012
@author: Anton
ticket #
Description: 
"""

from PyQt4.QtGui import QWidget, QIcon
from PyQt4.QtCore import pyqtSignal, QVariant

from electrolab.gui.common import UILoader


class SimpleChoice(QWidget, UILoader):
    u""" """
    choice = pyqtSignal(u'QVariant')
    
    def __init__(self, _env):
        super(QWidget, self).__init__()
        self.env = _env
        self.setUI(self.env.config, u'SimpleChoice.ui')
        self.iPrevKeyValue = None
        self.ui.tvChoice.env = _env
        self.ui.tvChoice.addButton(3, u"btnCancel", u'', QIcon(u':/ico/ico/block_64'))
        self.ui.tvChoice.addButton(4, u"btnOk", u'', QIcon(u':/ico/ico/tick_64'))
        self.ui.tvChoice.btnPressed.connect(self.item_btn_process)

    def set_query(self, _sQuery, _skeyFieldName, _iCurrentKey):
        self.ui.tvChoice.set_query(_sQuery)
        self.ui.tvChoice.keyFieldName = _skeyFieldName
        self.iPrevKeyValue = _iCurrentKey
        self.ui.tvChoice.set_row_by_key(_iCurrentKey)
        self.ui.tvChoice.table.hideColumn(0)

    def item_btn_process(self, _sender, _checked):
        u"""Обработка сигнала от кнопок на View"""
        if _sender.objectName() == u"btnCancel":
            self.choice.emit(self.iPrevKeyValue)
        elif _sender.objectName() == u"btnOk":
            keyValue = self.ui.tvChoice.get_value_by_name(self.ui.tvChoice.keyFieldName)
            #TODO: Странная фигня self.ui.tvChoice.get_value_by_name вместо None возвращает 0
            if 0 == keyValue.toInt()[0]:
                self.choice.emit(QVariant(None))
            else:
                self.choice.emit(keyValue)
    
