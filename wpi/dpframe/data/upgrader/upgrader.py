#coding=utf-8
from os import linesep
import uuid
from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from dpframe.data.mddecorators import DB_DEFAULTS
from dpframe.data.metadata import Metadata, DBMetadata
from dpframe.tech.typecheck import *

class Upgrader(object):

    create_connect = u'create'
    update_connect = u'update'

    @staticmethod
    @takes(optional(unicode), optional(unicode))
    @returns(QSqlDatabase)
    def getdb(type=u'QPSQL', name=None):
        if name is None:
            name = unicode(QSqlDatabase.database().connectionName())
        if QSqlDatabase.contains(name):
            return QSqlDatabase.database(name, False)
        else:
            return QSqlDatabase.addDatabase(type, name)

    @staticmethod
    @takes(QSqlDatabase)
    def raiseSqlError(db):
        err = db.lastError()
        if err.isValid():
            db.rollback()
            raise RuntimeError(unicode(err.text()))

    @staticmethod
    @takes(QSqlDatabase)
    def opendb(db):
        if not db.isOpen():
            db.open()
            Upgrader.raiseSqlError(db)


    @takes('Upgrader', Metadata, QSqlDatabase, unicode)
    def __init__(self, metadata, db, db_name):
        self.metadata = metadata
        self.metadata.validate()
        self.db = db
        self.db_name = db_name

    def update(self, drop_old_tables=True):
        #TODO: Использовать логгер вместо print
        print u'Создание эталонной базы'
        gauge_db_name = unicode(uuid.uuid4().hex)
        gauge_db = self.create(gauge_db_name)
        self.opendb(gauge_db)

        print u'Чтение новых метаданных'
        new_md = DBMetadata(gauge_db)

        print u'Удаление эталонной базы'
        gauge_db.close()
        del gauge_db
        QSqlDatabase.removeDatabase(self.create_connect)
        self.opendb(self.db)
        if not QSqlQuery(self.db).exec_(u'drop database "{0}";'.format(gauge_db_name)):
            self.raiseSqlError(self.db)

        print u'Соединение с обновляемой базой'
        db = self.getdb(name=self.update_connect)
        db.setDatabaseName(self.db_name)
        db.setHostName(self.db.hostName())
        db.setUserName(self.db.userName())
        db.setPassword(self.db.password())
        self.opendb(db)

        print u'Чтение метаданных обновляемой базы'
        old_md = DBMetadata(db)

        if not drop_old_tables:
            for tname in old_md.tables.keys():
                if tname not in new_md.tables:
                    del old_md.tables[tname]

        #TODO: Выкинуть после перехода на новые метаданные
        for tname in [u'db_property', u'meta_field', u'meta_table']:
            tbl_md = old_md.tables.get(tname)
            if tbl_md:
                del old_md.tables[tname]
        #END TODO

        if new_md == old_md:
            print u'Обновление не требуется, метаданные идентичны'
            return

        print u'Формирование SQL-скрипта'
        statements = []
        #Дополнение структуры новыми таблицами и полями
        added = []
        for tname, tbl_md in new_md.tables.iteritems():
            if tname not in old_md.tables:
                added.append(tname)
                statements.append(tbl_md._create_statement())
                statements.append(tbl_md._comment_on_statement())
            else:
                adding_flds = [fname for fname, fld_name in tbl_md.fields.iteritems() if not old_md.tables[tname].fields.get(fname)]
                if adding_flds:
                    statements.append(tbl_md._pure_add_column_statement(adding_flds))

        #TODO: Здесь добавить в statements скрипт обновления

        #Переименование таблиц на удаление
        removed = []
        for tname, tbl_md in old_md.tables.iteritems():
            if tbl_md != new_md.tables.get(tname):
                statements.append(u'alter table "{0}" rename to "removed_{0}";'.format(tname))
                removed.append(tname)

        for tname in removed:
            if tname in new_md.tables:
                #Создать новые таблицы
                statements += new_md.tables[tname]._create_statement()
                statements += new_md.tables[tname]._comment_on_statement()
                #DONE: Копирование данных из removed_table в table
                #DONE: Добавить coalesce для обязательных колонок
                fld_list = []
                fld_coalesce = []
                for fname, fld_md in new_md.tables[tname].fields.iteritems():
                    fld_list.append(u'"{0}"'.format(fname))
                    if fld_md.required and not fld_md.autoincrement:
                        fld_coalesce.append(u'coalesce("{0}", {1})'.format(fname, fld_md.default if fld_md.default else DB_DEFAULTS[fld_md.type]))
                    else:
                        fld_coalesce.append(u'"{0}"'.format(fname))
                statements.append(u'insert into "{0}" ({1}) (select {2} from "removed_{0}");'.format(tname,
                    u', '.join(fld_list), u', '.join(fld_coalesce)))

        #Удалить старые таблицы
        for tname in removed:
            statements.append(u'drop table "removed_{0}" cascade;'.format(tname))

        #DONE: Создать внешние ключи
        for tname in added + removed:
            if tname in new_md.tables:
                statements += new_md.tables[tname]._add_fk_statement()

        print u'Выполнение SQL-скрипта' + linesep
        self.opendb(db)
        for query in statements:
            print query
            if query.strip() and not QSqlQuery(db).exec_(query):
                self.raiseSqlError(db)
        db.close()
        print u'Готово!'


    @takes('Upgrader', optional(unicode))
    @returns(QSqlDatabase)
    def create(self, dbname=None):
        self.opendb(self.db)
        if not QSqlQuery(self.db).exec_(u'create database "{0}";'.format(dbname or self.db_name)):
            self.raiseSqlError(self.db)
        self.db.close()

        db = self.getdb(name=self.create_connect)
        db.setDatabaseName(dbname or self.db_name)
        db.setHostName(self.db.hostName())
        db.setUserName(self.db.userName())
        db.setPassword(self.db.password())

        self.opendb(db)
        db.transaction()
        for query in self.metadata.sql():
            if query.strip() and not QSqlQuery(db).exec_(query):
                self.raiseSqlError(db)
        db.commit()
        self.raiseSqlError(db)
        return db


