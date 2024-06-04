# -*- coding: UTF-8 -*-work
#
'''
Created on 20.03.2018

@author: atol
'''

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import  QIcon, QFont
from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue, msgBox
import win32print        
import json
import sys
import glob
import serial
import os
from electrolab.gui import  JournalMsr
from electrolab.gui.msgbox import getTrue, msgBox


def testConfig():
    try:
        f = open('config.json','r')
        data = json.load(f)
        try:
            knt05_port = data['devices']['knt05']['port']
        except Exception:
            return u'Неопределен порт для "knt05" в файле config.json!'

        try:
            scanner_port = data['devices']['scanner']
        except Exception:
            return u'Неопределен порт для "scanner" в файле config.json!'

        try:
            pr200_port = data['devices']['pr200']['port']
        except Exception:
            return u'Неопределен порт для "pr200" в файле config.json!'


        # Проверяем, присутствуют ли скорости передаче в файле config.json            
        try:
            baudrate1 = data['ports'][knt05_port]['baudrate']                
        except Exception:
            return u'Неопределена скорость передачи для порта "' + knt05_port + '" (knt05)!\nЗапускаем конфигурацию для исправления ошибки.'
        try:
            baudrate2 = data['ports'][scanner_port]['baudrate']
        except Exception:
            return u'Неопределена скорость передачи для порта "' + scanner_port + '" (scanner)!\nЗапускаем конфигурацию для исправления ошибки.'
                
        return ""
    except Exception:
        return u'Ошибка чтения config.json!\nЗапускаем конфигурацию для исправления ошибки.'


class Config(QDialog):
    def __init__(self):
        QWidget.__init__(self)

        from dpframe.base.envapp import checkenv
        from dpframe.base.inits import json_config_init
        from dpframe.base.inits import default_log_init
        from electrolab.gui.inits import serial_devices_init
        from dpframe.base.inits import db_connection_init
        @json_config_init
        @db_connection_init
        class ForEnv(QWidget):
            def getEnv(self):
                return self.env
        objEnv = ForEnv()
        env = objEnv.getEnv()
        
        db = env.db
        path_ui = env.config.paths.ui + "/"

        if not os.path.exists(path_ui):        
            path_ui = ""
        print("path_ui=", path_ui)
        if not JournalMsr.MyLoadUi(path_ui, "config.ui", self):
            self.is_show = False
            return

        import win32com.client

        self.pushButton_3.setVisible(False)
        self.groupBox_5.setVisible(False)
        self.spinBox_5.setVisible(False)

        # Считываем локальные принтеры в системе        
        try:
            sw = False   #####УБРАТЬ
            for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None,1)):
                self.comboBox.addItem(pName)
                self.comboBox_2.addItem(pName)
        except:
            print('Could not get local printers list.')
            
        # Считываем сетевые принтеры в системе        
        try:
            for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS,None,1)):
                self.comboBox.addItem(pName)
                self.comboBox_2.addItem(pName)
        except:
            print('Could not get network printers list.')


        s = 'nkjnKJNkjnkk'

        self.read_config()
                
        self.pushButton.setIcon(QIcon(u':/ico/ico/tick_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/delete_64.png'))

        self.comboBox.currentIndexChanged.connect(self.comboBox_indexChange)
        self.comboBox_2.currentIndexChanged.connect(self.comboBox_indexChange)
        self.checkBox.clicked.connect(self.comboBox_indexChange)
        self.checkBox_2.clicked.connect(self.comboBox_indexChange)
        self.lineEdit.textChanged.connect(self.comboBox_indexChange)
        self.lineEdit_2.textChanged.connect(self.comboBox_indexChange)
        self.lineEdit_3.textChanged.connect(self.comboBox_indexChange)
        self.spinBox_3.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_4.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_6.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_7.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_8.valueChanged.connect(self.comboBox_indexChange)


        self.checkBox_3.clicked.connect(self.checkBox_3_clicked)
        self.checkBox_4.clicked.connect(self.checkBox_4_clicked)
        self.checkBox_5.clicked.connect(self.checkBox_5_clicked)


        self.spinBox_9.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_10.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_11.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_12.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_13.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_14.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_15.valueChanged.connect(self.comboBox_indexChange)
        self.spinBox_16.valueChanged.connect(self.comboBox_indexChange)
                
        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton_2_Click)
        self.pushButton_3.clicked.connect(self.pushButton_3_Click)        
        
        self.checkBox_3_clicked()        
        self.checkBox_4_clicked()        
        self.checkBox_5_clicked()        
        self.pushButton.setEnabled(False)
        
                
    def checkBox_3_clicked(self):
        self.pushButton.setEnabled(True)        
        self.spinBox_9.setEnabled(self.checkBox_3.isChecked())
        self.spinBox_11.setEnabled(self.checkBox_3.isChecked())
        pass    
        
    def checkBox_4_clicked(self):
        self.pushButton.setEnabled(True)
        self.spinBox_10.setEnabled(self.checkBox_4.isChecked())
        self.spinBox_12.setEnabled(self.checkBox_4.isChecked())
        pass    
        
    def checkBox_5_clicked(self):
        self.pushButton.setEnabled(True)
        self.spinBox_15.setEnabled(self.checkBox_5.isChecked())
        self.spinBox_16.setEnabled(self.checkBox_5.isChecked())        
        self.checkBox_3.setEnabled(not self.checkBox_5.isChecked())
        self.checkBox_4.setEnabled(not self.checkBox_5.isChecked())
        if self.checkBox_5.isChecked():
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
        self.checkBox_3_clicked()
        self.checkBox_4_clicked()
        pass    
        
    def read_config(self):
        # Чтение параметров с config.json файла, если таковой имеется
        try:
            f = open('config.json','r')
            self.data = json.load(f)
            print(self.data)
            
            # Проверяем, присутствуют ли принтеры из файла config.json среди списка принтеров прикрепленных к компьютеру            
            try:
                report = self.data['printers']['report']
            except Exception:
                report = ''
            try:
                sticker = self.data['printers']['sticker']
            except Exception:
                sticker = ''

            for i in range(self.comboBox.count()):
                if self.comboBox.itemText(i) == report:
                   self.comboBox.setCurrentIndex(i)
                   i = -1
                   break
            if i != -1:
                self.pushButton.setEnabled(True)
                if report == '':
                    QMessageBox.warning(None, u"Предупреждение", u"Информация о принтере для печати отчетов отсутствует!'", QMessageBox.Ok)
                else:
                    QMessageBox.warning(None, u"Предупреждение", u"Принтер для печати отчетов: '" + self.data['printers']['report'] + u"'\nотсутствует среди прикрепленных к данному компьютеру принтеров!" , QMessageBox.Ok)

            for i in range(self.comboBox_2.count()):
                if self.comboBox_2.itemText(i) == sticker:
                   self.comboBox_2.setCurrentIndex(i)
                   i = -1
                   break
            if i != -1:
                self.pushButton.setEnabled(True)
                if sticker == '':
                    QMessageBox.warning(None, u"Предупреждение", u"Информация о принтере для печати этикеток отсутствует!'", QMessageBox.Ok)
                else:    
                    QMessageBox.warning(None, u"Предупреждение", u"Принтер для печати этикеток: '" + self.data['printers']['sticker'] + u"'\nотсутствует среди прикрепленных к данному компьютеру принтеров!" , QMessageBox.Ok)
                    

            # Проверяем, присутствуют ли com-порты из файла config.json среди списка активных com портов
            try:
                knt05_port = self.data['devices']['knt05']['port']
                self.spinBox_6.setValue(int(knt05_port[3:]))            
            except Exception:
                knt05_port = ''


            try:
                scanner_port = self.data['devices']['scanner']
                self.spinBox_7.setValue(int(scanner_port[3:]))            
            except Exception:
                scanner_port = ''

            try:
                chp02m_port = self.data['devices']['chp02m']['port']
                self.spinBox_8.setValue(int(chp02m_port[3:]))            
            except Exception:
                chp02m_port = ''

            try:
                ca5020_port = self.data['devices']['ca5020']['port']
                self.checkBox_5.setChecked(self.data['devices']['ca5020']['active'])
                self.spinBox_15.setValue(int(ca5020_port[3:]))            
                self.spinBox_16.setValue(int(self.data['devices']['ca5020']['address']))            
            except Exception:
                ca5020_port = ''

            try:
                ca5018_1_port = self.data['devices']['ca5018_1']['port']
                self.checkBox_3.setChecked(self.data['devices']['ca5018_1']['active'])
                self.spinBox_9.setValue(int(ca5018_1_port[3:]))            
                self.spinBox_11.setValue(int(self.data['devices']['ca5018_1']['address']))            
            except Exception:
                ca5018_1_port = ''

            try:
                ca5018_2_port = self.data['devices']['ca5018_2']['port']
                self.checkBox_4.setChecked(self.data['devices']['ca5018_2']['active'])
                self.spinBox_10.setValue(int(ca5018_2_port[3:]))            
                self.spinBox_12.setValue(int(self.data['devices']['ca5018_2']['address']))            
            except Exception:
                ca5018_2_port = ''

            try:
                pr200_port = self.data['devices']['pr200']['port']
                self.spinBox_13.setValue(int(pr200_port[3:]))            
                self.spinBox_14.setValue(int(self.data['devices']['pr200']['address']))            
            except Exception:
                pr200_port = ''


                
            # Проверяем, присутствуют ли скорости передаче в файле config.json            
            try:
                baudrate1 = self.data['ports'][knt05_port]['baudrate']                
            except Exception:
                baudrate1 = 0
            try:
                baudrate2 = self.data['ports'][scanner_port]['baudrate']
            except Exception:
                baudrate2 = 0
            self.spinBox_3.setValue(baudrate1)
            self.spinBox_4.setValue(baudrate2)

            # Проверяем, присутствуют ли данные по соединению с БД в файле config.json            
            try:
                host = self.data['db']['host']
            except Exception:
                host = ''
            try:
                database = self.data['db']['database']
            except Exception:
                database = ''
            try:
                user = self.data['db']['user']
            except Exception:
                user = ''
                
            self.lineEdit.setText(host)
            self.lineEdit_2.setText(database)
            self.lineEdit_3.setText(user)
            

            # Проверяем, присутствуют ли данные параметров окна в файле config.json            
            try:
                fullscreen = self.data['winparam']['fullscreen']
            except Exception:
                fullscreen = None
                
            try:
                nomouse = self.data['winparam']['nomouse']
            except Exception:
                nomouse = None
                
            self.checkBox.setChecked(fullscreen)
            self.checkBox_2.setChecked(not nomouse)
                                
                                    
        except Exception:
            print(u'Ошибка чтения config.json!')
            QMessageBox.warning(None, u"Предупреждение", u"Ошибка чтения config.json!", QMessageBox.Ok)
            self.data = {}


    def write_json(self):
        # ЗАПИСАТЬ
        f = open('config.json','w')                
        try:
            del self.data['printers']
        except Exception:
            pass
        self.data['printers']= {"report": str(self.comboBox.currentText()),"sticker": str(self.comboBox_2.currentText())}

        knt05 = {"port":self.port1}
        scanner = self.port2
        chp02m = {"port":self.port3, "ammeter":{"address":str(self.spinBox.value())}, "voltmeter":{"address":str(self.spinBox_2.value())}}
        ca5020 = {"port":self.port7, "address":self.spinBox_16.value(), "active": self.checkBox_5.isChecked()}
        ca5018_1 = {"port":self.port4, "address":self.spinBox_11.value(), "active": self.checkBox_3.isChecked()}
        ca5018_2 = {"port":self.port5, "address":self.spinBox_12.value(), "active": self.checkBox_4.isChecked()}
        pr200 = {"port":self.port6, "address":self.spinBox_14.value()}

#        self.data['devices']= {"knt05": knt05, "scanner": scanner, "chp02m": chp02m, "ca5018_1": ca5018_1, "ca5018_2": ca5018_2, "pr200": pr200}
        self.data['devices']= {"knt05": knt05, "scanner": scanner, "chp02m": chp02m, "ca5020": ca5020, "ca5018_1": ca5018_1, "ca5018_2": ca5018_2, "pr200": pr200}

        self.data['ports']= {self.port1: {"baudrate": self.spinBox_3.value()},
                             self.port2: {"baudrate": self.spinBox_4.value()}}
        
        self.data['db']= {"host": str(self.lineEdit.text()),
                          "database": str(self.lineEdit_2.text()), 
                          "user": str(self.lineEdit_3.text()), 
                          "password": self.data['db']['password']}

        self.data['winparam']= {"fullscreen": self.checkBox.isChecked(),"nomouse": not self.checkBox_2.isChecked()}
                      
        json.dump(self.data, f, indent=4, sort_keys=False)
        

    def comboBox_indexChange(self):
        self.pushButton.setEnabled(True)

    def pushButton_Click(self):
        self.port1 = "COM" + str(self.spinBox_6.value())
        self.port2 = "COM" + str(self.spinBox_7.value())
        self.port3 = "COM" + str(self.spinBox_8.value())
        self.port4 = "COM" + str(self.spinBox_9.value())
        self.port5 = "COM" + str(self.spinBox_10.value())
        self.port6 = "COM" + str(self.spinBox_13.value())
        self.port7 = "COM" + str(self.spinBox_15.value())
        '''
        if (self.port1 == self.port2) or (self.port1 == self.port3) or (self.port1 == self.port4) or (self.port1 == self.port5) or (self.port1 == self.port6) or \
           (self.port2 == self.port3) or (self.port2 == self.port4) or (self.port2 == self.port5) or (self.port2 == self.port6) or \
           (self.port3 == self.port4) or (self.port3 == self.port5) or (self.port3 == self.port6) or \
           (self.port4 == self.port5) or (self.port4 == self.port6) or \
           (self.port5 == self.port6):
        '''   
        if (self.port1 == self.port2) or (self.port1 == self.port3) or (self.port1 == self.port4) or (self.port1 == self.port5) or (self.port1 == self.port6) or (self.port1 == self.port7) or \
           (self.port2 == self.port3) or (self.port2 == self.port4) or (self.port2 == self.port5) or (self.port2 == self.port6) or (self.port2 == self.port7) or \
           (self.port3 == self.port4) or (self.port3 == self.port5) or (self.port3 == self.port6) or (self.port3 == self.port7) or \
           (self.port4 == self.port5) or (self.port4 == self.port6) or \
           (self.port5 == self.port6) or \
           (self.port6 == self.port7):
            QMessageBox.warning(None, u"Предупреждение", u"Все порты длжны быть разными!", QMessageBox.Ok)
            return
                                                              
        self.write_json()
        self.pushButton.setEnabled(False)

    def pushButton_2_Click(self):            
        if self.pushButton.isEnabled():
            if getTrue(self, u'Сохранить измененные настройки?'):
                self.pushButton_Click()        
        self.close()    

    def pushButton_3_Click(self):            
        ports = ["COM1", "COM2", "COM3"]
        for port in ports:
            self.comboBox_3.addItem(port)
            self.comboBox_4.addItem(port)
            self.comboBox_5.addItem(port)
        self.comboBox_4.setCurrentIndex(1)    
        self.comboBox_5.setCurrentIndex(2)    
        
        self.spinBox_3.setValue(4800)
        self.spinBox_4.setValue(57600)
                        
    def serial_ports(self):
        # Список активных com портов
        """ Lists serial port names    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except Exception:
                pass
        return result


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    wind = Config()
    wind.show()
    sys.exit(app.exec_())
