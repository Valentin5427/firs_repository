#!/usr/bin/env python
#coding=utf-8

import unittest
import os, sys
from datetime import datetime
import logging

from dpframe.base.agent import Agent, Schedule, Task
from dpframe.base.agentservice import AgentService, OptParser
from dpframe.tech.json import schema
from dpframe.uiagentsvc import AgentSvcHandler
import validictory

class AgentTestCase(unittest.TestCase):

    def testLoadSingleTaskInSingleFile(self):
        agent = Agent(u'./examples/agent/tasks/tasks1.tsk', syslog=True)
        self.assertTrue(agent.load())
        self.assertEqual(len(agent.tasks), 1)
        if agent.log_filename:
            self.assertTrue(os.path.exists(agent.log_filename))

    def testLoadMultipleTaskInSingleFile(self):
        agent = Agent(u'./examples/agent/tasks/tasks2.tsk', syslog=True)
        self.assertFalse(agent.load())
        self.assertEqual(len(agent.tasks), 2)
        if agent.log_filename:
            self.assertTrue(os.path.exists(agent.log_filename))

    def testLoadFromDir(self):
        agent = Agent(u'./examples/agent/', syslog=True)
        self.assertFalse(agent.load())
        self.assertEqual(len(agent.tasks), 3)
        if agent.log_filename:
            self.assertTrue(os.path.exists(agent.log_filename))

    def _set_log_filename(self):
        agent = Agent()
        agent.log_filename = u'filename'

    def testReadonlyLogFilename(self):
        self.assertRaises(AttributeError, self._set_log_filename)


class ScheduleTestCase(unittest.TestCase):

    def setUp(self):
        schdct = {
            u'cron': u'*/2 * * * *',
            u'start': u'2011-01-01T00:00:00Z',
            u'stop': u'2011-01-01T18:34:08Z',
        }
        schdct2 = {
            u'cron': u'0 0 1 */2 *',
        }

        self.sch = Schedule(schdct)
        self.sch2 = Schedule(schdct2)

    def testScheduleDateTypes(self):
        self.assertTrue(isinstance(self.sch.start, datetime))
        self.assertTrue(isinstance(self.sch.stop, datetime))
        self.assertTrue(isinstance(self.sch2.start, datetime))
        self.assertTrue(isinstance(self.sch2.stop, datetime))

    def testParseValidCron(self):
        self.assertEqual(self.sch._parse_cron(u'* *   * * *'), (set(range(0, 60)), set(range(0, 24)), set(range(1, 32)), set(range(1, 13)), set(range(1, 8))))
        self.assertEqual(self.sch._parse_cron(u'17 *   * * *'), (set([17]), set(range(0, 24)), set(range(1, 32)), set(range(1, 13)), set(range(1, 8))))
        self.assertEqual(self.sch._parse_cron(u'47 6    * * 7'), (set([47]), set([6]), set(range(1, 32)), set(range(1, 13)), set([7])))
        self.assertEqual(self.sch._parse_cron(u'0 22 * * 1-5'), (set([0]), set([22]), set(range(1, 32)), set(range(1, 13)), set(range(1, 6))))
        self.assertEqual(self.sch._parse_cron(u'23 */2 * * *'), (set([23]), set(range(0, 24, 2)), set(range(1, 32)), set(range(1, 13)), set(range(1, 8))))
        self.assertEqual(self.sch._parse_cron(u'0 0 1 1 *'), (set([0]), set([0]), set([1]), set([1]), set(range(1, 8))))
        self.assertEqual(self.sch._parse_cron(u'15 10,13 * * 1,4-6'), (set([15]), set([10, 13]), set(range(1, 32)), set(range(1, 13)), set([1] + range(4, 7))))
        self.assertEqual(self.sch._parse_cron(u'15, 10,13 * * ,1,4-6'), (set([15]), set([10, 13]), set(range(1, 32)), set(range(1, 13)), set([1] + range(4, 7))))
        self.assertEqual(self.sch._parse_cron(u'0-45/5 * * * *'), (set(range(0, 46, 5)), set(range(0, 24)), set(range(1, 32)), set(range(1, 13)), set(range(1, 8))))

    def testParseInvalidCron(self):
        # Заполняем по мере поступления, уж слишком непаханное поле
        pass

    def testFirstCheckSchedule(self):
        self.assertEqual(self.sch.match(datetime(2011, 1, 1, 2, 22, 30, 125)), True)
        self.assertEqual(self.sch.match(datetime(2011, 1, 1, 2, 22, 30, 128)), False)
        self.assertEqual(self.sch.match(datetime(2011, 1, 1, 2, 22, 39, 0)), False)
        self.assertEqual(self.sch.match(datetime(2011, 1, 1, 2, 23, 54, 128)), False)
        self.assertEqual(self.sch.match(datetime(2011, 1, 1, 2, 24, 18, 782)), True)


    def testPrevCheckSchedule(self):
        current = datetime(2010, 1, 1, 2, 21, 30)
        self.assertEqual(self.sch.match(current), False)

    def testPostCheckSchedule(self):
        current = datetime(2012, 1, 1, 2, 21, 30)
        self.assertEqual(self.sch.match(current), False)

class AgentOptParserTestCase(unittest.TestCase):

    def create(self):
        self.svc = AgentService()

    def testAgentSvcConstructor1(self):
        p = OptParser([u'-p', u'C:/temp', u'-l', u'info', u'-s', u'-f', u'./agent.log'])
        self.assertEqual(p.options.path, u'C:/temp')
        self.assertEqual(p.options.log_file, u'./agent.log')
        self.assertEqual(p.options.sys_log, True)
        self.assertEqual(p.options.log_level, logging.INFO)

        agent = Agent(p.options.path, p.options.log_file, p.options.sys_log, p.options.log_level)
        self.assertEqual(agent.tpath, u'C:/temp')
        self.assertEqual(agent.log_filename, u'./agent.log')
        self.assertEqual(agent.sys_log, True)
        self.assertEqual(agent.log_level, logging.INFO)

    def testAgentSvcConstructor2(self):
        p = OptParser((u'DipoAgent', u'-p', u'C:\\Work\\Dipo\\dpframe\\examples\\agent\\tasks\\tasks1.py', u'-s', u'-l', u'debug'))
        self.assertEqual(p.options.path, u'C:\\Work\\Dipo\\dpframe\\examples\\agent\\tasks\\tasks1.py')
        self.assertEqual(p.options.log_file, u'')
        self.assertEqual(p.options.sys_log, True)
        self.assertEqual(p.options.log_level, logging.DEBUG)

        agent = Agent(p.options.path, p.options.log_file, p.options.sys_log, p.options.log_level)
        self.assertEqual(agent.tpath, u'C:\\Work\\Dipo\\dpframe\\examples\\agent\\tasks\\tasks1.py')
        self.assertEqual(agent.log_filename, u'')
        self.assertEqual(agent.sys_log, True)
        self.assertEqual(agent.log_level, logging.DEBUG)

    def testAgentSvcConstructorDefault(self):
        p = OptParser([])
        self.assertEqual(p.options.path, None)
        self.assertEqual(p.options.log_file, u'')
        self.assertEqual(p.options.sys_log, False)
        self.assertEqual(p.options.log_level, logging.WARNING)


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        self.dct = {
            u'name': u'empty',
            u'active': True,
            u'executable': {
                u'module': u'dpframe.examples.agent.tasks',
                u'func': u'task_empty'
            },
            u'log_file': u'',
            u'sys_log': True,
            u'log_level': u'debug',
            u'schedule': {
                u'cron': u'* * * * *',
                u'start': u'1900-01-01T00:00:00Z',
                u'stop': u'2011-05-01T13:00:00Z'
            }
        }
        validictory.validate(self.dct, schema.AGENT_TASK, required_by_default=False)
        self.t = Task(self.dct)

    def testAutoDeactivate(self):
        self.assertTrue(self.t.active)
        self.t.try_(datetime(2010, 1, 1))
        self.assertTrue(self.t.active)
        self.t.try_(datetime(2012, 1, 1))
        self.assertFalse(self.t.active)

    def testTaskLog(self):
        self.assertTrue(self.t.env.log.sys_)
        self.assertEqual(self.t.env.log.filename, u'')
        self.assertEqual(len(self.t.env.log.handlers), 1)
        if u'win32' == sys.platform:
            self.assertEqual(self.t.env.log.handlers[0].__class__, logging.handlers.NTEventLogHandler)
        else:
            self.assertEqual(self.t.env.log.handlers[0].__class__, logging.handlers.SysLogHandler)

class ParamsTestCase(unittest.TestCase):

    def testJSON2argv(self):
        dct = {
                u'path': u'C:\\Work\\Dipo\\dpframe\\examples\\agent\\tasks\\tasks1.py',
                u'sys_log': True,
                u'log_level': u'debug'
        }
        validictory.validate(dct, schema.AGENT_SETTINGS, required_by_default=False)
        self.assertEqual(AgentSvcHandler.dict2argv(dct), [u'-p', u'C:\\Work\\Dipo\\dpframe\\examples\\agent\\tasks\\tasks1.py', u'-s', u'-l', u'debug'])


if __name__ == '__main__':
    unittest.main()


