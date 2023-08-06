-- depends: 011__block_evaluation_runs

create table ReportBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    report text not null,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);

create table ExportBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    export text not null,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);

insert into ReportBlockInput (id, block_id, report)
select id, block_id, 'report' from OutputBlockInput where output = 'REPORT';

insert into ExportBlockInput (id, block_id, export)
select id, block_id, 'export' from OutputBlockInput where output = 'EXPORT';

update BlockConfigurations set type = 'REPORT' where type ='OUTPUT';
delete from Exports;

drop table OutputBlockInput;
