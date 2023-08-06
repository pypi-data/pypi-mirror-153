-- depends: 001__create


create table if not exists SeriesSetPattern (
    id integer primary key autoincrement,
    series_set_id integer not null,
    source_name text not null,
    pattern text not null,
    structured integer not null,

    unique(series_set_id, source_name, pattern),
    foreign key (series_set_id) references SeriesSet(id) on delete cascade
);
