from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import  QMessageBox, QApplication
import json
import os

try:
        basedir = os.path.abspath(os.getcwd())
        basedir = '\\'.join(basedir.split('\\')[:4])
        print(basedir)
        path = basedir + "\config.json"
        with open(path, 'r') as file:
                data = json.load(file)
                print(data)
                db = QSqlDatabase.addDatabase('QPSQL')
                db.setHostName(data['db']['host'])
                db.setDatabaseName(data['db']['database'])
                db.setUserName(data['db']['user'])
                db.setPassword(data['db']['password'])
                db.setPort(5432)
                db.open()
                if not  db.isOpen() :
                        print(332,db.lastError().text())
                        app = QApplication([])
                        msg = QMessageBox()
                        msg.setWindowTitle("Ошибка подключения к базе")
                        msg.setText(db.lastError().text())
                        msg.exec_()
except Exception as ex:
        app = QApplication([])
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка подключения к базе")
        msg.setText(f"Файл 'config' отсутствует, {ex}")
        msg.exec_()





#
# db = QSqlDatabase.addDatabase('QPSQL')
# db.setHostName('10.5.0.21')
# db.setDatabaseName('electrolab')
# db.setUserName('electrolab')
# db.setPassword('electrolab')
# db.setPort(5432)
# db.open()
# print(db.isOpen())
#
# if not  db.isOpen() :
#         app = QApplication([])
#         msg = QMessageBox()
#         msg.setWindowTitle("Ошибка подключения к базе")
#         msg.setText("Проверьте файл 'config' или подключение к базе")
#         msg.exec_()



