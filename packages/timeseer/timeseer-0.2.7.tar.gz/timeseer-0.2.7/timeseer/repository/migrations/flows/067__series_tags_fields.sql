--depends: 066__remove_foreign_keys

CREATE TABLE new_Series (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text not null,
    state text not null,
    series_source text not null,
    series_field text not null default 'value',

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade,
    unique (flow_evaluation_id, series_id)
);

insert into new_Series (id, flow_evaluation_id, series_id, state, series_source, series_field)
select id, flow_evaluation_id, series_id, state, series_source, 'value' from Series;


create table SeriesTags (
    id integer primary key autoincrement,
    evaluation_series_id integer not null,
    tag_key text not null,
    tag_value text not null,

    unique(evaluation_series_id, tag_key, tag_value)
);

insert into SeriesTags (evaluation_series_id, tag_key, tag_value) select id, 'series name',  series_name from Series;

drop table Series;

alter table new_Series rename to Series;