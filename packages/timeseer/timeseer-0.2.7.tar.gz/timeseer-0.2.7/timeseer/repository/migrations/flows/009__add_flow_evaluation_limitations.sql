-- depends: 008__blocks_refer_to_configurations

create table FlowEvaluationLimitations (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    limitation text not null,
    evaluation_date datetime,
    has_run boolean not null default 0,

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade
);

