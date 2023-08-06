-- depends: 005__soft_delete

alter table WeightSetKPIs add column favorite integer not null default 0;
