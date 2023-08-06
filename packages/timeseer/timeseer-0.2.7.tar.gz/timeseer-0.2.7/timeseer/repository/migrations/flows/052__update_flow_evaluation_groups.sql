-- depends: 051__remove_foreign_keys

CREATE TABLE new_FlowEvaluationGroups (
    id integer primary key autoincrement,
    flow_id integer not null,
    start_date datetime not null,
    end_date datetime not null,
    evaluation_date datetime not null,

    foreign key (flow_id) references Flows(id) on delete cascade
);

insert into new_FlowEvaluationGroups (id, flow_id, start_date, end_date, evaluation_date)
select id, flow_id, start_date, end_date, evaluation_date from FlowEvaluationGroups;

drop table FlowEvaluationGroups;

alter table new_FlowEvaluationGroups rename to FlowEvaluationGroups;


