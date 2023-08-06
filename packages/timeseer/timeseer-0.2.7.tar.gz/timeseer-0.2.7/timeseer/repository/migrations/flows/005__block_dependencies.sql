-- depends: 004__add_flow_evaluation_dates

alter table BlockExecutionDependencies rename to old_BlockExecutionDependencies;

create table BlockExecutionDependencies (
    id integer primary key autoincrement,
    block_execution_id integer not null,
    dependency_block_execution_id integer not null,

    unique(block_execution_id, dependency_block_execution_id)
    foreign key (block_execution_id) references BlockExecutions(id) on delete cascade
    foreign key (dependency_block_execution_id) references BlockExecutions(id) on delete cascade
);

insert into BlockExecutionDependencies
select id, block_execution_id, (select id from BlockExecutions where block_id = dependency_block_id)
from old_BlockExecutionDependencies;

drop table old_BlockExecutionDependencies;
