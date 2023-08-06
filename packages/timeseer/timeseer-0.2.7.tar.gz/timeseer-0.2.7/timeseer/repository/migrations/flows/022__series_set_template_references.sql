-- depends: 020__block_configuration_in_flow_source 021__drop_score_table

create table SeriesSetTemplateReferences (
    id integer primary key autoincrement,
    flow_id integer not null,
    series_set_template_id integer not null,

    foreign key (flow_id) references Flows(id) on delete cascade,
    unique (flow_id, series_set_template_id)
);
