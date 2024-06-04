#coding=utf-8

import abc
import sys

class IDaemon(object):
    u'''Кроссплатформенный интерфейс класса службы/демона.
    При реализации на других ОС, возможно подлежит переработке.
    
    '''
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _do(self):
        u'''Выполнить код службы.
        
        Параметры командной строки доступны в переменной self.args в виде кортежа строк.
        Первый элемент кортежа - имя службы.
        
        '''
    
    def _start(self):
        u'''Выполнить действия при старте службы.
        
        Параметры командной строки доступны в переменной self.args в виде кортежа строк.
        Первый элемент кортежа - имя службы.
        
        '''
    
    def _stop(self):
        u'''Выполнить действия при остановке службы.
        
        Параметры командной строки доступны в переменной self.args в виде кортежа строк.
        Первый элемент кортежа - имя службы.
        
        '''
    
    def _pause(self):
        u'''Выполнить действия при приостановке службы.
        
        Параметры командной строки доступны в переменной self.args в виде кортежа строк.
        Первый элемент кортежа - имя службы.
        
        '''
    
    def _resume(self):
        u'''Выполнить действия при возобновлении работы службы.
        
        Параметры командной строки доступны в переменной self.args в виде кортежа строк.
        Первый элемент кортежа - имя службы.
        
        '''

    @classmethod
    def Install(cls, startType = None, errorControl = None, runInteractive = False, userName = None, password = None):
        u'''Установить демона.'''

    @classmethod
    def Remove(cls):
        u'''Удалить службу.'''

    @classmethod
    def Start(cls, args=None, waitSecs=0):
        u'''Запустить службу.'''

    @classmethod
    def Stop(cls, waitSecs=0):
        u'''Остановить службу.'''

    @classmethod
    def Restart(cls, args=None, waitSecs=30):
        u'''Перезапустить службу.'''

    @classmethod
    def QueryServiceStatus(cls):
        u'''Запросить состояние службы'''
        
    @classmethod
    def Pause(cls):
        u'''Приостановить службу'''
        
    @classmethod
    def Continue(cls):
        u'''Возобновить службу'''


if u'win32' == sys.platform:

    import win32serviceutil
    import win32service
    import win32event
    import winerror
    import servicemanager
    import pywintypes
     
    class BaseDaemon(IDaemon, win32serviceutil.ServiceFramework):
        u'''Абстрактный базовый класс службы Windows.
    
        Для создания собственного класса службы необходимо унаследовать его от класса BaseDaemon.
        Затем нужно определить в классе службы три переменные:
        
        _svc_name_ = u'ServiceName'                          # имя службы
        _svc_display_name_ = u'Display Name of the Service'  # отображаемое имя службы
        _svc_description_ = u'Service Description'           # описание службы
        
        Можно также определить зависимости службы _svc_deps_
            
        Далее необходимо переопределить абстрактный метод _do,
        и, по необходимости, методы _star, _stop, _pause, _resume.
        Для вывода в EventLog в этих функциях необходимо экспортировать
        модуль servicemanager и использовать его функции.
        
        При переопределении конструктора необходимо вначале вызвать конструктор базового класса.
        В конструкторе можно переопределить таймауты:
        
        self.timeout = 5000         # пауза между выполнением основного цикла службы (мсек)
        self.resumeTimeout = 1000   # таймаут ожидания команды возобновления работы службы (мсек)
        
        Для управления службой в модуль, содержащий класс службы, добавить код:
        
        import win32serviceutil
        if __name__ == '__main__':
            win32serviceutil.HandleCommandLine(CustomService)
            
        где CustomService - класс службы.
        
        Для получения справки о параметрах управления службой
        нужно запустить модуль, содержащий класс службы, без параметров.
            
        Примеры служб:
        dpframe/examples/simpleservice.py
        dpframe/base/agentservice.py
        
        
        '''
        
        _svc_name_ = u''
        _svc_display_name_ = u''
        _svc_description_ = u''
    
        NOTINSTALLED = 0
        RUNNING = win32service.SERVICE_RUNNING
        STOPPED = win32service.SERVICE_STOPPED
        PAUSED = win32service.SERVICE_PAUSED
        START_PENDING = win32service.SERVICE_START_PENDING
        STOP_PENDING = win32service.SERVICE_STOP_PENDING
        CONTINUE_PENDING = win32service.SERVICE_CONTINUE_PENDING
        PAUSE_PENDING = win32service.SERVICE_PAUSE_PENDING
        
        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            self.hWaitResume = win32event.CreateEvent(None, 0, 0, None)
            self.timeout = 5000         # пауза между выполнением основного цикла службы (мсек)
            self.resumeTimeout = 1000   # таймаут ожидания команды возобновления работы службы (мсек)
            self._paused = False
            self.args = args
     
        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STOPPED,
                                  (self._svc_name_, u''))
           
        def SvcPause(self):
            self.ReportServiceStatus(win32service.SERVICE_PAUSE_PENDING)
            self._paused = True
            self.ReportServiceStatus(win32service.SERVICE_PAUSED)
            servicemanager.LogInfoMsg(u'The {0} service has paused.'.format(self._svc_name_))
       
        def SvcContinue(self):
            self.ReportServiceStatus(win32service.SERVICE_CONTINUE_PENDING)
            win32event.SetEvent(self.hWaitResume)
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg(u'The {0} service has resumed.'.format(self._svc_name_))
                   
     
        def SvcDoRun(self):
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_,''))
            self._main()  
        
    
        def _main(self):
            u'''Цикл жизни службы.'''
            
            #Здесь выполняем необходимые действия при старте службы
            self._start()
            while True:
                #Здесь должен находиться основной код сервиса
                self._do()
               
                #Проверяем не поступила ли команда завершения работы службы
                rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                if rc == win32event.WAIT_OBJECT_0:
                    #Здесь выполняем необходимые действия при остановке службы
                    self._stop()
                    break
     
                if self._paused:
                    #Здесь выполняем необходимые действия при приостановке службы
                    self._pause()
                #Приостановка работы службы                
                while self._paused:
                    #Проверям не поступила ли команда возобновления работы службы
                    rc = win32event.WaitForSingleObject(self.hWaitResume, self.resumeTimeout)
                    if rc == win32event.WAIT_OBJECT_0:
                        self._paused = False
                        #Здесь выполняем необходимые действия при возобновлении работы службы
                        self._resume()
                        break                  
     
        @staticmethod
        def _win32errstr(exc):
            return u'{0}({1})'.format(exc.strerror.decode(u'cp1251'), exc.winerror)
            
        @classmethod
        def Install(cls, startType = None, errorControl = None, runInteractive = False, userName = None, password = None):
            u'''Установить службу.
            
            Если служба уже установлена, обновляется ее конфигурация.
            
            Параметры:
            startType - тип запуска
                win32service.SERVICE_DEMAND_START - ручной (default)
                win32service.SERVICE_AUTO_START - автоматический
                win32service.SERVICE_DISABLED - отключен
            errorControl - контроль ошибок
                win32service.SERVICE_ERROR_CRITICAL
                win32service.SERVICE_ERROR_IGNORE
                win32service.SERVICE_ERROR_NORMAL (default)
                win32service.SERVICE_ERROR_SEVERE
            runInteractive - доступ к рабочему столу (bool, default False)
            userName - пользователь
            password - пароль
            
            '''
            bRunInteractive = 1 if runInteractive else 0
            try:
                win32serviceutil.InstallService(win32serviceutil.GetServiceClassString(cls), cls._svc_name_, cls._svc_display_name_,
                                                startType, errorControl, bRunInteractive, cls._svc_deps_, userName, password,
                                                cls._exe_name_, exeArgs=None, description=cls._svc_description_)
            except win32service.error, exc:
                if winerror.ERROR_SERVICE_EXISTS == exc.winerror:
                    try:
                        win32serviceutil.ChangeServiceConfig(win32serviceutil.GetServiceClassString(cls), cls._svc_name_, startType, errorControl,
                                                             bRunInteractive, cls._svc_deps_, userName, password, cls._exe_name_,
                                                             displayName=cls._svc_display_name_, description=cls._svc_description_)
                    except win32service.error, excupd:
                        return BaseDaemon._win32errstr(excupd)
                else:
                    return BaseDaemon._win32errstr(exc)
    
        @classmethod
        def Remove(cls):
            u'''Удалить службу.'''
            try:
                win32serviceutil.RemoveService(cls._svc_name_)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)
    
        @classmethod
        def Start(cls, args=None, waitSecs=0):
            u'''Запустить службу.
            
            Параметры:
            args - дополнительные параметры (кортеж строк)
            waitSecs - таймаут ожидания старта (сек)
            
            '''
            try:
                win32serviceutil.StartService(cls._svc_name_, args)
                if waitSecs:
                    win32serviceutil.WaitForServiceStatus(cls._svc_name_, win32service.SERVICE_RUNNING, waitSecs)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)
    
        @classmethod
        def Stop(cls, waitSecs=0):
            u'''Остановить службу.
            
            Параметры:
            waitSecs - таймаут ожидания остановки(сек)
            
            '''
            try:
                if waitSecs:
                    win32serviceutil.StopServiceWithDeps(cls._svc_name_, waitSecs = waitSecs)
                else:
                    win32serviceutil.StopService(cls._svc_name_)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)
    
        @classmethod
        def Restart(cls, args=None, waitSecs=2):
            u'''Перезапустить службу.
            
            Параметры:
            args - дополнительные параметры (кортеж строк)
            waitSecs - таймаут ожидания старта (сек)
            
            '''
            try:
                win32serviceutil.RestartService(cls._svc_name_, args, waitSecs)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)
    
    
        @classmethod
        def QueryServiceStatus(cls):
            u'''Запросить состояние службы'''
            
            try:
                state = win32serviceutil.QueryServiceStatus(cls._svc_name_)[1]
            except pywintypes.error:
                return cls.NOTINSTALLED
            return state
            
        @classmethod
        def Pause(cls):
            u'''Приостановить службу'''
            
            try:
                win32serviceutil.ControlService(cls._svc_name_, win32service.SERVICE_CONTROL_PAUSE)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)
            
        @classmethod
        def Continue(cls):
            u'''Возобновить службу'''
            
            try:
                win32serviceutil.ControlService(cls._svc_name_, win32service.SERVICE_CONTROL_CONTINUE)
            except win32service.error, exc:
                return BaseDaemon._win32errstr(exc)

else:
    class BaseDaemon(IDaemon):
        u'''Абстрактный базовый класс демона Linux.
        Не реализован, реализация по необходимости
        '''
    
