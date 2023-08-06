create table if not exists SeriesSet (
    id integer primary key autoincrement,
    name text not null unique
);

create table if not exists SeriesSetSeries (
    id integer primary key autoincrement,
    series_set_id integer not null,
    series_id text not null,

    unique(series_set_id, series_id),
    foreign key (series_set_id) references SeriesSet(id) on delete cascade
);

