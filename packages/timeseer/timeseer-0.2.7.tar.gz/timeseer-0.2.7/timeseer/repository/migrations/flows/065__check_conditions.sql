-- depends: 064__bad_actor_state

create table CheckConditionMessages(
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id integer not null,
    check_name text not null,
    message text not null, 

    unique(block_evaluation_id, series_id, check_name),
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);