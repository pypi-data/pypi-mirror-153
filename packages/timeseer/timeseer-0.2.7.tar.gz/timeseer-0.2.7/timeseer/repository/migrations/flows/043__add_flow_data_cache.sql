-- depends: 042__update_filters

alter table Flows add column data_cache text not null default 'yes';

update Flows set data_cache = 'no' where id in (select flow_id from Blocks group by flow_id having count(*) = 1);
