#coding=UTF-8
u"""
TableView с кнопками перемещения курсора

Created on 16.06.2012
#123
@author: YuSer
"""

from PyQt4.Qt import QSizePolicy
from PyQt4.QtCore import pyqtProperty, QSize, Qt, pyqtSlot, pyqtSignal, QModelIndex, QVariant, QRectF, QMetaEnum
from PyQt4.QtGui import QWidget, QTableView, QToolButton, QVBoxLayout, QHBoxLayout, QBoxLayout, QFrame, QFont, QItemDelegate, QPixmap

from PyQt4.QtGui import QGridLayout, QLabel, QComboBox, QDialog, QLineEdit, QDialogButtonBox, QSpacerItem, QFileDialog
from dpframe.tech.AttrDict import AttrDict

from PyQt4.QtGui import QApplication, QAbstractItemView, QIcon
from PyQt4.QtSql import QSqlQueryModel
from dpframe.base.inits import db_connection_init

class DlgAddButton(QDialog):

    def __init__(self, parent=None, _env=None):
        super(DlgAddButton, self).__init__(parent)

        self.setWindowTitle(u"Установка параметров кнопки")
        self.resize(350, 170)
        
        self.mainLayout = QGridLayout(self)
#        self.mainLayout.setSpacing(0)
#        self.mainLayout.setMargin(0)
        self.mainLayout.setObjectName(u'mainLayout')

        self.lbPosition = QLabel(self)
        self.lbPosition.setText(u"Позиция")
        self.lbPosition.setObjectName(u'lbPosition')

        self.cbPosition = QComboBox(self)
        self.cbPosition.setObjectName(u'cbPosition')
        self.cbPosition.addItem(u"Не задано", 0)
        self.cbPosition.addItem(u"Справа вверху", 1)
        self.cbPosition.addItem(u"Слева вверху", 2)
        self.cbPosition.addItem(u"Справа внизу", 3)
        self.cbPosition.addItem(u"Слева внизу", 4)
        self.cbPosition.setFocusPolicy(Qt.NoFocus)

        self.lbName = QLabel(self)
        self.lbName.setText(u"Имя кнопки")
        self.lbName.setObjectName(u'lbName')

        self.leName = QLineEdit(self)
        self.leName.setObjectName(u'leName')

        self.lbText = QLabel(self)
        self.lbText.setText(u"Текст кнопки")
        self.lbText.setObjectName(u'lbText')

        self.leText = QLineEdit(self)
        self.leText.setObjectName(u'leText')

        self.lbIcon = QLabel(self)
        self.lbIcon.setText(u"Иконка для кнопки")
        self.lbIcon.setObjectName(u'lbIcon')

        self.btnIcon = QToolButton(self)
        self.btnIcon.setObjectName(u'btnIcon')
        self.btnIcon.setText(u'Иконка')
        self.btnIcon.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.btnIcon.setMinimumSize(QSize(0, 30))

        self.dlgBtn = QDialogButtonBox(self)
        self.btnOk = self.dlgBtn.addButton(self.dlgBtn.Ok)
        self.btnCancel = self.dlgBtn.addButton(self.dlgBtn.Cancel)        

        self.mainLayout.addWidget(self.lbPosition, 0, 0)
        self.mainLayout.addWidget(self.cbPosition, 0, 1)

        self.mainLayout.addWidget(self.lbName, 1, 0)
        self.mainLayout.addWidget(self.leName, 1, 1)

        self.mainLayout.addWidget(self.lbText, 2, 0)
        self.mainLayout.addWidget(self.leText, 2, 1)

        self.mainLayout.addWidget(self.lbIcon, 3, 0)
        self.mainLayout.addWidget(self.btnIcon, 3, 1, 2, 1)
        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 0, 1, 1)

        self.mainLayout.addWidget(self.dlgBtn, 5, 0, 1, 2)

        self.mainLayout.setColumnStretch(1, 0)
        
        self.setLayout(self.mainLayout)
        
        self.btnIcon.clicked.connect(self.selectIcon)
        

    def selectIcon(self):
        dlg = QFileDialog(self) 
        filename = dlg.getOpenFileName()
        from os.path import isfile
        if isfile(filename):
            icon = QIcon(filename)
            if not icon.isNull():
                self.btnIcon.setIcon(icon)
            else:
                self.btnIcon.setIcon(QIcon())
        else:
            self.btnIcon.setIcon(QIcon())

class DelegateIcon(QItemDelegate):
    
    def __init__(self, _owner, _iImageColumn):
        super(QItemDelegate, self).__init__(_owner)
        self.iImageColumn = _iImageColumn

    def paint_image(self, _painter, _option, _index):
        pixmap = QPixmap(_index.data().toString())
        _painter.save()
        _painter.drawPixmap(_option.rect, pixmap) 
        _painter.restore()
 
    def paint(self, _painter, _option, _index):
        if self.iImageColumn == _index.column():
            self.paint_image(_painter, _option, _index)
        else:
            QItemDelegate.paint(self, _painter, _option, _index)
            

class DPGrid(QWidget):

    btnPressed = pyqtSignal(QWidget, bool)
    rowChanged = pyqtSignal(QVariant)

    def __init__(self, parent=None, _env=None):
        super(DPGrid, self).__init__(parent)

        self.env = _env
        self.buttonState = 0
        self.btnSize = 30
        self.sKeyFieldName = u""
        self.stringQuery = u"" 
        self.btnContainer = AttrDict()
        
        self.iLayoutDirection = 0
        self.verticalLayout = QBoxLayout(self.iLayoutDirection, self)
        
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u'verticalLayout')
        
        self.hlUp = QBoxLayout(self.rotate_direction(self.iLayoutDirection))
        self.hlUp.setSpacing(0)
        self.hlUp.setMargin(0)
        self.hlUp.setObjectName(u'hlUp')

        self.hlDown = QBoxLayout(self.rotate_direction(self.iLayoutDirection))
        self.hlDown.setSpacing(0)
        self.hlDown.setMargin(0)
        self.hlDown.setObjectName(u'hlDown')

        self.tbUp = QToolButton(self)
        self.tbUp.setObjectName(u'tbUp')
        self.tbUp.setText(u'Up')
        self.tbUp.setMinimumSize(QSize(0, self.btnSize))
        self.tbUp.setFocusPolicy(Qt.NoFocus)
        self.tbUp.setArrowType(Qt.UpArrow)

        self.tbDownForHorizontal = QToolButton(self)
        self.tbDownForHorizontal.setObjectName(u'tbDownForHorizontal')
        self.tbDownForHorizontal.setText(u'Down')
        self.tbDownForHorizontal.setMinimumSize(QSize(0, self.btnSize))
        self.tbDownForHorizontal.setFocusPolicy(Qt.NoFocus)
        self.tbDownForHorizontal.setArrowType(Qt.DownArrow)
        
        self.table = QTableView(self)
        self.table.setObjectName(u'table')
        self.table.setFrameShape(QFrame.Box)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setDefaultSectionSize(self.btnSize) 
#        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.horizontalHeader().setCascadingSectionResizes(True) 
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True) 
        self.table.setWordWrap(True)
        self.table.setAutoScroll(True)
        
        #Фиксируем палитру, вне зависимости от того Активен/Недоступен Стиль отображения активной записи должен быть одинаков
        palette = self.table.palette()
        palette.setColor(palette.Inactive, palette.Highlight, palette.color(palette.Active, palette.Highlight))
        palette.setColor(palette.Disabled, palette.Highlight, palette.color(palette.Active, palette.Highlight))
        palette.setColor(palette.Inactive, palette.HighlightedText, palette.color(palette.Active, palette.HighlightedText))
        palette.setColor(palette.Disabled, palette.HighlightedText, palette.color(palette.Active, palette.HighlightedText))
        self.table.setPalette(palette) 
        
        
        self.tbDown = QToolButton(self)
        self.tbDown.setObjectName(u'tbDown')
        self.tbDown.setText(u'Down')
        self.tbDown.setMinimumSize(QSize(0, self.btnSize))
        self.tbDown.setFocusPolicy(Qt.NoFocus)
        self.tbDown.setArrowType(Qt.DownArrow)

        self.verticalLayout.addLayout(self.hlUp)
        self.verticalLayout.addWidget(self.table)

        self.verticalLayout.addLayout(self.hlDown)
        self.hlUp.addWidget(self.tbUp)
        self.hlUp.addWidget(self.tbDownForHorizontal)
        self.hlDown.addWidget(self.tbDown)

        self.setFocusProxy(self.table)
        self.setFocusPolicy(self.table.focusPolicy())

        self.tbUp.clicked.connect(self.UpPressed)
        self.tbDown.clicked.connect(self.DownPressed)
        self.tbDownForHorizontal.clicked.connect(self.DownPressed)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)
         
        self.table.selectionModel().currentRowChanged.connect(self.change_row)
        self.table.selectionModel().currentColumnChanged.connect(self.change_column)

        self.iImageColumn = None
 
#    def closeEvent(self, event):
#        print "close"
#        for btn_name, widget in self.btnContainer.iteritems():
#            widget.clicked.disconnect(self.pressButton)
#            widget.close()
#            if btn_name == "": pass
#        self.btnContainer.clear()

    def rotate_direction(self, _iDirection):
        u"""        
        QBoxLayout::LeftToRight    0    Horizontal from left to right.
        QBoxLayout::RightToLeft    1    Horizontal from right to left.
        QBoxLayout::TopToBottom    2    Vertical from top to bottom.
        QBoxLayout::BottomToTop    3    Vertical from bottom to top.
        """
        rotateDict = {0:2, 1:3, 2:0, 3:1}
        return rotateDict[min(max(_iDirection, 0), 3)]
        

    def create(self, window = 0, initializeWindow = True, destroyOldWindow = True):
        super(QWidget, self).create(window, initializeWindow, destroyOldWindow)
 
    def ensurePolished(self):
        super(QWidget, self).ensurePolished()
        
#    def setupUi(self, widget):
#        pass
 
    def change_column(self, currentIndex, previousIndex):
        #TODO: Не осилил ресайз последней колонки, из-за этого при выделении последней записи прокручиватся в правво (autoscroll отключать нельзя). ПО этому тупо перепозиционируюсь на первую колонку
        if 1 != currentIndex.column():
            self.table.setCurrentIndex(self.table.model().index(currentIndex.row(), 1, QModelIndex()))
 
    def change_row(self, _index, prev = QModelIndex()):
        rt = _index.row()
        if 0 == self.buttonState:
            self.tbUp.setEnabled(rt != 0)
            self.tbDown.setEnabled(rt != self.table.model().rowCount() - 1)
            self.tbDownForHorizontal.setEnabled(rt != self.table.model().rowCount() - 1)
        self.rowChanged.emit(self.get_value_by_name(self.getKeyFieldName()))
 
    @pyqtSlot(bool)
    def pressButton(self, _checked):
        button = self.sender()
        self.btnPressed.emit(button, _checked)

    def showEvent(self, _event):
        if -1 == self.table.currentIndex().row():
            self.table.selectRow(0)
        QWidget.showEvent(self, _event)

    def set_position(self, _tableViewWidget, _row_coeficent):
        u"""Перемещение по TableView _tableViewWidget,
        на количество строк _row_coeficent.
        Направление зависит от знака"""
        index = _tableViewWidget.currentIndex()
        if index.column() != -1:
            column = index.column()
        else:
            column = 0
        if index.row() != -1:
            row = index.row()
        else:
            row = 0
#        newRow = min(row + _row_coeficent, _tableViewWidget.model().rowCount() - 1)
        newRow = row + _row_coeficent
        newIndex = _tableViewWidget.model().index(newRow, column)
        if newIndex.isValid():
            _tableViewWidget.setFocus()
            _tableViewWidget.selectRow(newRow)
#        bRes = False
#        if _row_coeficent < 0:
#            if row + _row_coeficent > 0:
#                bRes = True
#        else:
#            if row + _row_coeficent < _tableViewWidget.model().rowCount() - 1:
#                bRes = True
#        return bRes

    def set_image_column(self, _iColumn, _imageSize):
        self.iImageColumn = _iColumn
        self.imageSize = _imageSize
        if None != _iColumn:
            self.table.setItemDelegate(DelegateIcon(self.table, _iColumn))
        else:
            self.table.setItemDelegate(QItemDelegate(self.table))
    
    def set_query(self, _query):
        self.stringQuery = _query 
        self.table.model().setQuery(self.stringQuery, self.env.db)
        if self.table.model().query().lastError().isValid():
            raise Exception(self.table.model().query().lastError().text())
#        self.table.resizeColumnsToContents()
#        self.table.selectionModel().currentRowChanged.connect(self.change_row)
        self.set_row(1)
        if None != self.iImageColumn:
            self.table.setColumnWidth(self.iImageColumn, self.imageSize.width())


    def addButton(self, _pos, _name, _text, _icon=QIcon(), _bStreech=False):
        u"""
        _pos - расположение кнопки:
            1 = "Справа вверху"
            2 = "Слева вверху"
            3 = "Справа внизу"
            4 = "Слева внизу"
        _name - имя кнопки (в коде)
        _text - надпись на кнопке
        _icon - иконка на кнопке
        """
        btn = QToolButton(self)
        btn.setObjectName(_name)
        btn.setText(_text)
        btn.setMinimumSize(QSize(self.btnSize, self.btnSize))
        btn.setFocusPolicy(Qt.NoFocus)
        btn.setIconSize(QSize(64, 64)) 
        btn.setIcon(_icon)
        btn.setVisible(1 != self.buttonState)
        btn.setProperty(u'bStreech', _bStreech)
        btn.setSizePolicy(self.btn_size_policy(_bStreech))

        hl = None
        cnt = None
        pos = None
        if _pos == 1 or _pos == 2:
            hl = self.hlUp
            cnt = hl.count()
            if _pos == 1:
                pos = cnt
            else:
                pos = 0
        elif _pos == 3 or _pos == 4:
            hl = self.hlDown
            cnt = hl.count()
            if _pos == 3:
                pos = cnt
            else:
                pos = 0
        else:
            btn.setParent(None)
            btn.close()
            #print u"Ошибка позиционирования"
            return
        hl.insertWidget(pos, btn)
        self.btnContainer[_name] = btn
        btn.clicked.connect(self.pressButton)
        return btn 

    @pyqtSlot()
    def UpPressed(self):
        self.set_position(self.table, -1)
#        isVisible = self.set_position(self.table, -1)
#        if 0 == self.buttonState:
#            self.tbUp.setEnabled(isVisible)
#            self.tbDown.setEnabled(True)

    @pyqtSlot()
    def DownPressed(self):
        self.set_position(self.table, 1)
#        isVisible = self.set_position(self.table, 1)
#        if 0 == self.buttonState:
#            self.tbDown.setEnabled(isVisible)
#            self.tbUp.setEnabled(True)

    @property
    def tableView(self):
        return self.table

    @property
    def btnUp(self):
        return self.tbUp

    @property
    def btnDown(self):
        if self.tbDownForHorizontal.isVisible():
            return self.tbDownForHorizontal
        else:
            return self.tbDown
    
    def refresh(self):
        key = self.get_value_by_name(self.sKeyFieldName)
        self.table.selectionModel().currentRowChanged.disconnect(self.change_row)
        self.table.model().setQuery(self.stringQuery, self.env.db)
        self.table.selectionModel().currentRowChanged.connect(self.change_row)
        self.set_row_by_key(key)
    
    def get_row_count(self):
        res = self.table.model().rowCount()
        return res
    
    def get_row(self):
        res = self.table.currentIndex().row() + 1
        return res

    def set_row(self, _row):
        index = self.table.currentIndex()
        col = max(index.column(), 0)
        newIndex = self.table.model().index(_row - 1, col)
        if newIndex.isValid():
            self.table.selectRow(_row - 1)
        self.change_row(self.table.currentIndex())

    def set_row_by_key(self, _value):
        model = self.table.model()
        q = model.query()
        if not q.isSelect():
            return
        numCol = model.record().indexOf(self.sKeyFieldName)
        bRes = False
        for i in xrange(0, model.rowCount()):
            rec = model.record(i)
            if _value == rec.field(numCol).value():
                bRes = True
                break
        if bRes:
            newIndex = model.index(i, 0)
            if newIndex.isValid():
                self.table.scrollTo(newIndex)
                self.table.selectRow(i)

    def get_value_by_name(self, _sField):
        t = self.table
        m = t.model()
        q = m.query()
        if not q.isSelect():
            return
        rec = m.record(t.currentIndex().row())
        numCol = rec.indexOf(_sField)
        return rec.value(numCol)    

    def getButtonSize(self):
        return self.tbUp.minimumHeight()

    def setButtonSize(self, value):
        self.btnSize = value
        self.tbUp.setMinimumHeight(self.btnSize)
        self.tbDown.setMinimumHeight(self.btnSize)
        self.tbDownForHorizontal.setMinimumHeight(self.btnSize)
        for btn_name, widget in self.btnContainer.iteritems():
            widget.setMinimumHeight(self.btnSize)
            if btn_name == "": pass

        self.table.verticalHeader().setDefaultSectionSize(self.btnSize)
        sz = int(self.btnSize / 3.75)
        font = QFont(self.table.font().family(), sz, QFont.Normal);
        self.table.setFont(font);

    buttonSize = pyqtProperty(int, getButtonSize, setButtonSize)

    def getButtonVisible(self):
        return self.buttonState

    def setButtonVisible(self, value):
        self.buttonState = value
        bSet = (1 != self.buttonState)
        self.tbUp.setVisible(bSet)
#        self.tbDown.setVisible(bSet)
        for btn_name, widget in self.btnContainer.iteritems():
            widget.setVisible(bSet)
            if btn_name == "": pass

    buttonVisible = pyqtProperty(Qt.ScrollBarPolicy, getButtonVisible, setButtonVisible)
    
    def getKeyFieldName(self):
        return self.sKeyFieldName

    def setKeyFieldName(self, value):
        self.sKeyFieldName = value

    keyFieldName = pyqtProperty("QString", getKeyFieldName, setKeyFieldName)

    def getCode(self):
        self._code = self.toPlainText()
        return self._code
    
    def setCode(self, text):
        self.setPlainText(text)
    
    showFields = pyqtProperty("QVariant", getCode, setCode)
    
    def getArrowTypeUp(self):
        return self.tbUp.arrowType()

    def setArrowTypeUp(self, value):
        self.tbUp.setArrowType(value)

    arrowTypeUp = pyqtProperty(Qt.ArrowType, getArrowTypeUp, setArrowTypeUp)

    def getIconUp(self):
        return self.tbUp.icon()

    def setIconUp(self, value):
        self.tbUp.setIcon(value)

    iconUp = pyqtProperty(QIcon, getIconUp, setIconUp)

    def getIconSizeUp(self):
        return self.tbUp.iconSize()

    def setIconSizeUp(self, value):
        if value.isValid() and self.tbUp.iconSize() != value:
            self.tbUp.setIconSize(value)

    iconSizeUp = pyqtProperty(QSize, getIconSizeUp, setIconSizeUp)

    def getArrowTypeDown(self):
        return self.tbDown.arrowType()

    def setArrowTypeDown(self, value):
        self.tbDown.setArrowType(value)
        self.tbDownForHorizontal.setArrowType(value)

    arrowTypeDown = pyqtProperty(Qt.ArrowType, getArrowTypeDown, setArrowTypeDown)

    def getIconDown(self):
        return self.tbDown.icon()

    def setIconDown(self, value):
        self.tbDown.setIcon(value)
        self.tbDownForHorizontal.setIcon(value)

    iconDown = pyqtProperty(QIcon, getIconDown, setIconDown)

    def getIconSizeDown(self):
        return self.tbDown.iconSize()

    def setIconSizeDown(self, value):
        if value.isValid() and self.tbDown.iconSize() != value:
            self.tbDown.setIconSize(value)
            self.tbDownForHorizontal.setIconSize(value)

    iconSizeDown = pyqtProperty(QSize, getIconSizeDown, setIconSizeDown)
    
    def is_horizontal(self):
        return self.iLayoutDirection in (0, 1)

    def btn_size_policy(self, _bStreech = False):
        if _bStreech:
            strechPolicy = QSizePolicy.Expanding
        else:
            strechPolicy = QSizePolicy.Minimum
            
#        if (self.is_horizontal()):
#            btnSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
#        else:
#            btnSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        if (self.is_horizontal()):
            btnSizePolicy = QSizePolicy(QSizePolicy.Minimum, strechPolicy)
        else:
            btnSizePolicy = QSizePolicy(strechPolicy, QSizePolicy.Minimum)
        return btnSizePolicy


    def set_btn_size_policy(self):
        for btn_name, widget in self.btnContainer.iteritems():
            widget.setSizePolicy(self.btn_size_policy(widget.property(u'bStreech').toBool()))


    def set_direction(self, _iDirection):
        self.iLayoutDirection = min(max(_iDirection, 0), 3)
        
        self.verticalLayout.setDirection(self.iLayoutDirection)
        self.hlUp.setDirection(self.rotate_direction(self.iLayoutDirection))
        self.hlDown.setDirection(self.rotate_direction(self.iLayoutDirection))
        
        btnSizePolicy = self.btn_size_policy(True)
        self.tbUp.setSizePolicy(btnSizePolicy)
        self.tbDown.setSizePolicy(btnSizePolicy)
        self.tbDownForHorizontal.setSizePolicy(btnSizePolicy)
        
        if self.is_horizontal():
            self.tbDown.setVisible(False)
            self.tbDownForHorizontal.setVisible(True)
        else:
            self.tbDown.setVisible(True)
            self.tbDownForHorizontal.setVisible(False)
        self.set_btn_size_policy()
          
        return self.iLayoutDirection
        
    def get_direction(self):
        return self.iLayoutDirection
#        return self.verticalLayout.direction()
    
    direction = pyqtProperty(int, get_direction, set_direction)


def test_widget(objEnv):
    import sys

    app = QApplication(sys.argv)

    MainWindow = DPGrid(None, objEnv.getEnv())
    MainWindow.direction = 1
#    MainWindow.buttonVisible = 2 # надо задавать до set_query
    MainWindow.set_image_column(0, QSize(24, 24))
#    MainWindow.set_query("SELECT ':/ico/ico/warning_64.png', i.id, sn.serialnumber, tm.createdatetime FROM item i INNER JOIN serial_number sn ON sn.id = i.serial_number INNER JOIN test_map tm ON tm.id = i.test_map")
    MainWindow.set_query("SELECT ':/ico/ico/warning_64.png', i.id FROM item i INNER JOIN serial_number sn ON sn.id = i.serial_number INNER JOIN test_map tm ON tm.id = i.test_map")
    MainWindow.keyFieldName = u"serialnumber"
    
    def testtest(sender, checked):
        if sender.objectName() == u"btnTest":
#            MainWindow.set_query(u"SELECT id,FullName FROM transformer LIMIT 2")
#            print "val", MainWindow.get_value_by_name(u"serialnumber").toString()
#            MainWindow.set_row_by_key("34505")
#            MainWindow.refresh()
            dlg = DlgAddButton(MainWindow)
            dlg.show()
#            MainWindow.buttonVisible = 1
        elif sender.objectName() == u"btnUpRight":
            MainWindow.buttonSize = MainWindow.buttonSize + 5
        elif sender.objectName() == u"btnUpLeft":
            MainWindow.buttonSize = MainWindow.buttonSize - 5

            
        print sender.objectName(), sender.text(), checked

    MainWindow.btnPressed.connect(testtest)
    MainWindow.addButton(1, u"btnUpRight", u"Жопа справа вверху")
    MainWindow.addButton(2, u"btnUpLeft", u"Жопа слева вверху")
    MainWindow.addButton(3, u"btnDownRight", u"Жопа справа внизу")
    MainWindow.addButton(4, u"btnDownLeft", u"Жопа слева внизу")
    MainWindow.addButton(4, u"btnDownLeft2", u"Жопа слева внизу2")
    MainWindow.addButton(3, u"btnDownRight2", u"Жопа справа внизу2", QIcon(), True)

    MainWindow.addButton(1, u"btnTest", u"!!!")

#    MainWindow.buttonSize = 35

    app.processEvents();
    MainWindow.show()
    app.processEvents();

    exitRes = app.exec_()
    MainWindow.btnPressed.disconnect(testtest)
    sys.exit(exitRes)

if u'__main__' == __name__:
    import electrolab.gui.ui.ico_64_rc
    @db_connection_init
    class ForEnv(QWidget):
        def getEnv(self):
            return self.env

    objEnv = ForEnv()
    test_widget(objEnv)
