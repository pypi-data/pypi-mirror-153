-- depends: 002__add_flow_evaluation

create table Exports (
    id integer primary key autoincrement,
    flow_evaluation_id integer not null,
    filename text not null,
    file blob not null,
    date datetime not null,

    foreign key (flow_evaluation_id) references FlowEvaluation(id) on delete cascade
);
