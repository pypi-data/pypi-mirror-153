-- depends: 018__add_scheduled_flows

alter table EventFrames rename to EventFrames_old;
alter table Series_EventFrame rename to Series_EventFrame_old;
alter table BivariateCheck_EventFrame rename to BivariateCheck_EventFrame_old;

create table EventFrames (
    id integer primary key autoincrement,
    type text not null,
    start_date datetime not null,
    end_date datetime,
    last_modified_date datetime

);

create table Series_EventFrame (
    id integer primary key autoincrement,
    series_source text not null,
    series_id text not null,
    event_frame_id integer not null,

    foreign key (event_frame_id) references EventFrames(id) on delete cascade
);


create table BivariateCheck_EventFrame (
    id integer primary key autoincrement,
    series_x_id text not null,
    series_y_id text not null,
    event_frame_id integer not null,

    foreign key (event_frame_id) references EventFrames(id) on delete cascade
);

create table EventFrameReferences (
    id integer primary key autoincrement,
    event_frame_id integer not null,
    block_evaluation_id integer not null,

    unique(event_frame_id, block_evaluation_id)
    foreign key (event_frame_id) references EventFrames(id) on delete cascade,
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

insert into EventFrames (id, type, start_date, end_date, last_modified_date)
select id, type, start_date, end_date, DateTime('now') from EventFrames_old;

insert into EventFrameReferences (event_frame_id, block_evaluation_id)
select id, block_evaluation_id from EventFrames_old;

insert into Series_EventFrame
select * from Series_EventFrame_old;

insert into BivariateCheck_EventFrame
select * from BivariateCheck_EventFrame_old;

drop table EventFrames_old;
drop table Series_EventFrame_old;
drop table BivariateCheck_EventFrame_old;

