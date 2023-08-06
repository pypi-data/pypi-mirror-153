create table Metadata (
    id integer primary key autoincrement,
    series_id text not null,
    field_name text not null,
    field_value text,

    unique(series_id, field_name)
);

create table Dictionary (
    id integer primary key autoincrement,
    series_id text not null,
    value integer not null,
    label text not null,

    unique(series_id, value)
);
