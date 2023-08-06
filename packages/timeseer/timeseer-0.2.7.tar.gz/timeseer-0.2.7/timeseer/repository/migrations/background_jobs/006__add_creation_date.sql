-- depends: 005__add_unique_constraints

alter table BackgroundJobs add column creation_date datetime;
alter table BackgroundJobs add column error text;
