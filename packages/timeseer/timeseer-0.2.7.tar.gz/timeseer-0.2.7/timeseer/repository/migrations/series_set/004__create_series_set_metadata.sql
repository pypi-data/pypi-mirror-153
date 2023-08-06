create table if not exists SeriesSetMetadata (
    id integer primary key autoincrement,
    series_set_id integer not null,
    field_name text not null,
    field_value text,

    unique(series_set_id, field_name),
    foreign key (series_set_id) references SeriesSet(id) on delete cascade
);

create table if not exists SeriesSetTemplateMetadata (
    id integer primary key autoincrement,
    series_set_template_id integer not null,
    field_name text not null,
    field_value text,

    unique(series_set_template_id, field_name),
    foreign key (series_set_template_id) references SeriesSetTemplates(id) on delete cascade
);

