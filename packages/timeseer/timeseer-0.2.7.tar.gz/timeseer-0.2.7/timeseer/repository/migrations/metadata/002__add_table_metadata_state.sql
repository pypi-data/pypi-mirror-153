-- depends: 001__create

create table if not exists MetadataRuns (
    id integer primary key autoincrement,
    series_source text not null,
    series_id text,
    state text not null,

    unique(series_source, series_id)
);
