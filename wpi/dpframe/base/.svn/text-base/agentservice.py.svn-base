#!/usr/bin/env python
#coding=utf-8

from dpframe.base.basedaemon import BaseDaemon
from dpframe.base.agent import Agent, OptParser

class AgentService(BaseDaemon):
    u'''Служба/демон агента'''
    
    _svc_name_ = u'DipoAgent'
    _svc_display_name_ = u'Dipo Agent'
    _svc_description_ = u'Периодически выполняет задания, написанные на Python.'

    def __init__(self, args):
        u'''Попарсить параметры, создать экземпляр агента.
        Параметры:
        args - список или кортеж строк
        
        '''
        args = list(args)
        BaseDaemon.__init__(self, args)
        parser = OptParser(args)
        self.agent = Agent(parser.options.path, parser.options.log_file, parser.options.sys_log, parser.options.log_level)

    def _do(self):
        u'''Выполнить проверку необходимости запуска задач'''
        self.agent.run()
    
    def _start(self):
        u'''При старте (рестарте) службы заново загрузить задачи агента'''
        try:
            self.agent.load()
        except ValueError as ex:
            self.agent.log.error(unicode(ex))
            #sys.exit(1)
            raise


