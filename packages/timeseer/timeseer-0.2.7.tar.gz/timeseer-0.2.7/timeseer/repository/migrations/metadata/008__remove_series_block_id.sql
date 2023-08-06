-- depends: 007__add_series_block_id

delete from SeriesNames where block_id is not NULL;

alter table SeriesNames rename to old_SeriesNames;

create table SeriesNames(
    series_id text primary key,
    series_source text not null,
    series_name text not null,
    removed integer not null default 0,

    unique(series_source, series_name)
);

insert into SeriesNames
select series_id, series_source, series_name, removed
from old_SeriesNames;

drop table old_SeriesNames;
