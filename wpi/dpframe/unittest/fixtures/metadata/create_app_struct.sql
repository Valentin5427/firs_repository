create table operator /*Справочник операторов*/
(
    ID serial PRIMARY KEY
    , FIO varchar(50) not null /*Фамилия И O. (Отображаемое поле)*/
    , Family varchar(30) not null /*Фамилия*/
    , FirstName varchar(30) not null /*Имя*/
    , SecondName varchar(30) not null /*Отчество*/
    , isExternal bool not null  /*Признак внешнего (не является сотрудником предприятия) поверителя*/
);

create table defect /*Справочник несоответствий*/
(
    ID serial PRIMARY KEY
    , DefectType int /*Тип несоответствия (перечеслитель)*/
    , IsCritical bool /*Критичность, подлежит ремонту или нет*/
    , ShortName varchar(10) not null /*Краткое наименование*/
    , FullName varchar(100) /*Полное наименование*/
    , Description text /*Описание*/
);

create table climat /*Журнал климата*/
(
    ID serial PRIMARY KEY
    , operator int references operator(ID) not null /*Ссылка на оператора*/
    , Temperature decimal(3, 1) not null /*Темература в градусах по цельсию согласно ГОСТ от 15 до 35*/
    , Humidity decimal(3, 1) not null /*Влажность в процентах согласно ГОСТ от 30 до 80*/
    , Pressure decimal(4, 1) not null /*Давление в кПа от согласно ГОСТ 85 до 105*/
    , LastUpdate timestamp DEFAULT(current_timestamp) not null /*Время последнего изменения согласно ГОСТ 3 раза не позднее 08:00, 12:00, 16:00*/ 
    , CONSTRAINT CTemperature CHECK (Temperature >= 15 and Temperature <= 35)
    , CONSTRAINT CHumidity CHECK (Humidity >= 30 and Humidity <= 80)
    , CONSTRAINT CPressure CHECK (Pressure >= 85 and Pressure <= 105)
);

create table transformer /*ОСНОВНЫЕ ТЕХНИЧЕСКИЕ ДАННЫЕ*/
(
    ID serial PRIMARY KEY
    , FullName varchar(100) /*наименование - ТРАНСФОРМАТОР ТОКА  ТЛП-10-2 М1АC-0.5/10P-10/15-300/5 У3 б 20кА */
    , Standart  varchar(100) /* Стандарт - ТУ 3414-003-52889537-05 */
    , Voltage decimal(4, 2) /* Номинальное напряжение, кВ */
    , MaxOperVoltage decimal(4, 2) /* Наибольшее рабочее напряжение, кВ */
    , PrimaryCurrent decimal(4, 2) /* Номинальный первичный ток, А <Поверка> */
    , SecondCurrent decimal(4, 2)/* Номинальный вторичный ток, А */
    , Frequency int /* Номинальная частота, Гц */
    /* , QuantSecondCoil  Число вторичных обмоток */
    , TestVoltagePrimaryCoil int /* Испытательное напряжение первичной обмотки 42 кВ  50 Гц */
    , TestVoltageSecondaryCoil int /* Испытательное напряжение вторичных обмоток  3 кВ 50 Гц */
    , IsolationLevel char /* Уровень изоляции */
    , Climat char /* Климатическое исполнение и категория размещения */
    , Weight decimal(4, 2)/* Масса трансформатора, кг (не более) */
);

create table coil /*Вторичные обмотки*/
(
    ID serial PRIMARY KEY
    , transformer int references transformer(ID) not null /*ССылка на трансформатор */
    , CoilType int /* Тип Измерительная/Защитная (Определяет по какой таблице ГОСТа проводятся поверка 8 или 9) <Поверка> */
    , ClassAccuracy int /* Класс точности (по таблице можно определить, по первой колонке таблиц 8 и 9) <Поверка> */
    , SecondCurrent decimal(4, 2)/* Номинальный вторичный ток <Поверка> */
    , SecondLoad decimal(4, 2) /* Номинальная вторичная нагрузка, ВА <Поверка> */
    , MagneticVoltage decimal(4, 2) /* Напряжение намагничивания, В   */
    , MagneticCurrent decimal(4, 2) /* Ток намагничивания, А (Трансформатор прошел первичную поверку по ГОСТ 8.217-2003) */
    , Resistance decimal(4, 2) /* Сопротивление постоянному току, мОм  */
    , Rating decimal(4, 2) /* Номинальный коэффициент безопасности приборов вторичной обмотки измерения,  Кб ном (FS) не более (Только для измерительно) ИЛИ Номинальная предельная кратность вторичной обмотки защиты, Кном не менее: (Только для защитной) */
);

create table serial_number /*Список серийных номеров*/
(
    ID serial PRIMARY KEY
    , SerialNumber int /*Заводской номер, ротация в рамках года*/
    , MakeDate date /*Дата изготовления*/
    , transformer int references transformer(ID) not null /*ССылка на трансформатор */
);

create table test_map /*Карта испытаний*/
(
    ID serial PRIMARY KEY
    , operator int references operator(ID) not null /*Ссылка на оператора*/
    , supervisor int references operator(ID) not null /*Ссылка на оператора "поверитель ЦСЛ" поле operator.isExternal = True*/
    , climat int references climat(ID) not null /*Ссылка на оператора "Журнал климата"*/
    , CreateDateTime timestamp DEFAULT(current_timestamp) not null /*Время создания*/ 
    , StandNumber int not null /*Номер стенда, на данном этапе берется из INI файла*/ 
    , Accepted bool null /*Испытания приняты*/
);

create table item /*Изделие в составе карты испытания*/
(
    ID serial PRIMARY KEY
    , serial_number int references serial_number(ID) /*Ссылка на серийный номер*/
    , test_map int references test_map(ID) not null /*Ссылка на карту испытаний*/
    , defect int references defect(ID) null /*Ссылка на несоответствие*/
    , IsTested bool not null /*Испытывался*/
);

create table checking /*Результаты поверки на КНТ-05 Режим TT - Поверка трансформаторов тока*/
(
    ID serial PRIMARY KEY
    , item int references item(ID) not null /*Ссылка на изделие*/
    , coil int references coil(ID) not null /*Ссылка на испытываемую обмотку*/
    , ChekTimeStamp timestamp not null /*Времянная метка измерения*/ 
    , A decimal(4, 3) not null /*амплитудная ошибка поверяемого трансформатора тока*/
    , P decimal(4, 3) not null /*угловая ошибка поверяемого трансформатора тока*/
    , I decimal(4, 3) not null /*вторичный ток образцового трансформатора*/
    , N decimal(4, 3) not null /*номинальный вторичный ток образцового и поверяемого трансформатора*/
    , F decimal(4, 3) not null /*частота вторичного тока образцового трансформатора*/
    , K decimal(4, 3) not null /*коэффициент несинусоидальности вторичного тока образцового трансформатора*/
);
