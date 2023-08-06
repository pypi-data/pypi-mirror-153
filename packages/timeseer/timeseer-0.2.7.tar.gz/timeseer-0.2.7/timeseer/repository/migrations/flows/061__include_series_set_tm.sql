-- depends: 060__univariate_series_state

drop table TrendMinerFlow;

create table TrendMinerFlow (
    id integer primary key autoincrement,
    name text not null unique,
    prefix text not null unique,
    block_evaluation_id integer not null,
    flow_id integer not null,
    series_set_name text not null,
    block_name text not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (flow_id) references Flows(id) on delete cascade
);

create index tm_flow_be_id on TrendMinerFlow(block_evaluation_id);
