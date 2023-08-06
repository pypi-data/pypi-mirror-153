-- depends: 010__add_run_when

create table WebhookCallbacks(
    id integer primary key autoincrement,
    url text not null
);

create table BackgroundJobCallbacks(
    id integer primary key autoincrement,
    job_id integer not null,
    callback_id integer not null,

    unique(job_id, callback_id),
    foreign key (job_id) references BackgroundJobs(id) on delete cascade,
    foreign key (callback_id) references WebhookCallbacks(id) on delete cascade
);