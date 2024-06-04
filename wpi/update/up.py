import datetime
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import  QKeyEvent, QIcon, QFont
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import updateUI
import sys
import os
import shutil
import datetime
from pathlib import Path

basedir = os.path.abspath(os.getcwd())
path = '\\'.join(basedir.split('\\'))
print(335, path)

class Config():
    def __init__(self):

        self.data = None
        self.check_file()
        self.read_config()


    def check_file(self):
        if  os.path.exists(path + '/update/config.json'):
            return True
        self.create_config()
        pass

    def read_config(self):
        try:
            with open(path + '/update/config.json', 'r') as file:
                self.data = json.load(file)

            pass
        except:
            self.create_config()
            self.read_config()


    def create_config(self):
        with open(path + '/update/config.json', 'w') as file:
            info = {'path':'\\\\10.5.0.16\\Laboratory\\!Документация по лаборатории\\Програмное обеспечение\\Отчет', }
            json.dump(info, file, indent=3)




class Update_Project(QDialog, updateUI.Ui_Dialog):
    signalError = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pix = QMovie(f"{path}\\update\\icons8.gif")
        self.pix1 = QMovie(f"{path}\\update\\icons9.gif")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pix.setScaledSize(QSize(80,80))
        self.pix1.setScaledSize(QSize(80, 80))
        self.label.setMovie(self.pix)
        self.pix.start()
        self.config = Config()
        QApplication.processEvents()
        self.tread = MyThread(self.config,self)
        self.tread.start()
        self.tread.mysignal.connect(self.end_update)
        self.tread.message_error.connect(self.show_error)


    def show_error(self,error):
        QMessageBox.warning(None, u"Ошибка", error, QMessageBox.Ok)




    def end_update(self):
        self.label_2.setText('Перезапустите программу')
        self.label_2.clicked.connect(self.open_project)
        self.label.setMovie(self.pix1)
        self.pix1.start()
        self.pix1.setSpeed(150)


    def open_project(self):
        os.system(f'start {path}\\wpi.exe')
        self.close()




class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal()
    message_error = QtCore.pyqtSignal(str)
    def __init__(self,config,objectUP):
        super().__init__()
        self.objectUP = objectUP
        self.congig = config
        self.objectUP.signalError.connect(self.stop_tread)

    def run(self):
        self.update_project()
        self.mysignal.emit()


    def update_project(self):
        try:
            path_full = sys.argv[1]
        except IndexError:
            self.message_error.emit(f"Не удалось найти обновление")
            return

        if os.path.exists(path_full):
            self.f_update(path_full)
            return
        self.message_error.emit(f"Не удалось найти файл по пути {path_full}!")
        return



    def f_update(self,path_full):
        self.delete_dir()
        import subprocess
        subprocess.call(f'xcopy "{path_full}" /E /Y ' + f"{path}", shell=True)
        return

    def delete_dir(self):
        for p in Path(path).iterdir():
            if str(p).count('update'):
                continue
            # print(56,p)
            if os.path.isdir(p):
                print(f'RMDIR /s /q {p}')
                os.system(f'RMDIR /s /q {p}')
            elif os.path.isfile(p):
                print(f'RD /s /q {p}')
                os.system(f'del /s /q {p}')



    def stop_tread(self):
        self.running = False




def excepthook(exc_type, exc_value, exc_tb):
    import traceback
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    QMessageBox.warning(None, u"Ошибка!!!!!", tb,QMessageBox.Ok)



if __name__ == '__main__':
    sys.excepthook = excepthook
    pp = QApplication(sys.argv) # Новый экземпляр QApplication
    env = {}
    window = Update_Project() # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    pp.exec()
