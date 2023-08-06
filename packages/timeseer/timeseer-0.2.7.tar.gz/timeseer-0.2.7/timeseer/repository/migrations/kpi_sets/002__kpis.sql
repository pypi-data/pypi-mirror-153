--depends: 001__create

create table KPIs (
    id integer primary key autoincrement,
    name text not null unique,
    origin text not null
);

create table KPIWeights (
    id integer primary key autoincrement,
    kpi_id integer not null,
    score_name text not null,
    score_weight real not null,

    unique(kpi_id, score_name),
    foreign key (kpi_id) references KPIs(id) on delete cascade
);