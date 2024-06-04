# -*- coding: utf-8 -*-
# Формирование счета для ЦСМ в Exel
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel, QSqlQuery, QSqlDatabase
import datetime
import os, stat, wmi
from win32com.client import Dispatch
#import Tkinter, tkFileDialog

class WinCSM(QtGui.QDialog):
    def __init__(self, db, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.query = QSqlQuery(db)
        self.query1 = QSqlQuery(db)
        self.query2 = QSqlQuery(db)

        self.db = db

        self.setWindowTitle(u'Счет для ЦСМ')

        self.label1 = QtGui.QLabel(u'Дата')
        self.label2 = QtGui.QLabel(u'Поверитель')
        self.label3 = QtGui.QLabel(u'Путь выгрузки в Excel')
        self.label4 = QtGui.QLabel(u'Имя файла')
        self.label5 = QtGui.QLabel(u'')
        self.label1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label5.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.date1 = QtGui.QDateEdit()
        self.date1.setFixedWidth(100)
        self.date1.setCalendarPopup(1)
                                
        self.combo1 = QtGui.QComboBox()
        self.combo1.setFixedWidth(250)
        self.text1 = QtGui.QLineEdit()
        self.text1.setText("C:/")
        self.text2 = QtGui.QLineEdit()
                
        self.button4 = QtGui.QPushButton("...")
        self.button4.setFixedWidth(30)
        self.filedialog1 = QtGui.QFileDialog()                
        self.button1 = QtGui.QPushButton(u"Расценки")        
        self.button1.setVisible(False)   # Прячем кнопку "Расценки", временно
        self.button2 = QtGui.QPushButton(u"Выгрузить")
        self.button3 = QtGui.QPushButton(u"Закрыть")
        self.button2.setFixedWidth(100)
        self.button3.setFixedWidth(100)
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.label1,  0, 0)
        grid.addWidget(self.date1,   0, 1, 1, 2)
        grid.addWidget(self.label2,  1, 0)
        grid.addWidget(self.combo1,  1, 1, 1, 2)
        grid.addWidget(self.label3,  2, 0)
        grid.addWidget(self.text1,   2, 1)
        grid.addWidget(self.button4, 2, 2)
        grid.addWidget(self.label4,  3, 0)
        grid.addWidget(self.text2,   3, 1, 1, 2)
        grid.addWidget(self.button1, 4, 0)
        grid.addWidget(self.button2, 5, 0)
        grid.addWidget(self.button3, 5, 1)
        grid.addWidget(self.label5,  6, 0, 1, 3)
        self.setLayout(grid)

        
        self.connect(self.date1, QtCore.SIGNAL("dateChanged(QDate)"), self.on_dateChanged1)              
        self.connect(self.combo1, QtCore.SIGNAL("currentIndexChanged(QString)"), self.on_comboChanged1)              
        self.connect(self.text1, QtCore.SIGNAL("textChanged(QString)"), self.on_comboChanged1)              
        self.connect(self.button2, QtCore.SIGNAL("clicked()"), self.on_clicked2)              
        self.connect(self.button3, QtCore.SIGNAL("clicked()"), self.on_clicked3)              
        self.connect(self.button4, QtCore.SIGNAL("clicked()"), self.on_clicked4)
        self.date1.setDate(datetime.date.today())
#        self.date1.setDate(datetime.date(2012, 05, 18))   # для отладки
        
    # Формируем имя файла
    def on_comboChanged1(self):
        self.text2.setText(u"Счет ЦСМ от " + self.date1.text() + " (" + self.combo1.currentText() + ").xls")    

        if self.text1.text()[self.text1.text().length() - 1] == "/":
            self.outputFile = unicode(self.text1.text() + self.text2.text())
        else:    
            self.outputFile = unicode(self.text1.text() + "/" + self.text2.text())
#        print self.outputFile
        
            
    # Загоняем поверителей в combobox
    def on_dateChanged1(self):
        sql = u"""
                 SELECT DISTINCT t1.id, t1.fio
                 FROM 
                 (
                   SELECT id, fio FROM operator
                   UNION
                   SELECT 0, 'без поверителя'
                 ) t1,
                 (
                   SELECT CASE WHEN (supervisor IS NULL) THEN 0 ELSE supervisor END AS supervisor
                   FROM test_map
                   WHERE CAST(createdatetime AS DATE)=:createdate
                 ) t2
                 WHERE t1.id = t2.supervisor
                 ORDER BY t1.fio"""
                                           
        self.query.prepare(sql)
        self.query.bindValue(':createdate', self.date1.date())
        self.query.exec_()
        
        self.combo1.clear()
        for i in range(0, self.query.size()):
            self.query.next()
            self.combo1.addItem(self.query.record().value(1).toString(), self.query.record().value(0).toString())
        if self.query.size() > 0:                
            self.combo1.addItem(u'ПО ВСЕМ ПОВЕРИТЕЛЯМ', '-1')            
        self.text2.setText(u"Счет ЦСМ от " + self.date1.text() + " (" + self.combo1.currentText() + ").xls")
            
        if self.query.lastError().isValid():
            raise Exception(self.query.lastError().text())
            
            
    # Формируем отчет в Excel
    def on_clicked2(self):        
        BuildAccount(True, self.db, self.date1.date(),
                     self.combo1.itemData(self.combo1.currentIndex()),
                     self.outputFile)
        
    # Закрываем окно
    def on_clicked3(self):
        self.close()
                
    # Выбираем путь
    def on_clicked4(self):
        #from electrolab.gui.msgbox import msgBox
        #msgBox(self, BeforeBuildAccount(self.db))
        #return
                
        from PyQt4.QtGui import QFileDialog
        self.text1.setText(QFileDialog.getExistingDirectory(None, "","C:\\",
        QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog))
        
        """        
        root = Tkinter.Tk()
        root.withdraw()
        dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title=u'Выберите папку и нажмите "OK"')
        self.text1.setText(dirname)
        """

# Функция BeforeBuildAccount расчитывает параметры: date, supervisor, outputFile для функции BuildAccount
# Задействована в рабочем месте испытателя
def BeforeBuildAccount(db):    
    query = QSqlQuery(db)
    
    strError = "Сбой при формировании счета для ЦСМ:" + chr(10)
    
    # Берем текущую дату
    date = datetime.date.today()
    #date = datetime.date(2012, 05, 18)   # для отладки
        
    # Выбираем первого попавшегося поверителя
    sql = """SELECT DISTINCT t1.id, t1.fio
             FROM operator t1, test_map t2
             WHERE t1.id = t2.supervisor
             AND CAST(createdatetime AS DATE)=:createdate
             ORDER BY t1.fio"""
                                           
    query.prepare(sql)
#    query.bindValue(':createdate', date.date())
    query.bindValue(':createdate', str(date))
    query.exec_()
    if query.lastError().isValid():
        return strError + u"Ошибка при запросе к БД" + chr(10) + str(query.lastError().text())
    query.next()
    if query.size() == 0:
        return strError + u"Нет данных для вывода, отсутствует поверитель"
    
    # Выбираем первый попавшийся съемный носитель
    c = wmi.WMI()
    i = 0
    for d in c.Win32_LogicalDisk(DriveType=2):                   
        i += 1
        disk = d.Name + "\\"
        break
    if i == 0:
        return strError + u"Вставьте, пожалуйста, флешку и повторите попытку"

    # Имя выходного файла
    outputFile = u"Счет ЦСМ от " + str(date) + " (" + unicode(query.record().value(1).toString()) + ").xls"
    
    return BuildAccount(False, db, str(date), query.record().value(0).toString(), disk + outputFile)



"""
Функция BuildAccount - формирует Счет для ЦСМ в формате Excel и сохраняет его на носителе
Параметры:
visibleExcel - определяет, отображается ли Excel во время формирования отчета
(True - отображается, False - не отображается)
db - база данных
date - дата, за которую выводится информация в счет
supervisor - код поверителя (-1 - по всем поверителям, 0 - без поверителя)
outputFile - выходной файл
"""
def BuildAccount(visibleExcel, db, date, supervisor, outputFile):
    query = QSqlQuery(db)
    query1 = QSqlQuery(db)
    query2 = QSqlQuery(db)
  #  print "BUILD..." + supervisor.toString()
        
    try:
        xl = Dispatch('Excel.Application')
    except:
        return u"Не запускается Excel"            
      
    xl.Visible = visibleExcel
    inputFile = os.getcwd() + u'\\rpt\\Счет ЦСМ.xls'  # Шаблон
#    inputFile = 'c:/1.xls'
    try:
        # установить на шаблон read-only на время формирования отчета 
        os.chmod(inputFile, stat.S_IREAD)
    except:    
        raise Exception(u"Отсутствует шаблон: " + inputFile)     
    try:
        wb = xl.Workbooks.Open(inputFile)
    except:
        raise Exception(u"Не открывается файл: " + inputFile)
                
    ws = wb.Worksheets(1)        
    nIns = 12  # № строки в шаблоне, откуда начинается вставка перечня трансформаторов 
    row = ws.Rows(str(nIns + 1))
        
    try:
        query.exec_("DROP TABLE temp_accountcsm")
    except:
        pass  

    sql = """
    CREATE TEMPORARY TABLE temp_accountcsm
    (
      type character varying(1000),
      quantity integer,
      quan_def integer,
      transformer integer
    )
    """
    query.exec_(sql)
    if query.lastError().isValid():
        raise Exception(u"Ошибка создания таблицы 'temp_accountcsm'" + chr(10) + str(query.lastError().text()))
#        raise Exception(query.lastError().text())
        
    sql = """
    SELECT t2.type || '-' || ROUND(t2.voltage) AS type, 
           t1.quantity, t1.quan_def, t1.transformer
    FROM
    (
        SELECT
        t1.supervisor, t3.transformer, count(*) AS quantity, count(t2.defect) AS quan_def
        FROM test_map t1, item t2, serial_number t3
        WHERE t1.id = t2.test_map
        AND t2.serial_number = t3.id
        AND CAST(t1.createdatetime AS DATE) = :createdate
    """
    if supervisor != -1:
        sql += """
        AND CASE WHEN (supervisor IS NULL) THEN 0 ELSE supervisor END = :supervisor
        """
    sql += """
    GROUP BY t1.supervisor, t3.transformer
    ) t1,
    transformer t2
    WHERE t1.transformer = t2.id
    ORDER BY t2.shortname
    """
    
    query.prepare(sql)
#    query.bindValue(':createdate', str(date))
    query.bindValue(':createdate', date)
    if supervisor != -1:
        query.bindValue(':supervisor', supervisor)
    query.exec_()
    if query.lastError().isValid():
        raise Exception(u"Ошибка запроса к БД1" + chr(10) + str(query.lastError().text()))
        
    query.first()            
    for i in range(0, query.size()):
        tip = unicode(query.record().value("type").toString())
        # Присоединяем к типу классы точности выбранные из таблицы "coil",
        # между которыми ставим "/"                
        sql = """
              SELECT classaccuracy FROM coil
              WHERE transformer = :transformer                            
              ORDER BY coilnumber
              """
        query1.prepare(sql)
        query1.bindValue(':transformer', query.record().value("transformer").toString())
        query1.exec_()
        if query1.lastError().isValid():
            return u"Ошибка запроса к БД" + chr(10) + str(query1.lastError().text())
        query1.first()            
        for j in range(0, query1.size()):
            if j == 0:
                tip = tip + " " + unicode(query1.record().value("classaccuracy").toString())
            else:    
                tip = tip + "/" + unicode(query1.record().value("classaccuracy").toString())
            query1.next()
        sql = """
        INSERT INTO temp_accountcsm (type, quantity, quan_def, transformer) VALUES
        (
          :type,
          :quantity,
          :quan_def,
          :transformer
        )
        """
        query2.prepare(sql)
        query2.bindValue(':type', tip)
        query2.bindValue(':quantity', query.record().value("quantity").toString())
        query2.bindValue(':quan_def', query.record().value("quan_def").toString())
        query2.bindValue(':transformer', query.record().value("transformer").toString())
        query2.exec_()
        if query2.lastError().isValid():
            return u"Ошибка запроса к БД2" + chr(10) + str(query2.lastError().text())
        query.next()

    sql = """
    SELECT type, sum(quantity) AS quantity, sum(quan_def) AS quan_def
    FROM temp_accountcsm
    GROUP BY type
    ORDER BY type
    """
            
    query.prepare(sql)
    query.exec_()
    if query.lastError().isValid():
        raise Exception(u"Ошибка запроса к БД3" + chr(10) + str(query.lastError().text()))
    
    # Добавляем пустые строки в шаблон                      
    for i in range(0, query.size() - 1):
        row.Insert()
     
    # Заполняем пустые строки
    query.first()            
    currN = nIns  # № текущей строки             
    for i in range(0, query.size()):           
        currN = nIns + i
        cell = ws.Cells(currN, 1)
        cell.Value = unicode(query.record().value("type").toString())
        cell = ws.Cells(currN, 2)
        cell.Value = unicode(query.record().value("quantity").toString())
        cell = ws.Cells(currN, 4)
        cell.Formula = "=B" + str(currN) + "*C" + str(currN)
        cell = ws.Cells(currN, 5)
        cell.Value = unicode(query.record().value("quan_defect").toString())
        cell = ws.Cells(currN, 6)
        cell.Value = unicode(query.record().value("transformer").toString())
        #cell.Value = unicode(self.query.record().value("fio").toString())
        query.next()

    # Вставляем формулы в итоговые ячейки                            
    cell = ws.Cells(currN + 1, 2)
    cell.SetValue("=SUM(B" + str(nIns) + ":B" + str(currN) + ")")    
    cell = ws.Cells(currN + 1, 4)
    cell.SetValue("=SUM(D" + str(nIns) + ":D" + str(currN) + ")")    
    cell = ws.Cells(currN + 1, 5)
    cell.SetValue("=SUM(E" + str(nIns) + ":E" + str(currN) + ")")    

    try:
        os.remove(outputFile)
    except:
        pass
                            
    try:
        wb.SaveAs(outputFile)
    except:
        raise Exception(u"Не сохраняется файл: " + outputFile)
    os.chmod(inputFile, stat.S_IWRITE) # снять read-only

    if not visibleExcel:
        xl.Quit()

#    return u"Счет для ЦСМ успешно сформирован в файле:" + chr(10) + outputFile     

            

# Для запуска модуля в автономном режиме
#===============================================================================
# if __name__ == "__main__":   
#    import sys
#    app = QtGui.QApplication(sys.argv)
#           
#    db = QSqlDatabase("QPSQL")
#    db.setHostName("localhost")
#    db.setDatabaseName("electrolab")
#    db.setUserName("electrolab")
#    db.setPassword("electrolab")
#    rez = db.open()
#    window = WinCSM(db)
#   
#    window.show()
#    sys.exit(app.exec_())
#===============================================================================
