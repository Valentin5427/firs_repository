--truncate table meta_table cascade;
insert into meta_table
(Description , Alias, TableName , NonAutoCreate)
select
'Основные технические данные трансформатора', 'Трансформатор', 'transformer', False
union all select
'Технические данные вторичных обмоток трансформатора', 'Вторичная обмотка', 'coil', False
union all select
'Серийные номера трансформаторов', 'Серийный номер', 'serial_number', False
union all select
'Справочник несоответствий', 'Несоответствия', 'defect', False
union all select
'Справочник операторов испятательных стендов', 'Операторы', 'operator', False
union all select
'Журнал окружающей среды', 'Окружающая среда', 'climat', False
union all select
'Карта испытаний трансформатора', 'Карта испытаний', 'test_map', False
union all select
'Состав карты испытания - список серийных номеров проходящих испытание', 'Состав', 'item', False
union all select
'Данные полученные в результате поверки на КНТ-05', 'Результаты поверки', 'checking', False
;


insert into meta_field
(meta_table, Field, Alias, Description, Visible, RefShowField)
select 'transformer', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'transformer', 'FullName', 'наименование', 'Уникальное наименование трансформатора', True, Null
union all select 'transformer', 'Standart', 'Стандарт', Null, True, Null
union all select 'transformer', 'Voltage', 'Номинальное напряжение', Null, True, Null
union all select 'transformer', 'MaxOperVoltage', 'Наибольшее рабочее напряжение', Null, True, Null
union all select 'transformer', 'PrimaryCurrent', 'Номинальный первичный ток', Null, True, Null
union all select 'transformer', 'SecondCurrent', 'Номинальный вторичный ток', Null, True, Null
union all select 'transformer', 'Frequency', 'Номинальная частота', Null, True, Null
union all select 'transformer', 'QuantSecondCoil', 'Число вторичных обмоток', Null, True, Null
union all select 'transformer', 'TestVoltagePrimaryCoil', 'Испытательное напряжение первичной обмотки', Null, True, Null
union all select 'transformer', 'TestVoltageSecondaryCoil', 'Испытательное напряжение вторичных обмоток', Null, True, Null
union all select 'transformer', 'IsolationLevel', 'Уровень изоляции', Null, True, Null
union all select 'transformer', 'Climat', 'Климатическое исполнение и категория размещения', Null, True, Null
union all select 'transformer', 'Weight', 'Масса трансформатора', 'не более', True, Null
union all select 'coil', 'transformer', Null  , 'Ссылка на Transformer', True, 'FullName'
union all select 'coil', 'CoilType', 'Тип', 'Определяет по какой таблице ГОСТа проводятся поверка 8 или 9', True, Null
union all select 'coil', 'ClassAccuracy', 'Класс точности', 'по таблице можно определить', True, Null
union all select 'coil', 'SecondCurrent', 'Номинальный вторичный ток', Null, True, Null
union all select 'coil', 'SecondLoad', 'Номинальная вторичная нагрузка', Null, True, Null
union all select 'coil', 'MagneticVoltage', 'Напряжение намагничивания', Null, True, Null
union all select 'coil', 'MagneticCurrent', 'Ток намагничивания', 'Трансформатор прошел первичную поверку по ГОСТ 8.217-2003', True, Null
union all select 'coil', 'Resistance', 'Сопротивление постоянному току', Null, True, Null
union all select 'coil', 'Rating', 'Коэффициент', 'Номинальный коэффициент безопасности приборов вторичной обмотки измерения или Номинальная предельная кратность вторичной обмотки защиты. Для измерительных или защитных обмоток соответственно', True, Null
union all select 'serial_number', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'serial_number', 'transformer', Null  , 'Ссылка на Transformer', True, 'FullName'
union all select 'serial_number', 'SerialNumber', 'Номер', 'Заводской номер ротация в рамках года', True, Null
union all select 'serial_number', 'MakeDate', 'Дата', 'Дата изготовления', True, Null
union all select 'defect', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'defect', 'DefectType', 'Тип', 'Тип несоответствия (перечислитель)', True, Null
union all select 'defect', 'IsCritical', 'Критичность', 'Подлежит ремонту или нет', True, Null
union all select 'defect', 'ShortName', 'Краткое наименование', Null, True, Null
union all select 'defect', 'FullName', 'Полное наименование', Null, True, Null
union all select 'defect', 'Description', 'Описание', Null, True, Null
union all select 'operator', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'operator', 'FIO', 'Фамилия И O', 'Строковый идентификатор', True, Null
union all select 'operator', 'Family', 'Фамилия', Null, True, Null
union all select 'operator', 'FirstName', 'Имя', Null, True, Null
union all select 'operator', 'SecondName', 'Отчество', Null, True, Null
union all select 'operator', 'isExternal', 'Не сотрудник', 'Признак внешнего (не является сотрудником предприятия) поверителя используется в печатных формах', True, Null
union all select 'climat', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'climat', 'operator', Null  , 'Ссылка на оператора', True, Null
union all select 'climat', 'Temperature', 'Темература', 'Темература в градусах по цельсию согласно ГОСТ от 15 до 35', True, Null
union all select 'climat', 'Humidity', 'Влажность', 'Влажность в процентах согласно ГОСТ от 30 до 80', True, Null
union all select 'climat', 'Pressure', 'Давление', 'Давление в кПа от согласно ГОСТ 85 до 105', True, Null
union all select 'climat', 'LastUpdate', 'Время', 'Время последнего изменения согласно ГОСТ 3 раза не позднее 08:00', True, Null
union all select 'test_map', 'ID', Null  , 'Первичный ключ', True, Null
union all select 'test_map', 'operator', 'Оператор', 'Ссылка на оператора', True, 'FIO'
union all select 'test_map', 'supervisor', 'Поверитель', 'Ссылка внешнего поверителя "поверитель ЦСЛ" поле operator.isExternal = True', True, 'FIO'
union all select 'test_map', 'climat', Null  , 'Ссылка на "Журнал окружающей среды"', False, Null
union all select 'test_map', 'CreateDateTime', 'Время создания', Null, True, Null
union all select 'test_map', 'StandNumber', 'Стенд', 'Номер стенда', True, Null
union all select 'test_map', 'Accepted', 'Испытания приняты', 'Устанавливается после подтверждения оператором правильности всех испытаний в карте. Карты испытаний со снятым флагом игнорируются', True, Null
union all select 'item', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'item', 'serial_number', 'Cерийный номер', 'Ссылка на серийный номер', True, 'SerialNumber'
union all select 'item', 'test_map', Null  , 'Ссылка на карту испытаний', False, Null
union all select 'item', 'defect', 'Несоответствие', 'Ссылка на несоответствие', True, 'ShortName'
union all select 'item', 'IsTested', 'Испытывался', Null, True, Null
union all select 'checking', 'ID', Null  , 'Первичный ключ', False, Null
union all select 'checking', 'item', Null  , 'Ссылка на изделие', False, Null
union all select 'checking', 'coil', Null  , 'Ссылка на испытываемую обмотку', False, Null
union all select 'checking', 'ChekTimeStamp', 'Время', 'Времянная метка измерения', True, Null
union all select 'checking', 'A', Null  , 'амплитудная ошибка поверяемого трансформатора тока', True, Null
union all select 'checking', 'P', Null  , 'угловая ошибка поверяемого трансформатора тока', True, Null
union all select 'checking', 'I', Null  , 'вторичный ток образцового трансформатора', True, Null
union all select 'checking', 'N', Null  , 'номинальный вторичный ток образцового и поверяемого трансформатора', True, Null
union all select 'checking', 'F', Null  , 'частота вторичного тока образцового трансформатора', True, Null
union all select 'checking', 'K', Null  , 'коэффициент несинусоидальности вторичного тока образцового трансформатора', True, Null
;
