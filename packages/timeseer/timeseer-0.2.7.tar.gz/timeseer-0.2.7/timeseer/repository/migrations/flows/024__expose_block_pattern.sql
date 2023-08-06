-- depends: 022__series_set_template_references 023__drop_block_dependencies

alter table FlightExposeBlockInput rename to FlightExposeBlockInput_old;

create table FlightExposeBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    pattern text,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);

insert into FlightExposeBlockInput (id, block_id, pattern)
select id, block_id, '%s' from FlightExposeBlockInput_old;

drop table FlightExposeBlockInput_old;

drop table FlowSource;

create table FlowSource (
    id integer primary key autoincrement,
    flow_id integer not null,
    series_set_name text not null,
    block_configuration_id integer not null,
    block_evaluation_id integer not null,
    name text not null unique,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (flow_id) references Flows(id) on delete cascade,
    foreign key (block_configuration_id) references BlockConfigurations(id) on delete cascade
);
