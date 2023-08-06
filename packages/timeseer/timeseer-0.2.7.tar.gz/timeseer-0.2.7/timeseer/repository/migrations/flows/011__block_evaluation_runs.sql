-- depends: 010__block_evaluations

drop table FlowEvaluationLimitations;

create table BlockEvaluationRuns (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table BlockEvaluationRunLimits (
    id integer primary key autoincrement,
    block_evaluation_run_id integer not null,
    "limit" text not null,

    foreign key (block_evaluation_run_id) references BlockEvaluationRuns(id) on delete cascade
);
