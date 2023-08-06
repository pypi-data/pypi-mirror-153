-- depends: 059__kpi_sets

create table UnivariateSeriesState (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    flow_evaluation_series_id integer not null,

    unique(block_evaluation_id, flow_evaluation_series_id),
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (flow_evaluation_series_id) references Series(id) on delete cascade
);

insert into UnivariateSeriesState (block_evaluation_id, flow_evaluation_series_id)
select b.id, s.id
from BlockEvaluations b, Series s
where b.flow_evaluation_id = s.flow_evaluation_id
  and b.type = 'UNIVARIATE_ANALYSIS'
  and s.state = 'DONE';

create index series_state_be_id on UnivariateSeriesState(block_evaluation_id);
