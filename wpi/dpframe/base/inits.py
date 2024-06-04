#coding=utf-8
u"""

"""
#TODO: Описать использование инитов-декораторов и агрегируемых инитов (коробок гвоздей)

import sys, logging, json
from optparse import OptionParser
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase
from dpframe.data.metadata import Metadata, DBMetadata, MetaData
from dpframe.base.session import Session
from dpframe.tech.AttrDict import AttrDict
from dpframe.base.application import get
from dpframe.data.mdmodel import MDRelationalTableModel
from dpframe.tech.typecheck import *

@takes(callable)
@returns(callable)
def requires_env(f):
    u"""
    Декоратор для декоратора класса :)
    Проверяет наличие переменной класса (не объекта) cls.env типа dict.
    Если не существует - создает.
    Является вспомогательным декоратором для инитов-декораторов.

    Не нужно трогать без осознанной необходимости :)
    """

    @takes(type)
    @returns(type)
    def wrapper(cls):
        try:
            if not isinstance(cls.env, dict):
                raise TypeError()
        except AttributeError:

            cls.env = AttrDict()

        except TypeError:

            cls.env = AttrDict()
        return f(cls)
        
    return wrapper

def requires_env_parts(*parts):
    u"""
    Декоратор для декоратора класса :)
    Проверяет соответствие состава cls.env переданным параметрам.
    При несоответствии выбрасывает исключение.

    Бессмысленно использовать вместе с декоратором requires_env,
    т.к. если окружения нет то оно и создастся пустым.

    Является вспомогательным декоратором для инитов-декораторов
    """

    @takes(callable)
    @returns(callable)
    def decorator(f):
        
        @takes(type)
        @returns(type)
        def wrapper(cls):
            res = []
            for part in parts:
                if part not in cls.env:  
                    res.append(part)
            if res:
                raise ValueError(u'Не существуют следующие разделы окружения класса {0}: {1}'.format(cls, res))          
            return f(cls)
        
        return wrapper
    
    return decorator
    

@takes(callable)
@returns(callable)
def requires_app(f):
    u"""
    Декоратор для декоратора класса :)
    Проверяет существование приложения Qt.
    Если не существует - создает.
    Является вспомогательным декоратором для инитов-декораторов
    """
    
    @takes(type)
    @returns(type)
    def wrapper(cls):
        cls._app = get() 
        return f(cls)
        
    return wrapper


@requires_env
@takes(type)
@returns(type)
def default_log_init(cls):
    u"""
    Инит-декоратор.
    Добавляет объект логгера в окружение, лог выводится в консоль.

    Возвращает декорированный класс.

    Примеры использования:

    dpframe.unittest.testinits.App1
    dpframe.gui.mainwnd
    """

    cls.env.log = logging
    return cls


class DBConnParmsNotFoundError(ValueError):
    pass

@requires_env
@requires_app
@takes(type)
@returns(type)
def db_connection_init(cls):
    u"""
    Инит-декоратор.
    Добавляет соединение с БД в окружение.

    Порядок определения параметров соединения:
    1. В sys.argv ищет параметры --host, --database, --user, --password
    2. При наличии раздела окружения cls.env.config, по ключу u'db'
       ищет объект со структурой {u'host': u'', u'database': u'', u'user': u'', u'': u'password'}
    3. В sys.argv ищет параметр --config <имя_файла.json>, парсит файл, по ключу u'db'
       ищет объект со структурой {u'host': u'', u'database': u'', u'user': u'', u'': u'password'}
    4. В текущей директории ищет файл config.json, далее аналогично п.2

    Возвращает декорированный класс.
    """
    #TODO: Юниттесты!!!
    #TODO: В докстринге дописать примеры использования

    log = cls.env.log if u'log' in cls.env else logging
    args = sys.argv[1:]
    parser = OptionParser()
    parser.add_option(u'--host', default=None)
    parser.add_option(u'--database', default=None)
    parser.add_option(u'--user', default=None)
    parser.add_option(u'--password', default=None)
    parser.add_option(u'--config', default=None)
    opts, args = parser.parse_args(list(args))
    if opts.host and opts.database and opts.user and opts.password:
        db = QSqlDatabase.addDatabase(u'QPSQL', cls.__name__)
        db.setHostName(opts.host)
        db.setDatabaseName(opts.database)
        db.setUserName(opts.user)
        db.setPassword(opts.password)
        db.open()
        cls.env.db = db
        return cls
    
    if opts.host or opts.database or opts.user or opts.password:
        log.warning(u'Заданы не все параметры соединения в командной строке: {0}'.format(sys.argv[1:]))

    dbcfg = cls.env.config.get(u'db', {}) if u'config' in cls.env else None
    if dbcfg:
        host = dbcfg.get(u'host', None)
        database = dbcfg.get(u'database', None)
        user = dbcfg.get(u'user', None)
        password = dbcfg.get(u'password', None)
        if host and database and user and password:
            db = QSqlDatabase.addDatabase(u'QPSQL', cls.__name__)
            db.setHostName(host)
            db.setDatabaseName(database)
            db.setUserName(user)
            db.setPassword(password)
            db.open()
            cls.env.db = db
            return cls

        if host or database or user or password:
            log.warning(u'Заданы не все параметры соединения в разделе конфигурации cls.env.config')

    config = AttrDict()
    #Читаем из файла opts.config
    try:
        with open(opts.config) as fp:
            config = json.load(fp, object_pairs_hook=AttrDict)
    except TypeError: # Обработка случая: opts.config == None
        log.warning(u'Не задан параметр командной строки --config.')
    except IOError: # Обработка случая: opts.config не существует
        log.warning(u'Файл {0} не существует.'.format(opts.config))
    except ValueError: # Обработка случая: opts.config не json
        log.warning(u'Файл {0} не соответствует формату JSON'.format(opts.config))

    dbcfg = config.get(u'db', {})
    if dbcfg:
        host = dbcfg.get(u'host', None)
        database = dbcfg.get(u'database', None)
        user = dbcfg.get(u'user', None)
        password = dbcfg.get(u'password', None)
        if host and database and user and password:
            db = QSqlDatabase.addDatabase(u'QPSQL', cls.__name__)
            db.setHostName(host)
            db.setDatabaseName(database)
            db.setUserName(user)
            db.setPassword(password)
            db.open()
            cls.env.db = db
            return cls

        if host or database or user or password:
            log.warning(u'Заданы не все параметры соединения в файле конфигурации {0}'.format(opts.config))

    else:
            log.warning(u'Не найдены параметры соединения в файле конфигурации {0}'.format(opts.config))
            
    #Читаем из файла u'config.json'
    try:

        with open(u'config.json') as fp:
            config = json.load(fp, object_pairs_hook=AttrDict)
    except IOError: # Обработка случая: 'config.json' не существует
        log.error(u'Файл config.json не существует.')
        raise DBConnParmsNotFoundError()
    except ValueError: # Обработка случая: 'config.json' не json
        log.error(u'Файл config.json не соответствует формату JSON')
        raise DBConnParmsNotFoundError()

    dbcfg = config.get(u'db', {})
    if dbcfg:
        host = dbcfg.get(u'host', None)
        database = dbcfg.get(u'database', None)
        user = dbcfg.get(u'user', None)
        password = dbcfg.get(u'password', None)
        if host and database and user and password:
            db = QSqlDatabase.addDatabase(u'QPSQL', cls.__name__)
            db.setHostName(host)
            db.setDatabaseName(database)
            db.setUserName(user)
            db.setPassword(password)
            db.open()
            cls.env.db = db
            return cls

        if host or database or user or password:
            log.error(u'Заданы не все параметры соединения в файле конфигурации config.json')
            raise DBConnParmsNotFoundError()

    else:
            log.error(u'Не найдены параметры соединения в файле конфигурации config.json')
            raise DBConnParmsNotFoundError()
        
    return cls


@requires_env
@takes(type)
@returns(type)
def json_config_init(cls):

    u"""
    Инит-декоратор.
    Добавляет настройки в окружение. Настройки читаются из json-файла в структуру AttrDict
    Должен следовать после инита, создающего лог.

    Порядок определения имени файла настроек:
    2. В sys.argv ищет параметр --config <имя_файла.json>
    3. В текущей директории ищет файл config.json

    Возвращает декорированный класс.
    Примеры использования:

    dpframe.unittest.testinits.App3
    """

    log = cls.env.log if u'log' in cls.env else logging

    args = sys.argv[1:]
    
    parser = OptionParser()
    parser.add_option(u'--config', default=None)
    opts, args = parser.parse_args(list(args))

    config = AttrDict()
    #Читаем из файла opts.config
    try:
        with open(opts.config) as fp:
            config = json.load(fp, object_pairs_hook=AttrDict)
    except TypeError: # Обработка случая: opts.config == None
        log.warning(u'Не задан параметр командной строки --config.')
    except IOError: # Обработка случая: opts.config не существует
        log.warning(u'Файл {0} не существует.'.format(opts.config))
    except ValueError: # Обработка случая: opts.config не json
        log.warning(u'Файл {0} не соответствует формату JSON'.format(opts.config))

    if config:
        cls.env.config = config
        return cls
    
    #Читаем из файла u'config.json'
    try:
        with open(u'config.json') as fp:
            config = json.load(fp, object_pairs_hook=AttrDict)
    except IOError: # Обработка случая: 'config.json' не существует
        log.warning(u'Файл config.json не существует.')
    except ValueError: # Обработка случая: 'config.json' не json
        log.warning(u'Файл config.json не соответствует формату JSON')

    cls.env.config = config
    #TODO: вынести winparam и отдельный инит
    cls.env.winparam = AttrDict(cls.env.config.get(u'winparam', {}))
    print(4342354366)
    return cls


@requires_env_parts(u'db')
@takes(type)
@returns(type)
def metadata_init(cls):
    u"""
    Инит-декоратор.
    Добавляет в окружение объект метаданных базы.
    Требует соединения с базой данных, поэтому должен следовать за инитом, создающим соединение.

    Возвращает декорированный класс.
    """
    cls.env.metadata = MetaData(cls.env.db).load()
    return cls 

def newmetadata_init(*modules):
    u"""
    Инит-декоратор.
    Добавляет в окружение объект новых метаданных базы.
    Требует соединения с базой данных, поэтому должен следовать за инитом, создающим соединение.

    Возвращает декорированный класс.
    """
    @requires_env_parts(u'db', u'log')
    def w(cls):
        cls.env.newmetadata = md = Metadata(*modules)
        md.validate(cls.env.log)
        md.check_db(DBMetadata(cls.env.db), cls.env.log)
        return cls

    return w


@requires_env_parts(u'db', u'metadata')
@takes(type)
@returns(type)
def models_init(cls):
    cls.env.models = AttrDict()
    for tbl_name, md in cls.env.metadata.iteritems():
        if tbl_name in [u'checking']: #Грубый хак, чтобы получить прирост производительности, не грузим гигантскую таблицу
            continue 
        if tbl_name not in [u'meta_table', u'meta_field'] and md.createModel:
            model = MDRelationalTableModel(cls.env.db, md)
            try:
                model.setSort(md.fields.id.cid, Qt.AscendingOrder)
            except KeyError:
                pass
            model.select()
            cls.env.models[tbl_name] = model

    return cls

@requires_env_parts(u'config')
@takes(type)
@returns(type)
def session_init(cls):
    cls.env.session = Session(cls.env.config)
    return cls
