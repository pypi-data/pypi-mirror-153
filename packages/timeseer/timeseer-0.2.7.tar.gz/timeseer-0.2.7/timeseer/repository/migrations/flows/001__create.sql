create table Flows (
    id integer primary key autoincrement,
    name text not null,
    start_date datetime,
    end_date datetime,
    relative_date text,

    unique(name)
);

create table FlowExecutions (
    id integer primary key autoincrement,
    flow_id integer not null,
    block_id integer not null,

    foreign key (flow_id) references Flows(id) on delete cascade,
    foreign key (block_id) references Blocks(id) on delete cascade
);

create table FlowExecutionDependencies (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    dependency_block_id integer not null,

    unique(flow_execution_id, dependency_block_id)
    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table Blocks (
    id integer primary key autoincrement,
    type text not null
);

create table SeriesSetBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    series_set_id integer not null,

    foreign key (block_id) references Blocks(id) on delete cascade
);

create table SeriesSetBlockOutput (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table UnivariateBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    analysis_type text not null,

    foreign key (block_id) references Blocks(id) on delete cascade
);

create table EventFrames (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table Series_EventFrame (
    id integer primary key autoincrement,
    series_source text not null,
    series_id text not null,
    event_frame_id integer not null,

    foreign key (event_frame_id) references EventFrames(id) on delete cascade
);

create table Checks (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text,
    check_name text not null,
    check_result real not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table CalculatedMetadata (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text ,
    field_name text not null,
    field_result text not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table Statistics (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text,
    statistic_name text not null,
    statistic_type text not null,
    statistic_result text not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table MultivariateBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    analysis_type text not null,

    foreign key (block_id) references Blocks(id) on delete cascade
);

create table BivariateChecks (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    check_name text not null,
    check_result real not null,
    series_x_id text not null,
    series_y_id text not null,

    unique(flow_execution_id, check_name, series_x_id, series_y_id),
    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table BivariateCheck_EventFrame (
    id integer primary key autoincrement,
    series_x_id text not null,
    series_y_id text not null,
    event_frame_id integer not null,

    foreign key (event_frame_id) references EventFrames(id) on delete cascade
);

create table FilterBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    augmentation_strategy text not null,
    frame_type_category text not null,
    frame_type text not null,
    series_id text,

    foreign key (block_id) references Blocks(id) on delete cascade
);

create table FilterBlockOutput (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);

create table OutputBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    output text not null,

    foreign key (block_id) references Blocks(id) on delete cascade
);

create table Scores (
    id integer primary key autoincrement,
    flow_execution_id integer not null,
    series_id text,
    score_name text not null,
    score float not null,

    foreign key (flow_execution_id) references FlowExecutions(id) on delete cascade
);
