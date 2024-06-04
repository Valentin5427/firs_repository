from dpframe.base.inits import db_connection_init
from dpframe.base.inits import json_config_init
import sys
# sys.path.append('\\electrolab\\gui\\ui')
# sys.path.append('\\gui')
# sys.path.append('E:\wpm_new_3.7')
# sys.path.append('\\electrolab\\gui')
print(sys.path)
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QMainWindow , QDesktopWidget , QApplication
app = QApplication(sys.argv)

@json_config_init
@db_connection_init
class ForEnv(QWidget):
    def getEnv(self):
        return self.env
objEnv = ForEnv()
env = objEnv.getEnv()
db = env.db
print(3245, db.hostName(), db.lastError().text())