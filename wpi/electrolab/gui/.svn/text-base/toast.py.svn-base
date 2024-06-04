#-*- coding: UTF-8 -*-
u"""
Created on 26.11.2012
@author: Anton
ticket #
Description: Тосты - всплывающие сообщения, пока сделана возможность выводить только текстовые сообщения в правом нижнем углу
Пример
oToast = ToastMessage()
oToast.ShowText(u'30 0001', 72)
"""

from PyQt4.QtGui import QWidget, QLabel, QGridLayout, QSizePolicy, QFont
from PyQt4.QtCore import Qt, QObject, QPropertyAnimation, pyqtSlot, QPoint
from PyQt4.QtGui import QApplication

left = 0
right = 1

class ToastWindows(QWidget):

    def __init__(self, _parent=None, _flags=Qt.Window | Qt.SplashScreen):
        super(QWidget, self).__init__(_parent, _flags)
        self.Layout = QGridLayout(self)
        self.Layout.setSizeConstraint(self.Layout.SetMinimumSize)
        

class ToastText(ToastWindows):
    
    def __init__(self, _parent=None, _text=None, _fontSize=None):
        ToastWindows.__init__(self, _parent)
        self.label = QLabel(_text, self)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
        if _fontSize:
            font = self.label.font()
            font.setPointSize(_fontSize)
            self.label.setFont(font)
        self.Layout.addWidget(self.label)
        
class ToastMessage(QObject):
    
    def __init__(self, _parent=None, _timeLife=5000, _opacity=1, _queueSize=5):
        super(QObject, self).__init__()
        self.parent = _parent
        self.opacity = _opacity
        self.timeLife = _timeLife
        self.queue = []
    
    def get_start_point(self):
        return QApplication.desktop().screenGeometry().bottomRight()
        
        
    @pyqtSlot()
    def close_and_delete(self):
        sender = self.sender()
        item = 0
        for widget, opaciti, geometry in self.queue:
            if sender == opaciti: 
                self.queue.pop(item)
                widget.close()
            item += 1
                
    def mov_up(self, _step):
        shift = len(self.queue) * _step
        for widget, opaciti, geometry in self.queue:
            geometry.setDuration(300)
            position = widget.pos()
            geometry.setStartValue(position)
            
            position.setY(self.get_start_point().y() - shift)
            geometry.setEndValue(position)
            geometry.start()
            shift -= _step

    def ShowText(self, _text, _fontSize=None):
        toastText = ToastText(self.parent, _text, _fontSize)
        opacity = QPropertyAnimation(toastText, u'windowOpacity')
        opacity.finished.connect(self.close_and_delete)
        
        opacity.setDuration(self.timeLife)
        opacity.setStartValue(self.opacity)
        opacity.setEndValue(0.0)

        toastText.move(self.get_start_point())
        toastText.show()
        step = toastText.geometry().height()
        point = self.get_start_point()
        point.setX(self.get_start_point().x() - toastText.geometry().width() )
        
        toastText.move(point)
        
        opacity.start()
        self.queue.append([toastText, opacity, QPropertyAnimation(toastText, u'pos')]) 
        self.mov_up(step)
        

if u'__main__' == __name__:
    import sys

    app = QApplication(sys.argv)

    oToast = ToastMessage()
    oToast.ShowText(u'11', 72)
    oToast.ShowText(u'30099', 72)
    oToast.ShowText(u'51', 72)
    exitRes = app.exec_()
    sys.exit(exitRes)
