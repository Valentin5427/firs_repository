#!/usr/bin/env python
#coding=utf-8

from dpframe.gui.commonapp import CommonApp

class MainWndHandler(object):

    def calculate(self):
        u'''Обработчик нажатия кнопки btnCalc.
        Провека корректности параметров и вычисление результата.'''
        
        try:
            p1 = float(self.ui.edParam1.text())
        except ValueError, e:
            self.ui.edResult.setText(u'Invalid parameter #1: {0}'.format(str(e)))
            return

        try:
            p2 = float(self.ui.edParam2.text())
        except ValueError, e:
            self.ui.edResult.setText(u'Invalid parameter #2: {0}'.format(str(e)))
            return

        op = self.ui.cbOperation.currentText()
        if u'+' == op:
            res = p1 + p2
        elif u'-' == op:
            res = p1 - p2
        elif u'*' == op:
            res = p1 * p2
        elif u'/' == op:
            try:
                res = p1 / p2
            except ZeroDivisionError:
                self.ui.edResult.setText(u'Division by zero')
                return
        
        self.ui.edResult.setText(str(res))


if __name__ == u'__main__':
    app = CommonApp(u'arithmetic.ui', [MainWndHandler], False)
    app.exec_()
