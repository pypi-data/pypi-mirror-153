-- depends: 001__create

alter table BackgroundJobs add column start_date datetime;
alter table BackgroundJobs add column end_date datetime;
