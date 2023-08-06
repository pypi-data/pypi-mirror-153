-- depends: 003__series_set_discovery

alter table BackgroundJobDependency rename to old_BackgroundJobDependency;

create table BackgroundJobDependency (
    id integer primary key autoincrement,
    job_id integer not null,
    dependent_job integer not null,

    unique(job_id, dependent_job),
    foreign key (job_id) references BackgroundJobs(id) on delete cascade
);

insert into BackgroundJobDependency select * from old_BackgroundJobDependency;

drop table old_BackgroundJobDependency;
