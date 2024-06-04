#-*- coding: UTF-8 -*-
'''
Created on 07.03.2011
diposoft(c)
@author: knur
Description: 
'''
import serial
import threading
import time
import re
#from PyQt4.QtCore import QObject
import logging
import string
import datetime
import electrolab.tech.logger as log

# шаманим, чтобы определить русский разделитель дробной части
import locale
locale.setlocale(locale.LC_ALL, '')
dec_sep = locale.localeconv()['decimal_point']
locale.setlocale(locale.LC_ALL, (None,None))
del locale

logtmp = logging.getLogger(u'config_device')
formatter = logging.Formatter(u'%(message)s', u'%Y-%m-%d %H:%M:%S')
logtmp.setLevel(logging.INFO)
hdlr = None

def setHdlr(_IsCont):
    global hdlr
    global logtmp
    try:
        if not _IsCont:
            if hdlr != None:
                hdlr.flush()
                hdlr.close()
                logtmp.removeHandler(hdlr)
                hdlr = None
            return False
        if _IsCont and hdlr != None:
            return True
        # имя файла
        hdlr = logging.FileHandler(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S-%f') + u'.csv')
        hdlr.setFormatter(formatter)
        logtmp.addHandler(hdlr)
        return True
    except:
        if hdlr != None:
            hdlr.flush()
            hdlr.close()
            logtmp.removeHandler(hdlr)
        return False

class SerialPortEmulator():
    '''Эмулирует ввод данных через '''
#    def __init__(self, port = 0, baudrate = 4800, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE):
    def __init__(self, _sEndLine = None, fileName = None):
        '''
        Входные параметры:
        * port – Device name or port number number or None.
        * baudrate – Baud rate such as 9600 or 115200 etc.
        * bytesize – Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
        * parity – Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        * stopbits – Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
        '''
        self.thread = None
        try:
            self.serial = open(fileName,"r")#.readlines()
            self.serial.seek(0)
            self.serial
            
            self.bAccesibly = True
        except:
            self.bAccesibly = False
        self.sEndLine = _sEndLine
        
    def SetHandler(self, handler):
        '''Установить обработчик сообщений, handler - ссылка'''
        self.handler = handler

    def Disable(self):
        if(not self.bAccesibly or not self.thread):
            self.serial.seek(0)
            return
        self.thread.Stop()
#        del self.thread
        self.serial.seek(0)

    def Enable(self):
        if(not self.bAccesibly):
            return
#        self.serial.open()
        self.thread = self.HandlerThread()
        self.thread.start(self.serial, self.handler, self.sEndLine)

    def SetEnabled(self, bEnabled):
        '''Включение/выключение сканера'''
        if(not self.bAccesibly):
            return False
        if(bEnabled):
            self.Enable()
            return True
        else:
            self.Disable()
            return False
        
    class HandlerThread(threading.Thread):
        ''' Класс потока эмуляции потока данных'''
        def __init__(self):
            self.serial = None 
            self.handler = None
            threading.Thread.__init__(self)

        def Stop(self):
            self.rRun = False
            
        def run(self):
            res = ''
            while(self.rRun):
#                time.sleep(0.01)
                try:
                    res += self.serial.readline()
                except:
                    pass
                if(None == self.sEndLine or self.sEndLine in res):
                    self.handler(res)
                    res = ''
                    time.sleep(0.5)

        def start(self, serial, handler, _sEndLine = None):
            self.sEndLine = _sEndLine
            self.serial = serial 
            self.handler = handler
            self.rRun = True
            threading.Thread.start(self)


class SerialPortReader():
    '''Читет последовательный порт'''
#    def __init__(self, port = 0, baudrate = 4800, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE):
    def __init__(self, _device, _sEndLine = None):
        '''
        Входные параметры:
        * _device – Девайс serial
        '''
        self.sEndLine = _sEndLine
        self.thread = None
        try:
            self.serial = _device
            self.serial.close()
            self.bAccesibly = True
        except:
            self.bAccesibly = False

    def SetHandler(self, handler):
        '''Установить обработчик сообщений, handler - ссылка'''
        self.handler = handler

    def Disable(self):
        if(not self.bAccesibly or not self.thread):
            return
        self.thread.Stop()
        del self.thread
        self.thread = None
        self.serial.close()

    def Enable(self):
        if(not self.bAccesibly):
            return
        self.serial.open()
        self.thread = self.HandlerThread()
        self.thread.start(self.serial, self.handler, self.sEndLine)

    def SetEnabled(self, bEnabled):
        '''Включение/выключение сканера'''
        if(not self.bAccesibly):
            return
        if(bEnabled):
            if(self.serial.isOpen()):
                return True
            self.Enable()
            return True
        else:
            self.Disable()
            return False

    class HandlerThread(threading.Thread):
        ''' Класс потока обработки сообщений от сканера'''
        def __init__(self):
            self.serial = None 
            self.handler = None
            threading.Thread.__init__(self)

        def Stop(self):
            self.rRun = False
            
        def run(self):
            res = ''
            while(self.rRun):
#TODO:Задержка нужна для USB сканера, похоже она гадит для КНТ                time.sleep(0.1)
                try:
#                    self.handler(self.serial.readline(1, self.sEndLine))
                    res += self.serial.readline()
                except:
                    pass
                if len(res) > 0 and (None == self.sEndLine or self.sEndLine in res):
                    self.handler(res)
                    res = ''
            
        def start(self, serial, handler, _sEndLine = None):
            self.sEndLine = _sEndLine
            self.serial = serial 
            self.handler = handler
            self.rRun = True
            threading.Thread.start(self)
            

class BarCodeScannerRS232(SerialPortReader):
    '''"Драйвер" сканера штрих-кодов'''
    def __init__(self, _device, _sEndLine = '\r\n'):
        SerialPortReader.__init__(self, _device, _sEndLine)
        
    def SetHandler(self, handler):
        '''Подключение обработчика штрих-кодов, handler - "callback" функция'''
        self.Parser = handler
        SerialPortReader.SetHandler(self, self.BarCodeParser)
        
    def BarCodeParser(self, sBarCode):
        '''Парсер, удаляет лишние символы'''
        if(str == type(sBarCode)):
            self.Parser(sBarCode.strip())

class KNT05DataPackage(object):
    '''
    Структура пакета сообщения для КНТ-05, который делают где-то в далёкой суровой сибири
    
    TT - Поверка трансформаторов тока
        A: амплитудная ошибка поверяемого трансформатора тока (идентификатор A, двоеточие, пробел, значение ошибки со знаком, пробел, символ размерности ‘%’);
        P: угловая ошибка поверяемого трансформатора тока (идентификатор P, двоеточие, пробел, значение ошибки со знаком, пробел, символ размерности ‘'’);
        I: вторичный ток образцового трансформатора (идентификатор ‘I’,двоеточие, два пробела, значение вторичного тока, пробел, размерность ‘%’ или ‘A’);
        N: номинальный вторичный ток образцового и поверяемого трансформатора (идентификатор ‘N’, двоеточие, два пробела, номинальное значение 1A, 5A или 5A/1A, когда номинальный вторичный ток образцового трансформатора составляет пять ампер, а поверяемого – один ампер);
        F: частота вторичного тока образцового трансформатора (идентификатор ‘F’, двоеточие, два пробела, значение частоты, пробел, размерность ‘Hz’);
        K: коэффициент несинусоидальности вторичного тока образцового трансформатора(идентификатор ‘K’, двоеточие, два пробела, значение коэффициента, пробел, размерность ‘%’);
    TS - Измерение полной мощности и коэффициента мощности нагрузки вторичной обмотки поверяемого трансформатора тока
    TR - Измерение активного и реактивного сопротивления нагрузки вторичной обмотки поверяемого трансформатора тока
    TZ - Измерение полного сопротивления и коэффициента мощности нагрузки вторичной обмотки поверяемого трансформатора тока
    NT - Поверка трансформаторов напряжения
    NS - Измерение полной мощности и коэффициента мощности нагрузки вторичной обмотки поверяемого трансформатора напряжения
    NG - Измерение активной и реактивной проводимости нагрузки вторичной обмотки поверяемого трансформатора напряжения
    NY - Измерение полного проводимости и коэффициента мощности нагрузки вторичной обмотки поверяемого трансформатора
    
    '''
    def __init__(self, sData):
        object.__init__(self)
        bDumpCSV = False
        if(0 == len(sData)):
            self.bParsed = False
            self.type = None
            self.A = None
            self.P = None
            self.I = None
            self.N = None
            self.F = None
            self.K = None
            return
        else:
            self.bParsed = True
        list = sData.split('\n')
        self.type = list[0][1:3]
        self.A = self.extract_data(list[1][3:11])
        self.P = self.extract_data(list[2][3:11])
        self.I = self.extract_data(list[3][3:11])
        self.N = self.extract_data(list[4][3:11])
        self.F = self.extract_data(list[5][3:11])
        self.K = self.extract_data(list[6][3:11])
        
        if not bDumpCSV:
            return
        
        tmpI = self.convert_str(self.I)
        tmpB = tmpI >= 0.7 and tmpI <= 120.1 and self.type == u'TT'
        log.info(u'Dump: <' + sData + u'> isLogged: ' + str(tmpB))
        if (setHdlr(tmpB)):
            # заменяем . на , специально для экселя, чтобы он понимал локализованный формат дробных чисел
            logtmp.info(str(self.convert_str(self.A)).replace(u'.', dec_sep)
                     + u';' + str(self.convert_str(self.P)).replace(u'.', dec_sep)
                     + u';' + str(self.convert_str(self.I)).replace(u'.', dec_sep)
                     + u';' + str(self.convert_str(self.N)).replace(u'.', dec_sep)
                     + u';' + str(self.convert_str(self.F)).replace(u'.', dec_sep)
                     + u';' + str(self.convert_str(self.K)).replace(u'.', dec_sep)
                     )

    def convert_str(self, _str):
        try:
            res = float(_str.strip(u' %`').strip(string.letters))
        except:
            res = float(0)
        return res

    def extract_data(self, _sData):
        try:
            sData = re.sub(u'''['`%\sAHz]''', u'', _sData).strip()
            if sData:
                return float(sData)
            else:
                return None
        except:
            res = float(0)
        return res

class KNT05(SerialPortReader):
    '''"Драйвер" измерительного прибора КНТ-05, делают где-то в далёкой суровой сибири'''
    
    def __init__(self, _oSerial):
        SerialPortReader.__init__(self, _oSerial, '')
        
    def SetHandler(self, handler):
        '''Подключение обработчика , handler - "callback" функция'''
        self.Parser = handler
        SerialPortReader.SetHandler(self, self.DataParser)
        
    def DataParser(self, sData):
        '''Парсер, удаляет лишние символы'''
        val = KNT05DataPackage(sData)
        self.Parser(val)
        

class KNT05_forTest(SerialPortEmulator):
    '''"Эмулятор КНТ-05'''
    
#    def __init__(self, port = 0, baudrate = 4800, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, fileName = None):
    def __init__(self, fileName = None):
        SerialPortEmulator.__init__(self, '', fileName)
        
    def SetHandler(self, handler):
        '''Подключение обработчика , handler - "callback" функция'''
        self.Parser = handler
        SerialPortEmulator.SetHandler(self, self.DataParser)
        
    def DataParser(self, sData):
        '''Парсер, удаляет лишние символы'''
        val = KNT05DataPackage(sData)
        self.Parser(val)


