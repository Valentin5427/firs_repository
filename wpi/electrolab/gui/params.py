#coding=utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QCheckBox, QDialogButtonBox, QVBoxLayout
from dpframe.tech.typecheck import takes, dict_of, anything, returns, nothing, env_type
from electrolab.gui.common import UILoader

class ParamDlg(QDialog, UILoader):

    _filterChanged = pyqtSignal()

    @classmethod
    @takes(type,  env_type)
    @returns(type)
    def get_dlg_class(cls, name, env):
        try:
            return env.filters[name].dialog
        except KeyError:
            return cls

    @takes('ParamDlg',  env_type)
    def __init__(self, name, env):
        QDialog.__init__(self)
        self.props = env.filters[name]
        self.setUI(env.config, self.props.dialog_ui)
        self.config = env.config

        self._set_labels()

    @takes('ParamDlg')
    def _set_labels(self):
        #устанавливаеm связанным меткам текст из метаданных
        for widget in self.ui.__dict__.itervalues():
            if isinstance(widget, QLabel) and widget.buddy() is not None:
                pname = widget.buddy().property(u'param').toString()
            elif isinstance(widget, QCheckBox):
                pname = widget.property(u'param').toString()
            else:
                continue
            try:
                widget.setText(self.props.params[pname].display)
            except KeyError:
                pass

    @takes('ParamDlg')
    # @returns(dict_of( anything))
    def _collect_params(self):
        return {}

    @takes('ParamDlg')
    @returns(str)
    def where_clause(self):
        # Вернуть правильный where clause
        return u'1=1'

    @property
    def params(self):
        return self._collect_params()

class OkCancelDlgContainer(QDialog):

    class Ui(object):

        @takes('Ui', 'OkCancelDlgContainer')
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
            self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
            self.buttonBox.setObjectName(u'buttonBox')
            self.verticalLayout.addWidget(self.buttonBox)
            self.buttonBox.accepted.connect(Dialog.accept)
            self.buttonBox.rejected.connect(Dialog.reject)

    @takes('OkCancelDlgContainer', ParamDlg)
    def __init__(self, dlg):
        super(OkCancelDlgContainer, self).__init__()
        self.ui = self.Ui(self)
        self.dlg = dlg
        self.dlg.setObjectName(u'widget')
        self.ui.widgetLayout.addWidget(self.dlg)
        self.setWindowTitle(self.dlg.props.display)

    @property
    def params(self):
        return self.dlg.params


class FilterContainer(QDialog, UILoader):

    filterChanged = pyqtSignal(str)

    @takes('FilterContainer', ParamDlg)
    def __init__(self, fdlg):
        QDialog.__init__(self)
        self.filter_dlg = fdlg
        # TODO: хардкодить ui
        self.setUI(self.filter_dlg.config, u'FilterContainer.ui')
        self.ui.widgetLayout.addWidget(self.filter_dlg)
        self.filter_dlg._filterChanged.connect(self.notify_reference)
        self.ui.btnApplyFilter.toggled.connect(self.apply_filter)

    @takes('FilterContainer')
    @returns(nothing)
    def notify_reference(self):
        self.apply_filter(self.ui.btnApplyFilter.isChecked())

    @takes('FilterContainer', bool)
    @returns(nothing)
    def apply_filter(self, checked):
        self.filterChanged.emit(self.filter_dlg.where_clause() if checked else u'1=1')
