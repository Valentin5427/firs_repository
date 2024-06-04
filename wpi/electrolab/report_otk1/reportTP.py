import datetime
import time

import win32print
from win32com.client import constants as const
import win32com.client
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtCore import QDateTime
# from Config_base import db
import locale
from electrolab.report_otk import Excel_const

import collections
locale.setlocale(locale.LC_NUMERIC, '')
decimal_point = locale.localeconv()['decimal_point']
# Основные объекты VBA http://bourabai.ru/einf/vba/2-04.htm

model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
windings = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
windingsKT = ["A-a2", "A-a3", "A-a4", "A-a5", "A-a6", "A-a7", "A-a8"]


sqrtPOV = {} # словарь сопоставления  корней к числам используется для поверки ТН
model_sqrt = QSqlQueryModel()
sql = 'select float_value, str_value  from parity_tabletn'
print(sql)
model_sqrt.setQuery(sql)
for i in range(model_sqrt.rowCount()):
    print(2323)
    sqrtPOV[float(model_sqrt.index(i,0).data())] = model_sqrt.index(i,1).data()
print(3323232,sqrtPOV)




p = 0.26
n = 0.09
a = 1
pickel_dict = {}
while p < 101:

    pickel_dict[a] = n
    p = round(float(p+ 0.26),2)
    n = round(float(n), 2)
    if n > 1:
        n += 0.17
    else:
        n += 0.09
    a +=1
print(pickel_dict)


import math


def float_or_int(number, digits = 1, digitsF = 2):
    if number % 1 == 0:
        return  toFixed(number,digits)
    else:
        return toFixed(number,digitsF)

# убирает лишние нули и округляет до
def delete_null(number):
    if type(number) in (float,int):
        number = str(number)
        while True:
            if number[-1] == '0':
                number = number[:-1]
            else:
                break
        number_to_points, number_after_dot = number.split('.')[0], number.split('.')[1]
        print(number_to_points)
        print(number_after_dot)
        if len(number_after_dot) > 1:
            value = round(float(f'{number_to_points}.{number_after_dot}'),2)
            return value
        elif len(number_after_dot) == 1:
            value = float(f'{number_to_points}.{number_after_dot}')
            return value
        else:
            return int(number_to_points)
    else:
        return None




# возвращает ширину столбцов для паспортов знол (1- до последнего столбца, 2- последний)
def col_column(c, s):
    if s%c == 0:
        print("ширина столбцов", s // c)
        return s//c, s//c

    elif c < 5:
        print(math.ceil(s/c))
        print("ширина столбцов до последней обмотки",math.ceil(s/c))
        print("ширина последней обмотки", s - ((c-1)* math.ceil(s/c) ))
        return math.ceil(s/c) , s-((c-1)*math.ceil(s/c))
    else:
        return s//c, s - (c-1)*(s//c)





def open_excel(name_file, name_printer, visible = 1 ):
    import os
    global wb, Excel
    p = os.path.abspath(name_file)
    if not os.path.exists(p):
        QMessageBox.warning(None, u"Ошибка шаблона отчета", f"Не удается найти файл {name_file}", QMessageBox.Ok)
        return False
    Excel = win32com.client.Dispatch("Excel.Application")
    Excel.Visible = visible
    if visible == 0:
        print(323232325324532)

    try:
        wb = Excel.Workbooks.Add(p)
        if check_printer(Excel, name_printer):
            Excel.ActivePrinter = np
            return True

        else:
            # QMessageBox.warning(None, u"Предупреждение", f"Проблемы с принтером, файл отправлен на принтер {Excel.ActivePrinter}", QMessageBox.Ok)
            return True
    except:
        QMessageBox.warning(None, u"Ошибка шаблона отчета", f"Не запускается файл {name_file}", QMessageBox.Ok)
        return False
# находим исполнение и уровень изоляции
def get_performance(stroka):
    import re
    try:
        result1 = re.findall(r'У\w+', stroka)[0]
    except:
        return None
    try:
        result2 = re.findall(r'\s[аб]\b', stroka)[0][1]
    except:
        result2 = ''
    print(result1)
    print(result2)
    result = f"{result1} {result2}"
    return result

def get_isp(stroka):
    import re

    result = re.findall(r'\s\w+', stroka)
    print(23232323,result)
    if result == []:
        return None
    return result[0][1:]





def check_printer(excel, namePrint):
    for i in range(100):
        try:
            global np
            np = f'{namePrint} (Ne{i:02}:)'
            excel.ActivePrinter = np
            return True
        except:
            pass
    return False


def get_count_point(coilId):
        count_point = {}
        for key in coilId:
            if coilId[key][0] != 'A-X':
                clscurasy = coilId[key][1]
                sql = f"""select ipercent from gost_detail
                                where gost_id = 7 and   classaccuracy = '{clscurasy}' and usequadro = False
                                ORDER BY ipercent"""
                model_point = QSqlQueryModel()
                model_point.setQuery(sql)
                count_point[clscurasy] = []
                count_point[clscurasy].append(model_point.rowCount())
                ipercent = []
                for i in range(model_point.rowCount()):
                    percent = [model_point.index(i, 0).data()]
                    ipercent.append(percent)
                count_point[clscurasy].append(ipercent * 2)

        return count_point


# ищем проверенные трасформаторы по указанной тележке
def select_result(items):
    sql = f"""select * from 
                    (
                    select row_number() OVER() as rn, *
                    FROM
                    (
                    select  tm.id as test_map, item.id as item,
                       tsf.fullname  as ShortName
                       , sn.transformer
                       , sn.serialnumber
                       , sn.makedate     
                       , type_transformer.tu
                       , tm.createdatetime            
                       , climat.temperature
                       , climat.humidity
                    --   , round(7.50 * climat.pressure, 0) as pressure              
                       , round(climat.pressure, 0) as pressure              																														
                       , tsf.id as tsfid            
                       , item.id as itemid
                       , oper.FIO as FIO
						, st.fullname
						,item.istested as tested
						--,item.defect as defect
						,df.fullname as name
						,pov.fio as poveritel
						,type_transformer.method
						,type_transformer.id
						, sn.id as idSn  
                    from
                       test_map tm
                    left join climat on climat.id = tm.climat
					inner join stand st on st.id = tm.stand 
                    inner join item on item.test_map = tm.id
					left join defect df on df.id = item.defect	
                    inner join serial_number sn on sn.id = item.serial_number
                    inner join transformer tsf on sn.transformer = tsf.id
                    left join type_transformer on tsf.type_transformer = type_transformer.id
                    inner join operator oper on oper.id = tm.operator
                    left join operator pov on pov.id = tm.supervisor
                    --where makedate = 21
                    --and item.istested                                                        
                    --where  item.istested  or item.defect is not NULL                                                       
                    order by
                           item.id
                    ) as t
                    ) as t1
                    where item in ({items})"""

    print(sql)
    model.setQuery(sql)
    if model.rowCount()> 0:
        return True
    else:
        return False



def toFixed(numObj, digits=0):
    if type(numObj) not in (float,int):
        return None
    print(33, numObj)
    return f"{numObj:.{digits}f}"



def searchPoveritel(item):
    sql1 = f"""select
                fio, t3.createdatetime
                from operator inner
                join
                (select stand.fullname, stand.test_type, t2.supervisor, t2.createdatetime
                from stand inner join
                (select test_map.id, test_map.stand, test_map.createdatetime, test_map.supervisor
                from test_map inner join
                (select id, serial_number, test_map, createdatetime from item
                where serial_number  in (select serial_number from item where id = {item}) )
                t1
                on
                test_map.id = t1.test_map)t2
                on
                stand.id = t2.stand
                where
                stand.test_type = 1
                order
                by
                t2.createdatetime
                DESC
                LIMIT
                1)t3

            on
            operator.id = t3.supervisor"""
    print(sql1)
    oQuerry1 = QSqlQuery(sql1)
    if oQuerry1.first():
        return (oQuerry1.value(0),oQuerry1.value(1).toString('dd.MM.yyyy'))

    return ('','')

# поиск оператора проводившего высокольтные испытания

def searchHV(item, test_type = 8 ):
    sql1 = f"""select
                fio, t3.createdatetime
                from operator inner
                join
                (select stand.fullname, stand.test_type, t2.operator, t2.createdatetime
                from stand inner join
                (select test_map.id, test_map.stand, test_map.createdatetime, test_map.operator
                from test_map inner join
                (select id, serial_number, test_map, createdatetime from item
                where serial_number  in (select serial_number from item where id = {item}) )
                t1
                on
                test_map.id = t1.test_map)t2
                on
                stand.id = t2.stand
                where
                stand.test_type = {test_type}
                order
                by
                t2.createdatetime
                DESC
                LIMIT
                1)t3

            on
            operator.id = t3.operator"""
    print(sql1)
    oQuerry1 = QSqlQuery(sql1)
    if oQuerry1.first():
        return (oQuerry1.value(0),oQuerry1.value(1).toString('dd.MM.yyyy'))

    return ('','')



def printRep():
    # ссылка на коды статусы принтера  http://systemmanager.ru/bv-admin.en/dscript/printerstatuscodes.htm
    try:
        print(0)
        wb.PrintOut()
        print(1)
        Excel.Visible = True
        print(2)
        Print = Excel.ActivePrinter
        print(3)
        namePrint = Print[:-8]
        print(1212,namePrint)
        status = win32print.GetPrinter(win32print.OpenPrinter(namePrint), 2)['Status']
        if status not in (0,1024,16384) :
            QMessageBox.warning(None, f"Ошибка печати",
                                f"Проверьте работу принтера  {status}", QMessageBox.Ok)
        wb.Close(SaveChanges=False)
        Excel.Quit()
        # log.info(f'статус принтера  {status}')
    except Exception as ex:
        print(3213213123412431242142142142142142354)
        QMessageBox.warning(None, f"Ошибка печати",
                            f"Проверьте работу принтера или Excel", QMessageBox.Ok)
        # log.info(f'ошибка печати  {ex}')
        #





# парсер наименований тт типа A-X, a1-x1, a2-x2
def parser_name_tt(item):
    winding = {}
    modelTT = QSqlQueryModel()
    sql = f"""select * from coil
            where transformer in (select serial_number.transformer from item
                                        inner join serial_number on item.serial_number = serial_number.id
                                    where item.id = {item})
                                    order by coilnumber, tap"""
    print(sql)
    modelTT.setQuery(sql)
    for i in range(modelTT.rowCount()):
        idCoil = modelTT.index(i,0).data()
        CoilNumber = modelTT.index(i,2).data()
        tap = modelTT.index(i,3).data()
        classcur = modelTT.index(i,5).data()
        rating = modelTT.index(i,12).data()
        if classcur.count('P'):
            type_win = 'Z'
        else:
            type_win = 'D'
        primarycur = int(modelTT.index(i,6).data())
        secondcur = int(modelTT.index(i,7).data())
        secondload = float_or_int(modelTT.index(i,8).data())
        name_win = f"{CoilNumber}И1-{CoilNumber}И{tap}"
        winding[idCoil] = [type_win, primarycur,secondcur, classcur,secondload,  name_win, rating,None,None,None,None,None]
    return winding


def parse_result_tt(item,winding):
    # записываем сначала заданные коэффициенты


    try:
        modelRating = QSqlQueryModel()
        sql1 = f"""select coil,rating, i2,u2, r20, r, predel from checking_2
                where item in (select DISTINCT ON (stand.test_type)  t1.id from test_map
                                    inner join
                                            (select test_map , item.id, item.istested, item.createdatetime from item
                                                where serial_number in (select serial_number from item where id = {item}))t1 on test_map.id = t1.test_map
                                    inner join stand on test_map.stand = stand.id
                                    where test_type in (4,5)  and t1.istested
                                    order by stand.test_type DESC, t1.createdatetime DESC
                                    LIMIT 1)"""
        print(sql1)
        print(292929, winding)
        modelRating.setQuery(sql1)
        for k in range(modelRating.rowCount()):
            idCoil1 =  modelRating.index(k,0).data()
            kf = modelRating.index(k, 1).data()
            u = modelRating.index(k, 2).data()
            i = modelRating.index(k, 3).data()
            r20 = modelRating.index(k, 4).data()
            r = modelRating.index(k, 5).data()
            predel = modelRating.index(k, 6).data()
            winding[idCoil1][6] = kf
            winding[idCoil1][7] = i
            winding[idCoil1][8] = u
            winding[idCoil1][9] = r20
            winding[idCoil1][10] = r
            winding[idCoil1][11] = predel

        print(winding)
        return winding
    except:
        return False
    # 75063: ['Z', 500, 5, '10P', 10, '2И1-2И2', 10.0, 23.3552676454, 0.1298098833, 0.0807335907]}
    # 1.Элемент тип обмотки,  2 И 3 ПЕРВИЧНЫЙ И ВТОРИЧНЫЙ ТОК, 3 КЛАСС Точности
    # 4 вторичная нагрузка, 5 название 6 коэффициент, 7 ток, 8 напряжение 9 сопротивление 10 измеренное сопротивление



# ___________________________________________________________ПЕЧАТЬ ПАСПОРТОВ_____________________________________________
def select_passportTP(items,func, kontroler = False):
    #получаем необходимые данные
    sql = f"""select      
            t1.id,
            t1.data,
            serial_number.id,
    		serial_number.ordernumber,
    		serial_number.series,
    		serial_number.serialnumber,
    		serial_number.makedate,
    		serial_number.transformer,
    		transformer.fullname,
            transformer.weight,
            transformer.copper_content,
            transformer.copper_alloy_content,
            type_transformer.tu,
            type_transformer.type,
            type_transformer.method,
            type_transformer.interval,
            type_transformer.declaration,
            type_transformer.number_reestr,
            transformer.voltage,
            transformer.maxopervoltage,
            t1.fio,
            transformer.dynamic_current,
            type_transformer.ID,
            transformer.time_thermal_current,
            transformer.thermal_current,
            transformer.lead_length,
            t1.operator as operator,
            t1.stand,
            transformer.turns_rario,
            transformer.ktt
            
                from serial_number INNER JOIN
                (select item.id, serial_number  AS sn, item.acceptdatetime AS data, poveritel.fio as fio, isptatel.fio as operator, stand.fullname as stand  from item
                inner join test_map on item.test_map = test_map.id
                left join operator as poveritel on test_map.supervisor = poveritel.id
                left join operator as isptatel on test_map.operator = isptatel.id
                inner join stand on test_map.stand = stand.id
                where item.id in ({items}))t1
                ON serial_number.id =t1.sn
                INNER JOIN transformer ON serial_number.transformer = transformer.id
                left JOIN type_transformer on transformer.type_transformer = type_transformer.id"""
    print(sql)

    model.setQuery(sql)
    if model.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return

    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()
    for i in range(model.rowCount()):
        info = {}
        info['idItem'] = model.index(i, 0).data()
        info['data'] = model.index(i, 1).data().toString('dd.MM.yyyy')
        info['ordernumber']  =  model.index(i, 3).data()
        info['series']  =  model.index(i, 4).data()
        info['serialnumber']  = model.index(i, 5).data()
        info['makedate']  = model.index(i, 6).data()
        info['idTransformer']  = model.index(i, 7).data()
        info['fullname']  = model.index(i, 8).data()
        info['weight']  = model.index(i, 9).data()
        info['copperP']  = model.index(i, 10).data()
        info['copperPN']  = model.index(i, 11).data()
        info['tu'] = model.index(i, 12).data()
        info['type']  = model.index(i, 13).data()
        info['method'] = model.index(i, 14).data()
        info['interval'] = model.index(i, 15).data()
        info['declaration'] = model.index(i, 16).data()
        info['nr'] = model.index(i, 17).data()
        info['voltage'] = model.index(i, 18).data()
        info['maxvoltage'] =  model.index(i, 19).data()
        info['poveritel'] = model.index(i, 20).data()
        info['dynamic_current'] = model.index(i, 21).data()
        info['type_transformer'] = model.index(i, 22).data()
        info['time_current'] = model.index(i, 23).data()
        info['thermal_current'] = model.index(i, 24).data()
        info['lead_length'] = model.index(i, 25).data()
        info['operator'] = model.index(i, 26).data()
        info['stand'] = model.index(i, 27).data()
        info['turns'] = model.index(i, 28).data()
        info['ktt'] = model.index(i, 29).data()
        info['kontroler'] = kontroler
        for key in info:
            if info[key] == 0:
                if key == 'copperP':
                    info[key] = 0.5
                elif key == 'copperPN':
                    info[key] = 0.3
                else:
                    info[key] = ''

        func(info)
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass


def check_px(transformer_id):
    model = QSqlQueryModel()
    sql = f"""select classaccuracy from coil where transformer = {transformer_id}"""
    model.setQuery(sql)
    print(sql)
    for i in range(model.rowCount()):
        print(1243, model.index(i, 0).data())
        print(453, model.index(i, 0).data().count('PX'))
        if model.index(i, 0).data().count('PX'):
            return True
    return False

def fill_passportTP_full(info):
    print('заполняем паспорт ТТ')
    print(info)
    sheet = wb.ActiveSheet
    coil_name = parser_name_tt(info['idItem'])
    coil = parse_result_tt(info['idItem'], coil_name)
    # if coil == False:
    #     if getTrue(None,'Не удается сопоставить id обмоток трансформатора c id результатами \n распечатать пустой?'):
    #         fill_passportTT_blank(info)
    #     return
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38,1).Value = info['fullname']
    sheet.Cells(40, 1).Value = info['tu']
    sheet.Cells(41, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(53, 22).Value = info['interval']
    sheet.Cells(20, 21).Value = info['type']
    sheet.Cells(45,17).Value = f"Трансформатор тока {info['type']}  соответствует требованиям {info['tu']} и признан годным для эксплуатации"
    sheet.Cells(53, 17).Value = f"Трансформатор тока {info['type']} законсервирован и упакован предприятием-изготовителем согласно требованиям Руководства по эксплуатации."
    sheet.Cells(41, 12).Value = info['data']
    sheet.Cells(58, 27).Value = info['copperP']
    sheet.Cells(59, 20).Value = info['copperPN']
    sheet.Cells(30, 20).Value = check_EAN_valid(f"90{info['serialnumber']}20{info['makedate']}00")
    primary_current = None
    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {} # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    first, last = col_column(countW,8)
    [last_coil] = collections.deque(coil, maxlen=1)
    for i in coil:
        if i != last_coil:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(45, sc)
        sc = sc+cor-1
        mx2 = sheet.Cells(45, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        sclst[i] = [x, f"{x}45:{y}45",cor]
        y = mx2.Address[1]
        sheet.Range(f"{x}45:{y}45").Merge()
        sheet.Range(f"{x}49:{y}49").Merge()
        sheet.Range(f"{x}51:{y}52").Merge()
        sheet.Range(f"{x}53:{y}53").Merge()
        sheet.Range(f"{x}54:{y}54").Merge()

        sc +=1

    for i in sclst:
        koef = 32 / countW / sclst[i][2]

        sheet.Range(sclst[i][1]).ColumnWidth = koef

    # закончили формировать_________________________________
    position = 1
    print(coil)
    # записываем сопротивление
    for i in coil:
        primary_current = [coil[i][1]]
        print(primary_current)
        print(645464, toFixed(coil[i][8],2)  )
        data = [[coil[i][5]], [None], [None],[coil[i][1]],[coil[i][2]], [None],  [toFixed(coil[i][9],3)] , [None],[toFixed(coil[i][7],1)],  [toFixed(coil[i][8],3)]]
        sheet.Range(f"{sclst[i][0]}45:{sclst[i][0]}54").Value = data
        position += 1
    print(334333434, primary_current)

    sheet.Cells(46, 7).Value = 0.66
    sheet.Cells(47, 7).Value = 0.72
    sheet.Cells(48, 7).Value = primary_current
    sheet.Cells(50,7).Value = get_rele(info['fullname'])

    print(2123,info['ktt'])
    if info['ktt'] in ('K,К'):
        sheet.Cells(57, 1).Value = 'Л3-Л4: вспомогательная обмотка, см. АДШП.1.800.001 РЭ'

    position = 55
    if info['ktt'] in ('B','В'):
        sheet.Cells(position, 1).Value = f"Длина гибких выводов вторичных обмоток, мм {info['lead_length']}"
        sheet.Range(f"A{position}:N{position}").Borders.LineStyle = True
        position +=1
    print(35)
    sheet.Cells(position, 1).Value = f"Масса трансформатора, не более   {info['weight']}   кг"
    print(56)
        # находим руковдство по эксплуатации
    sqlSP = f"""select transformer.type_transformer as tt, var_constr_isp as isp, climat as climat , type_transformersp.id as sp, type_transformersp.designation as designation, type_transformersp.manual as manual   from type_transformersp
                               inner join transformer on transformer.type_transformer =  type_transformersp.type_transformer
                               where transformer.id = {info['idTransformer']}"""

    print(sqlSP)
    modelSP = QSqlQueryModel()
    modelSP.setQuery(sqlSP)
    climat = modelSP.index(0, 2).data()
    print(11,climat)
    desigation = ''
    manual = ''

    for i in range(modelSP.rowCount()):
        print(312, modelSP.index(i, 1).data(),info['fullname'] )
        if info['fullname'].count(modelSP.index(i, 1).data()):

            desigation = modelSP.index(i, 4).data()
            manual = modelSP.index(i, 5).data()
            break
        print(121,modelSP.index(i, 1).data())
        if modelSP.index(i, 1).data() in (None, ''):
            desigation = modelSP.index(i, 4).data()
            manual = modelSP.index(i, 5).data()

    if modelSP.rowCount() != 0:
        sheet.Cells(16, 20).Value = desigation
        sheet.Cells(40, 17).Value =  f"Руководстве по эксплуатации {manual}"
    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}",
                            QMessageBox.Ok)



    #записываем контроллера
    if info['kontroler']:
        controler,data1 = searchHV(info['idItem'],10)
        sheet.Cells(48, 24).Value = f"{controler} \n {data1}"
        print(12121,controler,data1)


def get_rele(name):
    type_rele = ['АП1', 'АП2', 'КВ1', 'КВ2']
    for rele in type_rele:
        if name.count(rele):
            return rele
    return ''




def fill_dataTC(sheet,position,sclst,key,data):
    try:
        for i in data[key]:
            sheet.Range(f"{sclst[i][0]}{position}").Value = data[key][i]
    except:
        pass

def check_pr(coil):
    for i in coil.values():
        if i[3].count('PR'):
            return True
    return False


def cell_merging(sheet,position, sclst, countW, index = 1):
    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    first, last = col_column(countW, 8)
    for i in range(1, countW + 1):
        if i != countW:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(position, sc)
        sc = sc + cor - 1
        mx2 = sheet.Cells(position+1, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        print()
        print(11112, x, y)
        print(f"{x}{position+1}:{y}{position+1}")
        sheet.Range(f"{x}{position}:{y}{position+index}").Merge()
        sc += 1





def fill_passportTT_blank(info):
    print(334563456436346436436)
    # заполняем паспор
    print(info)
    coil = parser_name_tt(info['idItem'])
    sheet = wb.ActiveSheet
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38, 1).Value = info['fullname']
    sheet.Cells(40, 1).Value = info['tu']
    sheet.Cells(41, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(10, 17).Value = 'Декларация о соответствии ' + info['declaration']
    sheet.Cells(11, 17).Value = 'Номер в реестре СИ РФ ' + info['nr']
    sheet.Cells(53, 22).Value = info['interval']
    sheet.Cells(20, 21).Value = info['type']
    sheet.Cells(44,
                17).Value = f"Трансформатор тока {info['type']}  соответствует требованиям {info['tu']} и признан годным для эксплуатации"
    sheet.Cells(60,
                17).Value = f"Трансформатор тока {info['type']} законсервирован и упакован предприятием-изготовителем согласно требованиям Руководства по эксплуатации."
    sheet.Cells(51, 17).Value = f"Трансформатор тока прошел первичную поверку по {info['method']}"
    # sheet.Cells(41, 12).Value = info['data']
    sheet.Cells(65, 27).Value = info['copperP']
    sheet.Cells(66, 20).Value = info['copperPN']
    sheet.Cells(30, 20).Value = check_EAN_valid(f"90{info['serialnumber']}20{info['makedate']}00")
    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {}  # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    print(11, countW)
    # countW = 6

    first, last = col_column(countW, 8)
    for i in range(1, countW + 1):
        print(112, i)
        if i != countW:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(43, sc)
        sc = sc + cor - 1
        mx2 = sheet.Cells(43, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        sclst[i] = [x, f"{x}43:{y}43", cor]
        y = mx2.Address[1]
        print(11112, x, y)
        sheet.Range(f"{x}44:{y}44").Merge()
        sheet.Range(f"{x}47:{y}47").Merge()
        sheet.Range(f"{x}48:{y}48").Merge()
        sheet.Range(f"{x}49:{y}49").Merge()
        sheet.Range(f"{x}50:{y}50").Merge()
        sheet.Range(f"{x}51:{y}52").Merge()
        sheet.Range(f"{x}53:{y}54").Merge()
        sheet.Range(f"{x}55:{y}56").Merge()
        sheet.Range(f"{x}57:{y}57").Merge()
        sheet.Range(f"{x}58:{y}58").Merge()
        sc += 1
    print(sclst)
    # sheet.Range(f"G44:{y}55").Borders.LineStyle = True
    # sheet.Range(f"G43:{y}55").HorizontalAlignment = -4108
    # sheet.Range(f"G43:{y}55").VerticalAlignment = -4108
    print(sclst)
    for i in range(1, len(sclst) + 1):
        koef = 32 / countW / sclst[i][2]
        # if i == len(sclst):
        #     koef = 32/countW/countW

        sheet.Range(sclst[i][1]).ColumnWidth = koef
    # закончили формировать_________________________________
    position = 1
    # записываем сопротивление
    print(sclst)

    for i in coil:
        primary_current = [coil[i][1]]
        print(3242547487546734576)
        print(coil[i])
        print([coil[i][5]])
        if coil[i][0] == 'Z':
            print(43434354646)
            data = [[coil[i][5]], [None], [None], [coil[i][1]], [coil[i][2]], [coil[i][3]], [coil[i][4]], [None], [None],
                    [None], [None], [None], [None], [None],
                    [None]]
        else:
            data = [[coil[i][5]], [None], [None], [coil[i][1]], [coil[i][2]], [coil[i][3]], [coil[i][4]],  [None], [None],
                    [None], [None], [None], [None], [None],
                    [None]]

        sheet.Range(f"{sclst[position][0]}44:{sclst[position][0]}58").Value = data
        position += 1

    sheet.Cells(45, 7).Value = info['voltage']
    sheet.Cells(46, 7).Value = info['maxvoltage']
    # sheet.Cells(47, 7).Value = primary_current
    position1 = 58
    position = 59
    if info['thermal_current'] not in (None, '', 0):
        sheet.Range(F"A{position}:F{position}").Merge()
        sheet.Range(F"G{position}:N{position}").Merge()
        sheet.Cells(position, 1).Value = 'Ток термической стойкости, кА'
        sheet.Cells(position, 7).Value = info['thermal_current']
        position += 1
    if info['time_current'] not in (None, '', 0):
        sheet.Range(F"A{position}:F{position}").Merge()
        sheet.Range(F"G{position}:N{position}").Merge()
        sheet.Cells(position, 1).Value = 'Время протекания тока, с'
        sheet.Cells(position, 7).Value = info['thermal_current']
        position += 1
    if info['dynamic_current'] not in (None, '', 0):
        sheet.Range(F"A{position}:F{position}").Merge()
        sheet.Range(F"G{position}:N{position}").Merge()
        sheet.Cells(position, 1).Value = 'Ток эл/динамической стойкости, кА'
        sheet.Cells(position, 7).Value = info['dynamic_current']
        position += 1
    if info['lead_length'] not in (None, '', 0):
        sheet.Range(F"A{position}:F{position + 1}").Merge()
        sheet.Range(F"G{position}:N{position + 1}").Merge()
        sheet.Cells(position, 1).Value = 'Длина гибких выводов вторичных обмоток, мм'
        sheet.Cells(position, 7).Value = info['lead_length']
        position += 2
    sheet.Range(f"A{position1}:N{position - 1}").Borders.LineStyle = True
    sheet.Range(F"A{position}:N{position}").Merge()
    sheet.Cells(position, 1).Value = f"Масса трансформатора, не более   {info['weight']}   кг"

    # находим руковдство по эксплуатации
    sqlSP = f"""select  t1.designation, t1.manual,
                            CASE
                                WHEN t1.climat = t1.isp THEN t1.sp
                                ELSE (select type_transformersp.id FROM type_transformersp  where type_transformer = t1.tt and var_constr_isp in (NULL, ''))
                                end 
                        FROM
                            (select transformer.type_transformer as tt, var_constr_isp as isp, climat as climat , type_transformersp.id as sp, type_transformersp.designation as designation, type_transformersp.manual as manual   from type_transformersp
                                inner join transformer on transformer.type_transformer =  type_transformersp.type_transformer
                                where transformer.id = {info['idTransformer']} )t1
                                limit  1"""
    print(sqlSP)
    query = QSqlQuery(sqlSP)
    if query.first() == 1:
        sheet.Cells(16, 20).Value = query.value(0)
        sheet.Cells(40, 17).Value = f"Руководстве по эксплуатации {query.value(1)}"
    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}",
                            QMessageBox.Ok)


# ___________________________________________________________КОНЕЦ  ПЕЧАТИ ПАСПОРТОВ_____________________________________________






def resultDictTT(item, name, nomer = None):
    tt_name = parser_name_tt(item)[0]
    result = {}
    # проверка id coil  на случай если изменили параметры трансформатора на тележке
    sql1 = f"""select DISTINCT coil from test_tt
                where item = {item}"""
    print(4325432634567454567, tt_name)
    modelT = QSqlQueryModel()
    modelT.setQuery(sql1)
    if modelT.rowCount() != 0:
        for i in range(modelT.rowCount()):
            key = int(modelT.index(i,0).data())
            print('key',key, type(key))
            if key not in tt_name:
                print(212478,key)
                QMessageBox.warning(None, 'Ошибка ',
                                    f"Не удается сопоставить  ID обмотки  трансформатора {name} {nomer}  в полученных резутатах с данными в БД \n"
                                    f" Удалите трансформатор с тележки и заново проверьте",
                                    QMessageBox.Ok)
                return False
    else:
        print(323232323)
        QMessageBox.warning(None, 'Ошибка ',
                            f"Не удается сопоставить  ID обмотки  трансформатора {name}  {nomer} в полученных резутатах с данными в БД \n"
                            f" Удалите трансформатор с тележки и заново проверьте",
                            QMessageBox.Ok)
        return False









    #ШАБЛОН КЭША-СЛОВАРЯ ДЛЯ ТРАНСФОРМАТОР ТТ   {coil: {'P':{40 : {'full' : {'loaded': [a,o,p] , 'no_load':[a,o,p],   'half' : {'loaded': [a,o,p] , 'no_load':[a,o,p] }}}}}
    modelR = QSqlQueryModel()
    # получаем результаты сопротивлений
    sql = f"""select test_tt.coil, resist
         from test_tt inner join coil ON test_tt.coil = coil.id
           where item = {item} and resist is not null and current_xx is null and voltage_xx is Null and a is Null and u is Null and p is Null
            order by coil.coilnumber"""
    print(sql)
    modelR.setQuery(sql)
    print(1111,tt_name)
    try:
        for i in range(modelR.rowCount()):
            id  = modelR.index(i,0).data()
            resist = modelR.index(i,1).data()
            if 'R' not in result:
                result['R'] = {}
            print(222121,id, tt_name[id][0])
            if tt_name[id][0] != 'A-X':
                resist = toFixed(resist,3)
            result['R'][tt_name[id][0]] = resist
        print(result)
    except KeyError:
        QMessageBox.warning(None, 'Ошибка поиска результатов сопротивления' , f"Ошибка не удается определить ID обмотки трансформатора {name} \n Удалите трансформатор с тележки и заново проверьте ",QMessageBox.Ok)
        return False
    # return result


    modelP = QSqlQueryModel()
    # получаем результаты погрешностей
    sql = f"""select test_tt.coil, test_tt.point,
     test_tt.quadroload, test_tt.load,
     test_tt.a,test_tt.u,test_tt.p, coil.secondload
     from test_tt inner join coil ON test_tt.coil = coil.id
       where item = {item} and resist is Null and current_xx is null and voltage_xx is Null order by coilnumber"""
    print(sql)
    modelP.setQuery(sql)
    for i in range(modelP.rowCount()):
        id  = modelP.index(i,0).data()
        point = modelP.index(i,1).data()
        quadro = modelP.index(i,2).data()
        load = modelP.index(i,3).data()
        volt = float(modelP.index(i,7).data())
        # a = toFixed(float(modelP.index(i,4).data()),2)
        # print(a, modelP.index(i,4).data())
        a = modelP.index(i,4).data()
        u = modelP.index(i,5).data()
        p = toFixed(float(modelP.index(i, 6).data()), 2)
        if id not in result:
            result[id] = {}
            result[id]['P'] = {}
            result[id]['P']['load'] = {} # сохраняем данные 100% нагрузки
            result[id]['P']['nload'] = {} # сохраняем данные 25% нагрузки

        if point not in result[id]['P']['load']:
            result[id]['P']['load'][point] = {}
            result[id]['P']['load'][point]['full'] = [None,None,None,None]
            result[id]['P']['load'][point]['half'] = [None,None,None,None]
            result[id]['P']['nload'][point] = {}
            result[id]['P']['nload'][point]['full'] = [None,None,None,None]
            result[id]['P']['nload'][point]['half'] = [None,None,None,None]

        if quadro and not load:
            result[id]['P']['nload'][point]['half'] = [volt/4,  a, u, p]

        if quadro and load:
            result[id]['P']['nload'][point]['full'] = [volt/4,a, u, p]

        if not quadro and load:
            result[id]['P']['load'][point]['full'] = [volt,a, u, p]

        if not quadro and not load:
            result[id]['P']['load'][point]['half'] = [volt,a, u, p]

    # получаем результаты холостого хода
    modelX = QSqlQueryModel()
    sqlX = f"select current_xx, voltage_xx from test_tt where item = {item} and voltage_xx is not null"
    print(sqlX)
    result['X'] = {}
    modelX.setQuery(sqlX)
    for i in range(modelX.rowCount()):
        result['X'][modelX.index(i,1).data()] = modelX.index(i,0).data()
    return result

def fill_ticket_tc(info):
    print(info)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 1).Value = f"№{info['makedate']}-{info['serialnumber']} {info['operator']} {info['data']}"
    sheet.Cells(2, 1).Value = info['stand']
    coil_name = parser_name_tt(info['idItem'])
    coil = parse_result_tt(info['idItem'],coil_name)
    dop_params = extra_options(coil, info['idItem'],24)
    print(352,dop_params)
    print(3254,coil)
    position_parametr = 3
    position_coil = 4
    position_coils = {}
    pc = 0
    for i in dop_params:
        if dop_params[i] != {}:
            sheet.Cells(3,position_parametr).Value = i
            for c in dop_params[i]:
                if c not in position_coils:
                    position_coils[c] = position_coil
                    sheet.Range(f"A{position_coil}:B{position_coil}").Merge()
                    sheet.Cells(position_coil,1).Value = coil[c][5]
                    position_coil +=1
                pc = position_coils[c]
                val = dop_params[i][c]
                sheet.Cells(pc,position_parametr).Value = str(val)
            position_parametr += 1
    print(441,position_parametr)
    mx1 = sheet.Cells(3,position_parametr-1)
    x = mx1.Address[1]
    print(3331,x)
    sheet.Range(f"A3:{x}{position_coil-1}").Borders.LineStyle = True
    sheet.Range(f"A3:{x}{position_coil-1}").EntireColumn.AutoFit()
    # print(4543,f"A3:{sheet.Cells(pc,position_parametr)}")
    # sheet.Range(f"A3:{pc}")
    #

def fill_ticket_tp(info):
    # coil_name = parser_name_tt(info['idItem'])
    # coil = parse_result_tt(info['idItem'],coil_name)
    sheet = wb.ActiveSheet
    sheet.Cells(3,2).Value = info['fullname']
    sheet.Cells(3, 12).Value =  f"№{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(5, 12).Value = f"{info['weight']} кг"
    sheet.Cells(6, 2).Value = info['tu']
    sheet.Cells(6, 13).Value = f"20{int(info['makedate'])} г"

    return
    sheet.Cells(4, 2).Value = f"{info['type']}  {get_isp(info['fullname'])}       №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(11, 4).Value = f"{float_or_int(info['voltage'])}кВ"
    sheet.Cells(12, 2).Value = f"{info['tu']}         {info['weight']} кг 20{int(info['makedate'])} г"
    sheet.Cells(11, 2).Value = get_performance(info['fullname'])
    # формируем таблицу______________________________________________________
    sc = 4  # начальная координата
    sclst = {}  # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    if countW > 5:
        sheet.Range('D5:N5').Font.Size = 7
    first, last = col_column(countW,11)
    for i in range(1, countW + 1):
        print(112, i)
        if i != countW:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(6, sc)
        sc = sc + cor - 1
        mx2 = sheet.Cells(6, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        sclst[i] = [x, f"{x}43:{y}43", cor]
        y = mx2.Address[1]
        sheet.Range(f"{x}5:{y}5").Merge()
        sheet.Range(f"{x}6:{y}6").Merge()
        sheet.Range(f"{x}7:{y}7").Merge()
        sheet.Range(f"{x}8:{y}8").Merge()
        sheet.Range(f"{x}9:{y}9").Merge()
        sheet.Range(f"{x}10:{y}10").Merge()
        sc += 1
    longP = 275 # ширина столбцов обмоток в пикселях
    s = 0
    for i in range(1, len(sclst) + 1):
        koef = longP / countW / sclst[i][2]
        s+= sheet.Range(sclst[i][1]).ColumnWidth * sclst[i][2]
        sheet.Range(sclst[i][1]).ColumnWidth = pickel_dict[int(koef)]
    position = 1

    for i in coil:
        if coil[i][0] == 'Z':
            data = [ [coil[i][5]],[f'{coil[i][1]}/{coil[i][2]}'], [coil[i][3]], [coil[i][4]], [None],  [coil[i][6]]]
        else:
            data = [ [coil[i][5]],[f'{coil[i][1]}/{coil[i][2]}'], [coil[i][3]], [coil[i][4]], [coil[i][6]]  , [None]]

        sheet.Range(f"{sclst[position][0]}5:{sclst[position][0]}10").Value = data
        position += 1


def TTpoverka(func):
    print(3232323)
    item =  model.record(0).field('item').value()
    print(item)
    for i in range(model.rowCount() - 1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()
    for i in range(model.rowCount()):
        info = {}
        info['item'] = model.record(i).field('item').value()
        info['test_map'] = model.record(i).field('test_map').value()
        info['idSn'] = model.record(i).field('idSn').value()

        func(info,i)
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass

def fill_poverkaTT_full(info,nn):
    query = QSqlQuery()
    print(info)
    ws = wb.ActiveSheet
    global name_msr_etalon
    global name_msr_vspom

    # Средства измерения эталонные
    strSQL = f"""                
    select t1.id, t1.zav_msr, name_msr, zav_num, comment
    --select *
    from map_msr t1, zav_msr t2, msr t3
    where t1.zav_msr = t2.id
    and t2.id_msr = t3.id
    and t1.test_map = {info['test_map']}
    and type = 1                   
    order by name_msr
    """

    print(strSQL)
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)

    name_msr_etalon = ''
    for i in range(model_2.rowCount()):
        #        name_msr_etalon += unicode(model_2.record(i).field('name_msr').value().toString()) + u' №' + unicode(model_2.record(i).field('zav_msr').value().toString()) + '/'
        # 24.01.2022        name_msr_etalon += unicode(model_2.record(i).field('name_msr').value().toString()) + u' №' + unicode(model_2.record(i).field('zav_num').value().toString()) + '/'
        name_msr_etalon += model_2.record(i).field('comment').value() + u' №' + model_2.record(i).field('zav_num').value() + '/'

    name_msr_etalon = name_msr_etalon[0:len(name_msr_etalon) - 1]
    print(21212,name_msr_etalon)
    # Средства измерения вспомогательные
    strSQL = f"""                
select t1.id, t1.zav_msr, name_msr, zav_num, comment
--select *
from map_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and t1.test_map = {info['test_map']}
and type = 2                  
order by name_msr
"""

    print(strSQL)
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)
    #    if model_2.rowCount() < 1:
    #        QMessageBox.warning(None, u"Предупреждение", u"Нет данных по средствам измерения!", QMessageBox.Ok)

    name_msr_vspom = ''
    for i in range(model_2.rowCount()):
        #        name_msr_vspom += unicode(model_2.record(i).field('name_msr').value().toString()) + u' №' + unicode(model_2.record(i).field('zav_msr').value().toString()) + '/'
        name_msr_vspom += model_2.record(i).field('name_msr').value() + u' №' + model_2.record(i).field('zav_num').value() + '/'

    name_msr_vspom = name_msr_vspom[0:len(name_msr_vspom) - 1]


#     # ws.Range('A1:I40').Copy()
#     A = ws.Columns('A:A').ColumnWidth
#     B = ws.Columns('B:B').ColumnWidth
#     C = ws.Columns('C:C').ColumnWidth
#     D = ws.Columns('D:D').ColumnWidth
#     E = ws.Columns('E:E').ColumnWidth
#     F = ws.Columns('F:F').ColumnWidth
#     G = ws.Columns('G:G').ColumnWidth
#     H = ws.Columns('H:H').ColumnWidth
#     I = ws.Columns('I:I').ColumnWidth
#
#     LM = ws.PageSetup.LeftMargin
#     RM = ws.PageSetup.RightMargin
#     TM = ws.PageSetup.TopMargin
#     BM = ws.PageSetup.BottomMargin
#
#     '''
# With ActiveSheet.PageSetup
#     .LeftHeader = ""
#     .LeftMargin = Application.InchesToPoints(0.25)
#     .RightMargin = Application.InchesToPoints(0.25)
#     .TopMargin = Application.InchesToPoints(0.75)
#     .BottomMargin = Application.InchesToPoints(0.75)
#     '''
#
#     for i in range(model.rowCount() - 1):
#         wb.Worksheets.Add()
#         ws = wb.Worksheets(1)
#         ws.Columns('A:A').ColumnWidth = A
#         ws.Columns('B:B').ColumnWidth = B
#         ws.Columns('C:C').ColumnWidth = C
#         ws.Columns('D:D').ColumnWidth = D
#         ws.Columns('E:E').ColumnWidth = E
#         ws.Columns('F:F').ColumnWidth = F
#         ws.Columns('G:G').ColumnWidth = G
#         ws.Columns('H:H').ColumnWidth = H
#         ws.Columns('I:I').ColumnWidth = I
#
#         wb.ActiveSheet.Paste()
#
#         '''
#         ws.PageSetup.LeftMargin = LM
#         ws.PageSetup.RightMargin = RM
#         ws.PageSetup.TopMargin = TM
#         ws.PageSetup.BottomMargin = BM
# '''

    sub_ver_prot(int(model.record(0).field('item').value()),ws,nn,info)

    # # Удаление лишних закладок
    # nList = wb.Worksheets.count - model.rowCount()
    # for i in range(nList):
    #     ws = wb.Worksheets(model.rowCount() + 1)
    #     ws.Delete()
    #
    # return
    #
    # # # Печать с архива и тестирования
    # # for i in range(model.rowCount()):
    # #     sub_ver_prot(db, xl, wb, ws, test_map, int(model.record(i).field('item').value().toString()), i)
    # #
    # #     if visibleExcel == False:
    # #         xl.ActiveWindow.SelectedSheets.PrintOut()
    # #
    # #     if i != model.rowCount() - 1:
    # #         for i in range(model_3.rowCount() - 1):
    # #             ws.Rows(str(nrPogr)).EntireRow.Delete()
    #
    # if visibleExcel == False:
    #     wb.Close(SaveChanges=False)
    #     xl.Quit()


def sub_ver_prot(item,ws, nn, info):
    global name_msr_etalon
    global name_msr_vspom
    global decimal_point
    xl = Excel
    query = QSqlQuery(db)

    ''' 12.08.2021
    #Параметры    
    strSQL = """                
select * from params 
"""                
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки Разрешения на допуск в эксплуатацию и регистрационного номера", QMessageBox.Ok)
    else:    
        model_2.setQuery(query)

    for i in range(model_2.rowCount()):
        if int(model_2.record(i).field('id').value().toString()) == 1:
            ws.Range('B5').Select()
            xl.Selection.Value = unicode(model_2.record(i).field('name').value().toString())
        if int(model_2.record(i).field('id').value().toString()) == 2:
            ws.Range('B6').Select()
            xl.Selection.Value = unicode(model_2.record(i).field('name').value().toString())
'''

    # Параметры
    strSQL = """                
select * from params order by date_begin
"""
    print(221,strSQL)
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение",
                            u"Ошибка выборки Разрешения на допуск в эксплуатацию и регистрационного номера",
                            QMessageBox.Ok)
    else:
        model_2.setQuery(query)

    for i in range(model_2.rowCount()):
        if int(model_2.record(i).field('clsparams').value()) == 1 and QDateTime(model_2.record(i).field(
                'date_begin').value()) <= model.record(nn).field('createdatetime').value():
            ws.Range('B5').Select()
            xl.Selection.Value = model_2.record(i).field('name').value()
        if int(model_2.record(i).field('clsparams').value()) == 2 and   QDateTime(model_2.record(i).field(
                'date_begin').value()) <= model.record(nn).field('createdatetime').value():
            ws.Range('B6').Select()
            xl.Selection.Value = model_2.record(i).field('name').value()
    # return

    #    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toDate().toString("dd.MM.yyyy"))

    ws.Range('A7').Select()
    xl.Selection.Value = f"ПРОТОКОЛ ПОВЕРКИ № 20{model.record(nn).field('makedate').value()} /{model.record(nn).field('rn').value()} ППТ "
    ws.Range('C8').Select()
    xl.Selection.Value = model.record(nn).field('ShortName').value()
    ws.Range('B9').Select()
    xl.Selection.Value = f"{model.record(nn).field('makedate').value()}-{model.record(nn).field('serialnumber').value()}"
    ws.Range('E9').Select()
    # 5.04.2022    xl.Selection.Value = '20' + unicode(model.record(nn).field('makedate').value().toString())
    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toString("yyyy"))
    # Класс точности
    strSQL = f"""                
select classaccuracy from coil 
where transformer =  {model.record(nn).field('transformer').value()}
order by coilnumber                  
"""
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)
    if model_2.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных_ _!", QMessageBox.Ok)

    classaccuracy = ''
    for i in range(model_2.rowCount()):
        'classaccuracy = ' + model_2.record(i).field('classaccuracy').value()
        classaccuracy += model_2.record(i).field('classaccuracy').value() + '/'

    classaccuracy = classaccuracy[0:len(classaccuracy) - 1]

    #    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    ws.Range('B10').Select()
    xl.Selection.Value = classaccuracy

    # Первичный ток
    strSQL = f"""                
select distinct primarycurrent from coil 
where transformer = {model.record(nn).field('transformer').value()} 
--order by coilnumber                  
"""
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)
    if model_2.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных_ _ _!", QMessageBox.Ok)

    primarycurrent = ''
    for i in range(model_2.rowCount()):
        #        print 'classaccuracy = ' + unicode(model_2.record(i).field('primarycurrent').value().toString())
        primarycurrent += f"{int(model_2.record(i).field('primarycurrent').value())}/"

    primarycurrent = primarycurrent[0:len(primarycurrent) - 1]

    #    QMessageBox.warning(None, u"Предупреждение", u"3", QMessageBox.Ok)

    # Вторичный ток
    strSQL = f"""                
select distinct secondcurrent from coil 
where transformer = {model.record(nn).field('transformer').value()} 
--order by coilnumber                  
"""
    print
    strSQL
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)
    if model_2.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных_ _ _ _!", QMessageBox.Ok)

    secondcurrent = ''
    for i in range(model_2.rowCount()):
        secondcurrent += f"{int(model_2.record(i).field('secondcurrent').value())}/"
    secondcurrent = secondcurrent[0:len(secondcurrent) - 1]
    print(11111, primarycurrent , secondcurrent)
    #    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    ws.Range('G10').Select()
    xl.Selection.Value = primarycurrent + '/' + secondcurrent
    # '''

    #    QMessageBox.warning(None, u"Предупреждение", u"4", QMessageBox.Ok)

    #    QMessageBox.warning(None, u"Предупреждение111", name_msr_etalon, QMessageBox.Ok)

    #    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    ws.Range('E12').Select()
    xl.Selection.Value = name_msr_etalon
    # '''

    #    QMessageBox.warning(None, u"Предупреждение", u"5", QMessageBox.Ok)

    #    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    ws.Range('E13').Select()
    xl.Selection.Value = name_msr_vspom

    ws.Range('D15').Select()
    xl.Selection.Value = model.record(nn).field('temperature').value()
    ws.Range('D16').Select()
    xl.Selection.Value = model.record(nn).field('humidity').value()
    ws.Range('D17').Select()
    xl.Selection.Value = model.record(nn).field('pressure').value()
    ws.Range('F18').Select()
    xl.Selection.Value = model.record(nn).field('method').value()

    ws.Range('E32').Select()
    xl.Selection.Value = model.record(nn).field('poveritel').value()
    ws.Range('C33').Select()

    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toString("dd.MM.yyyy"))
    # '''
    # Погрешности
    strSQL = f"""                
select
   cl.coilnumber || 'И1-' || cl.coilnumber || 'И' || cl.Tap as fullCoilName
   , cl.coilnumber || 'И' as CoilName
   , primarycurrent
   , classaccuracy
   , 0.8 as cos
   , round(chk.point, 0) as point                                         
   , round(chk.a, 2) as a                                      
   , round(chk.p, 1) as p             
   , coalesce(chk.QuadroLoad, cl.SecondLoad) as SecondLoad
   , chk.QuadroLoad is not null as isQuadroLoad
   , chk.point = (select min(point) from checking where checking.coil = chk.coil) as isFirstPoint
   , cl.Tap            
from coil cl
left join checking chk on chk.coil = cl.id
where chk.item in (select item.id from item
        inner join test_map on test_map.id = item.test_map
        inner join stand on test_map.stand = stand.id 
where item.serial_number = {info['idSn']} and stand.test_type = 1)                                                                       
  and chk.point is not null                         
--order by cl.coilnumber, cl.Tap, chk.QuadroLoad is not null, chk.Point
--order by cl.coilnumber, secondload desc, round(chk.point, 0), primarycurrent
--order by primarycurrent, cl.coilnumber, secondload desc, round(chk.point, 0)
--order by cl.coilnumber, primarycurrent, secondload desc, round(chk.point, 0)
order by cl.coilnumber, cl.Tap, primarycurrent, secondload desc, round(chk.point, 0)

"""

    print(strSQL)
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:
        model_3.setQuery(strSQL)
    if model_3.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных_ _ _ _ _!", QMessageBox.Ok)

    nrPogr = 29

    #    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    ws.Range(f"A29:A{29 + model_3.rowCount() - 2}").EntireRow.Insert()
    sw1 = ''
    sw2 = ''

    M = []
    for i in range(model_3.rowCount()):
        M.append([model_3.record(i).field('fullCoilName').value(),
               model_3.record(i).field('primarycurrent').value(),
               '',
               model_3.record(i).field('classaccuracy').value(),
               model_3.record(i).field('cos').value(),
               model_3.record(i).field('secondload').value(),
               model_3.record(i).field('point').value(),
               model_3.record(i).field('a').value(),
               model_3.record(i).field('p').value()])

    n_empty1 = 0
    n_empty2 = 0
    for i in range(len(M)):
        pass
        '''       
        if M[i][0] != sw1:
            sw1 = M[i][0]
            if n_empty1 > 1:
                ws.Range("A" + str(nrPogr + i - 1 - n_empty1 ) + ":E" + str(nrPogr + i - 2)).Select()
                xl.Selection.Borders(4).LineStyle = 0
            n_empty1 = 0    
        else:     
            M[i][0] = ''
            M[i][1] = ''
            M[i][3] = ''
            M[i][4] = ''
            n_empty1 += 1

        if M[i][5] != sw2:
            sw2 = M[i][5]
            if n_empty2 > 1:
                ws.Range("F" + str(nrPogr + i - 1 - n_empty2 ) + ":F" + str(nrPogr + i - 2)).Select()
                xl.Selection.Borders(4).LineStyle = 0            
            n_empty2 = 0    
        else:
            M[i][5] = ''
            n_empty2 += 1            
        '''

        '''
        if M[i][0] != sw1:
            sw1 = M[i][0]

            sw2 = M[i][5]

            if n_empty1 > 1:
                ws.Range("A" + str(nrPogr + i - 1 - n_empty1 ) + ":E" + str(nrPogr + i - 2)).Select()
                xl.Selection.Borders(4).LineStyle = 0
            n_empty1 = 0    
        else:     
            M[i][0] = ''
            M[i][1] = ''
            M[i][3] = ''
            M[i][4] = ''
            n_empty1 += 1


            if M[i][5] != sw2:
                sw2 = M[i][5]
                if n_empty2 > 1:
                    ws.Range("F" + str(nrPogr + i - 1 - n_empty2 ) + ":F" + str(nrPogr + i - 2)).Select()
                    xl.Selection.Borders(4).LineStyle = 0            
                n_empty2 = 0    
            else:
                M[i][5] = ''
                n_empty2 += 1            
        '''

    if True:
        # Очищение повторяющихся знаений
        n = model_3.rowCount()
        print(3323,M)
        for i in range(n):
            if i != n - 1:
                if M[n - i - 1][0] == M[n - i - 2][0]:
                    M[n - i - 1][0] = ''
                    if M[n - i - 1][1] == M[n - i - 2][1]:
                        M[n - i - 1][1] = ''
                    if M[n - i - 1][2] == M[n - i - 2][2]:
                        M[n - i - 1][2] = ''
                    if M[n - i - 1][3] == M[n - i - 2][3]:
                        M[n - i - 1][3] = ''
                    if M[n - i - 1][4] == M[n - i - 2][4]:
                        M[n - i - 1][4] = ''
                    if M[n - i - 1][5] == M[n - i - 2][5]:
                        M[n - i - 1][5] = ''


        # Объединение очищеных ячеек
        endUnion = n - 1
        for i in range(n):
            if M[n - i - 1][0] != '':
                endUnion -= 1
                if endUnion != n - i - 2:
                    ws.Range("A" + str(n - i - 2 + 30) + ":A" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2

        '''                    
        endUnion = n - 1                
        for i in range(n):
            if M[n-i-1][1] != '':
                endUnion -= 1                
                if endUnion != n - i - 2:
                    ws.Range("B" + str(n - i - 2 + 30) + ":C" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    print 'Merge'
                    endUnion = n - i - 2                
        '''
        endUnion = n - 1
        for i in range(n):
            if M[n - i - 1][1] != '':
                endUnion -= 1
                ws.Range("B" + str(n - i - 2 + 30) + ":C" + str(endUnion + 30)).Select()
                xl.Selection.VerticalAlignment = 2
                xl.Selection.Merge()
                print
                'Merge'
                endUnion = n - i - 2

        endUnion = n - 1
        for i in range(n):
            if M[n - i - 1][3] != '':
                endUnion -= 1
                if endUnion != n - i - 2:
                    ws.Range("D" + str(n - i - 2 + 30) + ":D" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2

        endUnion = n - 1
        for i in range(n):
            if M[n - i - 1][4] != '':
                endUnion -= 1
                if endUnion != n - i - 2:
                    ws.Range("E" + str(n - i - 2 + 30) + ":E" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2

        endUnion = n - 1
        for i in range(n):
            if M[n - i - 1][5] != '':
                endUnion -= 1
                if endUnion != n - i - 2:
                    ws.Range("F" + str(n - i - 2 + 30) + ":F" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2

                #        ws.Range("A" + str(7) + ":I" + str(6 + len(M))).Select()
    #        xl.Selection.HorizontalAlignment = 3

    ws.Range("H" + str(nrPogr) + ":H" + str(nrPogr + len(M) - 1)).Select()

    #    Application.UseSystemSeparators = False

    #    xl.Selection.NumberFormat = "0,00"
    print
    'decimal_point = ' + decimal_point
    xl.Selection.NumberFormat = "0" + decimal_point + "00"

    #    print locale.localeconv()['decimal_point']

    ws.Range("A" + str(nrPogr) + ":I" + str(nrPogr + len(M) - 1)).Select()
    xl.Selection.Value = M

    '''    
    for i in range(model_3.rowCount() - 1):
        ws.Range('B' + str(nrPogr + i) + ':C' + str(nrPogr + i)).Select()
        xl.Selection.merge(True)
'''


def data_TP(func):
    sql_params = """select name from params
                    order by date_begin DESC
                    limit 1"""
    quer = QSqlQuery(sql_params)
    if quer.first():
        doc  = quer.value(0)
        print(111111,doc)

    # регистрационный номер
    sqlN = "select name from params where clsparams = 2 order by date_begin, id"
    quer = QSqlQuery(sqlN)
    if quer.first():
        lisnum = quer.value(0)


    if model.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет да5нных!", QMessageBox.Ok)
        return

    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()
    for i in range(model.rowCount()):
        nomer = f"{model.index(i, 6).data()}-{model.index(i, 5).data()}"
        item = model.index(i,13).data()
        shname = model.index(i,3).data()
        year = model.index(i,8).data().toString('yyyy')
        data = model.index(i,8).data().toString('dd.MM.yyyy')
        temp = int(model.index(i,9).data())
        hum = int(model.index(i,10).data())
        pres = int(model.index(i,11).data())
        idTr = model.index(i,12).data()
        oper = model.index(i,14).data()
        # num_protokol = "ПРОТОКОЛ ПОВЕРКИ  № " + str(year) +"/" +  str(model.index(i,0).data()) + " ППТ"
        num_protokol = str(model.index(i, 0).data())
        tu = model.index(i,7).data()
        sn = model.index(i, 5).data()
        test = model.index(i, 16).data()
        name_defect = model.index(i, 17).data()
        supervisor = model.index(i, 18).data()
        test_map = model.index(i, 1).data()
        method = model.index(i, 19).data()
        type_tr = model.index(i, 20).data()

        print(1111111111111111111,num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr)
        func(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum,type_tr )
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass

def fill_TPprotocol_full(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr):
    sheet = wb.ActiveSheet
    position = 22
    coil_name = parser_name_tt(item)
    coil = parse_result_tt(item, coil_name)
    if coil == False:
        if getTrue(None, 'Не удается сопоставить id обмоток трансформатора c id результатами \n распечатать пустой?'):
            fill_TTprotocol_blank(num_protokol, item, shname, year, data, temp, hum, pres, oper, doc, nomer, tu, sn,
                                  idTr, test, name_defect, test_map, supervisor, method, lisnum, type_tr)
        return
    sheet.Cells(9, 1).Value = f"Заводской № {nomer}"
    sheet.Cells(4, 2).Value = doc
    sheet.Cells(13, 5).Value = tu
    sheet.Cells(6, 1).Value = "ПРОТОКОЛ №" + year + "/" + num_protokol + 'ПСИ'
    sheet.Cells(9, 5).Value = year
    sheet.Cells(8, 2).Value = shname
    if temp == 0:
        temp =  None
    if hum ==0:
        hum = None
    if pres == 0:
        pres = None
    sheet.Cells(12, 2).Value = temp
    sheet.Cells(12, 5).Value = hum
    sheet.Cells(12, 8).Value = pres
    sheet.Cells(25, 2).Value = data
    # записываем операторов испытаний (высоковольтные и пси тн)
    operator = searchHV(item,5)
    sheet.Cells(21, 7).Value = f"{operator[0]} \n {operator[1]}"

    # записываем контролера
    controler = searchHV(item,23)
    sheet.Cells(17, 7).Value = f"{controler[0]}\n {controler[1]}"
    # Меняем заключение если обнаружен деффект
    print(44455, test, name_defect)
    if name_defect != "":
        sheet.Cells(26, 2).Value = str(name_defect).capitalize()
    # работаем с сопротивлением
    count = len(coil) - 2 # количество добавленных строк для результатов сопротивления
    if len(coil) > 1:
        corT = f"C{position}:C{position + count}"
        sheet.Range(corT).EntireRow.Insert()
        sheet.Range(f"A23:B{position + count}").Merge()
        for i in range(position, position + count + 1):  # объединение строк
            sheet.Range(f"C{i}:E{i}").Merge()
    for key in coil:
        data = [coil[key][5],None,  None, toFixed(coil[key][10],3)]
        sheet.Range(f"C{position-1}:F{position-1}").Value = data
        position +=1
    # print(1112,position , count)
    # записываем результаты намагничивания
    if len(coil) > 1:
        corT = f"A{position}:A{position + count}"
        sheet.Range(corT).EntireRow.Insert(Shift=Excel_const.xlDown, CopyOrigin=Excel_const.xlFormatFromRightOrBelow)

    for key in coil:
        print(91,position)
        sheet.Range(f"A{position}:B{position}").Merge()
        print(3333, coil)
        data = [coil[key][5], None,   toFixed(coil[key][8],4),None, toFixed(coil[key][7],2), toFixed(coil[key][11], 1)]
        sheet.Range(f"A{position}:F{position}").Value = data
        print(909,position)
        position += 1

    hv = searchHV(item)
    sheet.Range("C18:G18").Value = [f"Uисп = 3 кВ \n t = 1 мин", None, 'Не менее', 'cоответствует', f'{hv[0]} \n {hv[1]}']


#формирование словаря для создание отдельной таблицы с обмотками класса точночти pr pz и т.д
def extra_options(coil,item, test_type = 25):
    model_result = QSqlQueryModel()
    sql = f"""select test_tc.coil, test_tc.rct, test_tc.ts, test_tc.kr, test_tc.ie,test_tc.ek  from test_tc where item in
                    (select t2.item from (select test_map.id,  t1.id as item, t1.istested,t1.createdatetime, stand.test_type, t1.acceptdatetime  from test_map
                                    inner join 
                                            (select test_map , item.id, item.istested, item.createdatetime , item.acceptdatetime from item
                                                where serial_number in (select serial_number from item where id =  {item})
                                                and item.istested
                                                order by item.acceptdatetime DESC
                                                )t1 on test_map.id = t1.test_map
                                    inner join stand on test_map.stand = stand.id
                                    where test_type = {test_type}
                                    order by t1.acceptdatetime 
                                    limit 1)t2
                    where t2.istested)"""

    print(sql)
    model_result.setQuery(sql)
    def get_resultDD(model,name, id):
        if model.rowCount() == 0:
            return None
        for i in range(model_result.rowCount()):
            print(235,i, model.index(i,0).data())
            if model.index(i,0).data() == id:
                return model.index(i,name).data()

    extra_params = {'Rct': {}, 'Kr': {}, 'Ts': {}, 'Kssc': {}, 'Ek':{}, 'Ie':{}}
    for i in coil:
        print(7546,i)
        if coil[i][3].count('PR'):
            extra_params['Rct'][i]  = str(toFixed(get_resultDD(model_result,1,i),3))
            extra_params['Ts'][i]  = str(toFixed(get_resultDD(model_result,2,i),3))
            extra_params['Kr'][i] = str(toFixed(get_resultDD(model_result,3,i),2))
        if coil[i][3].count('PX'):
            extra_params['Rct'][i]  = str(toFixed(get_resultDD(model_result,1,i),3))
            extra_params['Ek'][i]  =  str(toFixed(get_resultDD(model_result,5,i),3))
            extra_params['Ie'][i] =   str(toFixed(get_resultDD(model_result, 4, i),4))


    print(475754, extra_params)
    return extra_params





def fill_TTprotocol_blank(num_protokol, item, shname, year, data, temp, hum, pres, oper, doc, nomer, tu, sn, idTr, test,
                         name_defect, test_map, supervisor, method, lisnum, type_tr):
    sheet = wb.ActiveSheet
    position = 24
    sheet.Cells(9, 1).Value = f"Заводской № {nomer}"
    sheet.Cells(4, 2).Value = doc
    sheet.Cells(13, 5).Value = tu
    sheet.Cells(6, 1).Value = "ПРОТОКОЛ №" + year + "/" + num_protokol + 'ПСИ'
    sheet.Cells(9, 5).Value = year
    sheet.Cells(8, 2).Value = shname

    # работаем с сопротивлением
    coil = parser_name_tt(item)

    count = len(coil) - 2  # количество добавленных строк для результатов сопротивления
    if len(coil) > 1:
        corT = f"C{position}:C{position + count}"
        sheet.Range(corT).EntireRow.Insert()
        sheet.Range(f"A23:B{position + count}").Merge()
        for i in range(position, position + count + 1):  # объединение строк
            sheet.Range(f"C{i}:E{i}").Merge()
    for key in coil:
        data = [coil[key][5], None, None, None]
        sheet.Range(f"C{position - 1}:F{position - 1}").Value = data
        position += 1
    # print(1112,position , count)
    # записываем результаты намагничивания
    if len(coil) > 1:
        corT = f"A{position}:A{position + count}"
        sheet.Range(corT).EntireRow.Insert(Shift=Excel_const.xlDown, CopyOrigin=Excel_const.xlFormatFromRightOrBelow)

    for key in coil:
        sheet.Range(f"A{position}:B{position}").Merge()
        sheet.Range(f"A{position}").Value = coil[key][5]
        position += 1

    # удаляем Uисп для первичной обмотки для трансофрматоров типи тв и тш
    if type_tr in (1, 6):
        if type_tr == 1:
            hv = searchHV(item, 5)
        else:
            hv = searchHV(item)
        sheet.Rows(20).EntireRow.Delete()
        sheet.Rows(18).EntireRow.Delete()
        sheet.Range("B19:D19").ClearContents()
        sheet.Range("B19:B20").Merge()
        sheet.Range("C19:D20").Merge()
        sheet.Range("C18:G18").Value = [f"Uисп = 3 кВ \n t = 1 мин", None, 'Не менее', 'cоответствует',
                                        None]


    else:
        hv = searchHV(item)
        print("____________________", hv)
        sheet.Range("E18:G18").Value = ['Не менее', 'cоответствует', None]
        sql = f"""select t1.type_isolation, prime_test_voltage, second_test_voltage,  prime_test_voltage2  from testing_voltage inner join
                            (select transformer, type_transformer.type_transform, transformer.voltage, transformer.isolationlevel,
                            CASE
                                WHEN isolationlevel IS Null or isolationlevel = 'б' THEN 'б'
                                ELSE 'а'
                                end type_isolation
                        from serial_number
                            INNER JOIN transformer ON serial_number.transformer = transformer.id
                            INNER JOIN type_transformer ON transformer.type_transformer = type_transformer.id
                        where serial_number.id in (select serial_number from item where id = {item}))t1
                        on t1.voltage = testing_voltage.nominal_voltage and t1.type_isolation = testing_voltage.isolation_level"""
        print(sql)

        oQuerry = QSqlQuery(sql)
        if oQuerry.first():
            sheet.Cells(18, 3).Value = f"Uисп = {int(oQuerry.value(1))} кВ \n t = 1 мин"
            sheet.Cells(19, 3).Value = f"Uисп = {int(oQuerry.value(2))} кВ \n t = 1 мин"
            if oQuerry.value(0) in (None, 'б'):
                print("удаляем")
                sheet.Rows(20).EntireRow.Delete()
            # записываем уровень чр
            else:
                sheet.Cells(20, 3).Value = f"Uисп = {oQuerry.value(3)} кВ"
                sheet.Cells(20, 6).Value = get_vv_result(sn, year[2:])


def get_vv_result(sn,year):
    sql = f"""select pdl from checking_3 where checking_3.item in
    (select item.id from item
    where serial_number  in  
                (select id from serial_number where serialnumber = {sn} and makedate = {year}))"""

    print(sql)

    quer = QSqlQuery(sql)
    if quer.first():
        result = toFixed(quer.value(0),1)
        return result
    return None



#     Расчет контрольной цифры в штрихкоде EAN-13
#
#     Шаг 1     Отбросить контрольный разряд (крайний справа)
#     Шаг 2     Сложить разряды, стоящие на четных местах
#     Шаг 3     Результат ШАГа 2 умножить на 3
#     Шаг 4     Сложить разряды, стоящие на нечетных местах
#     Шаг 5     Суммировать результаты ШАГов 3 и 4
#     Шаг 6     В полученном числе крайнюю справа цифру вычесть из 10. Полученный результат и есть значение контрольной цифры
#     Пример расчета контрольного разряда в коде EAN-13: 46 76221 35746 С
#     Шаг 1     46 76221 35746
#     Шаг 2     6+6+2+3+7+6=30
#     Шаг 3     30х3=90
#     Шаг 4     4+7+2+1+5+4=23
#     Шаг 5     90+23=113
#     Шаг 6     10-3=7
#     Полный номер EAN-13 будет следующим: 46 76221 35746 7
# """


# преобразовние штрих_кода
def varToInt(_symbol):
    try:
        res = int(_symbol)
    except:
        res = 0
    return res
def check_EAN_valid(_serNum):

    arrNum = []
    for item in _serNum:
        arrNum.append(varToInt(item))
    res = (arrNum[1] + arrNum[3] + arrNum[5] + arrNum[7] + arrNum[9] + arrNum[11]) * 3
    res = res + (arrNum[0] + arrNum[2] + arrNum[4] + arrNum[6] + arrNum[8] + arrNum[10])
    res = varToInt(str(res)[len(str(res)) - 1])
    if res > 0:
        res = 10 - res

    sernum = ''.join(map(str,arrNum))[:-1] + str(res)
    sn = f'''="("&{sernum}&")"'''

    # sn = sernum
    return sn

# # #
# from PyQt5.QtWidgets import QApplication
# import sys
# # # # #
# pp = QApplication(sys.argv)
# #
# if open_excel('passportTT.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportTT(2106328,fill_passportTT_full)
# #
# # # select_result(2026505)
# # # select_result(1917078)
# # # if open_excel('poverkaTT.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
# # #     TTpoverka(fill_poverkaTT_full)
# # # #
# select_result(2123224)
# if open_excel('protocolTP.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     data_TP(fill_TPprotocol_full)
# #

# # if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 0):
# #     data_TN(fill_TNpoverka)
# #     printRep()
# # #
# select_result(2006211)
# if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 1):
#     data_TN(fill_TNpoverka_blank)
# # 2012088
# # # # 2012089
# if open_excel('passportTP.xlsx', None):
#     select_passportTP(2123224, fill_passportTP_full)
#
# if open_excel('ticket_tp.xlsx', None):
#     select_passportTP(2123224, fill_ticket_tp)