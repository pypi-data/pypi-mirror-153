-- depends: 032__foreign_keys

create index series_series_id on Series(flow_evaluation_id, series_id);

create table EventFrameTypes (
    id integer primary key autoincrement,
    name text not null,

    unique (name)
);

insert into EventFrameTypes (name)
select distinct type
from UnivariateEventFrames;

insert into EventFrameTypes (name)
select distinct type
from BivariateEventFrames where true
on conflict do nothing;

insert into EventFrameTypes (name)
select distinct type
from MultivariateEventFrames where true
on conflict do nothing;

-- univariate event frames
alter table UnivariateEventFrames rename to UnivariateEventFrames_old;

drop index univariate_event_frames_series_id;
drop index univariate_event_frames_be_id;

create table UnivariateEventFrames (
    id integer primary key autoincrement,
    flow_evaluation_series_id integer not null,
    block_evaluation_id integer not null,

    type_id integer not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (flow_evaluation_series_id) references Series(id) on delete no action,
    foreign key (type_id) references EventFrameTypes(id) on delete no action,

    unique (block_evaluation_id, flow_evaluation_series_id, type_id, start_date)
);

insert or ignore into UnivariateEventFrames (
    flow_evaluation_series_id, block_evaluation_id, type_id, start_date, end_date
)
select
    (select id from Series s
        where s.series_id = o.series_id
          and s.flow_evaluation_id = (
            select flow_evaluation_id from BlockEvaluations b where b.id = o.block_evaluation_id)
          ) as new_series_id,
    block_evaluation_id,
    (select id from EventFrameTypes where name = type),
    cast(strftime('%s', start_date) as real) + cast(substr(strftime('%f', start_date), 3) as real),
    cast(strftime('%s', end_date) as real) + cast(substr(strftime('%f', end_date), 3) as real)
from UnivariateEventFrames_old o where new_series_id is not null;

drop table UnivariateEventFrames_old;

create index univariate_event_frames_series_id on UnivariateEventFrames(flow_evaluation_series_id);
create index univariate_event_frames_be_id on UnivariateEventFrames(block_evaluation_id);
create index univariate_event_frames_type_block on UnivariateEventFrames(type_id, block_evaluation_id);

-- bivariate event frames
alter table BivariateEventFrames rename to BivariateEventFrames_old;

create table BivariateEventFrames (
    id integer primary key autoincrement,
    flow_evaluation_series_x_id text not null,
    flow_evaluation_series_y_id text not null,
    block_evaluation_id integer not null,

    type_id integer not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (type_id) references EventFrameTypes(id) on delete no action,
    foreign key (flow_evaluation_series_x_id) references Series(id) on delete no action,
    foreign key (flow_evaluation_series_y_id) references Series(id) on delete no action,

    unique (block_evaluation_id, flow_evaluation_series_x_id, flow_evaluation_series_y_id, type_id, start_date)
);

insert or ignore into BivariateEventFrames (
    flow_evaluation_series_x_id, flow_evaluation_series_y_id, block_evaluation_id, type_id, start_date, end_date
)
select
    (select id from Series s
        where s.series_id = o.series_x_id
          and s.flow_evaluation_id = (
            select flow_evaluation_id from BlockEvaluations b where b.id = o.block_evaluation_id)
          ) as new_series_x_id,
    (select id from Series s
        where s.series_id = o.series_y_id
          and s.flow_evaluation_id = (
            select flow_evaluation_id from BlockEvaluations b where b.id = o.block_evaluation_id)
          ) as new_series_y_id,
    block_evaluation_id,
    (select id from EventFrameTypes where name = type),
    cast(strftime('%s', start_date) as real) + cast(substr(strftime('%f', start_date), 3) as real),
    cast(strftime('%s', end_date) as real) + cast(substr(strftime('%f', end_date), 3) as real)
from BivariateEventFrames_old o where new_series_x_id is not NULL and new_series_y_id is not NULL;

drop table BivariateEventFrames_old;

create index bivariate_event_frames_be_id on BivariateEventFrames(block_evaluation_id);

-- multivariate event frames
alter table MultivariateEventFrames rename to MultivariateEventFrames_old;

create table MultivariateEventFrames (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,

    type_id integer not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (type_id) references EventFrameTypes(id) on delete no action,

    unique (block_evaluation_id, type_id, start_date)
);

insert or ignore into MultivariateEventFrames (
    block_evaluation_id, type_id, start_date, end_date
)
select
    block_evaluation_id,
    (select id from EventFrameTypes where name = type),
    cast(strftime('%s', start_date) as real) + cast(substr(strftime('%f', start_date), 3) as real),
    cast(strftime('%s', end_date) as real) + cast(substr(strftime('%f', end_date), 3) as real)
from MultivariateEventFrames_old;

drop table MultivariateEventFrames_old;

create index multivariate_event_frames_be_id on MultivariateEventFrames(block_evaluation_id);

-- others
update Flows set start_date = cast(strftime('%s', start_date) as real);
update Flows set end_date = cast(strftime('%s', end_date) as real);

update Exports set "date" = cast(strftime('%s', "date") as real);

update ComparisonBlockInput set reference_start_date = cast(strftime('%s', reference_start_date) as real);
update ComparisonBlockInput set reference_end_date = cast(strftime('%s', reference_end_date) as real);

update FlowEvaluationGroups set start_date = cast(strftime('%s', start_date) as real);
update FlowEvaluationGroups set end_date = cast(strftime('%s', end_date) as real);
update FlowEvaluationGroups set evaluation_date = cast(strftime('%s', evaluation_date) as real);

-- trigger vacuum
create table if not exists RunVacuum(id integer primary key autoincrement);
