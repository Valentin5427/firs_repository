#-*- coding: UTF-8 -*-
u"""
Created on 01.12.2011

@author: Knurov
"""

from electrolab.gui.reference import MasterDetailReference
from dpframe.tech.typecheck import *
from dpframe.tech.typecheck import env_type
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import QAction, QWidget, QMenu
from electrolab.gui.reporting import FRPrintForm
from dpframe.gui.menuitem import menuSlot


class Testmap(MasterDetailReference):
    u"""Класс с журнала испытаний, только ради кнопочек"""

    # @takes('Testmap', QWidget,  env_type, optional(bool))
    def __init__(self, parent, name, env, selecting=False):
        u""""""
        super(Testmap, self).__init__(parent, name, env, selecting)
#        self.printReport = QAction(Dialog)
        self.VERIFER_REPORT_CAPTION = u'Отчет поверителя'
        self.TESTER_REPORT_CAPTION = u'Протокол испытаний'
        self.LABEL_REPORT_CAPTION = u'Этикетки'
        self.printReport = QAction(self)
        self.printMenu = QMenu(self)
        self.printMenu.addAction(QIcon(u':/EL/ico/print_32'), self.VERIFER_REPORT_CAPTION)
        self.printMenu.addAction(QIcon(u':/EL/ico/print_32'), self.TESTER_REPORT_CAPTION)
        self.printMenu.addAction(QIcon(u':/EL/ico/print_32'), self.LABEL_REPORT_CAPTION)
        self.printReport.setMenu(self.printMenu)
        self.printReport.setIcon(QIcon(u':/EL/ico/print_32'))
        self.printReport.setObjectName(u'printReport')
        self.printReport.setToolTip(u'Печать')
        self.master.ui.toolBar.addAction(self.printReport)
        self.printMenu.triggered.connect(self.print_report)
        
    def print_report(self, _action):
        u""""""
        test_mapID = self.detail.model.defaults[self.fk_detail]
        if self.VERIFER_REPORT_CAPTION == _action.text():
            rpt = FRPrintForm(u'verifier_protocol.fr3', {u'test_map':test_mapID}, self.env)
            rpt.preview()
            return
        
        if self.TESTER_REPORT_CAPTION == _action.text():
            # print 'FRPrintForm(utester_protocol.fr3, {utest_map:test_mapID}, self.env)'
###            rpt = FRPrintForm(u'tester_protocol.fr3', {u'test_map':test_mapID}, self.env)
            rpt = FRPrintForm(u'tester_protocol.fr3', {u'test_map':test_mapID, u'itemid':0}, self.env)
            rpt.preview()
            return
        
        if self.LABEL_REPORT_CAPTION == _action.text():
            rpt = FRPrintForm(u'ReportTickets.fr3', {u'test_map':test_mapID}, self.env)
            rpt.preview()
            return
   
