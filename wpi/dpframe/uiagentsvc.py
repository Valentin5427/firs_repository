#!/usr/bin/env python
#coding=utf-8
u"""Модуль запуска приложения, управляющего службой агента.
В качестве настроек ожидает файл dpframe/agent.cfg,
содержащий json-объект, который удовлетворяет схеме
dpframe.tech.json.schema.AGENT_SETTINGS

"""

import json
import sys
import validictory
from PyQt4.QtGui import QMenu, QIcon, QAction, QApplication, QMessageBox
from PyQt4.QtCore import QTimer, SIGNAL
from dpframe.gui.commonapp import SysTrayApp
from dpframe.ui.res import agent
from dpframe.base.agentservice import AgentService
from dpframe.tech.json import schema

class AgentSvcHandler(SysTrayApp.BaseHandler):
    u"""Прикладной обработчик, управлящий службой агента"""
    
    agent_title = u'Dipo Agent'
    
    @property
    def ico(self):
        u"""Вернуть иконку, соответствующую статусу службы"""
        return self.icons.get(self.status, self.icons[None])

    @property
    def menu(self):
        u"""Вернуть контекстное меню"""
        return self._menu
    
    @property
    def tooltip(self):
        u"""Вернуть подсказку, соответствующую статусу службы"""
        return self.tips.get(self.status)
    
    @staticmethod
    def dict2argv(dct):
        u"""Преобразовать словарь параметров в список строк"""
        return [u'-p', dct[u'path']] + \
               ([u'-f', dct[u'log_file']] if u'log_file' in dct and dct[u'log_file'] else []) + \
               ([u'-s'] if u'sys_log' in dct and dct[u'sys_log'] else []) + \
               ([u'-l', unicode(dct[u'log_level'])] if u'log_level' in dct and dct[u'log_level'] else [])
    
    def menu_activated(self, reason):
        u"""Установить активность пунктов контекстного меню в зависимости от статуса службы"""
        status = self.status
        if status == AgentService.NOTINSTALLED:
            self.act_install.setText(u'Установить')
        else:
            self.act_install.setText(u'Обновить')
        self.act_start.setEnabled(status == AgentService.STOPPED)
        self.act_stop.setEnabled(status == AgentService.RUNNING)
        self.act_restart.setEnabled(status == AgentService.RUNNING)
        self.act_pause.setEnabled(status == AgentService.RUNNING)
        self.act_continue.setEnabled(status == AgentService.PAUSED)
        self.act_remove.setEnabled(status == AgentService.STOPPED)

    def __init__(self):
        self.icons = {
            AgentService.NOTINSTALLED: QIcon(u':/main/notinstalled'),
            AgentService.STOPPED: QIcon(u':/main/stopped'),
            AgentService.RUNNING: QIcon(u':/main/started'),
            AgentService.PAUSED: QIcon(u':/main/paused'),
            None: QIcon(u':/main/nostate'),
        }
        templ = self.agent_title + u': {0}'
        self.tips = {
            AgentService.NOTINSTALLED: templ.format(u'Не установлен'),
            AgentService.STOPPED: templ.format(u'Остановлен'),
            AgentService.RUNNING: templ.format(u'Работает'),
            AgentService.PAUSED: templ.format(u'Приостановлен'),
            AgentService.START_PENDING: templ.format(u'Запускается...'),
            AgentService.STOP_PENDING: templ.format(u'Останавливается...'),
            AgentService.CONTINUE_PENDING: templ.format(u'Возобновляется...'),
            AgentService.PAUSE_PENDING: templ.format(u'Приостанавливается...'),
        }
        self._menu = None
        self.create_menu()
        #self._icon = QIcon(u':/main/nostate')
        self.status = None
        try:
            with open(u'agent.cfg') as fsett:
                self.sett = json.load(fsett)
        except ValueError as ex:
            msgBox = QMessageBox()
            msgBox.setText(u"Ошибка загрузки настроек: {0}.".format(unicode(ex)))
            msgBox.exec_()
            sys.exit(1) #not sure
        try:
            validictory.validate(self.sett, schema.AGENT_SETTINGS, required_by_default=False)
        except validictory.ValidationError as ex:
            msgBox = QMessageBox()
            msgBox.setText(u"Некорректный формат настроек: {0}.".format(unicode(ex)))
            msgBox.exec_()
            sys.exit(1) #not sure
        self.agent_args = self.dict2argv(self.sett)
        self.idletimer = QTimer()
        self.idletimer.connect(self.idletimer, SIGNAL(u'timeout()'), self.idle)
        self.idletimer.start()
        
    def idle(self):
        u"""Idle-обработчик. Получить статус службы, установить соответствующую иконку и подсказку"""
        
        self.status = AgentService.QueryServiceStatus()
        self.setIcon(self.ico)
        tip = self.tooltip
        if tip:
            self.setToolTip(tip)
        
    def create_menu(self):
        u"""Создать контекстное меню"""
        
        self.act_start = QAction(QIcon(u':/menu/start'), u'&Запустить', self._menu, triggered=self.start)
        self.act_stop = QAction(QIcon(u':/menu/stop'), u'&Остановить', self._menu, triggered=self.stop)
        self.act_restart = QAction(u'&Перезапустить', self._menu, triggered=self.restart)
        self.act_pause = QAction(QIcon(u':/menu/pause'), u'П&риостановить', self._menu, triggered=self.pause)
        self.act_continue = QAction(u'Пр&одолжить', self._menu, triggered=self.cont)
        self.act_install = QAction(u'&Установить/Обновить', self._menu, triggered=self.install)
        self.act_remove = QAction(u'У&далить', self._menu, triggered=self.remove)
        self.act_quit = QAction(u'&Выход', self._menu, triggered=QApplication.instance().quit)
        
        self._menu = QMenu(self.agent_title)
        self._menu.addAction(self.act_start)
        self._menu.addAction(self.act_stop)
        self._menu.addAction(self.act_restart)
        self._menu.addSeparator()
        self._menu.addAction(self.act_pause)
        self._menu.addAction(self.act_continue)
        self._menu.addSeparator()
        self._menu.addAction(self.act_install)
        self._menu.addAction(self.act_remove)
        self._menu.addSeparator()
        self._menu.addAction(self.act_quit)

    def start(self):
        err = AgentService.Start(self.agent_args)
        if err:
            self.showMessage(self.agent_title, u'Ошибка запуска службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Агент запущен')

    def stop(self):
        err = AgentService.Stop()
        if err:
            self.showMessage(self.agent_title, u'Ошибка остановки службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Агент остановлен')

    def restart(self):
        err = AgentService.Restart(self.agent_args)
        if err:
            self.showMessage(self.agent_title, u'Ошибка перезапуска службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Агент перезапущен')

    def pause(self):
        err = AgentService.Pause()
        if err:
            self.showMessage(self.agent_title, u'Ошибка приостановки службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Агент приостановлен')

    def cont(self):
        err = AgentService.Continue()
        if err:
            self.showMessage(self.agent_title, u'Ошибка возобновления службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Работа агента возобновлена')
        
    def install(self):
        status = AgentService.QueryServiceStatus()
        err = AgentService.Install(self.sett.get(u'start_type'), self.sett.get(u'err_control'),
                                   self.sett.get(u'interactive', False), self.sett.get(u'username'),
                                   self.sett.get(u'password'))
        if err:
            self.showMessage(self.agent_title, u'Ошибка установки службы: {0}'.format(err))
        else:            
            if status == AgentService.NOTINSTALLED:
                self.showMessage(self.agent_title, u'Служба агента установлена')
            else:
                self.showMessage(self.agent_title, u'Служба агента oбновлена')

    def remove(self):
        err = AgentService.Remove()
        if err:
            self.showMessage(self.agent_title, u'Ошибка удаления службы: {0}'.format(err))
        else:
            self.showMessage(self.agent_title, u'Служба агента удалена')


if __name__ == '__main__':
    app = SysTrayApp(AgentSvcHandler, app_unique_name=u'Dipo Agent Runner')
    app.exec_()