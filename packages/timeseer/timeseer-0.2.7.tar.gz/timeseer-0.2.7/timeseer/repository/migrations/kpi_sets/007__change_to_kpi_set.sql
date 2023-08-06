-- depends: 006__favorite_kpi

alter table WeightSets rename to KPISets;
alter table WeightSetKPIs rename column weight_set_id to kpi_set_id;
alter table WeightSetKPIs rename to KPISetKPIs;