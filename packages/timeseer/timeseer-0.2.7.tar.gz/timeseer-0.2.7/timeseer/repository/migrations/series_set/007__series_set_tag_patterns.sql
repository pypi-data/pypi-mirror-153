-- depends: 006__soft_delete

create table new_SeriesSetPattern (
    id integer primary key autoincrement,
    series_set_id integer not null,
    source_name text not null,
    field_pattern text not null,
    structured integer not null,

    foreign key (series_set_id) references SeriesSet(id) on delete cascade
);

insert into new_SeriesSetPattern (id, series_set_id, source_name, field_pattern, structured)
select id, series_set_id, source_name, '*', structured from SeriesSetPattern;

create table temp_SeriesSetPattern (
    id integer primary key autoincrement,
    series_set_id integer not null,
    source_name text not null,
    pattern text not null,
    structured integer not null,

    foreign key (series_set_id) references SeriesSet(id) on delete cascade
);

insert into temp_SeriesSetPattern select * from SeriesSetPattern;

drop table SeriesSetPattern;
alter table new_SeriesSetPattern rename to SeriesSetPattern;


create table SeriesSetTagPatterns (
    id integer primary key autoincrement,
    series_set_pattern_id integer not null,
    pattern_key text not null,
    pattern_value text not null,

    unique(series_set_pattern_id, pattern_key, pattern_value),
    foreign key (series_set_pattern_id) references SeriesSetPattern(id) on delete cascade
);

insert into SeriesSetTagPatterns (series_set_pattern_id, pattern_key, pattern_value) 
select id, 'series name', pattern from temp_SeriesSetPattern;

drop table temp_SeriesSetPattern;
