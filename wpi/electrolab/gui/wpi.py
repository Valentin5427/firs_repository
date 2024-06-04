import sys
# sys.path.append('\\electrolab\\gui\\ui')
# sys.path.append('\\gui')
# sys.path.append('E:\wpm_new_3.7')
# sys.path.append('\\electrolab\\gui')
print(sys.path)
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QMainWindow , QDesktopWidget , QApplication
app = QApplication(sys.argv)
from electrolab.gui.TestInfo import TestInfo
from electrolab.gui.sprHeart import sprHeart
from electrolab.gui.sprApg import sprApg
from electrolab.gui.sprJobHeart import sprJob
# from electrolab.gui.sprSerialNumber import sprSerialNumber
# from electrolab.gui.sprDefect import sprDefect
# from electrolab.gui.sprTester import sprTester
# from electrolab.gui.sprTestingVoltage import sprTestingVoltage
# from electrolab.gui.sprClimat import sprClimat
# from electrolab.gui.JournalTest import JournalTest
# from electrolab.gui.sprTypeTrans import sprTypeTransformer
# from electrolab.gui.sprRoom import sprRoom
# from electrolab.gui.sprStand import sprStand
# from electrolab.gui.ParamsForRep import ParamsForRep
# from electrolab.gui.sprTypeTest import sprTypeTest
# from electrolab.gui.SprVoltageTN import SprVoltageTN
from electrolab.gui.common import UILoader
from electrolab.gui.msgbox import getTrue
import json

from electrolab.gui.ReportsMsr import  *
from dpframe.base.inits import json_config_init

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




def MyLoadUi(UiDir, UiFile, wnd):
    try:
        uidir = UiDir

        if not os.path.exists(uidir + UiFile):        
            uidir = ""
            

        uic.loadUi(uidir + UiFile, wnd)

        wnd.tag = 1
        return True
    except:    
        wnd.tag = 0
        QMessageBox.warning(None, u"Предупреждение", u"Проблемы с загрузкой файла: " + UiFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
        return False

from dpframe.base.inits import db_connection_init
from dpframe.base.inits import json_config_init


# Трансформаторы
@db_connection_init
@json_config_init
class Container(QWidget):
    def __init__(self, text):
        

        
        super(Container, self).__init__()

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oClsTrans = ClsTrans(self.env, 0)
        self.hbox.addWidget(self.oClsTrans)

# Серийные номера
@db_connection_init
@json_config_init
class Container_2(QWidget):
    def __init__(self):
        super(Container_2, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprSerialNumber = sprSerialNumber(self.env)
        self.hbox.addWidget(self.oSprSerialNumber)

# Несоответствия
@db_connection_init
@json_config_init
class Container_3(QWidget):
    def __init__(self):
        super(Container_3, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprTransformer = TestInfo(self,self.env)
        self.hbox.addWidget(self.oSprTransformer)

# Испытатели
@db_connection_init
@json_config_init
class Container_4(QWidget):
    def __init__(self):
        super(Container_4, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprTester = sprTester(self.env)
        self.hbox.addWidget(self.oSprTester)

# Испытательные напряжения
@db_connection_init
@json_config_init
class Container_5(QWidget):
    def __init__(self):
        super(Container_5, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprTestingVoltage = sprTestingVoltage(self.env)
        self.oSprTestingVoltage.ui.pushButton_4.setVisible(False)
        self.oSprTestingVoltage.ui.pushButton_5.setVisible(False)                                        
        self.hbox.addWidget(self.oSprTestingVoltage)

# Окружающая среда
@db_connection_init
@json_config_init
class Container_6(QWidget):
    def __init__(self):
        super(Container_6, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprClimat = sprClimat(self.env)        
        self.oSprClimat.ui.pushButton_4.setVisible(False)
        self.oSprClimat.ui.pushButton_5.setVisible(False)                                
        self.hbox.addWidget(self.oSprClimat)


# Журнал испытаний
@db_connection_init
@json_config_init
class Container_7(QWidget):
    def __init__(self):
        super(Container_7, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oJournalTest = JournalTest(self.env)
        self.hbox.addWidget(self.oJournalTest)

# Типы трансформаторов
@db_connection_init
@json_config_init
class Container_9(QWidget):
    def __init__(self):
        super(Container_9, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprTypeTransformer = sprTypeTransformer(self.env)
        self.hbox.addWidget(self.oSprTypeTransformer)

# Помещения
@db_connection_init
@json_config_init
class Container_10(QWidget):
    def __init__(self):
        super(Container_10, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprRoom = sprRoom(self.env)
        self.hbox.addWidget(self.oSprRoom)



# Параметры для отчетов
@db_connection_init
@json_config_init
class Container_12(QWidget):
    def __init__(self):
        super(Container_12, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oParamsForRep = ParamsForRep(self.env)
        self.hbox.addWidget(self.oParamsForRep)


# Типы испытаний
@db_connection_init
@json_config_init
class Container_13(QWidget):
    def __init__(self):
        super(Container_13, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprTypeTest = sprTypeTest(self.env)
        self.oSprTypeTest.ui.pushButton_4.setVisible(False)
        self.oSprTypeTest.ui.pushButton_5.setVisible(False)
        self.hbox.addWidget(self.oSprTypeTest)

# Справочник напряжений для знолов
@db_connection_init
@json_config_init
class Container_14(QWidget):
    def __init__(self):
        print(75675675)
        super(Container_14, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprHeart = sprHeart(self.env)
        # self.oSprVoltageTN.ui.pushButton_4.setVisible(False)
        # self.oSprVoltageTN.ui.pushButton_5.setVisible(False)
        self.hbox.addWidget(self.oSprHeart)


# ГОСТ точки
@db_connection_init
@json_config_init
class Container_18(QWidget):
    def __init__(self):
        print(576575673)
        super(Container_18, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprApg = sprApg(self.env)
        self.hbox.addWidget(self.oSprApg)
        print(65867867)

# Время работы станков
@db_connection_init
@json_config_init
class Container_21(QWidget):
    def __init__(self):
        print(576575675756)
        super(Container_21, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprJob = sprJob(self.env)
        self.hbox.addWidget(self.oSprJob)
        print(65867867)

# ГОСТ нагрузки
@db_connection_init
@json_config_init
class Container_16(QWidget):
    def __init__(self):
        super(Container_16, self).__init__()
        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hbox)
        self.oSprGost1 = sprGost(self.env, 2)
        self.hbox.addWidget(self.oSprGost1)
        print(5576547)


class Container_17(QDialog, UILoader):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setUI(env.config, u"DlgUpdate.ui")
        self.ui.checkBox.setChecked(True)
        self.ui.btn_update.clicked.connect(self.update)

    def update(self):
        print('обновляем')
        arg = 1
        if self.ui.checkBox_2.isChecked():
            arg = 0
        print(334, f'start {path}\\update\\update.exe {arg}')
        os.system(f'start {path}\\update\\update.exe {arg}')
        del_pid_sessions()


@db_connection_init
@json_config_init
#class wpm_new(QWidget, UILoader):
class wpi(QMainWindow):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        self.is_show = True
        try:
            print(path_ui)
        except:
            path_ui =  self.env.config.paths.ui + "/"


        if not MyLoadUi(path_ui, "wpi.ui", self):
            self.is_show = False
            return
                
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.action.triggered.connect(self.Action)
        self.action_2.triggered.connect(self.Action_2)
        self.action_14.triggered.connect(self.Action_14)
        self.action_18.triggered.connect(self.Action_18)
        self.action_21.triggered.connect(self.Action_21)
        # self.action_17.triggered.connect(self.Action_17)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.removeTab(index))

        if not self.TestBase(self.env.db):
            return

        self.action_2.trigger()
        
    def removeTab(self,index):
        print(54353, self.tabWidget.tabText(index))

        if self.tabWidget.tabText(index) == u'Трансформаторы':
            # print 'self.action_4'
            self.action_2.setEnabled(True)
        if self.tabWidget.tabText(index) == u'Сердечники':
            # print 'self.action_8'
            self.action_14.setEnabled(True)

        if self.tabWidget.tabText(index) == u'Температура АПГ':
            # print 'self.action_2'
            self.action_18.setEnabled(True)

        if self.tabWidget.tabText(index) == u'Время работы станков':
            # print 'self.action_2'
            self.action_21.setEnabled(True)



        self.tabWidget.removeTab(index)
            

    def Action(self):
        self.close()       
#        print self.tabWidget.count()        
#        self.tabWidget.addTab(QtGui.QWidget(self.tabWidget), 'Tab One')        
#        self.tabWidget.addTab(Container("smalltext2"), "smalltext2")
        
                
    def Action_2(self):
        # print 'Action_2'
        self.tabWidget.insertTab(0, Container_3(), u"Трансформаторы")
        self.tabWidget.setCurrentIndex(0)
        self.action_2.setEnabled(False)

    def Action_3(self):
        # print 'Action_3'
        self.tabWidget.insertTab(0, Container_4(), u"Испытатели")
        self.tabWidget.setCurrentIndex(0)
        self.action_3.setEnabled(False)

    def Action_4(self):
        print(57568756856)
        self.tabWidget.insertTab(0, Container("smalltext2"), u"Трансформаторы")
        self.tabWidget.setCurrentIndex(0)
        self.action_4.setEnabled(False)


    def Action_8(self):
        # print 'Action_8'
        self.tabWidget.insertTab(0, Container_2(), u"Серийные номера")
        self.tabWidget.setCurrentIndex(0)
        self.action_8.setEnabled(False)

    def Action_5(self):
        # print 'Action_5'
        self.tabWidget.insertTab(0, Container_5(), u"Испытательные напряжение")
        self.tabWidget.setCurrentIndex(0)
        self.action_5.setEnabled(False)

    def Action_7(self):
        # print 'Action_7'
        self.tabWidget.insertTab(0, Container_6(), u"Окружающая среда")
        self.tabWidget.setCurrentIndex(0)
        self.action_7.setEnabled(False)

    def Action_6(self):
        # print 'Action_6'
        self.tabWidget.insertTab(0, Container_7(), u"Журнал испытаний")
        self.tabWidget.setCurrentIndex(0)
        self.action_6.setEnabled(False)

    def Action_9(self):
        # print 'Action_9'
        self.tabWidget.insertTab(0, Container_9(), u"Типы трансформаторов")
        self.tabWidget.setCurrentIndex(0)
        self.action_9.setEnabled(False)

    def Action_10(self):
        # print 'Action_10'
        self.tabWidget.insertTab(0, Container_10(), u"Помещения")
        self.tabWidget.setCurrentIndex(0)
        self.action_10.setEnabled(False)

    def Action_11(self):
        # print 'Action_11'
        self.tabWidget.insertTab(0, Container_11(), u"Стенды")
        self.tabWidget.setCurrentIndex(0)
        self.action_11.setEnabled(False)

    def Action_12(self):
        # print 'Action_12'
        self.tabWidget.insertTab(0, Container_12(), u"Параметры для отчетов")
        self.tabWidget.setCurrentIndex(0)
        self.action_12.setEnabled(False)

    def Action_13(self):
        # print 'Action_13'
        self.tabWidget.insertTab(0, Container_13(), u"Типы испытаний")
        self.tabWidget.setCurrentIndex(0)
        self.action_13.setEnabled(False)

    def Action_14(self):
        print(3543653)
        # print 'Action_13'
        self.tabWidget.insertTab(0, Container_14(), u"Сердечники")
        self.tabWidget.setCurrentIndex(0)
        self.action_14.setEnabled(False)

    def Action_18(self):
        self.tabWidget.insertTab(0, Container_18(), u"Температура АПГ")
        self.tabWidget.setCurrentIndex(0)
        self.action_18.setEnabled(False)

    def Action_21(self):
        self.tabWidget.insertTab(0, Container_21(), u"Время работы станков")
        self.tabWidget.setCurrentIndex(0)
        self.action_21.setEnabled(False)





    def TestBase(self, db):
        query = QSqlQuery(db)
        # print u"Проверка наличия таблиц БД"
        err_tbl = ""
        query = QSqlQuery(db)
        
        query.prepare("select iscontroller from operator")
#        query.prepare("select thermal_current from transformer")
#        query.prepare("select declaration from type_transformer")
        
        if not query.exec_(): err_tbl += "table params\n"
        
        # print err_tbl
                    
        if err_tbl != "":
            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД требуется произвести изменения,
необходимые для работы приложения\n""" +
u"Произвести изменения БД?", QMessageBox.Yes, QMessageBox.No)                        
                        
            if r == QMessageBox.Yes:
                self.InitBase(db)
                return True
            else:
                return False
        return True

                                 
    def InitBase(self, db):
        # print u"Инициализация БД"
        query = QSqlQuery(db)

        SQL = u"""
ALTER TABLE OPERATOR ADD COLUMN iscontroller boolean;
COMMENT ON COLUMN operator.iscontroller IS 'Признак контролера СК';

ALTER TABLE TRANSFORMER ADD COLUMN thermal_current numeric(8,4);
ALTER TABLE TRANSFORMER ADD COLUMN dynamic_current numeric(8,4);
ALTER TABLE TRANSFORMER ADD COLUMN time_thermal_current integer;
ALTER TABLE TRANSFORMER ADD COLUMN copper_content numeric(8,4);
ALTER TABLE TRANSFORMER ADD COLUMN copper_alloy_content numeric(8,4);
COMMENT ON COLUMN transformer.thermal_current IS 'Ток термической стойкости';
COMMENT ON COLUMN transformer.dynamic_current IS 'Ток динамической стойкости';
COMMENT ON COLUMN transformer.time_thermal_current IS 'Время протекания тока термической стойкости';
COMMENT ON COLUMN transformer.copper_content IS 'Содержание меди';
COMMENT ON COLUMN transformer.copper_alloy_content IS 'Содержание медных сплавов';

ALTER TABLE type_transformer ADD COLUMN declaration character varying(40);
COMMENT ON COLUMN type_transformer.declaration IS 'Декларация';

CREATE TABLE type_transformersp
(
    id serial PRIMARY KEY,
    type_transformer integer REFERENCES type_transformer,
    var_constr_isp character varying(20),
    designation character varying(40) NOT NULL,
    manual character varying(40) NOT NULL
);
COMMENT ON TABLE type_transformersp IS 'Подтаблица к справочнику типов трансформаторов';
COMMENT ON COLUMN type_transformersp.id IS 'Идентификатор записи';
COMMENT ON COLUMN type_transformersp.type_transformer IS 'Ссылка на таблицу type_transformer';
COMMENT ON COLUMN type_transformersp.var_constr_isp IS 'Вариант конструктивного исполнения';
COMMENT ON COLUMN type_transformersp.designation IS 'Обозначение ПС';
COMMENT ON COLUMN type_transformersp.manual IS 'Руководство РЭ';


"""

        if not query.exec_(SQL):
            # print "Ошибка инициализации"
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
        else:
            # print "Инициализация выполнена!"
            QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)            
        return

        SQL = u"""
ALTER TABLE params ADD column date_begin date;
ALTER TABLE params ADD column clsparams integer;
COMMENT ON COLUMN params.date_begin IS 'Дата начала действия параметра';
COMMENT ON COLUMN params.clsparams IS 'Признак параметра';
UPDATE params SET date_begin = '01.01.2021', clsParams = 1 WHERE id = 1;
UPDATE params SET date_begin = '01.01.2021', clsParams = 2 WHERE id = 2;
"""
        SQL = u"""
CREATE TABLE params
(
  id serial PRIMARY KEY,
  name character varying(200) NOT NULL
);

COMMENT ON TABLE params IS 'Пораметры для отчета';
COMMENT ON COLUMN params.id IS 'Первичный ключ';
COMMENT ON COLUMN params.name IS 'Наименование параметра';
INSERT INTO params (id, name) VALUES (1, '№ А09-15-1167 от 07.12.2015г.');
INSERT INTO params (id, name) VALUES (2, '№ RA.RU.311442 от 25.12.2015г.');
"""

def excepthook(exc_type, exc_value, exc_tb):
    import traceback
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(5454, tb)
    QMessageBox.warning(None, u"Ошибка!!!!!", tb, QMessageBox.Ok)

import sys
sys.excepthook = excepthook



if __name__ == "__main__":
    print(3335)
    try:
        check_update()
    except:
        QMessageBox.warning(None, u"Ошибка!!!!!", 'Не удалось обновить', QMessageBox.Ok)
        pass
    app = QApplication(sys.argv)

    from dpframe.base.inits import db_connection_init
    from dpframe.base.inits import json_config_init

    @json_config_init
    @db_connection_init
    class ForEnv(QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
    db = env.db
    print(3245, db.hostName(), db.lastError().text())
    path_ui = env.config.paths.ui + "/"
    print(3335)

    import os
    if not os.path.exists(path_ui):
        path_ui = ""

    rez = db.open()
    if not rez:
        QMessageBox.warning(None, u"Предупреждение",
u"""Не установлено соединение с БД со следующими параметрами:
host: """ + db.hostName() + """
database: """ + db.databaseName() + """
user: """ + db.userName() + """
password: """ + db.password(),
QMessageBox.Ok)

    else:
        wind = wpi()
        wind.setWindowState(QtCore.Qt.WindowFullScreen)
        wind.showMaximized()
        wind.setWindowFlags(
            QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        if wind.is_show: 
            wind.show()
            wind.resizeEvent(None)
        print(3434, sys.path)
        sys.exit(app.exec_())


