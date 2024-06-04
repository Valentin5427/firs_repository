#coding=utf-8
import sys
import os
import json
from PyQt5.QtWidgets import  QTabBar , QSplashScreen, QMainWindow, QWidget,QMessageBox
from PyQt5.QtGui import QShowEvent, QCloseEvent, QPixmap
from PyQt5.QtCore import QTranslator, Qt, QRect
from dpframe.base.inits import json_config_init, db_connection_init, metadata_init, models_init, session_init, newmetadata_init
from dpframe.base import application
from dpframe.tech.typecheck import *
from dpframe.tech.typecheck import int_type
from electrolab.gui.inits import reference_init, serial_devices_init, report_init, filter_init
from electrolab.gui.reference import cZero
from  electrolab.gui.TestInfo import TestInfo
from electrolab.gui.msgbox import getTrue
basedir = os.path.abspath(os.getcwd())
path = '\\'.join(basedir.split('\\'))

pid = os.getpid()

def del_pid_sessions():
    os.system("taskkill  /F /pid " + str(pid))



def check_update():
    version = '1.1'
    try:
        with open(path + '/version.json', 'r') as file:
            version = json.load(file)['version']
    except:
        with open(path + '/version.json', 'w') as file:
            data = {'version': version}
            json.dump(data, file, indent=3)

    print('текущая версия',version)
    # ищем актуальную версию по пути конфига в update
    with open(path + '/update/config.json', 'r',encoding='utf-8') as file:
        path_dir  = json.load(file)['path']

    if not os.path.exists(path_dir):
        QMessageBox.warning(None, u"Предупреждение",
                            f"Не удалось проверить наличие обновления по пути {path_dir}",QMessageBox.Yes)
        return
    path_up = os.listdir(path_dir)
    print(path_up)
    #пробегаем по всем директориям и ищем файла version записываем версию и путь м в current_path последнюю версию
    current_path = {'version':0, 'path':''}
    for p in path_up:
        if 'version.json' in os.listdir(f"{path_dir}/{p}"):
            try:
                with open(f"{path_dir}/{p}/version.json", 'r') as file:
                    vs = json.load(file)['version']
                    print(87,vs)
                    if float(vs) > float(current_path['version']):
                        current_path = {'version':vs, 'path':f"{path_dir}/{p}"}

            except:
                pass
    # сравниваем с актуальной версией если на серваке нашлась версии позже актуальная то спрашиваем откатить версию
    # если нет то спрашиваем обновлять ?
    print(2245, float(version) >  float(current_path['version']))
    print(3486, float(version),  float(current_path['version']))




    if float(version) >  float(current_path['version']):
            if getTrue(None,'при проверке обнаружена более поздняя версия программы, обновить на данную версию?"'):
                print('Обновляем')
            r = QMessageBox.warning(None, u"Предупреждение",
                                    f"при проверке обнаружена более поздняя версия программы, обновить на данную версию?",
                                    QMessageBox.Yes, QMessageBox.No)
            if r == QMessageBox.Yes:
                print('Обновляем')
                os.system(f'start {path}\\update\\update.exe "{current_path["path"]}"')
                del_pid_sessions()
                return True
            else:
                return False

    if float(version) <  float(current_path['version']):
        r = QMessageBox.warning(None, u"Предупреждение", f"при проверке обнаружена \n новая версия программы,\n обновить версию программы?", QMessageBox.Yes, QMessageBox.No)
        if r == QMessageBox.Yes:
            print('Обновляем')
            os.system(f'start {path}\\update\\update.exe "{current_path["path"]}"')
            del_pid_sessions()
            print(342,current_path)
            return True
        else:
            return False




@report_init
@db_connection_init
@session_init
@json_config_init
class MainWnd(QMainWindow):

    # def __init__(self, caption, menu):
    #     super(MainWnd, self).__init__(caption, menu)
    #     self.centralWidget().setViewMode(self.centralWidget().TabbedView)
    #     for tab in self.centralWidget().findChildren(QTabBar):
    #         tab.setExpanding(False)
    #         tab.setTabsClosable(True)
    #         tab.tabCloseRequested.connect(self.closeTab)


    def __init__(self, caption=u"Info", cwidgetclass=QWidget):
        QMainWindow.__init__(self)
        self.setObjectName(u'MainWindow')
        self.setWindowTitle(caption)
        # self.ui = self.Ui(self, menu, cwidgetclass)
        # self.env = _env
        self.centralwidget = cwidgetclass(self, self.env)
        self.setCentralWidget(self.centralwidget)

    @takes('MainWnd', QShowEvent)
    @returns(nothing)
    def showEvent(self, event):
        # load session data
        storage = self.env.session.storage.mainwnd
        self.setGeometry(QRect(storage.x, storage.y, storage.width, storage.height))
        self.setWindowState(Qt.WindowStates(storage.state))


    @takes('MainWnd', QCloseEvent)
    @returns(nothing)
    def closeEvent(self, event):
        # Save session data
        storage = self.env.session.storage.mainwnd
        storage.state = int(self.windowState())
        rect = self.geometry()
        storage.x = rect.x()
        storage.y = rect.y()
        storage.width = rect.width()
        storage.height = rect.height()


        self.env.session.save()

    @takes('MainWnd', int_type)
    @returns(nothing)
    def closeTab(self, index):
        sub = self.centralWidget().subWindowList()[index]
        self.centralWidget().setActiveSubWindow(sub)
        self.centralWidget().closeActiveSubWindow()


def ExceptionHook(errType, value, tback):
    cZero().error(errType, value.message)
    sys.__excepthook__(errType, value, tback)
    #===========================================================================
    # mb = self._get_msg_wnd(text, infotext, detailedtext, title,
    #               QMessageBox.Critical, QMessageBox.Ok
    #              )
    # return mb.exec_()
    #===========================================================================

@returns(nothing)
def main():
    # check_update()
    app = application.get()
    pix = QPixmap(u'ui/ico/user_64.png')
    pix.scaledToHeight(100)
    splash = QSplashScreen(pix) #, Qt.WindowStaysOnTopHint)
    splash.show();
    splash.showMessage(u'Инициализация приложения', Qt.AlignHCenter | Qt.AlignBottom, Qt.blue);
    app.processEvents();
    sys.excepthook = ExceptionHook;

    qt_translator = QTranslator()
    if qt_translator.load( u':EL/qt_ru.qm'):
        app.installTranslator( qt_translator )

    # menu = JSONMenuLoader(u'menu_wpi.json').load()
    # menu = {}
    MainWindow = MainWnd(u'Info', TestInfo)

    app.processEvents();
    MainWindow.show()
    app.processEvents();
    splash.finish(MainWindow);

    sys.exit(app.exec_())

if u'__main__' == __name__:
    main()

