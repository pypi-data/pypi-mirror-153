-- depends: 003__add_exports

drop table FlowEvaluation;

create table FlowEvaluation (
    id integer primary key autoincrement,
    flow_id integer not null,
    start_date datetime not null,
    end_date datetime not null,
    evaluation_date datetime not null,

    foreign key (flow_id) references Flows(id) on delete cascade
);

delete from SeriesSetBlockOutput;
delete from EventFrames;
delete from Checks;
delete from CalculatedMetadata;
delete from Statistics;
delete from FilterBlockOutput;
delete from Scores;
delete from BivariateChecks;
delete from Exports;

