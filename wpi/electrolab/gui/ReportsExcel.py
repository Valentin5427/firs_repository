# -*- coding: utf-8 -*-
from win32com.client import Dispatch, constants

from PyQt5.QtWidgets import QMessageBox


import math
import datetime

import os, stat

from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt5.uic.properties import QtGui

model_ = QSqlQueryModel()
model = QSqlQueryModel()
model_2 = QSqlQueryModel()
model_3 = QSqlQueryModel()
model_4 = QSqlQueryModel()


import locale
locale.setlocale(locale.LC_NUMERIC, '')
decimal_point = locale.localeconv()['decimal_point']


#name_msr_etalon = ''
#name_msr_vspom = ''

def BAX(A, V, in_diameter, out_diameter, weight_magnetic, dens_iron, CoefVoltmeter, ControlLoops):
        print("RepExcel1q", A, V)
        try:  
            try:
                xl = Dispatch('Excel.Application')
            except:
                print("Не запускается Excel")
                return    
                      
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            
            ws.Name = u'ВАХ'
            ws.Cells(2, 1).Value = "V"
            ws.Cells(2, 2).Value = "A"
            lenA = len(A)
            for i in range(0, lenA):
                ws.Cells(i+3, 1).Value = V[i]
                ws.Cells(i+3, 2).Value = A[i]
            
            ws.Range('A2:B' + str(lenA + 2)).Select()
            xl.Selection.HorizontalAlignment = 3
            
            for i in range(4):
                xl.Selection.Borders(i+1).LineStyle = 1
            ws.Range('A2:B2').Select()  # Без этой команды строятся два графика ??????????????????????????
            chart = xl.Charts.Add()            
#            chart = xl.AddChart(72, 10, 30, 50, 70)            
#            chart = xl.Charts.Add(72, 10, 30, 50, 70)  

            '''
You can specify the location at the time of creation of the chart 
expression.AddChart(Type, Left, Top, Width, Height) see here.
If you don't want to embed the chart in a worksheet, you can create a chart sheet :
 wb.Worksheets.Add(Type:=xlChart) Caveat : Microsoft.interop.Excel not win32com, but should work.
python excel charts win32com
            '''
                      
#            chart.ChartType = 65
            chart.ChartType = 72
            series = chart.SeriesCollection(1)
            series.Name = u"ВАХ"
            series.XValues = ws.Range('B3:B' + str(lenA + 2) )
            series.Values = ws.Range('A3:A' + str(lenA + 2))
                        
            chart.Location (2, Name=ws.Name)

            ws = wb.Worksheets(2)            
            ws.Name = u'Характеристика намагничивания'
            ws.Activate()
            
            ws.Cells(1, 1).ColumnWidth = 30            
            ws.Cells(1, 3).ColumnWidth = 5            
            ws.Cells(1, 4).ColumnWidth = 2            
            ws.Cells(1, 5).ColumnWidth = 30            
            
            ws.Cells(1, 1).Value = u"Внутренний диаметр     Dвнутр."
            ws.Cells(2, 1).Value = u"Наружний диаметр       Dнар."
            ws.Cells(3, 1).Value = u"Вес магнитопровода     Р"
            ws.Cells(1, 2).Value = in_diameter
            ws.Cells(2, 2).Value = out_diameter
            ws.Cells(3, 2).Value = weight_magnetic
            ws.Cells(1, 3).Value = u"мм"
            ws.Cells(2, 3).Value = u"мм"
            ws.Cells(3, 3).Value = u"кг"
            
            ws.Cells(1, 8).Value = u"Удельный вес электротехнического железа  - "
            ws.Cells(2, 8).Value = u"Коэф для вольтметра с действ. Знач. Напряж."
            ws.Cells(3, 8).Value = u"Контрольные витки на магнитопров."
            ws.Cells(1, 13).Value = dens_iron
            ws.Cells(2, 13).Value = CoefVoltmeter
            ws.Cells(3, 13).Value = ControlLoops
            ws.Cells(1, 14).Value = u"кг/м³"
                        
            ws.Cells(1, 5).Value = u"Диаметр средней линии      Dср."
            ws.Cells(2, 5).Value = u"Длинна средней линии       Lср."
            ws.Cells(3, 5).Value = u"Коэф. заполнения           Q"
            ws.Cells(4, 5).Value = u"К(Втл)"
            ws.Cells(1, 6).Formula = "=(B1+B2)/2000"   # F1
            ws.Cells(2, 6).Value = "=3.14*F1"          #F2
            ws.Cells(3, 6).Value = "=B3/(F2*M1)"       #F3
            ws.Cells(4, 6).Value = "=(M2/F3)/M3"       #F4
            ws.Cells(1, 7).Value = u"м"
            ws.Cells(2, 7).Value = u"м"

            rt = 6
            ct = 6
            ws.Cells(rt, ct).Value = u"Bтл (тесла)"
            ws.Cells(rt, ct+1).Value = "V"
            ws.Cells(rt, ct+2).Value = "A"
            ws.Cells(rt, ct+3).Value = "A/m (н)"
            ws.Cells(rt, ct+5).Value = "m"
            lenA = len(A)
            for i in range(0, lenA):
                ws.Cells(i+rt+1, ct).Value   = '=R4C6*R[0]C[1]'
                ws.Cells(i+rt+1, ct+1).Value = V[i]
                ws.Cells(i+rt+1, ct+2).Value = A[i]
                ws.Cells(i+rt+1, ct+3).Value = '=R[0]C[-1]/R2C6'
                ws.Cells(i+rt+1, ct+5).Value = '=R[0]C[-5]/R[0]C[-2]'
                
            ws.Range(ws.Cells(rt, ct), ws.Cells(rt + lenA, ct + 5)).Select()                
            xl.Selection.HorizontalAlignment = 3
            for i in range(4):
                xl.Selection.Borders(i+1).LineStyle = 1
            
            ws.Range('I7:I27').Select()                
            
#            ws.Range('A2:B2').Select()  # Без этой команды строятся два графика ??????????????????????????
            chart = xl.Charts.Add()            
            chart.ChartType = 72
            series = chart.SeriesCollection(1)
            series.Name = u"Характеристика намагничивания"
            series.XValues = ws.Range('I7:I27')
            series.Values  = ws.Range('F7:F27')
            
            chart.Location (2, Name=ws.Name)
                        
        except:
            print("Неопознанная ошибка1 ... ")
    


# Пример для изучения 
#https://github.com/spidezad/pywinexcel/blob/master/pywinexcel/pyExcel.py


def BAX_coil(fullname, serialnumbel, zakaz, coilsInfa):
        import win32com.client.dynamic     
        print("RepExcel1qqq")
        try:  
            try:
                '''        
    import win32com.client.dynamic     
    xlapp = win32com.client.dynamic.Dispatch("Excel.Application") 
    xlapp.Visible = 1
    xlbook = xlapp.Workbooks.Add()
    sht = xlbook.Worksheets(1)
    chart = sht.ChartObjects().Add(100, 20, 30, 40) 
           '''
        
                xl = win32com.client.dynamic.Dispatch("Excel.Application")
         
        #        xl = Dispatch('Excel.Application')
            except:
                print ("Не запускается Excel")
                return    
            # print 'type(xl)=', type(xl)
                      
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            
            ws.Name = u'ВАХ'
            
            ws.Range('A1:L1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток'
            
            ws.Range('A3:B3').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Объект испытаний:'
            ws.Range('C3:L3').Select()
            xl.Selection.Merge()
            xl.Selection.Value = fullname
            
            ws.Range('A4:B4').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заводской номер:'
            ws.Range('C4').Select()
            xl.Selection.Merge()
            xl.Selection.Value = serialnumbel
            
            ws.Range('A5:B5').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заказ:'
            ws.Range('C5:L5').Select()
            xl.Selection.Merge()
            xl.Selection.Value = zakaz
            
            nr = 4
            for i in range(len(coilsInfa)):
                nr += 2
                ws.Range('A' + str(nr) + ':' + 'B' + str(nr)).Select()
                xl.Selection.Merge()
                xl.Selection.Value = u'Катушка:'
#                ws.Range('C' + str(nr) + ':' + 'L' + str(nr)).Select()
                ws.Range('C' + str(nr)).Select()
                xl.Selection.Merge()
                xl.Selection.Value = coilsInfa[i]['coil']
                
                nr += 1
                ws.Cells(nr, 1).Value = "A"
                ws.Cells(nr, 2).Value = "V"
                
                for j in range(len(coilsInfa[i]['points'])):
                    nr += 1
                    ws.Cells(nr, 1).Value = coilsInfa[i]['points'][j][0]
                    ws.Cells(nr, 2).Value = coilsInfa[i]['points'][j][1]


                
            #???    ws.Range('I7:I27').Select()                
            
#            ws.Range('A2:B2').Select()  # Без этой команды строятся два графика ??????????????????????????
                '''
self.xlChart = self.xlBook.Sheets(sheet).ChartObjects().Add(
Left = left, Width = width, Top = top,
Height = height)
'''
               #wb     
                '''    
                #chart = xl.ChartObjects().Add(5, 6, 7, 8)
                #return sht.ChartObjects().Add(left, top, width, height)                 
                print 'q'
                print ws.ChartObjects()
                print ws.ChartObjects.Add(5, 6, 7, 8)
                #chart = ws.ChartObjects().Add(5, 6, 7, 8) 
                chart = ws.ChartObjects().Add()
                print 'w'
                ''' 
                
                ws.Range('A' + str(nr - len(coilsInfa[i]['points']) + 1) + ':A' + str(nr)).Select()
                
                
                
                ###chart = xl.Charts.Add()

                chartObj = ws.ChartObjects().Add(100, 20, 300, 400) 
                chart = chartObj.Chart
                
                            
#                chart = xl.Charts.Add(Left = 10, Width = 100, Top = 20, Height = 200)            
#                chart = xl.Charts.Add(72, 10, 10, 200, 200)            

                chart.ChartType = 72



                series = chart.SeriesCollection()
                
                # print chartObj.Chart.SeriesCollection().Count
                new_series =chartObj.Chart.SeriesCollection().Count
                # print new_series
                # print chartObj.Chart.SeriesCollection(new_series).Values
                # print chartObj.Chart.SeriesCollection(1).XValues
                # print chartObj.Chart.SeriesCollection(new_series).XValues
                # print 5
                series.Values  = ws.Range('B' + str(nr - len(coilsInfa[i]['points']) + 1) + ':B' + str(nr))


                chart.Location(2, Name=ws.Name)
                
                continue

                
                #chart.Location(10,10)
                
#            series = chart.SeriesCollection().NewSeries()
                series = chart.SeriesCollection(1)
                series.Name = u"Характеристика намагничивания"
                # print '1111111111111111111'
                series.XValues = ws.Range('A8:A15')
                series.Values  = ws.Range('B8:B15')
                
                chart.Location(2, Name=ws.Name)

                nr += 2

            # return

            ws.Cells(2, 1).Value = "V"
            ws.Cells(2, 2).Value = "A"
            # return
            lenA = len(A)
            for i in range(0, lenA):
                ws.Cells(i+3, 1).Value = V[i]
                ws.Cells(i+3, 2).Value = A[i]
            
            ws.Range('A2:B' + str(lenA + 2)).Select()
            xl.Selection.HorizontalAlignment = 3
            
            for i in range(4):
                xl.Selection.Borders(i+1).LineStyle = 1
            ws.Range('A2:B2').Select()  # Без этой команды строятся два графика ??????????????????????????
            chart = xl.Charts.Add()            
            chart.ChartType = 72
            series = chart.SeriesCollection(1)
            series.Name = u"ВАХ"
            series.XValues = ws.Range('B3:B' + str(lenA + 2) )
            series.Values = ws.Range('A3:A' + str(lenA + 2))
                        
            chart.Location (2, Name=ws.Name)

            ws = wb.Worksheets(2)            
            ws.Name = u'Характеристика намагничивания'
            ws.Activate()
            
            ws.Cells(1, 1).ColumnWidth = 30            
            ws.Cells(1, 3).ColumnWidth = 5            
            ws.Cells(1, 4).ColumnWidth = 2            
            ws.Cells(1, 5).ColumnWidth = 30            
            
            ws.Cells(1, 1).Value = u"Внутренний диаметр     Dвнутр."
            ws.Cells(2, 1).Value = u"Наружний диаметр       Dнар."
            ws.Cells(3, 1).Value = u"Вес магнитопровода     Р"
            ws.Cells(1, 2).Value = in_diameter
            ws.Cells(2, 2).Value = out_diameter
            ws.Cells(3, 2).Value = weight_magnetic
            ws.Cells(1, 3).Value = u"мм"
            ws.Cells(2, 3).Value = u"мм"
            ws.Cells(3, 3).Value = u"кг"
            
            ws.Cells(1, 8).Value = u"Удельный вес электротехнического железа  - "
            ws.Cells(2, 8).Value = u"Коэф для вольтметра с действ. Знач. Напряж."
            ws.Cells(3, 8).Value = u"Контрольные витки на магнитопров."
            ws.Cells(1, 13).Value = dens_iron
            ws.Cells(2, 13).Value = CoefVoltmeter
            ws.Cells(3, 13).Value = ControlLoops
            ws.Cells(1, 14).Value = u"кг/м³"
                        
            ws.Cells(1, 5).Value = u"Диаметр средней линии      Dср."
            ws.Cells(2, 5).Value = u"Длинна средней линии       Lср."
            ws.Cells(3, 5).Value = u"Коэф. заполнения           Q"
            ws.Cells(4, 5).Value = u"К(Втл)"
            ws.Cells(1, 6).Formula = "=(B1+B2)/2000"   # F1
            ws.Cells(2, 6).Value = "=3.14*F1"          #F2
            ws.Cells(3, 6).Value = "=B3/(F2*M1)"       #F3
            ws.Cells(4, 6).Value = "=(M2/F3)/M3"       #F4
            ws.Cells(1, 7).Value = u"м"
            ws.Cells(2, 7).Value = u"м"

            rt = 6
            ct = 6
            ws.Cells(rt, ct).Value = u"Bтл (тесла)"
            ws.Cells(rt, ct+1).Value = "V"
            ws.Cells(rt, ct+2).Value = "A"
            ws.Cells(rt, ct+3).Value = "A/m (н)"
            ws.Cells(rt, ct+5).Value = "m"
            lenA = len(A)
            for i in range(0, lenA):
                ws.Cells(i+rt+1, ct).Value   = '=R4C6*R[0]C[1]'
                ws.Cells(i+rt+1, ct+1).Value = V[i]
                ws.Cells(i+rt+1, ct+2).Value = A[i]
                ws.Cells(i+rt+1, ct+3).Value   = '=R[0]C[-1]/R2C6'
                ws.Cells(i+rt+1, ct+5).Value   = '=R[0]C[-5]/R[0]C[-2]'
                
            ws.Range(ws.Cells(rt, ct), ws.Cells(rt + lenA, ct + 5)).Select()                
            xl.Selection.HorizontalAlignment = 3
            for i in range(4):
                xl.Selection.Borders(i+1).LineStyle = 1
            
            ws.Range('I7:I27').Select()                
            
            chart = xl.Charts.Add()            
            chart.ChartType = 72
            series = chart.SeriesCollection(1)
            series.Name = u"Характеристика намагничивания"
            series.XValues = ws.Range('I7:I27')
            series.Values  = ws.Range('F7:F27')
                        
            chart.Location (2, Name=ws.Name)
                        
        except:
            print("Неопознанная ошибка2 ... ")



def report(shortName, series, ordernumber, globalReport, _accuracyR, _accuracyI, LastTest):
        try:
            try:
                xl = Dispatch('Excel.Application')
            except:
                QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel!", QMessageBox.Ok)
                

                                
            wb = xl.Workbooks.Add()

            xl.Visible = True

            ws = wb.Worksheets(1)  
            ws.Name = u'Результаты проверки тока'

            ws.PageSetup.Orientation = 2

            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42
            ws.PageSetup.PrintTitleRows = "$4:$5"    # Для переноса малой шапки на следующие страницы


            ws.Cells(1, 1).ColumnWidth = 8            
            ws.Cells(1, 2).ColumnWidth = 12            
            ws.Cells(1, 3).ColumnWidth = 12            
            ws.Cells(1, 4).ColumnWidth = 10            
            ws.Cells(1, 5).ColumnWidth = 10    
            
            ws.Cells(1, 6).ColumnWidth = 10            
            ws.Cells(1, 7).ColumnWidth = 10            
            ws.Cells(1, 8).ColumnWidth = 10 
            ws.Cells(1, 9).ColumnWidth = 10            
            ws.Cells(1, 10).ColumnWidth = 12            
            ws.Cells(1, 11).ColumnWidth = 12            
                        


            ws.Range('A1:K1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток'
            ws.Range('A2:K2').Select()
            xl.Selection.Merge()

            xl.Selection.Value = u'Трансформатор: ' + shortName

            ws.Range('A3:K3').Select()
            xl.Selection.Merge()
            
            if ordernumber == None:
                xl.Selection.Value = u'Серия: ' + str(series)
            else:    
                xl.Selection.Value = u'Серия: ' + str(series) + u'    Заказ: ' + str(ordernumber)
            ws.Range("A4:K5").Select()
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.HorizontalAlignment = 3
            
            xl.Selection.VerticalAlignment = 2
                        
            xl.Selection.WrapText = True
            
            ws.Range("A5:N5").Select() #???????????
            xl.Selection.RowHeight *= 3
            

            ws.Range("A4:A5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Зав.\n№'
            
            ws.Range("B4:B5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'№ обмот.'
            
            ws.Range("C4:E4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Сопротивление'
            ws.Range("C5:C5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Величина'
            ws.Range("D5:E5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Коридор (' + str(_accuracyR) + '%)' 

            ws.Range("F4:F5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'K'
            
            ws.Range("G4:G5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'U, В'
            
            ws.Range("H4:H5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'I, А'
            
            ws.Range("I4:I5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Макс. значение'
            
            ws.Range("J4:J5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Дата испытания'
            ws.Range("K4:K5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Код тележки'
                        
            M = []
            k = 0
            
            for i in range(len(globalReport)):
                if globalReport[i][1] == series:
                    print(ordernumber, globalReport[i][2])
                    if ordernumber == None or (ordernumber != None and globalReport[i][2] == ordernumber):
                        if not LastTest or (LastTest and globalReport[i][17] != 0):
                            
                            
#                            R = [globalReport[i][3:]]
#                            R = [globalReport[i][3:7], globalReport[i][13], globalReport[i][8], globalReport[i][11:12], globalReport[i][14], globalReport[i][15]]
                            R = [[globalReport[i][3], globalReport[i][4], globalReport[i][5], globalReport[i][6], globalReport[i][7], globalReport[i][13], globalReport[i][8], globalReport[i][11], globalReport[i][12], globalReport[i][14], globalReport[i][15]]]

                            
                            M += R
                            
            ws.Range("A" + str(6) + ":K" + str(5 + len(M))).Select()

            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.Value = M
                        
            ws.Range("E" + str(6) + ":E" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0
            ws.Range("H" + str(6) + ":H" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0

            #17.05.2017
            ws.Range("J" + str(6) + ":J" + str(5 + len(M))).Select()
                        
            for i in range(len(M)):
                # Подкраска ячеек, не входящих в коридор
                if M[i][2] < M[i][3] or M[i][2] > M[i][4]:
                    xl.ActiveSheet.Cells(i + 6, 3).Interior.Color = 255            
 #               if M[i][5] < M[i][6] or M[i][5] > M[i][7]:
 #                   xl.ActiveSheet.Cells(i + 6, 6).Interior.Color = 255
                            
                # Группировка колонок
                if i != len(M) - 1:
                    if M[i][1] == M[i + 1][1]:
                        xl.ActiveSheet.Cells(i + 7, 2).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 2).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 2).Borders(3).LineStyle = 0
                        if i != len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 2).Borders(4).LineStyle = 0
                    '''        
                    if M[i][8] == M[i + 1][8]:
                        xl.ActiveSheet.Cells(i + 7, 9).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 9).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 9).Borders(3).LineStyle = 0
                        if i <> len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 9).Borders(4).LineStyle = 0
                            '''                        
        except:
            print("Неопознанная ошибка3 ... ")
                       
        return


def report_old1(shortName, series, ordernumber, globalReport, _accuracyR, _accuracyI, LastTest):
#         print 'globalReport =', globalReport
        #print 'ordernumber =', ordernumber     
        #print 'type(ordernumber) =', type(ordernumber) 
        #LastTest = False - вывод на печать всех испытаний    
        #LastTest = True  - вывод на печать только последних испытаний испытаний    
        try:
            try:
                xl = Dispatch('Excel.Application')
            except:
                QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel!", QMessageBox.Ok)
                
            # print 11
                
                
            wb = xl.Workbooks.Add()
            # print 12
            xl.Visible = True
                              
            # print 1
            ws = wb.Worksheets(1)  
            
            
                      
            #ws.Name = u'Результаты поверки тока намагничивания вторичных обмоток'
            ws.Name = u'Результаты проверки тока'

            ws.PageSetup.Orientation = 2

            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42
            ws.PageSetup.PrintTitleRows = "$4:$5"    # Для переноса малой шапки на следующие страницы

            # print 2

#            for i in range(10):            
#                ws.Cells(1, i + 1).ColumnWidth = 9
            ws.Cells(1, 1).ColumnWidth = 7            
#            ws.Cells(1, 2).ColumnWidth = 7            
            ws.Cells(1, 2).ColumnWidth = 9            
            ws.Cells(1, 3).ColumnWidth = 11            
            ws.Cells(1, 4).ColumnWidth = 9            
            ws.Cells(1, 5).ColumnWidth = 9            
            ws.Cells(1, 6).ColumnWidth = 11            
            ws.Cells(1, 7).ColumnWidth = 9            
            ws.Cells(1, 8).ColumnWidth = 9 
            #17.05.2017
            '''           
            ws.Cells(1, 9).ColumnWidth = 9            
            ws.Cells(1, 10).ColumnWidth = 9            
            ws.Cells(1, 11).ColumnWidth = 9            
            ws.Cells(1, 12).ColumnWidth = 9            
            ws.Cells(1, 13).ColumnWidth = 7
            '''            
            ws.Cells(1, 9).ColumnWidth = 11            
            ws.Cells(1, 10).ColumnWidth = 11            
            ws.Cells(1, 11).ColumnWidth = 9            
            ws.Cells(1, 12).ColumnWidth = 10            
            ws.Cells(1, 13).ColumnWidth = 10            
            #ws.Cells(1, 14).ColumnWidth = 7
                        
            # print 3

            ws.Range('A1:L1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток'
            ws.Range('A2:M2').Select()
            xl.Selection.Merge()
            # print 4
            xl.Selection.Value = u'Трансформатор: ' + shortName
            # print 5
            #
#            xl.Selection.Value = u'Трансформатор: ' + '123'
            ws.Range('A3:M3').Select()
            xl.Selection.Merge()
         #   print 'series', series
            
            
            if ordernumber == None:
                #QMessageBox.warning(None, u"Предупреждение",  's13321', QMessageBox.Ok)
                xl.Selection.Value = u'Серия: ' + str(series)
            else:    
                #QMessageBox.warning(None, u"Предупреждение",  's13322', QMessageBox.Ok)
                xl.Selection.Value = u'Серия: ' + str(series) + u'    Заказ: ' + str(ordernumber)
                #xl.Selection.Value = u'Серия: ' + series + u'    Заказ: ' + ordernumber
            #QMessageBox.warning(None, u"Предупреждение",  's1333', QMessageBox.Ok)
            #17.05.2017
            ws.Range("A4:M5").Select()
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.HorizontalAlignment = 3
            
#    With Selection
#        .HorizontalAlignment = xlCenter
#        .VerticalAlignment = xlCenter
#        .WrapText = True
#    Rows("5:5").RowHeight = 27.75            
            
            xl.Selection.VerticalAlignment = 2
                        
            xl.Selection.WrapText = True
            
            ws.Range("A5:N5").Select()
            xl.Selection.RowHeight *= 3
            

            ws.Range("A4:A5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Зав.\n№'
            
            ws.Range("B4:B5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'№ обмот.'
            
            ws.Range("C4:E4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Сопротивление'
            ws.Range("C5:C5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Величина'
            ws.Range("D5:E5").Select()
            xl.Selection.Merge()
#            xl.Selection.Value = u'Коридор (' + str(Devices.data['accuracy']['r']) + '%)' 
            xl.Selection.Value = u'Коридор (' + str(_accuracyR) + '%)' 

            ws.Range("F4:H4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Напряжение намагничивания'
            ws.Range("F5:F5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Величина, В'
            ws.Range("G5:H5").Select()
            xl.Selection.Merge()
#            xl.Selection.Value = u'Коридор (' + str(Devices.data['accuracy']['a']) + '%)'
            xl.Selection.Value = u'Коридор (' + str(_accuracyI) + '%)'
            
            
            #23.05.2017            
            ws.Range("I4:I5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Ток. намагн. А'
            
            ws.Range("J4:J5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Предель\nные значения'
            
            ws.Range("K4:K5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Коэфф. безопас.'
            '''
            ws.Range("K5:K5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Расчет-ный'
            
            ws.Range("L5:L5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заданный'
            '''
                        
            ws.Range("L4:L5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Дата поверки'
            ws.Range("M4:M5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Код тележки'
                        
                        
                        
            M = []
            k = 0

            for i in range(len(globalReport)):
                #20.04
                '''
                if globalReport[i][1] == int(series):
                    M += [globalReport[i][2:]]
                '''
#11.11.16   ошивка преобразования       if globalReport[i][1] == int(series):
          #      print globalReport[i][1], series
                
#                if unicode(globalReport[i][1]) == unicode(series):
                if globalReport[i][1] == series:

                    if ordernumber == None or (ordernumber != None and globalReport[i][2] == ordernumber):
                        #17.05.2017
                        #if not LastTest or (LastTest and globalReport[i][17] != 0):
                        if not LastTest or (LastTest and globalReport[i][17] != 0):
                            #17.05.2017
                            #M += [globalReport[i][3:]]
                            
                            #R = [globalReport[i][3:17]]
                            R = [globalReport[i][3:]]

                            #R[5:7] = globalReport[i][18:20]
                            '''
                            if globalReport[i][20] != None or globalReport[i][21] != None:
                                R[0][5] = globalReport[i][19]
                                R[0][6] = globalReport[i][20]
                                R[0][7] = globalReport[i][21]
                                R[0][8] = globalReport[i][22]
                                #19.05.2017
                                #R[0][9] = globalReport[i][23]
                                '''

                            M += R
#            self.globalReport += [[checking_2, series, ordernumber, serialnumber, coilname, round(r, 3),
# min_r, max_r, round(inom, 2), min_in, max_in, round(un, 2), round(un_, 2), round(k, 2), rating,
# createdatetime, idMap, idClass, id4, round(inom2, 2), min_in2, max_in2, round(sun2, 2), round(un2, 2)]]
                            

            #17.05.2017
            #ws.Range("A" + str(6) + ":M" + str(5 + len(M))).Select()
            ws.Range("A" + str(6) + ":M" + str(5 + len(M))).Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
#            print 1
            xl.Selection.Value = M
#            print 2
                        
            ws.Range("E" + str(6) + ":E" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0
            ws.Range("H" + str(6) + ":H" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0

            #17.05.2017
            ws.Range("J" + str(6) + ":J" + str(5 + len(M))).Select()
            ###xl.Selection.Borders(7).LineStyle = 0
                        
            for i in range(len(M)):
                # Подкраска ячеек, не входящих в коридор
                if M[i][2] < M[i][3] or M[i][2] > M[i][4]:
                    xl.ActiveSheet.Cells(i + 6, 3).Interior.Color = 255            
                if M[i][5] < M[i][6] or M[i][5] > M[i][7]:
                    xl.ActiveSheet.Cells(i + 6, 6).Interior.Color = 255

            #17.05.2017
                '''
                if M[i][14] == 1:
                    if M[i][10] > M[i][11]:
                        xl.ActiveSheet.Cells(i + 6, 11).Interior.Color = 255 
                if M[i][14] == 2:
                    if M[i][10] < M[i][11]:
                        xl.ActiveSheet.Cells(i + 6, 11).Interior.Color = 255
                        ''' 
                '''    
                if M[i][13] == 1:
                    if M[i][9] > M[i][10]:
                        xl.ActiveSheet.Cells(i + 6, 10).Interior.Color = 255 
                if M[i][13] == 2:
                    if M[i][9] < M[i][10]:
                        xl.ActiveSheet.Cells(i + 6, 10).Interior.Color = 255 
                '''
                            
                # Группировка колонок
                if i != len(M) - 1:
                    if M[i][1] == M[i + 1][1]:
                        xl.ActiveSheet.Cells(i + 7, 2).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 2).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 2).Borders(3).LineStyle = 0
                        if i != len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 2).Borders(4).LineStyle = 0
                    if M[i][8] == M[i + 1][8]:
                        xl.ActiveSheet.Cells(i + 7, 9).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 9).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 9).Borders(3).LineStyle = 0
                        #4.02
                        #xl.ActiveSheet.Cells(i + 7, 10).Value = ''                        
                        #xl.ActiveSheet.Cells(i + 6, 10).Borders(4).LineStyle = 0
                        #xl.ActiveSheet.Cells(i + 7, 10).Borders(3).LineStyle = 0
                        if i != len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 9).Borders(4).LineStyle = 0
                            #xl.ActiveSheet.Cells(i + 7, 10).Borders(4).LineStyle = 0
                        
        except:
            print("Неопознанная ошибка3 ... ")
                       
        return


def report_old(shortName, series, ordernumber, globalReport, _accuracyR, _accuracyI, LastTest):
        # print 'globalReport =', globalReport
        #print 'ordernumber =', ordernumber     
        #print 'type(ordernumber) =', type(ordernumber) 
        #LastTest = False - вывод на печать всех испытаний    
        #LastTest = True  - вывод на печать только последних испытаний испытаний    
        try:
            try:
                xl = Dispatch('Excel.Application')
            except:
                QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel!", QMessageBox.Ok)
                
            # print 11
                
                
            wb = xl.Workbooks.Add()
            # print 12
            xl.Visible = True
                              
            # print 1
            ws = wb.Worksheets(1)  
            
            
                      
            #ws.Name = u'Результаты поверки тока намагничивания вторичных обмоток'
            ws.Name = u'Результаты проверки тока'

            ws.PageSetup.Orientation = 2

            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42
            ws.PageSetup.PrintTitleRows = "$4:$5"    # Для переноса малой шапки на следующие страницы

            # print 2

#            for i in range(10):            
#                ws.Cells(1, i + 1).ColumnWidth = 9
            ws.Cells(1, 1).ColumnWidth = 6            
#            ws.Cells(1, 2).ColumnWidth = 7            
            ws.Cells(1, 2).ColumnWidth = 8            
            ws.Cells(1, 3).ColumnWidth = 9            
            ws.Cells(1, 4).ColumnWidth = 8            
            ws.Cells(1, 5).ColumnWidth = 8            
            ws.Cells(1, 6).ColumnWidth = 9            
            ws.Cells(1, 7).ColumnWidth = 8            
            ws.Cells(1, 8).ColumnWidth = 8 
            #17.05.2017
            '''           
            ws.Cells(1, 9).ColumnWidth = 9            
            ws.Cells(1, 10).ColumnWidth = 9            
            ws.Cells(1, 11).ColumnWidth = 9            
            ws.Cells(1, 12).ColumnWidth = 9            
            ws.Cells(1, 13).ColumnWidth = 7
            '''            
            ws.Cells(1, 9).ColumnWidth = 8            
            ws.Cells(1, 10).ColumnWidth = 8            
            ws.Cells(1, 11).ColumnWidth = 9            
            ws.Cells(1, 12).ColumnWidth = 9            
            ws.Cells(1, 13).ColumnWidth = 9            
            ws.Cells(1, 14).ColumnWidth = 7

            ws.Range('A1:L1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток'
            ws.Range('A2:M2').Select()
            xl.Selection.Merge()

            xl.Selection.Value = u'Трансформатор: ' + shortName

            
#            xl.Selection.Value = u'Трансформатор: ' + '123'
            ws.Range('A3:M3').Select()
            xl.Selection.Merge()
         #   print 'series', series
            
            
            if ordernumber == None:
                #QMessageBox.warning(None, u"Предупреждение",  's13321', QMessageBox.Ok)
                xl.Selection.Value = u'Серия: ' + str(series)
            else:    
                #QMessageBox.warning(None, u"Предупреждение",  's13322', QMessageBox.Ok)
                xl.Selection.Value = u'Серия: ' + str(series) + u'    Заказ: ' + str(ordernumber)
                #xl.Selection.Value = u'Серия: ' + series + u'    Заказ: ' + ordernumber
            #QMessageBox.warning(None, u"Предупреждение",  's1333', QMessageBox.Ok)
            #17.05.2017
            ws.Range("A4:N5").Select()
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.HorizontalAlignment = 3
            
#    With Selection
#        .HorizontalAlignment = xlCenter
#        .VerticalAlignment = xlCenter
#        .WrapText = True
#    Rows("5:5").RowHeight = 27.75            
            
            xl.Selection.VerticalAlignment = 2
                        
            xl.Selection.WrapText = True
            
            ws.Range("A5:N5").Select()
            xl.Selection.RowHeight *= 3
            

            ws.Range("A4:A5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Зав.\n№'
            
            ws.Range("B4:B5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'№ обмот.'
            
            ws.Range("C4:E4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Сопротивление'
            ws.Range("C5:C5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Величина'
            ws.Range("D5:E5").Select()
            xl.Selection.Merge()
#            xl.Selection.Value = u'Коридор (' + str(Devices.data['accuracy']['r']) + '%)' 
            xl.Selection.Value = u'Коридор (' + str(_accuracyR) + '%)' 

            ws.Range("F4:H4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Ток намагничивания'
            ws.Range("F5:F5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Величина'
            ws.Range("G5:H5").Select()
            xl.Selection.Merge()
#            xl.Selection.Value = u'Коридор (' + str(Devices.data['accuracy']['a']) + '%)'
            xl.Selection.Value = u'Коридор (' + str(_accuracyI) + '%)'
            
            
            #23.05.2017            
            ws.Range("I4:I5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Напряж. намагни-чивания'
            
            ws.Range("J4:J5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Напряж. при номи-нальном токе'
            
            ws.Range("K4:L4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Коэфф. безопас'
            
            ws.Range("K5:K5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Расчет-ный'
            
            ws.Range("L5:L5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заданный'
                        
            ws.Range("M4:M5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Дата поверки'
            ws.Range("N4:N5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Код тележки'
                        
                        
            '''                        
            ws.Range("I4:I5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Ном. напряж'
            
            ws.Range("J4:K4").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Коэфф. безопас'
            
            ws.Range("J5:J5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Расч-ый'
            
            ws.Range("K5:K5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заданный'
                        
            ws.Range("L4:L5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Дата поверки'
            ws.Range("M4:M5").Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Код тележки'
            '''                                                            
                        
            M = []
            k = 0

            
            for i in range(len(globalReport)):
                #20.04
                '''
                if globalReport[i][1] == int(series):
                    M += [globalReport[i][2:]]
                '''
#11.11.16   ошивка преобразования       if globalReport[i][1] == int(series):
          #      print globalReport[i][1], series
                
#                if unicode(globalReport[i][1]) == unicode(series):
                if globalReport[i][1] == series:
                    # print ordernumber, globalReport[i][2]
                    if ordernumber == None or (ordernumber != None and globalReport[i][2] == ordernumber):
                        #17.05.2017
                        #if not LastTest or (LastTest and globalReport[i][17] != 0):
                        if not LastTest or (LastTest and globalReport[i][18] != 0):
                            #17.05.2017
                            #M += [globalReport[i][3:]]
                            
                            #R = [globalReport[i][3:17]]
                            R = [globalReport[i][3:]]
                            # print 'R1=', R
                            #R[5:7] = globalReport[i][18:20]
                            
                            if globalReport[i][20] != None or globalReport[i][21] != None:
                                R[0][5] = globalReport[i][19]
                                R[0][6] = globalReport[i][20]
                                R[0][7] = globalReport[i][21]
                                R[0][8] = globalReport[i][22]
                                #19.05.2017
                                #R[0][9] = globalReport[i][23]
                            # print 'R2=', R
                            M += R
#            self.globalReport += [[checking_2, series, ordernumber, serialnumber, coilname, round(r, 3),
# min_r, max_r, round(inom, 2), min_in, max_in, round(un, 2), round(un_, 2), round(k, 2), rating,
# createdatetime, idMap, idClass, id4, round(inom2, 2), min_in2, max_in2, round(sun2, 2), round(un2, 2)]]
                            
            # print 'M=', M
            #17.05.2017
            #ws.Range("A" + str(6) + ":M" + str(5 + len(M))).Select()
            ws.Range("A" + str(6) + ":N" + str(5 + len(M))).Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
            xl.Selection.Value = M
                        
            ws.Range("E" + str(6) + ":E" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0
            ws.Range("H" + str(6) + ":H" + str(5 + len(M))).Select()
            xl.Selection.Borders(7).LineStyle = 0

            #17.05.2017
            ws.Range("J" + str(6) + ":J" + str(5 + len(M))).Select()
            ###xl.Selection.Borders(7).LineStyle = 0
                        
            for i in range(len(M)):
                # Подкраска ячеек, не входящих в коридор
                if M[i][2] < M[i][3] or M[i][2] > M[i][4]:
                    xl.ActiveSheet.Cells(i + 6, 3).Interior.Color = 255            
                if M[i][5] < M[i][6] or M[i][5] > M[i][7]:
                    xl.ActiveSheet.Cells(i + 6, 6).Interior.Color = 255
                     
            #17.05.2017
                if M[i][14] == 1:
                    if M[i][10] > M[i][11]:
                        xl.ActiveSheet.Cells(i + 6, 11).Interior.Color = 255 
                if M[i][14] == 2:
                    if M[i][10] < M[i][11]:
                        xl.ActiveSheet.Cells(i + 6, 11).Interior.Color = 255 
                '''    
                if M[i][13] == 1:
                    if M[i][9] > M[i][10]:
                        xl.ActiveSheet.Cells(i + 6, 10).Interior.Color = 255 
                if M[i][13] == 2:
                    if M[i][9] < M[i][10]:
                        xl.ActiveSheet.Cells(i + 6, 10).Interior.Color = 255 
                '''
                            
                # Группировка колонок
                if i != len(M) - 1:
                    if M[i][1] == M[i + 1][1]:
                        xl.ActiveSheet.Cells(i + 7, 2).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 2).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 2).Borders(3).LineStyle = 0
                        if i != len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 2).Borders(4).LineStyle = 0
                    if M[i][8] == M[i + 1][8]:
                        xl.ActiveSheet.Cells(i + 7, 9).Value = ''                        
                        xl.ActiveSheet.Cells(i + 6, 9).Borders(4).LineStyle = 0
                        xl.ActiveSheet.Cells(i + 7, 9).Borders(3).LineStyle = 0
                        #4.02
                        #xl.ActiveSheet.Cells(i + 7, 10).Value = ''                        
                        #xl.ActiveSheet.Cells(i + 6, 10).Borders(4).LineStyle = 0
                        #xl.ActiveSheet.Cells(i + 7, 10).Borders(3).LineStyle = 0
                        if i != len(M) - 2:
                            xl.ActiveSheet.Cells(i + 7, 9).Borders(4).LineStyle = 0
                            #xl.ActiveSheet.Cells(i + 7, 10).Borders(4).LineStyle = 0
                        
        except:
            print("Неопознанная ошибка3 ... ")
                       
        return


def BAX_coil1(fullname, serialnumbel, zakaz, coilsInfa, code):
        try:  
            try:
                xl = Dispatch('Excel.Application')
            except:
                print ("Не запускается Excel")
                return    
                     
                      
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            
            ws.Name = u'ВАХ'
            
            ws.Range('A1:I2').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Электротехническая лаборатория ООО "Электрощит -К°"\nРоссия, 249210, Калужская обл., п. Бабынино, ул. Советская, 24 тел. +7 495 0110 500'
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1
                        
            ws.Range('A4:I4').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            if code == 3:
                xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток (цех)'
            if code == 4:
                xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток (лаборатория)'
            
            ws.Range('A6:B6').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Объект испытаний:'
            ws.Range('C6:I6').Select()
            xl.Selection.Merge()
            xl.Selection.Value = fullname
            
            ws.Range('A7:B7').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заводской номер:'
            ws.Range('C7').Select()
            xl.Selection.Merge()
            xl.Selection.Value = serialnumbel
            
            ws.Range('A8:B8').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заказ:'
            ws.Range('C8').Select()
            xl.Selection.Merge()
            xl.Selection.Value = zakaz
            
#            nr = 7
            nr = 10
            for i in range(len(coilsInfa)):
                ws.Range('A' + str(nr) + ':' + 'B' + str(nr)).Select()
                xl.Selection.Merge()
                xl.Selection.Value = u'Катушка:'
                                
                ws.Range('C' + str(nr)).Select()
                xl.Selection.Merge()
                xl.Selection.Value = coilsInfa[i]['coil']

#                ws.Range('D' + str(nr) + ':' + 'H' + str(nr)).Select()

                nrgr = nr    #Положение графика
                ws.Range('D' + str(nrgr) + ':' + 'I' + str(nr)).Select()
                xl.Selection.Merge()
                
                #24.10.17
                
                bnd = bend(coilsInfa[i]['points'])

                ''' 
                points1 =        [[1.000,    0.0522],         
                [1.938,    0.0707],
                [3.126,    0.0927],
                [5.044,    0.1231],
                [8.139,    0.1656],
                [13.13,    0.2248],
                [21.18,    0.3096],
                [34.16,    0.4309],
                [40.57,    0.5293],
                [48.81,    0.6057],
                [58.81,    0.6938],
                [71.10,    0.7978],
                [85.15,    0.9110],
                [102.6,    1.046],
                [126.9,    1.221],
                [180.1,    1.558],
                [272.2,    2.084],
                [406.3,    2.801],
                [514.0,    3.397],
                [616.3,    4.012],
                [697.5,    4.560],
                [762.2,    5.078],
                [813.6,    5.591],
                [854.1,    6.111],
                [885.7,    6.654],
        [910.5,    7.249],
        [930.2,    7.912],
        [968.9,    10.35],
        [995.3,    14.31],
        [1015,    20.86],
        [1031,    32.62],
        [1047,    52.26],
        [1063,    85.07],
        [1079,    140.9],
        [1095,    225.2],
        [1108,    348.3],
        [1119,    529.8],
        [1136,    955.5],
        [1162,    1703]]
                points = []
                for k in range(len(points1)):
                    points += [[points1[k][1],points1[k][0]]]
                 
                points = [[0.013,3.368],
[0.016,    4.097],
[0.018,    4.8],
[0.021,    5.518],
[0.063,    6.216],
[1.198,    6.657],
[2.238,    6.96],
[3.016,    7.219],
[3.76,    7.457],
[4.458,    7.679],
[5.133,    7.85],
[5.9,    8.067],
[6.516,    8.206]]


'''





                bnd5 = bend5(coilsInfa[i]['points'])
                
                
                
                            
                
                
                # if bnd5 == None:
                #     print('NoneNoneNoneNoneNoneNoneNoneNoneNone')
                # else:
                #     print(bnd5[0], bnd5[1])


                #ВРЕМЕННО  
#                print coilsInfa[i]['points']  
                coilsInfa[i]['points'].insert(bnd5[0], bnd5[1])  
#                print coilsInfa[i]['points']  
                #coilsInfa[i]['points'] += bnd4  
                bnd = bend(coilsInfa[i]['points'])


                
                if bnd5 == None:                
                    xl.Selection.Value = u'Нет точки перегиба'
                else:    
#                    xl.Selection.Value = u'Точка перегиба: ' + str(round(coilsInfa[i]['points'][bnd][0],3)) + 'A   ' + str(round(coilsInfa[i]['points'][bnd][1],3)) + u'V (п.3.4.215   ГОСТ Р МЭК 61869-2-2015)'
                    xl.Selection.Value = u'Точка перегиба:'
                    
                    nrgr += 1
                    ws.Range('D' + str(nrgr) + ':' + 'I' + str(nrgr)).Select()
                    xl.Selection.Merge()
                    xl.Selection.Value = str(round(bnd5[1][0],3)) + 'A   ' + str(round(bnd5[1][1],3)) + u'V  (п.3.4.215  ГОСТ Р МЭК 61869-2-2015)'
                    
                #24.10.17
                
                                
                nr += 1
                nrgr += 1
                
                ws.Cells(nr, 1).Value = "A"
                ws.Cells(nr, 2).Value = "V"
                ws.Range('A' + str(nr) + ':' + 'B' + str(nr)).Select()
                xl.Selection.HorizontalAlignment  = 3            
                xl.Selection.Borders(1).LineStyle = 1
                xl.Selection.Borders(2).LineStyle = 1
                xl.Selection.Borders(3).LineStyle = 1
                xl.Selection.Borders(4).LineStyle = 1
                                
                  
                countPoints = len(coilsInfa[i]['points'])
                # Расчет расположения графика
                left   = int(5.625 * (ws.Columns(1).ColumnWidth + ws.Columns(2).ColumnWidth) + 10)  
                top    = int((nrgr - 1) * ws.Rows(nrgr).RowHeight)
                width  = 320
                height = 15 * ws.Rows(nrgr).RowHeight
                for j in range(countPoints):
                    nr += 1
                    ws.Cells(nr, 1).Value = round(coilsInfa[i]['points'][j][0],3)
                    ws.Cells(nr, 2).Value = round(coilsInfa[i]['points'][j][1],3)
                    ws.Range('A' + str(nr) + ':' + 'B' + str(nr)).Select()
                    xl.Selection.HorizontalAlignment  = 3            
                    xl.Selection.Borders(1).LineStyle = 1
                    xl.Selection.Borders(2).LineStyle = 1
                    xl.Selection.Borders(3).LineStyle = 1
                    xl.Selection.Borders(4).LineStyle = 1
                    '''
                    if bnd != None and (bnd == j or bnd + 1 == j):
                        xl.Selection.Interior.Color = 255            
                    '''
                    
                    if bnd5 != None and bnd5[0] == j:
                        xl.Selection.Interior.Color = 255            
                chart = ws.ChartObjects().Add(left, top, width, height) 
                chart.Chart.ChartType = 72
                series = chart.Chart.SeriesCollection()
                ns = series.NewSeries()
                ns.XValues = ws.Range('A' + str(nr - len(coilsInfa[i]['points']) + 1) + ':A' + str(nr))
                ns.Values  = ws.Range('B' + str(nr - len(coilsInfa[i]['points']) + 1) + ':B' + str(nr))
                ns.Name = u""
                
                #series.Points(4).MarkerStyle = -4168
#                print 'series.Points=',len(series.points)
#                print 'series.Points=',series
#                print 'series.Points=',len(ns.Points())
#                # print 'series.Points=',ns.Values
#                 print 'ns=',ns
#                 try:
                #     print 'ns1=',ns.Points
                # except:
                #     print "ошибка1 ... "
                # try:
                #     print 'ns2=',ns.XValues
                # except:
                #     print "ошибка2 ... "
                # try:
                #     print 'ns3=',ns.Points[4]
                # except:
                #     print "ошибка3 ... "
                # try:
                #     print 'ns4=',ns.points
                # except:
                #     print "ошибка4 ... "
                #
                #
                # print 'end'
                
                '''                
                chart.Chart.Axes(1).HasTitle = True
                chart.Chart.Axes(1).AxisTitle.Caption = u"Сила тока A"
                chart.Chart.Axes(2).HasTitle = True
                chart.Chart.Axes(2).AxisTitle.Caption = u"Напряжение V"
                '''   
                chart.Chart.HasTitle = False
                chart.Chart.HasLegend = False


               # chart.Chart.SeriesCollection(1).Select
               # chart.Chart.SeriesCollection(1).Points(4).Select

                '''
    ActiveSheet.ChartObjects("Äèàãðàììà 1").Activate
    ActiveChart.SeriesCollection(1).Select
    ActiveChart.SeriesCollection(1).Points(9).Select
    With Selection
        .MarkerStyle = 2
        .MarkerSize = 7
    End With
    Selection.MarkerStyle = -4168
    Selection.MarkerSize = 8
    Selection.MarkerSize = 9
    Range("L18").Select
End Sub
'''


                   
#                if countPoints < 15:
#                    nr += 14 - countPoints 
        
                                                                
                if countPoints < 17:
                    nr += 16 - countPoints 
                                                                
                nr += 2



            ws.Cells(nr, 1).Value = u'Испытатель: ____________________'; 
            '''
            ws.Range('A4:I4').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты проверки тока намагничивания вторичных обмоток'
            '''            
        except:
            print("Неопознанная ошибка4 ... ")




# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает на 50%
def bend5(points):

    if len(points) < 3:
        return None
   #k2 = None

    circls = []      
    for i in range(len(points) - 2):

        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x3 = points[i+2][0]
        y3 = points[i+2][1]
        
        if x1 >= x3 or y1 >= y3:
            circls += [None]
            continue
        y = ((y1 - y3) * x2 + x1 * y3 - x3 * y1) / (x1 - x3)
        # print 'y=', y
        # print 'y2=', y2
        if y >= y2:
            circls += [None]
            continue
                
        circ = calcCircle(x1, y1, x2, y2, x3, y3)        
       # print 'circ=', circ
        if circ == None:
            circls += [None]
            continue
        
        x0 = circ[0]
        y0 = circ[1]
        r  = circ[2]
        
        '''
        #11.12.17        
        if y1 < y0:
            circls += [None]
            continue
        #11.12.17
        '''
        
        circls += [[x0, y0, r]]
    circls += [None]
    # print
    # print
    # print
    #
    # print 'circls=', circls
    
    dx = (points[len(points) - 1][0] - points[0][0]) / 10000.
    x = points[0][0]
    while x < points[len(points) - 1][0]:
        for i in range(len(points) - 1):
            if x >= points[i][0] and x <= points[i+1][0]:       
                if circls[i] == None:
                    x1 = points[i][0]
                    y1 = points[i][1]
                    x2 = points[i+1][0]
                    y2 = points[i+1][1]
                    y = ((y1 - y2) * x + x1 * y2 - x2 * y1) / (x1 - x2)
                else:
                    x0 = circls[i][0]
                    y0 = circls[i][1]
                    r  = circls[i][2]
                    y = (r**2 - (x - x0)**2)**0.5 + y0
                    pass
                break
#        print 'i1, x, y=', i, x, y
        i1 = i
        xp = 1.5 * x
        #yp = 1.1 * y
        for i in range(len(points) - 1):
            if xp >= points[i][0] and xp <= points[i+1][0]:       
                if circls[i] == None:
                    x1 = points[i][0]
                    y1 = points[i][1]
                    x2 = points[i+1][0]
                    y2 = points[i+1][1]
                    yp = ((y1 - y2) * xp + x1 * y2 - x2 * y1) / (x1 - x2)
                else:
                    x0 = circls[i][0]
                    y0 = circls[i][1]
                    r  = circls[i][2]
                    yp = (r**2 - (xp - x0)**2)**0.5 + y0
                    pass
                break
        if yp <= 1.1 * y:
            # print 'i2, x, y=', i, x, y
            return [i1+1, [x, y]]     
        x += dx
    return None




  
    return circls
              
              
              
    points1 = []
    for i in range(len(points) - 1):
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x = (x1 + x2) / 2
        x0 = circls[i][0]
        y0 = circls[i][1]
        r  = circls[i][2]
        
        if x0 > (x1 + x2) / 2 and y0 < (y1 + y2) / 2:
            y = (r**2 - (x - x0)**2)**0.5 + y0
        else:   
            y = (r**2 - (x - x0)**2)**0.5 + y0
#            y = (y1 + y2) / 2
        points1 += [[x,y]]

    return points1


    '''
        x = x1
        dx = (x3 - x1) / 10        
        for j in range(10):
            print 'j=', j
            print 'circl=', x0, y0, r, r**2 - (x - x0)**2
            y = (r**2 - (x - x0)**2)**0.5 + y0
            print 'x=', x, 'y=', y
            k = math.fabs(y*(y - y0)/(x*(x - x0)))
            print 'k=', k
            x += dx
'''
        
        
        
    return None    





# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает на 50%
def bend4(points):
    if len(points) < 3:
        return None
   #k2 = None

    circls = []      
    for i in range(len(points) - 2):
    #     print
    #     print 'i=', i
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x3 = points[i+2][0]
        y3 = points[i+2][1]
        circ = calcCircle(x1, y1, x2, y2, x3, y3)
        # print 'circ=', circ
        if circ == None:
            continue
        x0 = circ[0]
        y0 = circ[1]
        r  = circ[2]

        if i == 0:
            circls += [[x0, y0, r]]
        else:
            
            if x0 <= (x1 + x2) / 2 or y0 <= (y1 + y2) / 2: #яма
                circls += [[x01, y01, r1]]
            elif x01 <= (x1 + x2) / 2 or y01 <= (y1 + y2) / 2:  #яма
                circls += [[x0, y0, r]]
            else:  # кочки          
                x02 = (x0 + x01) / 2
                y02 = (y0 + y01) / 2
                cc = (x0 - x01)**2 + (y0 - y01)**2 
                # медиана
                r2 = (2*r**2 + 2*r1**2 - cc)**0.5 / 2            
                circls += [[x02, y02, r2]]
        x01 = x0    
        y01 = y0    
        r1  = r    
    circls += [[x0, y0, r]]

    
              
    points1 = []
    for i in range(len(points) - 1):
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x = (x1 + x2) / 2
        x0 = circls[i][0]
        y0 = circls[i][1]
        r  = circls[i][2]
        
        if x0 > (x1 + x2) / 2 and y0 < (y1 + y2) / 2:
            y = (r**2 - (x - x0)**2)**0.5 + y0
        else:   
            y = (r**2 - (x - x0)**2)**0.5 + y0
#            y = (y1 + y2) / 2
        points1 += [[x,y]]

    return points1


    '''
        x = x1
        dx = (x3 - x1) / 10        
        for j in range(10):
            print 'j=', j
            print 'circl=', x0, y0, r, r**2 - (x - x0)**2
            y = (r**2 - (x - x0)**2)**0.5 + y0
            print 'x=', x, 'y=', y
            k = math.fabs(y*(y - y0)/(x*(x - x0)))
            print 'k=', k
            x += dx
'''
        
        
        
    return None    



# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает на 50%
def bend3(points):
    if len(points) < 3:
        return None
   #k2 = None

    for i in range(len(points) - 2):

        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x3 = points[i+2][0]
        y3 = points[i+2][1]
        circ = calcCircle(x1, y1, x2, y2, x3, y3)
        if circ == None:
            continue
        x0 = circ[0]
        y0 = circ[1]
        r  = circ[2]

        x = x1
        dx = (x3 - x1) / 10        
        for j in range(10):
            # print 'j=', j
            # print 'circl=', x0, y0, r, r**2 - (x - x0)**2
            y = (r**2 - (x - x0)**2)**0.5 + y0
            # print 'x=', x, 'y=', y
            k = math.fabs(y*(y - y0)/(x*(x - x0)))
            # print 'k=', k
            x += dx

        
        
        
    return None    




# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает на 50%
def bend2(points):
    if len(points) < 3:
        return None
   #k2 = None
    # print '------------------'
    for i in range(len(points) - 2):        
        # print 'i=', i
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        x3 = points[i+2][0]
        y3 = points[i+2][1]
        circ = calcCircle(x1, y1, x2, y2, x3, y3)
        if circ == None:
            continue
        x0 = circ[0]
        y0 = circ[1]
        r  = circ[2]

        x = (x1 + x3) / 2
        for j in range(10):
            # print 'j=', j
            # print 'circl=', x0, y0, r, r**2 - (x - x0)**2
            dx = (x3 - x1) / (2**(j+2))
            # print x3, x1, x3-x1, 2**(j+2)
            # print 'x=', x
            # print 'dx=', dx
            y = (r**2 - (x - x0)**2)**0.5 + y0
            # print 'y=', y
###            k = (x0 - x) / (y - y0)
###            k = (y - y0) / (x0 - x)
            k = math.fabs(y*(y - y0)/(x*(x - x0)))
            # print 'k=', k
            
            if k < 5:
                x += dx
            else:
                x -= dx     

        
        
        
    return None    



# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает на 50%
def bend1(points):
    if len(points) < 3:
        return None
    k2 = None

    for i in range(len(points) - 1):
        k1 = k2
        a1 = points[i][0]
        a2 = points[i+1][0]
        v1 = points[i][1]
        v2 = points[i+1][1]
#        print 'a1,a2,v1,v2=', a1,a2,v1,v2
        percA = 100. * a2 / a1 - 100.
        percV = 100. * v2 / v1 - 100.
#        print 'percA=', percA,'percV=', percV
        k2 = percA / percV
#        print 'k1=', k1, 'k2=', k2
        if i == 0:
            continue
        
        if k1 >= k2:
            continue
        
        if k1 >= 5 or (k1 < 5 and k2 >= 5) or (i == len(points) - 1 and k2 < 5):
 #           print 'points[i-1][0], points[i-1][1], points[i][0], points[i][1], points[i+1][0], points[i+1][1]=',points[i-1][0], points[i-1][1], points[i][0], points[i][1], points[i+1][0], points[i+1][1]
            circ = calcCircle(points[i-1][0], points[i-1][1], points[i][0], points[i][1], points[i+1][0], points[i+1][1])
            if circ == None:
                return circ
            else:    
 #               print 'x=', circ[0], 'y=', circ[1], 'r=', circ[2]
                x = circ[0]
                y = circ[1]
                r = circ[2]
                
                Ang = math.pi / 4.
                for j in range(100):
                    pass
                    x_ = x - r * math.cos(Ang)   
                    y_ = y + r * math.sin(Ang)   
                    k = (y_ / x_) * math.tan(Ang)
#                    print 'k=', k
                    dAng = math.pi / (2**(j+3))
                    if k < 5:
                        Ang += dAng
                    else:    
                        Ang -= dAng
#                    print 'Ang=', Ang                                    
                        
#                print 'FINISH_Ang=', Ang                                    
                #x_= x - r / (26.**0.5)
                #y_= y + 5 * r / (26.**0.5)
                return (x_, y_)            
    return None    


def calcCircle(x1, y1, x2, y2, x3, y3):
    # Расчет окружности по трем точкам
    # Возвращает список состоящий из координат центра и радиуса
    try:
        a1 = 2 * (x1 - x2)
        b1 = 2 * (y1 - y2)
        c1 = x2**2. - x1**2. + y2**2. - y1**2.
        a2 = 2 * (x1 - x3)
        b2 = 2 * (y1 - y3)
        c2 = x3**2. - x1**2. + y3**2. - y1**2.
    
        x = (c2 * b1 - c1 * b2) / (a1 * b2 - a2 * b1)
        y = -(a1 * x + c1) / b1
        r = ((x - x1)**2. + (y - y1)**2.)**0.5
    except Exception:
        return None
    
    return (x, y, r)


# Вычисление точки перегиба
# при увеличении напряжения на 10% ток возрастает не более чем на 50%
# Сделано как описал Эрман
def bend(points):
    if len(points) < 3:
        return None
    bend1 = False
#    print '------------------'        
#    print points
    for i in range(len(points) - 1):
#        print 1
        a1 = points[i][0]
#        print 2
        a2 = points[i+1][0]
#        print 3
        v1 = points[i][1]
#        print 4
        v2 = points[i+1][1]
#        print 'a1,a2,v1,v2=', a1,a2,v1,v2
        percA = 100. * a2 / a1 - 100.
        percV = 100. * v2 / v1 - 100.
#        print 'percA, percV', round(percA, 3), round(percV, 3)
        bend2 = 5. * percV > percA
#        print 'q'
        if bend1 and not bend2:
#            print 'w'
#            return i - 1
            return i
#        print 'e', bend1, bend2
        bend1 = bend2
#    print 'r'
    return None    


    
#[[0.0598877519, 69.0289764404], [0.0835682154, 72.1728897095], [0.1829987913, 75.6985855103], [0.8334326744, 78.7585983276], [2.1251420975, 81.6595916748], [3.317841053, 83.6814880371], [4.5072016716, 86.2388000488], [5.8213949204, 87.9272766113]]
#[[0.0545752719, 198.329177856], [0.061714869, 204.407821655], [0.0732016861, 210.863189697], [0.1124484763, 217.264755249], [0.202557981, 223.535339355], [0.6093477011, 230.051864624], [2.0126786232, 236.107772827], [3.8174512386, 241.373641968], [4.06372118, 241.161254883], [4.0721650124, 240.692306519]]
#[[0.0522071049, 204.330688477], [0.0562394001, 229.16595459], [1.0379185677, 250.772232056], [2.802942276, 269.381103516], [4.8157720566, 284.326843262], [6.3285541534, 290.862915039]]

#def BAX_coil2(fullname, serialnumbel, zakaz, coilsInfa):
def BAX_coil2(charts):
        try:  
            try:
                xl = Dispatch('Excel.Application')
            except:
                print("Не запускается Excel")
                QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel", QMessageBox.Ok)
                #QMessageBox.warning(self, u"Предупреждение", u"Не запускается Excel", QMessageBox.Ok)
                return                         
                      
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            
            ws.Name = u'ВАХ'
                        


            '''
            ws.Range('A1:I1').Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Merge()
            xl.Selection.Value = u'Результаты поверки тока намагничивания вторичных обмоток'
            
            ws.Range('A3:B3').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Объект испытаний:'
            ws.Range('C3:I3').Select()
            xl.Selection.Merge()
            xl.Selection.Value = unicode(fullname)
            
            ws.Range('A4:B4').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заводской номер:'
            ws.Range('C4').Select()
            xl.Selection.Merge()
            xl.Selection.Value = unicode(serialnumbel)
            
            ws.Range('A5:B5').Select()
            xl.Selection.Merge()
            xl.Selection.Value = u'Заказ:'
            ws.Range('C5').Select()
            xl.Selection.Merge()
            xl.Selection.Value = unicode(zakaz)
            '''
   
                # Расчет расположения графика
            left   = 50  
            top    = 50
            width  = 850
            height = 550

            chart = ws.ChartObjects().Add(left, top, width, height) 
            chart.Chart.ChartType = 72                
            chart.Chart.Axes(1).HasTitle = True
            chart.Chart.Axes(1).AxisTitle.Caption = u"Сила тока A"
            chart.Chart.Axes(2).HasTitle = True
            chart.Chart.Axes(2).AxisTitle.Caption = u"Напряжение V"                
            chart.Chart.HasTitle = True
            chart.Chart.HasLegend = True

                
            nc = 1
            for i in range(len(charts)):
#            for i in range(3):
                nr = 1

                ws.Range(ws.Cells(nr, nc), ws.Cells(nr, nc+1)).Select()                
                xl.Selection.Merge()
###                xl.Selection.Value = u'Катушка:'
                xl.Selection.Value = charts[i][0]
###                ws.Range('C' + str(nr)).Select()
###                ws.Range('C' + str(nr)).Select()
###                xl.Selection.Merge()
                #xl.Selection.Value = coilsInfa[i]['coil']
                
                nr += 1
                ws.Cells(nr, nc).Value = "A"
                ws.Cells(nr, nc+1).Value = "V"
                ws.Range(ws.Cells(nr, nc), ws.Cells(nr, nc+1)).Select()
                xl.Selection.HorizontalAlignment  = 3            
                xl.Selection.Borders(1).LineStyle = 1
                xl.Selection.Borders(2).LineStyle = 1
                xl.Selection.Borders(3).LineStyle = 1
                xl.Selection.Borders(4).LineStyle = 1
                                

#                countPoints = len(coilsInfa[i]['points'])
                countPoints = len(charts[i][1])
                # Расчет расположения графика
###                left   = int(5.625 * (ws.Columns(1).ColumnWidth + ws.Columns(2).ColumnWidth) + 10)  
###                top    = int((nr - 1) * ws.Rows(nr).RowHeight)
###                width  = 320
###                height = 15 * ws.Rows(nr).RowHeight

                for j in range(countPoints):
                    nr += 1
                    #ws.Cells(nr, 1).Value = round(coilsInfa[i]['points'][j][0],3)
                    #ws.Cells(nr, 2).Value = round(coilsInfa[i]['points'][j][1],3)
                    ws.Cells(nr, nc).Value = round(charts[i][1][j][0],3)
                    ws.Cells(nr, nc+1).Value = round(charts[i][1][j][1],3)
                    ws.Range(ws.Cells(nr, nc), ws.Cells(nr, nc+1)).Select()
                    
                    xl.Selection.HorizontalAlignment  = 3            
                    xl.Selection.Borders(1).LineStyle = 1
                    xl.Selection.Borders(2).LineStyle = 1
                    xl.Selection.Borders(3).LineStyle = 1
                    xl.Selection.Borders(4).LineStyle = 1

#                continue
                ''' 
                chart = ws.ChartObjects().Add(left, top, width, height) 
                chart.Chart.ChartType = 72
                '''
                series = chart.Chart.SeriesCollection()
                ns = series.NewSeries()
                ns.XValues = ws.Range(ws.Cells(nr - len(charts[i][1]) + 1, nc), ws.Cells(nr, nc))
                ns.Values  = ws.Range(ws.Cells(nr - len(charts[i][1]) + 1, nc+1), ws.Cells(nr, nc+1))
#                ns.Name = u""
                ns.Name = charts[i][0]
                '''
                chart.Chart.Axes(1).HasTitle = True
                chart.Chart.Axes(1).AxisTitle.Caption = u"Сила тока A"
                chart.Chart.Axes(2).HasTitle = True
                chart.Chart.Axes(2).AxisTitle.Caption = u"Напряжение V"
                
                chart.Chart.HasTitle = False
                chart.Chart.HasLegend = False
                   
                if countPoints < 15:
                    nr += 14 - countPoints 
                '''
                                                                
###                nr += 2
                nc += 3
                        
        except:
            print("Неопознанная ошибка41 ... ")





def repMoveTask(zakaz, series, spisok):
        try:  
            try:
                xl = Dispatch('Excel.Application')
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
            xl.Selection.Value = u'Дата ' + str(datetime.date.today().day) + '.' + str(datetime.date.today().month) + '.' + str(datetime.date.today().year)

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
            xl.Selection.Value = u'Проверка\nвторичных\nобмоток'
            ws.Range('C' + str(nr)).Select()
            xl.Selection.Value = u'Проверка тока\nнамагничивания\nв цеху'
            ws.Range('D' + str(nr)).Select()
            xl.Selection.Value = u'Проверка\nактивных\nчастей'
            ws.Range('E' + str(nr)).Select()
            xl.Selection.Value = u'Высоковольтные\nиспытания'
            ws.Range('F' + str(nr)).Select()
            xl.Selection.Value = u'Проверка тока\nнамагничивания\nв ЭТЛ'
            ws.Range('G' + str(nr)).Select()
            xl.Selection.Value = u'Поверка\nв ЭТЛ'

            ws.Range('A' + str(nr) + ':G' + str(nr + len(spisok))).Select()
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
                #print 'spisok[i][0] = ', spisok[i][0]
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
                    #print 'spisok[i][3][j][2] = ', spisok[i][3][j][2]
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




# Отчет по браку
def repDefect(db, date1, date2, name_stand, id_defect, ordernumber, id_serial_number, sort):
    try:

            query = QSqlQuery(db)
            
            SQL = """                
select t1.createdatetime, t5.fullname as workplace, t3.fullname as transformer, t2.serialnumber, t2.makedate, t6.fullname as name_defect
from item t1, serial_number t2, transformer t3, test_map t4, stand t5, defect t6
--where t1.createdatetime between to_date('01.05.2021','dd.mm.yyyy') and to_date('01.06.2021','dd.mm.yyyy')
where t1.createdatetime between :DATE1 and :DATE2
and defect is not null
and t1.serial_number = t2.id
and t2.transformer = t3.id
and t1.test_map = t4.id
and t4.stand = t5.id
and t1.defect = t6.id
            """
            
            if name_stand != None:
                SQL += '''and t5.fullname = :NAME_STAND
'''                            
            if id_defect != None:
                SQL += '''and t1.defect = :ID_DEFECT
'''                            
            if ordernumber != None:
                SQL += '''and t2.ordernumber = :ORDERNUMBER
'''                            
            if id_serial_number != None:
                SQL += '''and t2.id = :ID_SERIAL_NUMBER
'''                            

            if sort == 1:
                SQL += '''order by t1.createdatetime
'''                

            if sort == 2:
                SQL += '''order by t5.fullname, t1.createdatetime
'''                            
            if sort == 3:
                SQL += '''order by t3.fullname, t1.createdatetime
'''                            
            if sort == 4:
                SQL += '''order by t2.makedate, t2.serialnumber, t1.createdatetime
'''                            
            if sort == 5:
                SQL += '''order by t6.fullname, t1.createdatetime
'''                            
                      

            query.prepare(SQL)
            query.bindValue(":DATE1", date1)

            query.bindValue(":DATE2", date2)

            if name_stand != None:
                query.bindValue(":NAME_STAND", name_stand)
            if id_defect != None:
                query.bindValue(":ID_DEFECT", id_defect)
            if ordernumber != None:
                query.bindValue(":ORDERNUMBER", ordernumber)
            if id_serial_number != None:
                query.bindValue(":ID_SERIAL_NUMBER", id_serial_number)            
            
            if not query.exec_():
                QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
                return
            else:    
                model.setQuery(query)

            if model.rowCount() < 1:
                QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
                return
            
            try:
                xl = Dispatch('Excel.Application')
            except:
                print ("Не запускается Excel")
                return
            
            xl.Visible = 1
            wb = xl.Workbooks.Add()
            ws = wb.Worksheets(1)            

            ws.PageSetup.Orientation = 2

            ws.PageSetup.TopMargin = 28
            ws.PageSetup.LeftMargin = 23
            ws.PageSetup.RightMargin = 23
            ws.PageSetup.BottomMargin = 42

            ws.Cells(1, 1).ColumnWidth = 10            
            ws.Cells(1, 2).ColumnWidth = 7            
            ws.Cells(1, 3).ColumnWidth = 30            
            ws.Cells(1, 4).ColumnWidth = 42            
            ws.Cells(1, 5).ColumnWidth = 12    
            ws.Cells(1, 6).ColumnWidth = 30                

            ws.Range('A1:G1').Select()
            xl.Selection.Font.Size = 16
            xl.Selection.Merge()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Value = u'ОТЧЕТ  О НЕСООТВЕТСТВУЮЩЕЙ ПРОДУКЦИИ'
            
            ws.Range('A2:G2').Select()
            xl.Selection.Font.Size = 12
            xl.Selection.Merge()
            xl.Selection.HorizontalAlignment = 3
            try:
                xl.Selection.Value = u'Период с ' + str(date1.toString("dd.MM.yyyy")) + u' по ' + str(date2.toString("dd.MM.yyyy"))
            except:
                pass
            
            nr = 3
            ws.Range('A' + str(nr) + ':G' + str(nr)).Select()
            xl.Selection.VerticalAlignment = 2
            xl.Selection.HorizontalAlignment = 3

            ws.Range('A' + str(nr)).Select()
            xl.Selection.Value = u'Дата'
            ws.Range('B' + str(nr)).Select()
            xl.Selection.Value = u'Время'
            ws.Range('C' + str(nr)).Select()
            xl.Selection.Value = u'Наименование\nрабочего места'
            ws.Range('D' + str(nr)).Select()
            xl.Selection.Value = u'Тип трансформатора'
            ws.Range('E' + str(nr)).Select()
            xl.Selection.Value = u'Зав. номер'
            ws.Range('F' + str(nr)).Select()
            xl.Selection.Value = u'Вид несоответствия'

            ws.Range('A' + str(nr) + ':F' + str(nr + 0)).Select()
            xl.Selection.VerticalAlignment = 1
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
            xl.Selection.Borders(3).LineStyle = 1
            xl.Selection.Borders(4).LineStyle = 1

            M = []

            for i in range(model.rowCount()):
                print(1144656 ,str(model.record(i).field('makedate').value()) , str((model.record(i).field('serialnumber').value())))
                R = [str(model.record(i).field('createdatetime').value().toString("dd.MM.yyyy")),
                     str(model.record(i).field('createdatetime').value().toString("hh:mm")),
                     model.record(i).field('workplace').value(),
                     model.record(i).field('transformer').value(),
                     f"{model.record(i).field('makedate').value()}-{model.record(i).field('serialnumber').value()}",
                     model.record(i).field('name_defect').value()]
                M += [R]
                


            ws.Range("A" + str(4) + ":B" + str(3 + len(M))).Select()
            xl.Selection.HorizontalAlignment = 3
            ws.Range("E" + str(4) + ":E" + str(3 + len(M))).Select()
            xl.Selection.HorizontalAlignment = 3
                
            ws.Range("A" + str(4) + ":F" + str(3 + len(M))).Select()
            xl.Selection.Font.Size = 10
            xl.Selection.WrapText = True
            xl.Selection.Borders(1).LineStyle = 1
            xl.Selection.Borders(2).LineStyle = 1
          #  xl.Selection.Borders(3).LineStyle = 1     # верх
            xl.Selection.Borders(4).LineStyle = 1     # низ
            
            
            # Удаление горизонтальных черточек
            '''
            n = model.rowCount()     
            for i in range(n):
                if i != n - 1:
                    if M[n-i-1][0] == M[n-i-2][0]:
                        M[n-i-1][0] = ''
                        ws.Range("A" + str(n - i + 2)).Select()
                        xl.Selection.Borders(4).LineStyle = 0      # низ
            '''            
                        
            ws.Range("A" + str(4) + ":F" + str(3 + len(M))).Select()
            xl.Selection.Value = M

            ws.Range('A' + str(4 + len(M))+ ':F' + str(4 + len(M))).Select()
            xl.Selection.Font.Size = 12
            xl.Selection.Merge()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.Value = u'ВСЕГО ' + str(len(M)) + u' шт.'
    except:
            print("Неопознанная ошибка7 ... ")







def verification_protocol(db, test_map, item, visibleExcel):
    # print 'test_map, item', test_map, item

    global name_msr_etalon
    global name_msr_vspom
    
    query = QSqlQuery(db)

    try:
        xl = Dispatch('Excel.Application')
    except:
        QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel", QMessageBox.Ok)
        return u"Не запускается Excel"            

    xl.Visible = visibleExcel
#    xl.Visible = False
    inputFile = os.getcwd() + u'\\rpt\\Протокол_поверки.xlsx'  # Шаблон
#    """
    try:
        # установить на шаблон read-only на время формирования отчета 
        os.chmod(inputFile, stat.S_IREAD)
    except:
        QMessageBox.warning(None, u"Предупреждение", u"Отсутствует шаблон: " + inputFile, QMessageBox.Ok)
        return
#        raise Exception(u"Отсутствует шаблон: " + inputFile)
#"""
    
    try:
        wb = xl.Workbooks.Open(inputFile)
        # print 'wb = ', wb
    except:
        QMessageBox.warning(None, u"Предупреждение", u"Не открывается файл: " + inputFile, QMessageBox.Ok)
        return

    ws = wb.Worksheets(1)        
    

    nrPogr  = 29

    strSQL = """                
select * from 
(
select row_number() OVER() as rn, *
FROM
(
select  tm.id as test_map, item.id as item,
   regexp_replace(regexp_replace(tsf.shortname, 'P\d+', 'P'), 'FS\d+', '')  as ShortName                                       
   , sn.transformer
   , sn.serialnumber
   , sn.makedate       
   , type_transformer.method    
   , tm.createdatetime            
   , climat.temperature
   , climat.humidity
--   , round(7.50 * climat.pressure, 0) as pressure              
   , round(climat.pressure, 0) as pressure              
   , tsf.id as tsfid            
   , item.id as itemid
   , oper.FIO as FIO                             
from
   test_map tm
left join climat on climat.id = tm.climat
inner join item on item.test_map = tm.id and item.defect is null
inner join serial_number sn on sn.id = item.serial_number
inner join transformer tsf on sn.transformer = tsf.id
left join type_transformer on tsf.type_transformer = type_transformer.id
inner join operator oper on oper.id = tm.supervisor                                  
--where makedate = 21
--and item.istested                                                        
where item.istested                                                        
order by
       item.id
) as t
) as t1
where test_map = """ + str(test_map)

    if item != None: 
        strSQL += """                
and item = """ + str(item)     

        strSQL += """                
order by item                                                                    
"""                

    # print strSQL
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания__", QMessageBox.Ok)
        return
    else:    
        model.setQuery(query)

    if model.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return

# Средства измерения эталонные
    strSQL = """                
select t1.id, t1.zav_msr, name_msr, zav_num, comment
--select *
from map_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and t1.test_map = """ + str(test_map) + """
and type = 1                   
order by name_msr
"""

#    print strSQL
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:    
        model_2.setQuery(query)

    name_msr_etalon = ''
    for i in range(model_2.rowCount()):
#        name_msr_etalon += unicode(model_2.record(i).field('name_msr').value().toString()) + u' №' + unicode(model_2.record(i).field('zav_msr').value().toString()) + '/'  
#24.01.2022        name_msr_etalon += unicode(model_2.record(i).field('name_msr').value().toString()) + u' №' + unicode(model_2.record(i).field('zav_num').value().toString()) + '/'  
        name_msr_etalon += model_2.record(i).field('comment').value().toString() + u' №' + model_2.record(i).field('zav_num').value().toString() + '/'

    name_msr_etalon = name_msr_etalon[0:len(name_msr_etalon) - 1]
# Средства измерения вспомогательные
    strSQL = """                
select t1.id, t1.zav_msr, name_msr, zav_num
--select *
from map_msr t1, zav_msr t2, msr t3
where t1.zav_msr = t2.id
and t2.id_msr = t3.id
and t1.test_map = """ + str(test_map) + """
and type = 2                   
order by name_msr
"""

#    print strSQL
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

    
    # Печать с рабочего места начальника
    if visibleExcel and item == None:
        ws.Range('A1:I33').Copy()
        A = ws.Columns('A:A').ColumnWidth 
        B = ws.Columns('B:B').ColumnWidth 
        C = ws.Columns('C:C').ColumnWidth 
        D = ws.Columns('D:D').ColumnWidth 
        E = ws.Columns('E:E').ColumnWidth 
        F = ws.Columns('F:F').ColumnWidth 
        G = ws.Columns('G:G').ColumnWidth 
        H = ws.Columns('H:H').ColumnWidth 
        I = ws.Columns('I:I').ColumnWidth
        
        LM = ws.PageSetup.LeftMargin
        RM = ws.PageSetup.RightMargin
        TM = ws.PageSetup.TopMargin
        BM = ws.PageSetup.BottomMargin
        
        
        '''
    With ActiveSheet.PageSetup
        .LeftHeader = ""
        .LeftMargin = Application.InchesToPoints(0.25)
        .RightMargin = Application.InchesToPoints(0.25)
        .TopMargin = Application.InchesToPoints(0.75)
        .BottomMargin = Application.InchesToPoints(0.75)
        '''
        
         
        for i in range(model.rowCount() - 1):
            wb.Worksheets.Add()
            ws = wb.Worksheets(1)        
            ws.Columns('A:A').ColumnWidth = A 
            ws.Columns('B:B').ColumnWidth = B 
            ws.Columns('C:C').ColumnWidth = C 
            ws.Columns('D:D').ColumnWidth = D 
            ws.Columns('E:E').ColumnWidth = E 
            ws.Columns('F:F').ColumnWidth = F 
            ws.Columns('G:G').ColumnWidth = G 
            ws.Columns('H:H').ColumnWidth = H 
            ws.Columns('I:I').ColumnWidth = I
            
            wb.ActiveSheet.Paste()
                    
            '''
            ws.PageSetup.LeftMargin = LM
            ws.PageSetup.RightMargin = RM
            ws.PageSetup.TopMargin = TM
            ws.PageSetup.BottomMargin = BM
'''
            

        for i in range(model.rowCount()):
            ws = wb.Worksheets(i+1)
            ws.Select()        
            ws.Name = model.record(i).field('serialnumber').value()
            ws.PageSetup.LeftMargin = LM
            ws.PageSetup.RightMargin = RM
            ws.PageSetup.TopMargin = TM
            ws.PageSetup.BottomMargin = BM
            sub_ver_prot(db, xl, wb, ws, test_map, int(model.record(i).field('item').value()), i)
    
        # Удаление лишних закладок
        nList = wb.Worksheets.count - model.rowCount() 
        for i in range(nList):
            ws = wb.Worksheets(model.rowCount() + 1)
            ws.Delete()        
    
        return
    

    # Печать с архива и тестирования
    for i in range(model.rowCount()):
        sub_ver_prot(db, xl, wb, ws, test_map, int(model.record(i).field('item').value()), i)
        
        if visibleExcel == False:
            xl.ActiveWindow.SelectedSheets.PrintOut()
            
        if i != model.rowCount() - 1:          
          for i in range(model_3.rowCount() - 1):
              ws.Rows(str(nrPogr)).EntireRow.Delete()

    if visibleExcel == False:
        wb.Close(SaveChanges=False)
        xl.Quit()



def sub_ver_prot(db, xl, wb, ws, test_map, item, nn):
    global name_msr_etalon
    global name_msr_vspom
    global decimal_point
    
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
   
    #Параметры    
    strSQL = """                
select * from params order by date_begin
"""                
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки Разрешения на допуск в эксплуатацию и регистрационного номера", QMessageBox.Ok)
    else:    
        model_2.setQuery(query)

    for i in range(model_2.rowCount()):
        if int(model_2.record(i).field('clsparams').value().toString()) == 1 and model_2.record(i).field('date_begin').value().toDate() <= model.record(nn).field('createdatetime').value().toDate():
            ws.Range('B5').Select()
            xl.Selection.Value = model_2.record(i).field('name').value().toString()
        if int(model_2.record(i).field('clsparams').value().toString()) == 2 and model_2.record(i).field('date_begin').value().toDate() <= model.record(nn).field('createdatetime').value().toDate():
            ws.Range('B6').Select()
            xl.Selection.Value = model_2.record(i).field('name').value().toString()


#    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toDate().toString("dd.MM.yyyy"))







    ws.Range('A7').Select()
    xl.Selection.Value = u'ПРОТОКОЛ ПОВЕРКИ № 20' + model.record(nn).field('makedate').value().toString() + '/' + model.record(nn).field('rn').value().toString() + u' ППТ'
    ws.Range('C8').Select()
    xl.Selection.Value = model.record(nn).field('ShortName').value().toString()
    ws.Range('B9').Select()
    xl.Selection.Value = model.record(nn).field('makedate').value().toString() + '-' + model.record(nn).field('serialnumber').value().toString()
    ws.Range('E9').Select()
#5.04.2022    xl.Selection.Value = '20' + unicode(model.record(nn).field('makedate').value().toString())
    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toDate().toString("yyyy"))
   
    #Класс точности    
    strSQL = """                
select classaccuracy from coil 
where transformer = """ + model.record(nn).field('transformer').value().toString() + """ 
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
        # print 'classaccuracy = ' + model_2.record(i).field('classaccuracy').value().toString()
        classaccuracy += model_2.record(i).field('classaccuracy').value().toString() + '/'

    classaccuracy = classaccuracy[0:len(classaccuracy) - 1]
        
#    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz        
    ws.Range('B10').Select()
    xl.Selection.Value = classaccuracy
    
    #Первичный ток    
    strSQL = """                
select distinct primarycurrent from coil 
where transformer = """ + model.record(nn).field('transformer').value().toString() + """ 
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
        primarycurrent += model_2.record(i).field('primarycurrent').value().toString() + ','
    primarycurrent = primarycurrent[0:len(primarycurrent) - 1]
    
#    QMessageBox.warning(None, u"Предупреждение", u"3", QMessageBox.Ok)
        
    #Вторичный ток    
    strSQL = """                
select distinct secondcurrent from coil 
where transformer = """ + model.record(nn).field('transformer').value().toString() + """ 
--order by coilnumber                  
"""                
    # print strSQL
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
#        print 'secondcurrent = ' + unicode(model_2.record(i).field('secondcurrent').value().toString())
        secondcurrent += umodel_2.record(i).field('secondcurrent').value().toString() + ','
    secondcurrent = secondcurrent[0:len(secondcurrent) - 1]
                        
#    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz        
    ws.Range('G10').Select()
    xl.Selection.Value = primarycurrent + '/' + secondcurrent
#'''

#    QMessageBox.warning(None, u"Предупреждение", u"4", QMessageBox.Ok)

#    QMessageBox.warning(None, u"Предупреждение111", name_msr_etalon, QMessageBox.Ok)

#    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz        
    ws.Range('E12').Select()
    xl.Selection.Value = name_msr_etalon
#'''

#    QMessageBox.warning(None, u"Предупреждение", u"5", QMessageBox.Ok)


#    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz        
    ws.Range('E13').Select()
    xl.Selection.Value = name_msr_vspom
    
    ws.Range('D15').Select()
    xl.Selection.Value = model.record(nn).field('temperature').value().toString()
    ws.Range('D16').Select()
    xl.Selection.Value = model.record(nn).field('humidity').value().toString()
    ws.Range('D17').Select()
    xl.Selection.Value = model.record(nn).field('pressure').value().toString()
    ws.Range('F18').Select()
    xl.Selection.Value = model.record(nn).field('method').value().toString()

    ws.Range('E32').Select()
    xl.Selection.Value = model.record(nn).field('fio').value().toString()
    ws.Range('C33').Select()

    xl.Selection.Value = str(model.record(nn).field('createdatetime').value().toString("dd.MM.yyyy"))
#'''

    #Погрешности    
    strSQL = u"""                
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
where chk.item = """ + str(item) + u"""                                                                         
  and chk.point is not null                         
--order by cl.coilnumber, cl.Tap, chk.QuadroLoad is not null, chk.Point
--order by cl.coilnumber, secondload desc, round(chk.point, 0), primarycurrent
--order by primarycurrent, cl.coilnumber, secondload desc, round(chk.point, 0)
--order by cl.coilnumber, primarycurrent, secondload desc, round(chk.point, 0)
order by cl.coilnumber, cl.Tap, primarycurrent, secondload desc, round(chk.point, 0)

"""
    
    # print strSQL
    query.prepare(strSQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания", QMessageBox.Ok)
        return
    else:    
        model_3.setQuery(query)
    if model_3.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных_ _ _ _ _!", QMessageBox.Ok)

    nrPogr  = 29

#    ''' zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz        
    for i in range(model_3.rowCount() - 1):
        ws.Rows(str(nrPogr)).EntireRow.Insert()
        
    sw1 = ''
    sw2 = ''

    M = []
    for i in range(model_3.rowCount()):        
        M += [[model_3.record(i).field('fullCoilName').value().toString(),
              model_3.record(i).field('primarycurrent').value().toString(),
              '',
              model_3.record(i).field('classaccuracy').value().toString(),
              model_3.record(i).field('cos').value().toString(),
              model_3.record(i).field('secondload').value().toString(),
              model_3.record(i).field('point').value().toString(),
              model_3.record(i).field('a').value().toString(),
              model_3.record(i).field('p').value().toString()]]
        
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
        for i in range(n):
            if i != n - 1:
                if M[n-i-1][0] == M[n-i-2][0]:
                    M[n-i-1][0] = ''
                    if M[n-i-1][1] == M[n-i-2][1]:
                        M[n-i-1][1] = ''
                    if M[n-i-1][2] == M[n-i-2][2]:
                        M[n-i-1][2] = ''
                    if M[n-i-1][3] == M[n-i-2][3]:
                        M[n-i-1][3] = ''
                    if M[n-i-1][4] == M[n-i-2][4]:
                        M[n-i-1][4] = ''
                    if M[n-i-1][5] == M[n-i-2][5]:
                        M[n-i-1][5] = ''

        # for i in range(n):
        #     print M[i]

        
        # Объединение очищеных ячеек
        endUnion = n - 1                
        for i in range(n):
            if M[n-i-1][0] != '':
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
            if M[n-i-1][1] != '':
                endUnion -= 1                
                ws.Range("B" + str(n - i - 2 + 30) + ":C" + str(endUnion + 30)).Select()
                xl.Selection.VerticalAlignment = 2
                xl.Selection.Merge()
                # print 'Merge'
                endUnion = n - i - 2                




        endUnion = n - 1                
        for i in range(n):
            if M[n-i-1][3] != '':
                endUnion -= 1                
                if endUnion != n - i - 2:
                    ws.Range("D" + str(n - i - 2 + 30) + ":D" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2                

        endUnion = n - 1                
        for i in range(n):
            if M[n-i-1][4] != '':
                endUnion -= 1                
                if endUnion != n - i - 2:
                    ws.Range("E" + str(n - i - 2 + 30) + ":E" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2                

        endUnion = n - 1                
        for i in range(n):
            if M[n-i-1][5] != '':
                endUnion -= 1                
                if endUnion != n - i - 2:
                    ws.Range("F" + str(n - i - 2 + 30) + ":F" + str(endUnion + 30)).Select()
                    xl.Selection.VerticalAlignment = 2
                    xl.Selection.Merge()
                    endUnion = n - i - 2                

            
#        ws.Range("A" + str(7) + ":I" + str(6 + len(M))).Select()
#        xl.Selection.HorizontalAlignment = 3
        
        
        
        
        
        
        
            
    ws.Range("H" + str(nrPogr) + ":H" + str(nrPogr + len(M) -1)).Select()
    
#    Application.UseSystemSeparators = False

#    xl.Selection.NumberFormat = "0,00"
#     print 'decimal_point = ' + decimal_point
    xl.Selection.NumberFormat = "0" + decimal_point + "00"
    
#    print locale.localeconv()['decimal_point']
            
    ws.Range("A" + str(nrPogr) + ":I" + str(nrPogr + len(M) -1)).Select()
    xl.Selection.Value = M
       
    '''    
    for i in range(model_3.rowCount() - 1):
        ws.Range('B' + str(nrPogr + i) + ':C' + str(nrPogr + i)).Select()
        xl.Selection.merge(True)
'''


#def CommonReport(db, test_map, item, visibleExcel):
def CommonReport(env, snID, accuracyR, accuracyI, gost_id, globalCorridors, globalCorridors_2, visibleExcel):
    print(1111, env)
    print(1111, snID)
    print(1111, accuracyR)
    print(1111, accuracyI)
    print(1111, gost_id)
    print(1111, globalCorridors)
    print(1111, globalCorridors)
    print(1111,globalCorridors_2)
    print(244214, visibleExcel)

    query = QSqlQuery(env.db)

    SQL = u'''    
select fullname, serialnumber, series, makedate, ordernumber             
from  serial_number sn
inner join transformer tf on sn.transformer = tf.id
where sn.id = :snID                                 
'''
    query.prepare(SQL)
    query.bindValue(":snID", snID)

    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания1", QMessageBox.Ok)
        return
    else:
        model.setQuery(query)

    fullname = model.record(0).field('fullname').value()
    serialnumber = model.record(0).field('serialnumber').value()
    series = model.record(0).field('series').value()
    makedate = model.record(0).field('makedate').value()
    ordernumber = model.record(0).field('ordernumber').value()

    SQL = u'''    
select
sn.id
, cast(cl.coilnumber as varchar ) || 'И1-' || cast(cl.coilnumber as varchar ) || 'И' || cast(cl.tap as varchar ) as coil
, primarycurrent
, coalesce(scChecking.quadroload, coalesce(apChecking.quadroload, coalesce(ltChecking.quadroload, cl.secondload))) as secondload
, points.ipercent
, scChecking.quadroload as quadroloadForOrder              
, cl.secondload as secondloadForOrder                      

, CASE WHEN scChecking.a IS NULL THEN 0 ELSE scChecking.a END as scA
, CASE WHEN scChecking.p IS NULL THEN 0 ELSE scChecking.p END as scP
, CASE WHEN apChecking.a IS NULL THEN 0 ELSE apChecking.a END as apA
, CASE WHEN apChecking.p IS NULL THEN 0 ELSE apChecking.p END as apP
, CASE WHEN ltChecking.a IS NULL THEN 0 ELSE ltChecking.a END as ltA
, CASE WHEN ltChecking.p IS NULL THEN 0 ELSE ltChecking.p END as ltP  
  
, scitem.acceptdatetime::date as scdate
, apitem.acceptdatetime::date as apdate
, ltitem.acceptdatetime::date as ltdate
  
, CASE WHEN scop.fio IS NULL THEN '' ELSE scop.fio END as scfio
, CASE WHEN apop.fio IS NULL THEN '' ELSE apop.fio END as apfio      
, CASE WHEN ltop.fio IS NULL THEN '' ELSE ltop.fio END as ltfio
        
from 
serial_number sn
inner join
coil cl
on
cl.transformer = sn.transformer
inner join
gost_detail points
on 
points.gost_id = :gost_id                 
and  points.classaccuracy = cl.classaccuracy
left join
item scItem
on
scItem.serial_number = sn.id
and scItem.acceptdatetime = (
  select 
    max(item.acceptdatetime) 
  from 
    item
  inner join
    test_map tm
  on
      item.test_map = tm.id
  inner join
      stand
  on
      stand.id = tm.stand
  inner join
      test_type tt
  on
      tt.id = stand.test_type
  where
    item.serial_number = :snID        
    and tt.code = 0 -- code of test type
)
left join
checking scChecking
on
scChecking.item = scItem.id
and scChecking.point = points.ipercent
and scChecking.coil = cl.id
and scChecking.quadroload is not null = points.usequadro
left join
item apItem
on
apItem.serial_number = sn.id
and apItem.acceptdatetime = (
  select 
    max(item.acceptdatetime) 
  from 
    item
  inner join
    test_map tm
  on
      item.test_map = tm.id
  inner join
      stand
  on
      stand.id = tm.stand
  inner join
      test_type tt
  on
      tt.id = stand.test_type
  where
    item.serial_number = :snID1
    and tt.code = 2 -- code of test type
)
left join
checking apChecking
on
apChecking.item = apItem.id
and apChecking.point = points.ipercent
and apChecking.coil = cl.id
and apChecking.quadroload is not null = points.usequadro
left join
item ltItem
on
ltItem.serial_number = sn.id
and ltItem.acceptdatetime = (
  select 
    max(item.acceptdatetime) 
  from 
    item
  inner join
    test_map tm
  on
      item.test_map = tm.id
  inner join
      stand
  on
      stand.id = tm.stand
  inner join
      test_type tt
  on
      tt.id = stand.test_type
  where
    item.serial_number = :snID2
    and tt.code = 1 -- code of test type
)
left join
checking ltChecking
on
ltChecking.item = ltItem.id
and ltChecking.point = points.ipercent
and ltChecking.coil = cl.id
and ltChecking.quadroload is not null = points.usequadro
left join
  test_map sctm
on
  sctm.id = scItem.test_map
left join
  operator scop
on
  scop.id = sctm.operator
--
left join
  test_map aptm
on
  aptm.id = apItem.test_map
left join
  operator apop
on
  apop.id = aptm.operator
--
left join
  test_map lttm
on
  lttm.id = ltItem.test_map
left join
  operator ltop
on
  ltop.id = lttm.operator

where
sn.id = :snID3
--order by coil, ipercent, secondload
--order by coil, secondload desc, ipercent, primarycurrent
order by coil, primarycurrent, secondload desc, ipercent, primarycurrent
'''

    query.clear()

    query.prepare(SQL)
    query.bindValue(":gost_id", gost_id)
    query.bindValue(":snID", snID)
    query.bindValue(":snID1", snID)
    query.bindValue(":snID2", snID)
    query.bindValue(":snID3", snID)

    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания2", QMessageBox.Ok)
        return
    else:
        model.setQuery(query)

    if model.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return


    SQL = u'''    
select t3.coilnumber
, cast(t3.coilnumber as varchar ) || 'И1-' || cast(t3.coilnumber as varchar ) || 'И' || cast(t3.tap as varchar )  as coil
, t1.r
, case when u2 is null then round(un,2) else round(u2,2) end as un              
, case when i2 is null then round(inom,4) else round(i2,4) end as inom             
, round(t1.k, 1) as k
, t1.rating
, t5.fio
, t2.createdatetime::date as sdate
, round(minR, 4) as minR, round(maxR, 4) as maxR, round(minI, 4) as minI, round(maxI, 4) as maxI            
, round(predel, 2) as predel
from checking_2 t1,            
(select max(t2.id) as id from item t1, checking_2 t2, stand t6, test_type t7
where t1.id=t2.item and t2.stand = t6.id and t6.test_type = t7.id
and t7.code = :code and serial_number = ''' + str(snID) + u'''    
group by serial_number, coil) t1_,                    
item t2, coil t3,
'''


#        SQL += u'''
#group by serial_number, coil) t1_,
#item t2, coil t3,
#'''

    SQL_2 = SQL

    # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors"
    SQL_ = ""
    if globalCorridors == []:
        SQL_ += u'''( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,
'''
    else:
        SQL_ += u'''(
'''
        for i in range(len(globalCorridors)):
            idCoil = str(globalCorridors[i][2])
            minR = str(globalCorridors[i][3])
            maxR = str(globalCorridors[i][4])

            minI = str(globalCorridors[i][5])
            maxI = str(globalCorridors[i][6])

            if minR == 'None':
                minR = '0'
            if maxR == 'None':
                maxR = '0'
            if minI == 'None':
                minI = '0'
            if maxI == 'None':
                maxI = '0'

            '''                    
            if minI == 'None':
                minI = 'null'    
            if maxI == 'None':
                maxI = 'null'
            '''

            if globalCorridors[i][7] != None:
                minI = str(globalCorridors[i][7])
            if globalCorridors[i][8] != None:
                maxI = str(globalCorridors[i][8])

            SQL_ += u'select ' + idCoil + u' as idCoil, ' + minR + u' as minR, ' + maxR + u' as maxR, ' + minI + u' as minI, ' + maxI + u''' as maxI
'''
            if i < len(globalCorridors) - 1:
                SQL_ += u'''union
'''
        SQL_ += u''') as corridor,
'''
    SQL += SQL_

    # Этот подзапрос будет тянуть данные не из таблицы а из списка "globalCorridors_2"
    SQL_ = ""
    if globalCorridors_2 == []:
        SQL_ += u'''( select 0 as idCoil, 0 as minR, 0 as maxR, 0 as minI, 0 as maxI ) as corridor,
'''
    else:
        SQL_ += u'''(
'''
        for i in range(len(globalCorridors_2)):
            idCoil = str(globalCorridors_2[i][2])
            minR = str(globalCorridors_2[i][3])
            maxR = str(globalCorridors_2[i][4])

            minI = str(globalCorridors_2[i][5])
            maxI = str(globalCorridors_2[i][6])

            if globalCorridors_2[i][7] != None:
                minI = str(globalCorridors_2[i][7])
            if globalCorridors_2[i][8] != None:
                maxI = str(globalCorridors_2[i][8])

            if minR == 'None':
                minR = '0'
            if maxR == 'None':
                maxR = '0'
            if minI == 'None':
                # print 2
                minI = '0'
            if maxI == 'None':
                maxI = '0'

            '''       
            if minI == 'None':
                minI = 'null'    
            if maxI == 'None':
                maxI = 'null'
            '''

            SQL_ += u'select ' + idCoil + u' as idCoil, ' + minR + u' as minR, ' + maxR + u' as maxR, ' + minI + u' as minI, ' + maxI + u''' as maxI
'''
            if i < len(globalCorridors_2) - 1:
                SQL_ += u'''union
'''
        SQL_ += u''') as corridor,
'''
    SQL_2 += SQL_

    SQL_ = u'''
test_map t4 LEFT OUTER JOIN operator t5 ON (t4.operator = t5.id),            
stand t6, test_type t7
where t1.id = t1_.id            
and t1.item = t2.id            
and t1.coil = t3.id
and t2.test_map = t4.id
and t2.serial_number = ''' + str(snID) + u'''                                                                  
and t3.id = corridor.idCoil
and t1.stand = t6.id
and t6.test_type = t7.id
and code = :code1
order by t3.coilnumber, t3.tap
'''

    SQL += SQL_
    SQL_2 += SQL_

    # print SQL
    # print
    # print
    # print
    # print SQL_2

    query.clear()
    query.prepare(SQL)
    print(56565,SQL)
    query.bindValue(":code", 3)
    query.bindValue(":code1", 3)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания_", QMessageBox.Ok)
        return
    else:
        model_2.setQuery(query)

    query.clear()
    query.prepare(SQL_2)
    query.bindValue(":code", 4)
    query.bindValue(":code1", 4)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов испытания_ _", QMessageBox.Ok)
        return
    else:
        model_3.setQuery(query)
    SQL = u'''
select t2.createdatetime::date as sdate, t4.fio, t1_.pdl       
from item t1 left outer join checking_3 t1_ on (t1.id = t1_.item)                     , 
test_map as t2, stand as t3, operator as t4, test_type as t5
where t1.test_map = t2.id
and t2.stand = t3.id
and t2.operator = t4.id
and t3.test_type = t5.id
and t5.code = 7
and t1.serial_number = ''' + str(snID) + u'''
'''
    query.clear()
    query.prepare(SQL)
    if not query.exec_():
        QMessageBox.warning(None, u"Предупреждение", u"Ошибка выборки результатов высоковоьтного испытания", QMessageBox.Ok)
        return
    else:
        model_4.setQuery(query)

    try:
        xl = Dispatch('Excel.Application')
    except:
        QMessageBox.warning(None, u"Предупреждение", u"Не запускается Excel", QMessageBox.Ok)
        return u"Не запускается Excel"

    xl.Visible = visibleExcel
    inputFile = os.getcwd() + u'\\rpt\\Общий_отчет.xlsx'  # Шаблон

    try:
    # установить на шаблон read-only на время формирования отчета
        os.chmod(inputFile, stat.S_IREAD)
    except:
        QMessageBox.warning(None, u"Предупреждение", u"Отсутствует шаблон: " + inputFile, QMessageBox.Ok)
        return

    wb = xl.Workbooks.Add(inputFile)
    # try:
    #     wb = xl.Workbooks.Workbooks.Add(inputFile)
    #     # wb = xl.Workbooks.Open(inputFile)
    # except:
    #     QMessageBox.warning(None, u"Предупреждение", u"Не открывается файл: " + inputFile, QMessageBox.Ok)
    #     return

    ws = wb.Worksheets(1)

    ws.Range("C2").Select()
    xl.Selection.Value = fullname
    ws.Range("C3").Select()
    xl.Selection.Value = serialnumber
    ws.Range("F3").Select()
    xl.Selection.Value = series
    ws.Range("C4").Select()
    xl.Selection.Value = '20' + str(makedate)
    ws.Range("F4").Select()
    xl.Selection.Value = ordernumber

    nrIns = 8
    for i in range(model.rowCount() - 1):
        ws.Rows(str(nrIns)).EntireRow.Insert()

    M = []

    for i in range(model.rowCount()):
        # print model.record(i).field('secondload').value().toString()
        # print model.record(i).field('scA').value().toString(), str(model.record(i).field('scA').value().toString())

        R = [model.record(i).field('coil').value(),
             str(model.record(i).field('primarycurrent').value()),
             str(model.record(i).field('secondload').value()),
             str(model.record(i).field('ipercent').value()),
             str(model.record(i).field('scA').value()),
             str(model.record(i).field('scP').value()),
             str(model.record(i).field('apA').value()),
             str(model.record(i).field('apP').value()),
             str(model.record(i).field('ltA').value()),
             str(model.record(i).field('ltP').value())]
        M += [R]

    '''
        ws.Range('A1:G1').Select()
        xl.Selection.Font.Size = 16
        xl.Selection.Merge()
        
        # Удаление горизонтальных черточек
        n = model.rowCount()     
        for i in range(n):
            if i != n - 1:
                if M[n-i-1][0] == M[n-i-2][0]:
                    M[n-i-1][0] = ''
                    ws.Range("A" + str(n - i + 2)).Select()
                    xl.Selection.Borders(4).LineStyle = 0      # низ
'''

    # Очищение повторяющихся знаений
    n = model.rowCount()
    for i in range(n):
        if i != n - 1:
            if M[n-i-1][0] == M[n-i-2][0]:
                M[n-i-1][0] = ''
                if M[n-i-1][1] == M[n-i-2][1]:
                    M[n-i-1][1] = ''

    # for i in range(n):
    #     print M[i]

    ws.Range("A" + str(7) + ":J" + str(6 + len(M))).Select()
    xl.Selection.HorizontalAlignment = 3

    xl.Selection.Value = M



#        '''
    # Объединение очищеных ячеек
    endUnion = n - 1
    for i in range(n):
        if M[n-i-1][0] != '':
            endUnion -= 1
            if endUnion != n - i - 2:
                ws.Range("A" + str(n - i - 2 + 8) + ":A" + str(endUnion + 8)).Select()
                xl.Selection.VerticalAlignment = 2
                xl.Selection.Merge()
                endUnion = n - i - 2

    endUnion = n - 1
    for i in range(n):
        if M[n-i-1][1] != '':
            endUnion -= 1
            if endUnion != n - i - 2:
                ws.Range("B" + str(n - i - 2 + 8) + ":B" + str(endUnion + 8)).Select()
                xl.Selection.VerticalAlignment = 2
                xl.Selection.Merge()
                endUnion = n - i - 2
#       '''


    ws.Range("E" + str(n + 7)).Select()
    xl.Selection.Value = model.record(0).field('scfio').value()
    ws.Range("F" + str(n + 7)).Select()
    try:
        xl.Selection.Value = str(model.record(0).field('scdate').value().toString("dd.MM.yy"))
    except:
        pass

    ws.Range("G" + str(n + 7)).Select()
    xl.Selection.Value = model.record(0).field('apfio').value()
    ws.Range("H" + str(n + 7)).Select()
    try:
        xl.Selection.Value = str(model.record(0).field('apdate').value().toString("dd.MM.yy"))
    except:
        pass

    ws.Range("I" + str(n + 7)).Select()
    xl.Selection.Value = model.record(0).field('ltfio').value()
    ws.Range("J" + str(n + 7)).Select()
    try:
        xl.Selection.Value = str(model.record(0).field('ltdate').value().toString("dd.MM.yy"))
    except:
        pass

    M = []
    for i in range(model_2.rowCount()):
        R = [model_2.record(i).field('coil').value(),
             str(model_2.record(i).field('r').value()),
             str(model_2.record(i).field('minr').value()),
             str(model_2.record(i).field('maxr').value()),
             str(model_2.record(i).field('k').value()),
             str(model_2.record(i).field('un').value()),
             str(model_2.record(i).field('inom').value()),
             str(model_2.record(i).field('predel').value())]
        M += [R]
    nrIns = 12 + model.rowCount()
    for i in range(model_2.rowCount() - 1):
        ws.Rows(str(nrIns)).EntireRow.Insert()

    sdvig = 1
    if model.rowCount() > 0:
        sdvig = model.rowCount()

    if model_2.rowCount() > 0:
####        ws.Range("A" + str(12 + model.rowCount()) + ":H" + str(11 + model.rowCount() + len(M))).Select()
        ws.Range("A" + str(12 + sdvig) + ":H" + str(11 + sdvig + len(M))).Select()
        xl.Selection.HorizontalAlignment = 3
        xl.Selection.Value = M
    ####        ws.Range("C" + str(12 + model.rowCount() + len(M))).Select()
        ws.Range("C" + str(12 + sdvig + len(M))).Select()
        xl.Selection.Value = model_2.record(0).field('fio').value()
    ####        ws.Range("F" + str(12 + model.rowCount() + len(M))).Select()
        ws.Range("F" + str(12 + sdvig + len(M))).Select()
        try:
            xl.Selection.Value = model_2.record(0).field('sdate').value().toString("dd.MM.yy")
        except:
            pass

    M = []

    for i in range(model_3.rowCount()):
        R = [model_3.record(i).field('coil').value(),
             str(model_3.record(i).field('r').value()),
             str(model_3.record(i).field('minr').value()),
             str(model_3.record(i).field('maxr').value()),
             str(model_3.record(i).field('k').value()),
             str(model_3.record(i).field('un').value()),
             str(model_3.record(i).field('inom').value()),
             str(model_3.record(i).field('predel').value())]
        M += [R]


    if model_2.rowCount() > 0:
        sdvig += model_2.rowCount()
    else:
        sdvig += 1



####        nrIns = 17 + model.rowCount() + model_2.rowCount()
    nrIns = 17 + sdvig
    for i in range(model_3.rowCount() - 1):
        ws.Rows(str(nrIns)).EntireRow.Insert()
####        ws.Range("A" + str(17 + model.rowCount() + model_2.rowCount()) + ":H" + str(16 + model.rowCount() + model_2.rowCount() + len(M))).Select()
    ws.Range("A" + str(17 + sdvig) + ":H" + str(16 + sdvig + len(M))).Select()
    xl.Selection.HorizontalAlignment = 3
    xl.Selection.Value = M
####        ws.Range("C" + str(17 + model.rowCount() + model_2.rowCount() + len(M))).Select()
    ws.Range("C" + str(17 + sdvig + len(M))).Select()
    xl.Selection.Value = model_3.record(0).field('fio').value()
####        ws.Range("F" + str(17 + model.rowCount() + model_2.rowCount() + len(M))).Select()
    ws.Range("F" + str(17 + sdvig + len(M))).Select()
    try:
        xl.Selection.Value = model_3.record(0).field('sdate').value().toString("dd.MM.yy")
    except:
        pass


#        if model_4.rowCount() < 1:
#            QMessageBox.warning(None, u"Предупреждение", u"По высоковольтным испытаниям нет данных!", QMessageBox.Ok)
#            return


    if model_3.rowCount() > 0:
        sdvig += model_3.rowCount()
    else:
        sdvig += 1


####        nrIns = 21 + model.rowCount() + model_2.rowCount() + model_3.rowCount()
    nrIns = 21 + sdvig
    ws.Range("A" + str(nrIns)).Select()
    try:
        xl.Selection.Value = model_4.record(0).field('sdate').value().toString("dd.MM.yy")
    except:
        pass
    ws.Range("C" + str(nrIns)).Select()
    xl.Selection.Value = model_4.record(0).field('fio').value()
    ws.Range("E" + str(nrIns)).Select()
    if str(model_4.record(0).field('pdl').value()) == '0':
        xl.Selection.Value = ''
    else:
        xl.Selection.Value = str(model_4.record(0).field('pdl').value())

    ws.Range("F" + str(nrIns + 2)).Select()
    print(4234, nrIns)


    #ищем дополнильные испытания с омикрона
    query_t24 = QSqlQuery()
    sql = f"""select ITEM.ID    from item
    inner join test_map on item.test_map = test_map.id
    inner join stand on test_map.stand = stand.id
    inner join test_tc on test_tc.item = item.id
    where item.serial_number = {snID} and stand.test_type = 24 and test_map.accepted
    order by test_map.acceptdatetime  DESC
    LIMIT 1
        """
    print(sql)
    query_t24.exec_(sql)
    query_t24.next()
    item = query_t24.value(0)
    if item:
        nrIns = nrIns + 2
        info = select_passportTT(item)
        print(info)
        ws.Range(f"A{nrIns}:H{nrIns}").Merge()
        # ws.Range(f"A:{nrIns}:H{nrIns}").Merge()
        # ws.Cells(nrIns, 1).Value = f"№{info['makedate']}-{info['serialnumber']} {info['operator']} {info['data']}"
        ws.Cells(nrIns, 1).Value = info['stand']
        ws.Cells(nrIns, 1).Font.Bold = True
        ws.Cells(nrIns, 1).Font.Size = 14


        coil_name = parser_name_tt(info['idItem'])
        coil = parse_result_tt(info['idItem'], coil_name)
        dop_params = extra_options(coil, info['idItem'], 24)
        position_parametr = 3
        position_coil = nrIns + 2
        position_coils = {}
        ws.Range(f"A{nrIns + 1}:B{nrIns + 1}").Merge()
        ws.Cells(nrIns + 1, 1).Value = 'Обмотки'
        pc = 0
        for i in dop_params:
            if dop_params[i] != {}:
                ws.Cells(nrIns + 1, position_parametr).Value = i
                for c in dop_params[i]:
                    if c not in position_coils:
                        position_coils[c] = position_coil
                        ws.Range(f"A{position_coil}:B{position_coil}").Merge()
                        ws.Cells(position_coil, 1).Value = coil[c][5]
                        print(5464,coil[c][5])
                        position_coil += 1
                    pc = position_coils[c]
                    val = dop_params[i][c]
                    print(5454,pc,val, position_parametr)
                    ws.Cells(pc, position_parametr).Value = str(val)
                position_parametr += 1
        mx1 = ws.Cells(3, position_parametr - 1)
        x = mx1.Address[1]
        print(545636,f"A{nrIns + 1}:{x}{position_coil - 1}")
        ws.Range(f"A{nrIns + 1}:{x}{position_coil - 1}").Borders.LineStyle = True
        print(464785, position_coil)
        ws.Range(f"A{position_coil}:B{position_coil}").Merge()
        ws.Range(f"A{position_coil}").Value = 'Испытатель, дата исп.:'
        ws.Range(f"A{position_coil}").Font.Bold = True
        ws.Range(f"A{position_coil}").Font.Size = 9
        ws.Range(f"C{position_coil}:D{position_coil}").Merge()
        ws.Range(f"C{position_coil}").Value = info['operator']
        ws.Range(f"E{position_coil}:F{position_coil}").Merge()
        ws.Range(f"E{position_coil}").Value = info['data']
        nrIns = position_coil



    #ищем дополнильные испытания с омикрона
    query_t24 = QSqlQuery()
    sql = f"""select ITEM.ID    from item
    inner join test_map on item.test_map = test_map.id
    inner join stand on test_map.stand = stand.id
    inner join test_tc on test_tc.item = item.id
    where item.serial_number = {snID} and stand.test_type = 25 and test_map.accepted
    order by test_map.acceptdatetime  DESC
    LIMIT 1
        """
    print(sql)
    query_t24.exec_(sql)
    query_t24.next()
    item = query_t24.value(0)
    if item:
        nrIns = nrIns + 2
        info = select_passportTT(item)
        print(info)
        ws.Range(f"A{nrIns}:H{nrIns}").Merge()
        # ws.Range(f"A:{nrIns}:H{nrIns}").Merge()
        # ws.Cells(nrIns, 1).Value = f"№{info['makedate']}-{info['serialnumber']} {info['operator']} {info['data']}"
        ws.Cells(nrIns, 1).Value = info['stand']
        ws.Cells(nrIns, 1).Font.Bold = True
        ws.Cells(nrIns, 1).Font.Size = 14


        coil_name = parser_name_tt(info['idItem'])
        coil = parse_result_tt(info['idItem'], coil_name)
        dop_params = extra_options(coil, info['idItem'], 25)
        position_parametr = 3
        position_coil = nrIns + 2
        position_coils = {}
        ws.Range(f"A{nrIns + 1}:B{nrIns + 1}").Merge()
        ws.Cells(nrIns + 1, 1).Value = 'Обмотки'
        pc = 0
        for i in dop_params:
            if dop_params[i] != {}:
                ws.Cells(nrIns + 1, position_parametr).Value = i
                for c in dop_params[i]:
                    if c not in position_coils:
                        position_coils[c] = position_coil
                        ws.Range(f"A{position_coil}:B{position_coil}").Merge()
                        ws.Cells(position_coil, 1).Value = coil[c][5]
                        print(5464,coil[c][5])
                        position_coil += 1
                    pc = position_coils[c]
                    val = dop_params[i][c]
                    print(5454,pc,val, position_parametr)
                    ws.Cells(pc, position_parametr).Value = str(val)
                position_parametr += 1
        mx1 = ws.Cells(3, position_parametr - 1)
        x = mx1.Address[1]
        print(545636,f"A{nrIns + 1}:{x}{position_coil - 1}")
        ws.Range(f"A{nrIns + 1}:{x}{position_coil - 1}").Borders.LineStyle = True
        print(464785, position_coil)
        ws.Range(f"A{position_coil}:B{position_coil}").Merge()
        ws.Range(f"A{position_coil}").Value = 'Испытатель, дата исп.:'
        ws.Range(f"A{position_coil}").Font.Bold = True
        ws.Range(f"A{position_coil}").Font.Size = 9
        ws.Range(f"C{position_coil}:D{position_coil}").Merge()
        ws.Range(f"C{position_coil}").Value = info['operator']
        ws.Range(f"E{position_coil}:F{position_coil}").Merge()
        ws.Range(f"E{position_coil}").Value = info['data']
        nrIns = position_coil





    xl.Selection.Value = u'Дата печати: ' + str(datetime.date.today().day) + '.' + str(datetime.date.today().month) + '.' + str(datetime.date.today().year)

    # except:
    #     print "Неопознанная ошибка 8 ... "
    #


def select_passportTT(items,  kontroler=True):
    # получаем необходимые данные
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
            transformer.voltage,
            transformer.maxopervoltage,
            t1.fio,
            transformer.dynamic_current,
            type_transformer.ID,
            type_transformer.type,
            transformer.time_thermal_current,
            transformer.thermal_current,
            t1.operator as operator,
            t1.stand,
            transformer_extra.lead_length,
            transformer_extra.turns_ratio,
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
                left JOIN type_transformer on transformer.type_transformer = type_transformer.id
                left join transformer_extra on serial_number.id = transformer_extra.serial_number
"""
    print(sql)

    model.setQuery(sql)
    if model.rowCount() < 1:
        QMessageBox.warning(None, u"Предупреждение", u"Нет данных!", QMessageBox.Ok)
        return False

    for i in range(model.rowCount()):
        info = {}
        info['idItem'] = model.index(i, 0).data()
        info['data'] = model.index(i, 1).data().toString('dd.MM.yyyy')
        info['idsn'] = model.index(i, 2).data()
        info['ordernumber'] = model.index(i, 3).data()
        info['series'] = model.index(i, 4).data()
        info['serialnumber'] = model.index(i, 5).data()
        info['makedate'] = model.index(i, 6).data()
        info['idTransformer'] = model.index(i, 7).data()
        info['fullname'] = model.index(i, 8).data()
        info['weight'] = model.index(i, 9).data()
        info['copperP'] = model.index(i, 10).data()
        info['copperPN'] = model.index(i, 11).data()
        info['voltage'] = model.index(i, 12).data()
        info['maxvoltage'] = model.index(i, 13).data()
        info['poveritel'] = model.index(i, 14).data()
        info['dynamic_current'] = model.index(i, 15).data()
        info['type_transformer'] = model.index(i, 16).data()
        info['type'] = model.index(i, 17).data()
        info['time_current'] = model.index(i, 18).data()
        info['thermal_current'] = model.index(i, 19).data()
        info['operator'] = model.index(i, 20).data()
        info['stand'] = model.index(i, 21).data()
        info['lead_length'] = model.index(i, 22).data()
        info['turns'] = model.index(i, 23).data()
        info['kontroler'] = kontroler
        for key in info:
            if info[key] == 0:
                if key == 'copperP':
                    info[key] = 0.5
                elif key == 'copperPN':
                    info[key] = 0.3
                else:
                    info[key] = ''
        return info

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
                                    order by t1.createdatetime desc
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

def toFixed(numObj, digits=0):
    if type(numObj) not in (float,int):
        return None
    print(33, numObj)
    return f"{numObj:.{digits}f}"


def float_or_int(number, digits = 1, digitsF = 2):
    if number % 1 == 0:
        return  toFixed(number,digits)
    else:
        return toFixed(number,digitsF)




def fill_report_heart(model):
    import win32com
    try:
        Excel = win32com.client.Dispatch("Excel.Application")
    except:
        print("Не запускается Excel")
        return
    Excel.Visible = 1
    inputFile = os.getcwd() + u'\\rpt\\Общий_отчет_сердечников.xlsx'
    Excel.Visible = 1
    print(233,inputFile)
    wb = Excel.Workbooks.Add(inputFile)
    ws = wb.Worksheets(1)
    p = 2

    for i in range(model.rowCount()):
        iron = model.record(i).field('feature').value()
        out_diameter = model.record(i).field('out_diameter').value()
        in_diameter = model.record(i).field('in_diameter').value()
        height = model.record(i).field('height').value()
        num = model.record(i).field('num').value()
        voltage = model.record(i).field('voltage').value()
        date = model.record(i).field('createdatetime').value().toString('MM.dd.yyyy')
        amount = model.record(i).field('amount').value()
        print(4325325, date)
        ws.Range(f'A{p}:H{p}').Value = [iron,out_diameter,in_diameter,height,num,amount, voltage,date]
        p +=1


def fill_report_apg(model):
    import win32com
    try:
        Excel = win32com.client.Dispatch("Excel.Application")
    except:
        print("Не запускается Excel")
        return
    Excel.Visible = 1
    inputFile = os.getcwd() + u'\\rpt\\Общий_отчет_АПГ.xlsx'
    Excel.Visible = 1
    print(233,inputFile)
    wb = Excel.Workbooks.Add(inputFile)
    ws = wb.Worksheets(1)
    p = 2

    for i in range(model.rowCount()):
        owens = model.record(i).field('owens').value()
        trm = model.record(i).field('trm').value()
        sv = model.record(i).field('set_value').value()
        pv = model.record(i).field('present_value').value()
        date = model.record(i).field('date').value().toString('dd.MM.yyyy hh:mm')
        print(4325325, date)
        ws.Range(f'A{p}:E{p}').Value = [owens,trm,sv,pv,date]
        p +=1