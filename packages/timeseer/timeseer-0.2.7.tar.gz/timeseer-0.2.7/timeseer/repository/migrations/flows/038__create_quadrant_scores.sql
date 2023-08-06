-- depends: 037__index_foreign_key

create table QuadrantScores(
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    name text not null,
    score real not null,

    unique(block_evaluation_id, name, score)
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create index quadrant_scores_be_id on QuadrantScores(block_evaluation_id);


