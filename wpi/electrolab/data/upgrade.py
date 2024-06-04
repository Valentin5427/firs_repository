#coding=utf-8
from PyQt4.QtCore import QCoreApplication
import sys
from PyQt4.QtSql import QSqlDatabase
from dpframe.data.metadata import Metadata
from dpframe.data.upgrader.upgrader import Upgrader
from electrolab.data import metadata

app = QCoreApplication(sys.argv)

db = QSqlDatabase.addDatabase(u'QPSQL', u'main')
db.setDatabaseName(u'postgres')
db.setHostName(u'localhost')
db.setUserName(u'postgres')
db.setPassword(u'postgres')
Upgrader.opendb(db)

db_name = u'electrolab'

upg = Upgrader(Metadata(metadata), db, db_name)
upg.update()
