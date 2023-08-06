-- depends: 025__block_configuration_ids

alter table Series add column state text not null default 'DONE'
