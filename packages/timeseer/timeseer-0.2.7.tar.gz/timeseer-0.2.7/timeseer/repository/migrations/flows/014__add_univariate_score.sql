-- depends: 013__series_sets

create table UnivariateScores(
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text not null,
    score_name text not null,
    score float not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);
