-- depends: 015__add_trendminer_expose_block

create table FlowEvaluationGroups (
    id integer primary key autoincrement,
    flow_id integer not null,
    start_date datetime not null,
    end_date datetime not null,
    evaluation_date datetime not null,

    foreign key (flow_id) references Flows(id) on delete cascade
);

drop table FlowEvaluations;

create table FlowEvaluations (
    id integer primary key autoincrement,
    group_id integer not null,
    series_set_name text not null,

    foreign key (group_id) references FlowEvaluationGroups(id) on delete cascade
);
