#-*- coding: UTF-8 -*-
u"""
Created on 14.08.2011
#10 #10
@author: knur
Доступ к метаданным. Работает через Qt драйвер БД
"""
import inspect
import logging
import os
from PyQt5.QtSql import QSqlQuery, QSqlRecord, QSqlDatabase
from PyQt5 import QtCore
from dpframe.data.mddecorators import DBTable, DBType, FKAction, MetaDBField, MetaDBTable, DB_DEFAULTS
from dpframe.tech.AttrDict import AttrDict
from dpframe.tech.typecheck import *

SCHEMA = u'public'

class DBMetadata(object):

    class _Field(object):

        @takes('_Field', QSqlRecord, int)
        def __init__(self, rec, ordinal):
            self.fieldName = rec.value(u'column_name').toString().lower()
            self.cid = ordinal
            self.description = rec.value(u'description').toString()

            self.required = rec.value(u'is_nullable').toString() == u'NO'
            self.autoincrement = rec.value(u'is_autoinc').toPyObject()

            self.type = rec.value(u'data_type').toString().lower()
            if u' ' in self.type:
                self.type = rec.value(u'udt_name').toString().lower()

            self.default = None
            self.length = None
            self.precision = None
            if not self.autoincrement:
                self.default = rec.value(u'column_default').toString()
            if self.type == DBType.numeric:
                self.length = rec.value(u'numeric_precision').toInt()[0]
                self.precision = rec.value(u'numeric_scale').toInt()[0]
            if self.type in [DBType.varchar, DBType.char]:
                self.length = rec.value(u'character_maximum_length').toInt()[0]
            self.isPrimaryKey = rec.value(u'is_primary_key').toPyObject()

        def __eq__(self, other):
            return (self.fieldName == other.fieldName
                    and self.cid == other.cid
                    and self.description == other.description
                    and self.required == other.required
                    and self.autoincrement == other.autoincrement
                    and self.type == other.type
                    and self.default == other.default
                    and self.length == other.length
                    and self.precision == other.precision
                    and self.isPrimaryKey == other.isPrimaryKey
            )

        @returns(str)
        def _pure_sql(self):
            res = [u'"{0}"'.format(self.fieldName)]
            type = u'serial' if self.autoincrement else self.type
            if self.type == DBType.numeric:
                type += u'({0}, {1})'.format(self.length, self.precision)
            elif self.type in [DBType.char, DBType.varchar]:
                type += u'({0})'.format(self.length)
            res.append(type)
            if (self.default or self.required) and not self.autoincrement:
                res.append(u'default {0}'.format(self.default or DB_DEFAULTS[self.type]))
            return u' '.join(res)

        @returns(str)
        def _sql(self):
            res = [u'"{0}"'.format(self.fieldName)]
            type = u'serial' if self.autoincrement else self.type
            if self.type == DBType.numeric:
                type += u'({0}, {1})'.format(self.length, self.precision)
            elif self.type in [DBType.char, DBType.varchar]:
                type += u'({0})'.format(self.length)
            res.append(type)
            res.append(u'not null' if self.required else u'null')
            if self.default:
                res.append(u'default {0}'.format(self.default))
            return u' '.join(res)

    class _FKey(object):

        @takes('_FKey', QSqlRecord)
        def __init__(self, rec):
            self.fieldName = rec.value(u'field').toString().lower()
            self.refTable = rec.value(u'ref_name').toString().lower()
            self.refField = rec.value(u'ref_field').toString().lower()
            self.onUpdate = rec.value(u'update_rule').toString()
            self.onDelete = rec.value(u'delete_rule').toString()

        def __eq__(self, other):
            return (self.fieldName == other.fieldName
                    and self.refTable == other.refTable
                    and self.refField == other.refField
                    and self.onUpdate == other.onUpdate
                    and self.onDelete == other.onDelete
                )

    class _Table(object):
        @takes('_Table', str, str, QSqlDatabase)
        def __init__(self, tableName, desc, db):
            self.tableName = tableName
            self.description = desc
            self.fields = AttrDict()
            sQuery = u"""
                    SELECT col.column_name,
                       col.column_default,
                       col.is_nullable,
                       col.data_type,
                       col.udt_name,
                       col.character_maximum_length,
                       col.numeric_precision,
                       col.numeric_scale,
                       pcol.constraint_type IS NOT NULL AS is_primary_key,
                       pg_get_serial_sequence(col.table_name,  col.column_name) IS NOT NULL as is_autoinc,
                       col_description((SELECT oid FROM pg_class WHERE relname = col.table_name), col.ordinal_position) as description
                    FROM   information_schema.columns col
                       LEFT JOIN (SELECT kcol.table_name        AS table_name,
                                 kcol.column_name       AS column_name,
                                 constr.constraint_type AS constraint_type
                              FROM   information_schema.key_column_usage kcol
                                 LEFT JOIN information_schema.table_constraints constr
                                   ON constr.table_name = kcol.table_name
                                  AND constr.constraint_name = kcol.constraint_name
                              WHERE  constr.constraint_type = 'PRIMARY KEY') pcol
                         ON pcol.table_name = col.table_name
                        AND pcol.column_name = col.column_name
                    WHERE  col.table_name = :table
                    """
            oQuery = QSqlQuery(db)
            oQuery.prepare(sQuery)
            oQuery.bindValue(u':table', self.tableName)
            oQuery.exec_()
            ordinal = 0
            while oQuery.next():
                fieldName = oQuery.value(0).toString().lower()
                self.fields[fieldName] = DBMetadata._Field(oQuery.record(), ordinal)
                ordinal += 1

            self.primaryKey = {fld_md.fieldName for fld_md in self.fields.itervalues() if fld_md.isPrimaryKey}

            self.fkeys = AttrDict()
            sQuery = u"""
                    SELECT kcol.column_name AS field,
                           rcol.table_name  AS ref_name,
                           rcol.column_name AS ref_field,
                           ref.update_rule,
                           ref.delete_rule
                    FROM   information_schema.key_column_usage kcol
                           LEFT JOIN information_schema.referential_constraints ref
                             ON kcol.constraint_name = ref.constraint_name
                           LEFT JOIN information_schema.key_column_usage rcol
                             ON rcol.constraint_name = ref.unique_constraint_name
                    WHERE  kcol.position_in_unique_constraint IS NOT NULL
                           AND kcol.table_name = :table
                    """
            oQuery = QSqlQuery(db)
            oQuery.prepare(sQuery)
            oQuery.bindValue(u':table', self.tableName)
            oQuery.exec_()
            while oQuery.next():
                fieldName = oQuery.value(0).toString().lower()
                self.fkeys[fieldName] = DBMetadata._FKey(oQuery.record())

            self.uniques = []
            sQuery = u'''
                    SELECT constraint_name
                    FROM   information_schema.table_constraints
                    WHERE  constraint_type = 'UNIQUE'
                           AND table_name = :table;
                    '''
            oQuery = QSqlQuery(db)
            oQuery.prepare(sQuery)
            oQuery.bindValue(u':table', self.tableName)
            oQuery.exec_()
            unique_names = []
            while oQuery.next():
                unique_names.append(oQuery.value(0).toString().lower())

            for name in unique_names:
                sQuery = u'''
                        SELECT column_name
                        FROM   information_schema.key_column_usage
                        WHERE  constraint_name = :unique
                               AND table_name = :table;
                        '''
                oQuery = QSqlQuery(db)
                oQuery.prepare(sQuery)
                oQuery.bindValue(u':unique', name)
                oQuery.bindValue(u':table', self.tableName)
                oQuery.exec_()
                uniq_fields = set()
                while oQuery.next():
                    uniq_fields.add(oQuery.value(0).toString().lower())
                self.uniques.append(uniq_fields)

            self.checks = set()
            sQuery = u'''
                    select cc.check_clause
                    from   information_schema.table_constraints tc
                           left join information_schema.check_constraints cc
                             on tc.constraint_name = cc.constraint_name
                    where  tc.constraint_type = 'CHECK'
                           and cc.check_clause not like '%IS NOT NULL'
                           and tc.table_name = :table;
                    '''
            oQuery = QSqlQuery(db)
            oQuery.prepare(sQuery)
            oQuery.bindValue(u':table', self.tableName)
            oQuery.exec_()
            while oQuery.next():
                self.checks.add(oQuery.value(0).toString())

        def __eq__(self, other):
            return (self.tableName == other.tableName
                and self.description == other.description
                and self.fields == other.fields
                and self.primaryKey == other.primaryKey
                and self.fkeys == other.fkeys
                and sorted(self.uniques) == sorted(other.uniques)
                and self.checks == other.checks
            )

        @takes('_Table', list_of(str))
        @returns(str)
        def _pure_add_column_statement(self, adding_fields):
            u"""Генерировать скрипт добавления отсутствующих полей. Создаются только поля c дефаултами, без констрейнтов"""

            return u'alter table "{0}" {1};'.format(self.tableName,
                u', '.join(u'add column {0}'.format(self.fields[fld_name]._pure_sql()) for fld_name in adding_fields)
            )

        @returns(list_of(str))
        def _create_statement(self):

            def key_cid(fld_md):
                return fld_md.cid

            res = [u'create table "{0}"({1});'.format(self.tableName,
                                                   u', '.join(fld_md._sql() for fld_md in sorted(self.fields.itervalues(), key=key_cid))),
                   u'alter table "{0}" add primary key({1});'.format(self.tableName,
                                                                  u', '.join([u'"{0}"'.format(fld_name) for fld_name in self.primaryKey]))]
            for uniq in self.uniques:
                res.append(u'alter table "{0}" add unique({1});'.format(self.tableName, u', '.join([u'"{0}"'.format(fld_name) for fld_name in uniq])))
            for check in self.checks:
                res.append(u'alter table "{0}" add check({1});'.format(self.tableName, check))
            return res

        @returns(list_of(str))
        def _add_fk_statement(self):
            res = []
            for fk_md in self.fkeys.itervalues():
                res.append(u'alter table "{0}" add foreign key ("{1}") references "{2}"("{3}") on delete {4} on update {5};'.format(
                    self.tableName, fk_md.fieldName, fk_md.refTable, fk_md.refField, fk_md.onDelete, fk_md.onUpdate))
            return res

        @returns(list_of(str))
        def _comment_on_statement(self):
            res = [u"comment on table \"{0}\" is '{1}';".format(self.tableName, self.description)]
            for fld_md in self.fields.itervalues():
                if fld_md.description:
                    res.append(u"comment on column \"{0}\".\"{1}\" is '{2}';".format(self.tableName, fld_md.fieldName, fld_md.description))
            return res


    @takes('DBMetadata', QSqlDatabase)
    def __init__(self, db):
        self.tables = AttrDict()
        sQuery = u"""
                SELECT tab.table_name,
                       obj_description((SELECT oid FROM pg_class WHERE relname = tab.table_name)) as description
                FROM   information_schema.tables tab
                WHERE  tab.table_schema = :schema
                """
        oQuery = QSqlQuery(db)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':schema', SCHEMA)
        oQuery.exec_()
        while oQuery.next():
            tableName = oQuery.value(0).toString().lower()
            desc = oQuery.value(1).toString()
            self.tables[tableName] = DBMetadata._Table(tableName, desc, db)

    def __eq__(self, other):
        return self.tables == other.tables


class Metadata(object):

    class _Field(object):

        @takes('_Field', MetaDBField)
        def __init__(self, fld_cls, tableName):
            self.tableName = tableName
            self.fieldName = fld_cls.__name__.lower()
            self.isPrimaryKey = fld_cls.primary_key

            self.cid = fld_cls.cid

            self.required = fld_cls.required
            self.autoincrement = fld_cls.autoinc

            self.type = fld_cls.type
            self.default = fld_cls.default
            self.length = fld_cls.length
            self.precision = fld_cls.prec
            self.max = fld_cls.max
            self.min = fld_cls.min
            self.alias = fld_cls.display or self.fieldName
            self.description = fld_cls.__doc__
            self.visible = fld_cls.visible
            self.readonly = fld_cls.readonly
            self.fkDescription = fld_cls.fkdescription
            self.visiblePosition = None
        print(536536, optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        # @takes('_Field', optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def validate(self, log=logging):
            valid = True

            if self.autoincrement and self.type != DBType.integer:
                log.error(u'Поле {0}.{1}: автоинкрементное поле не целочисленное'.format(self.tableName, self.fieldName))
                valid = False

            if self.autoincrement and self.default:
                log.error(u'Поле {0}.{1}: автоинкрементное поле имеет значение по умолчанию {2}'.format(self.tableName, self.fieldName, self.default))
                valid = False

            if self.type not in [DBType.integer, DBType.numeric, DBType.timestamp] and (self.max or self.min):
                log.error(u'Поле {0}.{1}: поле типа {2} имеет ограничения: max={3}, min={4}'.format(self.tableName, self.fieldName, self.type, self.max, self.min))
                valid = False

            if self.autoincrement and (self.max or self.min):
                log.error(u'Поле {0}.{1}: автоинкрементное поле имеет ограничения: max={3}, min={4}'.format(self.tableName, self.fieldName, self.max, self.min))
                valid = False

            return valid

        # @takes('_Field', DBMetadata._Field, optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def check_db(self, fld_db_md, log=logging):
            equal = True
            #DONE: имплементировать проверку
            if self.cid != fld_db_md.cid:
                equal = False
                log.error(u'Поле {0}.{1}: порядковый номер {2} не соответствует номеру в базе: {3}'.format(self.tableName, self.fieldName, self.cid, fld_db_md.cid))

            if self.type != fld_db_md.type:
                equal = False
                log.error(u'Поле {0}.{1}: тип {2} не соответствует типу в базе: {3}'.format(self.tableName, self.fieldName, self.type, fld_db_md.type))

            if self.required != fld_db_md.required:
                equal = False
                log.error(u'Поле {0}.{1}: обязательность {2} не соответствует базе: {3}'.format(self.tableName, self.fieldName, self.required, fld_db_md.required))
            if self.type in [DBType.numeric, DBType.varchar, DBType.char] and self.length != fld_db_md.length:
                equal = False
                log.error(u'Поле {0}.{1}: длина {2} не соответствует длине в базе: {3}'.format(self.tableName, self.fieldName, self.length, fld_db_md.length))

            if self.type == DBType.numeric and self.precision != fld_db_md.precision:
                equal = False
                log.error(u'Поле {0}.{1}: точность {2} не соответствует точности в базе: {3}'.format(self.tableName, self.fieldName, self.precision, fld_db_md.precision))

            if self.description != fld_db_md.description:
                log.warning(u"Поле {0}.{1}: описание '{2}' не совпадает с описанием поля в базе '{3}'".format(self.tableName, self.fieldName, self.description, fld_db_md.description))

            return equal

        @returns(str)
        def _sql(self):
            res = [self.fieldName]
            type = u'serial' if self.autoincrement else self.type
            if self.type == DBType.numeric:
                type += u'({0}, {1})'.format(self.length, self.precision)
            elif self.type in [DBType.char, DBType.varchar]:
                type += u'({0})'.format(self.length)
            res.append(type)
            res.append(u'not null' if self.required else u'null')
            if self.default:
                res.append(u'default {0}'.format(self.default))
            # DONE: генерировать выражение на минимум/максимум
            if self.max or self.min:
                checks = []
                if self.max:
                    checks.append(u'{0} <= {1}'.format(self.fieldName, self.max))
                if self.min:
                    checks.append(u'{0} >= {1}'.format(self.fieldName, self.min))
                res.append(u'check({0})'.format(u' and '.join(checks)))
            return u' '.join(res)

    class _FKey(object):

        @takes('_FKey', MetaDBField, '_Field')
        def __init__(self, fld_cls, fld_md):
            self.fldMD = fld_md
            self.fieldName = fld_cls.__name__.lower()
            self.refTable = fld_cls.parent or fld_cls.reference
            self.refField = None
            self.refTableMD = None
            self.onUpdate = FKAction.cascade
            self.onDelete = FKAction.cascade if fld_cls.parent else FKAction.restrict

        # @takes('_FKey', optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def validate(self, log=logging):
            valid = True

            if self.fldMD.type != self.refTableMD.fields[self.refField].type:
                log.error(u'Внешний ключ {0}.{1}: тип поля {2} не совпадает с типом ({3}) первичного ключа реляции {4}.{5} '.format(self.fldMD.tableName,
                                                                                                                                    self.fieldName,
                                                                                                                                    self.fldMD.type,
                                                                                                                                    self.refTableMD.fields[self.refTableMD.primaryKey[0]].type,
                                                                                                                                    self.refTableMD.tableName,
                                                                                                                                    self.refTableMD.fields[self.refTableMD.primaryKey[0]].fieldName))
                valid = False

            return valid
        #
        # @takes('_FKey', DBMetadata._FKey, optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def check_db(self, fkey_db_md, log=logging):
            equal = True
            #DONE: имплементировать проверку
            if self.refTable != fkey_db_md.refTable:
                equal = False
                log.error(u'Внешний ключ {0}.{1}: реляция {2} не соответствует базе {3}'.format(self.fldMD.tableName, self.fieldName, self.refTable, fkey_db_md.refTable))
            if self.refField != fkey_db_md.refField:
                equal = False
                log.error(u'Внешний ключ {0}.{1}: Связанное поле в реляции {2}.{3} не соответствует базе {4}.{5}'.format(self.fldMD.tableName, self.fieldName, self.refTable, self.refField, fkey_db_md.refTable, fkey_db_md.refField))
            #DONE: до появления апгрейдера
            if self.onUpdate != fkey_db_md.onUpdate:
                equal = False
                log.error(u'Внешний ключ {0}.{1}: Действие на обновление {2} не соответствует базе {3}.'.format(self.fldMD.tableName, self.fieldName, self.onUpdate, fkey_db_md.onUpdate))
            if self.onDelete != fkey_db_md.onDelete:
                equal = False
                log.error(u'Внешний ключ {0}.{1}: Действие на удаление {2} не соответствует базе {3}.'.format(self.fldMD.tableName, self.fieldName, self.onDelete, fkey_db_md.onDelete))

            return equal


    class _Table(object):

        @takes('_Table', MetaDBTable)
        def __init__(self, table_cls):
            self.tableName = table_cls.__name__.lower()
            self.alias = table_cls.display or self.tableName
            self.description = table_cls.__doc__
            self.createModel = table_cls.createmodel
            self.fields = AttrDict()
            self.fkeys = AttrDict()
            for fld_cls in table_cls.fld_classes:
                self.fields[fld_cls.__name__.lower()] = Metadata._Field(fld_cls, self.tableName)
            for fld_cls in table_cls.fld_classes:
                if fld_cls.reference or fld_cls.parent:
                    field_name = fld_cls.__name__.lower()
                    self.fkeys[field_name] = Metadata._FKey(fld_cls, self.fields[field_name])

            self.primaryKey = [name for name, md_fld in self.fields.iteritems() if md_fld.isPrimaryKey]
            self.uniques = []
            for fld_cls in table_cls.fld_classes:
                if fld_cls.unique:
                    self.uniques.append({fld_cls.__name__.lower()})
            # DONE: собрать объекты типа Unique
            for uniq in table_cls.uniques:
                self.uniques.append(set([fld_cls.__name__.lower() for fld_cls in uniq]))
            # DONE: проанализировать объект типа DisplayOrder, заполнить у полей атрибут visiblePosition
            for pos, fld_name in enumerate(table_cls.displayOrder):
                self.fields[fld_name].visiblePosition = pos
            self.isRelational = bool(self.fkeys)
            self.isRelation = False

        # @takes('_Table', optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def validate(self, log=logging):
            valid = True
            for fld_md in self.fields.itervalues():
                valid = fld_md.validate(log) and valid
            for fkey_md in self.fkeys.itervalues():
                valid = fkey_md.validate(log) and valid

            if not self.primaryKey:
                log.error(u'Таблица {0}: отсутствует первичный ключ'.format(self.tableName))
                valid = False

            if len(self.primaryKey) > 1:
                log.error(u'Таблица {0}: составной первичный ключ {1}'.format(self.tableName, list(self.primaryKey)))
                valid = False

            for pos, unique in enumerate(self.uniques):
                for tst_uniq in self.uniques[pos+1:]:
                    if unique == tst_uniq:
                        log.error(u'Таблица {0}: дублируется альтернативный ключ {1}.'.format(self.tableName, list(unique)))
                        valid = False

            #DONE: только одно поле с fk_description
            fk_descs = [fld_md.fieldName for fld_md in self.fields.itervalues() if fld_md.fkDescription]
            if len(fk_descs) > 1:
                log.error(u'Таблица {0}: Несколько полей-описаний внешнего ключа - {1}.'.format(self.tableName, fk_descs))
                valid = False
            #DONE: проверить налчие fkDescription у всех таблиц-реляций
            if self.isRelation and not fk_descs:
                log.error(u'Таблица {0}: У реляции отсутствует поле-описание внешнего ключа.'.format(self.tableName))
                valid = False

            #DONE: только одно автоинкрементное поле
            fk_autoinc = [fld_md.fieldName for fld_md in self.fields.itervalues() if fld_md.autoincrement]
            if len(fk_autoinc) > 1:
                log.error(u'Таблица {0}: Несколько автоинкрементных полей - {1}.'.format(self.tableName, fk_autoinc))
                valid = False

            return valid

        # @takes('_Table', DBMetadata._Table, optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
        @returns(bool)
        def check_db(self, tbl_db_md, log=logging):
            equal = True
            for fld_name, fld_md in self.fields.iteritems():
                if fld_name not in tbl_db_md.fields:
                    equal = False
                    log.error(u'Поле {0}.{1}: отсутствует в базе.'.format(fld_md.tableName, fld_name))
                    continue
                equal = fld_md.check_db(tbl_db_md.fields[fld_name], log) and equal
            if set(self.primaryKey) != set(tbl_db_md.primaryKey):
                equal = False
                log.error(u'Таблица {0}: первичный ключ {1} не соответствует ключу в базе ({2}).'.format(self.tableName, self.primaryKey, tbl_db_md.primaryKey))
            for fld_name, fkey_md in self.fkeys.iteritems():
                if fld_name not in tbl_db_md.fkeys:
                    equal = False
                    log.error(u'Поле {0}.{1}: внешний ключ отсутствует в базе.'.format(self.tableName, fld_name))
                    continue
                equal = fkey_md.check_db(tbl_db_md.fkeys[fld_name], log) and equal
            for unique in self.uniques:
                if unique not in tbl_db_md.uniques:
                    equal = False
                    log.error(u'Таблица {0}: альтернативный ключ {1} отсутствует в базе.'.format(self.tableName, list(unique)))
            if self.description != tbl_db_md.description:
                log.warning(u"Таблица {0}: описание '{1}' не совпадает с описанием поля в базе '{2}'".format(self.tableName, self.description, tbl_db_md.description))

            return equal

        @returns(list_of(str))
        def _create_statement(self):

            def key_cid(fld_md):
                return fld_md.cid

            res = [u'create table "{0}"({1});'.format(self.tableName,
                                                   u', '.join(fld_md._sql() for fld_md in sorted(self.fields.itervalues(), key=key_cid))),
                   u'alter table "{0}" add primary key({1});'.format(self.tableName,
                                                                  u', '.join([u'"{0}"'.format(fld_name) for fld_name in self.primaryKey]))]
            for uniq in self.uniques:
                res.append(u'alter table "{0}" add unique({1});'.format(self.tableName, u', '.join([u'"{0}"'.format(fld_name) for fld_name in uniq])))
            return res

        @returns(list_of(str))
        def _add_fk_statement(self):
            res = []
            for fk_md in self.fkeys.itervalues():
                res.append(u'alter table "{0}" add foreign key ("{1}") references "{2}"("{3}") on delete {4} on update {5};'.format(
                    self.tableName, fk_md.fieldName, fk_md.refTable, fk_md.refField, fk_md.onDelete, fk_md.onUpdate))
            return res

        @returns(list_of(str))
        def _comment_on_statement(self):
            res = [u"comment on table {0} is '{1}';".format(self.tableName, self.description)]
            for fld_md in self.fields.itervalues():
                if fld_md.description:
                    res.append(u"comment on column \"{0}\".\"{1}\" is '{2}';".format(self.tableName, fld_md.fieldName, fld_md.description))
            return res

    def __init__(self, *modules):
        self.tables = AttrDict()
        for md_module in modules:
            for name, table_cls in md_module.__dict__.iteritems():
                if inspect.isclass(table_cls) and issubclass(table_cls, DBTable) and table_cls is not DBTable:
                    name = name.lower()
                    self.tables[name] = Metadata._Table(table_cls)
        # DONE: заполнить атрибут _FKey.refField
        for table_md in self.tables.itervalues():
            for fkey_md in table_md.fkeys.itervalues():
                self.tables[fkey_md.refTable].isRelation = True
                fkey_md.refField = self.tables[fkey_md.refTable].primaryKey[0]
                for ref_fields_md in self.tables[fkey_md.refTable].fields.itervalues():
                    if ref_fields_md.fkDescription:
                        fkey_md.refShowField = ref_fields_md.fieldName
                        break
                fkey_md.refTableMD = self.tables[fkey_md.refTable]

    # @takes('Metadata', optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
    @returns(nothing)
    def validate(self, log=logging):
        valid = True
        if not self.tables:
            valid = False
            log.error(u'Метаданные пусты.')

        for table_md in self.tables.itervalues():
            valid = table_md.validate(log) and valid

        if not valid:
            raise RuntimeError(u'Метаданные невалидны. См. лог.')

    # @takes('Metadata', DBMetadata, optional(with_attr('debug', 'info', 'warning', 'error', 'critical')))
    @returns(nothing)
    def check_db(self, db_md, log=logging):
        equal = True
        for tbl_name, tbl_md in self.tables.iteritems():
            if tbl_name not in db_md.tables:
                equal = False
                log.error(u'Таблица {0}: отсутствует в базе'.format(tbl_name))
                continue
            equal = tbl_md.check_db(db_md.tables[tbl_name], log) and equal

        if not equal:
            raise RuntimeError(u'Метаданные не соответствуют структуре базы. См. лог.')

    @returns(list_of(str))
    def sql(self):
        res = []
        for tbl_md in self.tables.itervalues():
            res += tbl_md._create_statement()
            res += tbl_md._comment_on_statement()
        for tbl_md in self.tables.itervalues():
            res += tbl_md._add_fk_statement()

        return res


class Field(object):
    u"""Структура метаданных поля"""
    
    def __init__(self, _oRecord, _ordinal_position):
        u"""_oRecord - Запись с метаданными, обязательный параметр"""
        if not _oRecord:
            raise ValueError(u'Не передана запись с метаданными')
        self.fieldName = _oRecord.value(u'field').toString().lower()
        self.cid = _ordinal_position
        self.default = _oRecord.value(u'column_default').toString()
        self.required = _oRecord.value(u'is_nullable').toString()
        self.type = _oRecord.value(u'data_type').toString()
        self.length = _oRecord.value(u'character_maximum_length').toInt()[0]
        self.precision = _oRecord.value(u'numeric_precision').toInt()[0]
        self.alias = _oRecord.value(u'alias').toString() or self.fieldName
        self.visible = _oRecord.value(u'visible').toBool()
        self.visible  = True if self.visible is None else self.visible
        self.description = _oRecord.value(u'description').toString()
        self.visiblePosition = _oRecord.value(u'VisiblePosition').toInt()[0] if not _oRecord.value(u'VisiblePosition').isNull() else None
        self.readonly = _oRecord.value(u'ReadOnly').toBool()
        self.enum = _oRecord.value(u'enum').toString()
        self.enum = self.enum.split(u';') if self.enum else None

class FKey(object):
    u"""Структура метаданных поля"""
    
    def __init__(self, _oRecord):
        u"""_oRecord - Запись с метаданными, обязательный параметр"""
        if not _oRecord:
            raise ValueError(u'Не передана запись с метаданными')
        self.fieldName = _oRecord.value(u'field').toString().lower()
        self.refShowField = _oRecord.value(u'RefShowField').toString().lower()
        self.refAlias = _oRecord.value(u'refalias').toString()
        self.refTable = _oRecord.value(u'ref_name').toString()
        self.refField = _oRecord.value(u'ref_field').toString().lower()
        self.onUpdate = _oRecord.value(u'update_rule').toString()
        self.onDelete = _oRecord.value(u'delete_rule').toString()

class Table(object):
    u""""""
    
    def __init__(self, _sTableName, _alias, _description, _nonAutoCreation , _oQSqlDatabase = None):
        u""""""
        self.oQSqlDatabas = _oQSqlDatabase
        self._sTableName = _sTableName
        self._alias = _alias
        self._description = _description
        self._nonAutoCreation = _nonAutoCreation
        self.fields = AttrDict()
        self.fkeys = AttrDict()
        self._get_field_collection()

    def _get_field_collection(self):
        u"""Заполнить коллекцию объектов метаданных для всех полей таблицы"""
        sQuery = u"""
                    select
                      col.table_name as "table"
                      , col.column_name as field
                      , col.is_nullable
                      , col.data_type
                      , col.character_maximum_length
                      , col.numeric_precision
                      , metafld.alias
                      , metafld.visible
                      , metafld.description
                      , metafld.RefAlias
                      , metafld.RefShowField
                      , metafld.VisiblePosition
                      , metafld.ReadOnly
                      , metafld.enum
                      , ref_column.table_name as ref_name
                      , ref_column.column_name as ref_field
                      , col.ordinal_position 
                      , col.column_default
                      , ref.update_rule
                      , ref.delete_rule
                    from 
                      information_schema.columns col
                    left join
                      information_schema.key_column_usage key_column
                    on
                      col.column_name = key_column.column_name
                      and col.table_name = key_column.table_name
                      and key_column.position_in_unique_constraint is not null
                    left join
                      information_schema.referential_constraints ref
                    on
                      key_column.constraint_name = ref.constraint_name 
                    left join
                      information_schema.key_column_usage ref_column
                    on
                      ref_column.constraint_name = ref.unique_constraint_name
                    left join 
                      meta_field metafld
                    on
                      Upper(col.column_name) = Upper(metafld.Field)
                      and Upper(col.table_name) = Upper(metafld.meta_table)
                    where
                      col.table_name = :sTableName
                    order by
                      col.ordinal_position
                  """
        oQuery = QSqlQuery(self.oQSqlDatabas)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':sTableName', QtCore.QString(self.tableName))
        oQuery.exec_()
        iItem = 0
        while oQuery.next():
            sFieldName = str(oQuery.record().value(u'field').toString())
            self.fields[sFieldName] = Field(oQuery.record(), iItem)
            if oQuery.record().value(u'ref_name').toString():
                self.fkeys[sFieldName] = FKey(oQuery.record())
            iItem += 1
    @property
    def tableName(self):
        u"""Имя таблицы"""
        return self._sTableName
    
    @property
    def alias(self):
        u"""Алиас - альтернативное имя таблицы"""
        return self._alias
    
    @property
    def description(self):
        u"""Описание таблицы"""
        return self._description
    
    @property
    def createModel(self):
        u"""Запрет автосоздания модели"""
        return not self._nonAutoCreation
    
    @property
    def isRelational(self):
        return any(fk_md.refShowField for fk_md in self.fkeys.itervalues())
    
    
class MetaData(object):
    u"""Метаданные таблиц БД"""
    def __init__(self, _oQSqlDatabase = None):
        u"""_oQSqlDatabase - объект базы даннх QtSql.QSqlDatabase, иначе используется подключение по умолчанию"""
        self.oQSqlDatabas = _oQSqlDatabase
        
    def load(self):
        u"""Коллекция объектов Table содержащих метаданные таблиц"""
        tables = AttrDict()
        sQuery = u"""
                SELECT 
                    tab.table_name
                    , meta.alias
                    , meta.description
                    , meta.NonAutoCreate
                FROM 
                    information_schema.tables tab
                left join
                    meta_table meta
                on
                    tab.table_name = meta.tablename
                where
                    tab.table_schema = :schema
                """
        oQuery = QSqlQuery(self.oQSqlDatabas)
        oQuery.prepare(sQuery)
        oQuery.bindValue(u':schema', SCHEMA)
        oQuery.exec_()
        while oQuery.next():
            tableName = oQuery.value(0).toString()
            alias = oQuery.value(1).toString()
            desc = oQuery.value(2).toString()
            noAuto = oQuery.value(3).toPyObject()
            tables[tableName] = Table(tableName, alias, desc, noAuto, self.oQSqlDatabas)
        return tables
