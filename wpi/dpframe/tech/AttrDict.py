#coding=utf-8
u'''
Created on 07.08.2011

@author: kaa
'''

import collections
from dpframe.tech.typecheck import *

class AttrDict(dict):
    u'''
    Словарь с атрибутным стилем доступа.
    Пример использования: dpframe.unittest.testattrdct.TestAttrdct
    
    '''
    
    @staticmethod
    # @takes(dict_of(str, anything))
    @returns('AttrDict')
    def toAttrDict(dct):
        for k, v in dct.items():
            if isinstance(v, collections.Mapping):
                dct[k] = AttrDict.toAttrDict(v)
        return AttrDict(dct)
    
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return u'{0}({1})'.format(self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        return super(AttrDict, self).__getitem__(key)

    def __delitem__(self, key):
        return super(AttrDict, self).__delitem__(key)
    
    def __getattr__(self, name):
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        return self.__setitem__(name, value)
