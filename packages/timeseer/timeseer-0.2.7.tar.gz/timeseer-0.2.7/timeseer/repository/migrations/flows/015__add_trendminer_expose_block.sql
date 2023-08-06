-- depends: 014__add_univariate_score

create table TrendMinerExposeBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    name text unique,
    prefix text unique,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);


create table TrendMinerFlow (
    id integer primary key autoincrement,
    name text not null,
    prefix text not null unique,
    block_evaluation_id integer not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);
