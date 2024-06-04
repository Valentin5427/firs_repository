import sys
from configparser import ConfigParser
import  logging
from tech.integration import INI, LOG, FileSystem
import os.path
import traceback
import psycopg2
from xml.dom.minidom import parse
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
import re
from decimal import Decimal



def strip(num):

    string = str(num)
    ext = ''

    if re.search('[a-zA-Z]+',string):
        ext = str(num)[-2:]
        string = str(num).replace(ext, '')


    data = re.findall('\d+.\d+0$', string)
    if data:
        return data[0][:-1]+ext

    return string+ext


class DBParam():

    def __init__(self,_oLog):
        self.oLog = _oLog
        self.settings = ConfigParser()

    def connect_to_base(self):
        if not self.check_integration():
            self.oLog.error('файл integration.ini не найден')
        self.settings.read('integration.ini')
        try:
            self.host = self.settings['DB']['Host']
            self.db = self.settings['DB']['DB']
            self.user = self.settings['DB']['User']
            self.password = self.settings['DB']['Pass']
        except KeyError as er:
            self.oLog.error(f'не найдена информарции при подключении к базе по ключу {er}')


    def check_integration(self):
        if os.path.exists('integration.ini'):
            return True
        return False

    def connect(self):
        u"""Установить соединение. Возвращает истину при удачном соединении"""
        try:
            self._oConnection = psycopg2.connect(f"host={self.host} dbname={self.db} user={self.user} password={self.password}")
            self._connected = True
        except Exception :
            self._connected = False
        return self._connected
    @property
    def connection(self):
        return self._oConnection



class Loader():
    def __init__(self, _connect, _oLog, _noException = True):
        u"""_connect - Соединение с БД, _oLog - Журнал"""
        self.oConnect = _connect
        self.oLog = _oLog
        self.noException = _noException
        self.cache = {}


    def process(self, fileCollection):
        for file in fileCollection:
            self.file = file
            print(111,file.sErorrPath)
            print(315,self.file.sFileName)
            





            # if len(rootNodes) <= 0:
            #     self.oLog.error("в файле не найден блок 'трансфроматор'")
            #     return
            # for trans in rootNodes:
            #     self.parse_item(trans)
            # print('Состояние',self.file.state)
            # if self.file.state == 'correct':
            #     cur = file.sPath + file.sFileName
            #     new = f'{file.sArchPath}\\{file.sFileName}'
            #     os.replace(cur, new)
            # elif self.file.state == 'error':
            #     cur = file.sPath + file.sFileName
            #     new = f'{file.sErorrPath}\\{file.sFileName}'
            #     os.replace(cur, new)
            #
            #






    def save_serial(self):
        if self.check_serial():
            if self.update_serial():
                return True
        else:
            if self.insert_serial():
                return True
        self.file.state = 'error'
        return False

    def update_serial(self):
        self.oLog.info(f"Обновление параметров выпуска серийного номера {self.serial['year']} {self.serial['number']}")
        with  self.oConnect.connection.cursor() as curs:
            try:
                sql = f"""UPDATE serial_number
                                     set ordernumber = '{self.serial['order']}' ,
                                         series = {self.serial['series']} ,
                                         serialnumber = {self.serial['number']} ,
                                         makedate = {self.serial['year']} ,
                                         transformer = {self.transformer['Id']}
                                     where id = {self.serial['id']}"""
                # print(sql)
                curs.execute(sql)
                self.oConnect.connection.commit()
            except Exception as ex:
                # print(sql)
                self.oLog.error(f'Возникла ошибка при выгрузке Параметров выпуска {ex}')
                self.oConnect.connection.commit()
                return False
        return True

    def insert_serial(self):
        self.oLog.info(f"Добавление серийного номера {self.serial['year']} {self.serial['number']}")
        print('Добавление серийника')
        with  self.oConnect.connection.cursor() as curs:
            try:
                sql = f"""INSERT INTO serial_number(
                                                ordernumber,
                                                series,
                                                serialnumber,
                                                makedate,
                                                transformer
                                                )
                                                values(
                                                '{self.serial['order']}',
                                                {self.serial['series']},
                                                {self.serial['number']},
                                                {self.serial['year']},
                                                {self.transformer['Id']}
                                                )"""
                print(sql)
                curs.execute(sql)
                self.oConnect.connection.commit()
            except:
                self.oLog.error('Возникла ошибка при выгрузке Параметров выпуска')
                self.oConnect.connection.commit()
                return False
        return True


    def check_serial(self):
        with  self.oConnect.connection.cursor() as curs:
            sql = f"select *  from  serial_number  where serialnumber = {self.serial['number']} and makedate = {self.serial['year']}"
            print(sql)
            curs.execute(sql)
            if curs.rowcount > 0:
                data = curs.fetchone()
                self.serial['id'] = data[0]
                print(self.serial)
                return data
            curs.close()
            return False


    def parse_db_serial(self,serial):
        self.serialDB = {'id': None, 'number': None, 'year': None, 'order': None, 'series': None}
        self.serialDB['id'] = serial[0]
        self.serialDB['order'] = serial[1]
        self.serialDB['series'] = serial[2]
        self.serialDB['number'] = serial[3]
        self.serialDB['year'] = serial[4]
        self.compare_serial()

# метод сравнения данных серийника  полученных из xml и бд
    def compare_serial(self):
        print(1,self.serial)
        print(2,self.serialDB)
        # метод сравнения данных обмотки полученных из xml и бд
        for key in self.serial.keys():
            if self.serial[key] not in (None, self.serialDB[key]):
                self.oLog.info(f"Параметр выпуска {Loader.descripSerial[key]} изменился")
            else:
                self.serial[key] = self.serialDB[key]


#________________________________________методы и запросы для парсинга обмоток__________________________________________

    def parse_coil(self,trans):
        try:
            coils = trans.getElementsByTagName('Обмотки')[0]
        except IndexError:
            self.oLog.error('Не найдены обмотки трансформатора')
            return False

        coils = coils.getElementsByTagName("Обмотка")
        self.coils = []
        for coil in coils:
            print(1111,coil)
            self.winding = self.get_coil_fields()
            self.coil = coil
            if not self.params_coilTT():
                return False
        self.state_coil = True
        return True

# метод для парсинга параметров обмотки
    def params_coilTT(self):
        self.winding['Transformer'] = self.transformer['Id']
        try:
            self.winding['Coilnumber'] = int(self.coil.getElementsByTagName("НомерОбмотки")[0].firstChild.data)
        except:
            self.oLog.error("Отсутствует номер Обмотки, обмотка не будет выгружена")
            self.file.state = 'error'
            return False

        try:
            self.winding['Tap'] = int(self.coil.getElementsByTagName("НомерОтпайки")[0].firstChild.data)
        except:
            self.oLog.error("Отсутствует номер Отпайки, обмотка не будет выгружена")
            self.file.state = 'error'
            return False

        try:
            self.winding['PrimaryCurrent'] = float(self.coil.getElementsByTagName("НоминальныйПервичныйТок")[0].firstChild.data)
        except:
            self.oLog.error("Отсутствует Номинальный Первичный Ток, обмотка не будет выгружена")
            self.file.state = 'error'
            return False

        try:
            self.winding['SecondCurrent'] = float(self.coil.getElementsByTagName("НоминальныйВторичныйТок")[0].firstChild.data)
        except:
            self.oLog.error("Отсутствует Номинальный Вторичный Ток, обмотка не будет выгружена")
            self.file.state = 'error'
            return False

        try:
            clas = self.coil.getElementsByTagName("КлассТочности")[0].firstChild.data.upper()
            self.winding['ClassAccuracy'] = clas
        except:
            self.oLog.error("Отсутствует Класс Точности, обмотка не будет выгружена")
            self.file.state = 'error'
            return False

        try:
            self.winding['Rating'] = self.coil.getElementsByTagName("Коэффициент")[0].firstChild.data
        except:
            pass
            # self.oLog.error(f"Отсутствует значение коэффициента для обмотки с номером {self.winding['Coilnumber']} и отпайкой {self.winding['Tap']}")

        try:
            self.winding['SecondLoad'] = float(self.coil.getElementsByTagName("НоминальнаяВторичнаяНагрузка")[0].firstChild.data)
        except:
            self.file.state = 'error'
            self.oLog.error("Отсутствует Номинальная Вторичная Нагрузка, обмотка не будет выгружена")
            return False

        try:
            self.winding['AmpereTurn'] = int(self.coil.getElementsByTagName("АмперВитки")[0].firstChild.data)
        except:
            self.oLog.error("Отсутствует Ампер Витки, обмотка не будет выгружена")
            self.file.state = 'error'
            return False
        coil = self.search_coil()
        if coil:
            self.parse_db_coil(coil)
        else:
            self.coils.append(self.winding)
        return True


    def parse_db_coil(self, coil):
        self.base_winding = self.get_coil_fields()
        self.winding['ID'] = coil[0]
        self.base_winding['ID'] = coil[0]
        self.base_winding['Transformer'] = coil[1]
        self.base_winding['Coilnumber'] = coil[2]
        self.base_winding['Tap'] = coil[3]
        self.base_winding['Coiltype'] = coil[4]
        self.base_winding['ClassAccuracy'] = coil[5]
        self.base_winding['PrimaryCurrent'] = coil[6]
        self.base_winding['SecondCurrent'] = coil[7]
        self.base_winding['SecondLoad'] = coil[8]
        self.base_winding['MagneticVoltage'] = coil[9]
        self.base_winding['MagneticCurrent'] = coil[10]
        self.base_winding['Resistance'] = coil[11]
        self.base_winding['Rating'] = coil[12]
        self.base_winding['Quadroload'] = coil[13]
        self.base_winding['AmpereTurn'] = coil[14]
        for i in self.base_winding.keys():
            if type(self.base_winding[i]) == Decimal:
                self.base_winding[i] = float(self.base_winding[i])
        self.compare_coil()




    def search_coil(self):
        if self.transformer['Id'] == None:
            return False

        sql = f"""select * from coil where
                    transformer = {self.transformer['Id']} and 
                    coilnumber = {self.winding['Coilnumber']} and
                    tap = {self.winding['Tap']}"""
        # print(sql)
        with  self.oConnect.connection.cursor() as curs:
            curs.execute(sql)
            if curs.rowcount == 0:
                return False
            else:
                coil = curs.fetchone()
                return coil

# метод сравнения данных обмотки полученных из xml и бд
    def compare_coil(self):
        for key in self.winding.keys():
            if self.winding[key] not in (None, self.base_winding[key]):
                self.oLog.info(f"Параметр обмотки {Loader.descripCoils[key]} изменился с {self.base_winding[key]} на {self.winding[key]}  ")
            else:
                self.winding[key] = self.base_winding[key]
        self.coils.append(self.winding)


    def update_coil(self):
        try:
            with  self.oConnect.connection.cursor() as curs:
                curs.execute("""UPDATE COIL set
                                          transformer = %s,
                                          coilnumber = %s,
                                          tap = %s,
                                          coiltype = %s,
                                          classaccuracy = %s,
                                          primarycurrent = %s,
                                          secondcurrent = %s,
                                          secondload = %s,
                                          magneticVoltage = %s,
                                          magneticCurrent = %s,
                                          resistance = %s,
                                          rating = %s,
                                          quadroload = %s,
                                          ampereturn = %s
                                where id = %s""", (self.transformer['Id'],
                                                    self.winding['Coilnumber'],
                                                    self.winding['Tap'],
                                                    self.winding['Coiltype'],
                                                    self.winding['ClassAccuracy'],
                                                    self.winding['PrimaryCurrent'],
                                                    self.winding['SecondCurrent'],
                                                    self.winding['SecondLoad'],
                                                    self.winding['MagneticVoltage'],
                                                    self.winding['MagneticCurrent'],
                                                    self.winding['Resistance'],
                                                    self.winding['Rating'],
                                                    self.winding['Quadroload'],
                                                    self.winding['AmpereTurn'],
                                                    self.winding['ID']))
                self.oConnect.connection.commit()

        except:
            pass



    def insert_coil(self):
       try:
           with  self.oConnect.connection.cursor() as curs:
               curs.execute("""
                             INSERT INTO coil(
                                                  transformer,
                                                  coilnumber,
                                                  tap,
                                                  coiltype,
                                                  classaccuracy,
                                                  primarycurrent,
                                                  secondcurrent,
                                                  secondload,
                                                  magneticVoltage,
                                                  magneticCurrent,
                                                  resistance,
                                                  rating,
                                                  quadroload,
                                                  ampereturn
                                                  )
                                              VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s , %s , %s , %s);
                                              """, (self.transformer['Id'],
                                                    self.winding['Coilnumber'],
                                                    self.winding['Tap'],
                                                    self.winding['Coiltype'],
                                                    self.winding['ClassAccuracy'],
                                                    self.winding['PrimaryCurrent'],
                                                    self.winding['SecondCurrent'],
                                                    self.winding['SecondLoad'],
                                                    self.winding['MagneticVoltage'],
                                                    self.winding['MagneticCurrent'],
                                                    self.winding['Resistance'],
                                                    self.winding['Rating'],
                                                    self.winding['Quadroload'],
                                                    self.winding['AmpereTurn'],
                                                    ))
               self.oConnect.connection.commit()
       except:
            self.oLog.error('Ошибка добавления ОБМОТКИ трансформатора')




def job(_sINIFile):
    u"""Задача загрузки из 1с"""
    oINI = INI(_sINIFile)
    log = LOG(oINI.log)
    log.info(u'Инициализация задачи. Загрузка данных из %s' % oINI.path)
    try:
        base = DBParam(log)
        base.connect_to_base()
        if not base.connect():
            raise Exception
        log.info(f'Подключение к бд {base.db} установлено')
    except:
        log.error(u'Сбой при подключении к БД.')
        return
    try:
        fileCollection = FileSystem().get_filelist(oINI.path, oINI.arch, oINI.error)
        print(113,fileCollection)
    except Exception as er:
        log.error(u'Сбой при получении списка файлов. "s%"' + str(er))
    if not len(fileCollection):
        log.info(u'Нет файлов для загрузки')
        return
    try:
        oLoade = Loader(base, log)
        oLoade.process(fileCollection)
    except Exception as er:
        log.error(f'Сбой при загрузке {er}')
        return
    log.info(u'Загрузка данных из %s выполнена' % oINI.path)






if __name__ == "__main__":
    import sys
    job('integration.ini')
    # path = "settings.ini"
    # config = INI(path, 'Integration')
    # print(config.config.read(path))
    # print(sys.argv)

