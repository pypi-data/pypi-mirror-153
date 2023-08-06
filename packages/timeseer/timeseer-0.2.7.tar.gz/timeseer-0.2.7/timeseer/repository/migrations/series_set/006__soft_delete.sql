-- depends: 005__add_resource_origin

alter table SeriesSet add column removed integer not null default 0;
alter table SeriesSetTemplates add column removed integer not null default 0;