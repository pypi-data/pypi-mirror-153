-- depends: 033__real_datetime

create table WeightSetReference(
    id integer primary key autoincrement,
    flow_id integer not null,
    weight_set_id integer not null,

    foreign key (flow_id) references Flows(id) on delete cascade
);
