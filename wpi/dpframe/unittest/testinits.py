#coing=utf-8
'''
Created on 18.08.2011

@author: kaa
'''

import unittest, sys, logging, os
from PyQt4.QtSql import QSqlDatabase 
from dpframe.base.inits import default_log_init, json_config_init, db_connection_init
from dpframe.base.inits import DBConnParmsNotFoundError
from dpframe.tech.AttrDict import AttrDict


@default_log_init
class App1(object):
    pass

class TestDefaultLogInit(unittest.TestCase):

    def setUp(self):
        self.app = App1()

    def testLogExists(self):
        self.assertIn(u'log', self.app.env)

    def testLogType(self):
        self.assertIs(self.app.env.log, logging)


oldargv = sys.argv
sys.argv = [u'program', u'--config', u'./examples/gui/mainwnd/config.json']
@json_config_init
class App2(object):
    pass
sys.argv = oldargv

class TestJsonConfigInitCmd(unittest.TestCase):
    
    def setUp(self):
        self.app = App2()
        pass
    
    def testConfigExists(self):
        self.assertIn(u'config', self.app.env)

    def testConfigType(self):
        self.assertIsInstance(self.app.env.config, dict)

    def testConfigMatch(self):
        cfg = AttrDict({
            u'db': AttrDict({
                u'host': u'localhost',
                u'database': u'dpframe',
                u'user': u'dpframe',
                u'password': u'dpframe',
            })
        })
        self.assertDictEqual(self.app.env.config, cfg)


oldcurdir = os.path.abspath(os.curdir)
os.chdir(os.path.abspath(u'./examples/gui/mainwnd'))
@json_config_init
class App3(object):
    pass
os.chdir(oldcurdir)

class TestJsonConfigInitCurDir(TestJsonConfigInitCmd):

    def setUp(self):
        self.app = App3()
        pass


@json_config_init
class App4(object):
    pass

class TestJsonConfigInitDefault(unittest.TestCase):
    
    def setUp(self):
        self.app = App4()
        pass
    
    def testConfigFileNotExists(self):
        self.assertEqual(self.app.env.config, AttrDict())


class TestDBInitFailes(unittest.TestCase):
    
    def testFailed(self):
        try:
            @db_connection_init
            class DBApp(object):
                pass
        except DBConnParmsNotFoundError:
            self.assertTrue(True)

oldargv = sys.argv
sys.argv = [u'program', u'--host', u'localhost', u'--database', u'dpframe', u'--user', u'dpframe', u'--password', u'dpframe']
@db_connection_init
class DBArgvApp(object):
    pass
sys.argv = oldargv

class TestDBInitCmdParams(unittest.TestCase):
    
    def setUp(self):
        self.app = DBArgvApp()
        pass

    def testDBExists(self):
        self.assertIn(u'db', self.app.env)
        self.assertIsInstance(self.app.env.db, QSqlDatabase)
        self.assertEqual(unicode(self.app.env.db.hostName()), u'localhost')
        self.assertEqual(unicode(self.app.env.db.databaseName()), u'dpframe')
        self.assertEqual(unicode(self.app.env.db.userName()), u'dpframe')
        self.assertEqual(unicode(self.app.env.db.password()), u'dpframe')
        self.assertTrue(self.app.env.db.isOpen())


oldargv = sys.argv
sys.argv = [u'program', u'--config', u'./examples/gui/mainwnd/config.json']
@db_connection_init
@json_config_init
class DBCfgApp(object):
    pass
sys.argv = oldargv

class TestDBInitConfig(TestDBInitCmdParams):
    
    def setUp(self):
        self.app = DBCfgApp()
        pass


oldargv = sys.argv
sys.argv = [u'program', u'--config', u'./examples/gui/mainwnd/config.json']
@db_connection_init
class DBSelfCfgApp(object):
    pass
sys.argv = oldargv

class TestDBInitSelfConfig(TestDBInitCmdParams):
    
    def setUp(self):
        self.app = DBSelfCfgApp()
        pass


oldcurdir = os.path.abspath(os.curdir)
os.chdir(os.path.abspath(u'./examples/gui/mainwnd'))
@db_connection_init
@json_config_init
class DBCfgDefaultApp(object):
    pass
os.chdir(oldcurdir)

class TestDBCfgDefault(TestDBInitCmdParams):
    
    def setUp(self):
        self.app = DBCfgDefaultApp()
        pass


oldcurdir = os.path.abspath(os.curdir)
os.chdir(os.path.abspath(u'./examples/gui/mainwnd'))
@db_connection_init
@json_config_init
class DBDefaultApp(object):
    pass
os.chdir(oldcurdir)

class TestDBDefault(TestDBInitCmdParams):
    
    def setUp(self):
        self.app = DBDefaultApp()
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()