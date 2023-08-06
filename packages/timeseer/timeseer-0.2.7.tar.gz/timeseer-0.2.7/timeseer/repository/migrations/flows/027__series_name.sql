-- depends: 026__series_state

alter table Series rename to old_Series;

create table Series (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text not null,
    state text not null,
    series_source text not null,
    series_name text not null,

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade,
    unique (flow_evaluation_id, series_id)
);

drop index series_fe_id;
create index series_fe_id on Series(flow_evaluation_id);
