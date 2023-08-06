-- depends: 030__remove_filter_output

create table UnivariateEventFrames (
    id integer primary key autoincrement,
    series_source text not null,
    series_id text not null,
    block_evaluation_id integer not null,

    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,

    unique (block_evaluation_id, series_id, type, start_date)
);

insert into UnivariateEventFrames (
    series_source, series_id, block_evaluation_id, type, start_date, end_date
)
select se.series_source, se.series_id, er.block_evaluation_id, e.type, e.start_date, max(e.end_date)
from Series_EventFrame se, EventFrames e, EventFrameReferences er
where se.event_frame_id = e.id and er.event_frame_id = e.id
group by er.block_evaluation_id, se.series_id, e.type, e.start_date;

create index univariate_event_frames_series_id on UnivariateEventFrames(series_id);
create index univariate_event_frames_be_id on UnivariateEventFrames(block_evaluation_id);

create index tmp_er_e_id on EventFrameReferences(event_frame_id);
create index tmp_bc_e_id on BivariateCheck_EventFrame(event_frame_id);
create index tmp_se_id on Series_EventFrame(event_frame_id);

delete from EventFrames where id in (select event_frame_id from Series_EventFrame);
drop table Series_EventFrame;

create table BivariateEventFrames (
    id integer primary key autoincrement,
    series_x_id text not null,
    series_y_id text not null,
    block_evaluation_id integer not null,

    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,

    unique (block_evaluation_id, series_x_id, series_y_id, type, start_date)
);

insert into BivariateEventFrames (
    series_x_id, series_y_id, block_evaluation_id, type, start_date, end_date
)
select be.series_x_id, be.series_y_id, er.block_evaluation_id, e.type, e.start_date, max(e.end_date)
from BivariateCheck_EventFrame be, EventFrames e, EventFrameReferences er
where be.event_frame_id = e.id and er.event_frame_id = e.id
group by er.block_evaluation_id, be.series_x_id, be.series_y_id, e.type, e.start_date;

create index bivariate_event_frames_be_id on BivariateEventFrames(block_evaluation_id);

delete from EventFrames where id in (select event_frame_id from BivariateCheck_EventFrame);
drop table BivariateCheck_EventFrame;

create table MultivariateEventFrames (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,

    type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,

    unique (block_evaluation_id, type, start_date)
);

insert into MultivariateEventFrames (
    block_evaluation_id, type, start_date, end_date
)
select er.block_evaluation_id, e.type, e.start_date, max(e.end_date)
from EventFrames e, EventFrameReferences er
where e.id = er.event_frame_id
group by er.block_evaluation_id, e.type, e.start_date ;

create index multivariate_event_frames_be_id on MultivariateEventFrames(block_evaluation_id);

drop table EventFrameReferences;
drop table EventFrames;
