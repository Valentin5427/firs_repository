#!/usr/bin/env python
#coding=utf-8

def task1(env):
    env.log.info(u'Задача 1 выполняется.')
    env.log.debug(u'Levels {0}'.format([h.level for h in env.log.handlers]))
    
def task2(env):
    env.log.info(u'Задача 2 выполняется.')
    
def task3(env):
    env.log.info(u'Задача 3 выполняется.')
    
def task_empty(env):
    pass