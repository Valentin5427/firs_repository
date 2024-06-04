#!/usr/bin/env python
#coding=utf-8
u'''Запуск службы агента из консольной строки.
Использование: %prog [параметры] команда

Команда: install|remove|start|stop|restart
Параметры для команды install:
    --username domen\\user   пользователь, под которым запускается служба
    --password пароль        пароль пользователя 
    --startup тип_запуска    тип запуска службы [manual|auto|disabled], по умолчанию manual
    --interactive            разрешить службе доступ к рабочему столу
    --perfmonini файл        ini-файл для регистрации данных системного монитора ???
    --perfmondll file        dll-файл, используемый при запросе у службы данных производительности,
                             по умолчанию perfmondata.dll

Параметры для команд start/restart:
    --path (-p) путь           путь для поиска описаний заданий. Если путь к директории,
                               ищет в ней файлы по маске '*.tsk'. Файлы описания заданий
                               в формате JSON, содержащие объект или массив объектов,
                               удовлетворяющих схеме dpframe.tech.json.schema.AGENT_TASK
    --level (-l) уровень_лога  [debug|info|warning|error|critical], по умолчанию warning
    --log-file (-f) путь       путь к файлу лога
    --sys-log (-s)             признак записи в системный лог
    --wait секунд              пауза перед запуском (применима и для команды stop)
'''

import sys
import os.path
from optparse import OptionParser
import win32serviceutil
from dpframe.base.agentservice import AgentService, OptParser

if __name__ == '__main__':
    parser = OptParser()
    if len(sys.argv) == 1 or parser.options.help or not parser.args:
        print __doc__.replace(u'%prog', os.path.split(sys.argv[0])[-1])
    else:
        win32serviceutil.HandleCommandLine(AgentService)

