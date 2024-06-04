import datetime
import time

import win32print
from win32com.client import constants as const
import win32com.client
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
import math
from report_otk import reportTN , reportTT , reportOLS , reportTP
import os


# Основные объекты VBA http://bourabai.ru/einf/vba/2-04.htm

model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()

basedir = os.path.abspath(os.getcwd())
path = '\\'.join(basedir.split('\\')[:2]) + '\\report_otk\\'


def destroy_excel():
    os.system("taskkill /f /im excel.exe")


def printing_TT(result, params, printers, kontroler):
    print(1,result)
    print(2,params)
    print(333332323,kontroler)
    printer_rep =  printers['report']
    printer_tick = printers['sticker']
    # log.info('принтер этикеток' + printer_tick )
    # сначало печатаем полные, потом пустые
    for i in ['full','half']:
        if 'passport' in params:
            items = get_items(result, 'passportItem', i)
            if items:
                if reportTT.open_excel(path+'passportTT.xlsx', printer_rep , visible=0):
                    reportTT.select_passportTT(items,reportTT.fill_passportTT_full,kontroler)
                    reportTT.printRep()
                    time.sleep(0.5)
                    destroy_excel()

        if 'ticket' in params:
            print(65547456757476)
            items = get_items(result, 'ticketItem',i)
            if items:
                print(items)
                print(87878787878)
                if reportTT.open_excel(path+'ticket_tt.xlsx', printer_tick,0):
                    reportTT.select_passportTT(items,reportTT.fill_ticket_tt)
                    reportTT.printRep()
                    time.sleep(0.5)
                    destroy_excel()

        if 'poverka' in params:
            items = get_items(result, 'poverkaItem',i)
            if items:
                reportTT.select_result(items)
                if reportTT.open_excel(path+'poverkaTT.xlsx', printer_rep, visible=0 ):
                    reportTT.TTpoverka(reportTT.fill_poverkaTT_full)
                    reportTT.printRep()
                    time.sleep(0.5)
                    destroy_excel()


        if 'psi' in params:
            items = get_items(result, 'psiItem', i)
            if items:
                reportTT.select_result(items)
                if reportTT.open_excel(path + 'protocolTT.xlsx', printer_rep , visible=0):
                    reportTT.data_TT(reportTT.fill_TTprotocol_full)
                    reportTT.printRep()
                    time.sleep(0.5)
                    destroy_excel()
    # проверка печати этикеток у которых изменился коэф при этом печать этикеток была отключена
    if 'ticket' not in params:
        items  = check_print_new_ticket(result)
        if items:
            if reportTT.open_excel(path+'ticket_tt.xlsx', printer_tick,visible=0):
                reportTT.select_passportTT(items,reportTT.fill_ticket_tt)
                reportTT.printRep()




def printing_TN(result, params, printers,controler = False):
    print('знолы')
    print(result,params)
    printer_rep = printers['report']
    printer_tick = printers['sticker']
    for i in ['full','half']:
        items = get_items(result,'psiItem',i)

        if items:
            if 'psi' in params or 'poverka' in params:
                items = get_items(result,'psiItem','full')
                reportTN.select_result(items)

            if 'psi' in params:
                if reportTN.open_excel(path+'protocolTN.xlsx', printer_rep , visible=0):
                    reportTN.data_TN(reportTN.fill_TNprotocol_full)
                    reportTN.printRep()
                    time.sleep(0.5)
            if 'poverka' in params:
                if reportTN.open_excel(path+'poverkaTN.xlsx', printer_rep , visible=0):
                    reportTN.data_TN(reportTN.fill_TNpoverka_full)
                    reportTN.printRep()
                    time.sleep(0.5)
            if 'passport' in params:
                if reportTN.open_excel(path+'passportTN.xlsx', printer_rep , visible=0):
                    reportTN.select_passportTN(items,reportTN.fill_passportTN_full,controler)
                    reportTN.printRep()
                    time.sleep(0.5)
            if 'ticket' in params:
                if reportTN.open_excel(path+'ticket_tn.xlsx', printer_tick,visible=0):
                    reportTN.select_passportTN(items,reportTN.fill_ticket_tn)
                    reportTN.printRep()
                    time.sleep(0.5)

def printing_TP(result, params, printers, controler=False):
        print('.................ТП')
        print(result,params,printers)
        printer_rep = printers['report']
        printer_tick = printers['stickerDop']
        for i in ['full', 'half']:
            items = get_items(result, 'psiItem', i)

            if items:
                if 'psi' in params:
                    items = get_items(result, 'psiItem', 'full')
                    reportTP.select_result(items)
                    if reportTP.open_excel(path + 'protocolTP.xlsx', printer_rep, visible=0):
                        reportTP.data_TP(reportTP.fill_TPprotocol_full)
                        reportTP.printRep()
                        time.sleep(0.5)

                if 'passport' in params:
                    if reportTP.open_excel(path + 'passportTP.xlsx', printer_rep, visible=0):
                        reportTP.select_passportTP(items, reportTP.fill_passportTP_full, controler)
                        reportTP.printRep()
                        time.sleep(0.5)
                if 'ticket' in params:
                    if reportTP.open_excel(path + 'ticket_tp.xlsx', printer_tick, visible=0):
                        reportTP.select_passportTP(items, reportTP.fill_ticket_tp)
                        reportTP.printRep()
                        time.sleep(0.5)

    # # печатаем пустышки для ручного заполнения документов
    # items = get_items(result, 'item')
    # if items:
    #
    #     if 'psi' in params or 'poverka' in params:
    #         reportTN.select_result(items)
    #
    #     if 'psi' in params:
    #         if reportTN.open_excel(path+'protocolTN.xlsx', printer_rep , visible=1):
    #             reportTN.data_TN(reportTN.fill_TNprotocol_blank)
    #
    #     if 'poverka' in params:
    #         if reportTN.open_excel(path+'poverkaTN.xlsx', printer_rep , visible=1):
    #             reportTN.data_TN(reportTN.fill_TNpoverka_blank)
    #
    #     if 'passport' in params:
    #         if reportTN.open_excel(path+'passportTN.xlsx', printer_rep , visible=1):
    #             reportTN.select_passportTN(items,reportTN.fill_passportTN_blank)
    #                 # printRep(self.log)

def printing_OLS(result, params, printers):
    printer_rep = printers['report']
    printer_tick = printers['sticker']
    print(121212,result)
    for i in ['full', 'half']:
        items = get_items(result, 'psiItem', i)
        if items:
            if 'psi' in params:
                reportOLS.select_result(items)
                if reportOLS.open_excel(path+'protocolOLS.xlsx', printer_rep, visible=0):
                    reportOLS.fill_psi_ols(reportOLS.fill_file)
                    reportOLS.printRep()
                    time.sleep(0.5)

                    # printRep(self.log)

            if 'passport' in params:
                if reportOLS.open_excel(path+'passportOLS.xlsx', printer_rep, visible=0):
                    reportOLS.select_passportOLS(items, reportOLS.fill_passportOLS_full)
                    reportOLS.printRep()
                    time.sleep(0.5)

            if 'ticket' in params:
                print(8678678, printer_tick)
                items = get_items(result, 'ticketItem', i)
                if reportOLS.open_excel(path+'ticket_ols.xlsx', printer_tick,visible=0):
                    reportOLS.select_resultOLS(items,reportOLS.fill_ticket_ols)
                    reportOLS.printRep()
                    time.sleep(0.5)


def get_items(result,item, full):
    items = []
    for key in result:
        print(key)
        if result[key][item][0] ==   full:
            items.append(result[key][item][1])

    items = ','.join(map(str, items))
    if items == []:
        return False
    return items


def check_print_new_ticket(result):
    items = []
    for key in result:
        if result[key]['new_ticket']:
            items.append(result[key]['item'])
    if items == []:
        return False
    items = ','.join(map(str, items))
    return items




# def get_items(result,item):
#     items = []
#     for key in result:
#         if result[key]['fill']:
#             try:
#                 items.append(result[key][item])
#             except KeyError:
#                 pass
#     items = ','.join(map(str, items))
#     if items == []:
#         return False
#     return items



def check_printer(excel, namePrint):
    for i in range(9):
        try:
            global np
            np = f'{namePrint} (Ne0{i}:)'
            print(np)
            excel.ActivePrinter = np
            return True
        except:
            pass
    return False

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


# поиск оператора проводившего высокольтные испытания

def searchHV(item):
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
                stand.test_type = 8
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
        return (oQuerry1.value(0),oQuerry1.value(1))

    return False


def printRep(wb,Excel):
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

# #
# from PyQt5.QtWidgets import QApplication
# import sys
# # # # #
# pp = QApplication(sys.argv)
# if open_excel('passportTN.xlsx','hp LaserJet 1320 series (10.5.0.20)'):
#     select_passportTN(1969922)
# # # if open_excel('poverkaTN.xlsx','hp LaserJet 1320 series (10.5.0.20)' , visible= 0):
# # #     data_TN(fill_TNpoverka)
