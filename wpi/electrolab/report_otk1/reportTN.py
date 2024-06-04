import datetime
import time

import win32print
from win32com.client import constants as const
import win32com.client
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from electrolab.gui.Config_base import   db
# from Config_base import   db
# Основные объекты VBA http://bourabai.ru/einf/vba/2-04.htm

model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
windings = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
windingsKT = ["A-a2", "A-a3", "A-a4", "A-a5", "A-a6", "A-a7", "A-a8"]


sqrtPOV = {} # словарь сопоставления  корней к числам используется для поверки ТН
model_sqrt = QSqlQueryModel()
sql = 'select float_value, str_value  from parity_tabletn'
model_sqrt.setQuery(sql)
for i in range(model_sqrt.rowCount()):
    sqrtPOV[float(model_sqrt.index(i,0).data())] = model_sqrt.index(i,1).data()




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



import math

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




def open_excel(name_file, name_printer, visible = 1):
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

def repMoveTask(zakaz, series, spisok):
        try:
            try:
                xl = win32com.client.Dispatch("Excel.Application")
            except:
                print("Не запускается Excel")
                return

            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)
            ws.Name = u'ОТЧЕТ О ПРОХОЖДЕНИИ ЗАКАЗА'

            ws.PageSetup.Orientation = 2

            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42

            ws.Cells(1, 1).ColumnWidth = 12
            ws.Cells(1, 2).ColumnWidth = 20
            ws.Cells(1, 3).ColumnWidth = 20
            ws.Cells(1, 4).ColumnWidth = 20
            ws.Cells(1, 5).ColumnWidth = 20
            ws.Cells(1, 6).ColumnWidth = 20
            ws.Cells(1, 7).ColumnWidth = 20

            ws.Range('A1:G1').Select()
            xl.Selection.Font.Size = 16
            xl.Selection.Merge()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Value = u'ОТЧЕТ О ПРОХОЖДЕНИИ ЗАКАЗА'
            ws.Range('F2:G2').Select()
            xl.Selection.Merge()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Value = u'Дата ' + str(datetime.date.today().day) + '.' + str(
                datetime.date.today().month) + '.' + str(datetime.date.today().year)

            ws.Range('A3').Select()
            xl.Selection.HorizontalAlignment = 4
            xl.Selection.Value = u'Заказ №: '
            ws.Range('B3').Select()
            xl.Selection.HorizontalAlignment = 2
            xl.Selection.Value = str(zakaz)

            ws.Range('A4').Select()
            xl.Selection.HorizontalAlignment = 4
            xl.Selection.Value = u'Серия: '
            ws.Range('B4').Select()
            xl.Selection.HorizontalAlignment = 2
            xl.Selection.Value = str(series)

            nr = 5
            ws.Range('A' + str(nr) + ':G' + str(nr)).Select()
            xl.Selection.VerticalAlignment = 2
            xl.Selection.HorizontalAlignment = 3

            ws.Range('A' + str(nr)).Select()
            xl.Selection.Value = u'№ тр-ра'
            ws.Range('B' + str(nr)).Select()
            xl.Selection.Value = u'измерение \n сопротивления\n первичной\n обмотки в цеху'
            ws.Range('C' + str(nr)).Select()
            xl.Selection.Value = u'измерение\n погрешности\n в цеху'
            ws.Range('D' + str(nr)).Select()
            xl.Selection.Value = u'измерение\n сопротивления\n обмоток\n и погрешности в цеху'
            ws.Range('E' + str(nr)).Select()
            xl.Selection.Value = u'Высоковольтные\n испытания'
            ws.Range('F' + str(nr)).Select()
            xl.Selection.Value = u'измерение сопротивления,\n холостого хода\n и поверка в ЭТЛ'
            # ws.Range('G' + str(nr)).Select()
            # xl.Selection.Value = u'Поверка\nв ЭТЛ'

            ws.Range('A' + str(nr) + ':F' + str(nr + len(spisok))).Select()
            xl.Selection.VerticalAlignment = 1
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1

            nr += 1

            for i in range(len(spisok)):
                ws.Range('A' + str(nr + i)).Select()
                xl.Selection.VerticalAlignment = 2
                xl.Selection.HorizontalAlignment = 3
                # print 'spisok[i][0] = ', spisok[i][0]
                xl.Selection.Value = spisok[i][0]
                #                xl.Selection.Value = spisok[i][1][0][0]
                #                ws.Range('C' + str(nr + i)).Select()
                #                xl.Selection.Value = spisok[i][1][0][1]

                ws.Range('B' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][1])):
                    if j > 0:
                        s1 += '\n'
                    test = ''
                    #                    if not bool(spisok[i][1][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][1][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][1][j][0] + test + '\n' + spisok[i][1][j][1]
                    if spisok[i][1][j][4] != '':
                        s1 += '\n' + spisok[i][1][j][4]
                xl.Selection.Value = s1

                ws.Range('C' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][2])):
                    if j > 0:
                        s1 += '\n'
                    test = ''
                    #                    if not bool(spisok[i][2][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][2][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][2][j][0] + test + '\n' + spisok[i][2][j][1]
                    if spisok[i][2][j][4] != '':
                        s1 += '\n' + spisok[i][2][j][4]
                xl.Selection.Value = s1

                ws.Range('D' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][3])):
                    if j > 0:
                        s1 += '\n'
                    test = ''
                    # print 'spisok[i][3][j][2] = ', spisok[i][3][j][2]
                    #                    if not bool(spisok[i][3][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][3][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][3][j][0] + test + '\n' + spisok[i][3][j][1]
                    if spisok[i][3][j][4] != '':
                        s1 += '\n' + spisok[i][3][j][4]
                xl.Selection.Value = s1

                ws.Range('E' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][4])):
                    if j > 0:
                        s1 += '\n'
                    test = ''

                    #                    if not bool(spisok[i][4][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][4][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][4][j][0] + test + '\n' + spisok[i][4][j][1]
                    if spisok[i][4][j][4] != '':
                        s1 += '\n' + spisok[i][4][j][4]
                xl.Selection.Value = s1

                ws.Range('F' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][5])):
                    if j > 0:
                        s1 += '\n'
                    test = ''

                    #                    if not bool(spisok[i][5][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][5][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][5][j][0] + test + '\n' + spisok[i][5][j][1]

                    if spisok[i][5][j][4] != '':
                        s1 += '\n' + spisok[i][5][j][4]

                xl.Selection.Value = s1

                ws.Range('G' + str(nr + i)).Select()
                s1 = ''
                for j in range(len(spisok[i][6])):
                    if j > 0:
                        s1 += '\n'
                    test = ''

                    #                    if not bool(spisok[i][6][j][2]):
                    #                        test = u' (анулир)'
                    if bool(spisok[i][6][j][3]):
                        test = u' (брак)'
                    s1 += spisok[i][6][j][0] + test + '\n' + spisok[i][6][j][1]
                    if spisok[i][6][j][4] != '':
                        s1 += '\n' + spisok[i][6][j][4]
                xl.Selection.Value = s1
        except:
            print("Неопознанная ошибка7 ... ")



















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
                stand.test_type = 19
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





def check_printer(excel, namePrint):
    for i in range(100):
        try:
            global np
            np = f'{namePrint} (Ne{i:02}:)'
            print(np)
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
    return f"{numObj:.{digits}f}"


# поиск оператора проводившего высокольтные испытания

def searchHV(sn, test_type = 8 ):
    sql1 = f"""select
                fio, t3.createdatetime
                from operator inner
                join
                (select stand.fullname, stand.test_type, t2.operator, t2.createdatetime
                from stand inner join
                (select test_map.id, test_map.stand, test_map.createdatetime, test_map.operator
                from test_map inner join
                (select id, serial_number, test_map, createdatetime from item
                where serial_number  in (select id from serial_number where id = {sn}) )
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
        wb.PrintOut()
        Excel.Visible = True
        Print = Excel.ActivePrinter
        namePrint = Print[:-8]
        status = win32print.GetPrinter(win32print.OpenPrinter(namePrint), 2)['Status']
        if status not in (0,1024,16384) :
            QMessageBox.warning(None, f"Ошибка печати",
                                f"Проверьте работу принтера", QMessageBox.Ok)
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
        modelTT = QSqlQueryModel()
        sql = f"""select * from coil
                where transformer in (select serial_number.transformer from item
                                            inner join serial_number on item.serial_number = serial_number.id
                                        where item.id = {item})
                                        order by coilnumber"""
        print(sql)
        modelTT.setQuery(sql)
        winding = {}
        voltage = {'primary':None, 'second': []}
        sumI = 0
        sumD = 0
        for i in range(modelTT.rowCount()):
            winding[modelTT.index(i,0).data()] = {}
            winding[modelTT.index(i, 0).data()]['coilnumber'] = int(modelTT.index(i,2).data())
            winding[modelTT.index(i, 0).data()]['tap'] = int(modelTT.index(i, 3).data())
            winding[modelTT.index(i, 0).data()]['secload'] = modelTT.index(i, 8).data()
            winding[modelTT.index(i, 0).data()]['seccur'] = modelTT.index(i, 7).data()
            winding[modelTT.index(i, 0).data()]['primary'] = modelTT.index(i, 6).data()
            voltage['primary'] = model.index(i, 6).data()
            if modelTT.index(i, 7).data() != 0:
                voltage['second'].append(modelTT.index(i, 7).data())
            clas = modelTT.index(i, 5).data()
            winding[modelTT.index(i, 0).data()]['class'] = clas
            if clas in ('3.0','3P','6P'):
                sumD +=1
            else:
                if winding[modelTT.index(i, 0).data()]['coilnumber'] != 0:
                    sumI += 1
        sI = 1
        sD = 1
        coilId = {}
        for i in winding.keys():
            if winding[i]['coilnumber'] == 0 and  winding[i]['tap'] == 0:
                text = ['A-X',None]
                coilId[i] = text
                idPerv = i
                continue
            elif winding[i]['class'] in ('3.0','3P','6P'):
                if sumD == 1:
                    text = ['aд-xд', winding[i]['class'],  winding[i]['secload'],   sqrtPOV[winding[i]['seccur']]]
                else:
                    text = ["aд{sD}-xд{sD}",  winding[i]['class'] , winding[i]['secload'], sqrtPOV[winding[i]['seccur']]]
                    sD += 1

            else:
                if sumI == 1:
                    text = ['a-x', winding[i]['class'] , winding[i]['secload'], sqrtPOV[winding[i]['seccur']]]
                else:
                    text = [f"a{sI}-x{sI}", winding[i]['class'] , winding[i]['secload'], sqrtPOV[winding[i]['seccur']]]
                    sI += 1
            # записываем в первичную обмотку напряжение
            try:
                coilId[idPerv][1] = sqrtPOV[winding[i]['primary']]
                voltage['primary'] = sqrtPOV[winding[i]['primary']]
            except:
                pass
            coilId[i] = text
        return  coilId , voltage



# ___________________________________________________________ПЕЧАТЬ ПАСПОРТОВ_____________________________________________
def select_passportTN(items,func,controler = False):
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
            transformer.climat
                from serial_number INNER JOIN
                (select item.id, serial_number  AS sn, item.acceptdatetime AS data, operator.fio as fio  from item
                inner join test_map on item.test_map = test_map.id
                left join operator on test_map.supervisor = operator.id
                where item.id in ({items}))t1
                ON serial_number.id =t1.sn
                INNER JOIN transformer ON serial_number.transformer = transformer.id
                INNER JOIN type_transformer on transformer.type_transformer = type_transformer.id"""
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
        info['maxPover'] = model.index(i, 21).data()
        info['type_transformer'] = model.index(i, 22).data()
        info['climat'] = model.index(i, 23).data()
        info['controler'] = controler



        for key in info:
            if info[key] == 0:
                if key == 'copperP':
                    info[key] = 6.4
                elif key == 'copperPN':
                    info[key] = 0.5
                else:
                    info[key] = ''

        func(info)
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass



def fill_passportTN_full(info):
    # заполняем паспор
    print(info)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38,1).Value = info['fullname']
    sheet.Cells(39, 1).Value = info['tu']
    sheet.Cells(43, 20).Value = info['tu']
    sheet.Cells(40, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(57, 7).Value = info['weight']
    sheet.Cells(10,17 ).Value = 'Декларация о соответствии '+  info['declaration']
    sheet.Cells(11, 17).Value = 'Номер в реестре СИ РФ ' + info['nr']
    sheet.Cells(51, 22).Value = info['interval']
    sheet.Cells(21, 21).Value = info['type']
    sheet.Cells(42, 25).Value = info['type']
    sheet.Cells(58, 25).Value = info['type']
    sheet.Cells(40, 12).Value = info['data']
    sheet.Cells(54, 24).Value = info['data']

    sheet.Cells(63, 27).Value = info['copperP']
    sheet.Cells(64, 20).Value = info['copperPN']
    sheet.Cells(50, 17).Value = info['method']


    if info['controler']:
        # записываем контроллера
        controler, data1 = searchHV(info['idItem'], 10)
        sheet.Cells(45, 24).Value = f"{controler} \n {data1}"
        print(12121, controler, data1)

    # записываем поверителя
    poveritel, data2 = searchPoveritel(info['idItem'])
    sheet.Cells(53, 24).Value = f"{poveritel} \n {data2}"



    sheet.Cells(30, 20).Value = check_EAN_valid(f"90{info['serialnumber']}20{info['makedate']}00")

    result = resultDictTT(info['idItem'], info['fullname'])
    resultR =  result['R']
    resultX = result['X']
    coil = parser_name_tt(info['idItem'])[0]
    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {} # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    print(11,countW)
    # countW = 6

    first, last = col_column(countW,8)
    for i in range(1,countW+1):
        print(112,i)
        if i != countW:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(43, sc)
        sc = sc+cor-1
        mx2 = sheet.Cells(43, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        sclst[i] = [x, f"{x}43:{y}43",cor]
        y = mx2.Address[1]
        print(11112,x,y)
        sheet.Range(f"{x}43:{y}43").Merge()
        sheet.Range(f"{x}46:{y}46").Merge()
        sheet.Range(f"{x}47:{y}47").Merge()
        sheet.Range(f"{x}48:{y}49").Merge()
        sheet.Range(f"{x}52:{y}53").Merge()
        sheet.Range(f"{x}54:{y}54").Merge()
        sheet.Range(f"{x}55:{y}55").Merge()



        if info['type_transformer'] in (10, 11):
            sheet.Range(f"{x}54:{x}55").Merge()
        sc +=1
    print(sclst)
    sheet.Range(f"G43:{y}55").Borders.LineStyle = True
    sheet.Range(f"G43:{y}55").HorizontalAlignment = -4108
    sheet.Range(f"G43:{y}55").VerticalAlignment = -4108
    print(sclst)
    for i in range(1,len(sclst)+1):
        koef = 32 / countW / sclst[i][2]
        # if i == len(sclst):
        #     koef = 32/countW/countW

        sheet.Range(sclst[i][1]).ColumnWidth = koef

    # закончили формировать_________________________________
    position = 1
    # записываем сопротивление
    print(sclst)
    for i in coil:
        if coil[i][0] == 'A-X':
            sheet.Range(f"{sclst[1][0]}43:{sclst[1][0]}52").Value = [[coil[i][0]], [None], [None],[coil[i][1]],[None], [None], [None],[None], [None], [resultR[coil[i][0]]]]
            position +=1
        else:
            #запоминаем координату для записи результатов холостого хода для обмоток(a-x,a1-x1)
            if coil[i][0] in ('a-x','a1-x1'):
                corxx = sclst[position][0]
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}52").Value = [[coil[i][0]], [None], [None],[coil[i][3]],[coil[i][1]], [coil[i][2]], [None],[None], [None], [resultR[coil[i][0]]]]
            position += 1

    sheet.Cells(44, 7).Value = info['voltage']
    sheet.Cells(45, 7).Value = info['maxvoltage']
    sheet.Cells(50, 7).Value = info['maxPover']


    # записываем холостой ход
    # если нол то меняем заземляемый на незаземляемый
    if info['type_transformer'] in (10, 11):
        sheet.Range('A1:AF100').Replace('заземляемый', 'незаземляемый')
        sheet.Cells(37,1).Value = 'ТРАНСФОРМАТОР НАПРЯЖЕНИЯ НЕЗАЗЕМЛЯЕМЫЙ'
        sheet.Cells(20,21).Value = 'НЕЗАЗЕМЛЯЕМЫЙ'
        # объединяем ячейки холостого хода
        sheet.Range("A54:N55").ClearContents()
        sheet.Range("A54:F55").Merge()
        sheet.Range("A54:F55").Borders.LineStyle = True
        sheet.Range("G54:H55").Merge()
        sheet.Range("G54:H55").Borders.LineStyle = True
        sheet.Range("K54:L55").Merge()
        sheet.Range("K54:L55").Borders.LineStyle = True
        sheet.Range("I54:J55").Merge()
        sheet.Range("I54:J55").Borders.LineStyle = True
        sheet.Cells(54, 1).Value = 'Ток холостого хода при Uн, А'

        try:
            sheet.Range(f"{corxx}54").Value = resultX[1]
            # sheet.Cells(f'{corxx}54').Value = resultX[1]
            # sheet.Cells(f'{corxx}54').HorizontalAlignment = -4108
            # sheet.Cells(f'{corxx}54').VerticalAlignment = -4108
        except Exception as ex:
            print(5767676767, ex)
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные холостого хода трансформатора  {info['fullname']}", QMessageBox.Ok)
    else:
        print(resultX)
        try:
            sheet.Range(f'{corxx}54:{corxx}55').Value = [[resultX[1.2]], [resultX[1.9]]]
        except:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные холостого хода трансформатора  {info['fullname']}", QMessageBox.Ok)

    # Схема и группа соединения обмоток
    print(44444,(countW * '/1' + (countW-1) * '-0')[1:] )
    sheet.Cells(56, 7).Value = (countW * '/1' + (countW-1) * '-0')[1:]

    # находим руковдство по эксплуатации
    sqlSP = f"""select transformer.type_transformer as tt, var_constr_isp as isp, climat as climat , type_transformersp.id as sp, type_transformersp.designation as designation, type_transformersp.manual as manual   from type_transformersp
                            inner join transformer on transformer.type_transformer =  type_transformersp.type_transformer
                            where transformer.id = {info['idTransformer']}"""

    print(sqlSP)
    modelSP = QSqlQueryModel()
    modelSP.setQuery(sqlSP)
    climat = modelSP.index(0,2).data()
    desigation = ''
    manual = ''
    for i in range(modelSP.rowCount()):
        print(312, modelSP.index(i, 1).data(), info['fullname'])
        if info['fullname'].count(modelSP.index(i, 1).data()):
            desigation = modelSP.index(i, 4).data()
            manual = modelSP.index(i, 5).data()
            break
        print(121, modelSP.index(i, 1).data())
        if modelSP.index(i, 1).data() in (None, ''):
            desigation = modelSP.index(i, 4).data()
            manual = modelSP.index(i, 5).data()

    if modelSP.rowCount() != 0:
        sheet.Cells(16, 20).Value = desigation
        sheet.Cells(37, 23).Value = manual
    else:
        QMessageBox.warning(None, f"Предупреждение", f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}", QMessageBox.Ok)


def fill_passportTN_blank(info):
    print(334563456436346436436)
    # заполняем паспор
    print(info)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38,1).Value = info['fullname']
    sheet.Cells(39, 1).Value = info['tu']
    sheet.Cells(43, 20).Value = info['tu']
    sheet.Cells(40, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(57, 7).Value = info['weight']
    sheet.Cells(10,17 ).Value = 'Декларация о соответствии '+  info['declaration']
    sheet.Cells(11, 17).Value = 'Номер в реестре СИ РФ ' + info['nr']
    sheet.Cells(51, 22).Value = info['interval']
    sheet.Cells(21, 21).Value = info['type']
    sheet.Cells(42, 25).Value = info['type']
    sheet.Cells(58, 25).Value = info['type']
    sheet.Cells(40, 12).Value = info['data']
    sheet.Cells(54, 24).Value = info['data']
    sheet.Cells(46, 24).Value = info['data']
    sheet.Cells(63, 27).Value = info['copperP']
    sheet.Cells(64, 20).Value = info['copperPN']
    sheet.Cells(50, 17).Value = info['method']

    sheet.Cells(30, 20).Value = check_EAN_valid(f"90{info['serialnumber']}20{info['makedate']}00")
    # result = resultDictTT(info['idItem'], info['fullname'])
    # resultR =  result['R']
    # resultX = result['X']
    coil = parser_name_tt(info['idItem'])[0]
    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {} # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    print(11,countW)
    # countW = 6

    first, last = col_column(countW,8)
    for i in range(1,countW+1):
        print(112,i)
        if i != countW:
            cor = first
        else:
            cor = last
        mx1 = sheet.Cells(43, sc)
        sc = sc+cor-1
        mx2 = sheet.Cells(43, sc)
        x = mx1.Address[1]
        y = mx2.Address[1]
        sclst[i] = [x, f"{x}43:{y}43",cor]
        y = mx2.Address[1]
        print(11112,x,y)
        sheet.Range(f"{x}43:{y}43").Merge()
        sheet.Range(f"{x}46:{y}46").Merge()
        sheet.Range(f"{x}47:{y}47").Merge()
        sheet.Range(f"{x}48:{y}49").Merge()
        sheet.Range(f"{x}52:{y}53").Merge()
        sheet.Range(f"{x}54:{y}54").Merge()
        sheet.Range(f"{x}55:{y}55").Merge()



        if info['type_transformer'] in (10, 11):
            sheet.Range(f"{x}54:{x}55").Merge()
        sc +=1
    print(sclst)
    sheet.Range(f"G43:{y}55").Borders.LineStyle = True
    sheet.Range(f"G43:{y}55").HorizontalAlignment = -4108
    sheet.Range(f"G43:{y}55").VerticalAlignment = -4108
    print(sclst)
    for i in range(1,len(sclst)+1):
        koef = 32 / countW / sclst[i][2]
        # if i == len(sclst):
        #     koef = 32/countW/countW

        sheet.Range(sclst[i][1]).ColumnWidth = koef

    # закончили формировать_________________________________
    position = 1
    sheet.Cells(44, 7).Value = info['voltage']
    sheet.Cells(45, 7).Value = info['maxvoltage']
    sheet.Cells(50, 7).Value = info['maxPover']
    # записываем холостой ход
    # если нол то меняем заземляемый на незаземляемый
    if info['type_transformer'] in (10, 11):
        sheet.Range('A1:AF100').Replace('заземляемый', 'незаземляемый')
        sheet.Cells(37,1).Value = 'ТРАНСФОРМАТОР НАПРЯЖЕНИЯ НЕЗАЗЕМЛЯЕМЫЙ'
        sheet.Cells(20,21).Value = 'НЕЗАЗЕМЛЯЕМЫЙ'
        # объединяем ячейки холостого хода
        sheet.Range("A54:N55").ClearContents()
        sheet.Range("A54:F55").Merge()
        sheet.Range("A54:F55").Borders.LineStyle = True
        sheet.Range("G54:H55").Merge()
        sheet.Range("G54:H55").Borders.LineStyle = True
        sheet.Range("K54:L55").Merge()
        sheet.Range("K54:L55").Borders.LineStyle = True
        sheet.Range("I54:J55").Merge()
        sheet.Range("I54:J55").Borders.LineStyle = True
        sheet.Cells(54, 1).Value = 'Ток холостого хода при Uн, А'

    # Схема и группа соединения обмоток
    print(44444,(countW * '/1' + (countW-1) * '-0')[1:] )
    sheet.Cells(56, 7).Value = (countW * '/1' + (countW-1) * '-0')[1:]

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
    query= QSqlQuery(sqlSP)
    if query.first() == 1:
        sheet.Cells(16, 20).Value = query.value(0)
        sheet.Cells(37, 23).Value = query.value(1)
    else:
        QMessageBox.warning(None, f"Предупреждение", f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}", QMessageBox.Ok)




# ___________________________________________________________КОНЕЦ  ПЕЧАТИ ПАСПОРТОВ_____________________________________________






def resultDictTT(item, name, nomer = None):
    tt_name = parser_name_tt(item)[0]
    result = {}
    # проверка id coil  на случай если изменили параметры трансформатора на тележке
    sql1 = f"""select DISTINCT coil from test_tt
                where item = {item}"""
    print(sql1)
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


# метод заполнения для этикетки с испытаний погрешности тт
def stickerTTP(test):
    # аргумент test обозначает название испытания R - СОПРОТИВЛЕНИЕ ПЕРВИЧНОЙ ОМБОТКИ, P - ИЗМЕРЕНИЕ ПОГРЕШНОСТИ, RP - измерение сопротивлений и погрешности


    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()

    for tr in range(model.rowCount()):

        nomer =   f"{model.index(tr, 3).data()}-{model.index(tr, 2).data()}"
        print(nomer)
        item = model.index(tr, 0).data()
        print(item)
        shname = model.index(tr, 4).data()
        print(shname)
        namest = model.index(tr, 6).data()
        print(namest)
        oper = model.index(tr, 5).data()
        print(oper)
        data = model.index(tr, 7).data().toString('dd.MM.yyyy')
        print(data)
        idtr = model.index(tr, 8).data()
        sheet = wb.ActiveSheet
        sheet.Cells(1, 1).Value = f"{nomer} {oper} {data}" # a1
        sheet.Cells(2, 1).Value = f"{namest}"       # a2
        result = resultDictTT(item,shname,nomer)
        if result:
            coilID = parser_name_tt(item)[0]
            positionY = 3
            if test in ('R', 'RP'):
                obm = [None]
                val = ['Rом']
                positionY = 3
                count = len(result['R'])
                for key, value in result['R'].items():
                    obm.append(key)
                    val.append(value)
                x = sheet.Cells(positionY,1)
                y = sheet.Cells(positionY,count+1)
                sheet.Range(sheet.Cells(positionY,1),sheet.Cells(positionY,count+1)).Value = obm
                positionY += 1
                sheet.Range(sheet.Cells(positionY,1), sheet.Cells(positionY,count+1)).Value = val
                sheet.Range(sheet.Cells(3,1),sheet.Cells(positionY,count+1)).Borders.LineStyle = True
                sheet.Range(sheet.Cells(3,1),sheet.Cells(positionY,count+1)).Font.Size = 36
                positionY += 1

            if test in ('P','RP'):
                if len(coilID) > 3:
                    collums = ['обм','BA','Un%','f(%)','Δ','f(%)','Δ']
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Value = collums
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Font.Size = 36
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Borders.LineStyle = True
                    positionY +=1
                    for coil in result.keys():
                        if coil in ('R','X'):
                            continue
                        count = len(result[coil]['P']['load']) * 2 -1
                        corT = f"A{positionY}:G{positionY+count}"
                        corO = f"A{positionY}:A{positionY+count}"
                        corData = f"B{positionY}:G{positionY}"
                        sheet.Range(corT).Insert()
                        sheet.Range(corT).Borders.LineStyle = True
                        sheet.Range(corO).Merge()
                        print(3333,coilID)
                        sheet.Cells(positionY,1).value = coilID[coil][0]
                        # сначала записываем все данные обмотки с 100 % нагрузкой
                        for i in result[coil]['P']['load']:
                            full = result[coil]['P']['load'][i]['full']
                            half = result[coil]['P']['load'][i]['half']
                            dataFull = [half[0], i,half[3],half[1],full[3],full[1]]
                            print(dataFull)
                            sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                            positionY += 1
                        # Заполняем 1/4 нагрузку
                        for i in result[coil]['P']['nload']:
                            full = result[coil]['P']['nload'][i]['full']
                            half = result[coil]['P']['nload'][i]['half']
                            dataFull = [half[0], i,half[3],half[1],full[3],full[1]]
                            print(dataFull)
                            sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                            positionY += 1
                else:
                    print('ЗАПОЛНЯЯЯЯЯЯЕМ')
                    collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ']
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Value = collums
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Font.Size = 36
                    sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Borders.LineStyle = True
                    positionY += 1
                    for coil in result.keys():
                        if coil in ('R', 'X'):
                            continue
                        count = len(result[coil]['P']['load']) * 2 - 1
                        corT = f"A{positionY}:E{positionY + count}"
                        corO = f"A{positionY}:A{positionY + count}"
                        corData = f"B{positionY}:E{positionY}"
                        sheet.Range(corT).Insert()
                        sheet.Range(corT).Borders.LineStyle = True
                        sheet.Range(corO).Merge()
                        sheet.Cells(positionY, 1).value = coilID[coil][0]
                        # сначала записываем все данные обмотки с 100 % нагрузкой
                        for i in result[coil]['P']['load']:
                            full = result[coil]['P']['load'][i]['full']
                            half = result[coil]['P']['load'][i]['half']
                            dataFull = [half[0], i, half[3], half[1]]
                            print(dataFull)
                            sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                            positionY += 1
                        # Заполняем 1/4 нагрузку
                        for i in result[coil]['P']['nload']:
                            full = result[coil]['P']['nload'][i]['full']
                            half = result[coil]['P']['nload'][i]['half']
                            dataFull = [half[0], i, half[3], half[1]]
                            print(dataFull)
                            sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                            positionY += 1

            sheet.Range("A3:G16").EntireColumn.AutoFit()
        if tr < model.rowCount() - 1:
            wb.Worksheets(tr + 2).Activate()
        else:
            print(34534654356)
            # printRep()

def data_TN(func):
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
        temp = model.index(i,9).data()
        hum = model.index(i,10).data()
        pres = model.index(i,11).data()
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

def fill_TNpoverka_full(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr  ):
    sheet = wb.ActiveSheet
    try:
        b8 = sheet.Cells(9, 2).Value = nomer
        b5 = sheet.Cells(5, 2).Value = doc
        g15 = sheet.Cells(15, 7).Value = tu
        a7 = sheet.Cells(7, 1).Value =  "ПРОТОКОЛ ПОВЕРКИ  № " + str(year) +"/" +  num_protokol + " ППТ"
        e8 = sheet.Cells(9, 5).Value = year
        d7 = sheet.Cells(8, 3).Value = shname
        d12 = sheet.Cells(15, 4).Value = int(temp)
        d13 = sheet.Cells(16, 4).Value = int(hum)
        d14 = sheet.Cells(17, 4).Value = int(pres)
        # i25 = sheet.Cells(25, 9).Value = oper
        c31 = sheet.Cells(29, 3).Value = data
        sheet.Cells(28, 3).Value = supervisor
        E18 = sheet.Cells(18, 5).Value = method
        b6 = sheet.Cells(6, 2).Value = lisnum


    except Exception as ex:
        print(ex)
        pass


    #находим эталонные средства измерений
    sql1 = f"""select zav_msr.num_gosreestr, zav_msr.comment from zav_msr
    where zav_msr.id in (select zav_msr from map_msr where test_map = {test_map}) and zav_msr.comment  <> ''"""
    etalon = []
    query = QSqlQuery(sql1)
    while query.next():
        etalon.append(f"{query.value(1)} №{query.value(0)}")
    etalon = ';'.join(map(str,etalon))
    e13 = sheet.Cells(12, 3).Value = etalon

    result = resultDictTT(item,shname,nomer)
    if result:
        coilID, voltage  = parser_name_tt(item)
        positionY = 26
        # находим класс точности наших обмоток
        cls = []
        for i in coilID:
            print('ttt',i,coilID[i])
            if coilID[i][0] != 'A-X':
                cls.append(coilID[i][1])
        cls = '/'.join(map(str,cls))
        sheet.Cells(10,2).Value = cls

        # находим U1ном / U2ном,В
        U = []
        # сначала  первичное напряжение
        primary = voltage['primary']
        print(1212,voltage)
        if primary in sqrtPOV:
            primary = sqrtPOV[primary]
        U.append(primary)
        # теперь вторичное напряжение
        for u in voltage['second']:
            if u in sqrtPOV:
                u = sqrtPOV[u]
            U.append(u)
        U = ':'.join(map(str,U))
        sheet.Cells(10, 7).Value = U

        positionY += 1
        if len(coilID) > 3:
            sheet.Range("F26:I26").value = ['f(%)', "∆(')", 'f(%)', "∆(')"]
            for coil in result.keys():
                if coil in ('R','X'):
                    continue
                count = len(result[coil]['P']['load']) * 2 -1
                corT = f"A{positionY}:I{positionY + count}"
                corO = f"A{positionY}:E{positionY + count}"
                corData = f"B{positionY}:G{positionY}"
                sheet.Range(corT).EntireRow.Insert()
                sheet.Range(corT).Borders.LineStyle = True

                # объединение столбцов класс точности cos S Uном
                sheet.Range(f"A{positionY}:A{positionY + count}").Merge()
                sheet.Range(f"B{positionY}:B{positionY + count}").Merge()
                sheet.Range(f"C{positionY}:C{positionY + count}").Merge()
                # sheet.Range(f"D{positionY}:D{positionY + count}").Merge()
                # sheet.Range(f"E{positionY}:E{positionY + count}").Merge()
                print(332,coilID)
                sheet.Cells(positionY,1).value = coilID[coil][0]
                sheet.Cells(positionY, 2).value = coilID[coil][1]
                sheet.Cells(positionY, 3).value = 0.8
                print(1,result)
                for i in result[coil]['P']['load']:
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    full = result[coil]['P']['load'][i]['full']
                    half = result[coil]['P']['load'][i]['half']
                    dataFull = [i, half[3], half[1], full[3], full[1]]
                    print(dataFull)
                    sheet.Range(f"E{positionY}:I{positionY}").Value = dataFull
                    positionY += 1
                sheet.Range(f"D{positionY - len(result[coil]['P']['load'])}:D{positionY - 1}").Merge()
                sheet.Cells(positionY - len(result[coil]['P']['load']), 4).Value = half[0]
                # Заполняем 1/4 нагрузку
                for i in result[coil]['P']['nload']:
                    full = result[coil]['P']['nload'][i]['full']
                    half = result[coil]['P']['nload'][i]['half']
                    dataFull = [i, half[3], half[1], full[3], full[1]]
                    print(dataFull)
                    sheet.Range(f"E{positionY}:I{positionY}").Value = dataFull
                    positionY += 1
                sheet.Range(f"D{positionY - len(result[coil]['P']['load'])}:D{positionY - 1}").Merge()
                sheet.Cells(positionY - len(result[coil]['P']['load']), 4).Value = half[0]
        else:
            sheet.Range("F26:I26").value = ['f(%)', None, "∆(')", None]
            for coil in result.keys():
                print(333,coil)
                print(1234,result)
                if coil in ('R','X'):
                    continue
                sheet.Range("F26:G26").Merge()
                sheet.Range("H26:I26").Merge()
                count = len(result[coil]['P']['load']) * 2 - 1
                corT = f"A{positionY}:I{positionY + count}"
                corD1 = f"A{positionY}:E{positionY + count}"
                corD2 = f"B{positionY}:G{positionY}"
                sheet.Range(corT).EntireRow.Insert()
                sheet.Range(corT).Borders.LineStyle = True
                # объединение столбцов класс точности cos S Uном
                sheet.Range(f"A{positionY}:A{positionY + count}").Merge()
                sheet.Range(f"B{positionY}:B{positionY + count}").Merge()
                sheet.Range(f"C{positionY}:C{positionY + count}").Merge()
                # объединяем столбцы значений F И ДЕЛЬТА
                sheet.Cells(positionY, 1).value = coilID[coil][0]
                sheet.Cells(positionY, 2).value = coilID[coil][1]
                sheet.Cells(positionY, 3).value = 0.8
                for i in result[coil]['P']['load']:
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    half = result[coil]['P']['load'][i]['half']
                    # dataFull = [half[0], i, half[3], None, half[1],None]
                    dataFull = [i, half[3], None, half[1], None]
                    sheet.Range(f"E{positionY}:I{positionY}").Value = dataFull
                    sheet.Range(f"F{positionY}:G{positionY}").Merge()
                    sheet.Range(f"H{positionY}:I{positionY}").Merge()
                    positionY += 1

                    # объединяем нагрузки
                sheet.Range(f"D{positionY- len(result[coil]['P']['load']) }:D{positionY-1}").Merge()
                sheet.Cells(positionY - len(result[coil]['P']['load']),4).Value = half[0]
                # Заполняем 1/4 нагрузку
                for i in result[coil]['P']['nload']:
                    half = result[coil]['P']['nload'][i]['half']
                    dataFull = [i, half[3], None, half[1],None]
                    sheet.Range(f"E{positionY}:I{positionY}").Value = dataFull
                    sheet.Range(f"F{positionY}:G{positionY}").Merge()
                    sheet.Range(f"H{positionY}:I{positionY}").Merge()
                    positionY += 1
                sheet.Range(f"D{positionY - len(result[coil]['P']['load'])}:D{positionY - 1}").Merge()
                sheet.Cells(positionY - len(result[coil]['P']['load']), 4).Value = half[0]

def fill_TNpoverka_blank(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr  ):
    print(2323232323)
    sheet = wb.ActiveSheet
    try:
        sheet.Cells(9, 2).Value = nomer
        sheet.Cells(5, 2).Value = doc
        sheet.Cells(15, 7).Value = tu
        sheet.Cells(7, 1).Value =  "ПРОТОКОЛ ПОВЕРКИ  № " + str(year) +"/" +  num_protokol + " ППТ"
        sheet.Cells(9, 5).Value = year
        sheet.Cells(8, 3).Value = shname
        # sheet.Cells(15, 4).Value = int(temp)
        # sheet.Cells(16, 4).Value = int(hum)
        # sheet.Cells(17, 4).Value = int(pres)
        # i25 = sheet.Cells(25, 9).Value = oper
        c31 = sheet.Cells(29, 3).Value = data
        # c28 = sheet.Cells(28, 7).Value = supervisor
        E18 = sheet.Cells(18, 5).Value = method
        b6 = sheet.Cells(6, 2).Value = lisnum


    except Exception as ex:
        print(ex)
        pass


    #находим эталонные средства измерений
    # sql1 = f"""select zav_msr.num_gosreestr, zav_msr.comment from zav_msr
    # where zav_msr.id in (select zav_msr from map_msr where test_map = {test_map}) and zav_msr.comment  <> ''"""
    # etalon = []
    # query = QSqlQuery(sql1)
    # while query.next():
    #     etalon.append(f"{query.value(1)} №{query.value(0)}")
    # etalon = ';'.join(map(str,etalon))
    # e13 = sheet.Cells(12, 3).Value = etalon
    #
    # result = resultDictTT(item,shname,nomer)
    coilID, voltage = parser_name_tt(item)
    # находим класс точности наших обмоток
    cls = []
    for i in coilID:
        if coilID[i][0] != 'A-X':
            cls.append(coilID[i][1])
    cls = '/'.join(map(str,cls))
    sheet.Cells(10,2).Value = cls

    # находим U1ном / U2ном,В
    U = []
    # сначала  первичное напряжение
    primary = voltage['primary']
    if primary in sqrtPOV:
        primary = sqrtPOV[primary]
    U.append(primary)
    # теперь вторичное напряжение
    for u in voltage['second']:
        if u in sqrtPOV:
            u = sqrtPOV[u]
        U.append(u)
    U = ':'.join(map(str,U))
    sheet.Cells(10, 7).Value = U
    positionY = 27


    if len(coilID) > 3:
        sheet.Range("F26:I26").value = ['f(%)', "∆(')", 'f(%)', "∆(')"]
        count_point = get_count_point(coilID)
        for key in coilID:
            if coilID[key][0] != 'A-X':
                classcuracy = coilID[key][1]
                count_percent = count_point[classcuracy][0] * 2
                corT = f"A{positionY}:I{positionY  + count_percent-1}"
                sheet.Range(corT).EntireRow.Insert()
                sheet.Range(f"A{positionY}:A{positionY  + count_percent-1}").Merge()
                sheet.Range(f"B{positionY}:B{positionY  + count_percent-1}").Merge()
                sheet.Range(f"C{positionY}:C{positionY  + count_percent-1}").Merge()
                sheet.Range(f"A{positionY}:c{positionY}").Value = [coilID[key][0],coilID[key][1],0.8]
                sheet.Range(f"D{positionY}:D{positionY  + int(count_percent/2)-1}").Merge()
                sheet.Range(f"D{positionY}").Value = coilID[key][2]
                sheet.Range(f"E{positionY}:E{positionY  + count_percent-1}").Value = count_point[classcuracy][1]
                sheet.Range(f"D{positionY  +int(count_percent/2)}:D{positionY + count_percent-1}").Merge()
                sheet.Range(f"D{positionY  +int(count_percent/2)}").Value = coilID[key][2]/4
                positionY = positionY  + count_percent
    else:
        sheet.Range("F26:I26").value = ['f(%)', None, "∆(')", None]
        count_point = get_count_point(coilID)
        for key in coilID:
            if coilID[key][0] != 'A-X':
                classcuracy = coilID[key][1]
                count_percent = count_point[classcuracy][0] * 2
                corT = f"A{positionY}:I{positionY  + count_percent-1}"
                sheet.Range(corT).EntireRow.Insert()
                sheet.Range(f"A{positionY}:A{positionY  + count_percent-1}").Merge()
                sheet.Range(f"B{positionY}:B{positionY  + count_percent-1}").Merge()
                sheet.Range(f"C{positionY}:C{positionY  + count_percent-1}").Merge()
                sheet.Range(f"A{positionY}:c{positionY}").Value = [coilID[key][0],coilID[key][1],0.8]
                sheet.Range(f"D{positionY}:D{positionY  + int(count_percent/2)-1}").Merge()
                sheet.Range(f"D{positionY}").Value = coilID[key][2]
                sheet.Range(f"E{positionY}:E{positionY  + count_percent-1}").Value = count_point[classcuracy][1]
                sheet.Range(f"D{positionY  +int(count_percent/2)}:D{positionY + count_percent-1}").Merge()
                sheet.Range(f"D{positionY  +int(count_percent/2)}").Value = coilID[key][2]/4
                for i in range(positionY-1,positionY  + count_percent ):
                    sheet.Range(f"F{i}:G{i}").Merge()
                    sheet.Range(f"H{i}:I{i}").Merge()
                positionY = positionY  + count_percent

def fill_TNprotocol_full(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr):
    result = resultDictTT(item, shname,nomer)
    print('Печаетаем',year,nomer,shname)
    if result:
        sheet = wb.ActiveSheet
        position = 25
        try:
            sheet.Cells(9, 2).Value = nomer
            sheet.Cells(4, 2).Value = doc
            sheet.Cells(13, 5).Value = tu
            sheet.Cells(6, 1).Value =   "ПРОТОКОЛ №" + year + "/" +  num_protokol + 'ПСИ'
            sheet.Cells(9, 5).Value = year
            sheet.Cells(8, 3).Value = shname
            sheet.Cells(12, 2).Value = int(temp)
            sheet.Cells(12, 5).Value = int(hum)
            sheet.Cells(12, 8).Value = int(pres)
            sheet.Cells(27, 2).Value = data

        except Exception as ex:
            print(ex)
            pass
        # записываем операторов испытаний (отк , высоковольтные и пси тн)
        controler = searchHV(item, 23)
        sheet.Cells(17, 7).Value = f"{controler[0]}\n {controler[1]}"
        sheet.Cells(23, 7).Value = f"{oper}\n {data}"
        hv = searchHV(sn)
        print("____________________",hv)
        if hv:
            print("______________2323232______", hv)
            sheet.Cells(18, 7).Value = f'{hv[0]}\n {hv[1]}'
        # Меняем заключение если обнаружен деффект
        print(44455,test,name_defect )
        if name_defect != "":
            sheet.Cells(26, 2).Value = str(name_defect).capitalize()
        # записываем холостой ход
        if type_tr in (10,11):
            try:
                sheet.Range("C23:D24").ClearContents()
                sheet.Range("C23:D24").Merge()
                sheet.Range("C23:D24").Value = '1 Uн'
                sheet.Range("F23:F24").Merge()
                sheet.Range("F23:F24").Value = [result['X'][1.0]]

            except:
                print(2242424)
        else:
            try:
                print([result['X'][1.2], result['X'][1.9]])
                sheet.Range("F23:F24").Value = [[result['X'][1.2]], [result['X'][1.9]]]
                print(353564364646)
            except:
                QMessageBox.warning(None, f"Предупреждение",
                                    f"Отсутствуют данные холостого хода трансформатора  {shname}", QMessageBox.Ok)

        # записыв
        sql = f"""select isolation_level ,prime_test_voltage, second_test_voltage, prime_test_voltage2   from testing_voltage
            where (nominal_voltage, testing_voltage.isolation_level) in
            (select voltage , isolationlevel from transformer
            where id = {idTr})
                   """
        print(sql)

        oQuerry = QSqlQuery(sql)
        if oQuerry.first():
            if oQuerry.value(0) == 'б':
                print("удаляем")
                sheet.Rows(20).EntireRow.Delete()
                position = 24
            else:
                sheet.Cells(18, 3).Value = f"Uисп = {int(oQuerry.value(3))} кВ"

            sheet.Cells(18, 3).Value = f"Uисп = {int(oQuerry.value(1))} кВ \n t = 1 мин"
            sheet.Cells(19, 3).Value = f"Uисп = {int(oQuerry.value(2))} кВ \n t = 1 мин"

        #записываем сопротивление
        count = len(result['R']) - 1 # количество добавленных строк для результатов сопротивления
        print(count)
        corT = f"C{position}:C{position+count-1}"
        print(corT)
        sheet.Range(corT).EntireRow.Insert()
        sheet.Range(f"A25:B{position+count}").Merge()
        for i in range(position, position+count+1): # объединение строк
            sheet.Range(f"C{i}:D{i}").Merge()
            sheet.Range(f"E{i}:F{i}").Merge()
        for key, value in result['R'].items():
            print(333,key,value,result['R'],result)
            sheet.Range(f"C{position}:F{position}").Value = [key,None, value]
            position +=1

def fill_TNprotocol_blank(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect, test_map,supervisor,method,lisnum, type_tr):
    # result = resultDictTT(item, shname,nomer)
    print('Печаетаем',year,nomer,shname)
    sheet = wb.ActiveSheet
    position = 25
    try:
        sheet.Cells(9, 2).Value = nomer
        sheet.Cells(4, 2).Value = doc
        sheet.Cells(13, 5).Value = tu
        sheet.Cells(6, 1).Value =   "ПРОТОКОЛ №" + year + "/" +  num_protokol + 'ПСИ'
        sheet.Cells(9, 5).Value = year
        sheet.Cells(8, 3).Value = shname
        # sheet.Cells(12, 2).Value = int(temp)
        # sheet.Cells(12, 5).Value = int(hum)
        # sheet.Cells(12, 8).Value = int(pres)
        # sheet.Cells(27, 2).Value = data

    except Exception as ex:
        print(ex)
        pass

    # записываем холостой ход
    if type_tr in (10,11):
        sheet.Range("C23:D24").ClearContents()
        sheet.Range("C23:D24").Merge()
        sheet.Range("C23:D24").Value = '1 Uн'
        sheet.Range("F23:F24").Merge()

        # записыв
        sql = f"""select isolation_level ,prime_test_voltage, second_test_voltage, prime_test_voltage2   from testing_voltage
            where (nominal_voltage, testing_voltage.isolation_level) in
            (select voltage , isolationlevel from transformer
            where id = {idTr})
                   """
        print(sql)

        oQuerry = QSqlQuery(sql)
        if oQuerry.first():
            if oQuerry.value(0) == 'б':
                print("удаляем")
                sheet.Rows(20).EntireRow.Delete()
                position = 24
            else:
                sheet.Cells(18, 3).Value = f"Uисп = {int(oQuerry.value(3))} кВ"

            sheet.Cells(18, 3).Value = f"Uисп = {int(oQuerry.value(1))} кВ \n t = 1 мин"
            sheet.Cells(19, 3).Value = f"Uисп = {int(oQuerry.value(2))} кВ \n t = 1 мин"
    coil = parser_name_tt(item)[0]
    print(222,coil)

    #записываем сопротивление
    count = len(coil) - 1 # количество добавленных строк для результатов сопротивления
    print(count)
    corT = f"C{position}:C{position+count-1}"
    print(corT)
    sheet.Range(corT).EntireRow.Insert()
    sheet.Range(f"A25:B{position+count}").Merge()
    for i in range(position, position+count+1): # объединение строк
        sheet.Range(f"C{i}:D{i}").Merge()
        sheet.Range(f"E{i}:F{i}").Merge()
    for key in coil:
        sheet.Range(f"C{position}:F{position}").Value = [coil[key][0],None, None]
        position +=1



def fill_ticket_tn(info):
    print(info)
    sheet = wb.ActiveSheet
    if info['type_transformer'] in (10, 11):
        sheet.Cells(4,2).Value = 'НЕЗАЗЕМЛЯЕМЫЙ'


    sheet.Cells(5, 2).Value = f"{info['type']}-{int(info['voltage'])} {info['climat']}         №{info['makedate']}-{info['serialnumber']} "
    sheet.Cells(12, 2).Value = f"{info['tu']}     {int(info['weight'])} кг  20{info['makedate']}г"
    sheet.Cells(10, 9).Value = info['maxPover']
    sheet.Cells(10, 12).Value = get_performance(info['fullname'])
    coil = parser_name_tt(info['idItem'])[0]
    # формируем таблицу______________________________________________________
    sc = 5  # начальная координата
    sclst = {}  # словарь хранит координаты для внесения результатов обмотки
    countW = len(coil)
    # countW = 8

    print(11, countW)
    # countW = 6

    first, last = col_column(countW,10)
    print(1112,first,last)


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
        sheet.Range(f"{x}6:{y}6").Merge()
        sheet.Range(f"{x}7:{y}7").Merge()
        sheet.Range(f"{x}8:{y}8").Merge()
        sheet.Range(f"{x}9:{y}9").Merge()
        sc += 1
    longP = 235  # ширина столбцов обмоток в пикселях
    s = 0
    for i in range(1, len(sclst) + 1):
        koef = longP / countW / sclst[i][2]
        s+= sheet.Range(sclst[i][1]).ColumnWidth * sclst[i][2]
        sheet.Range(sclst[i][1]).ColumnWidth = pickel_dict[int(koef)]

    position = 1
    # записываем сопротивление
    print(sclst)

    for i in coil:
        if coil[i][0] == 'A-X':
            sheet.Range(f"{sclst[1][0]}6:{sclst[1][0]}7").Value = [[coil[i][0]],[coil[i][1]] ]
            position += 1
        else:
            # запоминаем координату для записи результатов холостого хода для обмоток(a-x,a1-x1)
            if coil[i][0] in ('a-x', 'a1-x1'):
                corxx = sclst[position][0]
            sheet.Range(f"{sclst[position][0]}6:{sclst[position][0]}9").Value = [[coil[i][0]],[coil[i][3]],[coil[i][1]],[coil[i][2]]]
            position += 1



    print(sclst)
    print(coil)

def select_repTN(sn):

    # sql = f"""select t1.id, serial_number.id,
	# 	serial_number.ordernumber,
	# 	serial_number.series,
	# 	serial_number.serialnumber,
	# 	serial_number.makedate,
	# 	serial_number.transformer,
	# 	transformer.fullname
    #         from serial_number INNER JOIN
    #         (select id, serial_number AS sn from item
    #         where id = {item})t1
    #         ON serial_number.id =t1.sn
    #         INNER JOIN transformer ON serial_number.transformer = transformer.id"""
    sql = f"""select  serial_number.id,
		serial_number.ordernumber,
		serial_number.series,
		serial_number.serialnumber,
		serial_number.makedate,
		serial_number.transformer,
		transformer.fullname
            from serial_number INNER JOIN  
            transformer ON serial_number.transformer = transformer.id
            where serial_number.id = {sn} """

    print(sql)

    query = QSqlQuery(sql)
    print(query.size())
    if query.size() == 1:
        model.setQuery(sql)
        idsn = model.index(0, 0).data()
        on =  model.index(0, 1).data()
        ser =  model.index(0, 2).data()
        sn = model.index(0, 3).data()
        year = model.index(0, 4).data()
        tr =  model.index(0, 5).data()
        name = model.index(0, 6).data()
        full_repTN(on,ser,sn,year,tr,name, idsn)

    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено информации по данному трансформатору", QMessageBox.Ok)
def full_repTN(on,ser,sn,year,tr,name, idsn):

    print('ЗАПОЛНЯЕМ ОБЩИЙ ПРОТОКОЛ')
    wb.Worksheets(1).Activate()
    sheet = wb.ActiveSheet
    # расписываем верхушку
    print(name)
    sheet.Cells(1, 2).Value = name
    sheet.Cells(2, 3).Value = f"{year}-{sn}"
    sheet.Cells(3, 3).Value = f"20{year}"
    sheet.Cells(2, 6).Value = ser
    sheet.Cells(3, 6).Value = on
    items = []
    positionY = 9

    # ЗАПОЛНЯЕМ РЕЗУЛЬТАТЫ ИСПЫТАНИЯ ПЕРВИЧНОЙ ОБМОТКИ
    # ищем по серийному номеру результы испытания КТ в цеху
    sqlR = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
    	                    INNER join test_map on item.test_map = test_map.id
    	                    inner join stand  on test_map.stand = stand.id
    	                    inner join operator on test_map.operator = operator.id
                            where serial_number = {idsn} and stand.test_type = 20
                            order by date  desc
                            limit 1
                           """
    cor = 2
    print(sqlR)
    queryR = QSqlQuery(sqlR)
    print(queryR.size())
    if queryR.size() == 1:
        model_2.setQuery(sqlR)
        item2 = model_2.index(0, 0).data()
        items.append(item2)
        sheet.Cells(7, 6).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        sheet.Cells(7, 3).Value = model_2.index(0, 4).data()
        result = resultDictTT(item2, name, sn)
        if result:
            coilID = parser_name_tt(item2)[0]
            if result.get('R'):
                if result['R'].get('A-X'):
                    sheet.Cells(6, 2).Value = result['R']['A-X']
    # ЗАПОЛНЯЕМ РЕЗУЛЬТАТЫ ИСПЫТАНИЯ ПОГРЕШНОСТЕЙ
    sqlP = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
                                INNER join test_map on item.test_map = test_map.id
                                inner join stand  on test_map.stand = stand.id
                                inner join operator on test_map.operator = operator.id
                                where serial_number = {idsn} and stand.test_type = 21
                                order by date  desc
                                limit 1
                               """
    print(sqlP)
    queryR = QSqlQuery(sqlP)
    print(queryR.size())
    print(111,positionY)
    if queryR.size() == 1:
        model_2.setQuery(sqlP)
        item3 = model_2.index(0, 0).data()
        items.append(item3)
        sheet.Cells(positionY+1, 6).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        sheet.Cells(positionY+1, 3).Value = model_2.index(0, 4).data()
        result = resultDictTT(item3, name, sn)
        print(7777,result,item3)
        if result:
            print(666666666666666666666666666666666666)
            coilID = parser_name_tt(item3)[0]
            type_load = define_load(coilID)
            print(77777777777777777777777777777777777777777)
            if type_load:
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Borders.LineStyle = True
                positionY += 1
                for coil in result.keys():
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:G{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:G{positionY}"
                    sheet.Range(corT).Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    print(3333, coilID)
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
            else:
                print('ЗАПОЛНЯЯЯЯЯЯЕМ')
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Borders.LineStyle = True

                print(positionY)
                positionY += 1
                print(2242,result,coilID)
                for coil in result.keys():
                    print(333,coil)
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:E{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:E{positionY}"
                    sheet.Range(corT).EntireRow.Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
        sheet.Range("A3:G16").EntireColumn.AutoFit()
        positionY +=2
        print(222,positionY)


    # ЗАПОЛНЯЕМ РЕЗУЛЬТАТЫ ИСПЫТАНИЯ ПОГРЕШНОСТЕЙ и сопротивлений
    sqlPR = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
                	                    INNER join test_map on item.test_map = test_map.id
                	                    inner join stand  on test_map.stand = stand.id
                	                    inner join operator on test_map.operator = operator.id
                                        where serial_number = {idsn} and stand.test_type = 22
                                        order by date  desc
                                        limit 1
                                       """
    print(sqlPR)
    queryR = QSqlQuery(sqlPR)
    print(queryR.size())
    if queryR.size() == 1:
        model_2.setQuery(sqlPR)
        item4 = model_2.index(0, 0).data()
        items.append(item4)
        sheet.Cells(positionY + 1, 6).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        sheet.Cells(positionY + 1, 3).Value = model_2.index(0, 4).data()
        result = resultDictTT(item4, name, sn)
        print(7777, result, item4)
        if result:
            coilID = parser_name_tt(item4)[0]
            type_load = define_load(coilID)
            obm = ['Обм']
            val = ['Rом']
            count = len(result['R'])
            for key, value in result['R'].items():
                obm.append(key)
                val.append(value)
            x = sheet.Cells(positionY, 1)
            y = sheet.Cells(positionY, count + 1)
            sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, count + 1)).Value = obm
            positionY += 1
            sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, count + 1)).EntireRow.Insert()
            sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, count + 1)).Value = val
            sheet.Range(sheet.Cells(positionY-1, 1), sheet.Cells(positionY, count + 1)).Borders.LineStyle = True
            sheet.Range(sheet.Cells(3, 1), sheet.Cells(positionY, count + 1)).Font.Size = 16
            positionY += 1
            sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, count + 1)).EntireRow.Insert()
            if type_load:
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Borders.LineStyle = True
                positionY += 1
                for coil in result.keys():
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:G{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:G{positionY}"
                    sheet.Range(corT).EntireRow.Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    print(3333, coilID)
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
            else:
                print('ЗАПОЛНЯЯЯЯЯЯЕМ')
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Borders.LineStyle = True
                positionY += 1
                for coil in result.keys():
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:E{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:E{positionY}"
                    sheet.Range(corT).EntireRow.Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
            positionY +=3
    # ЗАПОЛНЯЕМ РЕЗУЛЬТАТЫ ВЫСОКОВОЛЬТНЫХ ИСПЫТАНИЙ
    hv = searchHV(idsn)
    print(hv)
    print(positionY)
    if hv:
        sheet.Cells(positionY, 3).Value = hv[0]
        sheet.Cells(positionY, 1).Value = hv[1]
    print("высокие не найдены")
    print(positionY)
    positionY += 2


    # ЗАПОЛНЯЕМ РЕЗУЛЬТАТЫ ПСИ
    sqlPSI = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio, transformer.type_transformer from item
                    	                    INNER join test_map on item.test_map = test_map.id
                    	                    inner join stand  on test_map.stand = stand.id
                    	                    inner join operator on test_map.operator = operator.id
                    	                    inner join serial_number on item.serial_number = serial_number.id
                                            inner join transformer on serial_number.transformer = transformer.id
                                            where serial_number = {idsn} and stand.test_type = 19
                                            order by date  desc
                                            limit 1
                                           """
    print(sqlPSI)
    queryR = QSqlQuery(sqlPSI)
    print(queryR.size())
    if queryR.size() == 1:
        model_2.setQuery(sqlPSI)
        item5 = model_2.index(0, 0).data()
        items.append(item5)
        idTr = model_2.index(0, 5).data()
        sheet.Cells(positionY + 4, 6).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        sheet.Cells(positionY + 4, 3).Value = model_2.index(0, 4).data()
        print(23232323,positionY)
        result = resultDictTT(item5, name, sn)
        coilID = parser_name_tt(item5)[0]
        type_load = define_load(coilID)
        print(7777, result, item5)
        if result:
            if idTr in (10,11):
                try:
                    sheet.Range(f"C{positionY}:D{positionY+1}").ClearContents()
                    sheet.Range(f"C{positionY}:D{positionY+1}").Merge()
                    sheet.Range(f"C{positionY}:D{positionY+1}").Value = '1 Uн'
                    sheet.Range(f"C{positionY}:D{positionY+1}").Merge()
                    sheet.Range(f"C{positionY}:D{positionY+1}").Value = [result['X'][1.0]]

                except:
                    print(2242424)
            else:
                try:
                    print([result['X'][1.2], result['X'][1.9]])
                    sheet.Range(f"G{positionY}:G{positionY+1}").Value = [[result['X'][1.2]], [result['X'][1.9]]]
                    print(353564364646)
                except:
                    QMessageBox.warning(None, f"Предупреждение",
                                        f"Отсутствуют данные холостого хода трансформатора  {name}", QMessageBox.Ok)
            positionY +=2
            print(positionY)

            # записываем сопротивление
            count = len(result['R']) - 1  # количество добавленных строк для результатов сопротивления
            print(count)
            corT = f"C{positionY}:C{positionY + count - 1}"
            print(corT)
            sheet.Range(corT).EntireRow.Insert()
            sheet.Range(f"A{positionY}:D{positionY + count}").Merge()
            for i in range(positionY, positionY + count + 1):  # объединение строк
                sheet.Range(f"E{i}:F{i}").Merge()
            for key, value in result['R'].items():
                print(333, key, value, result['R'], result)
                sheet.Range(f"E{positionY}:G{positionY}").Value = [key,None,value]
                sheet.Range(f"E{positionY}:G{positionY}").Font.Bold = True
                sheet.Range(f"E{positionY}:G{positionY}").Font.Size = 16
                positionY += 1
            if type_load:
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 7)).Borders.LineStyle = True
                positionY += 1
                for coil in result.keys():
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:G{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:G{positionY}"
                    sheet.Range(corT).EntireRow.Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    print(3333, coilID)
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1], full[3], full[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:G{positionY}").Value = dataFull
                        positionY += 1
            else:
                print('ЗАПОЛНЯЯЯЯЯЯЕМ')
                collums = ['обм', 'BA', 'Un%', 'f(%)', 'Δ']
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Value = collums
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Font.Size = 16
                sheet.Range(sheet.Cells(positionY, 1), sheet.Cells(positionY, 5)).Borders.LineStyle = True
                positionY += 1
                for coil in result.keys():
                    if coil in ('R', 'X'):
                        continue
                    count = len(result[coil]['P']['load']) * 2 - 1
                    corT = f"A{positionY}:E{positionY + count}"
                    corO = f"A{positionY}:A{positionY + count}"
                    corData = f"B{positionY}:E{positionY}"
                    sheet.Range(corT).EntireRow.Insert()
                    sheet.Range(corT).Borders.LineStyle = True
                    sheet.Range(corO).Merge()
                    sheet.Cells(positionY, 1).value = coilID[coil][0]
                    # сначала записываем все данные обмотки с 100 % нагрузкой
                    for i in result[coil]['P']['load']:
                        full = result[coil]['P']['load'][i]['full']
                        half = result[coil]['P']['load'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
                    # Заполняем 1/4 нагрузку
                    for i in result[coil]['P']['nload']:
                        full = result[coil]['P']['nload'][i]['full']
                        half = result[coil]['P']['nload'][i]['half']
                        dataFull = [half[0], i, half[3], half[1]]
                        print(dataFull)
                        sheet.Range(f"B{positionY}:E{positionY}").Value = dataFull
                        positionY += 1
    print(444444,positionY)
    sheet.Range("A1:I80").EntireColumn.AutoFit()
    sheet.Range("A1:I80").EntireRow.AutoFit()
def define_load(info):
    for i in info:
        if info[i][0] in ('a1-x1','a2-x2'):
            return True
    return False

def select_Stikert(idItem = None):
    sql = f"""select item.id , item.test_map, serial_number.serialnumber, serial_number.makedate, transformer.fullname, operator.fio, stand.fullname, test_map.createdatetime, transformer.id  from item 
	            inner join serial_number on item.serial_number = serial_number.id
	            inner join transformer on serial_number.transformer = transformer.id
                inner join test_map on item.test_map = test_map.id
                inner join operator on test_map.operator = operator.id
                inner join stand on test_map.stand = stand.id
                where item.id = {idItem}"""

    print(sql)
    query = QSqlQuery()
    query.prepare(sql)

    if not query.exec_() or query.size() == 0:
        # print(323232323232323232323232323)
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return False
    else:

        model.setQuery(query)
        return True

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

#
# from PyQt5.QtWidgets import QApplication
# import sys
# # # # #
# pp = QApplication(sys.argv)
# if open_excel('ticket_tn.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportTN(2073553,fill_ticket_tn)

# # if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 0):
# #     data_TN(fill_TNpoverka)
# #     printRep()
# # #
# select_result(2006211)
# if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 1):
#     data_TN(fill_TNpoverka_blank)
