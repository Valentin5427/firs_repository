#-*- coding: UTF-8 -*-

'''
Created on 07.04.2012

@author: Anton
'''


#import pymodbus
#print 'ok'


from pymodbus.client.sync import ModbusSerialClient 

client = ModbusSerialClient(method='ascii', port='COM5', baudrate=9600)
result = client.write_coil(0, True, 16) #Установка реле 1 в сотсояние включено для устройства 16
result = client.write_coil(1, True, 16) #Установка реле 2 в сотсояние включено для устройства 16
client.close()
print 'ok'