#coding=utf-8
u"""
Комбобокс с кнопкой эллипсиса для выбора из связанного справочника
"""
from PyQt5.QtCore import pyqtProperty, QSize, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import  QKeyEvent
from PyQt5.QtWidgets import QWidget, QToolButton, QComboBox, QHBoxLayout
from dpframe.tech.typecheck import *

class EllipsisComboBox(QWidget):

    class _ResettableComboBox(QComboBox):

        @takes('_ResettableComboBox', QKeyEvent)
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Delete:
                self.setCurrentIndex(-1)
            else:
                super(EllipsisComboBox._ResettableComboBox, self).keyPressEvent(event)


    ellipsis = pyqtSignal(str)

    @takes('EllipsisComboBox', QWidget)
    def __init__(self, parent=None):
        super(EllipsisComboBox, self).__init__(parent)
        self._reference = None
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.cbCombo = self._ResettableComboBox(self)
        self.cbCombo.setObjectName(u'cbCombo')
        self.horizontalLayout.addWidget(self.cbCombo)
        self.tbEllipsis = QToolButton(self)
        self.tbEllipsis.setObjectName(u'tbEllipsis')
        self.tbEllipsis.setText(u'...')
        self.tbEllipsis.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.tbEllipsis)
        self.tbClear = QToolButton(self)
        self.tbClear.setObjectName(u'tbClear')
        self.tbClear.setText(u'X')
        self.tbClear.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.tbClear)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setFocusProxy(self.cbCombo)

        self.tbEllipsis.clicked.connect(self.ellipsisPressed)
        self.tbClear.clicked.connect(self.clear)

    @pyqtSlot()
    def ellipsisPressed(self):
        self.ellipsis.emit(self.reference)

    @pyqtSlot()
    def clear(self):
        self.comboBox.setCurrentIndex(-1)


    @property
    def comboBox(self):
        return self.cbCombo

    def isEllipsisVisible(self):
        return self.tbEllipsis.isVisible()

    def setEllipsisVisible(self, value):
        self.tbEllipsis.setVisible(value)

    def isClearVisible(self):
        return self.tbClear.isVisible()

    def setClearVisible(self, value):
        self.tbClear.setVisible(value)

    def getReference(self):
        return self._reference

    def setReference(self, value):
        self._reference = value

    reference = pyqtProperty(str, getReference, setReference)

    # Свойства комбобокса
    def getEditable(self):
        return self.comboBox.isEditable()

    def setEditable(self, value):
        self.comboBox.setEditable(value)

    def getMaxVisibleItems(self):
        return self.comboBox.maxVisibleItems()

    def setMaxVisibleItems(self, value):
        self.comboBox.setMaxVisibleItems(value)

    def getMaxCount(self):
        return self.comboBox.maxCount()

    def setMaxCount(self, value):
        self.comboBox.setMaxCount(value)

    def getIconSize(self):
        return self.comboBox.iconSize()

    def setIconSize(self, value):
        self.comboBox.setIconSize(value)

    def getDuplicatesEnabled(self):
        return self.comboBox.duplicatesEnabled()

    def setDuplicatesEnabled(self, value):
        self.comboBox.setDuplicatesEnabled(value)

    editable = pyqtProperty(bool, getEditable, setEditable)
    maxVisibleItems = pyqtProperty(int, getMaxVisibleItems, setMaxVisibleItems)
    maxCount = pyqtProperty(int, getMaxCount, setMaxCount)
    iconSize = pyqtProperty(QSize, getIconSize, setIconSize)
    duplicatesEnabled = pyqtProperty(bool, getDuplicatesEnabled, setDuplicatesEnabled)
    ellipsisVisible = pyqtProperty(bool, isEllipsisVisible, setEllipsisVisible)
    clearVisible = pyqtProperty(bool, isClearVisible, setClearVisible)

