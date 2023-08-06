-- depends: 040__update_excel_exports

create table DataServiceExposeBlockInput (
    id integer primary key autoincrement,
    block_configuration_id integer not null,
    pattern text,

    foreign key (block_configuration_id) references BlockConfigurations(id) on delete cascade
);


create table FlowDataService (
    id integer primary key autoincrement,
    name text not null unique,
    block_evaluation_id integer not null,
    flow_id integer not null,
    series_set_name text,
    block_configuration_id integer not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (flow_id) references Flows(id) on delete cascade,
    foreign key (block_configuration_id) references BlockConfigurations(id) on delete cascade
);
