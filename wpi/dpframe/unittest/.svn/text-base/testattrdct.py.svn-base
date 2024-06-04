#coding=utf-8
'''
Created on 07.08.2011

@author: kaa
'''

import unittest
import collections
from dpframe.tech.AttrDict import AttrDict

class TestAttrdct(unittest.TestCase):

    def testAccess(self):
        o = AttrDict(c=u'qwerty')
        o[u'a'] = 1
        o.b = 2
        self.assertEqual(o.a, o[u'a'])
        self.assertEqual(o.b, o[u'b'])
        self.assertEqual(o.c, u'qwerty')
        
    def testGet(self):
        o = AttrDict()
        o.a = 1
        o.get = 2
        self.assertIsInstance(o.get, collections.Callable)
        self.assertEqual(o.get(u'a'), o[u'a'])
        self.assertEqual(o.get(u'get'), o[u'get'])
        
    def testNonExisting(self):
        o = AttrDict()
        self.assertRaises(KeyError, lambda: o.a)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()