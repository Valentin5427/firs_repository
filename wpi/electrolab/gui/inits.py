#coding=utf-8
from PyQt5.QtCore import QDate
from dpframe.tech.typecheck import *
from serial.serialutil import SerialException
from dpframe.base.inits import requires_env, requires_env_parts
from dpframe.tech.AttrDict import AttrDict
from electrolab.gui.reference import MasterDetailReference
from electrolab.gui.TestMapFilterDlg import TestMapFilterDlg
from electrolab.gui.testmapref import Testmap
from electrolab.gui.msgbox import getTrue, msgBox
from electrolab.gui import config
@requires_env
@takes(type)
@returns(type)
def reference_init(cls):
    refs = {
            u'defect_testing_type':{
                u'table': u'defect_testing_type',
                u'display': u'Типы испытаний дефектов',
                u'dialog_ui': u'DlgDefectTestingType.ui'
            },
            u'_stand_user':{
                u'table': u'stand_user',
                u'display': u'Пользователи стендов',
                u'dialog_ui': u'DlgStandUser.ui'
            },
            u'_stand':{
                u'table': u'stand',
                u'display': u'Стенды',
                u'dialog_ui': u'DlgStand.ui'
            },
            u'stand':{
                u'cls': MasterDetailReference,
                u'master': u'_stand',
                u'detail': u'_stand_user',
                u'display': u'Стенды',
            },
            u'room':{
                u'table': u'room',
                u'display': u'Помещения',
                u'dialog_ui': u'DlgRoom.ui'
            },
            u'defect':{
                u'table': u'defect',
                u'display': u'Справочник несоответствий',
                u'dialog_ui': u'DlgDefect.ui'
            },
            u'operator':{
                u'table': u'operator',
                u'display': u'Справочник испытателей',
                u'dialog_ui': u'DlgOper.ui'
            },
            u'serial_number':{
                u'table': u'serial_number',
                u'display': u'Серийные номера',
                u'dialog_ui': u'DlgSerialNumber.ui'
            },
            u'climat':{
                u'table': u'climat',
                u'display': u'Журнал окружающей среды',
                u'dialog_ui': u'DlgClimat.ui'
            },
            u'_transformer':{
                u'table': u'transformer',
                u'display': u'Трансформаторы',
                u'dialog_ui': u'DlgTransformer.ui'
            },
            u'_coil':{
                u'table': u'coil',
                u'display': u'Вторичные обмотки',
                u'dialog_ui': u'DlgCoil.ui'
            },
            u'_test_map':{
                u'table': u'test_map',
                u'display': u'Карта испытаний',
                u'dialog_ui': u'DlgTestMap.ui',
                u'filter':u'testmap_filter'
            },
            u'_item':{
                u'table': u'item',
                u'display': u'Трансформатор',
                u'dialog_ui': u'DlgTestItem.ui'
            },
            u'transformer':{
                u'cls': MasterDetailReference,
                u'master': u'_transformer',
                u'detail': u'_coil',
                u'display': u'Трансформаторы',
            },
            u'test_map':{
                u'cls': Testmap,
                u'master': u'_test_map',
                u'detail': u'_item',
                u'display': u'Журнал испытаний',
            },
            u'testing_voltage': {
                u'table': u'testing_voltage',
                u'display': u'Справочник испытательных напряжений',
                u'dialog_ui': u'DlgTestingVoltage.ui'
            },
            u'device_command': {
                u'table': u'device_command',
                u'display': u'Команды периферийных устройств',
                u'dialog_ui': u'DlgDeviceCommands.ui',
            },
            u'_gost':{
                u'table': u'gost',
                u'display': u'ГОСТ',
                u'dialog_ui': u'DlgGOST.ui'
            },
            u'_gost_detail':{
                u'table': u'gost_detail',
                u'display': u'Таблица точек поверки',
                u'dialog_ui': u'DlgGOSTDetail.ui'
            },
            u'_gost_quadroload':{
                u'table': u'gost_quadroload',
                u'display': u'Таблица нагрузок',
                u'dialog_ui': u'DlgGOSTQuadroload.ui'
            },
            u'gost':{
                u'cls': MasterDetailReference,
                u'master': u'_gost',
                u'detail': u'_gost_detail',
                u'display': u'ГОСТ точки',
            },
            u'quadroload':{
                u'cls': MasterDetailReference,
                u'master': u'_gost',
                u'detail': u'_gost_quadroload',
                u'display': u'ГОСТ нагрузки',
            },
            u'test_type':{
                u'table': u'test_type',
                u'display': u'Тип испытания',
                u'dialog_ui': u'DlgTestType.ui'
            }
    }

    cls.env.refs = AttrDict.toAttrDict(refs)
    if u'filters' not in cls.env:
        cls.env.filters = AttrDict()
    return cls

@requires_env_parts(u'config')
@takes(type)
@returns(type)
def session_init(cls):
    u"""TODO: избавиться от гвоздей. При старте приложения создавать нормальную глобалюку с параметрами сессии, не через инит. """
    session = {
                u'operator': None
                , u'supervisor': None
                , u'climat': None
                , u'standNumber': cls.env.config.wpt_session.standNumber
               }
    #TODO: Вернул гвозди в параметры сеанса
    cls.env.session = AttrDict.toAttrDict(session)
    return cls


@requires_env_parts(u'config', u'log')
@takes(type)
@returns(type)
def serial_devices_init(cls):

    from serial import Serial
    from electrolab.tech import device

    def scaner(_portName):
        u""""""
        return device.BarCodeScannerRS232(cls.env.ports[_portName])

    def knt05(_params):
        u""""""
        fileName = _params.get(u'file', None)
        if fileName:
            return device.KNT05_forTest(fileName)
        else:
            return device.KNT05(cls.env.ports[_params.get(u'port', None)])
        
    cls.env.ports = AttrDict()
    cls.env.devices = AttrDict()
    ports = cls.env.config.get(u'ports', {})
    for name, params in ports.items():
        port = Serial()
        port.port = str(name)
        port.baudrate = params.get(u'baudrate', port.baudrate)
        port.bytesize = params.get(u'bytesize', port.bytesize)
        port.parity = params.get(u'parity', port.parity)
        port.stopbits = params.get(u'stopbits', port.stopbits)
        port.timeout = params.get(u'timeout', port.timeout)
        try:
            port.open()
        except (SerialException, OSError) as ex: # FIXME: уточнить тип исключения
            cls.env.log.warn(u'Порт ' + port.port + u' не обнаружен.')
        cls.env.ports[name] = port
        
    devices = cls.env.config.get(u'devices', {})
    
    
    st = config.testConfig()
    if st != "":
        msgBox(None, st)
        from config import Config
        from PyQt5 import QtGui
#        import sys
#        app = QtGui.QApplication(sys.argv)

        config1 = Config()
        config1.setEnabled(True)
        config1.exec_()


    
    cls.env.devices[u'scanner'] = scaner(devices.scanner)
    cls.env.devices[u'knt05'] = knt05(devices.knt05)
    return cls

@requires_env
@takes(type)
@returns(type)
def report_init(cls):
    reports = {
        u'verifier_protocol': {
            u'type': u'FR',
            u'template': u'verifier_protocol.fr3',
            u'initialization': u'verifier_params'
        }
        , u'verifier_protocol2': {
            u'type': u'FR',
            u'template': u'verifier_protocol.fr3',
            u'initialization': u'verifier_params2'
        }
        , u'tester_protocol': {
            u'type': u'FR',
            u'template': u'tester_protocol.fr3',
            u'initialization': u'verifier_params2'
        }
    }

    cls.env.reports = AttrDict.toAttrDict(reports)
    if u'filters' not in cls.env:
        cls.env.filters = AttrDict()
    return cls

@requires_env
@takes(type)
@returns(type)
def filter_init(cls):
    filters = {
        u'testmap_filter':{
            u'dialog': TestMapFilterDlg,
            u'dialog_ui': u'TestMapFilterDlg.ui',
            u'display': u'Фильтр журнала испытаний',
            u'params': {
                u'serial': {
                    u'display': u'Серийный номер'
                },
                u'from': {
                    u'display': u'С'
                },
                u'to': {
                    u'display': u'По'
                }
            }
        }
    }

    cls.env.filters = AttrDict.toAttrDict(filters)
    return cls
