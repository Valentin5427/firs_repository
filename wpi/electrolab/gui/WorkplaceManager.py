#coding=utf-8
u"""
Created on 19.08.2011
#14
@author: Anton
"""
import sys

from PyQt4.QtGui import QTabBar, QShowEvent, QCloseEvent, QPixmap, QSplashScreen
from PyQt4.QtCore import QTranslator, Qt, QRect
from dpframe.gui.mainwnd import BaseMDIMainWnd
from dpframe.gui.menuloaders import JSONMenuLoader
from dpframe.base.envapp import checkenv
from dpframe.base.inits import json_config_init, db_connection_init, metadata_init, models_init, session_init, newmetadata_init
from dpframe.base import application
from dpframe.tech.typecheck import *
from dpframe.tech.typecheck import int_type
from electrolab.gui.inits import reference_init, serial_devices_init, report_init, filter_init
from electrolab.gui.slots import RefSlotHolder
from electrolab.gui.reference import cZero

from PyQt4.QtGui import QMessageBox


from electrolab.data import metadata

@checkenv(u'config', u'db', u'metadata', u'models', u'filters', u'refs', u'devices', u'reports', u'session')
@serial_devices_init
@report_init
@reference_init
@filter_init
@models_init
#@newmetadata_init(metadata)
@metadata_init
@db_connection_init
@session_init
@json_config_init
class MainWnd(BaseMDIMainWnd):

    @takes('MainWnd', unicode, dict_of(unicode, anything))
    def __init__(self, caption, menu):
        super(MainWnd, self).__init__(caption, menu)
        self.centralWidget().setViewMode(self.centralWidget().TabbedView)
        for tab in self.centralWidget().findChildren(QTabBar):
            tab.setExpanding(False)
            tab.setTabsClosable(True)
            tab.tabCloseRequested.connect(self.closeTab)

        print 7
    @takes('MainWnd', QShowEvent)
    @returns(nothing)
    def showEvent(self, event):
        # load session data
        print 1
        storage = self.env.session.storage.mainwnd
        print 2
        self.setGeometry(QRect(storage.x, storage.y, storage.width, storage.height))
        print 3
        self.setWindowState(Qt.WindowStates(storage.state))
        print 4
        #return
        for ref_name in self.env.session.storage.refs:
            print 'ref_name', ref_name
            if (ref_name != 'operator'):
                continue
            RefSlotHolder.open_ref(self, ref_name, self.env)
            
         #   break
            
        for sub in self.centralWidget().subWindowList():
            print 6, sub.widget().name
            if sub.widget().name == self.env.session.storage.active_ref:
                print 7, sub.widget().name
                self.centralWidget().setActiveSubWindow(sub)
                break
            print 9
        print 10

    @takes('MainWnd', QCloseEvent)
    @returns(nothing)
    def closeEvent(self, event):
        # Save session data
        storage = self.env.session.storage.mainwnd
        storage.state = int(self.windowState())
        rect = self.geometry()
        storage.x = rect.x()
        storage.y = rect.y()
        storage.width = rect.width()
        storage.height = rect.height()

        refs = []
        for sub in self.centralWidget().subWindowList():
            refs.append(sub.widget().name)
        self.env.session.storage.refs = refs
        active = self.centralWidget().activeSubWindow()
        self.env.session.storage.active_ref = active.widget().name if active else None

        subs = self.centralWidget().subWindowList()
        for sub in subs:
            sub.widget().saveSession()

        self.env.session.save()

    @takes('MainWnd', int_type)
    @returns(nothing)
    def closeTab(self, index):
        sub = self.centralWidget().subWindowList()[index]
        self.centralWidget().setActiveSubWindow(sub)
        self.centralWidget().closeActiveSubWindow()


def ExceptionHook(errType, value, tback):
    cZero().error(unicode(errType), value.message);
    sys.__excepthook__(errType, value, tback)
    #===========================================================================
    # mb = self._get_msg_wnd(text, infotext, detailedtext, title,
    #               QMessageBox.Critical, QMessageBox.Ok
    #              )
    # return mb.exec_()
    #===========================================================================
        
@returns(nothing)
def main():
    app = application.get()

    pix = QPixmap(u'ui/ico/user_64.png')
    pix.scaledToHeight(100)
    splash = QSplashScreen(pix) #, Qt.WindowStaysOnTopHint)
#    splash.setMask(pix.mask())
    splash.show();
    splash.showMessage(u'Инициализация приложения', Qt.AlignHCenter | Qt.AlignBottom, Qt.blue);
    app.processEvents();
    #sys.excepthook = ExceptionHook;
    
    qt_translator = QTranslator()
    if qt_translator.load( u':EL/qt_ru.qm'):
        app.installTranslator( qt_translator )

    menu = JSONMenuLoader(u'menu_WorkplaceManage.json').load()
    MainWindow = MainWnd(u'Рабочее место начальника', menu)
    
    app.processEvents();
    print 'show1'
#    QMessageBox.warning(none, u"Предупреждение", u"Ошибка определения серии", QMessageBox.Ok)
    MainWindow.show()
    print 'show2'
    app.processEvents();
    print 'show3'
    splash.finish(MainWindow);
    print 'show4'

    sys.exit(app.exec_())

if u'__main__' == __name__:
    main()

