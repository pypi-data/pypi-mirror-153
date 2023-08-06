-- depends: 003__series_set_discovery

create table BackgroundJobDependency (
    id integer primary key autoincrement,
    job_id integer not null,
    dependent_job integer not null,

    foreign key (job_id) references BackgroundJobs(id) on delete cascade
);
