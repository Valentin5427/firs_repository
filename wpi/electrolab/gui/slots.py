#coding=utf-8
"""
Created on 23.08.2011

@author: kaa
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog
from dpframe.gui.menuitem import BaseSlotHolder, menuSlot
from electrolab.gui.reference import  BaseReference
from electrolab.gui.reporting import FRPrintForm, NCPrintForm
from electrolab.gui.params import OkCancelDlgContainer, ParamDlg
from electrolab.gui.testmapref import Testmap

class RefSlotHolder(BaseSlotHolder):

    @staticmethod
    def open_ref(window, ref_name, env):
        # print 'q'
        for sub in window.centralWidget().subWindowList():
            if sub.widget().name == ref_name:
                window.centralWidget().setActiveSubWindow(sub)
                return

        # print 'w'
        reference = BaseReference.get_ref_class(ref_name, env)(window, ref_name, env)
        # print 'e'
        window.centralWidget().addSubWindow(reference, Qt.SubWindow)
        # print 'r'
        reference.setWindowTitle(env.refs[ref_name].display)
        # print 't'
        reference.rejected.connect(window.centralWidget().closeActiveSubWindow)
        # print 'y'
        reference.show()
        # print 'u'

    @menuSlot
    def open_reference(self, checked, action, window, params, env):
        self.open_ref(window, params.reference, env)

    @menuSlot
    def open_reference_touch(self, checked, action, window, params, env):

        reference = BaseReference.get_ref_class(params.table, env)(params.table, env)
        reference.setWindowTitle(env.refs[params.table].display)
        if env.winparam.fullscreen:
            reference.setWindowState(Qt.WindowFullScreen)
        if env.winparam.nomouse:
            reference.setCursor(QCursor(Qt.BlankCursor))
        reference.exec_()

    @menuSlot
    def open_test_map(self, checked, action, window, params, env):
#        self.open_ref(window, params.reference, env)
        ref_name = params.reference
        for sub in window.centralWidget().subWindowList():
            if sub.widget().name == ref_name:
                window.centralWidget().setActiveSubWindow(sub)
                return
    
        reference = Testmap(window, ref_name, env)
        window.centralWidget().addSubWindow(reference, Qt.SubWindow)
        reference.setWindowTitle(env.refs[ref_name].display)
        reference.rejected.connect(window.centralWidget().closeActiveSubWindow)
        reference.show()
        
    @menuSlot
    def open_config_export1c(self, checked, action, window, params, env):
        ref_name = params.reference
        for sub in window.centralWidget().subWindowList():
            if sub.widget().name == ref_name:
                window.centralWidget().setActiveSubWindow(sub)
                return

        from electrolab.gui.ConfigExport1c import ConfigExport1c
        reference = ConfigExport1c(window, ref_name, env)
        window.centralWidget().addSubWindow(reference, Qt.SubWindow)
        reference.setWindowTitle(u"Выгрузка 1С")
        reference.rejected.connect(window.centralWidget().closeActiveSubWindow)
        reference.show()


class ReportSlotHolder(BaseSlotHolder):

    @menuSlot
    def show_report(self, checked, action, window, params, env):
        pass
        #TODO:Временно отключено. Не собиралось

        rpt_classes = {
            u'FR': FRPrintForm,
            u'NC': NCPrintForm
        }

        rpt_params = {}
        filter_name = env.reports[params.report].get(u'initialization')
        if filter_name:
            dlg = OkCancelDlgContainer(ParamDlg.get_dlg_class(filter_name, env)(filter_name, env))
            dlg.setModal(True)
            if QDialog.Accepted == dlg.exec_():
                rpt_params = dlg.params
            else:
                return
        rpt = rpt_classes[env.reports[params.report].type](env.reports[params.report].template ,rpt_params, env)
        rpt.preview()


    @menuSlot
    def open_accountSCM(self, checked, action, window, params, env):
        import AccountCSM
        window = AccountCSM.WinCSM(env.db)
        window.exec_()

