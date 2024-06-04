#coding=utf-8
u"""
Created on 09.08.2011

@author: kaa
"""

class EnvNotExistsError(AttributeError):
    u"""
    Исключение: Класс не содержит объекта окружения env
    """
    
class NotExistsRequiredPartError(ValueError):
    u"""
    Исключение: Объект окружения env не содержит заявленного раздела
    """

def _check_env(*parts):
    u"""
    Служебный декоратор конструктора приложения.
    Проверяет существование обьекта приложения и наличие заявленных разделов.
    """
    
    def wrapper(f):
        def tmp(*args, **kwargs):
            f(*args, **kwargs)
            
            try:
                env = args[0].env
            except AttributeError:
                raise EnvNotExistsError()
            
            for part in parts:
                if part not in env:
                    raise NotExistsRequiredPartError(u'{0}'.format(part))
                
        return tmp
    return wrapper


def checkenv(*parts):
    u"""
    Декоратор класса приложения.
    Добавляет проверку наличия объекта self.env и соответствие его компонентов переданным параметрам.
    """
    
    def wrapper(cls):
        
        
        cls.__init__ = _check_env(*parts)(cls.__init__)
        return cls
    
    return wrapper

