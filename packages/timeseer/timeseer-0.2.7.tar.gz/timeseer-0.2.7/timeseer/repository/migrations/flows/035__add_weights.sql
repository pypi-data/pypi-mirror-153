-- depends: 034__add_weight_sets

alter table FlowEvaluationGroups add column weight_set_name text default 'default';

create table ScoreWeights(
    id integer primary key autoincrement,
    group_id integer not null,
    score_name text not null,
    score_weight real not null,

    foreign key (group_id) references FlowEvaluationGroups(id) on delete cascade
);
