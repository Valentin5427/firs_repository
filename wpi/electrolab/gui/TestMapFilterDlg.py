#coding=utf-8
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtSql import QSqlQueryModel
from electrolab.gui.params import ParamDlg

class TestMapFilterDlg(ParamDlg):

    _indexChanged = pyqtSignal()

    def __init__(self, name, env):
        ParamDlg.__init__(self, name, env)

        self.model = QSqlQueryModel()
        self.model.setQuery(u'select id, serialnumber from serial_number', env.db)
        self.ui.cbSerial.setModel(self.model)
        self.ui.cbSerial.setModelColumn(1)
        self.ui.cbSerial.setCurrentIndex(-1)

        cur = QDate.currentDate()
        self.ui.dFrom.setDate(cur.addDays(-cur.dayOfWeek()+1))
        self.ui.dTo.setDate(cur)

        self.ui.cbSerial.currentIndexChanged.connect(self._filterChanged)
        self.ui.dFrom.dateChanged.connect(self._filterChanged)
        self.ui.dTo.dateChanged.connect(self._filterChanged)

    def where_clause(self):
        idx = self.ui.cbSerial.currentIndex()
        serial = self.model.record(self.ui.cbSerial.currentIndex()).value(0).toPyObject()
        from_date = self.ui.dFrom.date().toString(u'dd.MM.yyyy')
        to_date = self.ui.dTo.date().addDays(1).toString(u'dd.MM.yyyy')
        
        conds = []
        if idx > -1 and u'' != self.ui.cbSerial.currentText():
            conds.append(u'test_map.id in (select test_map from item where serial_number = {0})'.format(serial))
        if from_date:
            conds.append(u"createdatetime >= '{0}'".format(from_date))
        if to_date:
            conds.append(u"createdatetime < '{0}'".format(to_date))

        return u' and '.join(conds)
    
    def clearSerialNumber(self):
#        self.ui.cbSerial.clear()
        self.ui.cbSerial.setCurrentIndex(-1)