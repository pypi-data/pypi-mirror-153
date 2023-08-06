-- depends: 011__block_evaluation_runs

create table FlightExposeBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    name text unique,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);


create table FlowSource (
    id integer primary key autoincrement,
    name text not null,
    block_evaluation_id integer not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);
