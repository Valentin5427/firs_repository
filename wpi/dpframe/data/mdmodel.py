#coding=utf-8
u"""
Created on 23.08.2011

@author: dkasatsky
"""
from collections import defaultdict

from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlDatabase
from PyQt5.QtCore import Qt, QModelIndex, QVariant, QObject#, QDateTime, QDate, QTime
from dpframe.tech.typecheck import *


class MetadataModelMixin(object):

    def __init__(self, metadata):
        self._metadata = metadata

        self.setTable(self._metadata.tableName)
        self.setEditStrategy(self.OnManualSubmit)
        self._set_headers()
        self.defaults = {}

    @returns(nothing)
    def _set_headers(self):
        for fld_md in self._metadata.fields.itervalues():
            self.setHeaderData(fld_md.cid, Qt.Horizontal, fld_md.alias or fld_md.name)

class FilterMixin(object):

    def true(self):
        return u'(1=1)'

    def __init__(self):
        self._filters = defaultdict(self.true)

    @takes('FilterMixin')
    @returns(nothing)
    def set_filter(self, name, fltr):
        fltr = u'({0})'.format(fltr)
        if self._filters[name] != fltr:
            self._filters[name] = fltr
            QSqlTableModel.setFilter(self, u' and '.join(self._filters.itervalues()))
            self.select()


class MDRelationalTableModel (QSqlRelationalTableModel, MetadataModelMixin, FilterMixin):

    # @takes('MDRelationalTableModel', QSqlDatabase, anything, optional(QObject))
    def __init__(self, db, metadata, parent=None):
        super(MDRelationalTableModel, self).__init__(parent, db)
        MetadataModelMixin.__init__(self, metadata)
        FilterMixin.__init__(self)
        self.cache = {} #обновляемый контейнер для хранения связанных данных

        for fk_fld, fk_md in self._metadata.fkeys.iteritems():
            if fk_md.refShowField:
                self.setRelation(self._metadata.fields[fk_fld].cid, QSqlRelation(fk_md.refTable, fk_md.refField, fk_md.refShowField))

    @takes('MDRelationalTableModel', int, QSqlRelation)
    @returns(nothing)
    def setRelation(self, column, relation):
        u"""
        Перегрузка функции QSqlRelationalTableModel.setRelation
        Дополнительно инициализирует контейнер для соответствующей колонки
        """
        super(MDRelationalTableModel, self).setRelation(column, relation)
        self.cache[column] = {}

    # @takes('MDRelationalTableModel', QModelIndex, optional(int))
    @returns(QVariant)
    def data(self, index, role=Qt.DisplayRole):
        u"""
        Перегрузка функции QSqlRelationalTableModel.data
        Заполняет контейнер данными для соответствующей колонки,
        если еще не заполнен
        """
        col = index.column()
        if col in self.cache and not self.cache[col]:
            self._populateDictionary(col)
        val = QSqlRelationalTableModel.data(self, index, role)
        if not val.isValid() and Qt.DisplayRole == role:
            tm_val = QSqlTableModel.data(self, index, role)
            if tm_val.isValid() and not tm_val.isNull():
                return self.cache[col][tm_val.toPyObject()]
        return val

    # @takes('MDRelationalTableModel', QModelIndex, QVariant, optional(int))
    @returns(bool)
    def setData(self, index, value, role=Qt.EditRole):
        u"""
        Перегрузка функции QSqlRelationalTableModel.data
        Заполняет контейнер данными для соответствующей колонки,
        если еще не заполнен.
        Проверка на валидность внешнего ключа использует self.cache, а не
        внутренний контейнер QSqlRelationalTableModel
        """
        col = index.column()
        if Qt.EditRole == role and col > 0 and self.relation(col).isValid():
            if not self.cache[col]:
                self._populateDictionary(col)
            if not value.isNull() and value.toPyObject() not in self.cache[col]:
                return False
        return QSqlTableModel.setData(self, index, value, role)

    @returns(nothing)
    def _populateDictionary(self, column):
        u"""
        Заполнение контейнера соответствующей колонки из связанной модели.
        Контейнер предварительно не очищается.
        Функция предназначена для использования только внутри класса.
        """
        rel_model = self.relationModel(column)
        rel = self.relation(column)
        for i in xrange(0, rel_model.rowCount()):
            rec = rel_model.record(i)
            self.cache[column][rec.field(rel.indexColumn()).value().toPyObject()] = \
                rec.field(rel.displayColumn()).value().toPyObject()

    @returns(nothing)
    def relationRefresh(self, column):
        u"""
        Обновление контейнера соответствующей колонки из связанной модели
        с предварительной очисткой и обновлением связанной модели.
        """
        rel_model = self.relationModel(column)
        if rel_model:
            rel_model.select()
            self.cache[column] = {}
            self._populateDictionary(column)

    @returns(nothing)
    def relationsRefresh(self):
        u"""
        Обновление контейнеров всех колонок из связанных моделей.
        """
        for i in xrange(0, self.columnCount()):
            self.relationRefresh(i)

    @returns(str)
    def _get_rel_select(self):
        u"""Вариант без использования метаданных, не чистите, может пригодиться"""
        tname = self.tableName()
        fields = []
        joins = []
        rec = self.record()
        for cid in range(rec.count()):
            fname = rec.fieldName(cid)
            relation = self.relation(cid)
            if relation.isValid():
                reftable = relation.tableName()
                alias = u't{0}'.format(cid)
                reffld = relation.indexColumn()
                fields.append(u'{0}.{1}'.format(alias, relation.displayColumn()))
                joins.append(u'left join {reftable} {alias} on {tname}.{fname} = {alias}.{reffld}'.format(**locals()))
            else:
                fields.append(u'{0}.{1}'.format(tname, fname))
        filter = self.filter()
        filter = u'1=1' if not filter else filter
        return u'select {0} from {1} {2} where({3}) {4}'.format(u', '.join(fields), tname, u' '.join(joins), filter, unicode(self.orderByClause()))

    @returns(str)
    def _get_md_select(self):
        tname = self._metadata.tableName
        fields = []
        joins = []
        for cid, fname in sorted((fld_md.cid, fld_md.fieldName) for fld_md in self._metadata.fields.itervalues()):
            if fname in self._metadata.fkeys:
                reftable = self._metadata.fkeys[fname].refTable
                alias = u'relTblAl_{0}'.format(cid)
                reffld = self._metadata.fkeys[fname].refField
                if self._metadata.fkeys[fname].refShowField:
                    fields.append(u'{0}.{1}'.format(alias, self._metadata.fkeys[fname].refShowField))
                    joins.append(u'left join {reftable} {alias} on {tname}.{fname} = {alias}.{reffld}'.format(**locals()))
                else:
                    raise Exception(u'Meta data error. Link from table "%s" to table "%s" by reffields "%s", not exists fields "%s"' % (tname, self._metadata.fkeys[fname].refTable, fname, self._metadata.fkeys[fname].refShowField))
            else:
                fields.append(u'{0}.{1}'.format(tname, fname))
        filter = self.filter()
        filter = u'1=1' if not filter else filter
        return u'select {0} from {1} {2} where({3}) {4}'.format(u', '.join(fields), tname, u' '.join(joins), filter, unicode(self.orderByClause()))

    # @returns(QString)
    @returns(str)
    def selectStatement(self):
        return str(self._get_md_select())

    def insert(self, **kwargs):
        row_idx = self.rowCount()
        self.insertRow(row_idx)
        for fname, val in kwargs.items():
            self.setData(self.index(row_idx, self._metadata.fields[fname].cid), QVariant(val))

    def nowDB(self):
        sql = u'SELECT now()'
        oQuery = self.query()
#        oQuery = QSqlQuery(self.env.db)
        oQuery.prepare(sql)
        if oQuery.exec_() and oQuery.first():
            return oQuery.record().value(0).toDateTime()
        else:
#            return QDateTime(QDate().currentDate(),QTime().currentTime())
            raise Exception(u'Не удалось взять время из БД')

