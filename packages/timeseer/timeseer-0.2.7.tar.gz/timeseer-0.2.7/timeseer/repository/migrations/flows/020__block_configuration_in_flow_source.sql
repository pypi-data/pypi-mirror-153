-- depends: 013__add_flight_expose_block 019__add_event_frame_reference

drop table FlowSource;

create table FlowSource (
    id integer primary key autoincrement,
    name text not null unique,
    block_configuration_id integer not null,
    block_evaluation_id integer not null,

    foreign key (block_configuration_id) references BlockConfigurations(id) on delete cascade,
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);
