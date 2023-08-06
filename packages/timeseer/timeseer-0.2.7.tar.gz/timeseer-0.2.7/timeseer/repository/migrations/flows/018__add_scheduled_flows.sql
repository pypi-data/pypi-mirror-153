-- depends: 017__add_block_configuration_name

alter table Flows add column schedule_interval text;
