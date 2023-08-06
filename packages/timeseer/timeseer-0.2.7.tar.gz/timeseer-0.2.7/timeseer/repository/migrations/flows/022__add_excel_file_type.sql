-- depends: 021__drop_score_table

alter table Exports add column file_type text default 'excel';

