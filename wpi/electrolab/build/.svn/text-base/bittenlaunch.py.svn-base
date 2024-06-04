#!/usr/bin/env python

import subprocess, time

cmd = ['bitten-slave.exe',
          '--verbose',
          '--config=bitten.ini',
          '--log=bitten.log',
          'http://diposoft.ru/trac/ElectroLab/builds']


if cmd[0] not in subprocess.Popen('tasklist', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()[:]:
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)