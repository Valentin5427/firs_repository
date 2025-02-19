#-*- coding: UTF-8 -*-
'''
Created on 16.01.2011
diposoft(c)
Description: Запустить как приложение
'''
import signal
import time
import os
import sys

class DPApplication:
    """Приложение"""
    def __init__(self):
        self.__bWork = True
        if os.name == "nt":
            import win32api
            win32api.SetConsoleCtrlHandler(self.SignalWinHandler, True)
#        except ImportError:
#            version = “.”.join(map(str, sys.version_info[:2]))
#            raise Exception(”pywin32 not installed for Python ” + version)
        else:
            signal.signal(signal.SIGINT , self.SignalLinHandler)
         
    def RunMainLoop(self):
        """Запуск главного цикла"""
        while(self.__bWork):
            #signal.pause()
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.__bWork
        sys.exit()
        
    def Stop(self):
        """Остановка главного цикла"""
        self.__bWork = False
        
    def SignalWinHandler(self, sig):
        """Обработчик прерывания из консоли"""
        # Номер сигнала sig не понятен, надо смотреть сигналы от SetConsoleCtrlHandler
        # print "User abort by ^C"
        self.Stop()
        
    def SignalLinHandler(self, sig, frame):
        """Обработчик прерывания из консоли"""
        if(sig == signal.SIGINT):
            print("User abort by ^C")
        #frame - точка программы где приехал ^C
        self.Stop()

from PyQt5.QtWidgets import QApplication

def get():
    return QApplication.instance() if QApplication.instance() else QApplication(sys.argv) 

if __name__ == "__main__":
    oApp = DPApplication()
    oApp.RunMainLoop()
