#coding=utf-8

import io
import logging
import os
from PyQt4 import uic
from PyQt4.QtCore import QDir
from PyQt4.QtGui import QWizardPage, QWizard, QApplication, QFileDialog
from PyQt4.QtSql import QSqlQuery
from dpframe.data.upgrader.upgrader import Upgrader
from dpframe.data.metadata import Metadata

class BaseWizardPage(QWizardPage, object):

    def loadUI(self, ui_fpath):
        UIClass = uic.loadUiType(ui_fpath)[0]
        self.ui = UIClass()
        self.ui.setupUi(self)

class SelectMetadataPage(BaseWizardPage):

    def __init__(self):
        BaseWizardPage.__init__(self)
        self.setTitle(u'Выбор и проверка метаданных')
        self.setSubTitle(u'Выберите python-модуль, содержащий описание метаданных проекта. Проверьте метаданные на корректность.')
        self.loadUI(u'ui/SelectMetadataPage.ui')

        self.registerField(u'MDModule*', self.ui.leMDModule)
        self.verified = False

        self.ui.leMDModule.textChanged.connect(self.toggle_verify_btn)
        self.ui.leMDModule.textChanged.emit(self.ui.leMDModule.text())

        self.ui.btnBrowse.clicked.connect(self.browse)
        self.ui.btnVerify.clicked.connect(self.verify)

    def isComplete(self):
        return BaseWizardPage.isComplete(self) and self.verified

    def toggle_verify_btn(self, text):
        self.verified = False
        self.completeChanged.emit()
        self.ui.btnVerify.setEnabled(bool(unicode(text)))

    def browse(self):
        file = QFileDialog.getOpenFileName(self, u'Выбрать модуль', QDir.currentPath(), u'Модули python (*.py *.pyw)')

        if file:
            self.ui.leMDModule.setText(file)

    def verify(self):
        outlog = io.StringIO()
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(outlog))

        self.ui.ptVerboseResult.clear()

        p = unicode(unicode(self.field(u'MDModule').toString()))
        sys.path.insert(0, os.path.split(p)[0])
        try:
            self.module = __import__(os.path.splitext(os.path.split(p)[1])[0])
            self.metadata = Metadata(self.module)
            self.metadata.validate(logger)
        except Exception as exc:
            self.ui.lblVerifyResult.setText(unicode(exc))
            strlog = outlog.getvalue()
            if strlog:
                self.ui.ptVerboseResult.setPlainText(strlog)
            self.verified = False
            self.completeChanged.emit()
            return

        self.ui.lblVerifyResult.setText(u'Метаданные проверены.')
        self.verified = True
        self.completeChanged.emit()

    def validatePage(self):
        self.wizard().metadata = self.metadata
        return QWizardPage.validatePage(self)

class SQLConnectPage(BaseWizardPage):

    def __init__(self):
        BaseWizardPage.__init__(self)
        self.setTitle(u'Параметры соединения с сервером баз данных')
        self.setSubTitle(u'Задайте параметры соединения с SQL-сервером. Протестируйте соединение')
        self.loadUI(u'ui/SQLConnectPage.ui')

        self.ui.leServer.textChanged.connect(self.toggle_check_btn)
        self.ui.leUser.textChanged.connect(self.toggle_check_btn)
        self.ui.lePassword.textChanged.connect(self.toggle_check_btn)

        self.ui.leServer.textChanged.emit(self.ui.leServer.text())

        self.ui.btnCheck.clicked.connect(self.check_connect)

        self.registerField(u'Server*', self.ui.leServer)
        self.registerField(u'User*', self.ui.leUser)
        self.registerField(u'Password*', self.ui.lePassword)

        self.checked = False
        self.db = None

    def isComplete(self):
        return BaseWizardPage.isComplete(self) and self.checked

    def toggle_check_btn(self):
        self.checked = False
        self.completeChanged.emit()
        self.ui.btnCheck.setEnabled(bool(unicode(self.field(u'Server').toString()) and
                                          unicode(self.field(u'User').toString()) and
                                          unicode(self.field(u'Password').toString())))

    def check_connect(self):
        server = unicode(self.field(u'Server').toString())
        user = unicode(self.field(u'User').toString())
        password = unicode(self.field(u'Password').toString())
        database = u'postgres'

        self.ui.ptVerboseResult.clear()

        del self.db
        self.db = Upgrader.getdb()
        self.db.setHostName(server)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        self.db.setPassword(password)
        if self.db.open():
            self.checked = True
            self.ui.lblCheckResult.setText(u'Соединение установлено.')
        else:
            self.checked = False
            err = self.db.lastError()
            self.ui.lblCheckResult.setText(u'Ошибка соединения.')
            self.ui.ptVerboseResult.setPlainText(u'Ошибка драйвера:{0}\nОшибка сервера:{1}'.format(unicode(err.driverText()),
                                                                                                   unicode(err.databaseText())))
        self.completeChanged.emit()

    def __del__(self):
        del self.db

    def validatePage(self):
        self.wizard().db = self.db
        return QWizardPage.validatePage(self)

class SelectDatabasePage(BaseWizardPage):

    def __init__(self):
        BaseWizardPage.__init__(self)
        self.setTitle(u'Выбор базы данных для обновления')
        self.setSubTitle(u'Выберите существующую базу данных для обновления или создайте новую на основе выбранных ранее метаданных.')
        self.loadUI(u'ui/SelectDatabasePage.ui')

        self.registerField(u'Database*', self.ui.cbDatabase)
        self.ui.cbDatabase.editTextChanged.connect(self.completeChanged)
        self.ui.cbDatabase.editTextChanged.connect(self.storeParams)
        self.ui.cbDatabase.currentIndexChanged.connect(self.storeParams)

    def initializePage(self):
        BaseWizardPage.initializePage(self)
        self.db = self.wizard().db

        qstatement = u"select datname from pg_database where not datistemplate and datname <> 'postgres'"
        query = QSqlQuery(self.db)
        query.exec_(qstatement)
        while query.next():
            self.ui.cbDatabase.addItem(query.value(0).toString())
        self.ui.cbDatabase.setCurrentIndex(0)

    def isComplete(self):
        return BaseWizardPage.isComplete(self) and not self.ui.cbDatabase.currentText().isEmpty()

    def storeParams(self):
        db_name = unicode(self.ui.cbDatabase.currentText())
        self.wizard().db_name = db_name
        self.wizard().is_new = self.ui.cbDatabase.findText(db_name) == -1



class UpgraderWizard(QWizard, object):

    def __init__(self):
        QWizard.__init__(self)

        self.setWindowTitle(u'Обновление базы данных')

        self.addPage(SelectMetadataPage())
        self.addPage(SQLConnectPage())
        self.addPage(SelectDatabasePage())

        self.metadata = None
        self.db = None
        self.db_name = None
        self.is_new = None


    def accept(self):
        upgrader = Upgrader(self.metadata, self.db, self.db_name)
        if self.is_new:
            upgrader.create()
        else:
            upgrader.update()
        QWizard.accept(self)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    wizard = UpgraderWizard()
    wizard.show()
    sys.exit(app.exec_())
