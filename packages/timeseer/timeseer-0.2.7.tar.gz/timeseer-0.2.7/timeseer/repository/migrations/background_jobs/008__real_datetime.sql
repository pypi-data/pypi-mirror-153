-- depends: 007__add_error_tasks

update BackgroundJobs set start_date = cast(strftime('%s', start_date) as real);
update BackgroundJobs set end_date = cast(strftime('%s', end_date) as real);
update BackgroundJobs set creation_date = cast(strftime('%s', creation_date) as real);
