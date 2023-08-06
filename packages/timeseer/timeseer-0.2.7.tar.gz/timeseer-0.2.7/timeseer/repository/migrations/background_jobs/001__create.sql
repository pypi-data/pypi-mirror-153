create table BackgroundJobs (
    id integer primary key autoincrement,
    state text not null,
    name text not null,
    arguments text
);

create table BackgroundTasks (
    id integer primary key autoincrement,
    job_id integer not null,
    state text not null,
    name text not null,

    unique (job_id, name),
    foreign key (job_id) references BackgroundJobs(id) on delete cascade
);

create table BackgroundJobReferences (
    id integer primary key autoincrement,
    job_id integer not null,
    reference text not null,

    foreign key (job_id) references BackgroundJobs(id) on delete cascade
);
