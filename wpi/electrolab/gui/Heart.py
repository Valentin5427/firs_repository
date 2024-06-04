# -*- coding: UTF-8 -*-

'''
Created on 16.08.2013

@author: atol
'''

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt4.QtGui import QMessageBox, QIcon
#import ui.ico_64_rc
import ui.ico_64_rc
import os
import JournalMsr
import TestHeart

#QtGui.QTableView.

#from electrolab.gui.DigitalKeyboard import DigitalKeyboard
from electrolab.gui.DigitalKeyboard import DigitalKeyboard
#from DigitalKeyboard import DigitalKeyboard


selHeart = """SELECT t1.id, sizes, apc, vpc, pogr, weight_magnetic, dens,
in_diameter, out_diameter, height, in_length, in_height, depth, width, left_border, right_border, name_group, t1.id_group, t1.id_grade
FROM heart t1 LEFT OUTER JOIN group_heart t2 ON (t1.id_group = t2.id)
LEFT OUTER JOIN grade_iron t3 ON (t1.id_grade = t3.id)
WHERE 0=0\n"""
selHeart_2 = ""
selHeart_3 = "ORDER BY sizes "

model = QSqlQueryModel()

#tv = QtGui.QTableView()



withCol1 = 200
withCol2 = 50
withCol3 = 50
withCol4 = 50
withCol5 = 50
withCol6 = 50
withCol7 = 50
withCol8 = 50
withCol9 = 50
withCol10 = 50
withCol11 = 50
withCol12 = 50
withCol13 = 50
#26.10
withCol14 = 50
withCol15 = 50
withCol16 = 100



VSB1 = False

id_heart = ''
shapes = []
shape = -1

def noneValue(v):
    if v.trimmed() == '':
        return None
    else:
        return v.trimmed()

    
def nullValue(fild):
    if fild.isNull():
        return ''
    else:
        return fild.value().toString()
    
    
class MyFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
    def widthArea(self, tableView):
        # Возвращает ширину свободной области таблицы tableView
        HSWidth = tableView.verticalHeader().width() + 4
        if tableView.verticalScrollBar().width() < 100 and tableView.verticalScrollBar().isVisible():
            HSWidth += tableView.verticalScrollBar().width()
        return tableView.width() - HSWidth    
    def eventFilter(self, obj, e):
        
        try:
            QtCore.QEvent.Resize
        except:
            return True    
        global VSB1
        
        if obj.objectName() == 'tv1' and (e.type() == QtCore.QEvent.Resize or VSB1 <> obj.verticalScrollBar().isVisible()):        

            sw1 = 0
            sw2 = 0
            
            if shape in [-1, 1]:
                sw1 = withCol7 + withCol8 + withCol9
            if shape in [-1, 2]:
                sw2 = withCol10 + withCol11 + withCol12 + withCol13
            
#            print 'sw1, sw2', sw1, sw2

            sumWith = withCol1 + withCol2 + withCol3 + withCol4 + withCol5 + withCol6 + sw1 + sw2 + withCol14 + withCol15 + withCol16
   
            koef = (1.0 * (self.widthArea(obj)) / sumWith)
            obj.setColumnWidth(1, koef * withCol1)
            obj.setColumnWidth(2, koef * withCol2)
            obj.setColumnWidth(3, koef * withCol3)
            obj.setColumnWidth(4, koef * withCol4)
            obj.setColumnWidth(5, koef * withCol5)
            obj.setColumnWidth(6, koef * withCol6)
            
            obj.setColumnWidth(7, koef * withCol7)
            obj.setColumnWidth(8, koef * withCol8)
            obj.setColumnWidth(9, koef * withCol9)
            
            obj.setColumnWidth(10, koef * withCol10)
            obj.setColumnWidth(11, koef * withCol11)
            obj.setColumnWidth(12, koef * withCol12)
            obj.setColumnWidth(13, koef * withCol13)
            
            obj.setColumnWidth(14, koef * withCol14)
            
            obj.setColumnWidth(15, koef * withCol15)
            obj.setColumnWidth(16, koef * withCol16)
            VSB1 = obj.verticalScrollBar().isVisible()
                    
        return False
        
from dpframe.base.inits import json_config_init

@json_config_init
class Heart(QtGui.QDialog):
    def __init__(self, env):
        QtGui.QDialog.__init__(self)
                        
        global db1
        db1 = env.db
        global path_ui
        path_ui = env.config.paths.ui + "/"
        if not os.path.exists(path_ui):        
            path_ui = ""
        if not JournalMsr.MyLoadUi(path_ui, "heart.ui", self):
            self.is_show = False
            return

        self.id_h = ''

        self.pushButton.setIcon(QIcon(u':/ico/ico/plus_64.png'))
        self.pushButton_2.setIcon(QIcon(u':/ico/ico/trash_64.png'))
        self.pushButton_3.setIcon(QIcon(u':/ico/ico/pencil_64.png'))
        self.pushButton_6.setIcon(QIcon(u':/ico/ico/64_down.png'))
        self.pushButton_7.setIcon(QIcon(u':/ico/ico/up_64.png'))

        self.oDigitalKeyboard = DigitalKeyboard(self.env)
        self.oDigitalKeyboard.ui.btn_dot.setText('%')
        self.horizontalLayout_4.addWidget(self.oDigitalKeyboard)
        self.oDigitalKeyboard.setEnabled(True)
        self.lineEdit.installEventFilter(self)
        
        self.horizontalLayout_4.setEnabled(False)
        self.verticalLayout_3.setEnabled(False)
        

        # Корректировка размеров цифровой клавиатуры
        fnt = self.oDigitalKeyboard.ui.btn_0.font()
        fnt.setPointSize(fnt.pointSize() * 0.7)        
        fnt_dot = self.oDigitalKeyboard.ui.btn_0.font()
        fnt_dot.setPointSize(fnt.pointSize() * 0.65)        
        self.oDigitalKeyboard.ui.btn_0.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_1.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_2.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_3.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_4.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_5.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_6.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_7.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_8.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_9.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_dot.setFont(fnt_dot)
        
        self.oDigitalKeyboard.ui.btn_BackSpace.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_Clear.setFont(fnt)
        self.oDigitalKeyboard.ui.btn_Ok.setFont(fnt)        
        minWidth = self.oDigitalKeyboard.ui.btn_BackSpace.minimumWidth() * 0.7
        self.oDigitalKeyboard.ui.btn_BackSpace.setMinimumSize(minWidth, 0)
        self.oDigitalKeyboard.ui.btn_Clear.setMinimumSize(minWidth, 0)
        self.oDigitalKeyboard.ui.btn_Ok.setMinimumSize(minWidth, 0)


        SQL = u"""
                 SELECT -1 AS id, 'ПО ВСЕМ ГРУППАМ' AS name_group, -1 AS shape,  -1 AS srt
                 UNION ALL
                 SELECT id, name_group, shape, 1 AS srt FROM group_heart
                 UNION ALL
                 SELECT 0 AS id, 'БЕЗ ГРУППЫ' AS name_group, -2 AS shape,  2 AS srt
                 ORDER BY srt, name_group"""                                           
        query = QSqlQuery(db1)
        query.prepare(SQL)
        query.exec_()
        self.comboBox.clear()
        global shapes
        for i in range(0, query.size()):
            query.next()
            self.comboBox.addItem(query.record().value(1).toString(), query.record().value(0).toString())
            if int(query.record().value(2).toString()) <> -2:
                shapes += [int(query.record().value(2).toString())]
                                
        print 'shapes=', shapes
        self.comboBox.insertSeparator(1)
        self.comboBox.insertSeparator(self.comboBox.count() - 1)


        self.pushButton.clicked.connect(self.pushButton_Click)
        self.pushButton_2.clicked.connect(self.pushButton2_Click)
        self.pushButton_3.clicked.connect(self.pushButton3_Click)
        self.pushButton_4.clicked.connect(self.pushButton4_Click)
        self.pushButton_5.clicked.connect(self.pushButton5_Click)
        self.pushButton_6.clicked.connect(self.pushButton6_Click)
        self.pushButton_7.clicked.connect(self.pushButton7_Click)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)
        
        self.comboBox.currentIndexChanged.connect(self.lineEdit_textChanged)

        self.tableView.setModel(model)
        self.selModel = self.tableView.selectionModel()        
        self.connect(self.selModel, QtCore.SIGNAL("currentChanged(const QModelIndex &, const QModelIndex &)"), self.selectionChanged1)

        self.tableView.setObjectName('tv1')

        
        self.tableView.setHorizontalScrollBarPolicy(1)
        self.tableView.installEventFilter(MyFilter(self.tableView))
                
        self.ViewHeart(0)
        
        self.lineEdit.setFocus()
    
    def eventFilter(self, _object, _event):
        if _event.type() == QtCore.QEvent.FocusOut:
            self.oDigitalKeyboard.setVisible(False)
        if _event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
            self.oDigitalKeyboard.connect_to_widget(_object)
            self.oDigitalKeyboard.setVisible(True)
            
        return False


    def ViewHeart(self, id_search):
        if id_search == '':
            return
                        
        selHeart_2 = ""
        if str(self.comboBox.itemData(self.comboBox.currentIndex()).toString()) not in ["-1", "0"]:
            selHeart_2 += "AND t1.id_group = " + str(self.comboBox.itemData(self.comboBox.currentIndex()).toString()) + "\n"
        if str(self.comboBox.itemData(self.comboBox.currentIndex()).toString()) == "0":
            selHeart_2 += "AND t1.id_group IS NULL\n"
        if self.lineEdit.text() <> '':
            selHeart_2 += "AND sizes LIKE '%" + self.lineEdit.text() + "%'"
            
        print selHeart + selHeart_2 + selHeart_3    
                
        r = model.setQuery(selHeart + selHeart_2 + selHeart_3, db1)
        print 'r=', r
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnHidden(17, True)        
        self.tableView.setColumnHidden(18, True)

        #26.01
        #self.tableView.setColumnHidden(17, True)        
        #self.tableView.setColumnHidden(18, True)
        
        global shape
        CurInd = self.comboBox.currentIndex()                
        if CurInd == 0:
            shape = -1
        else:
            if CurInd > len(shapes):
                shape = -2
            else:
                shape = shapes[CurInd - 1]         
                
        if shape in [-1, 1]:
            self.tableView.setColumnHidden(7, False)        
            self.tableView.setColumnHidden(8, False)        
            self.tableView.setColumnHidden(9, False)                    
        if shape in [-1, 2]:
            self.tableView.setColumnHidden(10, False)        
            self.tableView.setColumnHidden(11, False)        
            self.tableView.setColumnHidden(12, False)        
            self.tableView.setColumnHidden(13, False)            
        if shape in [2, 0, -2]:
            self.tableView.setColumnHidden(7, True)        
            self.tableView.setColumnHidden(8, True)        
            self.tableView.setColumnHidden(9, True)                    
        if shape in [1, 0, -2]:
            self.tableView.setColumnHidden(10, True)        
            self.tableView.setColumnHidden(11, True)        
            self.tableView.setColumnHidden(12, True)        
            self.tableView.setColumnHidden(13, True)        
        
                
        TestHeart.searchInModel(id_search, self.tableView, model)
        enab = self.selModel.currentIndex().row() >= 0
        
        model.setHeaderData(1, QtCore.Qt.Horizontal, u"Размеры")
        model.setHeaderData(2, QtCore.Qt.Horizontal, u"Сила тока в контрольной точке (A)")
        model.setHeaderData(3, QtCore.Qt.Horizontal, u"Минимальное напряжение в контрольной точке (V)")
        model.setHeaderData(4, QtCore.Qt.Horizontal, u"Погрешность измерения (%)")
        model.setHeaderData(5, QtCore.Qt.Horizontal, u"Вес магнитопровода (кг)")
        model.setHeaderData(6, QtCore.Qt.Horizontal, u"Удельный вес электротехнического железа (кг/м³)")
        
        model.setHeaderData(7, QtCore.Qt.Horizontal, u"Внутренний диаметр (мм)")
        model.setHeaderData(8, QtCore.Qt.Horizontal, u"Наружный диаметр (мм))")
        model.setHeaderData(9, QtCore.Qt.Horizontal, u"Высота (мм))")
        model.setHeaderData(10, QtCore.Qt.Horizontal, u"Внутренняя длина (мм))")
        model.setHeaderData(11, QtCore.Qt.Horizontal, u"Внутренняя высота (мм))")
        model.setHeaderData(12, QtCore.Qt.Horizontal, u"Толщина (мм))")
        model.setHeaderData(13, QtCore.Qt.Horizontal, u"Ширина ленты (мм))")
        #26.01
        model.setHeaderData(14, QtCore.Qt.Horizontal, u"Нижняя граница диапазона поверки")
        model.setHeaderData(15, QtCore.Qt.Horizontal, u"Верхняя граница диапазона поверки")
                
        model.setHeaderData(16, QtCore.Qt.Horizontal, u"Группа")
        
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.pushButton_2.setEnabled(enab)
        self.pushButton_3.setEnabled(enab)
        self.pushButton_4.setEnabled(enab)

#        self.tableView.setFocus()    




    def selectionChanged1(self):
        row = self.selModel.currentIndex().row()
        if row == -1:
            return
        global id_heart
        id_heart = model.record(row).field('id').value().toString()

# Редактирование сердечников (начало кода)        
    def pushButton_Click(self):
        global id_heart
        self.wind1 = self.editHeart(self.env)
#        self.wind1 = self.editHeart(self.env)
        #if self.wind1.tag == 0: ?????????????????????????
        #    return
        self.wind1.tag = 1
                
        self.wind1.setWindowTitle(u'Добавление нового сердечника')
        
        self.wind1.lineEdit_2.setText('5')
        self.wind1.lineEdit_4.setText('10')
        
        self.wind1.exec_()        
        
        self.lineEdit.textChanged.disconnect(self.lineEdit_textChanged)
        self.lineEdit.setText('')        
        self.ViewHeart(id_heart)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)


    def pushButton2_Click(self):        
#        if model2.rowCount() > 0:
#            QMessageBox.warning(self, u"Предупреждение", u"Удаление текущей позиции невозможно,\n\r поскольку она содержит группы средств измерения!", QMessageBox.Ok)
#            return
        r = QMessageBox.warning(self, u"Предупреждение", u"Вы действительно желаете удалить текущую запись?", QMessageBox.Yes, QMessageBox.No)            
        if r == QMessageBox.Yes:
            query = QSqlQuery(db1)
            query.prepare("DELETE FROM heart WHERE id = :ID")
            row = self.selModel.currentIndex().row()                
            print model.record(row).field('id').value().toString()            
            query.bindValue(":id", model.record(row).field('id').value().toString());
            query.exec_()
            model.setQuery(selHeart + selHeart_2 + selHeart_3, db1)
            # Навигация на предыдущую позицию
            if row > 0:
                row -= 1
            self.tableView.selectRow(row)                                    
            enab = self.selModel.currentIndex().row() >= 0
            self.pushButton_2.setEnabled(enab)
            self.pushButton_3.setEnabled(enab)
            self.pushButton_4.setEnabled(enab)
           # self.viewButtons(1, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.selModel)
            
    def pushButton3_Click(self):
        global id_heart
#######        self.wind1 = self.editHeart()
        print 2, self.env
        self.wind1 = self.editHeart(self.env)
        if self.wind1.tag == 0:
            return
        self.wind1.tag = 2
        self.wind1.setWindowTitle(u'Редактирование текущего сердечника')
        row = self.selModel.currentIndex().row()        
        
        
        self.wind1.lineEdit.setText(model.record(row).field('sizes').value().toString())
        self.wind1.lineEdit_2.setText(nullValue(model.record(row).field('apc')))
        self.wind1.lineEdit_3.setText(nullValue(model.record(row).field('vpc')))
        self.wind1.lineEdit_4.setText(nullValue(model.record(row).field('pogr')))
        self.wind1.lineEdit_5.setText(nullValue(model.record(row).field('in_diameter')))
        #self.wind1.lineEdit_6.setText(nullValue(model.record(row).field('right_border')))
        self.wind1.lineEdit_6.setText(nullValue(model.record(row).field('out_diameter')))
        self.wind1.lineEdit_7.setText(nullValue(model.record(row).field('weight_magnetic')))
        
        self.wind1.lineEdit_8.setText(nullValue(model.record(row).field('height')))
        self.wind1.lineEdit_9.setText(nullValue(model.record(row).field('in_length')))
        self.wind1.lineEdit_10.setText(nullValue(model.record(row).field('in_height')))
        self.wind1.lineEdit_11.setText(nullValue(model.record(row).field('depth')))
        self.wind1.lineEdit_12.setText(nullValue(model.record(row).field('width')))
        
        #26.01
        self.wind1.lineEdit_15.setText(nullValue(model.record(row).field('left_border')))
        self.wind1.lineEdit_16.setText(nullValue(model.record(row).field('right_border')))
        
        for i in range(self.wind1.comboBox.count()):
            if self.wind1.comboBox.itemData(i) == int(model.record(row).field('id_group').value().toString()):
                self.wind1.comboBox.setCurrentIndex(i)
                
        for i in range(self.wind1.comboBox_2.count()):
            if self.wind1.comboBox_2.itemData(i) == int(model.record(row).field('id_grade').value().toString()):
                self.wind1.comboBox_2.setCurrentIndex(i)

        
        
        self.wind1.exec_()
                
        self.lineEdit.textChanged.disconnect(self.lineEdit_textChanged)
        self.lineEdit.setText('')        
        self.ViewHeart(id_heart)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)

    def pushButton4_Click(self):
        row = self.selModel.currentIndex().row()
        self.id_h = model.record(row).field('id').value().toString()
        self.sizes = model.record(row).field('sizes').value().toString()
        self.apc = float(model.record(row).field('apc').value().toString())
        self.vpc = float(model.record(row).field('vpc').value().toString())
        self.pogr = model.record(row).field('pogr').value().toString()
        
        self.in_diameter = float(model.record(row).field('in_diameter').value().toString())
        self.out_diameter = float(model.record(row).field('out_diameter').value().toString())
        self.weight_magnetic = float(model.record(row).field('weight_magnetic').value().toString())
        self.dens = float(model.record(row).field('dens').value().toString())
             
        #???????????????????????????????????        
        self.left_border = float(model.record(row).field('left_border').value().toString())
        self.right_border = float(model.record(row).field('right_border').value().toString())
                
        print u'ВЫБОР'
        self.close()

    def pushButton5_Click(self):
#        self.id_h = ''
        self.close()

    def pushButton6_Click(self):
        iRow = self.tableView.currentIndex().row()
        if model.rowCount() - 1 > iRow:
#            self.tableView.setCurrentIndex(model.index(iRow + 1, 0))
            self.tableView.selectRow(iRow + 1)
        self.tableView.setFocus()    

    def pushButton7_Click(self):
        iRow = self.tableView.currentIndex().row()
        if iRow > 0:
            self.tableView.selectRow(iRow - 1)
        self.tableView.setFocus()    

    def lineEdit_textChanged(self):
        self.ViewHeart(0)
        pass


    class editHeart(QtGui.QDialog):
        def __init__(self, env, *args):
            QtGui.QDialog.__init__(self, *args)
            if not JournalMsr.MyLoadUi(path_ui, "editHeart.ui", self):
                return

            print 3, env


            SQL = u"""
                     SELECT id, name_group, shape, 1 AS srt FROM group_heart
                     UNION ALL
                     SELECT 0 AS id, 'БЕЗ ГРУППЫ' AS name_group, 0 AS shape, 2 AS srt
                     ORDER BY srt, name_group"""                                           
            query = QSqlQuery(db1)
            query.prepare(SQL)
            query.exec_()        
            self.comboBox.clear()
            
            for i in range(0, query.size()):
                query.next()
                self.comboBox.addItem(query.record().value(1).toString(), query.record().value(0).toString())
            self.comboBox.insertSeparator(self.comboBox.count() - 1)
                        
            SQL = u"""SELECT id, mark, dens, 1 AS srt FROM grade_iron
                     UNION ALL
                     SELECT 0 AS id, 'БЕЗ УДЕЛЬНОГО ВЕСА' AS mark, NULL AS dens, 2 AS srt
                     ORDER BY srt, mark"""                                           
            query = QSqlQuery(db1)
            query.prepare(SQL)
            query.exec_()        
            self.comboBox_2.clear()
            for i in range(0, query.size()):
                query.next()
                if query.record().value(0).toString() <> '0':
                    self.comboBox_2.addItem(query.record().value(2).toString() + ' (' + query.record().value(1).toString()+ ')',
                                            query.record().value(0).toString())
                else:                        
                    self.comboBox_2.addItem(query.record().value(1).toString(),
                                            query.record().value(0).toString())
            self.comboBox_2.insertSeparator(self.comboBox_2.count() - 1)
                        
                                                
            self.pushButton.clicked.connect(self.pushButton1_Click)
            self.pushButton_2.clicked.connect(self.pushButton2_Click)
            self.pushButton_3.clicked.connect(self.pushButton3_Click)

            self.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
            self.comboBox_currentIndexChanged()



            self.oDigitalKeyboard = DigitalKeyboard(env)
            self.horizontalLayout_4.addWidget(self.oDigitalKeyboard)
            self.oDigitalKeyboard.setEnabled(True)
          
          
            self.oDigitalKeyboard.enter.connect(self.change_focus) 
          
            self.lineEdit.installEventFilter(self)
            self.lineEdit_2.installEventFilter(self)
            self.lineEdit_3.installEventFilter(self)
            self.lineEdit_4.installEventFilter(self)
            self.lineEdit_5.installEventFilter(self)
            self.lineEdit_6.installEventFilter(self)
            self.lineEdit_7.installEventFilter(self)
            self.lineEdit_8.installEventFilter(self)
            self.lineEdit_9.installEventFilter(self)
            self.lineEdit_10.installEventFilter(self)
            self.lineEdit_11.installEventFilter(self)
            self.lineEdit_12.installEventFilter(self)
            #26.01
            self.lineEdit_15.installEventFilter(self)
            self.lineEdit_16.installEventFilter(self)
         
            self.lineEdit_2.setFocus()

        
            self.horizontalLayout_4.setEnabled(False)
            self.verticalLayout_3.setEnabled(False)       

            # Корректировка размеров цифровой клавиатуры
            fnt = self.oDigitalKeyboard.ui.btn_0.font()
            fnt.setPointSize(fnt.pointSize() * 0.7)        
                   
            self.oDigitalKeyboard.ui.btn_0.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_1.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_2.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_3.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_4.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_5.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_6.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_7.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_8.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_9.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_dot.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_BackSpace.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_Clear.setFont(fnt)
            self.oDigitalKeyboard.ui.btn_Ok.setFont(fnt)        
            minWidth = self.oDigitalKeyboard.ui.btn_BackSpace.minimumWidth() * 0.7
            self.oDigitalKeyboard.ui.btn_BackSpace.setMinimumSize(minWidth, 0)
            self.oDigitalKeyboard.ui.btn_Clear.setMinimumSize(minWidth, 0)
            self.oDigitalKeyboard.ui.btn_Ok.setMinimumSize(minWidth, 0)

        def change_focus(self):
            if self.lineEdit.hasFocus():   
                self.lineEdit_2.setFocus()   
                return
            if self.lineEdit_2.hasFocus():   
                self.lineEdit_3.setFocus()   
                return
            if self.lineEdit_3.hasFocus():   
                self.lineEdit_4.setFocus()   
                return
            if self.lineEdit_4.hasFocus():   
                self.lineEdit_7.setFocus()   
                return
            if self.lineEdit_7.hasFocus():   
                if self.lineEdit_5.isVisible():   
                    self.lineEdit_5.setFocus()
                else:       
                    if self.lineEdit_9.isVisible():   
                        self.lineEdit_9.setFocus()
                    else:    
                        self.lineEdit.setFocus()
                return
            
            if self.lineEdit_5.hasFocus():   
                self.lineEdit_6.setFocus()   
                return
            if self.lineEdit_6.hasFocus():   
                self.lineEdit_8.setFocus()   
                return
            
            if self.lineEdit_8.hasFocus():   
                if self.lineEdit_9.isVisible():   
                    self.lineEdit_9.setFocus()
                else:       
                    self.lineEdit.setFocus()
                return
            
            if self.lineEdit_9.hasFocus():   
                self.lineEdit_10.setFocus()   
                return
            if self.lineEdit_10.hasFocus():   
                self.lineEdit_11.setFocus()   
                return
            if self.lineEdit_11.hasFocus():   
                self.lineEdit_12.setFocus()   
                return
            if self.lineEdit_12.hasFocus():   
                self.lineEdit.setFocus()   
                return
            
            print self.lineEdit.hasFocus()
            return 
            

        def eventFilter(self, _object, _event):
            
            u"""Отлавливает переход фокуса, для подключения экранной клавиатуры"""
            if _event.type() == QtCore.QEvent.FocusOut:
                self.oDigitalKeyboard.connect_to_widget()
            if _event.type() in (QtCore.QEvent.FocusIn, QtCore.QEvent.MouseButtonPress):
                self.oDigitalKeyboard.connect_to_widget(_object)
            return False

        
        def comboBox_currentIndexChanged(self):
            global shapes
            self.label_5.setVisible(False)
            self.lineEdit_5.setVisible(False)
            self.label_6.setVisible(False)
            self.lineEdit_6.setVisible(False)
            self.label_10.setVisible(False)
            self.lineEdit_8.setVisible(False)
            self.label_11.setVisible(False)
            self.lineEdit_9.setVisible(False)
            self.label_12.setVisible(False)
            self.lineEdit_10.setVisible(False)
            self.label_13.setVisible(False)
            self.lineEdit_11.setVisible(False)
            self.label_14.setVisible(False)
            self.lineEdit_12.setVisible(False)
            if self.comboBox.currentIndex() < len(shapes):
                if shapes[self.comboBox.currentIndex() + 1] == 1:
                    print 1111111111111
                    self.label_5.setVisible(True)
                    self.lineEdit_5.setVisible(True)
                    self.label_6.setVisible(True)
                    self.lineEdit_6.setVisible(True)
                    self.label_10.setVisible(True)
                    self.lineEdit_8.setVisible(True)
                if shapes[self.comboBox.currentIndex() + 1] == 2:
                    print 2222222222222
                    self.label_11.setVisible(True)
                    self.lineEdit_9.setVisible(True)
                    self.label_12.setVisible(True)
                    self.lineEdit_10.setVisible(True)
                    self.label_13.setVisible(True)
                    self.lineEdit_11.setVisible(True)
                    self.label_14.setVisible(True)
                    self.lineEdit_12.setVisible(True)
                
                        
            #print self.comboBox.currentIndex(), shapes[self.comboBox.currentIndex()]
            pass
        
        def pushButton1_Click(self):
            if self.lineEdit.text() == '':
                QMessageBox.warning(None, u"Предупреждение",
                u"Введи размеры",
                QMessageBox.Ok)
                self.lineEdit.setFocus()
                return
                
            global id_heart
            query = QSqlQuery(db1)
            print 2
            if self.tag == 1:            
                query.prepare("SELECT CASE WHEN (MAX(id) IS NULL) THEN 1 ELSE MAX(id) + 1 END FROM heart");
                query.exec_()
                query.next()
                id_heart = query.value(0).toString()
                query.prepare("""INSERT INTO heart (id, sizes, apc, vpc, pogr, in_diameter, out_diameter, height, in_length, in_height, depth, width, weight_magnetic, left_border, right_border, id_grade, id_group)
                                            VALUES (:id, :sizes, :apc, :vpc, :pogr, :in_diameter, :out_diameter, :height, :in_length, :in_height, :depth, :width, :weight_magnetic, :left_border, :right_border, :id_grade, :id_group)""")
            else:
                query.prepare("""UPDATE heart SET sizes = :sizes, apc = :apc, vpc = :vpc, pogr = :pogr,
                 in_diameter = :in_diameter, out_diameter = :out_diameter, height = :height, in_length = :in_length, in_height = :in_height, depth = :depth, width = :width,
                 weight_magnetic = :weight_magnetic, left_border = :left_border, right_border = :right_border, id_grade = :id_grade, id_group = :id_group WHERE id = :id""")
                
            #print 'aaaself.id_heart=', id_heart, str(self.lineEdit_2.text()).strip()   
            print 'id_heart=', id_heart            
            query.bindValue(":id", id_heart);
            query.bindValue(":sizes", noneValue(self.lineEdit.text()))
            query.bindValue(":apc", noneValue(self.lineEdit_2.text()))
            query.bindValue(":vpc", noneValue(self.lineEdit_3.text()))
            query.bindValue(":pogr", noneValue(self.lineEdit_4.text()))
            query.bindValue(":in_diameter", noneValue(self.lineEdit_5.text()))
            query.bindValue(":out_diameter", noneValue(self.lineEdit_6.text()))
            query.bindValue(":height", noneValue(self.lineEdit_8.text()))
            query.bindValue(":in_length", noneValue(self.lineEdit_9.text()))
            query.bindValue(":in_height", noneValue(self.lineEdit_10.text()))
            query.bindValue(":depth", noneValue(self.lineEdit_11.text()))
            query.bindValue(":width", noneValue(self.lineEdit_12.text()))
            
            query.bindValue(":weight_magnetic", noneValue(self.lineEdit_7.text()))

            query.bindValue(":left_border", noneValue(self.lineEdit_15.text()))
            query.bindValue(":right_border", noneValue(self.lineEdit_16.text()))
            
            if int(self.comboBox_2.itemData(self.comboBox_2.currentIndex()).toString()) == 0:
                query.bindValue(":id_grade", None)
            else:    
                query.bindValue(":id_grade", str(self.comboBox_2.itemData(self.comboBox_2.currentIndex()).toString()))
            
            if int(self.comboBox.itemData(self.comboBox.currentIndex()).toString()) == 0:
                query.bindValue(":id_group", None)
            else:    
                query.bindValue(":id_group", str(self.comboBox.itemData(self.comboBox.currentIndex()).toString()))
                        
            if not query.exec_():
                QMessageBox.warning(None, u"Предупреждение",
                u"Ошибка сохранения",
                QMessageBox.Ok)
            else:    
                self.close()

        def pushButton2_Click(self):
            global id_heart
            #26.01 
            #id_heart = '' #непонятно зачем?
            self.close()
            
        def pushButton3_Click(self):
            if self.lineEdit_5.isVisible():
#                self.lineEdit.setText(self.lineEdit_5.text() + 'x' + self.lineEdit_6.text() + 'x' + self.lineEdit_8.text() + str(self.comboBox_2.currentText())[str(self.comboBox_2.currentText()).find(' '):])            
                self.lineEdit.setText(self.lineEdit_5.text() + 'x' + self.lineEdit_6.text() + 'x' + self.lineEdit_8.text() + unicode(str(self.comboBox_2.currentText())[str(self.comboBox_2.currentText()).find(' '):]))            
            if self.lineEdit_9.isVisible():
#                self.lineEdit.setText(self.lineEdit_9.text() + 'x' + self.lineEdit_10.text() + 'x' + self.lineEdit_11.text() + 'x' + self.lineEdit_12.text() + str(self.comboBox_2.currentText())[str(self.comboBox_2.currentText()).find(' '):])
                self.lineEdit.setText(self.lineEdit_9.text() + 'x' + self.lineEdit_10.text() + 'x' + self.lineEdit_11.text() + 'x' + self.lineEdit_12.text() + unicode(str(self.comboBox_2.currentText())[str(self.comboBox_2.currentText()).find(' '):]))



                        
# Редактирование сердечников (конец кода)        


if __name__ == "__main__":    
    import sys
    app = QtGui.QApplication(sys.argv)
    db = QSqlDatabase("QPSQL")
#    db.setHostName("alpha")
#    db.setHostName("10.5.0.6")
    db.setHostName("localhost")
    db.setDatabaseName("electrolab1")
    db.setUserName("electrolab")
    db.setPassword("electrolab")
    rez = db.open();    
    
    class Env():
        class config():
            class paths():
                pass    
    env = Env()
    env.db = db    
    env.config.paths.ui = "ui"

    wind = Heart(env)
#    wind.show()
    if wind.tag <> 0:        
        wind.show()
        wind.resizeEvent(None)
    sys.exit(app.exec_())
