-- depends: 054__resource_origin

alter table Flows add column removed integer not null default 0;