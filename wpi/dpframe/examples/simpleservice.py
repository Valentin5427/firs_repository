#coding=utf-8

import win32serviceutil
import servicemanager as smgr

from dpframe.base.basedaemon import BaseDaemon

class SimpleService(BaseDaemon):

    _svc_name_ = u'SimpleService'
    _svc_display_name_ = u'Демо-служба на Python\'е'
    _svc_description_ = u'Демонстрация возможностей Python и PyWin32 по созданию полноценных служб Windows'

    def _do(self):
        smgr.LogInfoMsg(u'Работаю, работаю, работаю.')

    def _start(self):
        smgr.LogInfoMsg(u'Старт. Параметры: {0}'.format(self.args))

    def _stop(self):
        smgr.LogInfoMsg(u'Стоп.')

    def _pause(self):
        smgr.LogInfoMsg(u'Пауза.')

    def _resume(self):
        smgr.LogInfoMsg(u'Возобновление работы.')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SimpleService)
