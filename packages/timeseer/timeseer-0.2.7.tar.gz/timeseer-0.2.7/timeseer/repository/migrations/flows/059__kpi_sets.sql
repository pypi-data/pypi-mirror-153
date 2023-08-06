-- depends: 058__remove_constraint_kpi_score

alter table WeightSetReference rename column weight_set_id to kpi_set_id;
alter table WeightSetReference rename to KPISetReference;
