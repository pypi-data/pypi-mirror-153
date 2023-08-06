create table SensorSpecs (
    id integer primary key autoincrement,
    series_id text not null,
    field_name text not null,
    field_value text,

    unique(series_id, field_name)
);
