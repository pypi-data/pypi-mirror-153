-- depends: 006__index

alter table SeriesNames rename to old_SeriesNames;

create table SeriesNames(
    series_id text primary key,
    series_source text not null,
    series_name text not null,
    block_id integer,
    removed integer not null default 0,

    unique(series_source, series_name, block_id)
);

insert into SeriesNames
select series_id, series_source, series_name, NULL, removed
from old_SeriesNames;

drop table old_SeriesNames;
