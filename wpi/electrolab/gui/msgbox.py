#-*- coding: UTF-8 -*-
u"""
Стандартные диалоги для сенсорного экрана

Created on 04.08.2012
#130
@author: YuSer
"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import  QPixmap, QIcon, QFont
from PyQt5.Qt import QSizePolicy
from PyQt5.QtWidgets import QDialog, QMessageBox, QGridLayout, QToolButton, QApplication, QLabel, QSpacerItem
#import electrolab.gui.ui.ico_rc
# import electrolab.gui.ui.ico_64_rc

DLGYES = 1
DLGYESNO = 2
DLGYESNOCANCEL = 3
DLGOK = 4
DLGOKCLOSE = 5
DLGOKCLOSECANCEL = 6

class StdDlg(QDialog):
#    btnYesPressed = pyqtSignal(QWidget, bool)
#    btnNoPressed = pyqtSignal(QWidget, bool)
#    btnCancelPressed = pyqtSignal(QWidget, bool)

    def __init__(self, parent=None, mode=DLGYESNOCANCEL, _sText=u""):
        super(StdDlg, self).__init__(parent)

        self.mode = mode
        self.dlgLayout = QGridLayout(self)
        self.dlgLayout.setObjectName(u'dlgLayout')
        
        self.txtLayout = QGridLayout()
        self.txtLayout.setObjectName(u'txtLayout')
        
        self.lblIco = QLabel(self)
        self.lblIco.setObjectName(u'lblIco')
        self.lblIco.setText(u'ICO')
        self.lblIco.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.lblIco.setPixmap(QPixmap(u':/ico/ico/warning_64.png'))
#        self.setStyleSheet("QLabel { border: 1px solid #000000; }")

        self.lblTxt = QLabel(self)
        self.lblTxt.setObjectName(u'lblTxt')
        self.lblTxt.setText(_sText)
        self.lblTxt.setFont(QFont('MS Shell Dlg 2', 16))
        self.lblTxt.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.tbYes = QToolButton(self)
        self.tbYes.setObjectName(u'tbYes')
        txtYes = u'Да'
        if self.mode > 3:
            txtYes = u'ОК'
        self.tbYes.setText(txtYes)
        self.tbYes.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.tbYes.setFont(QFont('MS Shell Dlg 2', 14))
        self.tbYes.setIcon(QIcon(u':/ico/ico/tick_64.png'))
        self.tbYes.setIconSize(QSize(64, 64))
        self.tbYes.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbYes.setFocusPolicy(Qt.NoFocus)

        self.tbNo = QToolButton(self)
        self.tbNo.setObjectName(u'tbNo')
        txtNo = u'Нет'
        if self.mode > 3:
            txtNo = u'Закрыть'
        self.tbNo.setText(txtNo)
        self.tbNo.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.tbNo.setFont(QFont('MS Shell Dlg 2', 14))
        self.tbNo.setIcon(QIcon(u':/ico/ico/delete_64.png'))
        self.tbNo.setIconSize(QSize(64, 64))
        self.tbNo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tbNo.setFocusPolicy(Qt.NoFocus)
        
        self.tbCancel = QToolButton(self)
        self.tbCancel.setObjectName(u'tbCancel')
        self.tbCancel.setText(u'Отмена')
        self.tbCancel.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.tbCancel.setFont(QFont('MS Shell Dlg 2', 14))
        self.tbCancel.setIcon(QIcon(u':/ico/ico/block_64.png'))
        self.tbCancel.setIconSize(QSize(64, 64))
        self.tbCancel.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
#        self.tbCancel.setMinimumSize(QSize(64, 64))
        self.tbCancel.setFocusPolicy(Qt.NoFocus)
        
        self.txtLayout.addWidget(self.lblIco, 0, 0)
        self.txtLayout.addWidget(self.lblTxt, 0, 1, 2, 1)
        self.txtLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 1, 0)

        self.dlgLayout.addLayout(self.txtLayout, 0, 0, 1, 3)
        self.dlgLayout.addWidget(self.tbYes, 1, 0)
        self.dlgLayout.addWidget(self.tbNo, 1, 1)
        self.dlgLayout.addWidget(self.tbCancel, 1, 2)

        self.tbYes.clicked.connect(self.closed)
        self.tbNo.clicked.connect(self.closed)
        self.tbCancel.clicked.connect(self.closed)

        if 1 == self.mode or 4 == self.mode:
            self.tbNo.setVisible(False)
            self.tbCancel.setVisible(False)
            
        if 2 == self.mode or 5 == self.mode:
            self.tbCancel.setVisible(False)
            
#        self.setWindowFlags(self.windowFlags() | QtCore.Qt.SplashScreen)
        self.setWindowFlags(Qt.SplashScreen)
        self.setStyleSheet("QDialog { border: 2px solid palette(shadow); }")
        self.cnt = 0

    def closeEvent(self, event):
        pass # убирать нельзя!!!
#        print self.cnt, self.sender()
#        if self.sender() == None:
#            self.cnt = self.cnt + 1
#            event.ignore()

    def closed(self):
        if (self.sender() == self.tbYes):
#            print "yes!"
            self.setResult(QMessageBox.Yes if self.mode <= 3 else QMessageBox.Ok)
            self.close()
        if (self.sender() == self.tbNo):
#            print "no!"
            self.setResult(QMessageBox.No if self.mode <= 3 else QMessageBox.Close)
            self.close()
        if (self.sender() == self.tbCancel):
#            print "cancel!"
            self.setResult(QMessageBox.Cancel)
            self.close()
        else:
            return

def getTrue(parent, _sText):
    u"""
    if getTrue(u"Процесс может затянуться. Затянуться?"):
        pass
    """
    mb = StdDlg(parent, DLGYESNO, _sText)
    return (mb.exec_() == QMessageBox.Yes)

def msgBox(parent, _sText):
    u"""
    """
    mb = StdDlg(parent, DLGOK, _sText)
    return (mb.exec_() == QMessageBox.Yes)

def msgBox3(parent, _sText):
    mb = StdDlg(parent, DLGYESNOCANCEL, _sText)
    return mb.exec_()




if u'__main__' == __name__:
    import sys

    app = QApplication(sys.argv)

    MainWindow = StdDlg(None, DLGYESNOCANCEL , u'Случилась какая-то неведомая фигня.\nНужно все пропатчить и заапдейтить.')
    res = MainWindow.exec_()
    if res == QMessageBox.Cancel:
        print(u"отмена")
    elif res == QMessageBox.Yes:
        print(u"да")
    elif res == QMessageBox.No:
        print(u"нет")
    else:
        print(u"чозафигня?")
#    tmp = app.exec_()
#    sys.exit(tmp)
    sys.exit()
