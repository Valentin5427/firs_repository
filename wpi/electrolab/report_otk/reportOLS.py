import win32print
import datetime
from win32com.client import constants as const
import win32com.client
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import  QSqlQuery, QSqlQueryModel
from electrolab.gui.Config_base import   db


# Основные объекты VBA http://bourabai.ru/einf/vba/2-04.htm

model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
windings = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
windingsKT = ["A-a2", "A-a3", "A-a4", "A-a5", "A-a6", "A-a7", "A-a8"]





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


def float_or_int(number, digits = 1, digitsF = 2):
    try:
        number = float(number)
    except:
        return ''

    number = float(number)
    if number % 1 == 0:
        print(4442,number)
        return int(number)
    else:
        return toFixed(number,digitsF)



def open_excel(name_file, name_printer, visible = 1):
    import os
    global wb, Excel
    p = os.path.abspath(name_file)
    if not os.path.exists(p):
        QMessageBox.warning(None, u"Ошибка шаблона отчета", f"Не удается найти файл {name_file}", QMessageBox.Ok)
        return False
    Excel = win32com.client.Dispatch("Excel.Application")
    try:
        Excel.Visible = visible
    except:
        pass
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



def fill_psi_ols(func):
    sql_params = """select name from params
                    order by date_begin DESC
                    limit 1"""

    quer = QSqlQuery(sql_params)
    if quer.first():
        doc  = quer.value(0)
        print(111111,doc)

    if model.rowCount() < 1:
        print(4434, model.rowCount() )
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return

    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()
    print(44444444444444444444444444444444444444,model.rowCount())
    for i in range(model.rowCount()):
        nomer = f"{model.index(i, 6).data()}-{model.index(i, 5).data()}"
        item = model.index(i,13).data()
        shname = model.index(i,3).data()
        # year = '20' + str(model.index(i,6).data())
        year = model.index(i,8).data().toString('yyyy')
        data = model.index(i,8).data().toString('dd.MM.yyyy')
        temp = model.index(i,9).data()
        hum = model.index(i,10).data()
        pres = model.index(i,11).data()
        idTr = model.index(i,12).data()
        oper = model.index(i,14).data()
        num_protokol = "ПРОТОКОЛ приемо-сдаточных испытаний  № " + str(year) +"/" +  str(model.index(i,0).data())
        tu = model.index(i,7).data()
        sn = model.index(i, 5).data()
        test = model.index(i, 16).data()
        name_defect = model.index(i, 17).data()
        print(1111111111111111111,num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect)
        func(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect )
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass
            # printRep()


def resultDict(item, shname):
    sql = f"""select coil.tap, t.coil, t.resist, t.kt, t.pkz, t.ukz,  t.cur_xx, t.loss_xx, t.kt_istested from coil
            left join test_ols as t on coil.id = t.coil
            where transformer in(select serial_number.transformer from item
                                    inner join serial_number on item.serial_number = serial_number.id
                                        where item.id = {item}) and (item is null or item = {item})
            order by coil.tap"""
    print(sql)
    quer = QSqlQuery(db)
    quer.prepare(sql)
    if not quer.exec_():
        QMessageBox.warning(None, f"Предупреждение",
                            f"Ошибка выборки результатов испытания трансформатора {shname}", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(quer)
    # словарь в котором формируется сопоставление название обмотки и её результатов AX : resist, pkt, ukz, loss_xx, cur_xx
    # dictRes = {'resist':{},  'kt':{}, 'xx':{}, 'kz':{}}
    dictRes = {}
    dictId = {}
    for i in range(model_2.rowCount()):
        print(model_2.index(i, 0).data())
        if model_2.index(i, 0).data() == 0:
            dictRes[0] = [model_2.index(i, 2).data(), model_2.index(i, 4).data(), model_2.index(i, 5).data(),
                          model_2.index(i, 6).data(), model_2.index(i, 7).data()]
        if model_2.index(i, 0).data() == 2:
            dictRes[2] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 3:
            print(1111)
            dictRes[3] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 4:
            print(1111)
            dictRes[4] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 5:
            print(1111)
            dictRes[5] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 6:
            print(1111)
            dictRes[6] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 7:
            print(1111)
            dictRes[7] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
        if model_2.index(i, 0).data() == 8:
            print(1111)
            dictRes[8] = [model_2.index(i, 2).data(), model_2.index(i, 3).data(),model_2.index(i, 8).data()]
    print(66666)
    dictRes = dict(sorted(dictRes.items()))
    print(1111112,dictRes)
    return dictRes


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

# поиск оператора проводившего ПРИЕМКУ ОКК ПОСЛЕ ПСИ

def searchOKK(item):
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
                stand.test_type = 10
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

    return (None,None)



def fill_file(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer, tu,sn, idT, test, name_defect):
    try:
        print(111,   num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer, tu,sn, idT, test, name_defect )
        sheet = wb.ActiveSheet
        b8 = sheet.Cells(8,2).Value = nomer
        b5 = sheet.Cells(4,2).Value = doc
        g15 = sheet.Cells(15,7).Value = tu
        a6 = sheet.Cells(5,1).Value = num_protokol
        e8 = sheet.Cells(8,5).Value = year
        d7 = sheet.Cells(7,4).Value = shname
        d12 = sheet.Cells(12, 4).Value = int(temp)
        d13 = sheet.Cells(13, 4).Value = int(hum)
        d14 = sheet.Cells(14, 4).Value = int(pres)
        i25 = sheet.Cells(25,9).Value = f"{oper}\n {data}"
        c33 = sheet.Cells(33,3).Value = data
        controler = searchHV(item, 23)
        print(111345, controler)
        sheet.Cells(19, 9).Value = f"{controler[0]}\n {controler[1]}"
    #формирование словаря результатов по каждой обмотке
        dictRes = resultDict(item,shname)

        sql1 = f"""select * from permissible_ols
                    where load in (select secondload as sl from coil 
                                    where transformer = {idT} and tap = 2)"""

        print(11,dictRes)

        oQuerry = QSqlQuery(sql1)
        if oQuerry.first():
            G27 = sheet.Cells(27, 7).Value = oQuerry.value(1)
            G28 = sheet.Cells(28, 7).Value = oQuerry.value(2)
            G29 = sheet.Cells(29, 7).Value = oQuerry.value(3)
            G30 = sheet.Cells(30, 7).Value = oQuerry.value(4)

        # проверка номинальных значений, если не сходится закрашиваем фоном
        if test == False:
            c32 = sheet.Cells(32, 3).Value = str(name_defect).capitalize()

        if dictRes[0][3] != 0:
            H27 = sheet.Cells(27, 8).Value = dictRes[0][3]
            if float(sheet.Cells(27, 7).Value) < float(sheet.Cells(27, 8).Value):
                sheet.Cells(27, 8).Interior.Color = 99999
        if dictRes[0][4] != 0:
            H28 = sheet.Cells(28, 8).Value = dictRes[0][4]
            if float(sheet.Cells(28, 7).Value) < float(sheet.Cells(28, 8).Value):
                print(2)
                sheet.Cells(28, 8).Interior.Color = 99999
        if dictRes[0][2] != 0:
            H29 = sheet.Cells(29, 8).Value = dictRes[0][2]
            if float(sheet.Cells(29, 7).Value) < float(sheet.Cells(29, 8).Value):
                print(3)
                sheet.Cells(29, 8).Interior.Color = 99999
        if dictRes[0][1] !=0:
            H30 = sheet.Cells(30, 8).Value = dictRes[0][1]
            if float(sheet.Cells(30, 7).Value) < float(sheet.Cells(30, 8).Value):
                sheet.Cells(30, 8).Interior.Color = 99999
                print(4)

        sql = f""" select fullname, voltage, t1.prime_test_voltage, t1.second_test_voltage from transformer tr inner join 
                (select * from testing_voltage
                where isolation_level LIKE 'С')t1
                on tr.voltage = t1.nominal_voltage
            where tr.fullname LIKE '{shname}'
           """
        print(sql)

        oQuerry = QSqlQuery(sql)
        if oQuerry.first():
            print(oQuerry.value(2), oQuerry.value(3))
            e20 = sheet.Cells(20, 5).Value = f"Uисп = {int(oQuerry.value(2))} кВ \n t = 1 мин"
            e21 = sheet.Cells(21, 5).Value = f"Uисп = {int(oQuerry.value(3))} кВ \n t = 1 мин"

        else:
            print('Ошибка выборки номинального напряжения')

        # поиск оператора проводившего высоковольтные испытания транса
        hv = searchHV(item)
        if hv:
            i20 = sheet.Cells(20, 9).Value =  f"{hv[0]}\n {hv[1]}"

        #переменные, от которых будем расписывать данные по обмоткам
        poleR0 = 25

        #  формирование строк для записи сопротивления
        countW  = len(dictRes)
        countD = countW * 2 -4
        print(11,countD,countW)
        sheet.Range(f"E26:E{26+countD}").EntireRow.Insert()
        sheet.Range(f"A{25}:D{countW+24}").Merge()
        print(countW+25,countD+22 +countW )
        sheet.Range(f"A{countW+25}:D{countD+22 +countW}").Merge()
        print(windings)
        # Заполняем сопротивление
        for i in range(len(dictRes)):
            if i == 0:
                data = ['A-X',  None, dictRes[i][0]]
                sheet.Range(f"F{poleR0}:H{poleR0}").Value = data
                poleR0 +=1
                continue
            else:
                index = i +1
                data = [ f'a{i}', None,  dictRes[index][0] ]
                sheet.Range(f"F{poleR0}:H{poleR0}").Value = data
                poleR0 += 1
                print(data)
        print(dictRes)
        for i in range(2, len(dictRes)+1):
            try:
                if i not in dictRes:
                    poleR0 +=1
                    continue
                data = [f'A-a{i-1}', None, dictRes[i][1]]
                sheet.Range(f"F{poleR0}:H{poleR0}").Value = data
                # если не соответствие то закрашиваем
                if  dictRes[i][2] != True:
                    sheet.Cells(poleR0, 8).Interior.Color = 150000
                poleR0 += 1
            except KeyError:
                print('Ошибка выборки данных трансформатора ', shname)
                QMessageBox.warning(None, f"Предупреждение",
                                    f"Ошибка выборки результатов испытания трансформатора {shname}", QMessageBox.Ok)
                poleR0 += 1

    except:
        pass

def get_count_win(id):
    sql_len_win = F"""select id from coil where transformer = {id}"""
    print(sql_len_win)
    query = QSqlQuery()

    if query.exec(sql_len_win):
        return query.size()





def fill_file_blank(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer, tu,sn, idT, test, name_defect):
    print('печатаем пустой бланк олс')
    try:
        sheet = wb.ActiveSheet
        b8 = sheet.Cells(8,2).Value = nomer
        b5 = sheet.Cells(5,2).Value = doc
        g15 = sheet.Cells(15,7).Value = tu
        a6 = sheet.Cells(6,1).Value = num_protokol
        e8 = sheet.Cells(8,5).Value = year
        d7 = sheet.Cells(7,4).Value = shname
    #получаем количество обмоток
        countW = get_count_win(idT)
        if countW == 0:
            QMessageBox.warning(None, f"ошибка",
                                f"Не удалось получить сведения по обмоткам для  трансформатора {shname}", QMessageBox.Ok)
            return


        print(12121212,countW)

        sql1 = f"""select * from permissible_ols
                    where load in (select secondload as sl from coil 
                                    where transformer = {idT} and tap = 2)"""


        oQuerry = QSqlQuery(sql1)
        if oQuerry.first():
            G27 = sheet.Cells(27, 7).Value = oQuerry.value(1)
            G28 = sheet.Cells(28, 7).Value = oQuerry.value(2)
            G29 = sheet.Cells(29, 7).Value = oQuerry.value(3)
            G30 = sheet.Cells(30, 7).Value = oQuerry.value(4)


        sql = f""" select fullname, voltage, t1.prime_test_voltage, t1.second_test_voltage from transformer tr inner join 
                (select * from testing_voltage
                where isolation_level LIKE 'С')t1
                on tr.voltage = t1.nominal_voltage
            where tr.fullname LIKE '{shname}'
           """
        print(sql)

        oQuerry = QSqlQuery(sql)
        if oQuerry.first():
            print(oQuerry.value(2), oQuerry.value(3))
            e20 = sheet.Cells(20, 5).Value = f"Uисп = {int(oQuerry.value(2))} кВ \n t = 1 мин"
            e21 = sheet.Cells(21, 5).Value = f"Uисп = {int(oQuerry.value(3))} кВ \n t = 1 мин"

        else:
            print('Ошибка выборки номинального напряжения')

        #переменные, от которых будем расписывать данные по обмоткам
        poleR0 = 25

        #  формирование строк для записи сопротивления
        countD = countW * 2 -4
        print(11,countD,countW)
        sheet.Range(f"E26:E{26+countD}").EntireRow.Insert()
        sheet.Range(f"A{25}:D{countW+24}").Merge()
        print(countW+25,countD+22 +countW )
        sheet.Range(f"A{countW+25}:D{countD+22 +countW}").Merge()
        print(windings)
        # Заполняем сопротивление
        for i in range(countW):
            if i == 0:
                data = ['A-X']
                sheet.Range(f"F{poleR0}").Value = data
                poleR0 +=1
                continue
            else:
                index = i +1
                data = [ f'a{i}']
                sheet.Range(f"F{poleR0}").Value = data
                poleR0 += 1
                print(data)
        for i in range(2, countW+1):
            data = [f'A-a{i-1}']
            sheet.Range(f"F{poleR0}").Value = data
            poleR0 += 1

    except:
        pass





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

    except Exception as ex:
        print(321321, ex)
        QMessageBox.warning(None, f"Ошибка печати",
                            f"Проверьте работу принтера или Excel {ex}", QMessageBox.Ok)





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


def select_passport(item):

    sql = f"""select t1.id, serial_number.id,
		serial_number.ordernumber,
		serial_number.series,
		serial_number.serialnumber,
		serial_number.makedate,
		serial_number.transformer,
		transformer.fullname
            from serial_number INNER JOIN
            (select id, serial_number AS sn from item
            where id = {item})t1
            ON serial_number.id =t1.sn
            INNER JOIN transformer ON serial_number.transformer = transformer.id"""
    print(sql)

    query = QSqlQuery(sql)
    print(query.size())
    if query.size() == 1:
        model.setQuery(sql)
        item = model.index(0, 0).data()
        print(item)
        idsn = model.index(0, 1).data()
        on =  model.index(0, 2).data()
        ser =  model.index(0, 3).data()
        sn = model.index(0, 4).data()
        year = model.index(0, 5).data()
        tr =  model.index(0, 6).data()
        name = model.index(0, 7).data()
        # passportOLS(item,on,ser,sn,year,tr,name, idsn)

    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено информации по данному трансформатору", QMessageBox.Ok)


def fill_passportOLS_full(info):
    print('заполняем паспорт')
    print(info)
    sheet = wb.ActiveSheet
    controler, data = searchOKK(info['idItem'])
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38,1).Value = info['fullname']
    sheet.Cells(39, 1).Value = info['tu']
    sheet.Cells(40, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(60, 7).Value = info['weight']
    sheet.Cells(21, 21).Value = info['type']
    sheet.Cells(52, 22).Value = info['type']
    sheet.Cells(42, 17).Value = f"Трансформатор силовой, {info['type']} соответствует требованиям, \n {info['tu']} и признан годным для эксплуатации"
    sheet.Cells(40, 10).Value = data
    sheet.Cells(47, 24).Value = data
    sheet.Cells(45, 23).Value = controler
    sheet.Cells(57, 17).Value = f"Суммарная масса цветных металлов не более: медь (Cu) {info['copperP']} kg (кг), медные сплавы {info['copperPN']} kg (кг). Драгоценные металлы отсутствуют."
    sheet.Cells(50, 17).Value = info['method']
    sheet.Cells(30, 20).Value = check_EAN_valid(str(info['serialnumber']),f"20{info['makedate']}")
    sheet.Cells(10, 17).Value = 'Декларация о соответствии ' + info['declaration']
    add_picture_keaz(info['idsn'], sheet)

    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {} # словарь хранит координаты для внесения результатов обмотки
    countW = get_count_win(info['idTransformer'])
    result = resultDict(info['idItem'], info['fullname'])
    coil = get_nominal_current(info['idTransformer'])
    print(result)
    print(coil)
    print(11,countW)
    # countW = 6
    #
    first, last = col_column(countW,8)
    for i in range(1,countW+1):
        # print(112,i)
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
        # print(11112,x,y)
        sheet.Range(f"{x}43:{y}43").Merge()
        sheet.Range(f"{x}46:{y}46").Merge()
        sheet.Range(f"{x}47:{y}47").Merge()
        sheet.Range(f"{x}48:{y}48").Merge()
        sheet.Range(f"{x}49:{y}50").Merge()
        sheet.Range(f"{x}51:{y}51").Merge()
        sheet.Range(f"{x}52:{y}52").Merge()
        sheet.Range(f"{x}53:{y}54").Merge()
        sheet.Range(f"{x}55:{y}56").Merge()
        sc +=1
    for i in range(1,len(sclst)+1):
        koef = 32 / countW / sclst[i][2]
        sheet.Range(sclst[i][1]).ColumnWidth = koef
    # # закончили формировать_________________________________
    position = 1
    # записываем данные в таблицу
    # print(sclst)
    print(3456, coil)
    for i in coil['win']:
        if i == 0:
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value =   [[f"A-X"],[None], [None], [None], [coil['win'][i][0]], [coil['win'][i][1]], [result[0][0]],['-'],['-'],['-'],[result[0][2]],['-'],[result[0][1]]]
        elif i == 4:
             sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value = [[f"x-{windings[i-2]}"],
                                                                                    [None],
                                                                                    [None],
                                                                                    [None],
                                                                                    [coil['win'][i][0]],
                                                                                    [coil['win'][i][1]],
                                                                                    [result[i][0]],
                                                                                    [result[i][0]],
                                                                                    [result[0][3]],
                                                                                    [result[0][4]],
                                                                                    [result[0][2]],
                                                                                    [None],
                                                                                    [result[0][1]]]

        else:
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value = [[f"x-{windings[i-2]}"], [None], [None], [None],[coil['win'][i][0]],[coil['win'][i][1]], [result[i][0]],['-'], ['-'], ['-'], ['-'], ['-'],['-']]
        position += 1
    sheet.Cells(44, 7).Value = info['voltage']
    sheet.Cells(45, 7).Value = info['maxvoltage']
    sheet.Cells(46, 7).Value = float_or_int(coil['sec_pow'])

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
        sheet.Cells(37, 23).Value = query.value(1)
    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}",
                            QMessageBox.Ok)



def add_picture_keaz(sn,sheet):
    sql = f"""select info from serial_number where id = {sn}"""
    print(sql)
    query = QSqlQuery(sql)
    if query.first():
        text = query.value(0)
        if text.count('Печать для КЭАЗ'):
            import os
            basedir = os.path.abspath(os.getcwd())
            path = '\\'.join(basedir.split('\\')[:2]) + '\\report_otk\\' + 'keaz.png'
            print(2214, path)
            sheet.Shapes.AddPicture(path,True, True, 180, 5, 100, 30)

def add_acceptance(info, typeTr,sheet):
    sql = f"""select info from serial_number where id = {info['idsn']}"""
    print(sql)
    query = QSqlQuery(sql)
    if query.first():
        text = query.value(0)
        print(567,text)
        if text.count('Морской Регистр'):
            sheet.Cells(44,
                        17).Value = f"""Трансформатор тока {info['type']}  соответствует требованиям {typeTr['tu']}, требованиям п.2.1.1 и п.2.1.2 раздела 2 Правил классификации и постройки морских судов (часть XI) и признан годным для эксплуатации"""
        else:
            sheet.Cells(44,
                        17).Value = f"Трансформатор тока {info['type']}  соответствует требованиям {typeTr['tu']} и признан годным для эксплуатации"


# Получаем результаты трансформаторов
def select_resultOLS(items,func):
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
            t1.data1
                from serial_number INNER JOIN
                (select item.id, serial_number  AS sn, item.acceptdatetime AS data, item.createdatetime AS data1 , operator.fio as fio  from item
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
        info['data1'] = model.index(i, 23).data().toString('yyyy')[2:]



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


def fill_passportOLS_blank(info):
    print('заполняем паспорт')
    print(info)
    sheet = wb.ActiveSheet
    sheet.Cells(1, 2).Value = f"Заводской №{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(2, 2).Value = f"Заказ №{info['ordernumber']}"
    sheet.Cells(38, 1).Value = info['fullname']
    sheet.Cells(39, 1).Value = info['tu']
    sheet.Cells(40, 4).Value = f"{info['makedate']}-{info['serialnumber']}"
    sheet.Cells(60, 7).Value = info['weight']
    sheet.Cells(21, 21).Value = info['type']
    sheet.Cells(52, 22).Value = info['type']
    sheet.Cells(42,
                17).Value = f"Трансформатор силовой, {info['type']} соответствует требованиям, \n {info['tu']} и признан годным для эксплуатации"
    sheet.Cells(57,
                17).Value = f"Суммарная масса цветных металлов не более: медь (Cu) {info['copperP']} kg (кг), медные сплавы {info['copperPN']} kg (кг). Драгоценные металлы отсутствуют."
    sheet.Cells(50, 17).Value = info['method']
    sheet.Cells(30, 20).Value = check_EAN_valid(str(info['serialnumber']),f"20{info['makedate']}")
    sheet.Cells(10, 17).Value = 'Декларация о соответствии ' + info['declaration']

    # формируем таблицу______________________________________________________
    sc = 7  # начальная координата
    sclst = {}  # словарь хранит координаты для внесения результатов обмотки
    countW = get_count_win(info['idTransformer'])
    result = resultDict(info['idItem'], info['fullname'])
    coil = get_nominal_current(info['idTransformer'])
    print(result)
    print(coil)
    print(11, countW)
    # countW = 6
    #
    first, last = col_column(countW, 8)
    for i in range(1, countW + 1):
        # print(112,i)
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
        # print(11112,x,y)
        sheet.Range(f"{x}43:{y}43").Merge()
        sheet.Range(f"{x}46:{y}46").Merge()
        sheet.Range(f"{x}47:{y}47").Merge()
        sheet.Range(f"{x}48:{y}48").Merge()
        sheet.Range(f"{x}49:{y}50").Merge()
        sheet.Range(f"{x}51:{y}51").Merge()
        sheet.Range(f"{x}52:{y}52").Merge()
        sheet.Range(f"{x}53:{y}54").Merge()
        sheet.Range(f"{x}55:{y}56").Merge()
        sc += 1
    for i in range(1, len(sclst) + 1):
        koef = 32 / countW / sclst[i][2]
        sheet.Range(sclst[i][1]).ColumnWidth = koef
    # # закончили формировать_________________________________
    position = 1
    # записываем данные в таблицу
    # print(sclst)
    for i in coil['win']:
        if i == 0:
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value = [[f"A-X"], [None], [None], [None],
                                                                                   [coil['win'][i][0]],
                                                                                   [coil['win'][i][1]], [None],
                                                                                   ['-'], ['-'], ['-'], ['-'], ['-'],
                                                                                   ['-']]

        elif i == 3:
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value = [[f"x-{windings[i - 2]}"],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None],
                                                                                   [coil['win'][i][0]],
                                                                                   [coil['win'][i][1]],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None],
                                                                                   [None]]

        else:
            sheet.Range(f"{sclst[position][0]}43:{sclst[position][0]}56").Value = [[f"x-{windings[i - 2]}"], [None],
                                                                                   [None], [None],[coil['win'][i][0]],
                                                                                    [coil['win'][i][1]], [None],
                                                                                   ['-'], ['-'], ['-'], ['-'], ['-'],
                                                                                   ['-']]
        position += 1
    sheet.Cells(44, 7).Value = info['voltage']
    sheet.Cells(45, 7).Value = info['maxvoltage']
    sheet.Cells(46, 7).Value = float_or_int(coil['sec_pow'],0)

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
        sheet.Cells(37, 23).Value = query.value(1)
    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено руководство по эксплуатации для трансформатора {info['fullname']}",
                            QMessageBox.Ok)


def fill_ticket_ols(info):
    print(info)
    sheet = wb.ActiveSheet
    coil = get_nominal_current(info['idTransformer'])
    sheet.Cells(4, 2).Value = info['fullname']
    sernum = f"№{info['makedate']}-{info['serialnumber']}"
    tu = info['tu']
    weight = str(int(info['weight'])) + ' кг'
    year = f"20{info['makedate']} г"
    power = float_or_int(coil['sec_pow'])
    sheet.Cells(12, 2).Value = f"{tu}      {weight}          20{info['data1']}г"
    sheet.Cells(5, 2).Value = f"  ном. мощность  {power} ВА"
    sheet.Cells(5, 10).Value = sernum

    # формируем таблицу______________________________________________________
    sc = 5  # начальная координата
    sclst = {}  # словарь хранит координаты для внесения результатов обмотки
    countW = get_count_win(info['idTransformer']) - 1
    print(11, countW)
    first, last = col_column(countW, 10)
    print(1112, first, last)

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
        sheet.Range(f"{x}6:{y}6").Merge()
        sheet.Range(f"{x}7:{y}7").Merge()
        sheet.Range(f"{x}8:{y}8").Merge()
        sc += 1
    longP = 235  # ширина столбцов обмоток в пикселях
    s = 0
    for i in range(1, len(sclst) + 1):
        print(332323)
        koef = longP / countW / sclst[i][2]
        s += sheet.Range(sclst[i][1]).ColumnWidth * sclst[i][2]
        sheet.Range(sclst[i][1]).ColumnWidth = pickel_dict[int(koef)]
    position = 1
    # заполняем таблицу
    print(coil)
    for i in coil['win']:
        if i == 0:
            continue
        print(3332,i)
        print([coil['win'][i][0]])
        sheet.Range(f"{sclst[position][0]}6:{sclst[position][0]}8").Value = [ [f"x-{windings[i-2]}"], [coil['win'][i][0]],[coil['win'][i][1]] ]
        position += 1

def data_OLSprotocol():
    sql_params = """select name from params
                    order by date_begin DESC
                    limit 1"""

    quer = QSqlQuery(sql_params)
    if quer.first():
        doc  = quer.value(0)
        print(111111,doc)

    if model.rowCount() < 1:
        print(4434, model.rowCount() )
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return

    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()
    print(44444444444444444444444444444444444444,model.rowCount())
    for i in range(model.rowCount()):
        nomer = f"{model.index(i, 6).data()}-{model.index(i, 5).data()}"
        item = model.index(i,13).data()
        shname = model.index(i,3).data()
        # year = '20' + str(model.index(i,6).data())
        year = model.index(i,8).data().toString('yyyy')
        data = model.index(i,8).data().toString('dd.MM.yyyy')
        temp = model.index(i,9).data()
        hum = model.index(i,10).data()
        pres = model.index(i,11).data()
        idTr = model.index(i,12).data()
        oper = model.index(i,14).data()
        num_protokol = "ПРОТОКОЛ №" + str(year) +"/" +  str(model.index(i,0).data()) + 'ПСИ'
        tu = model.index(i,7).data()
        sn = model.index(i, 5).data()
        test = model.index(i, 16).data()
        name_defect = model.index(i, 17).data()
        print(1111111111111111111,num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect)
        fill_file(num_protokol,item,shname,year,data,temp,hum,pres,oper,doc, nomer,tu,sn, idTr, test, name_defect )
        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            pass
            # printRep()





def get_nominal_current(idTransformer):
    model_current = QSqlQueryModel()
    sql =  f"select * from coil where transformer = {idTransformer} order by coilnumber, tap"
    print(sql)
    model_current.setQuery(sql)
    num_cur = {}
    num_cur['win'] = {}
    num_cur['win'][0] = []

    for i in  range(model_current.rowCount()):
        if model_current.index(i,2).data() == 1 and model_current.index(i,3).data() == 2:
            num_cur['primary_cur'] = model_current.index(i,6).data()
            num_cur['sec_vol'] = model_current.index(i,7).data()
            num_cur['sec_pow'] = model_current.index(i,8).data()
        if model_current.index(i,2).data() != 0 and model_current.index(i,3).data() != 0:
            num_cur['win'][model_current.index(i, 3).data()] = [float_or_int(model_current.index(i, 7).data())]

    num_cur['win'][0] = [num_cur['primary_cur']]

    #получаем токи для обмоток для первичной забираем из таблицы под индексом 3 для остальных прибавляем по два индекса к текущей обмотке
    sql_cur = f"select * from nominal_current_ols where power = {num_cur['sec_pow']} and voltage_x_a1 = {num_cur['sec_vol']} and primary_voltage = {num_cur['primary_cur']}"
    query1 = QSqlQuery(sql_cur)
    if query1.first():
        for i in num_cur['win']:
            index = 2
            if i == 0:
                index = 3
            num_cur['win'][i].append(query1.value(index+i))
    return num_cur


# ЭТИКЕТКА ДЛЯ КТ И R
def stickerRKT():
    for i in range(model.rowCount() - 1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()

    for i in range(model.rowCount()):
        nomer = f"{model.index(i, 3).data()}-{model.index(i, 2).data()}"
        print(nomer)
        item = model.index(i, 0).data()
        print(item)
        shname = model.index(i, 4).data()
        print(shname)
        namest = model.index(i, 6).data()
        print(namest)
        oper = model.index(i, 5).data()
        print(oper)
        data = model.index(i, 7).data().toString('dd.MM.yyyy')
        print(data)
        sheet = wb.ActiveSheet
        a1 = sheet.Cells(1, 1).Value = f"{nomer} {oper} {data}"
        a2 = sheet.Cells(2, 1).Value = f"{namest}"
        windings = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
        dictRes = resultDict(item, shname)
        if dictRes == {}:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные истытания трансформатора {shname}", QMessageBox.Ok)
            return

        try:
            b4 = sheet.Cells(4, 2).Value = dictRes[0][0]
            # sheet.Cells(4, 2).Font.Bold = True
            # sheet.Cells(4, 2).Font.Size = 20
        except:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствует  сопротивление первичной обмотки трансформатора {shname}", QMessageBox.Ok)
            print(dictRes)

        try:
            cor = 3  # от этой точки начинаем рисовать сетку
            for j in range(len(dictRes) - 1):
                mx = sheet.Cells(3, cor)
                my = sheet.Cells(5, cor)
                x = mx.Address
                y = my.Address
                sheet.Range(f"{x}:{y}").Borders.LineStyle = True
                sheet.Cells(3, cor).Value = windings[j]
                # sheet.Cells(3, cor).Font.Bold = True
                # sheet.Cells(3, cor).Font.Size = 20
                # sheet.Cells(3, cor).HorizontalAlignment = const.xlCenter
                sheet.Cells(4, cor).Value = dictRes[j + 2][0]
                # sheet.Cells(4, cor).Font.Bold = True
                # sheet.Cells(4, cor).HorizontalAlignment = const.xlCenter
                # sheet.Cells(4, cor).Font.Size = 18
                sheet.Cells(5, cor).Value = dictRes[j + 2][1]
                # sheet.Cells(5, cor).Font.Bold = True
                # sheet.Cells(5, cor).HorizontalAlignment = const.xlCenter
                # sheet.Cells(5, cor).Font.Size = 18
                cor += 1
        except:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные испытания трансформатора {shname}", QMessageBox.Ok)

        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            print(34534654356)
            # printRep()

def select_passportOLS(items,func,controler = True):
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
        info['idsn'] = model.index(i, 2).data()
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
        info['maxPover'] =   float_or_int(model.index(i, 21).data(),0,2)
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


def stickerKT():
    for i in range(model.rowCount()-1):
        ws = wb.Worksheets(1)
        ws.Copy(Before=wb.Worksheets(1))
        wb.Worksheets(1).Activate()

    for i in range(model.rowCount()):
        print(1111,i)
        nomer = f"{model.index(i, 3).data()}-{model.index(i, 2).data()}"
        print(nomer)
        item = model.index(i, 0).data()
        print(item)
        shname = model.index(i, 4).data()
        print(shname)
        namest = model.index(i, 6).data()
        print(namest)
        oper = model.index(i, 5).data()
        print(oper)
        data = model.index(i, 7).data().toString('dd.MM.yyyy')
        print(data)
        sheet = wb.ActiveSheet
        a1 = sheet.Cells(1, 1).Value = f"{nomer} {oper} {data}"
        a2 = sheet.Cells(2, 1).Value = f"{namest}"
        try:
            windings = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
            dictRes =  resultDict(item, shname)
            print(dictRes)
            # try:
            #     b4 = sheet.Cells(4, 2).Value = dictRes[0][0]
            #     sheet.Cells(4, 2).Font.Bold = True
            # except:
            #     QMessageBox.warning(None, f"Предупреждение",
            #                         f"Отсутствуют данные первичной обмотки трансформатора {shname}", QMessageBox.Ok)
            try:
                cor = 2 # от этой точки начинаем рисовать сетку
                for j in range(len(dictRes)):
                    mx = sheet.Cells(3, cor)
                    my = sheet.Cells(4, cor)
                    x = mx.Address
                    y = my.Address
                    sheet.Range(f"{x}:{y}").Borders.LineStyle = True
                    sheet.Cells(3, cor).Value = windings[j]
                    # sheet.Cells(3, cor).Font.Size = 20
                    # sheet.Cells(3, cor).HorizontalAlignment = const.xlCenter
                    sheet.Cells(4, cor).Value = dictRes[j+2][1]
                    cor+=1
            except:
                QMessageBox.warning(None, f"Предупреждение",
                              f"Ошибка выборки результатов испытания трансформатора {shname}", QMessageBox.Ok)
        except:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Проверьте или проведите испытание трасформатора {shname}", QMessageBox.Ok)


        if i < model.rowCount() - 1:
            wb.Worksheets(i + 2).Activate()
        else:
            print(34534654356)
            # printRep()






def select_Stikert(idItem):
    sql = f"""select item.id , item.test_map, serial_number.serialnumber, serial_number.makedate, transformer.fullname, operator.fio, stand.fullname, test_map.createdatetime, transformer.id  from item 
	            inner join serial_number on item.serial_number = serial_number.id
	            inner join transformer on serial_number.transformer = transformer.id
                inner join test_map on item.test_map = test_map.id
                inner join operator on test_map.operator = operator.id
                inner join stand on test_map.stand = stand.id
                where item.id in  ({idItem})"""

    print(sql)
    query = QSqlQuery(db)
    query.prepare(sql)

    if not query.exec_() or query.size() == 0:
        # print(323232323232323232323232323)
        # QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return False
    else:
        model.setQuery(query)
        return True



def select_repOLS(item):

    sql = f"""select  serial_number.id,
		serial_number.ordernumber,
		serial_number.series,
		serial_number.serialnumber,
		serial_number.makedate,
		serial_number.transformer,
		transformer.fullname from serial_number
    inner join transformer on serial_number.transformer = transformer.id
    where serial_number.id = {item}"""
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
        full_repOLS(on,ser,sn,year,tr,name, idsn)

    else:
        QMessageBox.warning(None, f"Предупреждение",
                            f"Не найдено информации по данному трансформатору", QMessageBox.Ok)


def full_repOLS(on,ser,sn,year,tr,name, idsn):
    wb.Worksheets(1).Activate()
    sheet = wb.ActiveSheet
    #
    # sheet.Range("E5:F6").Clear()
    # return

    # расписываем верхушку
    print(name)
    sheet.Cells(1, 3).Value = name
    sheet.Cells(2, 3).Value = f"{year}-{sn}"
    sheet.Cells(3, 3).Value = f"20{year}"
    sheet.Cells(2, 6).Value = ser
    sheet.Cells(3, 6).Value = on

    items = []

    # ищем по серийному номеру результы испытания КТ в цеху
    sql = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
    	                    INNER join test_map on item.test_map = test_map.id
    	                    inner join stand  on test_map.stand = stand.id
    	                    inner join operator on test_map.operator = operator.id
                            where serial_number = {idsn} and stand.test_type = 17
                            order by date  desc
                            limit 1
                           """
    cor = 2
    print(sql)
    query = QSqlQuery(sql)
    print(query.size())
    if query.size() == 1:
        model_2.setQuery(sql)
        item2 = model_2.index(0, 0).data()
        items.append(item2)
        sheet.Cells(7, 6).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        sheet.Cells(7, 3).Value = model_2.index(0, 4).data()

        dictRes = resultDict(item2, name)
        if dictRes == {}:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные истытания трансформатора {name}", QMessageBox.Ok)
            return
        else:
            print(32323234684684684684684984, dictRes)
            try:
                del dictRes[0]
            except:
                pass
            for j in range(len(dictRes)):
                sheet.Cells(6, cor).Value = dictRes[j + 2][1]
                cor += 1
            # sheet.Range("E5:F6").Clear()
            x = sheet.Cells(6, cor).Address
            sheet.Range(f"{x}:F5").Clear()

    # ищем по серийному номеру результы испытания КТ и R в цеху
    sql = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
    	                    INNER join test_map on item.test_map = test_map.id
    	                    inner join stand  on test_map.stand = stand.id
    						inner join operator on test_map.operator = operator.id
                            where serial_number = {idsn} and stand.test_type = 16
                            order by date  desc
                            limit 1
                                   """
    cor = 2
    print(sql)
    query = QSqlQuery(sql)
    print(query.size())
    if query.size() == 1:
        model_2.setQuery(sql)
        item1 = model_2.index(0, 0).data()
        items.append(item1)
        sheet.Cells(13, 7).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        print(1111111111111111, model_2.index(0, 3).data())
        sheet.Cells(13, 3).Value = model_2.index(0, 4).data()

        print(item1)
        dictRes = resultDict(item1, name)
        cor = 3  # от этой точки начинаем рисовать сетку
        if dictRes == {}:
            QMessageBox.warning(None, f"Предупреждение",
                                f"Отсутствуют данные истытания трансформатора {name}", QMessageBox.Ok)
            return
        else:
            sheet.Cells(11, 2).Value = dictRes[0][0]
            for j in range(len(dictRes) - 1):
                sheet.Cells(11, cor).Value = dictRes[j + 2][0]
                sheet.Cells(12, cor).Value = dictRes[j + 2][1]
                cor += 1
            x = sheet.Cells(10, cor).Address
            sheet.Range(f"{x}:H12").Clear()
            print(434343, cor)

    # ищем по серийному номеру результы испытания на высоковольтных
    hv = searchHV(item2)
    if hv:
        sheet.Cells(17, 3).Value = hv[0]
        sheet.Cells(17, 1).Value = hv[1].toString('dd.MM.yyyy')
    print("высокие не найдены")
    # дата печати
    sheet.Cells(28, 7).Value = datetime.datetime.now().strftime("%d.%m.%Y")

    sql = f"""select item.id, test_map, stand.fullname, test_map.createdatetime as date, operator.fio from item
        	                    INNER join test_map on item.test_map = test_map.id
        	                    inner join stand  on test_map.stand = stand.id
        						inner join operator on test_map.operator = operator.id
                                where serial_number = {idsn} and stand.test_type = 18 
                                order by date  desc
                                limit 1
                                       """
    cor = 2
    print(sql)
    query = QSqlQuery(sql)
    print(query.size())

    if query.size() == 1:
        model_2.setQuery(sql)
        item3 = model_2.index(0, 0).data()
        items.append(item3)
        print(1111111111111111, model_2.index(0, 3).data())
        sheet.Cells(26, 7).Value = model_2.index(0, 3).data().toString('dd.MM.yyyy')
        print(1111111111111111, model_2.index(0, 3).data())
        sheet.Cells(26, 3).Value = model_2.index(0, 4).data()
        print(item3)
        dictRes = resultDict(item3, name)
        print(dictRes)
        try:
            if dictRes[0][3] != 0:
                H27 = sheet.Cells(22, 7).Value = dictRes[0][3]
            if dictRes[0][4] != 0:
                H28 = sheet.Cells(23, 7).Value = dictRes[0][4]
            if dictRes[0][2] != 0:
                H29 = sheet.Cells(24, 7).Value = dictRes[0][2]
            if dictRes[0][1] != 0:
                H30 = sheet.Cells(25, 7).Value = dictRes[0][1]
        except:
            print("Отсутствуют данные истытания  трансформатора")

            # переменные, от которых будем расписывать данные по обмоткам
        poleR0 = 20
        poleR1 = 21

        #  формирование строк для записи сопротивления
        try:
            if dictRes[0][0] != 0:
                sheet.Cells(poleR0, 7).Value = dictRes[0][0]
            for i in range(len(dictRes) - 1):
                sheet.Cells(poleR1, 5).EntireRow.Insert()
                sheet.Range(f"E{str(poleR1)}:F{str(poleR1)}").Merge()
                sheet.Cells(poleR1, 5).Value = windings[i]
                if dictRes[i + 2][0] != 0:
                    sheet.Cells(poleR1, 7).Value = dictRes[i + 2][0]
                poleR1 += 1
            # #  формирование строк для записи кт
            if dictRes[2][1] != 0:
                sheet.Cells(poleR1, 7).Value = dictRes[2][1]
                print(dictRes[2][2])
            poleR1 += 1
            for i in range(len(dictRes) - 2):
                sheet.Cells(poleR1, 5).EntireRow.Insert()
                sheet.Range(f"E{str(poleR1)}:F{str(poleR1)}").Merge()
                sheet.Cells(poleR1, 5).Value = windingsKT[i]
                if dictRes[i + 3][1] != 0:
                    sheet.Cells(poleR1, 7).Value = dictRes[i + 3][1]
                    print(dictRes[i + 3][2], i + 3)
                poleR1 += 1
            print(poleR0)
            print(poleR1)
        except:
            pass

        # ищем дефекты по  указанным itemam
    sqlD = f"""select item.id, defect, defect.fullname from item
                        left JOIN defect on item.defect = defect.id
                        where item.id in {tuple(items)}"""
    print(sqlD)
    model_3.setQuery(sqlD)
    defect = 0
    for i in range(model_3.rowCount()):
        if model_3.index(i, 1).data() != 0:
            defect = model_3.index(0, 4).data()

    for i in wb.Worksheets(1).Range("A20:A34"):
        if i.Value == "Результат:":
            if defect != 0:
                sheet.Cells(int(str(i.Address)[3:]), 7).Value = defect




#   """
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
def check_EAN_valid(serNum, data):
    _serNum = f'9{serNum.zfill(6)}{data}00'

    arrNum = []
    for item in _serNum:
        arrNum.append(varToInt(item))
    res = (arrNum[1] + arrNum[3] + arrNum[5] + arrNum[7] + arrNum[9] + arrNum[11]) * 3
    res = res + (arrNum[0] + arrNum[2] + arrNum[4] + arrNum[6] + arrNum[8] + arrNum[10])
    res = varToInt(str(res)[len(str(res)) - 1])
    if res > 0:
        res = 10 - res

    sernum = ''.join(map(str, arrNum))[:-1] + str(res)
    sn = f'''="("&{sernum}&")"'''

    # sn = sernum
    return sn

# # # #
# from PyQt5.QtWidgets import QApplication
# import sys
# # # # #
# # pp = QApplication(sys.argv)
# # if open_excel('passportOLS.xlsx', None, visible=1):
# #     select_resultOLS(2015960, fill_passportOLS_blank)
# pp = QApplication(sys.argv)
# if open_excel('ticket_ols.xlsx', None, visible=1):
#     select_resultOLS(2015960, fill_ticket_ols)

# if open_excel('protocolTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 0):
#     data_TN(fill_TNpoverka)
# # #     printRep()
# # # #
#



# if open_excel('passportTN.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     sheet = wb.ActiveSheet
#     arr = [[1],[2],[3],[4],[5],[6],[7]]
#     sheet.Range("A1:A7").Value = arrQ


# #
# gbpltw

# #
# if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#      select_result(627986, idItem= 2000491, tested="--")
#      data_TN(fill_TNpoverka)
# # # #
#
# # # # #
# if open_excel('passportTN.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportTN(628215, 2001051)
# if open_excel('passportTN.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportTN(626515, 1996184) 628215 and item.id = 2001051
#     select_passportTN(626515, 1996184)


#     stickerTTP('P')
# parser_name_tt(1923600)



#
# if open_excel('passportOLS.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportOLS(2302671, fill_passportOLS_full)

# #
# if open_excel('stickerOLS.xlsx','HP LaserJet Pro MFP M127-M128 PCLmS'):
#     # Excel.Application.ScreenUpdating = False
#     select_Stikert(578234 )
#     stickerRKT()
# #
# # #

#
# #
# import time
# t1 = time.time()
# if open_excel('OLS.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_result(615378, 1965697)
#     data_OLSprotocol()
# t2 = time.time()
# t3 = t2 - t1
# print('Время выполнения', t3)


#     print(1)

# if open_excel('stickerKT.xlsx','ZDesigner TLP 2824 Plus (ZPL)'):
#     select_Stikert(578212 ,1859344)
#     stickerKT()
# open_excel('OLS.xlsx','hp LaserJet 1320 series (10.5.0.20)')

