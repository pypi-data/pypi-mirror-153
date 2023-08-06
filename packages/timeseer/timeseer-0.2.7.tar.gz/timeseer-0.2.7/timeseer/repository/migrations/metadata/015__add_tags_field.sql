--depends: 014__clean_audit_trail

create table SeriesTags (
    id integer primary key autoincrement,
    series_id text not null,
    tag_key text not null,
    tag_value text not null,

    unique(series_id, tag_key, tag_value)
);


insert into SeriesTags (series_id, tag_key, tag_value) select series_id, 'series name',  series_name from SeriesNames;

CREATE TABLE new_SeriesNames(
    series_id text primary key,
    series_source text not null,
    series_field text not null,
    removed integer not null default 0
);

insert into new_SeriesNames select series_id, series_source, 'value', removed from SeriesNames;
drop table SeriesNames;
alter table new_SeriesNames rename to SeriesNames;
