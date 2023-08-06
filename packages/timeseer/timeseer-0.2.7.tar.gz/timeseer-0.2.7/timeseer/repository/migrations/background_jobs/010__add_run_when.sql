-- depends: 009__remove_planning

alter table BackgroundJobs add column run_when text not null default 'NORMAL';
