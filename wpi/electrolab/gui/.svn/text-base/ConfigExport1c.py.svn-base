#-*- coding: UTF-8 -*-
u"""
Created on 01.12.2011

@author: Knurov
"""

from PyQt4.QtGui import QDialog
from electrolab.gui.common import UILoader
from PyQt4.QtCore import QString
from PyQt4.QtCore import pyqtSlot
from electrolab.data.helper import DBProp


class ConfigExport1c(QDialog, UILoader):

    def __init__(self, _window, _name, _env):
        QDialog.__init__(self)
        self.name = _name
        self.setUI(_env.config, u"DlgExportProp.ui")
        self.oDBProp = DBProp(_env)
        self.undo()

    @pyqtSlot()
    def save(self):
        self.oDBProp.set_date(u'LastExport', self.ui.dtLastExport.dateTime())

    @pyqtSlot()
    def undo(self):
        self.ui.dtLastExport.setDateTime(self.oDBProp.get_date(u'LastExport'))
