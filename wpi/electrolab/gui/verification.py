#coding=UTF-8
u"""
Created on 24.07.2012
#
@author: Knur
desc: 
"""
from PyQt4.QtGui import QDialog, QMessageBox, QIcon, QPalette, QColor
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QVariant, Qt, QString, QSize, QTime, QTimer, SIGNAL

from dpframe.tech.SimpleSound import SimpleSound

from electrolab.app.testmap import TestMap, BarCode  
from electrolab.app.item import Item  
from electrolab.app.coil import Coil   
from electrolab.app.verification import CoilVerification  
from electrolab.gui.common import UILoader
from electrolab.gui.simplechoice import SimpleChoice
from electrolab.gui.paramclimat import ParamClimat
from electrolab.gui.msgbox import getTrue, msgBox, msgBox3
from electrolab.gui.findserialnumber import FindSerialNumber
from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.data import helper
from electrolab.gui.reporting import FRPrintForm
from AccountCSM import WinCSM, BeforeBuildAccount
from electrolab.gui.toast import ToastMessage
import socket
import time
import json
import ReportsExcel

#tam
from electrolab.gui.TestCoil import TestCoil
from electrolab.gui.TestHighVoltage import TestHighVoltage
from devices import Devices
from config import Config
from StandMsr import StandMsr

# Временно
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
model_9 = QSqlQueryModel()
model_10 = QSqlQueryModel()


class PoingGrid(object):
    u"""Обертка над полями, используется для отображения точек. Надо на TableView переделать """
    
    class PointRecord(object):
        def __init__(self, _label, _A, _P):
            self.label = _label
            self.A = _A
            self.P = _P
            
    def __init__(self, _ui):
        self.ui = _ui
        self.pointGrid = {
                          1:self.PointRecord(self.ui.l1, self.ui.leA1, self.ui.leP1)
                          , 2:self.PointRecord(self.ui.l5, self.ui.leA5, self.ui.leP5)
                          , 3:self.PointRecord(self.ui.l20, self.ui.leA20, self.ui.leP20)
                          , 4:self.PointRecord(self.ui.l50, self.ui.leA50, self.ui.leP50)
                          , 5:self.PointRecord(self.ui.l100, self.ui.leA100, self.ui.leP100)
                          , 6:self.PointRecord(self.ui.l120, self.ui.leA120, self.ui.leP120)
                          , 7:self.PointRecord(self.ui.l14, self.ui.leA14, self.ui.leP14)
                          }

        self.normalPalette = QPalette()
        self.normalPalette.setColor(QPalette.Text, QColor(Qt.black))
        self.alarmPalette = QPalette()
        self.alarmPalette.setColor(QPalette.Text, QColor(Qt.red))
    
    def _show_point_record(self, _iKey, _oPointList):
        u"""Отображение точек"""
        bVisible = _oPointList and _oPointList.has_key(_iKey)
        if bVisible:
            if _oPointList[_iKey].quadroLoad:
                label = u'1/4'
            else:
                label = unicode(int(_oPointList[_iKey].I)) + u'%'
        else:
            label = None
        self.set_point_record(_iKey, bVisible, label)
    
    def show_point_grid(self, _oPointList):
        u"""Отображение точек"""
        for key in range(1,8):
            self._show_point_record(key, _oPointList)
        
    def clear(self):
        for key in range(1,8):
            self.pointGrid[key].A.setPalette(self.normalPalette)
            self.pointGrid[key].P.setPalette(self.normalPalette)
            self.pointGrid[key].A.clear()
            self.pointGrid[key].P.clear()
            
    def set_current_error(self, _key):
        self.pointGrid[_key].A.setPalette(self.alarmPalette)
            
    def set_angular_error(self, _key):
        self.pointGrid[_key].P.setPalette(self.alarmPalette)

    def set_point_record(self, _key, _visible, _I = None, _P = None, _A = None):
        #
        self.pointGrid[_key].label.setVisible(_visible)
        self.pointGrid[_key].A.setVisible(_visible)
        self.pointGrid[_key].P.setVisible(_visible)
        if None != _I:
            self.pointGrid[_key].label.setText(str(_I))
        if None != _A:
            self.pointGrid[_key].A.setPalette(self.normalPalette)
            self.pointGrid[_key].A.setText(unicode(_A))
        else:
            self.pointGrid[_key].A.clear()
        if None != _P:
            self.pointGrid[_key].P.setPalette(self.normalPalette)
            self.pointGrid[_key].P.setText(unicode(_P))
        else:
            self.pointGrid[_key].P.clear()


class VerificationForm(QDialog, UILoader):
    u""" """
    scan = pyqtSignal(str)
    recived = pyqtSignal(object)

    def __init__(self):
        super(QDialog, self).__init__()
                            
        
        #tam
        self.info = None
        self.codeTypeTest = None  # код теста
        
        self.setUI(self.env.config, u'Verification.ui')
        self.oHelpItem = helper.Item(self.env)
        self.oHelpCoil = helper.Coil(self.env)
        self.oHelpSerial = helper.SerialNumber(self.env)
        self.sound = SimpleSound(self.env)
        self.toast = ToastMessage()
        self.oDlgClimat = None
        self.lastSecondLoad = 0  #Последняя загрузка (для исключения повторений переключения магазина CA5018 и CA5020) 
        self.lastSecondCurrent = 0  #Последняя загрузка (для исключения повторений переключения магазина CA5020) 

        # self.oHelpStand = helper.Stand(self.env)
        # iStandID = self.oHelpStand.get_id(socket.gethostname())
        # if(iStandID == None):
        #     msgBox(self, u"Не настроено ни одного рабочего места для компьютера '%s'" % (socket.gethostname()))
        #     exit()
        # self.adStandInfo = None
        # if(self.oHelpStand.is_Single(socket.gethostname())):
        #     # self.adStandInfo = self.oHelpStand.get_info(iStandID)
        #     self.ui.btnTestType.setVisible(False)
        #     self.apply_test_type(iStandID)

    # # Применяем параметры видимости для данного стенда
    #     self.ui.btnAssistant.setVisible(self.adStandInfo.EnableAssistant)
    #     self.ui.btnSupervisor.setVisible(self.adStandInfo.EnableSupervisor)

    # Раскраска
        self.normalPalette = QPalette()
        self.normalPalette.setColor(QPalette.Foreground, QColor(Qt.black))
        self.alarmPalette = QPalette()
        self.alarmPalette.setColor(QPalette.Foreground, QColor(Qt.red))
        self.donePalette = QPalette()
        self.donePalette.setColor(QPalette.Foreground, QColor(Qt.darkGreen))
        
    #Агрегация диалогов Порядок не менять, с начала диалоги, потом логика! При старте генерятся события вызова формы
        self.oDlgChoice = SimpleChoice(self.env)
        self.ui.hlMain.addWidget(self.oDlgChoice)
        self.oDlgChoice.setVisible(False)
        
        # self.oDlgClimat = ParamClimat(self.env, self.adStandInfo.Room)
        self.oDlgClimat = ParamClimat(self.env, None)
        self.ui.hlMain.addWidget(self.oDlgClimat)
        self.oDlgClimat.setVisible(False)
        self.oDlgClimat.applied.connect(self.set_climat)
        
        self.oKeyboard = DigitalKeyboard(self.env)
        self.ui.vlInfo.addWidget(self.oKeyboard)
        self.oKeyboard.setVisible(False)

        self.oDlgSerialNumber = FindSerialNumber(self.env, self.oKeyboard)
        self.ui.vlView.addWidget(self.oDlgSerialNumber)
        self.oDlgSerialNumber.setVisible(False)
        self.oDlgSerialNumber.hideDialog.connect(self.hide_serial_find)
        
    #Агрегация логики
        self.oMap = TestMap(self.env)
                
        # if(self.adStandInfo):
        #     self.oMap.set_up(self.adStandInfo)
        #     self.oDlgClimat.setRoom(self.adStandInfo.Room)
        self.oMap.requestTester.connect(self.get_tester)
        self.oMap.requestSupervisor.connect(self.get_supervisor)
        self.oMap.requestClimat.connect(self.get_climat)
        # self.oMap.testTypeSelected.connect(self.testtype_apply)
        self.oMap.testerSelected.connect(self.tester_apply)
        self.oMap.assistantSelected.connect(self.assistant_apply)
        self.oMap.supervisorSelected.connect(self.supervisor_apply)
        self.oMap.selected.connect(self.map_select)
        self.oMap.mapRefresh.connect(self.view_refresh)
        self.oMap.mapRefresh.connect(self.button_refresh)
        self.oMap.dublicated.connect(self.msg_item_dublicate)
        
        #tam 24.11.2016       
        self.oMap.calc_global.connect(self.calc_global)
        


        #tam
        # Создаем объект oTestCoil для испытаний типа 3,4 
        
        self.oTestCoil = TestCoil(self.env, self.oMap, self.ui.tvItem, self.ui.tvCoil, self.ui.btnStart, self)
        self.ui.vlInfo.addWidget(self.oTestCoil)
        self.oTestCoil.setEnabled(True)
        self.oTestCoil.setVisible(False)
        # 7.12.2016 Создаем объект oTestHighVoltage для испытаний типа 7 
        self.oTestHighVoltage = TestHighVoltage(self.env, self.oMap, self.ui.tvItem, self.ui.tvCoil, self.ui.btnStart, self)
#        self.oTestHighVoltage = TestHighVoltage(self.env, self.oMap, iStandID, self.ui.tvItem, self.ui.btnStart, self)
        self.ui.vlInfo.addWidget(self.oTestHighVoltage)
        self.oTestHighVoltage.setEnabled(True)
        self.oTestHighVoltage.setVisible(False)
        
        self.ui.toolButton.setVisible(False)
        
        # Создаем объект self.Devices_ для работы с прибором CA5018 
        self.Devices_ = Devices(self.env)
        
        #TAM
        self.ui.btnStickers.setVisible(False)
        self.ui.btnDevices.setVisible(False)
        self.ui.btnMsr.setVisible(False)
        self.ui.btnStickers.clicked.connect(self.btnStickers_Click)
        self.ui.btnInfo.clicked.connect(self.btnInfo_Click)
        self.ui.btnArchive.clicked.connect(self.StartArchive)
        self.ui.btnMsr.clicked.connect(self.StartMsr)
        self.ui.toolButton.clicked.connect(self.toolButton_Click)
        #self.ui.btnDevices.clicked.connect(self.btnDevices_Click1)
        #self.ui.btnDevices.clicked.connect(self.btnDevices_Click)
                    
        self.ui.btnConfig.clicked.connect(self.setConfig)
                    
                                        


        self.oItem = None
        self.oCoil = None
        self.oCoilVerification = None
        self.oDlgSerialNumber.adding.connect(self.oMap.item_add)
        print '                          VERIFICATION self.oMap.item_add1'
        self.errorPointIndex = None
        
        
#TODO:        self.scan.connect(self.oMap.item_add)
        
    # подключение окружения к View
        self.ui.tvItem.env = self.env
        self.ui.tvCoil.env = self.env
    # Кнопки для tvItem
        #_pos - расположение кнопки:
        #    1 = "Справа вверху"
        #    2 = "Слева вверху"
        #    3 = "Справа внизу"
        #    4 = "Слева внизу"
        #_name - имя кнопки (в коде)
        #_text - надпись на кнопке
        #_icon - иконка на кнопке
    
        self.btnItemDelete = self.ui.tvItem.addButton(3, u"btnItemDelete", u'', QIcon(u':/ico/ico/delete_64'))
        self.btnItemSetDefect = self.ui.tvItem.addButton(3, u"btnItemSetDefect", u'', QIcon(u':/ico/ico/warning_64'), True)
        self.btnItemAddI = self.ui.tvItem.addButton(2, u"btnItemAddI", u'', QIcon(u':/ico/ico/pencil_64'))
        self.ui.tvItem.btnPressed.connect(self.item_btn_process)
        self.ui.tvItem.rowChanged.connect(self.item_change_row)
        self.item_view_button_refresh()
        
        self.btnCoilClear = self.ui.tvCoil.addButton(3, u"btnCoilClear", u'', QIcon(u':/ico/ico/redo'), True)
        self.btnCoilErrorClear = self.ui.tvCoil.addButton(3, u"btnCoilErrorClear", u'', QIcon(u':/ico/ico/redo_green'), True)
        self.ui.tvCoil.btnPressed.connect(self.coil_btn_process)
        self.ui.tvCoil.rowChanged.connect(self.coil_change_row)
        self.coil_view_button_refresh()
        
        self.oPointGrid = PoingGrid(self.ui)
    #Иницифлизация стенда
        self.oHelpStand = helper.Stand(self.env)
        iStandID = self.oHelpStand.get_id(socket.gethostname())
        if(iStandID == None):
            msgBox(self, u"Не настроено ни одного рабочего места для компьютера '%s'" % (socket.gethostname()))
            #exit() TAM закоментировал, чтобы иметь возможность войти в редактор файла config.json
        self.adStandInfo = None
        
#        self.oHelpStand.
        
        #tam
        self.VSpacer = self.ui.vlInfo.itemAt(1)
        self.ui.vlInfo.removeItem(self.VSpacer)

        if(self.oHelpStand.is_Single(socket.gethostname())):
            # self.adStandInfo = self.oHelpStand.get_info(iStandID)
            self.ui.btnTestType.setVisible(False)
            self.apply_test_type(iStandID)

    #Обновить интерфейс
        self.button_refresh()
        if(self.adStandInfo == None):
            self.get_test_type()
        else:
            self.get_tester()
#        self.for_debug()#TODO: Убрать каку - Это вызов тестилки
        
        #Цепляем сканер
        self.oBarCode = BarCode()
        self.scanner = self.env.devices.scanner
        self.scanner.SetHandler(self.scanning)

        
        #Включаем сканер
        try:
            self.scanner.SetEnabled(True)
            self.scan.connect(self.scan_slot)
        except:
            msgBox(self, u"Ошибка подключения сканера.")
        #Включаем knt05
        self.oKNT05 = self.env.devices.knt05
        self.oKNT05.SetHandler(self.recive_data)
        try:
            self.oKNT05.SetEnabled(True)
        except:
            msgBox(self, u"Ошибка подключения КНТ-05.")
        
        # Подключаем таймер
        self.timer = QTimer()
#        self.timer.connect(self.timer, PyQt4.QtCore.SIGNAL('timeout()'), lambda: self.outTime())        
        self.timer.connect(self.timer, SIGNAL('timeout()'), lambda: self.outTime())        
        self.timer.start(1000)

        #TAM
        self.oTestHighVoltage.get_standId(iStandID)

        self._I_old = None # Для сохранения предыдущей точки после нажатия на паузу

        try:
            #Сохранение в config.json состояния галочек
            f = open('config.json','r')
            dataConfig = json.load(f)
            
#            self.ui.checkBox.setChecked(dataConfig['verification']['autoCA5018'])
#            self.ui.checkBox_2.setChecked(dataConfig['verification']['autoPR200']) 
            #30.06.2020               
            self.ui.autoTest.setChecked(dataConfig['verification']['autoTest'])
            self.ui.autoCA5018.setChecked(dataConfig['verification']['autoCA5018'])
            self.ui.autoPR200.setChecked(dataConfig['verification']['autoPR200'])                
        except:
            pass

            
        # регулируем размеры и положение окна
#        self.setMaximumHeight(850)
#        self.setMaximumWidth(800)
#        self.move(300,0)
                        
                        
#    def timerEvent(self, event):
        #self.seconds += 1
#        self.lineEdit_2.setText(str(self.seconds))
#        self.ui.label_3.setText(str(self.seconds))
                        
    def outTime(self):
        self.ui.timeEdit.setTime(QTime.currentTime())
                        
                                                
    # Временно                                            
    def toolButton_Click(self):
        
       # print self.env.devices
        
        print 'env.config.devices.ca5018_1.active = ', self.env.config.devices.ca5018_1.active
        print 'env.config.devices.ca5020.active = ', self.env.config.devices.ca5020.active
        print 'env.config.devices.ca5020.port = ', self.env.config.devices.ca5020.port
        
        
#        self.Devices_.WriteToCA5020(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)
        self.Devices_.WriteToCA5020(10, 5)
        
        
        
        return
        
        
        print u'Поиск точки ' + unicode(5) + u'%'
        return
        
        #self.start(self.ui.btnStart)
        self.ui.btnStart.click()
        return        
                
        self.WritePointToPR200(7)
        return
        
        self.Devices_.WriteToPR200(512, 88)        
        
        return
    
        self.Devices_.WriteToCA5018(1.25)        
        
        return
        self.print_temp(157287, 1, True)
                                                    
#        self.print_temp(157469, 2, True)
                                            
                                                
    def btnStickers_Click(self):
        print 'btnStickers_Click  self.oMap.iMapID=', self.oMap.iMapID
        
        #from electrolab.gui.reporting import FRPrintForm
#        inputParms = {}
#        inputParms = {u'test_map':52877}
#        inputParms = {u'test_map':self.oMap.iMapID, u'coefR':self.oTestCoil.coefR}
        inputParms = {u'test_map':self.oMap.iMapID, u'item':0}
        try:
            rpt = FRPrintForm(u'ReportStickers.fr3' ,inputParms , self.env)
            rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
            rpt.preview()
            # rpt.design()
        except:
            pass

        
    def btnInfo_Click(self):
        self.oTestCoil.pushButton_Click()



                
    def for_debug(self):#TODO: Убрать каку - Это тестилка
        self.oMap.select(2686)

    def scanning(self, _sSerialNumber = None):
        #TODO: Это сделано чтобы работать через сигналв Qt иначе глюки в интерфейсе, сканер живет в отдельном потоке
        self.scan.emit(QString(_sSerialNumber))

    def recive_data(self, _oData):
        #TODO: Это сделано чтобы работать через сигналв Qt иначе глюки в интерфейсе, сканер живет в отдельном потоке
        self.recived.emit(_oData)

    @pyqtSlot(str)
    def scan_slot(self, _sSerialNumber = None):
        print 'scan_slot' #22.11.2016
        if self.is_work():
            return
        parseResult = self.oBarCode.parse_barcode(_sSerialNumber)
        if parseResult.error:
            msgBox(self, parseResult.error)
            return
        serialDescription = self.oHelpSerial.get_id(parseResult.year, parseResult.serial)
        if serialDescription.id and self.oMap:
            self.oMap.item_add(serialDescription.id)
            print '                          VERIFICATION self.oMap.item_add2'
            self.toast.ShowText(unicode(parseResult.serial), 72)
        else: 
            msgBox(self, u'Не найден заводской номер %s за %s год' % (parseResult.serial, parseResult.year))
        
    def item_btn_process(self, _sender, _checked):
        u"""Обработка сигнала от кнопок на View трансформаторов"""
        if _sender.objectName() == u"btnItemAddI":
            self.show_serial_find()
        elif self.oItem == None:
            return
        elif _sender.objectName() == u"btnItemDelete" and getTrue(self, u'Удалить трансформатор?'):
            self.oItem.delete()
        elif _sender.objectName() == u"btnItemSetDefect":
            self.get_defect()

    def coil_clear(self):
        self.oCoilVerification.clear()
        self.oCoil.clear(self.oCoil.iCoilID) #TODO: Плохо надо сделать через сигнал, пока и так сойдет
        self.oItem.set_noteste(self.oItem.iItemID)
        self.oMap.reset_state()
        self.errorPointIndex = None
        self.cheking_refresh()


    def coil_clear_error(self):
        self.oCoilVerification.clear_error(self.errorPointIndex)
        self.oCoil.clear(self.oCoil.iCoilID) #TODO: Плохо надо сделать через сигнал, пока и так сойдет
        self.oItem.set_noteste(self.oItem.iItemID)
        self.oMap.reset_state()
        self.errorPointIndex = None
        self.cheking_refresh()

    def coil_btn_process(self, _sender, _checked):
        u"""Обработка сигнала от кнопок на View обмоток"""
        if self.oItem == None:
            return
        
        #tam
        if self.codeTypeTest in [3,4]:
#            if _sender.objectName() == u"btnCoilClear" and getTrue(self, u'Очистить обмотку?'):
#                self.oTestCoil.coil_clear()
            if _sender.objectName() == u"btnCoilClear":
                if getTrue(self, u'Вы действительно желаете очистить график?'):
                #rez = msgBox3(self, u'Очистить только график без сопротивления?')
                #if rez == QMessageBox.Yes:
                    self.oTestCoil.coil_clear(2)
                    self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True)
                    print 'calcGlobal                     111111111111111111111111111111'
                #if rez == QMessageBox.No:
                #    self.oTestCoil.coil_clear(1)
                #self.oTestCoil.calcGlobal()            
            return                
        
        
        if _sender.objectName() == u"btnCoilClear" and getTrue(self, u'Очистить обмотку?'):
            self.coil_clear()
        if _sender.objectName() == u"btnCoilErrorClear" and getTrue(self, u'Очистить точку?'):
            self.coil_clear_error()
            
    @pyqtSlot(QVariant)
    def item_change_row(self, _qvValue):
        u"""Обработка сигнала перехода по трансформаторам"""
        #QMessageBox.warning(self, u"Предупреждение", u"Переход по трансформаторам", QMessageBox.Ok)
        # Отключаем временно
        '''
        if self.is_work():
            if self.codeTypeTest not in [3,4]:                
                if self.ui.checkBox_2.isChecked():        
                    self.WriteToPR200_zero()
                #    time.sleep(5)
        '''
        
        if self.oItem:
            iValue = _qvValue.toInt()[0] if _qvValue.toInt()[1] else None 
            if iValue: 
                self.oItem.select(iValue)
            self.oItem.select(iValue)       #tam нафиг эта строчка нужна? може убрать?
            
            #tam 
            if self.oCoil:
                if self.codeTypeTest in [3,4]:
                    self.oTestCoil.item_change_row(self.oCoil.iItemID)
                #7.12.2016                    
                if self.codeTypeTest in [7]:
                    self.oTestHighVoltage.item_change_row(self.oCoil.iItemID)                
            
            
                        
        self.item_view_button_refresh()

        
    @pyqtSlot(QVariant)
    def coil_change_row(self, _qvValue):
       # print u"Обработка сигнала перехода по обмоткам___________________________", self.oCoil
        u"""Обработка сигнала перехода по обмоткам"""
        #QMessageBox.warning(self, u"Предупреждение", u"Переход по обмоткам", QMessageBox.Ok)
        if self.oCoil:
            iValue = _qvValue.toInt()[0] if _qvValue.toInt()[1] else None
            
            #tam            
            if self.codeTypeTest in [3,4]:
                self.oTestCoil.coil_change_row(self.oCoil.iCoilID, self.oCoil.iItemID)                
            #7.12.2016            
            #if self.codeTypeTest in [7]:
            #    self.oTestCoil.coil_change_row(self.oCoil.iCoilID, self.oCoil.iItemID)                

                            
            if iValue: 
                self.oCoil.select(iValue)
        self.coil_view_button_refresh()
        self.button_refresh()


#        16.06.2020
        if self.oCoilVerification != None and self.oCoil != None:
###30            self.ui.lineEdit.setText(self.ui.lineEdit.text() + "*" + str(self.oCoilVerification.info.SecondLoad))
            if self.is_work():
                if self.codeTypeTest not in [3,4]:                
#                    if self.ui.checkBox.isChecked() and self.lastSecondLoad != self.oCoilVerification.info.SecondLoad:
                    
                    if self.env.config.devices.ca5020.active:
# 11.10.2021                        if self.ui.autoCA5018.isChecked() and self.lastSecondLoad != self.oCoilVerification.info.SecondLoad and self.lastSecondCurrent != self.oCoilVerification.info.SecondCurrent:
                        if self.ui.autoCA5018.isChecked() and (self.lastSecondLoad != self.oCoilVerification.info.SecondLoad or self.lastSecondCurrent != self.oCoilVerification.info.SecondCurrent):
                            self.Devices_.WriteToCA5020(self.oCoilVerification.info.SecondLoad, self.info.SecondCurrent)
                            self.lastSecondLoad = self.oCoilVerification.info.SecondLoad
                            self.lastSecondCurrent = self.oCoilVerification.info.SecondCurrent
                    else:        
                        #30.06.2020
                        if self.ui.autoCA5018.isChecked() and self.lastSecondLoad != self.oCoilVerification.info.SecondLoad:
                            self.Devices_.WriteToCA5018(self.oCoilVerification.info.SecondLoad, self.info.SecondCurrent)
                            self.lastSecondLoad = self.oCoilVerification.info.SecondLoad
###30                        self.ui.lineEdit_2.setText(self.ui.lineEdit_2.text() + "*" + str(self.oCoilVerification.info.SecondLoad))

#            print 'self.oCoilVerification.info.SecondLoad &&&&&&&&&&&&1 self.oCoilVerification.info.SecondLoad = ', self.oCoilVerification
#            if self.oCoilVerification != None:
#                print 'self.oCoilVerification.info.SecondLoad &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&1 self.oCoilVerification.info.SecondLoad = ', self.oCoilVerification.info.SecondLoad, self.ui.lbSecondLoad.text()

        
       # print u"Обработка сигнала перехода по обмоткам", self.oCoil
        #tam
        if self.oCoil != None:
            if self.codeTypeTest in [3,4]:
               # print "oTestCoil.isVisible()oTestCoil.isVisible()oTestCoil.isVisible()=", self.oTestCoil.isVisible()
                self.oTestCoil.coil_after_change_row(self.oCoil.iCoilID, self.oCoil.iItemID, self.oCoilVerification.info)                
        
    @pyqtSlot()
    def map_close(self):
        self.ImportIntoMapMsr()
        #tam        
#        if self.is_work(): self.is_work скорее всего в этот момент = false 
        if self.codeTypeTest not in [3,4]:
                            
#            if self.ui.checkBox_2.isChecked():        
#                self.WriteToPR200_zero()
            #30.06.2020
            if self.ui.autoPR200.isChecked():
                self.WriteToPR200_zero()
                
        if self.oMap.iMapID != None and self.codeTypeTest in [3,4]:
            # Проверяем, вся ли тележка протестирована
            if self.oTestCoil.done_test():
                self.oMap.stateMap = self.oMap.DONE                
        
        if self.oMap.DONE == self.oMap.stateMap:
            if getTrue(self, u'Сохранить тележку?'):
                
                
                #TAM 5.04.21
#                QMessageBox.warning(self, u"Предупреждение", str(self.oMap.iMapID) + " " + str(self.adStandInfo.Room) + " " + str(iStandID) + " " + str(self.adStandInfo.ID), QMessageBox.Ok)
#                QMessageBox.warning(self, u"Предупреждение", str(self.oMap.iMapID) + " " + str(self.adStandInfo.Room) + " " + str(self.adStandInfo.ID), QMessageBox.Ok)
                self.update_climat(self.oMap.iMapID, self.adStandInfo.Room)
                #self.adStandInfo.Room
                #iStandID    
                #self.adStandInfo.ID
                
                
                
                self.print_report(self.oMap.iMapID)
            else:
                return False
        elif self.oMap.FULL == self.oMap.stateMap:
            if not getTrue(self, u'Отложить тележку?'):
                return False
            #TAM
            else:
                
                
                #TAM 5.04.21
#                QMessageBox.warning(self, u"Пред_2", str(self.oMap.iMapID), QMessageBox.Ok)
#                QMessageBox.warning(self, u"Пред_2", str(self.oMap.iMapID) + " " + str(self.adStandInfo.Room) + " " + str(self.adStandInfo.ID), QMessageBox.Ok)
#                self.update_climat(self.oMap.iMapID, self.adStandInfo.ID, self.adStandInfo.Room)
                self.update_climat(self.oMap.iMapID, self.adStandInfo.Room)
                
                
                
                if self.ui.btnTicketMatrix.isChecked() and self.ui.btnTicketMatrix.isVisible():
                    try:
                        inputParms = {u'test_map':self.oMap.iMapID, u'item':0}
                        if self.codeTypeTest in [3,4]:
                            rpt = FRPrintForm(u'ReportStickers.fr3' ,inputParms , self.env)
                            #rpt.preview()
                            rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                            rpt.print_()
                            # rpt.design()
                        if self.codeTypeTest in [0,2]:
                            
                            
                            # Временно
                            if self.codeTypeTest == 0:
                                self.print_temp(self.oMap.iMapID, 1, False)
                            else:    
                                self.print_temp(self.oMap.iMapID, 2, False)

                        
                            # Вернуть
                            ###
                            #inputParms = {u'test_map':84016, u'item':0}
                            rpt = FRPrintForm(u'ReportStickers_2.fr3' ,inputParms , self.env)
                            rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                            #rpt.preview()
                            rpt.print_()
                            # rpt.design()
                            ###
                    except:
                        pass
                                
        self.oMap.close()
        self.button_refresh()
        self.view_refresh()
        #tam
        self.oTestCoil.clear()
        return True
        

           
    #TAM 5.04.21
    # Присоединение климатических условий к таблице test_map,
    # если этого не произошло во время испытаний по непонятным причинам
#    def update_climat(self, test_map, stand, room):
    def update_climat(self, test_map, room):
        try:
            print 'self.codeTypeTest = ', self.codeTypeTest
            if self.codeTypeTest != 1:
                return
      #      print 'stand = ', stand, type(stand)
            self.query_9 = QSqlQuery(self.env.db)
            print 44
            print test_map, type(test_map)
                     
            strSQL = u"select climat from test_map where id = " + str(test_map)                   

            print strSQL
                
            self.query_9.prepare(strSQL)
            print 55
            if not self.query_9.exec_():
                return
#                QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса", QMessageBox.Ok)
            else:    
                model_10.setQuery(self.query_9)
            print 66
            if model_10.rowCount() > 0:
                print 77
                print model_10.rowCount()
                print model_10.record(0).field('climat').value().toString()
              #  print 'model_10.record(0).field(climat) = ', model_10.record(0).field('climat').value(), model_10.record(0).field('climat').toString()
                print 771
                if model_10.record(0).field('climat').value().toString() == '' or model_10.record(0).field('climat').value().toString() == '0':
                    print 88
                     
                    strSQL = u"select max(id) as id from climat where room = " + str(room)                   
                    print 99

                    print strSQL
                
                    self.query_9.prepare(strSQL)
                    if not self.query_9.exec_():
                        print 1
#                        QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса_2", QMessageBox.Ok)
                        return
                    else:    
                        print 2
                        model_10.setQuery(self.query_9)
                        print 3
#                        QMessageBox.warning(self, u"Предупреждение", model_10.record(0).field('id').value().toString(), QMessageBox.Ok)
                    
                    


                        strSQL = u"update test_map set climat = " + model_10.record(0).field('id').value().toString() + " where id = " + str(test_map)                   
                        print 991

                        print strSQL
                
                        self.query_9.prepare(strSQL)
                        if not self.query_9.exec_():
                            print 11
#                            QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса_2", QMessageBox.Ok)
                            return


                    
                    
                    pass
                
                
        except:
            pass
        
        
        
    @pyqtSlot(int)
    def map_select(self, _iMapID):
        print 'map_select=', _iMapID
        #print 'self.oItem.iItemID=', self.oItem.iItemID
        #print 'self.oTestCoil.globalInfa=', self.oTestCoil.globalInfa
        
        if not _iMapID.toInt()[1]:
            if self.oItem:
                self.oItem.select(None)
                self.oItem = None
        else:
            if self.oItem:
                self.oItem.selectedItem.connect(self.item_select)
                self.oItem.deleted.connect(self.oMap.reset_state)
                self.oItem.changeItem.connect(self.oMap.reset_state)
                self.oItem.noEmptyItem.connect(self.msg_item_full)
#                self.oItem.lastItemDone.disconnect(self.oMap.stop)

            self.oItem = Item(self.env, self.adStandInfo, _iMapID.toInt()[0], True)
            self.oItem.selectedItem.connect(self.item_select)  # Зачем повторять?
            self.oItem.deleted.connect(self.oMap.reset_state)
            self.oItem.changeItem.connect(self.oMap.reset_state)
            self.oItem.noEmptyItem.connect(self.msg_item_full)
#            self.oItem.lastItemDone.connect(self.oMap.stop)
        
#        self.oMap.select(_iMapID)
        sQuery = u'''
                select 
                    it.id
                    , case
                        when defect is not null then ':/ico/ico/warning_64.png'
                        when istested then ':/ico/ico/tick_64.png'
                        else null
                    end
                    , sn.serialnumber 
                    , tsf.shortname
                    /*, df.fullname*/
                from  
                    item it
                left join
                    serial_number sn
                on
                    it.serial_number = sn.id
                left join
                    transformer tsf
                on
                    tsf.id = sn.transformer
                left join
                    defect df
                on
                    df.id = it.defect
                where 
                    it.test_map = %s
                order by
                    it.id
                ;''' % (_iMapID.toInt()[0] or 0)
        self.ui.tvItem.set_image_column(1, QSize(72, 72))
        self.ui.tvItem.set_query(sQuery)
        self.ui.tvItem.keyFieldName = u"id"
        self.ui.tvItem.table.hideColumn(0)
#        self.ui.tvItem.set_row(0)
        self.button_refresh()
        self.view_refresh()
        print '                     map_select1'
        #14.11.2016  TAM                        
        #if self.codeTypeTest in [3,4]:
        #    self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None)            
        print '                           map_select2'
#        print 'self.oItem.iItemID=', self.oItem.iItemID
        #msgBox(self, u"Латер не достиг номинального тока.\n Перепроверьте эту катушку заново!")
        
        #print 'self.oTestCoil.globalInfa=', self.oTestCoil.globalInfa



    @pyqtSlot(int)
    def item_select(self, _iItemID):
        #print 'item_select=', _iItemID
        self.show_item_info(_iItemID)
        if not _iItemID.toInt()[1]:
            self.oCoil.select(None)
            self.oCoil = None
            self.oCoilVerification = None
        else:
            if self.oCoil:
                self.oCoil.selected.disconnect(self.coil_select)
                self.oCoil.cleared.disconnect(self.cheking_refresh)
                self.oCoil.lastCoilDone.disconnect(self.oItem.complit)
                self.oCoil.done.disconnect(self.oItem.chek_done)
            self.oCoil = Coil(self.env, self.adStandInfo, self.oMap.iMapID, _iItemID.toInt()[0], True)
            self.oCoil.selected.connect(self.coil_select)
            self.oCoil.cleared.connect(self.cheking_refresh) 
            self.oCoil.lastCoilDone.connect(self.oItem.complit)
            self.oCoil.done.connect(self.oItem.chek_done)

            '''            
                                  unicode(info.CoilNumber) + u'И1'
                                  + u'-' 
                                  + unicode(info.CoilNumber) + u'И' + unicode(info.Tap)
select cast(coilnumber as integer)||'И1-'||cast(coilnumber as integer)||'И'||cast(tap as integer) as coilname,
                                  
            '''
        
        coil = 'coil cl'
        if self.codeTypeTest in [0,3,4]:
            coil = '(select min(id) id, coilnumber, tap, transformer from coil group by coilnumber, tap, transformer) cl'
            
        sQuery = u'''
                    select 
                        cl.id
                        --, 'И' || cl.coilnumber || 'И' || cl.tap
                        , cast(coilnumber as integer)||'И1-'||cast(coilnumber as integer)||'И'||cast(tap as integer) as coilname
                    from  
                        item it
                    left join
                        serial_number sn
                    on
                        it.serial_number = sn.id
                    inner join
                    '''
        sQuery += coil
            
#                        coil cl
#(select min(id) id, coilnumber, tap, transformer from coil group by coilnumber, tap, transformer) cl

        sQuery += u'''
                    on
                        sn.transformer = cl.transformer
                    where
                        it.id = %s
                    order by
                        cl.coilnumber 
                        , cl.tap

                    ;''' % (_iItemID.toInt()[0] or 0)
                    
#        print sQuery            
#        self.ui.tvCoil.rowChanged.disconnect(self.coil_change_row)
        self.ui.tvCoil.set_query(sQuery)
        self.ui.tvCoil.keyFieldName = u"id"
        self.ui.tvCoil.table.hideColumn(0)
#        self.ui.tvCoil.rowChanged.connect(self.coil_change_row)
        self.ui.tvItem.set_row_by_key(_iItemID)
#        self.button_refresh()
        #msgBox(self, u"item_select")

    @pyqtSlot(int)
    def coil_select(self, _iCoilID):
        self.show_coil_info(_iCoilID)
        self.oPointGrid.clear()
        self.ui.lState.setPalette(self.normalPalette)
        self.ui.lState.setText(u'Нет обмотки')
        prevStateWork = False #Сохраняет состояние работы прикладной верификации 

        if None == self.oItem or None == self.oCoil or not _iCoilID.toInt()[1]:
            self.oCoilVerification = None
            return
            
        if None != self.oCoilVerification:
            prevStateWork = self.oCoilVerification.is_work()
            self.oCoilVerification.PointFound.disconnect(self.draw_point)
            self.oCoilVerification.PointErrorAngular.disconnect(self.draw_point_angular_error)
            self.oCoilVerification.PointErrorCurrent.disconnect(self.draw_point_current_error)
            self.oCoilVerification.PointError.disconnect(self.draw_point_error)
#            self.oCoilVerification.worked.disconnect(self.oMap.start)
            self.oCoilVerification.paused.disconnect(self.full_refresh)
            self.oCoilVerification.worked.disconnect(self.button_refresh)
            self.oCoilVerification.proggress.disconnect(self.draw_proggress)
            self.oCoilVerification.PointLeft.disconnect(self.draw_point_left)
            self.oCoilVerification.PointRight.disconnect(self.draw_point_right)
            self.oCoilVerification.PointEmpty.disconnect(self.draw_coil_empty)
#TODO:иногда oCoil умерает раньше чем oCoilVerification по этому disconnect не прокатывает 
#            self.oCoilVerification.PointOut.disconnect(self.oCoil.set_done)
            self.oCoilVerification.CoilDone.disconnect(self.draw_coil_done)
#            self.oCoilVerification.NeedCurrentOff.disconnect(self.draw_needCurrentOff)
            self.oCoilVerification.PointQuadro.disconnect(self.draw_QuadroPoint)
            self.oItem.lastItemDone.disconnect(self.oCoilVerification.pause)
            self.recived.disconnect(self.oCoilVerification.process_data)
            self.oCoilVerification.TermsSwithLoad.disconnect(self.swith_load)
        
        self.oCoilVerification = CoilVerification(self.env, self.adStandInfo, self.oItem.iItemID,  _iCoilID.toInt()[0])
        
        self.oPointGrid.show_point_grid(self.oCoilVerification.oGOST.get_point_list())
        self.oCoilVerification.PointFound.connect(self.draw_point)
#        self.oCoilVerification.worked.connect(self.oMap.start)
        self.oCoilVerification.paused.connect(self.full_refresh)
        self.oCoilVerification.worked.connect(self.button_refresh)
        self.oCoilVerification.PointErrorAngular.connect(self.draw_point_angular_error)
        self.oCoilVerification.PointErrorCurrent.connect(self.draw_point_current_error)
        self.oCoilVerification.PointError.connect(self.draw_point_error)
        self.oCoilVerification.proggress.connect(self.draw_proggress)
        self.oCoilVerification.PointLeft.connect(self.draw_point_left)
        self.oCoilVerification.PointRight.connect(self.draw_point_right)
        self.oCoilVerification.PointOut.connect(self.oCoil.set_done)
        self.oCoilVerification.CoilDone.connect(self.draw_coil_done)
        self.oCoilVerification.PointEmpty.connect(self.draw_coil_empty)
#        self.oCoilVerification.NeedCurrentOff.connect(self.draw_needCurrentOff)
        self.oCoilVerification.PointQuadro.connect(self.draw_QuadroPoint)
        self.oItem.lastItemDone.connect(self.oCoilVerification.pause)
        self.recived.connect(self.oCoilVerification.process_data)
        self.oCoilVerification.TermsSwithLoad.connect(self.swith_load)
        
        self.ui.tvCoil.set_row_by_key(_iCoilID)
        
        self.cheking_refresh()
        #Переключения при смене обмотки
        if prevStateWork and not self.oCoilVerification.is_done():
            self.oCoilVerification.work()
        elif prevStateWork and self.oCoilVerification.is_done(): #TODO: Подозрительное место, была ошибка с рекурсией - падала прога изза рекурсивного сигнала setRow
            self.oCoilVerification.pause()
            
#        self.oCoilVerification.prepared()

    def start_set_enable(self, _bEnable):
        u"""_bEnable - не гарантирует блокировку, при испытании не заблокируется. И не гарантирует разблокировку, если нелзя тестировать обмотку"""
        self.ui.btnStart.setEnabled(bool(
                                    self.is_work() #Если идет испытание - всегда кнопка доступна
                                    or (
                                        _bEnable #Принудительное отключение, иногда надо обязательно блокировать(к примеру при подъеме диалогов)
#                                        and (self.oItem and self.oItem.stateItem != self.oItem.DONE) #Есть трансформатор и он не испытан
                                        and (self.oCoil and self.oCoil.is_ready()) #Есть обмотка и она готова к испытанию
#                                        and (self.oCoilVerification and not self.oCoilVerification.is_done())
                                        )
                                    ))
        self.ui.btnStart.setChecked(self.is_work())
            
        

# Служеьные слоты ################################################
    @pyqtSlot()
    def button_refresh(self):
        #    NOMAP = u'No test map'
        #    EMPTY = u'Empty test map'
        #    FULL = u'In test map exist item'
        #    DONE = u'Test map done testing'
        #    TESTING = u'Testing in progress'
        
        if self.oMap.stateMap == self.oMap.NOMAP:
            self.ui.btnNewMap.setEnabled(False)
#            self.start_set_enable(False)
            self.ui.tvItem.setEnabled(True)
            self.ui.tvCoil.setEnabled(False)
            self.ui.btnQuit.setEnabled(True)
            self.ui.btnTester.setEnabled(True)
            self.ui.btnAssistant.setEnabled(True)
            self.ui.btnSupervisor.setEnabled(True)
            self.ui.btnSupervisorReport.setEnabled(True)
            self.ui.btnCheckReport.setEnabled(True)
            self.ui.btnTicketMatrix.setEnabled(True)
            self.ui.btnTestType.setEnabled(True)
            #self.ui.btnDevices.setEnabled(True)            
        elif self.oMap.stateMap in (self.oMap.EMPTY, self.oMap.FULL, self.oMap.DONE):
            self.ui.btnNewMap.setEnabled(True)
#            self.start_set_enable(True)
            self.ui.tvItem.setEnabled(True)
            self.ui.tvCoil.setEnabled(True)
            self.ui.btnQuit.setEnabled(True)
            self.ui.btnTester.setEnabled(True)
            self.ui.btnAssistant.setEnabled(True)
            self.ui.btnSupervisor.setEnabled(True)
            self.ui.btnSupervisorReport.setEnabled(True)
            self.ui.btnCheckReport.setEnabled(True)
            self.ui.btnTicketMatrix.setEnabled(True)
            self.ui.btnTestType.setEnabled(False)
            #self.ui.btnDevices.setEnabled(False)
            
#        elif self.oMap.stateMap == self.oMap.TESTING:
        if self.is_work():
            self.ui.btnNewMap.setEnabled(False)
#            self.ui.btnStart.setEnabled(True)
            self.ui.tvItem.setEnabled(False)
            self.ui.tvCoil.setEnabled(False)
            self.ui.btnQuit.setEnabled(False)
            self.ui.btnTester.setEnabled(False)
            self.ui.btnAssistant.setEnabled(False)
            self.ui.btnSupervisor.setEnabled(False)
            self.ui.btnSupervisorReport.setEnabled(False)
            self.ui.btnCheckReport.setEnabled(False)
            self.ui.btnTicketMatrix.setEnabled(False)
            self.ui.btnTestType.setEnabled(False)
            #self.ui.btnDevices.setEnabled(False)
            

            #tam
            #self.oTestCoil.setVisible(True)
        
            
        #tam        
        if not self.ui.frVerification.isVisible(): #Чтобы случайно не запустили тестирование когда не видно панеле верификации 
#        if not self.ui.frVerification.isVisible() and not self.oTestCoil.isVisible(): #Чтобы случайно не запустили тестирование когда не видно панеле верификации
            self.start_set_enable(False)
        else:
            if self.oTestCoil.isWork : #tam
                return
            self.start_set_enable(True)


        '''
        if not self.ui.frVerification.isVisible(): #Чтобы случайно не запустили тестирование когда не видно панеле верификации 
            print 'knur5' 
            self.start_set_enable(False)
            print 'knur6' 
        else:
            print 'knur7' 
            self.start_set_enable(True)
            print 'knur8' 
       '''

    @pyqtSlot()
    def view_refresh(self):
        self.view_item_refresh()
        self.view_coil_refresh()
        
    @pyqtSlot()
    def full_refresh(self):
        self.view_refresh()
        self.button_refresh()

    def view_item_refresh(self):
        self.ui.tvItem.refresh()
        self.ui.tvItem.setEnabled(not self.is_work()) 
        if 0 == self.ui.tvItem.get_row():
            self.ui.tvItem.set_row(1)
        self.item_view_button_refresh()
        #msgBox(self, u"view_item_refresh")

    def view_coil_refresh(self):
        self.ui.tvCoil.refresh()
        self.ui.tvCoil.setEnabled(bool(self.oItem and self.oItem.iItemID) and (not self.is_work()))
        self.coil_view_button_refresh()
        
    def cheking_refresh(self):
        self.oPointGrid.clear()
        self.ui.lState.setPalette(self.normalPalette)
        self.ui.lState.setText(u'Нет обмотки')
        self.oCoilVerification.fill_existing_points()
        self.coil_view_button_refresh()
    
    def item_view_button_refresh(self):
        self.btnItemDelete.setEnabled(bool(self.oItem and self.oItem.iItemID and self.oItem.able_delete()))
        self.btnItemSetDefect.setEnabled(bool(self.oItem and self.oItem.iItemID))

    def coil_view_button_refresh(self):
        self.btnCoilClear.setEnabled(bool(self.oCoil and self.oCoil.iCoilID and self.oCoil.stateCoil != self.oCoil.NOTESTE))
        self.btnCoilErrorClear.setEnabled(bool(self.oCoil and self.oCoil.iCoilID and self.oCoil.stateCoil != self.oCoil.NOTESTE and self.errorPointIndex != None))
        
        #tam
        #print 'coil_view_button_refresh'
        if self.codeTypeTest in [3,4] and self.oTestCoil.points != None:
            self.btnCoilClear.setEnabled(len(self.oTestCoil.points) > 0)


    def hide_serial_find(self):
        self.oDlgSerialNumber.setVisible(False)
        self.oKeyboard.setVisible(False)
        # 6.12.2016 self.ui.frCoil.setVisible(True)
        self.ui.frVerification.setVisible(True)
        
        
        #02.2021
        #getTrue(self, str(self.oMap.iMapID) + '  ' + str(self.oMap.iStandID))
        #self.oMap.iMapID
        #self.oMap.iStandID
        
        
        
        
        print 'self.codeTypeTest2=', self.codeTypeTest
        #tam

        # 6.12.2016
        if self.codeTypeTest not in [7]:
            self.ui.frCoil.setVisible(True)
        
        if self.codeTypeTest in [3,4,7]:
            if self.codeTypeTest in [3,4]:
                self.ui.btnStickers.setEnabled(True)
                self.ui.btnInfo.setEnabled(True)
                self.oTestCoil.setVisible(True)
                #14.11.2016 перенес в "map_select"
                #пока вернул назад
                self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True)
                print 'calcGlobal                     222222222222222222222222222222'
#tam 2.12.2016            
            if self.codeTypeTest in [7]:
                self.ui.frPointList.setVisible(False)
                self.ui.frInfo.setVisible(False)
                # 7.12.2016
                self.oTestHighVoltage.setVisible(True)
                self.ui.label_12.setVisible(False)
                self.ui.pbPrimaryCurrent.setVisible(False)
        else:            
            self.ui.frPointList.setVisible(True)
            self.ui.frInfo.setVisible(True)
            self.ui.label_12.setVisible(True)
            self.ui.pbPrimaryCurrent.setVisible(True)
            
        
        self.button_refresh()
            
    def show_serial_find(self):
        self.ui.frCoil.setVisible(False)
        self.ui.frVerification.setVisible(False)
        
        #tam
        self.ui.btnStickers.setEnabled(False)
        self.ui.btnInfo.setEnabled(False)
        self.oTestCoil.setVisible(False)
        # 7.12.2016
        self.oTestHighVoltage.setVisible(False)
                
        self.oDlgSerialNumber.setVisible(True)
        self.oKeyboard.setVisible(True)
        self.button_refresh()
        
    def set_visible_simple_choice(self, _bEnabled):
        self.oDlgChoice.setVisible(_bEnabled)
        self.set_enabled_main_frames(not _bEnabled)
        
    def set_visible_climat(self, _bEnabled):
        self.oDlgClimat.setVisible(_bEnabled)
        self.set_enabled_main_frames(not _bEnabled)
        
    def set_enabled_main_frames(self, _bEnabled):
        self.ui.frKNT.setVisible(_bEnabled)
        self.ui.frView.setVisible(_bEnabled)
        self.ui.frButton.setVisible(_bEnabled)
        if _bEnabled:
            self.button_refresh()
        else:
            self.ui.btnNewMap.setEnabled(False)
            self.ui.btnAssistant.setEnabled(False)
            self.ui.btnTester.setEnabled(False)
            self.ui.btnSupervisor.setEnabled(False)
            self.ui.btnTestType.setEnabled(False)
            #self.ui.btnDevices.setEnabled(False)
            

        
# Вызов диалогов ################################################

    @pyqtSlot()
    def msg_item_dublicate(self):
        msgBox(self, u'Такой трансформатор уже есть на тележке')

    @pyqtSlot()
    def msg_item_full(self):
        msgBox(self, u'Трансформатор не пустой или с дефектом\n очистите перед удалением')

    @pyqtSlot()
    def exit(self):
        if getTrue(self, u'Выйти из программы?') and self.map_close():
            try:
                self.scan.disconnect(self.scan_slot)
                self.scanner.SetEnabled(False)
            except:
                pass

            try:
                self.oKNT05.SetEnabled(False)
            except:
                pass


            try:
                #Сохранение в config.json состояния галочек
#                print(u'Сохранение в config.json состояния галочек')
                f = open('config.json','r')
#                print 1
                dataConfig = json.load(f)
#                print 2
#                print dataConfig

    
#                dataConfig['verification'] = {'autoCA5018': self.ui.checkBox.isChecked(), 'autoPR200': self.ui.checkBox_2.isChecked()}                                   
                #30.06.2020               
#                dataConfig['verification'] = {'autoCA5018': self.ui.autoCA5018.isChecked(), 'autoPR200': self.ui.autoPR200.isChecked()}   
                #13.07.2020               
                dataConfig['verification'] = {'autoTest': self.ui.autoTest.isChecked(), 'autoCA5018': self.ui.autoCA5018.isChecked(), 'autoPR200': self.ui.autoPR200.isChecked()}   
                                
                
#                print 2
#                print dataConfig    
#                print 4                
                f = open('config.json','w')
                json.dump(dataConfig, f, indent=4, sort_keys=False)
#                print 5
            except:
                pass


            
            self.done(1)
    
    #tam
    def closeEvent(self, event):
        return
        if self.codeTypeTest in [3,4]:
            self.oTestCoil.closeEvent()    
    
    
    @pyqtSlot()
    def get_tester(self):
        sSql = u"""
                select 
                    id
                    , fio 
                from 
                    operator 
                where 
                    not isexternal 
                    and not isdismiss 
                    and exists(
                        select id from stand_user 
                        where stand_user.operator = operator.id and stand_user.stand = {0}
                        )
                ;""".format(self.adStandInfo.ID)
        self.oDlgChoice.set_query(sSql, u'ID', self.oMap.iTesterID)
        self.ui.btnTester.setChecked(True)
        self.set_visible_simple_choice(True)
        self.oDlgChoice.choice.connect(self.set_tester)
        
        #tam ВРЕМЕННО        
        #self.move(300,0)
        #self.setMaximumHeight(850)
        
            
    @pyqtSlot()
    def get_assistant(self):
        sSql = u"""
                select 
                    id
                    , fio 
                from 
                    operator 
                where 
                    not isexternal 
                    and not isdismiss 
                    and exists(
                        select id from stand_user 
                        where stand_user.operator = operator.id and stand_user.stand = {0}
                        )
                union all
                select Null, 'Без ассистента' 
                ;""".format(self.adStandInfo.ID)
        self.oDlgChoice.set_query(sSql, u'ID', self.oMap.iAssistantID)
        self.ui.btnAssistant.setChecked(True)
        self.set_visible_simple_choice(True)
        self.oDlgChoice.choice.connect(self.set_assistant)

    @pyqtSlot()
    def get_supervisor(self):
        sSql = u"""
                select id, fio from operator where (isexternal or isSupervisor) and not isdismiss
                /*union all
                select Null, 'Без поверителя ЦСМ'*/
                ;"""
        self.oDlgChoice.set_query(sSql, u'ID', self.oMap.iSupervisorID)
        self.ui.btnSupervisor.setChecked(True)
        self.set_visible_simple_choice(True)
        self.oDlgChoice.choice.connect(self.set_supervisor)

    @pyqtSlot()
    def get_defect(self):
        #tam
        '''        
        sSql = "select id, fullname from defect where defecttype=\'1\'" 
        if self.codeTypeTest in [3,4]:
            sSql = "select id, fullname from defect where defecttype=\'2\'" 
        if self.codeTypeTest in [7]:
            sSql = "select id, fullname from defect where defecttype=\'7\'" 
        sSql = "select id, fullname from defect" 
        '''
        #tam 16.11.2022
        sSql = '''
select id, fullname from defect    
where id in 
(
    select defect from defect_test_type where test_type in 
    (
        select id from test_type where code = ''' + str(self.codeTypeTest) + '''
    )
)        
'''
        
        sSql += u"""
                union all
                select Null as id, 'Без ошибок' as fullname 
                order by
                    fullname                    
                ;"""
        self.oDlgChoice.set_query(sSql, u'ID', None)
        self.set_visible_simple_choice(True)
        self.oDlgChoice.choice.connect(self.set_defect)

    @pyqtSlot()
    def get_climat(self):
        if not self.oMap.iTesterID:
            return
        self.oDlgClimat.set_operator(self.oMap.iTesterID)
        self.set_enabled_main_frames(False)
        self.oDlgClimat.setVisible(True)
        
    @pyqtSlot()
    def get_test_type(self):
        sSql = u"""
                select
                    id
                    , fullname
                from
                    stand
                where
                    hostname = '{0}'
                    """.format(socket.gethostname())
        self.oDlgChoice.set_query(sSql, u'ID', self.adStandInfo.ID if self.adStandInfo != None else None)
        self.ui.btnTestType.setChecked(True)
        self.set_visible_simple_choice(True)
        self.oDlgChoice.choice.connect(self.set_test_type)


# Обработка ответов от диалогов ################################################
#TODO: Слишком сложно....
    @pyqtSlot(u'QVariant')
    def set_tester(self, _iOperatorID):
        if _iOperatorID.toInt()[1]: 
            iOperatorID = _iOperatorID.toInt()[0]
        else: 
            iOperatorID = None
        
        if not self.oMap.iTesterID and not iOperatorID:
            msgBox(self, u'Для дальнейшей раброты необходимо указать испытателя.')
            return 
        
        self.oDlgChoice.choice.disconnect(self.set_tester)
        self.ui.btnTester.setChecked(False)
        self.set_visible_simple_choice(False)
        self.oMap.tester_select(iOperatorID)
        
    @pyqtSlot(u'QVariant')
    def set_assistant(self, _qvOperatorID):
        self.oDlgChoice.choice.disconnect(self.set_assistant)
        self.ui.btnAssistant.setChecked(False)
        self.set_visible_simple_choice(False)
        self.oMap.asistant_select(_qvOperatorID)
        
    @pyqtSlot(u'QVariant')
    def set_supervisor(self, _qvOperatorID):
        if _qvOperatorID.toInt()[1]:
            iOperatorID = _qvOperatorID.toInt()[0]
        else:
            iOperatorID = None

        if not self.oMap.iSupervisorID and not iOperatorID:
            msgBox(self, u'Для дальнейшей раброты необходимо указать поверителя.')
            return
            
        '''
        self.oDlgChoice.choice.disconnect(self.set_supervisor)
        self.ui.btnSupervisor.setChecked(False)
        self.set_visible_simple_choice(False)
        self.oMap.supervisor_select(iOperatorID)
        '''
        
        #9.04.2018
        self.oDlgChoice.choice.disconnect(self.set_supervisor)
        self.ui.btnSupervisor.setChecked(False)
        self.set_visible_simple_choice(False)
        self.oMap.supervisor_select(_qvOperatorID)
        
        
    @pyqtSlot(u'QVariant')
    def set_defect(self, _qvDefectID):
        self.oItem.set_defect(self.oItem.iItemID, _qvDefectID)
        self.oDlgChoice.choice.disconnect(self.set_defect)
        self.set_visible_simple_choice(False)
        if self.codeTypeTest in [3,4]:
            if self.oTestCoil.recalcTesting():
                self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True)
                print 'calcGlobal                     333333333333333333333333333333'
                

    @pyqtSlot(int)
    def set_climat(self, _iClimatID):
        self.oDlgClimat.setVisible(False)
        self.set_enabled_main_frames(True)
        self.oMap.iClimatID = _iClimatID
        
    def show_error_confirmation(self, _I ,_angularError, _currentError):
        sMsg = u'Превышение'
        if _angularError:
#            sMsg = sMsg + u" угловой погрешности на " + unicode(_angularError) + u"'"
            sMsg = sMsg + u' угловой погрешности'
        if _currentError:
#            sMsg = sMsg + u' токовой погрешности на ' + unicode(_currentError) + u'%' 
            sMsg = sMsg + u' токовой погрешности' 
        sMsg = sMsg + u'\nв точке ' + unicode(int(round(_I))) + u'% \nПовторить испытание?'
        if getTrue(self, sMsg):
            self.coil_clear()
        else:
            self.get_defect()


    @pyqtSlot(u'QVariant', u'QString')
    def set_test_type(self, _iStandID):
        iStandID = None
        if _iStandID.toInt()[1]:
            iStandID = _iStandID.toInt()[0]

        if not iStandID:
            msgBox(self, u'Укажите тип испытания.')
            return
        self.set_visible_simple_choice(False)
        self.oDlgChoice.choice.disconnect(self.set_test_type)
        self.apply_test_type(iStandID)


    def apply_test_type(self, _iStandID):
        adStandInfoOld = self.adStandInfo
        self.adStandInfo = self.oHelpStand.get_info(_iStandID)
        
        #tam
        self.codeTypeTest = self.oTestCoil.code_type_test(self.adStandInfo.ID)
        
        # 6.12.2016
        self.ui.frCoil.setVisible(self.codeTypeTest not in [7])
        
        print 'self.codeTypeTest1=', self.codeTypeTest
        self.ui.btnMsr.setVisible(True)
        if self.codeTypeTest in [3,4,7]:
#            self.ui.btnMsr.setVisible(True)
            self.ui.frPointList.setVisible(False)
            if self.codeTypeTest in [3,4]:
                self.ui.btnDevices.setVisible(True)
                # 7.12.2016
                self.oTestHighVoltage.setVisible(False)
                self.oTestCoil.setVisible(True)
                self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True)
                print 'calcGlobal                     444444444444444444444444444444'
                self.ui.vlInfo.removeItem(self.VSpacer)
                self.oTestCoil.clear()
                        
                # Восстанавливаем полноэкранный режим, нарушаемый командой 'self.oTestCoil.setVisible(True)'
                if self.env.winparam.fullscreen:
                    self.setWindowState(Qt.WindowFullScreen)
                        
                self.ui.frInfo.setVisible(True)
                self.ui.label_12.setVisible(True)
                self.ui.pbPrimaryCurrent.setVisible(True)
                                                
            #self.Devices = Devices(self.env)
            #print 2, self.Devices.data
            #tam 2.12.2016            
            if self.codeTypeTest in [7]:
                self.oTestCoil.setVisible(False)
                # 7.12.2016
                self.oTestHighVoltage.setVisible(True)
                self.ui.frInfo.setVisible(False)
                self.ui.label_12.setVisible(False)
                self.ui.pbPrimaryCurrent.setVisible(False)
                self.ui.vlInfo.addItem(self.VSpacer)
#            self.ui.frVerification.setVisible(False)
        else:            
            self.ui.frPointList.setVisible(True)
            self.ui.btnDevices.setVisible(False)
            self.oTestCoil.setVisible(False)
            # 7.12.2016
            self.oTestHighVoltage.setVisible(False)
            
            self.ui.vlInfo.addItem(self.VSpacer)
            self.ui.frInfo.setVisible(True)
            self.ui.label_12.setVisible(True)
            self.ui.pbPrimaryCurrent.setVisible(True)

                                        
                
        # self.oDlgChoice.choice.disconnect(self.set_test_type)
        self.ui.btnTestType.setChecked(False)

        # Применяем параметры видимости для данного стенда
        self.ui.btnAssistant.setVisible(self.adStandInfo.EnableAssistant)
        self.ui.btnSupervisor.setVisible(self.adStandInfo.EnableSupervisor)
        self.ui.btnSupervisorReport.setVisible(self.adStandInfo.SupervisorReport)
        self.ui.btnCheckReport.setVisible(self.adStandInfo.CheckReport)
        self.ui.btnTicketMatrix.setVisible(self.adStandInfo.TicketMatrix)
        ###self.ui.btnTicketMatrix.setVisible(True)
#        self.ui.btnAccountReport.setVisible(False)
#        self.ui.btnAccountReport.setVisible(self.codeTypeTest in [3,4])
        #TAM
###        self.ui.btnStickers.setVisible(self.codeTypeTest in [3,4])
        self.ui.btnInfo.setVisible(self.codeTypeTest in [3,4])
        
        self.ui.lState.setVisible(self.codeTypeTest not in [3,4])
        self.ui.pbPrimaryCurrent.setVisible(self.codeTypeTest not in [3,4])
        self.ui.pbPrimaryCurrent.setVisible(self.codeTypeTest not in [3,4])
        
        self.ui.label_12.setVisible(self.codeTypeTest not in [3,4])
        self.ui.label_4.setVisible(self.codeTypeTest not in [3,4])
        self.ui.label_5.setVisible(self.codeTypeTest not in [3,4])
        self.ui.label_6.setVisible(self.codeTypeTest not in [3,4])
        self.ui.label_10.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbLabelKTrans.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbSerialNumber.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbKTrans.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbClassAccuracy.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbSecondLoad.setVisible(self.codeTypeTest not in [3,4])
        self.ui.lbTap.setVisible(self.codeTypeTest not in [3,4])
        
#        self.ui.checkBox.setVisible(self.codeTypeTest not in [3,4])
#        self.ui.checkBox_2.setVisible(self.codeTypeTest not in [3,4])
#        self.ui.checkBox.clicked.connect(self.checkBox_Click)
#        self.ui.checkBox_2.clicked.connect(self.checkBox_2_Click)        
        #30.06.2020               
        self.ui.autoTest.setVisible(self.codeTypeTest not in [3,4])
        self.ui.autoCA5018.setVisible(self.codeTypeTest not in [3,4])
        self.ui.autoPR200.setVisible(self.codeTypeTest not in [3,4])
        self.ui.autoTest.clicked.connect(self.autoTest_Click)
        self.ui.autoCA5018.clicked.connect(self.checkBox_Click)
        self.ui.autoPR200.clicked.connect(self.checkBox_2_Click)
        self.ui.checkBox.setVisible(False)
        self.ui.checkBox_2.setVisible(False)
        self.ui.lineEdit.setVisible(False)
        self.ui.lineEdit_2.setVisible(False)



                
        #self.ui..setVisible(self.codeTypeTest not in [3,4])
        #QMessageBox.warning(self, u"Предупреждение",  "qwe", QMessageBox.Ok)
        
        
                
        if(self.adStandInfo.useAmpereTurn):
            self.ui.lbLabelKTrans.setText(u'Ампер-витки')
        else:
            self.ui.lbLabelKTrans.setText(u'Коэф. транс.')

        if(adStandInfoOld == None or adStandInfoOld.ID != self.adStandInfo.ID):
            self.oDlgClimat.setRoom(self.adStandInfo.Room) #Ужасный костыль, убрать потом. Надо привязывать помещение к компьютеру, а не к раб. месту как сейчас
            self.oMap.set_up(self.adStandInfo)
            self.ui.btnTestType.setText(unicode(self.adStandInfo.FullName))
            if(self.oMap.iTesterID == None):
                self.ui.btnTester.setText(u'Испытатель:\n')
            if(self.oMap.iSupervisorID == None):
                self.ui.btnSupervisor.setText(u'Поверитель:\n')
            if(self.oMap.iAssistantID == None):
                self.ui.btnAssistant.setText(u'Ассистент:\n')


# Установка значений на элементах окна (приходят сигналы от логики) ############
#TODO: Слишком сложно....
    # @pyqtSlot(int, str)
    # def testtype_apply(self, _iTesterID, _testName):
    #     self.ui.btnTester.setText(u'Тип испытания:\n%s' % unicode(_testName))

    @pyqtSlot(int, str)
    def tester_apply(self, _iTesterID, _sFIO):
        self.ui.btnTester.setText(u'Испытатель:\n%s' % unicode(_sFIO))
    
    @pyqtSlot(int, str)
    def assistant_apply(self, _iTesterID, _sFIO):
        self.ui.btnAssistant.setText(u'Ассистент:\n%s' % unicode(_sFIO))
    
    @pyqtSlot(int, str)
    def supervisor_apply(self, _iTesterID, _sFIO):
        self.ui.btnSupervisor.setText(u'Поверитель:\n%s' % unicode(_sFIO))

# Отображение процесса верификации
    def swith_load(self, _fSecondLoad):
#        print 'swith_load(self, _fSecondLoad)   swith_load(self, _fSecondLoad)   swith_load(self, _fSecondLoad)'
        self.ui.lbSecondLoad.setText(unicode(_fSecondLoad))
######################        self.checkBox_Click()        
#####################        self.checkBox_2_Click()
        #05.2020
#        QMessageBox.warning(self, u"РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ",  unicode(_fSecondLoad), QMessageBox.Ok)
        print "self.ui.lbSecondLoad.text()*************  self.ui.lbSecondLoad.text() = ", self.ui.lbSecondLoad.text() 
        print self.info.SecondCurrent            
#        self.Devices_.WriteToCA5018(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)

        
#        16.06.2020
###30        self.ui.lineEdit.setText(self.ui.lineEdit.text() + "%" + self.ui.lbSecondLoad.text())
        if self.is_work():
            if self.codeTypeTest not in [3,4]:                
                if self.env.config.devices.ca5020.active:
                    if self.ui.autoCA5018.isChecked(): 
                        if self.ui.lbSecondLoad.text() != '':
# 11.10.2021                            if self.lastSecondLoad != float(self.ui.lbSecondLoad.text()) and self.lastSecondCurrent != self.oCoilVerification.info.SecondCurrent:
                            if self.lastSecondLoad != float(self.ui.lbSecondLoad.text()) or self.lastSecondCurrent != self.oCoilVerification.info.SecondCurrent:
                                self.Devices_.WriteToCA5020(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)
                                self.lastSecondLoad = float(self.ui.lbSecondLoad.text())
                                self.lastSecondCurrent = self.oCoilVerification.info.SecondCurrent
                else:        
                    #30.06.2020
                    if self.ui.autoCA5018.isChecked():
                        if self.ui.lbSecondLoad.text() != '':
                            if self.lastSecondLoad != float(self.ui.lbSecondLoad.text()):
                                self.Devices_.WriteToCA5018(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)
                                self.lastSecondLoad = float(self.ui.lbSecondLoad.text())
###30                            self.ui.lineEdit_2.setText(self.ui.lineEdit_2.text() + "%" + self.ui.lbSecondLoad.text())
                    
           
           
                        
        '''             
                if self.ui.checkBox_2.isChecked():
###                    self.Devices_.WriteToPR200(514, 1)
                    self.WriteToPR200(self.info)       
           '''             
                     
    def autoTest_Click(self):
        #tam
        if self.codeTypeTest not in [3,4]:
        #15.07.2020
            if self.ui.autoTest.isChecked():
#                print 1
                self.Devices_.WriteToPR200(515, 1)
            else:      
#                print 2      
                self.Devices_.WriteToPR200(515, 0)
            #20.07.2020   ???????????????????????????????????????????????????
            if self.ui.autoPR200.isChecked():
                self.WritePointToPR200(0)                
                     
                                          
    def checkBox_Click(self):
        #tam
####        if self.is_work(): добавить, чтобы сигналы посылались только в момент испытания
        '''
        if self.codeTypeTest not in [3,4]:
            if self.ui.checkBox.isChecked():
                if self.ui.lbSecondLoad.text() != '':
                    self.Devices_.WriteToCA5018(float(self.ui.lbSecondLoad.text()))
'''


    def checkBox_2_Click(self):
        #tam
        if self.codeTypeTest not in [3,4]:
            
#            if self.ui.checkBox_2.isChecked():
#                self.Devices_.WriteToPR200(514, 1)
#            else:            
#                self.Devices_.WriteToPR200(514, 0)
        #30.06.2020
            if self.ui.autoPR200.isChecked():
                self.Devices_.WriteToPR200(514, 1)
            else:            
                self.Devices_.WriteToPR200(514, 0)
                       


        

    def show_item_info(self, _iItemID):
        if _iItemID:
            itemInfo = self.oHelpItem.get_fields(_iItemID)
            snInfo = self.oHelpSerial.get_info(itemInfo.serial_number)
            self.ui.lbSerialNumber.setText(unicode(snInfo.serialnumber) or u'')
                        
            #16.07.2020 ставим на паузу после каждого трансформатора
            if self.is_work():
                if self.codeTypeTest not in [3,4]:
                    if self.ui.autoTest.isChecked():
                        self.ui.btnStart.click()
                        
        else:
            self.ui.lbSerialNumber.clear()

    def show_coil_info(self, _coilID):
        u""""""
    #    print "show_coil_info"
        if _coilID.isNull():
            self.ui.lbShortName.clear()
            self.ui.lbKTrans.clear()
            self.ui.lbSecondLoad.clear()
            self.ui.lbClassAccuracy.clear()
            self.ui.lbTap.clear()
            self.ui.lbSerialNumber.clear()
        else:
            info = self.oHelpCoil.get_check_terms(_coilID)
            self.info = info
            self.ui.lbShortName.setText(info.ShortName)
            if(self.adStandInfo.useAmpereTurn):
                self.ui.lbKTrans.setText(unicode(info.AmpereTurn))
            else:
                self.ui.lbKTrans.setText(unicode(info.PrimaryCurrent) + u'/' + unicode(info.SecondCurrent))
            self.ui.lbClassAccuracy.setText(info.ClassAccuracy)
            self.ui.lbTap.setText(
                                  unicode(info.CoilNumber) + u'И1'
                                  + u'-' 
                                  + unicode(info.CoilNumber) + u'И' + unicode(info.Tap)
                                  ) 
###????????????            if self.is_work():
###????????????                self.WriteToPR200(self.info)       
#            info.CoilNumber

            print "self.ui.lbSecondLoad.text() = self.ui.lbSecondLoad.text() = self.ui.lbSecondLoad.text() = ", self.ui.lbSecondLoad.text()
            print "info.SecondCurrent = ", info.SecondCurrent

            if self.is_work():
                if self.codeTypeTest not in [3,4]:
                    '''  вернул назад в swith_load              
                    if self.ui.checkBox.isChecked():
                        if self.ui.lbSecondLoad.text() != '':
                            self.Devices_.WriteToCA5018(float(self.ui.lbSecondLoad.text()))
                    '''
                                                                        
#                    if self.ui.checkBox_2.isChecked():
#                        self.WriteToPR200(self.info)       
                    #30.06.2020
                    if self.ui.autoPR200.isChecked():
                        self.WriteToPR200(self.info)       


#                    #16.07.2020
#                    if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
#                        self.WritePointToPR200(0)                


                    #16.07.2020 ставим на паузу после каждой обмотки
                    if self.ui.autoTest.isChecked() and not self.ui.autoCA5018.isChecked():
                        self.ui.btnStart.click()



    def WriteToPR200(self, info):
        print 'info.primarycurrent = ', info.PrimaryCurrent
        print 'info.secondcurrent = ', info.SecondCurrent
        if info == None:
            return
        
# 19.10.2020        
#        self.Devices_.WriteToPR200(512, info.PrimaryCurrent)

###        if self.codeTypeTest in [0] and info.AmpereTurn != None:
        if self.adStandInfo.useAmpereTurn:
            self.Devices_.WriteToPR200(512, info.AmpereTurn)
        else:    
            self.Devices_.WriteToPR200(512, info.PrimaryCurrent)
        
                
        self.Devices_.WriteToPR200(513, info.SecondCurrent)
        self.Devices_.WriteToPR200(516, info.CoilNumber)
                
    def WriteToPR200_zero(self):
        # Обнуление на ПР200 первичного тока и номера обмотки (используется при переходе на другой транс во время испытания)
        self.Devices_.WriteToPR200(512, 0)        
        self.Devices_.WriteToPR200(516, 0)
                
            

    def draw_proggress(self, _I, _A, _P):
        self.ui.pbPrimaryCurrent.setValue(_I)
        self.ui.pbPrimaryCurrent.setValue(_I)

    def draw_QuadroPoint(self):
        #TODO: Похоже панель верификации надо переносить в отдельный модуль, связанный с app/verification.py
        self.ui.lState.setPalette(self.normalPalette)
        quadroLoad = self.oCoilVerification.oGOST.get_point_by_index(self.oCoilVerification.pointIndex).quadroLoad
        if quadroLoad:
            sMessage = u'Установите 1|4 нагрузки ' + unicode(quadroLoad)
            self.ui.lState.setText(sMessage)

            #16.07.2020
            if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
                self.WritePointToPR200(0)                
                if not self.ui.autoCA5018.isChecked():
                    self.ui.btnStart.click()
                

    def draw_needCurrentOff(self):
        pass
        #TODO: Похоже панель верификации надо переносить в отдельный модуль, связанный с app/verification.py
#        self.ui.lState.setPalette(self.normalPalette)
#        quadroLoad = self.oCoilVerification.oGOST.get_point_by_index(self.oCoilVerification.pointIndex).quadroLoad
#        if quadroLoad:
#            sMessage = u'Установите 1|4 нагрузки ' + unicode(quadroLoad)
#            self.ui.lState.setText(sMessage)

    def draw_point_left(self, _I, _isGuadroLoad):
        self.sound.stop_loop()
        self.ui.lState.setPalette(self.normalPalette)
        quadroLoad = self.oCoilVerification.oGOST.get_point_by_index(self.oCoilVerification.pointIndex).quadroLoad
        if quadroLoad:
            self.ui.lState.setText(u'Поиск точки 1|4')
                
            #16.07.2020
            if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
                self.WritePointToPR200_(_I)  #четвертная            
#                self.WritePointToPR200(7)  #четвертная            
#???                if not self.ui.autoCA5018.isChecked():
#???                    self.ui.btnStart.click()
                                                        
        else:
            self.ui.lState.setText(u'Поиск точки ' + unicode(_I) + u'%')
            self._I_old = _I

            #16.07.2020
            if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
                self.WritePointToPR200_(_I)

#TODO:Надо ли отображать?        self.ui.lState.setText(u'Поиск точки %s' % self.get_pint_stringID())

    def draw_point_right(self, _I, _isGuadroLoad):
        self.ui.lState.setPalette(self.alarmPalette)
        self.ui.lState.setText(u'Пропущена точка ' + unicode(_I) + u'%')
        if self.is_work():
            self.sound.play_loop(self.env.config.snd_notify.point_skipped)
        
    def draw_point(self, _pointIndex, _I, _P, _A, _isQuadroLoad):
        print 'D R A W _ P O I N T'
        self.oPointGrid.set_point_record(_pointIndex, True, None, _P, _A)
#        self.ui.lState.setPalette(self.normalPalette)
#        self.ui.lState.setText(u'Точка найдена!')
        if self.is_work() and _pointIndex == self.oCoilVerification.pointIndex:
            self.sound.play(self.env.config.snd_notify.point_found)
            
            
            #16.07.2020
            # Перенес в draw_point_left 
            #if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
            #    self.WritePointToPR200(_pointIndex)
        

        
    def WritePointToPR200(self, _pointIndex):
        points = {0: 0, 1: 1, 2: 5, 3: 20, 4: 50, 5: 100, 6: 120, 7:120}
        print 'points[_pointIndex]', points[_pointIndex]
        self.Devices_.WriteToPR200(517, points[_pointIndex])
        
    def WritePointToPR200_(self, perc):
        self.Devices_.WriteToPR200(517, perc)
        
        
        
        
        
        
#    def point_error(self, _pointIndex, _I, _P, _A, _isQuadroLoad):
#        self.ui.lState.setPalette(self.alarmPalette)
#        self.ui.lState.setText(u'Ошибка!')
#        if self.oMap.stateMap == self.oMap.TESTING:
#            self.sound.play(self.env.config.snd_notify.point_error)

    def draw_coil_empty(self):
        self.ui.lState.setPalette(self.normalPalette)
        self.ui.lState.setText(u'Готов к работе')
        
            
    def draw_coil_done(self):
        self.ui.lState.setPalette(self.donePalette)
        self.ui.lState.setText(u'Все точки найдены')
        if self.is_work():
            self.sound.play(self.env.config.snd_notify.coil_done)
            #20.07.2020
            if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
                self.WritePointToPR200(0)                
            
    def draw_point_error(self, _pointIndex, _I, _P, _A, _isQuadroLoad, _angularError, _currentError):
        self.ui.lState.setPalette(self.alarmPalette)
        self.oPointGrid.set_point_record(_pointIndex, True, None, _P, _A)
        self.ui.lState.setText(u'Ошибка!!!')
        self.sound.play(self.env.config.snd_notify.point_error)
        # self.show_error_confirmation(_I, _angularError, _currentError) #Отключено #202

    def draw_point_angular_error(self, _pointIndex, _I, _P, _A, _isQuadroLoad, _angularError):
        self.oPointGrid.set_angular_error(_pointIndex)
        self.errorPointIndex = _pointIndex
        self.coil_view_button_refresh() #Нужно только для разблокировки очистки точки
        
    def draw_point_current_error(self, _pointIndex, _I, _P, _A, _isQuadroLoad, _currentError):
        self.oPointGrid.set_current_error(_pointIndex)
        self.errorPointIndex = _pointIndex
        self.coil_view_button_refresh() #Нужно только для разблокировки очистки точки

    def start(self, _bChecked):
        if _bChecked:
            #Тестируем
            #tam            
            if self.codeTypeTest in [3,4]:
                if self.oTestCoil.work():
                    self.ui.tvCoil.setEnabled(False)                
                    self.ui.tvItem.setEnabled(False)
                    self.ui.btnNewMap.setEnabled(False)
                    self.ui.btnTestType.setEnabled(False)
                    #self.ui.btnDevices.setEnabled(False)
                    self.ui.btnTester.setEnabled(False)
                    self.ui.btnAssistant.setEnabled(False)
                    self.ui.btnSupervisor.setEnabled(False)
                    self.ui.btnQuit.setEnabled(False)
#                    self.ui.btnAccountReport.setEnabled(False)
                    self.ui.btnStickers.setEnabled(False)
                    self.ui.btnInfo.setEnabled(False)
            else:
                self.oCoilVerification.work()

                if self.env.config.devices.ca5020.active:
                    if self.ui.autoCA5018.isChecked(): 
                        if self.ui.lbSecondLoad.text() != '':
                            self.Devices_.WriteToCA5020(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)
                        self.lastSecondLoad = 0
                else:        
                #30.06.2020
                    if self.ui.autoCA5018.isChecked():
                        if self.ui.lbSecondLoad.text() != '':
                            self.Devices_.WriteToCA5018(float(self.ui.lbSecondLoad.text()), self.info.SecondCurrent)
                        self.lastSecondLoad = 0
###30                    self.ui.lineEdit.setText(self.ui.lineEdit.text() + "*" + self.ui.lbSecondLoad.text())                        
###30                    self.ui.lineEdit_2.setText(self.ui.lineEdit_2.text() + "*" + self.ui.lbSecondLoad.text())                        
                        
#                if self.ui.checkBox_2.isChecked():
#                    self.WriteToPR200(self.info)                
                #30.06.2020
                if self.ui.autoPR200.isChecked():
                    self.WriteToPR200(self.info)
                           
                #30.07.2020            
                if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked() and self._I_old != None:
                    self.WritePointToPR200_(self._I_old)
                    self._I_old = None
                                
        else:
            #Ждем
            self.sound.stop_loop()
            #tam
            if self.codeTypeTest in [3,4]:
                self.oTestCoil.pause()
                self.ui.tvCoil.setEnabled(True)                
                self.ui.tvItem.setEnabled(True)                
                self.ui.btnNewMap.setEnabled(True)
                self.ui.btnTestType.setEnabled(True)
                #self.ui.btnDevices.setEnabled(True)
                self.ui.btnTester.setEnabled(True)
                self.ui.btnAssistant.setEnabled(True)
                self.ui.btnSupervisor.setEnabled(True)
                self.ui.btnQuit.setEnabled(True)                
#                self.ui.btnAccountReport.setEnabled(True)
                self.ui.btnStickers.setEnabled(True)
                self.ui.btnInfo.setEnabled(True)
            else:                
                self.oCoilVerification.pause()
                #20.07.2020
                if self.ui.autoTest.isChecked() and self.ui.autoPR200.isChecked():
                    self.WritePointToPR200(0)                
                    
                        
            

    def is_work(self):
        return bool(self.oCoilVerification and self.oCoilVerification.is_work()) 

    def print_report(self, _iMapID):
        from electrolab.gui.reporting import FRPrintForm  # Лишнняя команда, но без нее отчеты почему-то не печатаются
        
        u"""Печать"""
#        inputParms = {u'test_map':_iMapID, u'ConnectionString':self.get_connection_string()} 
        inputParms = {u'test_map':_iMapID} 
        try:
                
            if self.ui.btnCheckReport.isChecked() and self.ui.btnCheckReport.isVisible():

                ReportsExcel.verification_protocol(self.env.db, _iMapID, None, False)
                
                #25.05.2021
                '''
                try:
                    
                    
                    self.query_9 = QSqlQuery(self.env.db)
            
                    test_map = _iMapID
                     
                    strSQL = """                
select id as item
from item
where test_map = """ + str(test_map) + """
and istested
order by id
"""
                #    print strSQL
                
                    self.query_9.prepare(strSQL)
                    if not self.query_9.exec_():
                        QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
#                        return
                    else:    
                        model_9.setQuery(self.query_9)
                 
                    for i in range(model_9.rowCount()):
                        item = int(model_9.record(i).field('item').value().toString())
#                        if self.ui.checkBox_2.isChecked():
#                            ReportsExcel.verification_protocol(self.env.db, test_map, item, True)
#                        else:    
                        ReportsExcel.verification_protocol(self.env.db, test_map, item, False)
                
                except:
                    pass
                
        #        return        
'''


                #20.05.2021
                '''
                rpt = FRPrintForm(u'tester_protocol.fr3' ,inputParms , self.env)                
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
                rpt.print_()
                '''
                
                
                
            if self.ui.btnSupervisorReport.isChecked() and self.ui.btnSupervisorReport.isVisible():
                rpt = FRPrintForm(u'verifier_protocol.fr3' ,inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
                rpt.print_()
#                rpt.preview()
                
            if self.ui.btnTicketMatrix.isChecked() and self.ui.btnTicketMatrix.isVisible():
                from electrolab.gui.reporting import FRPrintForm
                inputParms = {u'test_map':self.oMap.iMapID, u'item':0}
                try:
                    if self.codeTypeTest in [3,4]:
                        rpt = FRPrintForm(u'ReportStickers.fr3' ,inputParms , self.env)
                        rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                        #rpt.preview()
                        rpt.print_()
                        # rpt.design()
                    if self.codeTypeTest in [0,2]:
                        
                        # Временно
                        if self.codeTypeTest == 0:
                            self.print_temp(self.oMap.iMapID, 1, False)
                        else:    
                            self.print_temp(self.oMap.iMapID, 2, False)
                        
                        # Вернуть
                        """
                        rpt = FRPrintForm(u'ReportStickers_2.fr3' ,inputParms , self.env)
                        rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                        #rpt.preview()
                        rpt.print_()
                        """
                                                                        
                except:
                    pass
                                
#                rpt = FRPrintForm(u'ReportTickets.fr3' ,inputParms , self.env)
#                rpt.print_()
#                rpt.preview()

#            if self.ui.btnAccountReport.isChecked():
            if self.ui.btnStickers.isChecked():
                msgBox(self, BeforeBuildAccount(self.env.db))

        except:
            pass

    
    # Времнный алгоритм печати шильдиков
    def print_temp(self, testMap, typeTest, view):
#        msgBox(self, print_temp)
#        return

        try:
            print 3
            self.query_9 = QSqlQuery(self.env.db)
            print 4
                     
#/ Временно
# 7.04.2020
            strSQL = """                
--select t1.id as item, t1.serial_number, makedate||'-'||serialnumber as zavnum, ordernumber, series, gost_id,
select t1.id as item, t1.serial_number, makedate||'-'||serialnumber as zavnum, ordernumber, series, gost_id,
to_char(t3.createdatetime, 'dd.mm.yy') as date, t4.fio as fio, t5.fullname                                                                                                
from item t1, serial_number t2, test_map t3, operator t4, stand t5                          
where t1.serial_number = t2.id
and t1.test_map = t3.id
and t3.operator = t4.id
and t3.stand = t5.id
and test_map = """ + str(testMap) + """                   
--and test_map = 52877
order by item        
"""

            print strSQL
                
            self.query_9.prepare(strSQL)
            if not self.query_9.exec_():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
            else:    
                model_9.setQuery(self.query_9)
                 
            for i in range(model_9.rowCount()):
# # 7.04.2020               inputParms = {u'test_map':testMap, u'item':int(model_9.record(i).field('item').value().toString()), u'type_test':typeTest}
                inputParms = {u'test_map':testMap, u'item':int(model_9.record(i).field('item').value().toString()), u'gost_id':int(model_9.record(i).field('gost_id').value().toString()), u'type_test':typeTest}
                rpt = FRPrintForm(u'ReportStickers_2.fr3' ,inputParms , self.env)
                rpt.fr.PrintOptions.Printer = self.env.config['printers']['sticker']
                if view:
                  rpt.preview()
                else:
                  rpt.print_()  
        except:
            pass


        
    def setConfig(self):
        '''
        inputParms = {u'test_map': 132065} ############################
                
        print "PRINT2"
        rpt = FRPrintForm(u'tester_protocol.fr3' ,inputParms , self.env)
                
        print "PRINT3"
        rpt.fr.PrintOptions.Printer = self.env.config['printers']['report']
        print "PRINT4"
        rpt.preview()
        print "PRINT5"
        return
        '''
        '''        
        self.print_report(self.oMap.iMapID)
        return
        '''
        
        
#        self.Config = Config(self.env)
        self.Config = Config()
        self.Config.setEnabled(True)
        self.Config.exec_()


    def setDevices(self):
        self.Devices = Devices(self.env)
        self.Devices.setEnabled(True)
        self.Devices.exec_()
        self.oTestCoil.Devices.data = self.Devices.data
        self.oTestCoil.setMeasureR(self.Devices.ui.comboBox.currentText())
        
        self.oTestCoil.Devices_comboBox_currentText = self.Devices.ui.comboBox.currentText()        
        
        
        self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True);
        print 'calcGlobal                     555555555555555555555555555555'


    def StartArchive(self):        
        from Archive import archive
        wind = archive(self.env)
        wind.exec_()

    def StartMsr(self):
        #self.map_close()
        #return           
        print u"Проверка наличия таблиц БД", self.adStandInfo.ID
        err_tbl = ""
        query = QSqlQuery(self.env.db)

#        query.prepare("select * from stand_msr")
        query.prepare("select * from map_msr")
        if not query.exec_(): err_tbl += "stand_msr\n"

        if err_tbl != "":
            print err_tbl  
            
            r = QMessageBox.warning(self, u"Предупреждение", u"""В БД требуется произвести изменения,
необходимые для работы приложения\n""" +
u"Произвести изменения БД?", QMessageBox.Yes, QMessageBox.No)                        
            
                        
            if r == QMessageBox.Yes:
                SQL = u"""
CREATE TABLE stand_msr
(
  id serial PRIMARY KEY,
  stand integer REFERENCES stand (id),
  zav_msr integer REFERENCES zav_msr (id)
);
COMMENT ON TABLE stand_msr IS 'Справочник привязки средств измерений к стенду';
COMMENT ON COLUMN stand_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN stand_msr.stand IS 'Ссылка на таблицу рабочих мест';
COMMENT ON COLUMN stand_msr.zav_msr IS 'Ссылка на таблицу заводских номеров средств измерений';
"""
                SQL = u"""
CREATE TABLE map_msr
(
  id serial PRIMARY KEY,
  test_map integer REFERENCES test_map (id),
  zav_msr integer REFERENCES zav_msr (id)
);
COMMENT ON TABLE map_msr IS 'Справочник привязки средств измерений к тележке';
COMMENT ON COLUMN map_msr.id IS 'Идентификатор записи';
COMMENT ON COLUMN map_msr.test_map IS 'Ссылка на таблицу тележек';
COMMENT ON COLUMN map_msr.zav_msr IS 'Ссылка на таблицу заводских номеров средств измерений';
COMMENT ON COLUMN stand_msr.stand IS 'Ссылка на таблицу рабочих мест';
COMMENT ON COLUMN stand_msr.zav_msr IS 'Ссылка на таблицу заводских номеров средств измерений';
"""
                print SQL
        
                if not query.exec_(SQL):
                    QMessageBox.warning(self, u"Предупреждение", u"Ошибка инициализации", QMessageBox.Ok)
                    return
                else:
                    QMessageBox.warning(self, u"Предупреждение", u"Инициализация выполнена!", QMessageBox.Ok)
            else:
                return
                          
                 
                 
#        from StandMsr import StandMsr
#        QMessageBox.warning(self, u"Предупреждение", u"ИнициализаSSSSSSSSSSS", QMessageBox.Ok)
        wind = StandMsr(self.env, self.adStandInfo.ID, self.adStandInfo.FullName)
        wind.exec_()
#        if wind.IS_SELECT:
#            zzz = wind.ID_ZAV_MSR


    def ImportIntoMapMsr(self):
        #print 'self.adStandInfo = ', self.adStandInfo
        if self.adStandInfo != None:
            wind = StandMsr(self.env, self.adStandInfo.ID, self.adStandInfo.FullName)
#        QMessageBox.warning(self, u"Предупреждение", str(self.adStandInfo.ID) + "   " + str(self.oMap.iMapID), QMessageBox.Ok)
            wind.generate_map_msr(self.oMap.iMapID, False, False)
#        self.adStandInfo.


        #tam 24.11.2016       
    def calc_global(self):
        if self.codeTypeTest in [3,4]:
            #print '++++++++++++++++++++calc_global'
            pass
# Комментируем за ненадобностью        
#            self.oTestCoil.calcGlobal(self.oMap.iMapID, None, self.adStandInfo.ID, None, None, True)
#            print 66666666666666666666            


