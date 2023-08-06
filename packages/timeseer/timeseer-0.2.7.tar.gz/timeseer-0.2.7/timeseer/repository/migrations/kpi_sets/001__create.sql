create table WeightSets (
    id integer primary key autoincrement,
    name text not null,

    unique(name)
);

create table ScoreWeightOverrides (
    id integer primary key autoincrement,
    weight_set_id integer not null,
    score_name text not null,
    score_weight real not null,

    unique(score_name)
    foreign key (weight_set_id) references WeightSets(id) on delete cascade
);

