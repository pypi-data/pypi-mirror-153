-- depends: 005__block_dependencies

alter table FlowEvaluation rename to FlowEvaluations;

alter table Blocks rename to BlockConfigurations;

alter table BlockExecutions rename to Blocks;

create table BlockDependencies (
    id integer primary key autoincrement,
    block_id integer not null,
    dependency_block_id integer not null,

    unique(block_id, dependency_block_id)
    foreign key (block_id) references Blocks(id) on delete cascade
    foreign key (dependency_block_id) references Blocks(id) on delete cascade
);

insert into BlockDependencies
select * from BlockExecutionDependencies;

drop table BlockExecutionDependencies;
