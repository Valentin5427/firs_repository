#!/usr/bin/env python
#coding=utf-8

u'''Модуль реализует функциональность агента'''

import os.path
import json
import logging.handlers
import sys
import collections
import validictory
from datetime import datetime
import re
import thread
from optparse import OptionParser

from dpframe.tech.json import schema
from dpframe.tech.AttrDict import AttrDict
from dpframe.base.envapp import checkenv


class OptParser(object):
    u'''Парсер параметров командной строки'''
    
    levels = {
        u'debug': logging.DEBUG,
        u'info': logging.INFO,
        u'warning': logging.WARNING,
        u'error': logging.ERROR,
        u'critical': logging.CRITICAL
    }
    
    def __init__(self, args=sys.argv[1:]):
        parser = OptionParser(add_help_option=False)
        parser.add_option(u'--username')
        parser.add_option(u'--password')
        parser.add_option(u'--startup')
        parser.add_option(u'--interactive')
        parser.add_option(u'--perfmonini')
        parser.add_option(u'--perfmondll')
        parser.add_option(u'--wait')
        parser.add_option(u'-p', u'--path', dest=u'path')
        parser.add_option(u'-l', u'--level', dest=u'log_level', type=u'choice', choices=[u'debug', u'info', u'warning', u'error', u'critical'], default=u'warning')
        parser.add_option(u'-f', u'--log-file', dest=u'log_file', default=u'')
        parser.add_option(u'-s', u'--sys-log', dest=u'sys_log', action=u'store_true', default=False)
        parser.add_option(u'-h', u'--help', action=u'store_true', default=False)
        self.options, self.args = parser.parse_args(list(args))
        self.options.log_level = self.levels[self.options.log_level]


class AgentLogger(logging.Logger):
    u'''Логгер агента.
    Расширяет функциональность стандартного логгера данными об имени файла лога,
    уровне лога и о наличии вывода в системный лог.
    
    '''
    
    def __init__(self, name, level=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
        self.filename = None
        self.sys_ = False
        self.level = level


def getLogger(name, file=None, syslog=False, level=logging.WARNING, format=u'%(asctime)s - %(levelname)s - %(message)s'):
    u'''Создать или получить экземпляр логгера агента.
    Параметры:
    name - уникальное имя логгера
    file - имя файла лога, если bool(file) == False - лог не выводится в файл
    syslog - признак вывода в системный лог
    level - уровень лога
    format - формат строки лога
    
    '''
    old_log_class = logging.getLoggerClass()
    logging.setLoggerClass(AgentLogger)
    log = logging.getLogger(name)
    log.level = level
    log.filename = file
    if not log.handlers:
        if file:
            fhandler = logging.FileHandler(file)
            fhandler.setLevel(level)
            fhandler.setFormatter(logging.Formatter(format))
            log.addHandler(fhandler)
        if syslog:
            if sys.platform.startswith(u'win'):
                shandler = logging.handlers.NTEventLogHandler(name)
            else:
                shandler = logging.handlers.SysLogHandler()
            shandler.setLevel(level)
            shandler.setFormatter(logging.Formatter(format))
            log.addHandler(shandler)
            log.sys_ = True
    logging.setLoggerClass(old_log_class)
    return log


class Schedule(object):
    u'''Расписание задачи агента.
    Проверяет необходимость запуска задачи в данное время.
    Использует формат cron.
    
    '''
    
    __format = u'%Y-%m-%dT%H:%M:%SZ'
    __bounds = {
        0: (0, 59),
        1: (0, 23),
        2: (1, 31),
        3: (1, 12),
        4: (1, 7)
    }
    
    def _parse_cron(self, cron):
        u'''Парсить строку cron'''
        
        parts = re.split(ur'\s+', cron)
        if len(parts) != 5:
            raise ValueError(u"Некорректный формат cron, строка '{0}' должна содержать 5 элементов через пробелы.")
        
        compiled = []
        for i, part in enumerate(parts):
            partcompiled = set()
            for item in part.split(u','):
                if item:
                    if u'/' in item:
                        val, step = item.split(u'/')
                        step = int(step)
                    else:
                        val, step = item, 1
                    if u'*' == val:
                        start, stop = self.__bounds[i]
                    elif u'-' in val:
                        start, stop = [int(b) for b in val.split(u'-')]
                    else:
                        start, stop = int(val), int(val)
                    stop += 1
                    
                    partcompiled |= set(range(start, stop, step))
            compiled.append(partcompiled)
        return tuple(compiled)
    
    def __init__(self, scheduledict):
        self.start = datetime.strptime(scheduledict.get(u'start', datetime.strftime(datetime.today(), self.__format)), self.__format)
        self.stop = datetime.strptime(scheduledict.get(u'stop', datetime.strftime(datetime.max, self.__format)), self.__format)
        self.cron = self._parse_cron(scheduledict[u'cron'])
        self.last = None
        
    def match(self, current):
        u'''Проверить, удовлетворяет ли время current выражению cron'''
        
        current = datetime(current.year, current.month, current.day, current.hour, current.minute)
        res = (self.last != current
                and self.start <= current <= self.stop 
                and current.minute in self.cron[0]
                and current.hour in self.cron[1]
                and current.day in self.cron[2]
                and current.month in self.cron[3]
                and current.isoweekday() in self.cron[4]
                )
        if res:
            self.last = current
        return res
    

class TaskInit(object):
    u'''
    Агрегируемый инит задачи агента. Создаваемое окружение содержит:
    self.env.params - параметры задаче (AttrDict);
    self.env.log    - логгер.
    
    Доступ к параметрам задачи может осуществляться как в стиле словаря (self.env.params[u'pname']),
    так и в атрибутном стиле (self.env.params.pname)
    
    '''
    
    def __init__(self, taskdict):
        self.env = AttrDict()
        self.env.params = AttrDict.toAttrDict(taskdict.get(u'params', {}))
        self.env.log = getLogger(name=u"Dipo Agent Task {0}".format(taskdict[u'name']),
                             file=taskdict.get(u'log_file', None),
                             syslog=taskdict.get(u'sys_log', False),
                             level=OptParser.levels[taskdict.get(u'log_level',u'warning')],
                            )

@checkenv(u'log', u'params')
class Task(object):
    u'''Задача агента.
    Содержит ссылку на функцию, выполняемую по расписанию.
    
    '''
    
    def __init__(self, taskdict):
        u'''Параметры:
        taskdict - словарь, удовлетворяющий схеме dpframe.tech.json.schema.AGENT_TASK
        '''
        
        self.name = taskdict[u'name']
        self.displayname = taskdict.get(u'display_name', self.name)
        self.active = taskdict[u'active']
        module_name = taskdict[u'executable'][u'module']
        func_name = taskdict[u'executable'][u'func']
        try:
            module = __import__(module_name, fromlist=[func_name])
        except ImportError:
            raise ImportError(u"Невозможно загрузить модуль '{0}' для задачи '{1}'. Возможно его не существует.".format(module_name, self.displayname))
        try:
            self.executable = getattr(module, func_name)
        except AttributeError:
            raise AttributeError(u"В модуле '{0}' нет атрибута '{1}'.".format(module_name, func_name))
        if not isinstance(self.executable, collections.Callable):
            raise TypeError(u"Объект '{0}' модуля '{1}' не является вызываемым.".format(func_name, module_name))
        self.schedule = Schedule(taskdict[u'schedule'])
        self.env = TaskInit(taskdict).env
        
    def try_(self, current):
        u'''Проверить, нужно ли запускать задачу'''
        
        #self.log.debug(u"Проверка необходимости выполнения задачи {0}.".format(self.displayname))
        if current > self.schedule.stop:
            self.active = False
            self.env.log.info(u"Задача '{0}' деактивирована. Срок действия истек {1}.".format(self.displayname, self.schedule.stop))
        if self.active and self.schedule.match(current):
            self.run()

    def run(self):
        u'''Запустить задачу в новом потоке'''
        
        self.env.log.debug(u"Задача '{0}' запущена.".format(self.displayname))
        thread.start_new_thread(self.executable, (self.env,))
        
        
        
class Agent(object):
    u'''Агент'''
    
    _taskext = u'.tsk'

    def __init__(self, task_path=os.path.curdir, log_file=None, syslog=False, log_level=logging.WARNING):
        u'''Параметры:
        task_path - путь поиска описаний задач. Если путь к файлу - пытаемся загрузить задачи из него,
                    если к директории - ищем в ней рекурсивно файлы *.tsk. Файлы задач должны содержать
                    объект или массив объектов, удовлетворяющих схеме dpframe.tech.json.schema.AGENT_TASK
        
        '''
        
        self.tpath = task_path
        self.tasks = {}
        self.log = getLogger(u'Dipo Agent {0}'.format(id(self)), log_file, syslog, log_level)
        self.loadwarn = None
        
    @property
    def log_filename(self):
        u'''Имя файла лога агента'''
        
        try:
            return self.log.filename
        except AttributeError:
            return None
        
    @property
    def sys_log(self):
        u'''Признак вывода в системный лог'''
        
        try:
            return self.log.sys_
        except AttributeError:
            return None
        
    @property
    def log_level(self):
        u'''Уровень лога'''
        
        try:
            return self.log.level
        except AttributeError:
            return logging.NOTSET

    def _load_file(self, path):
        u'''Загрузить задачи из файла path'''
        
        with open(path) as fp:
            try:
                task = json.load(fp)
            except ValueError as ex:
                self.log.error(u"Файл '{0}' имеет некорректный формат: {1}.".format(path, unicode(ex)))
                self.loadwarn = True
                return
            if not isinstance(task, collections.Sequence):
                task = [task]
            for tsk in task:
                try:
                    validictory.validate(tsk, schema.AGENT_TASK, required_by_default=False)
                except validictory.ValidationError as ex:
                    self.log.warning(unicode(ex))
                    self.loadwarn = True
                    continue
                try:
                    tsk = Task(tsk)
                except ImportError as ex:
                    self.log.warning(unicode(ex))
                    self.loadwarn = True
                    continue
                except AttributeError as ex:
                    self.log.warning(unicode(ex))
                    self.loadwarn = True
                    continue
                if tsk.name in self.tasks:
                    self.log.warning(u"Дублирование идентификатора задачи '{0}': id - '{1}'. Задача не загружена.".format(tsk.displayname, tsk.name))
                    self.loadwarn = True
                    continue
                self.tasks[tsk.name] = tsk
                if tsk.active:
                    self.log.info(u"Загружена активная задача '{0}'.".format(tsk.displayname))
                else:
                    self.log.info(u"Загружена неактивная задача '{0}', выполняться не будет.".format(tsk.displayname))
        
    @staticmethod
    def _visit(self, dirname, names):
        for name in names:
            if name.endswith(self._taskext):
                path = os.path.abspath(os.path.join(dirname, name))
                self._load_file(path)                

    def load(self, task_path=None):
        u'''Загрузить все задачи.
        Параметры:
        task_path - путь поиска описаний задач. Если путь к файлу - пытаемся загрузить задачи из него,
                    если к директории - ищем в ней рекурсивно файлы *.tsk. Файлы задач должны содержать
                    объект или массив объектов, удовлетворяющих схеме dpframe.tech.json.schema.AGENT_TASK
        
        '''
        path = os.path.abspath(task_path or self.tpath)
        self.loadwarn = False
        self.tasks = {}
        if os.path.exists(path):
            if os.path.isdir(path):
                os.path.walk(path, self._visit, self)
            else:
                self._load_file(path)
        else:
            raise ValueError(u"Путь '{0}' не существует. Задачи не загружены.".format(path))
        return not self.loadwarn

    def run(self):
        u'''Запустить проверку необходимости запуска задач.
        Должна вызываться циклически с частотой не реже раз в минуту.
        
        '''
        current = datetime.today()
        for task in self.tasks.itervalues():
            task.try_(current)


