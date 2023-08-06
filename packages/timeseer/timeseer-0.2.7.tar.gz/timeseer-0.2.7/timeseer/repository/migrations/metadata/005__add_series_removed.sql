-- depends: 004__clear_metadata_table

alter table SeriesNames add column removed integer not null default 0
