-- depends: 007__series_set_tag_patterns

create table new_SeriesSetTemplates(
    id integer primary key autoincrement,
    name text not null unique,
    name_pattern text not null,
    source_name text not null,
    field_grouping_pattern text not null,
    origin text not null,
    removed integer not null default 0
);


insert into new_SeriesSetTemplates (id, name, name_pattern, source_name, field_grouping_pattern, origin, removed)
select id, name, name_pattern, source_name, '*', origin, removed from SeriesSetTemplates;

create table temp_SeriesSetTemplates (
    id integer primary key autoincrement,
    name text not null unique,
    name_pattern text not null,
    source_name text not null,
    grouping_pattern text not null, 
    origin text not null,
    removed integer not null default 0
);

insert into temp_SeriesSetTemplates select * from SeriesSetTemplates;

drop table SeriesSetTemplates;
alter table new_SeriesSetTemplates rename to SeriesSetTemplates;

create table SeriesSetTemplateTagFilters(
    id integer primary key autoincrement,
    template_id integer not null,
    tag_key text not null,
    tag_pattern text not null,

    foreign key (template_id) references SeriesSetTemplates(id) on delete cascade
);

insert into SeriesSetTemplateTagFilters (template_id, tag_key, tag_pattern) 
select id, 'series name', grouping_pattern from temp_SeriesSetTemplates;

drop table temp_SeriesSetTemplates;