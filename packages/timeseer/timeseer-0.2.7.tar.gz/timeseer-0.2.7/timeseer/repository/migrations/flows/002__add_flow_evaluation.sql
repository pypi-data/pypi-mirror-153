-- depends: 001__create

drop table FlowExecutionDependencies;
drop table SeriesSetBlockOutput;
drop table EventFrames;
drop table Checks;
drop table CalculatedMetadata;
drop table Statistics;
drop table FilterBlockOutput;
drop table Scores;

drop table BivariateChecks;

alter table FlowExecutions rename to BlockExecutions;

create table FlowEvaluation (
    id integer primary key autoincrement,
    flow_id integer not null,
    evaluation_date datetime not null,

    foreign key (flow_id) references Flows(id) on delete cascade
);

create table BlockExecutionDependencies (
    id integer primary key autoincrement,
    block_execution_id integer not null,
    dependency_block_id integer not null,

    unique(block_execution_id, dependency_block_id),
    foreign key (block_execution_id) references BlockExecutions(id) on delete cascade
);

create table SeriesSetBlockOutput (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text not null,

    unique(flow_evaluation_id, series_id),
    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table EventFrames (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table Checks (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text,
    check_name text not null,
    check_result real not null,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table CalculatedMetadata (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text,
    field_name text not null,
    field_result text not null,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table Statistics (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text,
    statistic_name text not null,
    statistic_type text not null,
    statistic_result text not null,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table FilterBlockOutput (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text not null,

    unique(flow_evaluation_id, series_id),
    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table Scores (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text,
    score_name text not null,
    score float not null,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

create table BivariateChecks (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    check_name text not null,
    check_result real not null,
    series_x_id text not null,
    series_y_id text not null,

    unique(flow_evaluation_id, check_name, series_x_id, series_y_id),
    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);

