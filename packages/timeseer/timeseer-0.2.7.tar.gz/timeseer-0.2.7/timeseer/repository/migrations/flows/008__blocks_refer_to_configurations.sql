-- depends: 007__index_foreign_keys

alter table Blocks rename to Blocks_old;
alter table BlockDependencies rename to BlockDependencies_old;

create table Blocks (
    id integer primary key autoincrement,
    flow_id integer not null,
    configuration_id integer not null,

    foreign key (flow_id) references Flows(id) on delete cascade,
    foreign key (configuration_id) references BlockConfigurations(id) on delete cascade
);

create table BlockDependencies (
    id integer primary key autoincrement,
    block_id integer not null,
    dependency_block_id integer not null,

    unique(block_id, dependency_block_id)
    foreign key (block_id) references Blocks(id) on delete cascade
    foreign key (dependency_block_id) references Blocks(id) on delete cascade
);

insert into Blocks
select * from Blocks_old;

insert into BlockDependencies
select * from BlockDependencies_old;

drop table Blocks_old;
drop table BlockDependencies_old;
