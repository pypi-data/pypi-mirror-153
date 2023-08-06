-- depends: 012__add_report_block

create table SeriesSetReferences (
    id integer primary key autoincrement,
    flow_id integer not null,
    series_set_id integer not null,

    foreign key (flow_id) references Flows(id) on delete cascade,
    unique (flow_id, series_set_id)
);

create table Series (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    series_id text not null,

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade,
    unique (flow_evaluation_id, series_id)
);

create index series_fe_id on Series(flow_evaluation_id);

insert into SeriesSetReferences (flow_id, series_set_id)
select b.flow_id, s.series_set_id
from SeriesSetBlockInput s, BlockConfigurations c, Blocks b
where c.type = 'SERIES_SET' and c.id = s.block_id and b.configuration_id = c.id;

insert into Series (flow_evaluation_id, series_id)
select b.flow_evaluation_id, s.series_id
from BlockEvaluations b, SeriesSetBlockOutput s
where s.block_evaluation_id = b.id;

delete from Blocks
where configuration_id in (
    select id from BlockConfigurations where type = 'SERIES_SET'
);

drop index seriesset_output_fe_id;

delete from BlockConfigurations where type = 'SERIES_SET';

drop table SeriesSetBlockInput;
drop table SeriesSetBlockOutput;
