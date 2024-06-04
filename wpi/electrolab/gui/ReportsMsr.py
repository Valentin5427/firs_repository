# -*- coding: UTF-8 -*-

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from win32com.client import Dispatch
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import  QMessageBox, QDialog

import time
import os, stat
import datetime
import calendar
from electrolab.gui import  JournalMsr
from datetime import date

# Отчет 'График поверки измерительного инструмента'
class GraphPPR(QDialog):
    def __init__(self, env, *args):
        QDialog.__init__(self, *args)
                       
        global db1
        db1 = env.db
        
        global path_ui                    
        path_ui = env.config.paths.ui + "/"
        global path_rpt                    
        path_rpt = env.config.paths.rpt + "/"
        if not JournalMsr.MyLoadUi(path_ui, "ReportlocationMsr.ui", self):
            return
                                                                           
        self.pushButton.clicked.connect(self.pushButton1_Click)
        
        self.query = QSqlQuery(db1)
        self.query_2 = QSqlQuery(db1)
        
        self.dateEdit.setDate(datetime.date.today())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def pushButton1_Click___(self):
        ALF = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
                        
        try:
            xl = Dispatch('Excel.Application')
        except:
            return u"Не запускается Excel"
                    
        name_file = u'График ППР и аттестации.xlsx'
        inputFile = os.getcwd() + u'/' + path_rpt + name_file  # Шаблон
        
        if not os.path.exists(inputFile):        
            inputFile = os.getcwd() + u'/' + name_file  # Шаблон        
        
        try:
            # установить на шаблон read-only на время формирования отчета 
            os.chmod(inputFile, stat.S_IREAD)
        except:    
            QMessageBox.warning(self, u"Предупреждение", u"Отсутствует шаблон: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(self, u"Предупреждение", u"Не открывается файл: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
  
        xl.Visible = True
                
        ws = wb.Worksheets(1)
        
        nIns = 10  # № строки в шаблоне, откуда начинается вставка перечня средств 
        nTitle = 6
        row = ws.Rows(str(nIns + 1))                    
        
        ws.Cells(nTitle - 2, 1).Value += u" " + str(self.dateEdit.date().year()) + u" г."
        ws.Cells(nTitle - 2, 11).Value += u" " + str(self.dateEdit.date().year()) + u" г."
        
        ws.Cells(nTitle, 1).Value += u" " + str(self.dateEdit.date().year()) + u" год"
        ws.Cells(nTitle + 1, 1).Value += u" " + str(self.dateEdit.text()) + u" г."
        '''
select t0.*, cd1, vd1, cd2, vd2, cd3, vd3, cd4, vd4, cd5, vd5, cd6, vd6, cd7, vd7, cd8, vd8, cd9, vd9, cd10, vd10, cd11, vd11, cd12, vd12,
case when cd1 is not null and vd1 is not null then cd1||'/'||vd1 else case when cd1 is not null then cd1 when vd1 is not null then vd1 end end m1,
case when cd2 is not null and vd2 is not null then cd2||'/'||vd2 else case when cd2 is not null then cd2 when vd2 is not null then vd2 end end m2,
case when cd3 is not null and vd3 is not null then cd3||'/'||vd3 else case when cd3 is not null then cd3 when vd3 is not null then vd3 end end m3,
case when cd4 is not null and vd4 is not null then cd4||'/'||vd4 else case when cd4 is not null then cd4 when vd4 is not null then vd4 end end m4,
case when cd5 is not null and vd5 is not null then cd5||'/'||vd5 else case when cd5 is not null then cd5 when vd5 is not null then vd5 end end m5,
case when cd6 is not null and vd6 is not null then cd6||'/'||vd6 else case when cd6 is not null then cd6 when vd6 is not null then vd6 end end m6,
case when cd7 is not null and vd7 is not null then cd7||'/'||vd7 else case when cd7 is not null then cd7 when vd7 is not null then vd7 end end m7,
case when cd8 is not null and vd8 is not null then cd8||'/'||vd8 else case when cd8 is not null then cd8 when vd8 is not null then vd8 end end m8,
case when cd9 is not null and vd9 is not null then cd9||'/'||vd9 else case when cd9 is not null then cd9 when vd9 is not null then vd9 end end m9,
case when cd10 is not null and vd10 is not null then cd10||'/'||vd10 else case when cd10 is not null then cd10 when vd10 is not null then vd10 end end m10,
case when cd11 is not null and vd11 is not null then cd11||'/'||vd11 else case when cd11 is not null then cd11 when vd11 is not null then vd11 end end m11,
case when cd12 is not null and vd12 is not null then cd12||'/'||vd12 else case when cd12 is not null then cd12 when vd12 is not null then vd12 end end m12
'''
                
        SQL = u"""
select t0.*, cd1, vd1, cd2, vd2, cd3, vd3, cd4, vd4, cd5, vd5, cd6, vd6, cd7, vd7, cd8, vd8, cd9, vd9, cd10, vd10, cd11, vd11, cd12, vd12
from
(
  select t3.id, name_group || ' ' || name_msr as name, zav_num, period, period_view
  from group_msr t1, msr t2, zav_msr t3, type_msr t4
  where t1.id = t2.id_group
  and t2.id = t3.id_msr
  and t1.id_type = t4.id
  and t4.id_category = 3        
) t0
LEFT OUTER JOIN (select id_zav, 'А' cd1 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 1 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc1 on (t0.id = tc1.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd1 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 1 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv1 on (t0.id = tv1.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd2 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 2 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc2 on (t0.id = tc2.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd2 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 2 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv2 on (t0.id = tv2.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd3 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 3 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc3 on (t0.id = tc3.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd3 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 3 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv3 on (t0.id = tv3.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd4 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 4 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc4 on (t0.id = tc4.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd4 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 4 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv4 on (t0.id = tv4.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd5 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 5 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc5 on (t0.id = tc5.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd5 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 5 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv5 on (t0.id = tv5.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd6 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 6 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc6 on (t0.id = tc6.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd6 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 6 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv6 on (t0.id = tv6.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd7 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 7 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc7 on (t0.id = tc7.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd7 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 7 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv7 on (t0.id = tv7.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd8 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 8 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc8 on (t0.id = tc8.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd8 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 8 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv8 on (t0.id = tv8.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd9 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 9 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc9 on (t0.id = tc9.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd9 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 9 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv9 on (t0.id = tv9.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd10 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 10 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc10 on (t0.id = tc10.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd10 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 10 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv10 on (t0.id = tv10.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd11 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 11 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc11 on (t0.id = tc11.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd11 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 11 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv11 on (t0.id = tv11.id_zav)
LEFT OUTER JOIN (select id_zav, 'А' cd12 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(checking_date)) = 12 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tc12 on (t0.id = tc12.id_zav)
LEFT OUTER JOIN (select id_zav, 'П' vd12 from journal_checking group by id_zav having EXTRACT(MONTH FROM max(view_date)) = 12 and max(checking_date) <= to_date('""" + unicode(self.dateEdit.text()) + u"""','dd.mm.yyyy')) tv12 on (t0.id = tv12.id_zav)
order by zav_num
"""        



        '''
        QMessageBox.warning(self, u"Предупреждение", u"1", QMessageBox.Ok)
        f = open('D:\SQL.TXT', 'w')
        QMessageBox.warning(self, u"Предупреждение", u"2", QMessageBox.Ok)
        f.write(SQL)
        QMessageBox.warning(self, u"Предупреждение", u"3", QMessageBox.Ok)
        f.close()
        QMessageBox.warning(self, u"Предупреждение", u"4", QMessageBox.Ok)
        '''
        
        self.query.prepare(SQL)            
        self.query.exec_()
        if self.query.lastError().isValid():
            #return u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса к БД1", QMessageBox.Ok)
            # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            return
        
        
#        QMessageBox.warning(self, u"Предупреждение", u"Колич. позиций = " + str(self.query.size()), QMessageBox.Ok)
        

        xl.Visible = False
        for i in range(self.query.size() + 1):
            row.Insert()
        xl.Visible = True
 
        # print 'self.query.size() = ', self.query.size()

        M = range(self.query.size())       
        
        self.query.first()
        # Суммарные списки
        scd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
        svd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
        for i in range(0, self.query.size()):
            cd = range(12)
            vd = range(12)
            m  = range(12)
            
            for j in range(12):
                cd[j] = self.query.record().value("cd" + str(j + 1)).toString()
                vd[j] = self.query.record().value("vd" + str(j + 1)).toString()

            period_view = 0
            if self.query.record().value("period_view").toString() != '':
                period_view = int(self.query.record().value("period_view").toString())
            for j in range(12):
                if cd[11 - j] != '' and j > period_view:
                    cd[11 - j + period_view] = cd[11 - j]

                
            for j in range(12):
                m[j] = ''
                if cd[j] != '': m[j] = cd[j]
                if vd[j] != '': m[j] = vd[j]
                if cd[j] != '' and vd[j] != '': m[j] = cd[j] + '/' + vd[j]
            
                            
                if self.query.record().value("cd" + str(j + 1)).toString() != '':
                    scd[j] += 1
                if self.query.record().value("vd" + str(j + 1)).toString() != '':
                    svd[j] += 1
                
            # Заполняем пустые строки
            currN = nIns + i   # № текущей строки

            # Заполняем массив M данными
            M[i]=range(16)
            for j in range(16):
                M[i][j] = ''
            
            '''
            cd1 = unicode(self.query.record().value("cd1").toString())
            vd1 = unicode(self.query.record().value("vd1").toString())
            cd2 = unicode(self.query.record().value("cd2").toString())
            vd2 = unicode(self.query.record().value("vd2").toString())
            cd3 = unicode(self.query.record().value("cd3").toString())
            vd3 = unicode(self.query.record().value("vd3").toString())
            cd4 = unicode(self.query.record().value("cd4").toString())
            vd4 = unicode(self.query.record().value("vd4").toString())
            cd5 = unicode(self.query.record().value("cd5").toString())
            vd5 = unicode(self.query.record().value("vd5").toString())
            cd6 = unicode(self.query.record().value("cd6").toString())
            vd6 = unicode(self.query.record().value("vd6").toString())
            cd7 = unicode(self.query.record().value("cd7").toString())
            vd7 = unicode(self.query.record().value("vd7").toString())
            cd8 = unicode(self.query.record().value("cd8").toString())
            vd8 = unicode(self.query.record().value("vd8").toString())
            cd9 = unicode(self.query.record().value("cd9").toString())
            vd9 = unicode(self.query.record().value("vd9").toString())
            cd10 = unicode(self.query.record().value("cd10").toString())
            vd10 = unicode(self.query.record().value("vd10").toString())
            cd11 = unicode(self.query.record().value("cd11").toString())
            vd11 = unicode(self.query.record().value("vd11").toString())
            cd12 = unicode(self.query.record().value("cd12").toString())
            vd12 = unicode(self.query.record().value("vd12").toString())
            m1 = ''
            if cd1 != '': m1 = cd1
            if vd1 != '': m1 = vd1
            if cd1 != '' and vd1 != '': m1 = cd1 + '/' + vd1
            m2 = ''
            if cd2 != '': m2 = cd2
            if vd2 != '': m2 = vd2
            if cd2 != '' and vd2 != '': m2 = cd2 + '/' + vd2
            m3 = ''
            if cd3 != '': m3 = cd3
            if vd3 != '': m3 = vd3
            if cd3 != '' and vd3 != '': m3 = cd3 + '/' + vd3
            m4 = ''
            if cd4 != '': m4 = cd4
            if vd4 != '': m4 = vd4
            if cd4 != '' and vd4 != '': m4 = cd4 + '/' + vd4
            m5 = ''
            if cd5 != '': m5 = cd5
            if vd5 != '': m5 = vd5
            if cd5 != '' and vd5 != '': m5 = cd5 + '/' + vd5
            m6 = ''
            if cd6 != '': m6 = cd6
            if vd6 != '': m6 = vd6
            if cd6 != '' and vd6 != '': m6 = cd6 + '/' + vd6
            m7 = ''
            if cd7 != '': m7 = cd7
            if vd7 != '': m7 = vd7
            if cd7 != '' and vd7 != '': m7 = cd7 + '/' + vd7
            m8 = ''
            if cd8 != '': m8 = cd8
            if vd8 != '': m8 = vd8
            if cd8 != '' and vd8 != '': m8 = cd8 + '/' + vd8
            m9 = ''
            if cd9 != '': m9 = cd9
            if vd9 != '': m9 = vd9
            if cd9 != '' and vd9 != '': m9 = cd9 + '/' + vd9
            m10 = ''
            if cd10 != '': m10 = cd10
            if vd10 != '': m10 = vd10
            if cd10 != '' and vd10 != '': m10 = cd10 + '/' + vd10
            m11 = ''
            if cd11 != '': m11 = cd11
            if vd11 != '': m11 = vd11
            if cd11 != '' and vd11 != '': m11 = cd11 + '/' + vd11
            m12 = ''
            if cd12 != '': m12 = cd12
            if vd12 != '': m12 = vd12
            if cd12 != '' and vd12 != '': m12 = cd12 + '/' + vd12
               '''         
            
                        
            M[i][0] = i + 1
            M[i][1] = unicode(self.query.record().value("name").toString())
            M[i][2] = unicode(self.query.record().value("zav_num").toString())
            

            for j in range(12):
              M[i][j + 3] = m[j]
            
            '''
            M[i][3] = m1
            M[i][4] = m2
            M[i][5] = m3
            M[i][6] = m4
            M[i][7] = m5
            M[i][8] = m6
            M[i][9] = m7
            M[i][10] = m8
            M[i][11] = m9
            M[i][12] = m10
            M[i][13] = m11
            M[i][14] = m12
               '''
                                                 
            self.query.next()
            if self.query.lastError().isValid():
                pass
                # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())

        ws.Range("A" + str(nIns) + ":P" + str(self.query.size() + nIns)).Select()
        xl.Selection.Borders(1).LineStyle = 1
        xl.Selection.Borders(2).LineStyle = 1
        xl.Selection.Borders(3).LineStyle = 1
        xl.Selection.Borders(4).LineStyle = 1

        for c in (0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.VerticalAlignment = 2

        ws.Range(ALF[2] + str(nIns) + ":" + ALF[2] + str(self.query.size() + nIns)).Select()
        xl.Selection.NumberFormat = "@"


        for c in (1, 2, 15):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.HorizontalAlignment = 2
            xl.Selection.VerticalAlignment = 1
            
        for c in range(16):
#            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.WrapText = True
                                        
        ws.Range("A" + str(nIns) + ":P" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Value = M
        
        ws.Range('B' + str(self.query.size() + nIns) + ":B" + str(self.query.size() + nIns)).Select()
        xl.Selection.Value = u'Всего: (аттестация/ППР)' 
#        xl.Selection.Font.Size = 16
        xl.Selection.Font.bold = True
        for j in range(12):
            ws.Range(ALF[j + 3] + str(self.query.size() + nIns) + ":" + ALF[j + 3] + str(self.query.size() + nIns)).Select()
            xl.Selection.NumberFormat = '@'
            xl.Selection.Value = str(scd[j]) + '/' + str(svd[j]) 

        ws.PageSetup.PrintTitleRows = "$8:$9"    # Для переноса малой шапки на следующие страницы

        os.chmod(inputFile, stat.S_IWRITE) # снять read-only

        return u"Отчет успешно сформирован!"     










        
        
        
        
        
    def pushButton1_Click(self):
                
        currYear = self.dateEdit.date().year()
        ALF = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
                        
        try:
            xl = Dispatch('Excel.Application')
        except:
            return u"Не запускается Excel"
                    
        name_file = u'График ППР и аттестации.xlsx'
        inputFile = os.getcwd() + u'/' + path_rpt + name_file  # Шаблон
        
        if not os.path.exists(inputFile):        
            inputFile = os.getcwd() + u'/' + name_file  # Шаблон        
        
        try:
            # установить на шаблон read-only на время формирования отчета 
            os.chmod(inputFile, stat.S_IREAD)
        except:    
            QMessageBox.warning(self, u"Предупреждение", u"Отсутствует шаблон: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(self, u"Предупреждение", u"Не открывается файл: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
  
        xl.Visible = True
                
        ws = wb.Worksheets(1)
        
        nIns = 10  # № строки в шаблоне, откуда начинается вставка перечня средств 
        nTitle = 6
        row = ws.Rows(str(nIns + 1))                    
        
        ws.Cells(nTitle - 2, 1).Value += u" " + str(self.dateEdit.date().year()) + u" г."
        ws.Cells(nTitle - 2, 11).Value += u" " + str(self.dateEdit.date().year()) + u" г."
        
        ws.Cells(nTitle, 1).Value += u" " + str(self.dateEdit.date().year()) + u" год"
        ws.Cells(nTitle + 1, 1).Value += u" " + str(self.dateEdit.text()) + u" г."
        
                
        SQL = u"""
select *
from
(
  select t3.id, name_group || ' ' || name_msr as name, zav_num, period, period_view
  from group_msr t1, msr t2, zav_msr t3, type_msr t4
  where t1.id = t2.id_group
  and t2.id = t3.id_msr
  and t1.id_type = t4.id
  and t4.id_category = 3
  order by zav_num 
) t0
LEFT OUTER JOIN
(
  select id_zav, max(checking_date), max(view_date),
         EXTRACT(YEAR FROM max(checking_date)) year_checking, EXTRACT(MONTH FROM max(checking_date)) month_checking,
         EXTRACT(YEAR FROM max(view_date)) year_view, EXTRACT(MONTH FROM max(view_date)) month_view
  from journal_checking group by id_zav
) t5 on (t0.id = t5.id_zav)
"""        

        # print SQL

        self.query.prepare(SQL)            
        self.query.exec_()
        if self.query.lastError().isValid():
            #return u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса к БД1", QMessageBox.Ok)
            # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            return

        xl.Visible = False
        for i in range(self.query.size() + 1):
            row.Insert()
        xl.Visible = True
 
 
        M = range(self.query.size())       
        
        self.query.first()
        # Суммарные списки
        scd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
        svd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
        for i in range(0, self.query.size()):
            cd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
            vd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]             
            m  = range(12)

            period_checking = 0
            if self.query.record().value("period").toString() != '':
                period_checking = int(self.query.record().value("period").toString())
            period_view = 0
            if self.query.record().value("period_view").toString() != '':
                period_view = int(self.query.record().value("period_view").toString())
                
            max_year_checking = 0
            if self.query.record().value("year_checking").toString() != '':
                max_year_checking = int(self.query.record().value("year_checking").toString())
            max_month_checking = 0
            if self.query.record().value("month_checking").toString() != '':
                max_month_checking = int(self.query.record().value("month_checking").toString())
                
            max_year_view = 0
            if self.query.record().value("year_view").toString() != '':
                max_year_view = int(self.query.record().value("year_view").toString())
            max_month_view = 0
            if self.query.record().value("month_view").toString() != '':
                max_month_view = int(self.query.record().value("month_view").toString())
                

# П О В Е Р К А

            SQL = u"""
select checking_date, EXTRACT(YEAR FROM checking_date) year_checking, EXTRACT(MONTH FROM checking_date) month_checking
from journal_checking where id_zav =  """ + self.query.record().value("id").toString() + u""" and checking_date is not null order by checking_date
"""        
            # print SQL
        
            self.query_2.prepare(SQL)            
            self.query_2.exec_()
            if self.query_2.lastError().isValid():
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса к БД1", QMessageBox.Ok)
                # print u"Ошибка запроса к БД1" + chr(10) + str(self.query_2.lastError().text())
                return

            # Формирование выполненых поверок
            self.query_2.first()
            for j in range(self.query_2.size()):
                year = int(self.query_2.record().value("year_checking").toString())  
                month = int(self.query_2.record().value("month_checking").toString())  
                
                if year == currYear:
                    # print '***', year, month
                    cd[month - 1] = 1
                
                self.query_2.next()                

            # Формирование предстоящих поверок
            if period_checking != 0:
                months_ = (max_year_checking * 12) + max_month_checking            
                while True:
                    months_ = months_ + period_checking
                    year_ = months_ // 12 
                    month_ = months_ % 12
                    if month_ == 0:
                        year_ = year_ - 1
                        month_ = 12 
                    if year_ < currYear:
                        continue 
                    if year_ == currYear:
                        cd[month_ - 1] = 2
                    if year_ > currYear:
                        break 


# О С М О Т Р

            SQL = u"""
select view_date, EXTRACT(YEAR FROM view_date) year_view, EXTRACT(MONTH FROM view_date) month_view 
from journal_checking where id_zav = """ + self.query.record().value("id").toString() + u""" and view_date is not null order by view_date
"""        

            self.query_2.prepare(SQL)            
            self.query_2.exec_()
            if self.query_2.lastError().isValid():
                #return u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
                QMessageBox.warning(self, u"Предупреждение", u"Ошибка запроса к БД1", QMessageBox.Ok)
                # print u"Ошибка запроса к БД1" + chr(10) + str(self.query_2.lastError().text())
                return


            # Формирование выполненых осмотров
            self.query_2.first()
            for j in range(self.query_2.size()):
                year = int(self.query_2.record().value("year_view").toString())  
                month = int(self.query_2.record().value("month_view").toString())  
 
                if year == currYear:
                    vd[month - 1] = 1
                    
                self.query_2.next()                


            # Формирование предстоящих осмотров
            if period_view != 0:
                months_ = (max_year_view * 12) + max_month_view            
                while True:
                    months_ = months_ + period_view
                    year_ = months_ // 12 
                    month_ = months_ % 12
                    if month_ == 0:
                        year_ = year_ - 1
                        month_ = 12 
                    if year_ < currYear:
                        continue 
                    if year_ == currYear:
                        vd[month_ - 1] = 2
                    if year_ > currYear:
                        break 
                      
            for j in range(12):                
                m[j] = ''
                if cd[j] == 1:
                    m[j] = u'а'
                    scd[j] += 1
                if cd[j] == 2:
                    m[j] = u'А'
                    scd[j] += 1
                    
                if vd[j] == 1:
                    m[j] = u'п'
                    svd[j] += 1
                if vd[j] == 2:
                    m[j] = u'П'
                    svd[j] += 1
                
                                         
                if cd[j] == 1 and vd[j] == 1:
                    m[j] = u'а/п'
                if cd[j] == 1 and vd[j] == 2:
                    m[j] = u'а/П'
                if cd[j] == 2 and vd[j] == 1:
                    m[j] = u'А/п'
                if cd[j] == 2 and vd[j] == 2:
                    m[j] = u'А/П'
                
            # Заполняем пустые строки
            currN = nIns + i   # № текущей строки

            # Заполняем массив M данными
            M[i]=range(16)
            for j in range(16):
                M[i][j] = ''
            
            M[i][0] = i + 1
            M[i][1] = self.query.record().value("name").toString()
            M[i][2] = self.query.record().value("zav_num").toString()
            

            for j in range(12):
              M[i][j + 3] = m[j]
            
                                                 
            self.query.next()
            if self.query.lastError().isValid():
                print(u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text()))


        ws.Range("A" + str(nIns) + ":P" + str(self.query.size() + nIns)).Select()
        xl.Selection.Borders(1).LineStyle = 1
        xl.Selection.Borders(2).LineStyle = 1
        xl.Selection.Borders(3).LineStyle = 1
        xl.Selection.Borders(4).LineStyle = 1

        for c in (0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.VerticalAlignment = 2

        ws.Range(ALF[2] + str(nIns) + ":" + ALF[2] + str(self.query.size() + nIns)).Select()
        xl.Selection.NumberFormat = "@"

        for c in (1, 2, 15):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.HorizontalAlignment = 2
            xl.Selection.VerticalAlignment = 1
            
        for c in range(16):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns)).Select()
            xl.Selection.WrapText = True
                                        
        ws.Range("A" + str(nIns) + ":P" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Value = M
        
        ws.Range('B' + str(self.query.size() + nIns) + ":B" + str(self.query.size() + nIns)).Select()
        xl.Selection.Value = u'Всего: (аттестация/ППР)' 
        xl.Selection.Font.bold = True
        for j in range(12):
            ws.Range(ALF[j + 3] + str(self.query.size() + nIns) + ":" + ALF[j + 3] + str(self.query.size() + nIns)).Select()
            xl.Selection.NumberFormat = '@'
            xl.Selection.Value = str(scd[j]) + '/' + str(svd[j]) 

        ws.PageSetup.PrintTitleRows = "$8:$9"    # Для переноса малой шапки на следующие страницы

        os.chmod(inputFile, stat.S_IWRITE) # снять read-only
        
        return u"Отчет успешно сформирован!"     







# Отчет 'График поверки измерительного инструмента'
class GraphTestMsr(QDialog):
    def __init__(self, env, *args):
        QDialog.__init__(self, *args)
                       
        global db1
        db1 = env.db
        
        global path_ui                    
        path_ui = env.config.paths.ui + "/"
        global path_rpt                    
        path_rpt = env.config.paths.rpt + "/"
        if not JournalMsr.MyLoadUi(path_ui, "ReportGraphTestMsr.ui", self):
            return
                                                                   
        self.pushButton.clicked.connect(self.pushButton1_Click)
        
        self.query = QSqlQuery(db1)
        self.query1 = QSqlQuery(db1)
        self.query2 = QSqlQuery(db1)

        SQL = u"""
                 SELECT 1 AS srt, -1 AS id, 'По всем видам измерения' AS name_type
                 UNION ALL
                 SELECT 2 AS srt, id, '    ' || name_type AS name_type FROM type_msr
                 WHERE id_category = 1
                 UNION ALL
                 SELECT 3 AS srt, -2 AS id, 'По всем видам защиты' AS name_type
                 UNION ALL
                 SELECT 4 AS srt, id, '    ' || name_type AS name_type FROM type_msr
                 WHERE id_category = 2
                 UNION ALL
                 SELECT 5 AS srt, -3 AS id, 'По всем видам испытательного оборудования' AS name_type
                 UNION ALL
                 SELECT 6 AS srt, id, '    ' || name_type AS name_type FROM type_msr
                 WHERE id_category = 3
                 ORDER BY srt, name_type
               """
                                           
        self.query.prepare(SQL)
        self.query.exec_()
        
        self.comboBox.clear()
        for i in range(0, self.query.size()):
            self.query.next()
            self.comboBox.addItem(self.query.record().value(2).toString(), self.query.record().value(1).toString())
            
        self.spinBox.setValue(datetime.date.today().year)
        
        self.dateEdit.setDate(datetime.date.today())                        
        self.radioButton.toggled.connect(self.radioButton_Toggle)

                        
    def radioButton_Toggle(self, check):
        self.spinBox.setEnabled(check)    
        self.dateEdit.setEnabled(not check)                            

        
    def pushButton1_Click(self):
        ALF = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')        
        try:
            xl = Dispatch('Excel.Application')
        except:
            return u"Не запускается Excel"
                    
        name_file = u'График поверки средств измерения.xls'
        inputFile = os.getcwd() + u'/' + path_rpt + name_file  # Шаблон
        
        if not os.path.exists(inputFile):        
            inputFile = os.getcwd() + u'/' + name_file  # Шаблон        
        
        try:
            # установить на шаблон read-only на время формирования отчета 
            os.chmod(inputFile, stat.S_IREAD)
        except:    
            QMessageBox.warning(self, u"Предупреждение", u"Отсутствует шаблон: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(self, u"Предупреждение", u"Не открывается файл: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
  
        xl.Visible = True
                
        ws = wb.Worksheets(1)

        nIns = 15  # № строки в шаблоне, откуда начинается вставка перечня средств 
        nTitle = 10
        if self.checkBox.isChecked():
            ws.Rows("15:24").Delete()
            ws.Rows("1:8").Delete()
            nTitle = 2
            nIns = 7 
        row = ws.Rows(str(nIns + 1))
                        
        if self.radioButton.isChecked():
            strDate = str(self.spinBox.text()) + "-12-31"
            ws.Cells(nTitle, 1).Value += " " + str(self.spinBox.text()) + u" год"
        else:    
            strDate = self.dateEdit.date().toString("yyyy-MM-dd")
            ws.Cells(nTitle, 1).Value += " " + str(self.dateEdit.text()) + u" г."
            
        currInd = self.comboBox.itemData(self.comboBox.currentIndex()).toString()
        
        if str(currInd) in ["-1","-2","-3"]:
            id_category = -1 * int(currInd)
            strType = "AND t5.id_category = " + str(id_category)
            ws.Cells(nTitle + 1, 1).Value = self.comboBox.currentText()
                        
        else:            
            SQL = u"""
                   SELECT id_category FROM type_msr
                   WHERE id = """ + str(self.comboBox.itemData(self.comboBox.currentIndex()).toString())
            
            self.query.prepare(SQL)
            self.query.exec_()
            self.query.next()
            id_category = int(self.query.record().value(0).toString())
                                                    
            strType = "AND t4.id_type = " + str(currInd)
            ws.Cells(nTitle + 1, 1).Value += " " + self.comboBox.currentText()
         
        SQL = """
SELECT id, id_msr, name_group, name_msr, zav_num, period, period_view, first_checking, start_date, finish_date, last_checking_date, last_view_date, name_firm,
to_char(last_checking_date + period * '1 month'::INTERVAL - '1 day'::INTERVAL, 'dd.mm.yyyy') as checking_date

FROM
(
SELECT t1.id, t1.id_msr, t1.zav_num, t1.first_checking, t1.start_date, t1.finish_date, t5.id_category,
t2.checking_date,
t3.name_msr, t3.period, t3.period_view,
t4.name_group, name_firm,
CASE WHEN (t2.checking_date IS NULL) THEN t1.first_checking ELSE t2.checking_date END AS last_checking_date,
CASE WHEN (t2.view_date IS NULL) THEN t1.first_checking ELSE t2.view_date END AS last_view_date,

AGE(timestamp '""" + strDate + """', CASE WHEN (t2.checking_date IS NULL) THEN t1.first_checking ELSE t2.checking_date END) AS period_age,
AGE(timestamp '""" + strDate + """', CASE WHEN (t2.view_date IS NULL) THEN t1.first_checking ELSE t2.view_date END) AS view_period_age

FROM
zav_msr t1 LEFT OUTER JOIN 
(
  select a.*, b.name_firm from
  (
    select MAX(id) id, id_zav, MAX(checking_date) AS checking_date, MAX(view_date) AS view_date   --, firms_repair_msr
    FROM journal_checking GROUP BY id_zav   --, firms_repair_msr
  ) a,
  (
    SELECT c.id, c.firms_repair_msr, d.name_firm 
    FROM journal_checking c LEFT OUTER JOIN firms_repair_msr d ON (c.firms_repair_msr = d.id)
  ) b
  where a.id = b.id    
) t2
ON (t1.id = t2.id_zav),
msr t3,
group_msr t4,
type_msr t5
WHERE t1.id_msr = t3.id
AND t3.id_group = t4.id """ + strType + """
AND t4.id_type = t5.id
AND finish_date IS NULL
AND t1.reserve_date IS NULL
) AS t
WHERE
(
  t.id_category = 1 and
  (last_checking_date IS NULL OR 12 * EXTRACT(YEAR FROM period_age) + EXTRACT(MONTH FROM period_age) > period - 1)
) OR
(
  t.id_category = 2 and
  (
    (last_checking_date IS NULL OR 12 * EXTRACT(YEAR FROM period_age) + EXTRACT(MONTH FROM period_age) > period - 1) or
    (last_view_date IS NULL OR 12 * EXTRACT(YEAR FROM view_period_age) + EXTRACT(MONTH FROM view_period_age) > period_view - 1)
  )
) OR
(
  t.id_category = 3 and
  (
    (last_checking_date IS NULL OR 12 * EXTRACT(YEAR FROM period_age) + EXTRACT(MONTH FROM period_age) > period - 1) or
    (last_view_date IS NULL OR 12 * EXTRACT(YEAR FROM view_period_age) + EXTRACT(MONTH FROM view_period_age) > period_view - 1)
  )
)
ORDER BY zav_num
"""
        

        self.query.prepare(SQL)            
        self.query.exec_()
        if self.query.lastError().isValid():
            # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            return
 
#        QMessageBox.warning(self, u"Предупреждение", u"3", QMessageBox.Ok)
 
        M = range(self.query.size())       
        
        self.query.first()            
        for i in range(0, self.query.size()):
            # Присоединяем к типу классы точности и диапазон измерения, выбранные из таблицы "accuracy_msr",
            # между которыми ставим "\n"                
            SQL = """
                  SELECT name_vid, classaccuracy, range_msr FROM accuracy_msr
                  WHERE id_msr = :id_msr                            
                  ORDER BY name_vid, classaccuracy, range_msr
                  """
            self.query1.prepare(SQL)
            self.query1.bindValue(':id_msr', self.query.record().value("id_msr").toString())
            self.query1.exec_()
            if self.query1.lastError().isValid():
                # print u"Ошибка запроса к БД" + chr(10) + str(self.query1.lastError().text())
                return
            name_vid = ""
            classaccuracy = ""
            range_msr = ""
            perenos = ""
            self.query1.first()            
            for j in range(0, self.query1.size()):
                if j != 0:
                    perenos = "\n"
                if self.query1.record().value("name_vid").toString() != "":
                    name_vid += "\n" + self.query1.record().value("name_vid").toString()
                if self.query1.record().value("classaccuracy").toString() != "":
                    classaccuracy += perenos + self.query1.record().value("classaccuracy").toString()
                if self.query1.record().value("range_msr").toString() != "":
                    range_msr += perenos + self.query1.record().value("range_msr").toString()
                self.query1.next()
                    
            # Добавляем пустые строки в шаблон                      
            row.Insert()     
     
            # Заполняем пустые строки
            currN = nIns + i   # № текущей строки
            sheet = xl.Worksheets.Item(1)
            
            # Заполняем массив M данными
#            M[i]=range(10)
            M[i]=range(9)
            M[i][0] = i + 1
            M[i][1] = self.query.record().value("name_group").toString() + " " + self.query.record().value("name_msr").toString() + name_vid
            M[i][2] = self.query.record().value("zav_num").toString()
            M[i][3] = classaccuracy
            M[i][4] = range_msr
            M[i][5] = self.query.record().value("period").toString()
            M[i][6] = self.query.record().value("last_checking_date").toString()
           
            M[i][7] = self.query.record().value("name_firm").toString()
            M[i][8] = self.query.record().value("checking_date").toString()
                                    
            self.query.next()
            if self.query.lastError().isValid():
                print(u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text()))


#        QMessageBox.warning(self, u"Предупреждение", u"4", QMessageBox.Ok)

        ws.Range("A" + str(nIns) + ":J" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Borders(1).LineStyle = 1
        xl.Selection.Borders(2).LineStyle = 1
        xl.Selection.Borders(3).LineStyle = 1
        xl.Selection.Borders(4).LineStyle = 1

        ws.Range(ALF[2] + str(nIns) + ":" + ALF[2] + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.NumberFormat = '@'

        ws.Range(ALF[0] + str(nIns) + ":" + ALF[7] + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.HorizontalAlignment = 2
        xl.Selection.VerticalAlignment = 1
        xl.Selection.WrapText = True
        
        for c in (0, 3, 5, 6, 8):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.HorizontalAlignment = 3
            xl.Selection.VerticalAlignment = 2
        
        if self.query.size() > 3:
            ws.Range(ALF[9] + str(nIns) + ":" + ALF[9] + str(self.query.size() + nIns - 1)).Select()
        else:    
            ws.Range(ALF[9] + str(nIns) + ":" + ALF[9] + str(3 + nIns - 1)).Select()
            
            
        xl.Selection.Merge(False)
        xl.Selection.WrapText = True
        xl.Selection.HorizontalAlignment = 3
                
        ws.Range("A" + str(nIns) + ":I" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Value = M        
        ws.Range("A1").Select()

        # print 'id_category = ', id_category
        
        if self.checkBox.isChecked():
            ws.Columns(4).Delete()
            ws.Columns(6).Delete()
            ws.Columns(9).Delete()
            if id_category == 1:
                ws.Columns(8).Delete()
            ws.PageSetup.Orientation = 1
            QMessageBox.warning(self, u"Предупреждение", u"53", QMessageBox.Ok)

            ws.PageSetup.LeftMargin = 28
            ws.PageSetup.RightMargin = 28
            ws.PageSetup.BottomMargin = 42
            ws.PageSetup.PrintTitleRows = "$6:$6"    # Для переноса малой шапки на следующие страницы

            QMessageBox.warning(self, u"Предупреждение", u"54", QMessageBox.Ok)
            for i in range(1,5):
                ws.Cells(1, i).ColumnWidth = 0.85 * ws.Cells(1, i).ColumnWidth
            QMessageBox.warning(self, u"Предупреждение", u"55", QMessageBox.Ok)
        else:
            if id_category == 1:
                ws.Columns(9).Delete()
            ws.PageSetup.PrintTitleRows = "$14:$14"    # Для переноса малой шапки на следующие страницы

        os.chmod(inputFile, stat.S_IWRITE) # снять read-only

        return u"Отчет успешно сформирован!"     



    def calcDateCheck(self, speriod, sdate):
        # Гавнокод для расчета даты испытания. Думаю можно сделать все проще                        
#        speriod = str(self.query.record().value("period").toString())
#        sdate = str(self.query.record().value("last_checking_date").toString())
        if speriod != "" and sdate != "":
            period = int(speriod)                         
            mydate = datetime.datetime.strptime(sdate, "%Y-%m-%d")                        
            year, month, day, hour, minutes, sec, wday, yday, isdst = mydate.timetuple()
            nmonth = month + period
             
            y = year + nmonth / 12
            m = nmonth % 12
            if m == 0:
                m = 12
                y -= 1
            # Последний день месяца
            weekday_for_first_day, last_month_day = calendar.monthrange(y, m)
            if day > last_month_day:
                day = last_month_day                                    
                
            return  str(y) + "-" + str(m) + "-" + str(day)
#            return  str(day) + "." + str(m) + "." + str(y)
        else:
            return ""




# Отчет 'Местонахождение измерительного инструмента'
class LocationMsr(QDialog):
    def __init__(self, env, *args):
        QDialog.__init__(self, *args)
                       
        global db1
        db1 = env.db
        
        global path_ui                    
        path_ui = env.config.paths.ui + "/"
        global path_rpt                    
        path_rpt = env.config.paths.rpt + "/"
        if not JournalMsr.MyLoadUi(path_ui, "ReportLocationMsr.ui", self):
            return
                                                                   
        self.pushButton.clicked.connect(self.pushButton1_Click)
        
        self.query = QSqlQuery(db1)
        self.query1 = QSqlQuery(db1)
        self.query2 = QSqlQuery(db1)

        SQL = u"SELECT id, name_location FROM location_msr ORDER BY name_location"
                                           
        self.query.prepare(SQL)
        self.query.exec_()
        
        self.comboBox.clear()
        for i in range(0, self.query.size()):
            self.query.next()
            self.comboBox.addItem(self.query.record().value(1).toString(), self.query.record().value(0).toString())
            
        self.dateEdit.setDate(datetime.date.today())                        
    
        
    def pushButton1_Click(self):
        if self.label.isVisible():   
            self.reportLocation()
        else:    
            self.reportReserve()
    
    
    def reportLocation(self):
        ALF = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')        
        try:
            xl = Dispatch('Excel.Application')
        except:
            return u"Не запускается Excel"
                    
        name_file = u'Список СИ по месту нахождения-эксплуатации.xlsx'
        inputFile = os.getcwd() + u'/' + path_rpt + name_file  # Шаблон
        
        if not os.path.exists(inputFile):        
            inputFile = os.getcwd() + u'/' + name_file  # Шаблон        
        try:
            # установить на шаблон read-only на время формирования отчета 
            os.chmod(inputFile, stat.S_IREAD)
        except:    
            QMessageBox.warning(self, u"Предупреждение", u"Отсутствует шаблон: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(self, u"Предупреждение", u"Не открывается файл: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
  
        xl.Visible = True
                                
        ws = wb.Worksheets(1)
        
        nIns = 6  # № строки в шаблоне, откуда начинается вставка перечня средств 
        nTitle = 2
        ws.Cells(2, 1).Value += " " + self.comboBox.currentText()
        ws.Cells(3, 1).Value += " " + str(self.dateEdit.text()) + u" г."        
        
        row = ws.Rows(str(nIns + 1))

        currInd = self.comboBox.itemData(self.comboBox.currentIndex()).toString()

        SQL = """
SELECT t1.id, t1.id_msr, t4.name_group, t3.name_msr, t1.zav_num, t1.checking_date, reserve_date,
       sertificate, firms_repair_msr, t2.name_firm, t3.period
FROM
(
  select t1.*, t2.sertificate, t2.firms_repair_msr from
  (
    select t1.*, t2.checking_date from
    zav_msr t1 LEFT OUTER JOIN 
    (
      select id_zav, MAX(checking_date) AS checking_date
      FROM journal_checking GROUP BY id_zav
    ) t2
    ON (t1.id = t2.id_zav)
  ) t1 LEFT OUTER JOIN journal_checking t2
  ON (t1.id = t2.id_zav AND t1.checking_date = t2.checking_date)
) t1 LEFT OUTER JOIN firms_repair_msr t2
ON (t1.firms_repair_msr = t2.id),
msr t3,
group_msr t4,
type_msr t5
WHERE t1.id_msr = t3.id
AND t3.id_group = t4.id
AND t4.id_type = t5.id
AND t1.reserve_date IS NULL
AND t1.id in
(
SELECT t1.zav_msr FROM
(
SELECT MAX(date_move) AS date_move, zav_msr FROM history_location_msr
WHERE date_move <= TO_DATE('""" + self.dateEdit.date().toString("dd.MM.yyyy") + "','dd.mm.yyyy')" + """
GROUP BY zav_msr
) t1,
(
SELECT MAX(date_move) AS date_move, zav_msr FROM history_location_msr
WHERE location_msr = """ + str(currInd) + """
AND date_move <= TO_DATE('""" + self.dateEdit.date().toString("dd.MM.yyyy") + "','dd.mm.yyyy')" + """
GROUP BY zav_msr
) t2
WHERE t1.date_move = t2.date_move
AND t1.zav_msr = t2.zav_msr
)

ORDER BY zav_num
"""

        #
        # print 'self.dateEdit.date()=', self.dateEdit.date()
        #
        # print SQL
        self.query.prepare(SQL)            
        self.query.exec_()
        if self.query.lastError().isValid():
            # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            return
 
        if self.query.size() < 1:
            QMessageBox.warning(self, u"Предупреждение", u"Нет данных на дату: " + self.dateEdit.text(), QMessageBox.Ok)
            return
  
        M = range(self.query.size())       
        
        self.query.first()            
        for i in range(0, self.query.size()):
            
            # Присоединяем к типу классы точности и диапазон измерения, выбранные из таблицы "accuracy_msr",
            # между которыми ставим "\n"                
            SQL = """
                  SELECT name_vid, classaccuracy, range_msr FROM accuracy_msr
                  WHERE id_msr = :id_msr                            
                  ORDER BY name_vid, classaccuracy, range_msr
                  """
            self.query1.prepare(SQL)
            self.query1.bindValue(':id_msr', self.query.record().value("id_msr").toString())
            self.query1.exec_()
            if self.query1.lastError().isValid():
                # print u"Ошибка запроса к БД" + chr(10) + str(self.query1.lastError().text())
                return
            name_vid = ""
            classaccuracy = ""
            range_msr = ""
            perenos = ""
            self.query1.first()            
            for j in range(0, self.query1.size()):
                if j != 0:
                    perenos = "\n"
                if self.query1.record().value("name_vid").toString() != "":
                    name_vid += "\n" + self.query1.record().value("name_vid").toString()
                if self.query1.record().value("classaccuracy").toString() != "":
                    classaccuracy += perenos + self.query1.record().value("classaccuracy").toString()
                if self.query1.record().value("range_msr").toString() != "":
                    range_msr += perenos + self.query1.record().value("range_msr").toString()
                self.query1.next()
            
            # Заполняем массив M данными
            M[i]=range(7)
            M[i][0] = i + 1
            M[i][1] = self.query.record().value("name_group").toString() + " " + self.query.record().value("name_msr").toString() + name_vid
            M[i][2] = self.query.record().value("zav_num").toString()
            M[i][3] = self.query.record().value("checking_date").toString()
            M[i][4] = self.query.record().value("sertificate").toString()
            M[i][5] = self.query.record().value("name_firm").toString()
            M[i][6] = self.calcDateCheck(str(self.query.record().value("period").toString()), str(self.query.record().value("checking_date").toString()))

            self.query.next()
            if self.query.lastError().isValid():
                pass
                # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())

        ws.Range("A" + str(nIns) + ":G" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Borders(1).LineStyle = 1
        xl.Selection.Borders(2).LineStyle = 1
        xl.Selection.Borders(3).LineStyle = 1
        xl.Selection.Borders(4).LineStyle = 1

        for c in (2, 4):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.NumberFormat = '@'
        
        for c in (0, 1, 2, 3, 4, 5, 6):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.VerticalAlignment = 2

        for c in (0, 3, 6):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.HorizontalAlignment = 3

        for c in (1, 2, 4, 5):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.HorizontalAlignment = 1

        ws.Range("A" + str(nIns) + ":G" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Value = M        
        ws.Range("A1").Select()

        ws.PageSetup.PrintTitleRows = "$5:$5"    # Для переноса малой шапки на следующие страницы
        os.chmod(inputFile, stat.S_IWRITE) # снять read-only
        return u"Отчет успешно сформирован!"     


    def reportReserve(self):
        ALF = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')        
        try:
            xl = Dispatch('Excel.Application')
        except:
            return u"Не запускается Excel"
                    
        name_file = u'СИ, находящиеся в резерве-консервации.xlsx'
        inputFile = os.getcwd() + u'/' + path_rpt + name_file  # Шаблон
        
        if not os.path.exists(inputFile):        
            inputFile = os.getcwd() + u'/' + name_file  # Шаблон        
        try:
            # установить на шаблон read-only на время формирования отчета 
            os.chmod(inputFile, stat.S_IREAD)
        except:    
            QMessageBox.warning(self, u"Предупреждение", u"Отсутствует шаблон: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
        try:
            wb = xl.Workbooks.Open(inputFile)
        except:
            QMessageBox.warning(self, u"Предупреждение", u"Не открывается файл: " + inputFile + u".\nПродолжение невозможно!", QMessageBox.Ok)
            return
  
        xl.Visible = True
                                
        ws = wb.Worksheets(1)
        
        nIns = 6  # № строки в шаблоне, откуда начинается вставка перечня средств 
        nTitle = 2
        ws.Cells(nTitle, 1).Value += " " + str(self.dateEdit.text()) + u" г."
        row = ws.Rows(str(nIns + 1))
            
        SQL = """
SELECT t1.id, t1.id_msr, t4.name_group, t3.name_msr, t1.zav_num, checking_date, reserve_date, t3.period
FROM
--zav_msr t1,
zav_msr t1 LEFT OUTER JOIN 
(
  select id_zav, MAX(checking_date) AS checking_date, MAX(view_date) AS view_date 
  FROM journal_checking GROUP BY id_zav
) t2
ON (t1.id = t2.id_zav),
msr t3,
group_msr t4,
type_msr t5
WHERE t1.id_msr = t3.id
AND t3.id_group = t4.id
AND t4.id_type = t5.id
--AND finish_date IS NULL
AND reserve_date IS NOT NULL
AND reserve_date <= :reserve_date
ORDER BY zav_num
"""

        # print 'self.dateEdit.date()=', self.dateEdit.date()

        self.query.prepare(SQL)            
        self.query.bindValue(":reserve_date", self.dateEdit.date())
        self.query.exec_()
        if self.query.lastError().isValid():
            # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())
            return
 
        if self.query.size() < 1:
            QMessageBox.warning(self, u"Предупреждение", u"Нет данных на дату: " + self.dateEdit.text(), QMessageBox.Ok)
            return
  
        M = range(self.query.size())       
        
        self.query.first()            
        for i in range(0, self.query.size()):
            # Присоединяем к типу классы точности и диапазон измерения, выбранные из таблицы "accuracy_msr",
            # между которыми ставим "\n"                
            SQL = """
                  SELECT name_vid, classaccuracy, range_msr FROM accuracy_msr
                  WHERE id_msr = :id_msr                            
                  ORDER BY name_vid, classaccuracy, range_msr
                  """
            self.query1.prepare(SQL)
            self.query1.bindValue(':id_msr', self.query.record().value("id_msr").toString())
            self.query1.exec_()
            if self.query1.lastError().isValid():
                # print u"Ошибка запроса к БД" + chr(10) + str(self.query1.lastError().text())
                return
            name_vid = ""
            classaccuracy = ""
            range_msr = ""
            perenos = ""
            self.query1.first()            
            for j in range(0, self.query1.size()):
                if j != 0:
                    perenos = "\n"
                if self.query1.record().value("name_vid").toString() != "":
                    name_vid += "\n" + self.query1.record().value("name_vid").toString()
                if self.query1.record().value("classaccuracy").toString() != "":
                    classaccuracy += perenos + self.query1.record().value("classaccuracy").toString()
                if self.query1.record().value("range_msr").toString() != "":
                    range_msr += perenos + self.query1.record().value("range_msr").toString()
                self.query1.next()
            
            # Заполняем массив M данными
            M[i]=range(7)
            M[i][0] = i + 1
            M[i][1] = self.query.record().value("name_group").toString() + " " + self.query.record().value("name_msr").toString() + name_vid
            M[i][2] = self.query.record().value("zav_num").toString()
            M[i][3] = classaccuracy
            M[i][4] = range_msr
            M[i][5] = self.calcDateCheck(str(self.query.record().value("period").toString()), str(self.query.record().value("checking_date").toString()))
            M[i][6] = self.query.record().value("reserve_date").toString()

            self.query.next()
            if self.query.lastError().isValid():
                pass
                # print u"Ошибка запроса к БД1" + chr(10) + str(self.query.lastError().text())

        ws.Range("A" + str(nIns) + ":G" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Borders(1).LineStyle = 1
        xl.Selection.Borders(2).LineStyle = 1
        xl.Selection.Borders(3).LineStyle = 1
        xl.Selection.Borders(4).LineStyle = 1

        for c in (2, 3, 4):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.NumberFormat = '@'
        
        for c in (0, 1, 2, 3, 4, 5, 6):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.VerticalAlignment = 2

        for c in (0, 5, 6):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.HorizontalAlignment = 3

        for c in (1, 2, 3, 4):
            ws.Range(ALF[c] + str(nIns) + ":" + ALF[c] + str(self.query.size() + nIns - 1)).Select()
            xl.Selection.HorizontalAlignment = 1

        ws.Range("A" + str(nIns) + ":G" + str(self.query.size() + nIns - 1)).Select()
        xl.Selection.Value = M        
        ws.Range("A1").Select()

        ws.PageSetup.PrintTitleRows = "$5:$5"    # Для переноса малой шапки на следующие страницы
        os.chmod(inputFile, stat.S_IWRITE) # снять read-only
        return u"Отчет успешно сформирован!"     


    def calcDateCheck(self, speriod, sdate):
        # Гавнокод для расчета даты испытания. Думаю можно сделать все проще                        
#        speriod = str(self.query.record().value("period").toString())
#        sdate = str(self.query.record().value("last_checking_date").toString())
        if speriod != "" and sdate != "":
            period = int(speriod)                         
            mydate = datetime.datetime.strptime(sdate, "%Y-%m-%d")                        
            year, month, day, hour, minutes, sec, wday, yday, isdst = mydate.timetuple()
            nmonth = month + period
             
            y = year + nmonth / 12
            m = nmonth % 12
            if m == 0:
                m = 12
                y -= 1
            # Последний день месяца
            weekday_for_first_day, last_month_day = calendar.monthrange(y, m)
            if day > last_month_day:
                day = last_month_day                                    
                
            return  str(y) + "-" + str(m) + "-" + str(day)
        else:
            return ""








# Для запуска модуля в автономном режиме
if __name__ == "__main__":
    
    import sys
    app = QtGui.QApplication(sys.argv)
    
    from dpframe.base.inits import db_connection_init   
    from dpframe.base.envapp import checkenv
    from dpframe.base.inits import json_config_init
    from dpframe.base.inits import db_connection_init
    from dpframe.base.inits import default_log_init
    from electrolab.gui.inits import serial_devices_init
   
    
    @serial_devices_init
    @json_config_init
    @db_connection_init
    @default_log_init    
    class ForEnv(QtGui.QWidget):
        def getEnv(self):
            return self.env
    objEnv = ForEnv()
    env = objEnv.getEnv()
    db = env.db
    path_ui = env.config.paths.ui + "/"

    import os
    if not os.path.exists(path_ui):        
        path_ui = ""

    rez = db.open();
    if not rez:
        QMessageBox.warning(None, u"Предупреждение",
u"""Не установлено соединение с БД со следующими параметрами:
host: """ + db.hostName() + """
database: """ + db.databaseName() + """
user: """ + db.userName() + """
password: """ + db.password(),
QMessageBox.Ok)
    else:
        wind = GraphTestMsr(env)
        wind.setEnabled(True)
        wind.show()
        sys.exit(app.exec_())
    
