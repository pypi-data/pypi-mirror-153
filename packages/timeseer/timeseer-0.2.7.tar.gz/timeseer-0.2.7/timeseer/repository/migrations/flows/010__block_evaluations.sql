-- depends: 009__analysis_modules

create table BlockEvaluations (
    id integer primary key autoincrement,
    block_id integer not null,
    flow_evaluation_id integer not null,

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade,
    foreign key (block_id) references Blocks(id) on delete cascade
);

drop table Exports;
drop table SeriesSetBlockOutput;
drop table EventFrames;
drop table Checks;
drop table CalculatedMetadata;
drop table Statistics;
drop table BivariateChecks;
drop table FilterBlockOutput;
drop table Scores;

create table Exports (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    filename text not null,
    file blob not null,
    date datetime not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);


create table SeriesSetBlockOutput (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table EventFrames (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table Checks (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text,
    check_name text not null,
    check_result real not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table CalculatedMetadata (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text ,
    field_name text not null,
    field_result text not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table Statistics (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text,
    statistic_name text not null,
    statistic_type text not null,
    statistic_result text not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table BivariateChecks (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    check_name text not null,
    check_result real not null,
    series_x_id text not null,
    series_y_id text not null,

    unique(block_evaluation_id, check_name, series_x_id, series_y_id),
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table FilterBlockOutput (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table Scores (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text,
    score_name text not null,
    score float not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create index filter_output_fe_id on FilterBlockOutput(block_evaluation_id);
create index seriesset_output_fe_id on SeriesSetBlockOutput(block_evaluation_id);

create index bivariate_fe_id on BivariateChecks(block_evaluation_id);
create index calculated_metadata_fe_id on CalculatedMetadata(block_evaluation_id);
create index checks_fe_id on Checks(block_evaluation_id);
create index eventframes_fe_id on EventFrames(block_evaluation_id);
create index statistics_fe_id on Statistics(block_evaluation_id);

create index exports_fe_id on Exports(block_evaluation_id);
create index scores_fe_id on Scores(block_evaluation_id);
