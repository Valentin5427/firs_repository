create table meta_table
(
TableName varchar(100) not null CONSTRAINT pkey_meta_table PRIMARY KEY
, Alias varchar(200) not null
, NonAutoCreate bool not null default true
, Description Text
);


create table meta_field
(
meta_table varchar(100) references meta_table(TableName) not null
, Field varchar(100) not null
, Alias varchar(200)
, Visible bool not null
, Description Text
, RefAlias varchar(100)
, RefShowField varchar(100)
);

