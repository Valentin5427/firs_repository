#coding=utf-8
u"""
Метаданные проекта electrolab
"""
from datetime import datetime
from dpframe.data.mddecorators import DBTable, DBField, integer, primary_key, invisible, required, reference, display, unique, char, parent, enum
from dpframe.data.mddecorators import numeric, default, timestamp, boolean, varchar, text, fk_description

@display(u'Окружающая среда')
class climat(DBTable):
    u"""Журнал окружающей среды"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @integer
    @required
    @display(u'Испытатель')
    @reference(u'operator')
    class operator(DBField):
        u"""Ссылка на оператора"""

    @numeric(length=3, precision=1, min=15, max=35)
    @required
    @display(u'Температура воздуха, °С')
    class temperature(DBField):
        u"""Температура в градусах по цельсию согласно ГОСТ от 15°С до 35°С"""

    @numeric(length=3, precision=1, min=30, max=80)
    @required
    @display(u'Относительная влажность, %')
    class humidity(DBField):
        u"""Влажность в процентах согласно ГОСТ, от 30% до 80%"""

    @numeric(length=4, precision=1, min=85, max=105)
    @required
    @display(u'Атмосферное давление, кПа')
    class pressure(DBField):
        u"""Давление в кПа от согласно ГОСТ 85кПа до 105кПа"""

    @timestamp
    @required
    @unique
    @default(u'now()')
    @display(u'Время')
    @fk_description
    class lastupdate(DBField):
        u"""Время последнего измерения согласно ГОСТ 3 раза не позднее (08:00, 12:00, 16:00)"""


@display(u'Несоответствия')
class defect(DBTable):
    u"""Справочник несоответствий"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @char(2)
    @display(u'Тип')
    class defecttype(DBField):
        u"""Тип несоответствия (перечислитель)"""

    @boolean
    @display(u'Критичность')
    class iscritical(DBField):
        u"""Подлежит ремонту или нет"""

    @varchar(100)
    @display(u'Полное наименование')
    @fk_description
    class fullname(DBField):
        u""""""

    @text
    @display(u'Описание')
    class description(DBField):
        u""""""


@display(u'Операторы')
class operator(DBTable):
    u"""Справочник операторов испытательных стендов"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @varchar(50)
    @required
    @display(u'Фамилия И.О.')
    @fk_description
    class fio(DBField):
        u"""Строковый идентификатор"""

    @varchar(30)
    @required
    @display(u'Фамилия')
    class family(DBField):
        u""""""

    @varchar(30)
    @required
    @display(u'Имя')
    class firstname(DBField):
        u""""""

    @varchar(30)
    @required
    @display(u'Отчество')
    class secondname(DBField):
        u""""""

    @boolean
    @required
    @display(u'Не сотрудник')
    class isexternal(DBField):
        u"""Признак внешнего (не является сотрудником предприятия) поверителя, используется в печатных формах"""

    @varchar(100)
    @display(u'Телефон')
    class phone(DBField):
        u""""""

    @boolean
    @required
    @default(u'false')
    @display(u'Уволен')
    class isdismiss(DBField):
        u"""Признак уволенного сотрудника"""


@display(u'Трансформатор')
class transformer(DBTable):
    u"""Основные технические данные трансформатора"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @varchar(100)
    @required
    @unique
    @display(u'Наименование')
    class fullname(DBField):
        u"""Уникальное наименование трансформатора"""

    @varchar(100)
    @required
    @display(u'Краткое наименование')
    @fk_description
    class shortname(DBField):
        u"""Краткое наименование. Используется при печати"""

    @varchar(10)
    @required
    @display(u'Тип')
    class type(DBField):
        u"""ТЛО/ТЛП/ТВ-ЭК - префикс из имени"""

    @varchar(100)
    @display(u'Стандарт')
    class standart(DBField):
        u""""""

    @numeric(length=6, precision=2)
    @display(u'Напряжение (ном.)')
    class voltage(DBField):
        u"""Номинальное напряжение"""

    @numeric(length=8, precision=2)
    @display(u'Напряжение (макс.)')
    class maxopervoltage(DBField):
        u"""Наибольшее рабочее напряжение"""

    @integer
    @display(u'Частота')
    class frequency(DBField):
        u"""Номинальная частота"""

    @integer
    @display(u'Число вторичных обмоток')
    class quantsecondcoil(DBField):
        u""""""

    @char(1)
    @display(u'Уровень изоляции')
    class isolationlevel(DBField):
        u""""""

    @varchar(3)
    @display(u'Исполнение')
    class climat(DBField):
        u"""Климатическое исполнение и категория размещения"""

    @numeric(length=6, precision=2)
    @display(u'Масса, кг')
    class weight(DBField):
        u"""Масса трансформатора не более"""


@display(u'Результаты поверки')
class checking(DBTable):
    u"""Данные, полученные в результате поверки на КНТ-05"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @integer
    @required
    @reference(u'item')
    @invisible
    class item(DBField):
        u"""Ссылка на изделие"""

    @integer
    @required
    @reference(u'coil')
    class coil(DBField):
        u"""Ссылка на испытываемую обмотку"""

    @numeric(length=6, precision=2)
    @display(u'Контрольная точка')
    class point(DBField):
        u""""""

    @numeric(length=6, precision=2)
    @display(u'Четвертная нагрузка')
    class quadroload(DBField):
        u"""Четвертная нагрузка при испытании на 120%"""

    @timestamp
    @required
    @display(u'Время')
    class chektimestamp(DBField):
        u"""Временная метка измерения"""

    @numeric(length=8, precision=4)
    @required
    class a(DBField):
        u"""Амплитудная ошибка поверяемого трансформатора тока"""

    @numeric(length=8, precision=4)
    class p(DBField):
        u"""Угловая ошибка поверяемого трансформатора тока"""

    @numeric(length=8, precision=4)
    @required
    class i(DBField):
        u"""Вторичный ток образцового трансформатора"""

    @numeric(length=8, precision=4)
    class n(DBField):
        u"""Номинальный вторичный ток образцового и поверяемого трансформатора"""

    @numeric(length=8, precision=4)
    class f(DBField):
        u"""Частота вторичного тока образцового трансформатора"""

    @numeric(length=8, precision=4)
    class k(DBField):
        u"""Коэффициент несинусоидальности вторичного тока образцового трансформатора"""


@display(u'Вторичная обмотка')
class coil(DBTable):
    u"""Технические данные вторичных обмоток трансформатора"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @integer
    @required
    @parent(u'transformer')
    @display(u'Трансформатор')
    class transformer(DBField):
        u"""Ссылка на Transformer"""

    @integer
    @required
    @display(u'Номер')
    @fk_description
    class coilnumber(DBField):
        u"""Номер обмотки"""

    @integer
    @required
    @display(u'Отпайка')
    class tap(DBField):
        u"""Номер отпайки"""

    @integer
    @display(u'Тип')
    class coiltype(DBField):
        u"""Определяет по какой таблице ГОСТа проводятся поверка 8 или 9"""

    @varchar(10)
    @required
    @display(u'Класс точности')
    class classaccuracy(DBField):
        u"""Класс точности определяемый по таблице"""

    @numeric(length=8, precision=2)
    @display(u'Первичный ток')
    class primarycurrent(DBField):
        u"""Номинальный первичный ток"""

    @numeric(length=8, precision=2)
    @display(u'Вторичный ток')
    class secondcurrent(DBField):
        u"""Номинальный вторичный ток"""

    @numeric(length=8, precision=2)
    @required
    @display(u'Вторичная нагрузка')
    class secondload(DBField):
        u"""Номинальная вторичная нагрузка"""

    @numeric(length=8, precision=2)
    @display(u'Напряжение (магн.)')
    class magneticvoltage(DBField):
        u"""Напряжение намагничивания"""

    @numeric(length=8, precision=2)
    @display(u'Ток (магн.)')
    class magneticcurrent(DBField):
        u"""Ток намагничивания. Трансформатор прошел первичную поверку по ГОСТ 8.217-2003"""

    @numeric(length=8, precision=2)
    @display(u'Сопротивление')
    class resistance(DBField):
        u"""Сопротивление постоянному току"""

    @varchar(10)
    @display(u'Коэфф.')
    class rating(DBField):
        u"""Номинальный коэффициент безопасности приборов вторичной обмотки измерения или Номинальная предельная кратность вторичной обмотки защиты. Для измерительных или защитных обмоток соответственно"""

    @numeric(length=8, precision=2)
    @display(u'Четвертная нагрузка')
    class quadroload(DBField):
        u"""Четвертная нагрузка при испытании на 120%"""


@display(u'Состав')
class item(DBTable):
    u"""Состав карты испытания - список серийных номеров проходящих испытание"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @integer
    @reference(u'serial_number')
    @display(u'Cерийный номер')
    class serial_number(DBField):
        u"""Ссылка на серийный номер"""

    @varchar(100)
    @display(u'Наименование')
    class fullname(DBField):
        u"""Уникальное наименование трансформатора"""

    @integer
    @required
    @parent(u'test_map')
    @display(u'Карта испытаний')
    class test_map(DBField):
        u"""Ссылка на карту испытаний"""

    @integer
    @reference(u'defect')
    @display(u'Несоответствие')
    class defect(DBField):
        u"""Ссылка на несоответствие"""

    @boolean
    @required
    @default(u'false')
    @display(u'Испытывался')
    @fk_description
    class IsTested(DBField):
        u""""""


@display(u'Серийный номер')
class serial_number(DBTable):
    u"""Серийные номера трансформаторов"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @varchar(20)
    @required
    @display(u'Заказ')
    class ordernumber(DBField):
        u"""Заказ"""

    @varchar(20)
    @required
    @display(u'Серия')
    class series(DBField):
        u"""Серия"""

    @integer
    @required
    @display(u'Номер')
    @fk_description
    class serialnumber(DBField):
        u"""Заводской номер ротация в рамках года"""

    @integer
    @required
    @display(u'Дата')
    class makedate(DBField):
        u"""Дата изготовления"""

    @integer
    @required
    @parent(u'transformer')
    @display(u'Трансформатор')
    class transformer(DBField):
        u"""Ссылка на Transformer"""

    uniques = [{serialnumber, makedate}]


@display(u'Карта испытаний')
class test_map(DBTable):
    u"""Карта испытаний трансформатора"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @integer
    @required
    @reference(u'operator')
    @display(u'Оператор')
    class operator(DBField):
        u"""Ссылка на оператора"""

    @integer
    @reference(u'operator')
    @display(u'Поверитель')
    class supervisor(DBField):
        u"""Ссылка внешнего поверителя "поверитель ЦСЛ" поле operator.isExternal = True"""

    @integer
    @required
    @reference(u'climat')
    @display(u'Климат (время)')
    class climat(DBField):
        u"""Ссылка на \"Журнал окружающей среды\""""

    @timestamp
    @required
    @default(u'now()')
    @display(u'Дата создания')
    class createdatetime(DBField):
        u""""""

    @timestamp
    @required
    @default(u'now()')
    @display(u'Дата подтверждения')
    class acceptdatetime(DBField):
        u""""""

    @integer
    @required
    @display(u'Стенд')
    @fk_description
    class standnumber(DBField):
        u"""Номер стенда"""

    @boolean
    @display(u'Принято')
    class accepted(DBField):
        u"""Устанавливается после подтверждения оператором правильности всех испытаний в карте. Карты испытаний со снятым флагом игнорируются"""

    uniques = [{operator, standnumber, createdatetime}]


@display(u'Испытательные напряжения')
class testing_voltage(DBTable):
    u"""Справочник испытательных напряжений"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @numeric(length=10, precision=3)
    @required
    @display(u'Номинальное напряжение')
    class nominal_voltage(DBField):
        u""""""

    @char(1)
    @required
    @display(u'Уровень изоляции, А/В')
    class isolation_level(DBField):
        u""""""

    @numeric(length=10, precision=3)
    @display(u'Испытательное напряжение перв.')
    class prime_test_voltage(DBField):
        u""""""

    @numeric(length=10, precision=3)
    @display(u'Испытательное напряжение втор.')
    class second_test_voltage(DBField):
        u""""""

    @numeric(length=10, precision=3)
    @display(u'Испытательное напряжение перв.2')
    class prime_test_voltage2(DBField):
        u""""""

    @numeric(length=10, precision=3)
    @display(u'Уровень ЧР')
    class pd_level(DBField):
        u""""""

@display(u'Команды периферийных устройств')
class device_command(DBTable):
    u"""Сопоставление пар 'тип-значение' и реле периферийных устройств"""

    @integer(autoinc=True)
    @primary_key
    @invisible
    class id(DBField):
        u""""""

    @char(2)
    @required
    @display(u'Тип значения')
    @enum(CR=u'Ток', SG=u'Сигнализация', CL=u'Номер обмотки', MD=u'Режим')
    class type(DBField):
        u""""""

    @integer
    @required
    @display(u'Значение')
    class value(DBField):
        u""""""

    @integer
    @required
    @display(u'Номер устройства')
    class device(DBField):
        u""""""

    @integer
    @required
    @display(u'Номер реле')
    class relay(DBField):
        u""""""

    uniques = [{type, value}]