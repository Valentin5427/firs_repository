#coding=utf-8
u"""
Декораторы для описания полей
"""


class DBType(object):
    integer = u'integer'
    numeric = u'numeric'
    varchar = u'varchar'
    char = u'character'
    text = u'text'
    timestamp = u'timestamp'
    date = u'date'
    time = u'time'
    bool = u'boolean'

DB_DEFAULTS = {
    DBType.integer: u'0',
    DBType.numeric: u'0.0',
    DBType.varchar: u"''",
    DBType.char: u"''",
    DBType.text: u"''",
    DBType.timestamp: u"'01.01.0000'",
    DBType.date: u"'01.01.0000'",
    DBType.time: u"'00:00'",
    DBType.bool: u'false'
}

class FKAction(object):
    noAction = u'NO ACTION'
    restrict = u'RESTRICT'
    cascade = u'CASCADE'
    setNull = u'SET NULL'
    setDefault = u'SET DEFAULT'


class MetaDBTable(type):
    fld_classes = []
    def __init__(cls, name, bases, dct):
        inner_classes = set(incls for incls in dct.itervalues() if issubclass(incls.__class__, MetaDBField))
        lst = []
        for fldcls in MetaDBTable.fld_classes:
            if fldcls in inner_classes:
                fldcls.cid = len(lst)
                lst.append(fldcls)
        cls.fld_classes = lst
        MetaDBTable.fld_classes = []
        super(MetaDBTable, cls).__init__(name, bases, dct)

class MetaDBField(type):
    def __init__(cls, name, bases, dct):
        MetaDBTable.fld_classes.append(cls)
        super(MetaDBField, cls).__init__(name, bases, dct)

class DBTable(object):
    __metaclass__ = MetaDBTable

    fld_classes = []
    
    display = u''
    createmodel = True

    uniques = []
    displayOrder = []


class DBField(object):
    __metaclass__ = MetaDBField

    cid = None

    primary_key = False
    default = None
    required = False
    unique = False
    display = u''
    visible = True
    readonly = False
    fkdescription = False

    type = None
    autoinc = False
    max = None
    min = None
    prec = None
    length = 0

    reference = None
    parent = None
    
    enum = None

    
def nocreatemodel(cls):
    cls.createmodel = False
    return cls

def default(value):
    def w(cls):
        cls.default = value
        return cls
    return w

def required(cls):
    cls.required = True
    return cls

def unique(cls):
    cls.unique = True
    return cls

def primary_key(cls):
    cls.primary_key = True
    cls.required = True
    return cls

# интерфейсные декораторы
def display(dspl_str):
    def w(cls):
        cls.display = dspl_str
        return cls
    return w

def invisible(cls):
    cls.visible = False
    return cls

def readonly(cls):
    cls.readonly = True
    return cls

def fk_description(cls):
    cls.fkdescription = True
    return cls

# декораторы типов, читайте внимательно докстринги
def integer(*args, **kwargs):
    if len(args) and issubclass(args[0], DBField):
        args[0].type = DBType.integer
        return args[0]
    else:
        def w(cls):
            cls.type = DBType.integer
            cls.autoinc = kwargs.get(u'autoinc', False)
            cls.max = kwargs.get(u'max')
            cls.min = kwargs.get(u'min')
            return cls
        return w

def numeric(*args, **kwargs):
    if len(args) and issubclass(args[0], DBField):
        args[0].type = DBType.numeric
        return args[0]
    else:
        def w(cls):
            cls.type = DBType.numeric
            cls.max = kwargs.get(u'max')
            cls.min = kwargs.get(u'min')
            cls.prec = kwargs.get(u'precision')
            cls.length = kwargs.get(u'length')
            return cls
        return w

def timestamp(cls):
    cls.type = DBType.timestamp
    return cls

def varchar(length):
    def w(cls):
        cls.type = DBType.varchar
        cls.length = length
        return cls
    return w

def char(length):
    def w(cls):
        cls.type = DBType.char
        cls.length = length
        return cls
    return w

def text(cls):
    cls.type = DBType.text
    return cls

def boolean(cls):
    cls.type = DBType.bool
    return cls

#декораторы ссылок

def reference(table_name):
    def w(cls):
        cls.reference = table_name
        return cls
    return w

def parent(table_name):
    def w(cls):
        cls.parent = table_name
        return cls
    return w

def enum(**kwargs):
    def w(cls):
        cls.enum = kwargs
        return cls
    return w