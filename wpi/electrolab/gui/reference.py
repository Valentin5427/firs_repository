#-*- coding: UTF-8 -*-
u"""
Created on 09.08.2011

@author: yuser
"""

import os

from PyQt5.QtCore import QModelIndex, QVariant, QSize, Qt, QObject, QRect, QEvent, QStringListModel
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QLabel, QDialog, QDataWidgetMapper, QComboBox, QCheckBox,  QLineEdit, QItemDelegate,  QAbstractButton,  QInputDialog
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QTableView, QAction,  QSplitter, QWidget
from PyQt5.QtGui import QIcon ,QKeySequence,  QShowEvent, QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QLabel
from PyQt5.QtSql import QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlQuery, QSqlRecord
from dpframe.data.mdmodel import MDRelationalTableModel
from dpframe.data.metadata import Table
from dpframe.tech.AttrDict import AttrDict
from dpframe.tech.typecheck import *
from dpframe.tech.typecheck import env_type
from electrolab.gui.params import FilterContainer, ParamDlg
from electrolab.gui.common import UILoader
from electrolab.gui.ellipsiscombobox import EllipsisComboBox

class NullRelationalDelegate(QSqlRelationalDelegate):

    @takes('NullRelationalDelegate', QWidget, MDRelationalTableModel, QModelIndex)
    @returns(nothing)
    def setModelData(self, widget, model, index):
        if not index.isValid():
            return

        childModel = model.relationModel(index.column())
        if childModel and isinstance(widget, QComboBox): # lookup reference
            currentItem = widget.currentIndex()
            childColIndex = childModel.fieldIndex(model.relation(index.column()).displayColumn())
            childEditIndex = childModel.fieldIndex(model.relation(index.column()).indexColumn())

            displayData = childModel.data(childModel.index(currentItem, childColIndex), Qt.DisplayRole)
            displayData = displayData if displayData.isValid() else QVariant(QVariant.String)

            editData = childModel.data(childModel.index(currentItem, childEditIndex), Qt.EditRole)
            editData = editData if editData.isValid() else QVariant(QVariant.Int)

            model.setData(index, displayData, Qt.DisplayRole)
            model.setData(index, editData, Qt.EditRole)
        elif isinstance(widget, QComboBox): # enum combobox
            model.setData(index, QVariant(widget.currentIndex()))
            model.setData(index, QVariant(widget.currentText()), Qt.DisplayRole)
            #TODO: разобраться, после этого кода в DisplayRole все равно currentIndex вместо currentText
        else: #plain values
            QItemDelegate.setModelData(self, widget, model, index)

    def setEditorData(self, widget, index):
        model = index.model()
        if isinstance(widget, QComboBox) and model.relationModel(index.column()):
            QSqlRelationalDelegate.setEditorData(self, widget, index)
        elif isinstance(widget, QComboBox) and model._metadata.fields[unicode(widget.property(u'field').toString())].enum:
            widget.setCurrentIndex(model.data(index).toInt()[0])
        else:
            QItemDelegate.setEditorData(self, widget, index)

#    def createEditor(self, parent, option, index):
#        mdenum = None
#        model = index.model()
#        for mdfld in model._metadata.fields.itervalues:
#            if mdfld.cid == index.column and mdfld.enum:
#                mdenum = mdfld
#
#        if mdenum:
#            combo = QComboBox(parent)
#            combo.setModel(QStringListModel(mdenum.enum))
#            combo.setModelColumn(0)
#            combo.installEventFilter(self)
#            return combo
#        else:
#            return super(NullRelationalDelegate, self).createEditor(parent, option, index)


class RefMapper(QDataWidgetMapper):

    @takes('RefMapper', Table)
    def __init__(self, metadata):
        super(RefMapper, self).__init__()
        self.metadata = metadata

    @takes('RefMapper', QWidget)
    @returns(nothing)
    def mapping(self, widget, fld_name):
        fld_index = self.metadata.fields[fld_name].cid
        model = self.model()
        if isinstance(widget, EllipsisComboBox) and self.metadata.fkeys[fld_name].refField:
            widget = widget.comboBox
            rel_model = model.relationModel(fld_index)
            rel_model.select()
            widget.setModel(rel_model)
            dspl_col_idx = rel_model.fieldIndex(model.relation(fld_index).displayColumn())
            widget.setModelColumn(dspl_col_idx)
            widget.model().setSort(dspl_col_idx, Qt.AscendingOrder)
        if isinstance(widget, QComboBox) and self.metadata.fields[fld_name].enum:
            widget.setModel(QStringListModel(self.metadata.fields[fld_name].enum))
            widget.setModelColumn(0)

        self.addMapping(widget, fld_index)

    @takes('RefMapper')
    @returns(nothing)
    def relationsRefresh(self):
        cur_values = {}
        for sect in xrange(len(self.metadata.fields)):
            widget = self.mappedWidgetAt(sect)
            if isinstance(widget, QComboBox):
                cur_values[widget] = widget.currentText()

        self.model().relationsRefresh()

        for widget, text in cur_values.iteritems():
            widget.setCurrentIndex(widget.findText(text))


#TODO: ПЕРЕИМЕНОВАТЬ!!! А еще лучше перенести функции в отдельный модуль
class cZero(object):
    
    def __init__(self, _parent=None):
        self.parent = _parent
    
    def _get_msg_wnd(self, text, infotext=None, detailedtext=None, title=u'electrolab', icon=None, buttons=None, default=None):
        msgbox = QMessageBox(icon or QMessageBox.Information, title, text)
        if infotext:
            msgbox.setInformativeText(infotext)
        if detailedtext:
            msgbox.setDetailedText(detailedtext)
        if title:
            msgbox.setWindowTitle(title)
        if icon:
            msgbox.setIcon(icon)
        if buttons:
            if type(buttons) == QMessageBox.StandardButtons:
                msgbox.setStandardButtons(buttons)
                if default:
                    msgbox.setDefaultButton(default)
            else:
                msgbox.addButton(buttons)
        return msgbox

    def info(self, text, infotext=None, detailedtext=None, title=u'Сообщение'):
        mb = self._get_msg_wnd(text, infotext, detailedtext, title,
                           QMessageBox.Information, QMessageBox.Ok
                          )
        return mb.exec_()

    def warning(self, text, infotext=None, detailedtext=None, title=u'Предупреждение'):
        mb = self._get_msg_wnd(text, infotext, detailedtext, title,
                           QMessageBox.Warning, QMessageBox.Ok
                          )
        return mb.exec_()

    def error(self, text, infotext=None, detailedtext=None, title=u'Ошибка'):
        mb = self._get_msg_wnd(text, infotext, detailedtext, title,
                           QMessageBox.Critical, QMessageBox.Ok
                          )
        return mb.exec_()

    def reportError(self, _lastError, _sMessage = u'Невозможно сохранить данные', _sTitle = u'Ошибка записи данных'):
        if _lastError.isValid():
            self.error(u'Ошибка', _sMessage,
                    os.linesep.join([u'Код: {0}',
                                     u'Сообщение базы данных: {1}',
                                     u'Сообщение драйвера: {2}']).format(_lastError.number(),
                                                                         _lastError.databaseText(),
                                                                         _lastError.driverText()),
                    title=_sTitle
                   )

    def msgBox(self, sText):
        u"""Сообщение"""
        self.info(sText)
        
    def getTrue(self, _sText, _bDef=True):
        u"""
        if cZero().getTrue(u"Процесс может затянуться. Затянуться?", False):
            pass
        """

        mb = self._get_msg_wnd(_sText,
                           None,
                           None,
                           u'Сообщение',
                           QMessageBox.Information,
                           QMessageBox.StandardButtons(QMessageBox.Yes|QMessageBox.No),
                           QMessageBox.Yes if _bDef == True else QMessageBox.No
                          )
        return (mb.exec_() == QMessageBox.Yes)

    def getCancelTrue(self, _sText, _bDef=True):
        u"""
        res = cZero().getCancelTrue(u"Продолжить выполнение?", False)
        """

        mb = self._get_msg_wnd(_sText,
                           None,
                           None,
                           u'Сообщение',
                           QMessageBox.Information,
                           QMessageBox.StandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel),
                           QMessageBox.Yes if _bDef == True else QMessageBox.No
                          )
        ret = mb.exec_()
        res = None
        if ret != QMessageBox.Cancel:
            res = (ret == QMessageBox.Yes)
        return res
    
    def getInteger(self, _sText, _defValue):
        u"""
        res, btnOkCancel = cZero().getInteger(u"Введите число", 125)
        """
        res, btn = QInputDialog.getInt(QWidget(),
                           u'Сообщение',
                           _sText,
                           _defValue
                           )
        return res, btn   

    def getText(self, _sText):
        u"""
        res, btnOkCancel = cZero().getText(u"Введите текст:")
        """
        res, btn = QInputDialog.getText(QWidget(),
                           u'Сообщение',
                           _sText
                           )
        return res, btn   

class RefDlgContainer(QDialog):

    class Ui(object):

        @takes('Ui', 'RefDlgContainer')
        def __init__(self, Dialog):
            Dialog.setObjectName(u'Dialog')
            Dialog.resize(10, 10)
            self.verticalLayout = QVBoxLayout(Dialog)
            self.verticalLayout.setSpacing(9)
            self.verticalLayout.setObjectName(u'verticalLayout')
            self.widgetLayout = QVBoxLayout()
            self.widgetLayout.setSpacing(6)
            self.widgetLayout.setObjectName(u'widgetLayout')
            self.verticalLayout.addLayout(self.widgetLayout)
            self.buttonBox = QDialogButtonBox(Dialog)
            self.buttonBox.setOrientation(Qt.Horizontal)
            self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
            self.buttonBox.setObjectName(u'buttonBox')
            self.verticalLayout.addWidget(self.buttonBox)


    @takes('RefDlgContainer', QWidget, 'BaseReference')
    def __init__(self, parent, ref):
        QDialog.__init__(self, parent)
        self.ui = self.Ui(self)
        self.dlg = ref.dlg
        self.dlg.setObjectName(u'widget')
        self.ui.widgetLayout.addWidget(self.dlg)
        self.setWindowTitle(self.dlg.params.display)
        self.ui.buttonBox.clicked.connect(self.pressButton)

    @takes('RefDlgContainer')
    @returns(bool)
    def apply_report(self):
        if self.dlg.mapper.submit():
            if self.dlg.model.submitAll():
                return True
            cZero().reportError(self.dlg.mapper.model().lastError())
        else:
            cZero().error(u'Ошибка маппинга')
        return False


    @takes('RefDlgContainer', QShowEvent)
    @returns(nothing)
    def showEvent(self, event):
        try:
            geom = self.dlg.env.session.storage.dialog[self.dlg.name]
        except KeyError:
            return
        except AttributeError:
            return

        self.setGeometry(QRect(geom.x, geom.y, geom.width, geom.height))

    @takes('RefDlgContainer')
    @returns(nothing)
    def saveSession(self):
        rect = self.geometry()
        self.dlg.env.session.storage.dialog[self.dlg.name] = AttrDict()
        self.dlg.env.session.storage.dialog[self.dlg.name].x = rect.x()
        self.dlg.env.session.storage.dialog[self.dlg.name].y = rect.y()
        self.dlg.env.session.storage.dialog[self.dlg.name].width = rect.width()
        self.dlg.env.session.storage.dialog[self.dlg.name].height = rect.height()
        self.dlg.env.session.save()

    @takes('RefDlgContainer', QCloseEvent)
    @returns(nothing)
    def closeEvent(self, event):
        self.dlg.mapper.model().revertAll()
        self.saveSession()

    @takes('RefDlgContainer', QKeyEvent)
    @returns(nothing)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.pressButton(self.ui.buttonBox.button(QDialogButtonBox.Cancel))
        else:
            QDialog.keyPressEvent(self, event)

    @takes('RefDlgContainer', QAbstractButton)
    @returns(nothing)
    def pressButton(self, _btn):
        if self.ui.buttonBox.standardButton(_btn) == QDialogButtonBox.Apply:
            idx = self.dlg.mapper.currentIndex()
            self.apply_report()
            self.dlg.mapper.setCurrentIndex(idx)

        elif self.ui.buttonBox.standardButton(_btn) == QDialogButtonBox.Ok:
            if self.apply_report():
                self.saveSession()
                self.accept()

        elif self.ui.buttonBox.standardButton(_btn) == QDialogButtonBox.Cancel:
            self.dlg.model.revertAll()
            self.saveSession()
            self.reject()


class RefDialog(QDialog, UILoader):
    u""""""

    @takes('RefDialog',  env_type)
    def __init__(self, name, env):
        QDialog.__init__(self)
        self.params = env.refs[name]
        self.name = name
        self.setUI(env.config, self.params.dialog_ui)
        self.model = env.models[self.params.table]
        self.metadata = env.metadata[self.params.table]
        self.env = env

        self.edits_for_mapping = dict([(widget.property(u'field').toString().lower(), widget)
                           for widget in self.ui.__dict__.itervalues()
                           if QVariant.String == widget.property(u'field').type()])

        self.ellipsis = [widget for widget in self.ui.__dict__.itervalues()
                           if isinstance(widget, EllipsisComboBox) and widget.reference
                                and QVariant.String == widget.property(u'field').type()]

        self.mapper = RefMapper(self.metadata)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(NullRelationalDelegate(self.mapper))
        self.automapping()
        self.set_labels()
        self.set_constraints()
        self.connect_ellipsis()
        
    @takes('RefDialog', QKeyEvent)
    @returns(nothing)
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return]:
            event.ignore()
        else:
            QDialog.keyPressEvent(self, event)

    @takes('RefDialog')
    @returns(nothing)
    def automapping(self):
        #автоматический маппинг
        for fld_name, widget in self.edits_for_mapping.iteritems():
            self.mapper.mapping(widget, fld_name)

    @takes('RefDialog')
    @returns(nothing)
    def connect_ellipsis(self):
        for widget in self.ellipsis:
            widget.ellipsis.connect(self.ellipsis_handler)

    @takes('RefDialog')
    @returns(nothing)
    def set_labels(self):
        #устанавливаеm связанным меткам текст из метаданных
        for widget in self.ui.__dict__.itervalues():
            if isinstance(widget, QLabel) and widget.buddy() is not None:
                fld_name = widget.buddy().property(u'field').toString()
            elif isinstance(widget, QCheckBox):
                fld_name = widget.property(u'field').toString()
            else:
                continue
            try:
                widget.setText(self.metadata.fields[fld_name].alias)
            except KeyError:
                pass

    @takes('RefDialog')
    @returns(nothing)
    def set_constraints(self):
        for fld_name, widget in self.edits_for_mapping.iteritems():
            fld_len = self.metadata.fields[fld_name].length
            if isinstance(widget, QLineEdit) and fld_len:
                widget.setMaxLength(fld_len)

    @takes('RefDialog', str)
    @returns(nothing)
    def ellipsis_handler(self, refname):
        refname = refname
        fld_name = QObject().sender().property(u'field').toString()
        widget = QObject().sender().comboBox
        ref_table = self.metadata.fkeys[fld_name].refTable
        ref_show_fld = self.metadata.fkeys[fld_name].refShowField
        selecting = SelectingRefContainer(self,
                                          self.env,
                                          refname,
                                          self.env.metadata[ref_table].fields[ref_show_fld],
                                          widget.currentText())
        res = selecting.exec_()
        self.mapper.relationsRefresh()
        widget.setCurrentIndex(widget.findText(selecting.ret.toString()))
        if QDialog.Accepted == res:
            self.mapper.submit()
            widget.setFocus()


class BaseReference(QDialog):

    # @takes('BaseReference', QWidget,  env_type, optional(bool))
    def __init__(self, parent, name, env, selecting=False):
        super(BaseReference, self).__init__( parent)
        self.name = name
        self.env = env
        self.params = env.refs[name]


    @staticmethod
    @takes(env_type)
    @returns(type)
    def get_ref_class(name, env):
        try:
            return env.refs[name].cls
        except KeyError:
            return Reference

    @staticmethod
    @takes(env_type)
    @returns(type)
    def get_dlg_class(name, env):
        try:
            return env.refs[name].dialog
        except KeyError:
            return RefDialog

    @takes('BaseReference')
    @returns(nothing)
    def saveSession(self):
        pass

class Reference(BaseReference):
    
    class Ui(object):
        
        ICON_SIZE = 32

        # @takes('Ui', 'Reference', optional(QWidget))
        def __init__(self, Dialog, filterDlg=None):
            Dialog.setObjectName(u'Reference')
            self.verticalLayout = QVBoxLayout(Dialog)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setMargin(0)
            self.verticalLayout.setObjectName(u'verticalLayout')
            self.toolBar = QToolBar(Dialog)
            self.toolBar.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
            self.toolBar.setObjectName(u'toolBar')
            self.verticalLayout.addWidget(self.toolBar)
            if filterDlg:
                self.filterContainer = FilterContainer(filterDlg)
                self.verticalLayout.addWidget(self.filterContainer)
                self.filterContainer.filterChanged.connect(Dialog.set_user_filter)
            self.tableView = QTableView(Dialog)
            self.tableView.setEditTriggers(self.tableView.NoEditTriggers)
            self.tableView.setAlternatingRowColors(True)
            self.tableView.setSelectionMode(self.tableView.SingleSelection)
            self.tableView.setSelectionBehavior(self.tableView.SelectRows)
            self.tableView.setSortingEnabled(True)
            self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())
            self.tableView.setObjectName(u'tableView')
            self.verticalLayout.addWidget(self.tableView)
            self.actionInsert = QAction(Dialog)
            self.actionInsert.setIcon(QIcon(u':/EL/ico/add_32.png'))
            self.actionInsert.setObjectName(u'actionInsert')
            self.actionInsert.setToolTip(u'Добавить')
            self.actionInsert.setShortcut(QKeySequence(Qt.Key_Insert))
            self.actionUpdate = QAction(Dialog)
            self.actionUpdate.setEnabled(True)
            self.actionUpdate.setIcon(QIcon(u':/EL/ico/pencil_32.png'))
            self.actionUpdate.setVisible(True)
            self.actionUpdate.setObjectName(u'actionUpdate')
            self.actionUpdate.setToolTip(u'Изменить')
            self.actionDelete = QAction(Dialog)
            self.actionDelete.setIcon(QIcon(u':/EL/ico/trash_32.png'))
            self.actionDelete.setObjectName(u'actionDelete')
            self.actionDelete.setToolTip(u'Удалить')
            self.actionDelete.setShortcut(QKeySequence(Qt.Key_Delete))
            self.actionRefresh = QAction(Dialog)
            self.actionRefresh.setIcon(QIcon(u':/EL/ico/refresh.png'))
            self.actionRefresh.setObjectName(u'actionRefresh')
            self.actionRefresh.setToolTip(u'Обновить')
            self.actionRefresh.setShortcut(QKeySequence(Qt.Key_F5))
            self.toolBar.addAction(self.actionInsert)
            self.toolBar.addAction(self.actionUpdate)
            self.toolBar.addAction(self.actionDelete)
            self.toolBar.addSeparator()
            self.toolBar.addAction(self.actionRefresh)
            self.toolBar.addSeparator()
            self.toolBar.setStyleSheet(u'QToolBar{border:0px}')
    
            self.actionInsert.triggered.connect(Dialog.insert)
            self.actionDelete.triggered.connect(Dialog.delete)
            self.actionUpdate.triggered.connect(Dialog.edit)
            self.actionRefresh.triggered.connect(Dialog.refresh)

    # @takes('Reference', QWidget,  env_type, optional(bool))
    def __init__(self, parent, name, env, selecting=False):
        u""""""
        
        super(Reference, self).__init__(parent, name, env)
        filter_id = env.refs[name].get(u'filter', None)
        self.filter_dlg = ParamDlg.get_dlg_class(filter_id, env)(filter_id, env) if filter_id else None
        self.ui = self.Ui(self, self.filter_dlg)
        self.selecting = selecting

        self.model = env.models[self.params.table]
        self.metadata = env.metadata[self.params.table]

        self.dlg = self.get_dlg_class(name, env)(name, env)
        self.ui.tableView.selectionModel().currentRowChanged.connect(self.dlg.mapper.setCurrentModelIndex)
        self.dlg_container = RefDlgContainer(self.parent() if self.selecting else self, self)

        #TODO: в будущем перенести в конструктор собственного виджета грида
        header = self.ui.tableView.horizontalHeader()
        header.setMovable(True)

        for fld_md in self.metadata.fields.values():
            self.ui.tableView.setColumnHidden(fld_md.cid, not fld_md.visible)
            if fld_md.visiblePosition >= 0:
                header.moveSection(header.visualIndex(fld_md.cid), fld_md.visiblePosition)

        header.setResizeMode(QHeaderView.ResizeToContents)
        #END TODO

        self.ui.tableView.setItemDelegate(NullRelationalDelegate(self.ui.tableView))
        self.ui.tableView.selectionModel().currentRowChanged.connect(self.on_currentRowChanged)
        #Похоже это лишнее телодвижение, тормозит работу        self.ui.tableView.selectRow(0)
        self.ui.tableView.installEventFilter(self)
        if not self.selecting:
            self.ui.tableView.doubleClicked.connect(self.ui.actionUpdate.trigger)

    @takes('Reference', str)
    @returns(nothing)
    def set_user_filter(self, filter):
        self.model.set_filter(u'user', filter)
        self.ui.tableView.setCurrentIndex(self.model.index(0, 0))

    @takes('Reference', QKeyEvent)
    @returns(nothing)
    def keyPressEvent(self, _event):
        if _event.key() != Qt.Key_Escape:
            QDialog.keyPressEvent(self, _event)
        
    @takes('Reference', QShowEvent)
    @returns(nothing)
    def showEvent(self, _event):
        QDialog.showEvent(self, _event)
        self.set_enabled_button(self.ui.tableView.currentIndex().isValid())

    #TODO: разобраться, избавиться от параметров
    # @takes('Reference', bool, optional(bool))
    @returns(nothing)
    def set_enabled_button(self, _bValidPosition, _bEditable=True):
        self.ui.actionUpdate.setEnabled(_bValidPosition and _bEditable)
        self.ui.actionDelete.setEnabled(_bValidPosition and _bEditable and not self.selecting)
        self.ui.actionInsert.setEnabled(_bEditable)

    # @takes('Reference', QModelIndex, optional(QModelIndex))
    @returns(nothing)
    def on_currentRowChanged(self, cur, prev=QModelIndex()):
        self.set_enabled_button(cur.isValid())

    # @takes('Reference', optional(bool))
    @returns(nothing)
    def refresh(self, checked=False):
        u"""Обновить"""
        nrow = self.ui.tableView.currentIndex().row()
        self.model.select()
        for i in range(self.model.columnCount()):
            relmodel = self.model.relationModel(i)
            if relmodel:
                relmodel.select()
        self.ui.tableView.selectRow(nrow)
        currentIndex = self.model.index(nrow, 0, QModelIndex())
        if currentIndex.isValid():
            self.ui.tableView.setCurrentIndex(currentIndex)
        self.set_enabled_button(currentIndex.isValid())

    # @takes('Reference', optional(bool))
    @returns(nothing)
    def insert(self, checked=False):
        tv = self.ui.tableView
        oldnrow = tv.currentIndex().row()
        nrow = self.model.rowCount()
        self.model.relationsRefresh()
        self.model.insertRow(nrow)
        for fld, value in self.model.defaults.iteritems():
            self.model.setData(self.model.index(nrow, self.metadata.fields[fld].cid), QVariant(value))
        tv.selectRow(nrow)
        if QDialog.Rejected == self.edit():
            tv.selectRow(oldnrow)

    # @takes('Reference', optional(bool))
    @returns(int)
    def edit(self, checked=False):
        tv = self.ui.tableView
        cur_idx = tv.currentIndex()
        ret = self.dlg_container.exec_()
        tv.selectRow(cur_idx.row())
        self.refresh()
        return ret

    # @takes('Reference', optional(bool))
    @returns(nothing)
    def delete(self, checked=False):
        tv = self.ui.tableView
        model = self.model
        mindex = tv.currentIndex()
        nrow = mindex.row()
        if QMessageBox.Yes == QMessageBox.question(self, u'Удаление',
                                               u'Удалить запись?',
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.Yes):
            model.removeRow(nrow)
            model.submitAll()
            err = model.lastError()
            if err.isValid():
                #TODO: Сообщение с перечислением таблиц, ссылающихся на запись
                cZero().reportError(err, u'Вероятно, на эту запись ссылаются записи других таблиц.', u'Ошибка удаления записи')
            if nrow >= model.rowCount():
                mindex = model.index(model.rowCount()-1, mindex.column())
            tv.setCurrentIndex(mindex)

    @property
    def model(self):
        return self.ui.tableView.model()

    @model.setter
    def model(self, value):
        self.ui.tableView.setModel(value)
    #
    # @takes('Reference', dict_of(int, unicode), QSqlRecord)
    @returns(bool)
    def _is_match(self, dct_values, record):
        return all(strval == record.value(idx).toString() for idx, strval in dct_values.iteritems())


    # @takes('Reference', dict_of(int, unicode))
    @returns(nothing)
    def selectRow(self, dct_values):
        #TODO: performance - если поле одно и модель по нему сортирована, искать двоичным поиском
        for nrow in range(self.model.rowCount()):
            if self._is_match(dct_values, self.model.record(nrow)):
                self.ui.tableView.selectRow(nrow)
                break


class MasterDetailDlgContainer(QDialog, UILoader):

    def __init__(self, parent, ref):
        super(MasterDetailDlgContainer, self).__init__(parent)
        self.setUI(ref.env.config, u'MasterDetailDlg.ui')
        self.ui.masterDlg = ref.ui.master.dlg_class(ref.cur_idx.row(), ref.name, ref.env)
        self.ui.masterDlg.setObjectName(u'masterDlg')
        self.ui.MasterLayout.addWidget(self.ui.masterDlg)
        self.ui.DetailLayout.addWidget(ref.ui.detail)
        self.ui.buttonBox.clicked.connect(self.ui.masterDlg.pressButton)

        
class MasterDetailReference(BaseReference):
    u"""
    Универсальный справочник. Предназначен для вызова из меню. 
    Читает из входных параметров имя таблицы, имя класса диалога редактирования
    """

    class Ui(object):

        SECTION_TITLE_HEIGHT = 15

        def __init__(self, Dialog):
            Dialog.setObjectName(u'Dialog')
            self.verticalLayout = QVBoxLayout(Dialog)
            self.verticalLayout.setObjectName(u'verticalLayout')
            self.splitter = QSplitter(Dialog)
            self.splitter.setOrientation(Qt.Vertical)
            self.splitter.setChildrenCollapsible(True)
            self.splitter.setObjectName(u'splitter')
            self.wMaster = QWidget(self.splitter)
            self.wMaster.setObjectName(u'wMaster')
            self.verticalLayout_3 = QVBoxLayout(self.wMaster)
            self.verticalLayout_3.setMargin(0)
            self.verticalLayout_3.setObjectName(u'verticalLayout_3')
            self.lbMaster = QLabel(self.wMaster)
            self.lbMaster.setMaximumSize(QSize(16777215, self.SECTION_TITLE_HEIGHT))
            self.lbMaster.setObjectName(u'lbMaster')
            self.verticalLayout_3.addWidget(self.lbMaster)
            self.MasterLayout = QVBoxLayout()
            self.MasterLayout.setObjectName(u'MasterLayout')
            self.verticalLayout_3.addLayout(self.MasterLayout)
            self.wDetail = QWidget(self.splitter)
            self.wDetail.setObjectName(u'wDetail')
            self.verticalLayout_5 = QVBoxLayout(self.wDetail)
            self.verticalLayout_5.setMargin(0)
            self.verticalLayout_5.setObjectName(u'verticalLayout_5')
            self.lbDetail = QLabel(self.wDetail)
            self.lbDetail.setMaximumSize(QSize(16777215, self.SECTION_TITLE_HEIGHT))
            self.lbDetail.setObjectName(u'lbDetail')
            self.verticalLayout_5.addWidget(self.lbDetail)
            self.DetailLayout = QVBoxLayout()
            self.DetailLayout.setObjectName(u'DetailLayout')
            self.verticalLayout_5.addLayout(self.DetailLayout)
            self.verticalLayout.addWidget(self.splitter)

    # @takes('MasterDetailReference', QWidget,  env_type, optional(bool))
    def __init__(self, parent, name, env, selecting=False):
        u""""""
        super(MasterDetailReference, self).__init__(parent, name, env, selecting)
        self.ui = self.Ui(self)

        master = self.get_ref_class(self.params.master, env)(self, self.params.master, env, selecting)
        master.setObjectName(u'masterRef')
        #master.dlg_container = MasterDetailDlgContainer(self)
        detail = self.get_ref_class(self.params.detail, env)(self, self.params.detail, env)
        detail.setObjectName(u'detailRef')

        self.master = master
        self.detail = detail

        self.ui.lbMaster.setText(self.env.refs[self.params.master].display)
        self.ui.lbDetail.setText(self.env.refs[self.params.detail].display)
        
        self.ui.MasterLayout.addWidget(self.master)
        self.ui.DetailLayout.addWidget(self.detail)

        self.detail.ui.actionInsert.setShortcut(QKeySequence(Qt.ALT+Qt.Key_Insert))
        self.detail.ui.actionDelete.setShortcut(QKeySequence(Qt.ALT+Qt.Key_Delete))
        self.detail.ui.actionRefresh.setShortcut(QKeySequence(Qt.ALT+Qt.Key_F5))

        self.fk_detail = None
        self.pk_master = None
        for md_fk in self.detail.metadata.fkeys.itervalues():
            if md_fk.refTable == self.master.metadata.tableName:
                self.fk_detail = md_fk.fieldName
                self.pk_master = md_fk.refField
                break

        self.master.ui.tableView.selectionModel().currentRowChanged.connect(self.setFilter)
        self.setFilter(self.master.ui.tableView.currentIndex())

    # @takes('MasterDetailReference', QModelIndex, optional(QModelIndex))
    @returns(nothing)
    def setFilter(self, idx, prev=QModelIndex()):
        value = self.master.model.record(idx.row()).value(self.pk_master).toInt()[0]
        self.detail.model.set_filter(u'{0}_detail'.format(self.name), u"{0} = {1}".format(self.fk_detail, value))
        self.detail.model.select()
        self.detail.model.defaults[self.fk_detail] = value
        self.detail.ui.tableView.selectRow(0)


    @takes('MasterDetailReference')
    @returns(nothing)
    def saveSession(self):
        self.env.session.storage.splitter[self.name] = self.ui.splitter.sizes()

    @takes('MasterDetailReference', QShowEvent)
    @returns(nothing)
    def showEvent(self, event):
        try:
            sizes = self.env.session.storage.splitter[self.name]
        except KeyError:
            return
        except AttributeError:
            return

        self.ui.splitter.setSizes(sizes)

    @takes('MasterDetailReference', QCloseEvent)
    @returns(nothing)
    def closeEvent(self, event):
        self.saveSession()
        self.env.session.save()
        
class SelectingRefContainer(QDialog, UILoader):

    def __init__(self, parent, env, refname, fld_md, init_value):
        super(SelectingRefContainer, self).__init__(parent)
        self.setUI(env.config, u'SelectingRef.ui')
        self.fld_md = fld_md
        self.reference = BaseReference.get_ref_class(refname, env)(self, refname, env, True)
        if isinstance(self.reference, MasterDetailReference):
            self.overref = self.reference
            self.reference = self.overref.master
        self.reference.setObjectName(u'SelectingReference')
        self.ui.verticalLayout.addWidget(self.reference)
        self.setWindowTitle(self.reference.params.display)
        self.reference.selectRow({fld_md.cid: init_value})
        #TODO: Убрать хардкод pk после перехода на новые метаданные
        self.id = self.model.record(self.tableView.currentIndex().row()).value(u'id').toPyObject()
        self.tableView.doubleClicked.connect(self.accept)

    @property
    def model(self):
        return self.reference.model

    @property
    def tableView(self):
        return self.reference.ui.tableView

    def accept(self):
        self.ret = self.model.data(self.model.index(self.tableView.currentIndex().row(), self.fld_md.cid))
        super(SelectingRefContainer, self).accept()

    def reject(self):
        #TODO: Убрать хардкод pk после перехода на новые метаданные
        qstr = u'select {0}.{1} from {0} where id = :id'.format(self.reference.metadata.tableName, self.fld_md.fieldName)
        query = QSqlQuery(self.reference.env.db)
        query.prepare(qstr)
        query.bindValue(u':id', self.id)
        query.exec_()
        query.next()
        self.ret = query.record().value(0)
        super(SelectingRefContainer, self).reject()