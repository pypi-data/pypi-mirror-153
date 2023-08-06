
create table SeriesSetTemplates(
    id integer primary key autoincrement,
    name text not null unique,
    name_pattern text not null,
    source_name text not null,
    grouping_pattern text not null
);

create table SeriesSetTemplateMetadataFilters(
    id integer primary key autoincrement,
    template_id integer not null,
    metadata_field text not null,
    filter_pattern text not null,

    foreign key (template_id) references SeriesSetTemplates(id) on delete cascade
);
