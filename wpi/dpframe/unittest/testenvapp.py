#coding=utf-8
'''
Created on 09.08.2011

@author: dkasatsky
'''
import unittest
from dpframe.base import envapp
from dpframe.base.envapp import checkenv
from dpframe.base.inits import default_log_init
from dpframe.base.inits import json_config_init


@checkenv()
class TestApp(object):
    pass

@default_log_init
@checkenv()
class TestApp2(object):
    pass

@default_log_init
@checkenv(u'log')
class TestApp21(object):
    pass

@default_log_init
@checkenv(u'log', u'config')
class TestApp3(object):
    pass

@default_log_init
@json_config_init
@checkenv(u'log', u'config')
class TestApp4(object):
    pass

class TestEnvironmentDecorator(unittest.TestCase):

    def testDecoratedObject(self):
        self.assertRaises(envapp.EnvNotExistsError, lambda: TestApp())

    def testDecoratedEnvAppEmpty(self):
        self.assertIsNotNone(TestApp2())

    def testDecoratedEnvApp(self):
        self.assertRaises(envapp.NotExistsRequiredPartError, lambda: TestApp3())

    def testDecoratedValidApp(self):
        self.assertIsNotNone(TestApp4())

    def testDecoratedValidApp2(self):
        self.assertIsNotNone(TestApp21())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
