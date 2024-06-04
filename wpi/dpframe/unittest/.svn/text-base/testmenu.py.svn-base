#!/usr/bin/env python
#coding=utf-8

import unittest
import sys
from PyQt4.QtGui import QApplication, QAction, QMenu

from dpframe.gui.mainwnd import BaseMDIMainWnd
from dpframe.gui.menuloaders import JSONMenuLoader

class TestMainMenu(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        menu = JSONMenuLoader(u'./examples/gui/mainwnd/menu.json').load()
        self.mainwnd = BaseMDIMainWnd(u'Example Main Window', menu)

    def testTopMenuCount(self):
        self.assertEqual(len(self.mainwnd.menuBar().actions()), 3)

    def testMenuItemsCount(self):
        self.assertEqual(len(self.mainwnd.ui.items), 14)

    def testMenuItemsExists(self):
        self.assertTrue(u'refs.refPeople' in self.mainwnd.ui.items)
        self.assertTrue(u'file.exit' in self.mainwnd.ui.items)
        self.assertTrue(u'file.-' in self.mainwnd.ui.items)
        self.assertTrue(u'edit.search.search' in self.mainwnd.ui.items)
        self.assertTrue(u'edit.search' in self.mainwnd.ui.items)
        self.assertTrue(u'edit' in self.mainwnd.ui.items)
        self.assertTrue(u'edit.paste' in self.mainwnd.ui.items)
        self.assertTrue(u'refs' in self.mainwnd.ui.items)
        self.assertTrue(u'edit.search.replace' in self.mainwnd.ui.items)
        self.assertTrue(u'refs.refCountry' in self.mainwnd.ui.items)
        self.assertTrue(u'file' in self.mainwnd.ui.items)
        self.assertTrue(u'edit.copy' in self.mainwnd.ui.items)
        self.assertTrue(u'file.open' in self.mainwnd.ui.items)
        self.assertTrue(u'file.save' in self.mainwnd.ui.items)

    def testMenuItemTypes(self):
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'refs.refPeople'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'file.exit'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'file.-'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit.search.search'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit.search'], QMenu))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit'], QMenu))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit.paste'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'refs'], QMenu))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit.search.replace'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'refs.refCountry'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'file'], QMenu))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'edit.copy'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'file.open'], QAction))
        self.assertTrue(isinstance(self.mainwnd.ui.items[u'file.save'], QAction))

    def testMenuChangeWindowTitle(self):
        self.assertEqual(self.mainwnd.windowTitle(), u'Example Main Window')
        self.mainwnd.ui.items[u'file.open'].trigger()
        self.assertEqual(self.mainwnd.windowTitle(), u'New Window Title')

    def testToolbarsCount(self):
        self.assertEqual(len(self.mainwnd.ui.toolbars), 2)

if __name__ == u'__main__':
    unittest.main()